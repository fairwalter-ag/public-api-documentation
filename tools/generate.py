"""Turn the Fairwalter public OpenAPI document into the files of this repository.

Two pure functions over data, no network, no filesystem, no git:

    validate(raw_text, baseline_spec) -> refusal reason or None
    generate(spec)                    -> {relative path: file content}

tools/publish.py is the glue that fetches, writes and lets the workflow commit.
"""

from __future__ import annotations

import json
import re

SCALAR_URL = "https://my.fairwalter.ch/public-api/docs"
SPEC_URL = "https://my.fairwalter.ch/public-api/docs.json"
MIN_OPERATION_RATIO = 0.8
INLINE_ENUM_MAX = 12
METHODS = ("get", "post", "put", "patch", "delete", "head", "options")


# --------------------------------------------------------------------------- validate


def validate(raw: str, baseline: dict | None) -> str | None:
    """Return a refusal reason, or None when the fetched document may be published."""
    try:
        spec = json.loads(raw)
    except (ValueError, TypeError):
        return "response is not JSON (a maintenance page or an error page?)"

    if not isinstance(spec, dict) or "openapi" not in spec or not isinstance(spec.get("paths"), dict):
        return "response is JSON but not an OpenAPI document (no `openapi` key, or no `paths` object)"

    count = len(operations(spec))
    if count == 0:
        return "document declares zero operations"

    if baseline is not None:
        previous = len(operations(baseline))
        if previous and count < previous * MIN_OPERATION_RATIO:
            return f"operation count fell from {previous} to {count}, past the {int((1 - MIN_OPERATION_RATIO) * 100)}% threshold"

    return None


def operations(spec: dict) -> list[dict]:
    """Every operation as {path, method, op}, in document order."""
    out = []
    for path, item in (spec.get("paths") or {}).items():
        if not isinstance(item, dict):
            continue
        for method, op in item.items():
            if method in METHODS and isinstance(op, dict):
                out.append({"path": path, "method": method, "op": op})
    return out


# --------------------------------------------------------------------------- helpers


def slug(name: str) -> str:
    name = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "-", name)
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def anchor(name: str) -> str:
    """The in-page link GitHub derives from a `### Name` heading."""
    return re.sub(r"[^a-z0-9-]", "", name.lower())


def cell(text: str) -> str:
    return re.sub(r"\s+", " ", str(text)).replace("|", "\\|").strip()


def deref(schema: dict, spec: dict) -> dict:
    """Resolve a $ref (and the `oneOf: [$ref]` shape nelmio emits for nullable enums)."""
    seen = set()
    while isinstance(schema, dict):
        ref = schema.get("$ref")
        if ref and ref not in seen:
            seen.add(ref)
            schema = spec.get("components", {}).get("schemas", {}).get(ref.rsplit("/", 1)[-1], {})
            continue
        one_of = schema.get("oneOf")
        if one_of and len(one_of) == 1:
            schema = {**{k: v for k, v in schema.items() if k != "oneOf"}, **one_of[0]}
            continue
        break
    return schema if isinstance(schema, dict) else {}


def ref_name(schema: dict) -> str | None:
    """The component name a property points at, directly or through a single-item oneOf."""
    if not isinstance(schema, dict):
        return None
    ref = schema.get("$ref")
    if not ref and len(schema.get("oneOf") or []) == 1:
        ref = schema["oneOf"][0].get("$ref")
    return ref.rsplit("/", 1)[-1] if ref else None


def type_label(schema: dict, spec: dict) -> str:
    """Human type for the field table, linking named schemas to their appendix entry."""
    name = ref_name(schema)
    target = deref(schema, spec)

    if target.get("type") == "array":
        return type_label(target.get("items") or {}, spec) + "[]"

    if name:
        label = f"[{name}](#{anchor(name)})"
    else:
        label = target.get("type", "object")
        if target.get("format"):
            label += f" ({target['format']})"
        values = target.get("enum")
        if values:
            label = (
                f"{target.get('type', 'string')}: " + " \\| ".join(f"`{v}`" for v in values)
                if len(values) <= INLINE_ENUM_MAX
                else f"{target.get('type', 'string')} enum ({len(values)} values)"
            )

    if schema.get("nullable") or target.get("nullable"):
        label += " · nullable"
    return label


def referenced(schema: dict, spec: dict, found: list[str] | None = None) -> list[str]:
    """Component schema names reachable from `schema`, in first-seen order."""
    found = [] if found is None else found
    name = ref_name(schema)
    target = deref(schema, spec)
    if name:
        if name in found:
            return found
        found.append(name)
    for child in list((target.get("properties") or {}).values()) + ([target["items"]] if "items" in target else []):
        referenced(child, spec, found)
    return found


def example(schema: dict, spec: dict, stack: tuple[str, ...] = ()) -> object:
    """Synthesise an example value: each field's own `example` where present, a placeholder otherwise."""
    name = ref_name(schema)
    if name and name in stack:
        return None
    target = deref(schema, spec)
    stack = stack + ((name,) if name else ())

    for source in (schema, target):
        if "example" in source:
            return source["example"]

    if target.get("enum"):
        return target["enum"][0]

    kind = target.get("type") or ("object" if "properties" in target else "string")
    if kind == "object":
        return {key: example(value, spec, stack) for key, value in (target.get("properties") or {}).items()}
    if kind == "array":
        item = example(target.get("items") or {}, spec, stack)
        return [item] if item is not None else []
    if kind == "integer":
        return 1
    if kind == "number":
        return 1.0
    if kind == "boolean":
        return True
    fmt = target.get("format")
    return {"date": "2025-01-31", "date-time": "2025-01-31T09:00:00+01:00"}.get(fmt, "string")


def success_schema(op: dict) -> dict:
    return ((op.get("responses") or {}).get("200") or {}).get("content", {}).get("application/json", {}).get("schema") or {}


def row_schema(op: dict) -> dict:
    """The resource schema of an operation: the list envelope's item, or the detail body itself."""
    schema = success_schema(op)
    data = (schema.get("properties") or {}).get("data")
    return (data or {}).get("items") or {} if data else schema


def is_list(op: dict) -> bool:
    return "data" in (success_schema(op).get("properties") or {})


# --------------------------------------------------------------------------- markdown


def parameter_table(op: dict, spec: dict) -> list[str]:
    params = op.get("parameters") or []
    if not params:
        return []
    lines = ["| Parameter | In | Type | Required | Description |", "| --- | --- | --- | --- | --- |"]
    for param in params:
        schema = param.get("schema") or {}
        extra = []
        if "default" in schema:
            extra.append(f"Default `{schema['default']}`.")
        if "maximum" in schema:
            extra.append(f"Maximum `{schema['maximum']}`.")
        if len(schema.get("enum") or []) > INLINE_ENUM_MAX:
            extra.append("One of: " + ", ".join(f"`{v}`" for v in schema["enum"]) + ".")
        description = " ".join([param.get("description", "")] + extra)
        lines.append(
            f"| `{cell(param.get('name', ''))}` | {param.get('in', '')} | {type_label(schema, spec)} "
            f"| {'yes' if param.get('required') else ''} | {cell(description)} |"
        )
    return lines + [""]


def capabilities(op: dict) -> list[str]:
    """Searchable, filterable and sortable keys plus page sizes, read off the parameters."""
    params = {p.get("name"): p for p in (op.get("parameters") or []) if isinstance(p, dict)}
    lines = []

    search = params.get("q")
    if search:
        fields = re.sub(r"^Free-text search across:\s*", "", search.get("description", "")).split(".")[0]
        lines.append(f"- **Searchable (`q`):** {cell(fields)}")

    filters = []
    for name, param in params.items():
        if not str(name).startswith("filter["):
            continue
        values = (param.get("schema") or {}).get("enum")
        filters.append(f"`{name}`" + (f" ({', '.join(f'`{v}`' for v in values)})" if values else ""))
    if filters:
        lines.append(f"- **Filterable:** {', '.join(filters)}")

    sort = params.get("sort")
    if sort:
        keys = [v for v in ((sort.get("schema") or {}).get("enum") or []) if not str(v).startswith("-")]
        if keys:
            lines.append(f"- **Sortable:** {', '.join(f'`{k}`' for k in keys)} (prefix `-` for descending)")

    limit = (params.get("limit") or {}).get("schema") or {}
    if limit:
        lines.append(f"- **Page size:** default `{limit.get('default')}`, maximum `{limit.get('maximum')}`")

    return ["**List capabilities**", ""] + lines + [""] if lines else []


def response_table(op: dict) -> list[str]:
    lines = ["| Status | Description |", "| --- | --- |"]
    for status, response in (op.get("responses") or {}).items():
        lines.append(f"| `{status}` | {cell((response or {}).get('description', ''))} |")
    return lines + [""]


def schema_section(name: str, spec: dict) -> list[str]:
    schema = spec.get("components", {}).get("schemas", {}).get(name) or {}
    lines = [f"### {name}", ""]

    if schema.get("enum"):
        lines += [schema.get("description", "").strip() or f"String enum, {len(schema['enum'])} values.", ""]
        lines += [", ".join(f"`{v}`" for v in schema["enum"]), ""]
        return lines

    if schema.get("description"):
        lines += [schema["description"].strip(), ""]

    required = set(schema.get("required") or [])
    lines += ["| Field | Type | Required | Description |", "| --- | --- | --- | --- |"]
    for field, value in (schema.get("properties") or {}).items():
        lines.append(
            f"| `{field}` | {type_label(value, spec)} | {'yes' if field in required else ''} "
            f"| {cell(deref(value, spec).get('description', '') if 'description' not in value else value['description'])} |"
        )
    return lines + [""]


def resource_page(tag: str, tag_description: str, ops: list[dict], spec: dict) -> str:
    lines = [f"# {tag}", ""]
    if tag_description and tag_description.strip() != tag:
        lines += [tag_description.strip(), ""]

    lines += ["| Method | Path | Operation | Summary |", "| --- | --- | --- | --- |"]
    for entry in ops:
        op = entry["op"]
        lines.append(
            f"| {entry['method'].upper()} | `{entry['path']}` | `{op.get('operationId', '')}` | {cell(op.get('summary', ''))} |"
        )
    lines.append("")

    schemas: list[str] = []
    for entry in ops:
        op, path = entry["op"], entry["path"]
        lines += [f"## {entry['method'].upper()} {path}", ""]
        if op.get("summary"):
            lines += [f"**{op['summary'].strip()}** — `{op.get('operationId', '')}`", ""]
        if op.get("description"):
            lines += [op["description"].strip(), ""]

        lines += parameter_table(op, spec)
        lines += capabilities(op)

        row = row_schema(op)
        name = ref_name(row)
        if name:
            envelope = "a list envelope around" if is_list(op) else ""
            lines += [f"**Response** — `200` returns {envelope} [{name}](#{anchor(name)}).".replace("  ", " "), ""]
        lines += response_table(op)

        body = success_schema(op)
        if body:
            sample = example(body, spec)
            if is_list(op):
                limit = next((p.get("schema", {}).get("default") for p in (op.get("parameters") or []) if p.get("name") == "limit"), 30)
                sample = {"data": [example(row, spec)], "meta": {"pagination": {"limit": limit, "offset": 0, "total": 1, "hasMore": False}}}
            lines += ["**Example response**", "", "```json", json.dumps(sample, indent=2, ensure_ascii=False), "```", ""]

        for found in referenced(body, spec):
            if found not in schemas:
                schemas.append(found)

    if schemas:
        lines += ["## Schemas", ""]
        for name in schemas:
            lines += schema_section(name, spec)

    return "\n".join(lines).rstrip() + "\n"


def readme(spec: dict, pages: dict[str, str]) -> str:
    info = spec.get("info") or {}
    lines = [
        f"# {info.get('title', 'Public API')}",
        "",
        f"Reference documentation for the read-only Fairwalter public API, version `{info.get('version', '')}`.",
        "",
        "This repository is generated once a day from the live specification at "
        f"[`{SPEC_URL}`]({SPEC_URL}). Everything below is produced from it — nothing here is written by hand, "
        "and the commit history is the changelog of the API.",
        "",
        "- [`openapi.json`](openapi.json) — the OpenAPI 3 document, committed verbatim. Point a client generator at it.",
        "- [`reference/`](reference/) — one page per resource: endpoints, parameters, field tables and an example response.",
        "- [`llms.txt`](llms.txt) / [`llms-full.txt`](llms-full.txt) — the same reference in one file, for handing to an assistant.",
        f"- [Interactive API console]({SCALAR_URL}) — execute a request against your own data (sign-in required).",
        "",
        "## Resources",
        "",
    ]
    for path in sorted(pages):
        lines.append(f"- [{pages[path]}]({path})")
    lines += ["", "---", "", (info.get("description") or "").strip(), ""]
    lines += [
        "---",
        "",
        "## About this repository",
        "",
        "Every file here except `tools/` and `.github/` is generated by "
        "[`tools/publish.py`](tools/publish.py) from the live specification — edit the API, not the Markdown.",
        "",
        "This documentation is licensed under [CC BY 4.0](LICENSE). Attribution to Fairwalter AG is required.",
        "",
    ]
    return "\n".join(lines)


def generate(spec: dict) -> dict[str, str]:
    """The whole repository content (except openapi.json, which is copied verbatim) as {path: content}."""
    descriptions = {t.get("name"): t.get("description", "") for t in (spec.get("tags") or []) if isinstance(t, dict)}

    grouped: dict[str, list[dict]] = {}
    for entry in operations(spec):
        tag = (entry["op"].get("tags") or ["Other"])[0]
        grouped.setdefault(tag, []).append(entry)

    order = [t for t in descriptions if t in grouped] + [t for t in grouped if t not in descriptions]

    files: dict[str, str] = {}
    titles: dict[str, str] = {}
    for tag in order:
        ops = sorted(grouped[tag], key=lambda e: not str(e["op"].get("operationId", "")).startswith("list"))
        path = f"reference/{slug(tag)}.md"
        files[path] = resource_page(tag, descriptions.get(tag, ""), ops, spec)
        titles[path] = tag

    files["README.md"] = readme(spec, titles)

    title = (spec.get("info") or {}).get("title", "Public API")
    index = [
        f"# {title}",
        "",
        "> Read-only REST API for Swiss property management data: portfolio, occupancy, files and the general ledger. "
        "Generated daily from the live OpenAPI document.",
        "",
        "## Reference",
        "",
        "- [README](README.md): authentication, resource model, modes, pagination, errors and the accounting contract.",
    ]
    index += [f"- [{titles[p]}]({p}): {p.split('/')[-1][:-3]} endpoints and fields." for p in sorted(titles)]
    index += ["", "## Optional", "", "- [openapi.json](openapi.json): the machine-readable specification.", ""]
    files["llms.txt"] = "\n".join(index)

    full = [files["README.md"]] + [files[p] for p in sorted(titles)]
    files["llms-full.txt"] = "\n\n".join(part.strip() for part in full) + "\n"

    return files
