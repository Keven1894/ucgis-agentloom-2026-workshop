#!/usr/bin/env python3
"""test_mcp_kg_tools.py — operator smoke test for kg_index (no Cline required).

Run from repo root:
    python scripts/test_mcp_kg_tools.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from scripts.kg.kg_index import get_index  # noqa: E402


def main() -> int:
    idx = get_index()
    errors: list[str] = []

    print("=== kg_search: iso 3166 ===")
    hits = idx.search("iso 3166", limit=5, role="domain")
    print(json.dumps(hits, indent=2))
    if not hits:
        errors.append("kg_search('iso 3166') returned 0 hits")
    elif not any("iso3166" in (h.get("title") or "").lower() or "3166" in (h.get("description_preview") or "") for h in hits):
        # accept pending proposal hits from Wave C
        if not any(h.get("status") == "pending_proposal" for h in hits):
            errors.append("kg_search('iso 3166') had no domain-relevant hits")

    print("\n=== kg_get_node: knowledge:domain:root ===")
    root = idx.get_node("knowledge:domain:root")
    if root is None:
        errors.append("kg_get_node knowledge:domain:root not found")
    else:
        print(json.dumps({k: root[k] for k in ("id", "title", "role", "path")}, indent=2))

    print("\n=== kg_list_proposals ===")
    props = idx.list_proposals()
    print(json.dumps({"count": len(props), "first": props[:2]}, indent=2))

    print("\n=== kg_search: catalog storytelling (builder) ===")
    hits2 = idx.search("catalog storytelling", limit=3, role="builder")
    print(json.dumps(hits2, indent=2))
    if not hits2:
        errors.append("kg_search catalog storytelling (builder) returned 0 hits")

    if errors:
        print("\nFAIL:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print("\nPASS — kg_index smoke test OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
