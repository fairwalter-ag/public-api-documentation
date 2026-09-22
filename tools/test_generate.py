"""Tests for the generator and the publish gate.

Run from the repository root:  python3 -m unittest discover -s tools

The snapshot test regenerates the repository from the committed `openapi.json` and
compares it against the committed Markdown, so a change in rendering shows up as a
failing test until the output is regenerated with `python3 tools/publish.py`.
"""

from __future__ import annotations

import json
import pathlib
import re
import unittest

import generate

ROOT = pathlib.Path(__file__).resolve().parent.parent
SPEC = json.loads((ROOT / "openapi.json").read_text())


def spec_with(operation_count: int) -> dict:
    return {
        "openapi": "3.0.0",
        "paths": {f"/thing/{i}": {"get": {"operationId": f"getThing{i}"}} for i in range(operation_count)},
    }


class ValidateTest(unittest.TestCase):
    def test_refuses_html(self):
        self.assertIn("not JSON", generate.validate("<html><body>Maintenance</body></html>", SPEC))

    def test_refuses_json_that_is_not_openapi(self):
        self.assertIn("not an OpenAPI document", generate.validate('{"status": "ok"}', SPEC))

    def test_refuses_openapi_document_without_operations(self):
        self.assertIn("zero operations", generate.validate(json.dumps({"openapi": "3.0.0", "paths": {}}), SPEC))

    def test_refuses_operation_count_dropping_past_the_threshold(self):
        baseline = spec_with(100)
        reason = generate.validate(json.dumps(spec_with(79)), baseline)
        self.assertIsNotNone(reason)
        self.assertIn("79", reason)

    def test_accepts_operation_count_dropping_just_under_the_threshold(self):
        self.assertIsNone(generate.validate(json.dumps(spec_with(80)), spec_with(100)))

    def test_accepts_the_live_document_without_a_baseline(self):
        self.assertIsNone(generate.validate(json.dumps(SPEC), None))

    def test_accepts_the_committed_document_against_itself(self):
        self.assertIsNone(generate.validate(json.dumps(SPEC), SPEC))


class GenerateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = generate.generate(SPEC)

    def test_output_matches_the_committed_repository(self):
        committed = {str(p.relative_to(ROOT)) for p in ROOT.glob("reference/*.md")}
        committed |= {"README.md", "llms.txt", "llms-full.txt"}
        self.assertEqual(committed, set(self.files))
        for path, content in self.files.items():
            with self.subTest(path=path):
                self.assertEqual(
                    (ROOT / path).read_text(),
                    content,
                    f"{path} is stale — run `python3 tools/publish.py` to regenerate",
                )

    def test_list_endpoint_documents_its_search_filter_and_sort_keys(self):
        page = self.files["reference/account.md"]
        self.assertIn("- **Searchable (`q`):** number, label", page)
        self.assertIn("- **Filterable:** `filter[category]`", page)
        self.assertIn("- **Sortable:** `number`, `id`", page)

    def test_list_endpoint_documents_its_page_size(self):
        self.assertIn("- **Page size:** default `30`, maximum `100`", self.files["reference/account.md"])
        self.assertIn("maximum `500`", self.files["reference/booking.md"])

    def test_every_resource_page_carries_a_json_example_that_parses(self):
        for path, content in self.files.items():
            if not path.startswith("reference/"):
                continue
            blocks = re.findall(r"```json\n(.*?)\n```", content, re.S)
            with self.subTest(path=path):
                self.assertTrue(blocks, f"{path} has no example response")
                for block in blocks:
                    json.loads(block)

    def test_list_example_uses_the_envelope_and_the_detail_example_does_not(self):
        blocks = re.findall(r"```json\n(.*?)\n```", self.files["reference/account.md"], re.S)
        listed, detail = json.loads(blocks[0]), json.loads(blocks[1])
        self.assertEqual(["data", "meta"], list(listed))
        self.assertEqual({"limit": 30, "offset": 0, "total": 1, "hasMore": False}, listed["meta"]["pagination"])
        self.assertNotIn("data", detail)
        self.assertEqual(listed["data"][0], detail)

    def test_field_table_links_resolve_to_a_schema_heading(self):
        for path, content in self.files.items():
            if not path.startswith("reference/"):
                continue
            headings = {generate.anchor(h) for h in re.findall(r"^### (.+)$", content, re.M)}
            with self.subTest(path=path):
                for link in set(re.findall(r"\]\(#([a-z0-9-]+)\)", content)):
                    self.assertIn(link, headings, f"{path} links to #{link} with no matching schema heading")

    def test_llms_index_references_every_generated_page(self):
        index = self.files["llms.txt"]
        for path in self.files:
            if path.startswith("reference/"):
                self.assertIn(f"({path})", index)
        self.assertIn("(README.md)", index)
        self.assertIn("(openapi.json)", index)

    def test_llms_full_contains_the_readme_and_every_page(self):
        full = self.files["llms-full.txt"]
        for path, content in self.files.items():
            if path.startswith("reference/") or path == "README.md":
                self.assertIn(content.strip(), full)

    def test_readme_carries_the_api_description_prose(self):
        readme = self.files["README.md"]
        self.assertIn(SPEC["info"]["description"].strip(), readme)
        self.assertIn(generate.SCALAR_URL, readme)
        self.assertIn("CC BY 4.0", readme)

    def test_every_operation_of_the_spec_is_documented(self):
        pages = "\n".join(content for path, content in self.files.items() if path.startswith("reference/"))
        for entry in generate.operations(SPEC):
            self.assertIn(f"`{entry['op']['operationId']}`", pages)


if __name__ == "__main__":
    unittest.main()
