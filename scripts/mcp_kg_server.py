#!/usr/bin/env python3
"""mcp_kg_server.py — read-only MCP server for AgentLoom KG access (W2).

Tools (stdio transport):
  kg_search       — keyword search over KG nodes + markdown bodies
  kg_get_node     — fetch one node by id + linked markdown
  kg_list_proposals — pending proposals queue

Run:
    python scripts/mcp_kg_server.py
    make mcp

Logging goes to stderr only (stdout is JSON-RPC).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# Ensure repo root is importable when launched as a script.
_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from mcp.server.fastmcp import FastMCP  # noqa: E402

from scripts.kg.kg_index import get_index  # noqa: E402

mcp = FastMCP(
    "agentloom-kg",
    instructions=(
        "Read-only AgentLoom knowledge graph tools. "
        "Use kg_search before proposing nodes. "
        "Mutations: shell out to python scripts/kg/propose_node.py only; "
        "never accept proposals yourself."
    ),
)


@mcp.tool(name="kg_search")
def kg_search(
    query: str,
    limit: int = 5,
    role: str | None = None,
    track: str | None = None,
) -> str:
    """Search KG nodes by keyword over titles, descriptions, and markdown bodies.

    Args:
        query: Search terms, e.g. "iso 3166" or "catalog storytelling"
        limit: Max results (default 5)
        role: Optional filter: "builder" or "domain"
        track: Optional filter: "knowledge", "skills", or "behaviors"
    """
    idx = get_index()
    results = idx.search(query=query, limit=limit, role=role, track=track)
    return json.dumps({"query": query, "count": len(results), "results": results}, indent=2)


@mcp.tool(name="kg_get_node")
def kg_get_node(node_id: str) -> str:
    """Fetch a KG node by id plus its linked markdown body.

    Args:
        node_id: Full node id, e.g. knowledge:builder:data-catalog-ui-storytelling
    """
    idx = get_index()
    node = idx.get_node(node_id)
    if node is None:
        return json.dumps({"error": f"node not found: {node_id}"}, indent=2)
    return json.dumps(node, indent=2)


@mcp.tool(name="kg_list_proposals")
def kg_list_proposals() -> str:
    """List pending KG proposals in agents/knowledge-graphs/proposals/."""
    idx = get_index()
    proposals = idx.list_proposals()
    return json.dumps({"count": len(proposals), "proposals": proposals}, indent=2)


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
