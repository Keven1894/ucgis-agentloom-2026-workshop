# Cline MCP tools — AgentLoom KG (read-only)

**Last updated**: 2026-05-31  
**Server**: `scripts/mcp_kg_server.py`  
**Launch**: stdio — Cline spawns `.venv` Python (see below)  
**Workflow**: [`00-workshop-workflow.md`](./00-workshop-workflow.md)  
**Architecture**: [`kg-access-and-human-review.md`](./kg-access-and-human-review.md)

## Prerequisites: repo `.venv` (required)

Workshop standard is **repo-local venv**, not system Python. MCP and Cline shell commands must share the same interpreter.

```bash
cd C:/projects/ucgis-agentloom-2026   # your clone path

# Windows
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt
.venv/Scripts/python scripts/test_mcp_kg_tools.py

# macOS / Linux
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/test_mcp_kg_tools.py
```

Set VS Code interpreter: **Python: Select Interpreter** → `.venv/Scripts/python.exe` (Windows) or `.venv/bin/python`.

Optional: copy `.vscode/settings.json.example` → `.vscode/settings.json` so integrated terminal auto-activates `.venv`.

---

## Configure Cline MCP (human — not Cline)

Cline **cannot** reliably configure its own MCP settings. You paste JSON once.

1. Complete `.venv` setup above
2. Cline panel → **MCP Servers** → **Configure** → **Configure MCP Servers**
3. Replace `REPO_ROOT` in the template below with your **absolute** repo path
4. Save → **Done** → `Developer: Reload Window`
5. Confirm **agentloom-kg** shows **connected** (green). Tool names may not appear in the panel — see [Troubleshooting](#troubleshooting).
6. Run the [functional test](#cline-acceptance-test-operator) in a Cline task.

### Windows template

Replace `REPO_ROOT` with e.g. `C:/projects/ucgis-agentloom-2026`:

```json
{
  "mcpServers": {
    "agentloom-kg": {
      "command": "C:/projects/ucgis-agentloom-2026/.venv/Scripts/python.exe",
      "args": [
        "C:/projects/ucgis-agentloom-2026/scripts/mcp_kg_server.py"
      ],
      "disabled": false,
      "autoApprove": ["kg_search", "kg_get_node", "kg_list_proposals"]
    }
  }
}
```

### macOS / Linux template

```json
{
  "mcpServers": {
    "agentloom-kg": {
      "command": "/path/to/ucgis-agentloom-2026/.venv/bin/python",
      "args": [
        "/path/to/ucgis-agentloom-2026/scripts/mcp_kg_server.py"
      ],
      "disabled": false,
      "autoApprove": ["kg_search", "kg_get_node", "kg_list_proposals"]
    }
  }
}
```

**Rules:**

- Use **forward slashes** in paths (even on Windows)
- `command` = `.venv` Python, **not** system `python`
- Paths must be **absolute** (Cline does not inherit your shell PATH reliably on Windows)

Shipped placeholder file: [`cline-mcp-settings.example.json`](./cline-mcp-settings.example.json)

---

## Tools

| Tool | Purpose | Example |
|---|---|---|
| `kg_search` | Keyword search over accepted nodes + pending proposals | `query="iso 3166"`, `role="domain"`, `limit=5` |
| `kg_get_node` | Full node JSON + markdown body | `node_id="knowledge:builder:data-catalog-ui-storytelling"` |
| `kg_list_proposals` | Pending queue (same as dashboard Proposals tab) | no args |

All tools are **read-only**. To file a proposal, Cline shells out to:

```bash
.venv/Scripts/python scripts/kg/propose_node.py ...   # Windows
# or .venv/bin/python ...                             # macOS/Linux
```

(with VS Code interpreter set to `.venv`, plain `python` also works in integrated terminal)

---

## Recommended Cline workflow

1. `kg_search` — find related nodes before proposing
2. `kg_get_node` — read full conventions
3. `kg_list_proposals` — check pending queue
4. Inspect snapshot (first 8 KB for large files)
5. `propose_node.py` per proposal — **stop**
6. Human: dashboard Proposals tab → `accept_proposal.py` if satisfied

---

## Human review (not MCP)

```bash
.venv/Scripts/python -m uvicorn server.dashboard.app:app --port 8000 --host 127.0.0.1
# or: make dashboard
```

→ `http://127.0.0.1:8000` · open [`welcome.html`](./welcome.html)

---

## Fallback (MCP unavailable)

Disable `agentloom-kg` in MCP settings. Cline falls back to selective file read per `.clinerules/02-cline-host-adaptation.md` (W1 verified).

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| Connected (green) but **no tools in MCP list** | **Often OK** — Cline + FastMCP hide tools in UI while chat still works ([cline#1272](https://github.com/cline/cline/issues/1272)). Run acceptance test below. `mcp_kg_server.py` sets `log_level="ERROR"` to help. |
| Connection closed (Windows) | Absolute paths; `.venv/Scripts/python.exe` as `command` |
| No tools listed **and** Cline cannot call them in chat | Run `.venv/Scripts/pip show mcp`; check Developer Tools console |
| Server crashes | `.venv/Scripts/python scripts/mcp_kg_server.py` — errors on stderr |
| Wrong packages | Recreate venv; never point MCP at system Python after workshop prep |
| Cline shell uses wrong Python | Set VS Code interpreter to `.venv`; copy `settings.json.example` |

---

## Cline acceptance test (operator)

After MCP connects:

```
Use MCP kg_search for "catalog storytelling" with role=builder.
Use MCP kg_list_proposals.
Do NOT read agents/knowledge-graphs/*-graph.json directly.
Report what you found and stop.
```

Save transcript to `runs/agent/`.
