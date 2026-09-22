"""Fetch the live OpenAPI document, validate it, write this repository's files.

Exits non-zero (and writes nothing) when the fetched document is refused, so the
scheduled job goes red instead of publishing garbage. Committing is the workflow's job.
"""

from __future__ import annotations

import json
import pathlib
import sys
import urllib.request

from generate import SPEC_URL, generate, validate

ROOT = pathlib.Path(__file__).resolve().parent.parent
SPEC_FILE = ROOT / "openapi.json"


def main() -> int:
    request = urllib.request.Request(SPEC_URL, headers={"Accept": "application/json", "User-Agent": "fairwalter-public-api-docs"})
    raw = urllib.request.urlopen(request, timeout=60).read().decode("utf-8")

    baseline = json.loads(SPEC_FILE.read_text()) if SPEC_FILE.exists() else None
    reason = validate(raw, baseline)
    if reason is not None:
        print(f"Refused to publish {SPEC_URL}: {reason}", file=sys.stderr)
        return 1

    files = generate(json.loads(raw))
    files["openapi.json"] = raw if raw.endswith("\n") else raw + "\n"

    for stale in sorted((ROOT / "reference").glob("*.md")):
        if str(stale.relative_to(ROOT)) not in files:
            stale.unlink()
            print(f"removed {stale.relative_to(ROOT)}")

    for path, content in sorted(files.items()):
        target = ROOT / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    print(f"wrote {len(files)} files from {SPEC_URL}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
