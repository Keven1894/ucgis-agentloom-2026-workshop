# 01 — Setup (attendee)

**UCGIS 2026 workshop** · ~20 minutes · do this once after forking  
**Prerequisite**: fork [`ucgis-agentloom-2026-workshop`](https://github.com/Keven1894/ucgis-agentloom-2026-workshop), clone locally, workshop API key in hand  
**Next**: [`02-quickstart.md`](./02-quickstart.md) · full checklist: [`00-workshop-workflow.md`](./00-workshop-workflow.md)

---

## What you are wiring

| Surface | Tool | Your job |
| --- | --- | --- |
| Python env | Repo **`.venv`** | Create once; all CLIs + MCP use this |
| Agent | VS Code + **Cline** + `.clinerules/` | Install + API key |
| KG read | MCP **`agentloom-kg`** | Paste JSON config (human once) |
| KG review | Dashboard **`:8000`** | Run server; read Proposals tab |
| KG write | `propose_node.py` / `accept_proposal.py` | Cline proposes; **you** accept |

Cline does **not** configure MCP for you. See [`cline-mcp-tools.md`](./cline-mcp-tools.md).

---

## Step 1 — Repo `.venv`

From your fork root (replace path):

```bash
cd ucgis-agentloom-2026-workshop
git checkout -b workshop-YOURHANDLE
```

**Windows (VS Code terminal):**

```bash
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python scripts\test_mcp_kg_tools.py
.venv\Scripts\python scripts\kg\propose_node.py --help
```

**macOS / Linux:**

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/test_mcp_kg_tools.py
.venv/bin/python scripts/kg/propose_node.py --help
```

**Pass**: `test_mcp_kg_tools.py` prints PASS; `--help` shows propose_node usage.

---

## Step 2 — VS Code interpreter

1. `Ctrl+Shift+P` → **Python: Select Interpreter**
2. Choose `.venv/Scripts/python.exe` (Windows) or `.venv/bin/python` (macOS/Linux)

Optional: copy [`.vscode/settings.json.example`](../../.vscode/settings.json.example) → `.vscode/settings.json`.

---

## Step 3 — Install Cline

1. Extensions → **Cline** (`saoudrizwan.claude-dev`) → install → reload
2. `Ctrl+Shift+P` → **Cline: New Task** (confirms extension loaded)

Use the **left Cline panel**, not Copilot Chat.

---

## Step 4 — Cline LLM settings

`Ctrl+Shift+P` → **Cline: Settings**

| Field | Workshop value |
| --- | --- |
| API Provider | OpenAI (or OpenAI Compatible if using organizer proxy) |
| API Key | your workshop key |
| Model | `gpt-5.2` (or organizer-specified) |
| Temperature | `0.2` |

**Sanity check** — paste into Cline:

```
Quote the first 200 characters of .clinerules/01-builder-agent-prompt.md verbatim.
```

**Pass**: response mentions governance / propose-review / not hand-editing `*-graph.json`.

Details: [`cline-wrapper.md`](./cline-wrapper.md)

---

## Step 5 — MCP server (agentloom-kg)

1. Cline → **MCP Servers** → Configure → **Configure MCP Servers**
2. Open [`cline-mcp-settings.example.json`](./cline-mcp-settings.example.json)
3. Replace every `REPO_ROOT` with your **absolute** fork path  
   Example Windows: `C:/Users/you/ucgis-agentloom-2026-workshop`
4. Ensure `command` is **`REPO_ROOT/.venv/Scripts/python.exe`** (Windows) or **`REPO_ROOT/.venv/bin/python`** (macOS/Linux)
5. Save → Done → **Developer: Reload Window**

**Pass**: MCP panel shows **agentloom-kg** with 3 tools: `kg_search`, `kg_get_node`, `kg_list_proposals`.

Troubleshooting: [`cline-mcp-tools.md`](./cline-mcp-tools.md)

---

## Step 6 — Dashboard (human review)

Terminal (leave running during workshop):

```bash
# Windows
.venv\Scripts\python -m uvicorn server.dashboard.app:app --reload --port 8000 --host 127.0.0.1

# macOS/Linux
.venv/bin/python -m uvicorn server.dashboard.app:app --reload --port 8000 --host 127.0.0.1
```

Or: `make dashboard` if `make` is available.

Browser: **http://127.0.0.1:8000** → open **Proposals** tab.

Optional cheat sheet: open [`welcome.html`](./welcome.html) in a browser tab.

---

## Step 7 — Governance floor

```bash
# Windows
.venv\Scripts\python scripts\kg\validate_all.py
.venv\Scripts\python scripts\validators\run_all.py

# macOS/Linux — same with .venv/bin/python
```

**Pass**: all schema + integrity + Tier-A behavior validators succeed (8/8).

This is the same gate GitHub Actions runs on your PR.

---

## Setup checklist

| # | Step | Pass? |
| --- | --- | --- |
| 1 | `.venv` + requirements installed | ☐ |
| 2 | `test_mcp_kg_tools.py` → PASS | ☐ |
| 3 | VS Code interpreter = `.venv` | ☐ |
| 4 | Cline installed + API configured | ☐ |
| 5 | `.clinerules` sanity quote test | ☐ |
| 6 | MCP `agentloom-kg` — 3 tools green | ☐ |
| 7 | Dashboard `:8000` Proposals tab loads | ☐ |
| 8 | `validate_all` + `run_all` → PASS | ☐ |

All checked → continue to [**02-quickstart.md**](./02-quickstart.md).

---

## Troubleshooting

| Issue | Fix |
| --- | --- |
| MCP "Connection closed" | Absolute paths; MCP `command` must be `.venv` python |
| Cline uses wrong Python | Re-select interpreter; reload window |
| Port 8000 in use | Stop other service or change port in uvicorn command |
| Empty VS Code extension settings for Cline | Expected — use **Cline: Settings** from command palette |

Architecture: [`kg-access-and-human-review.md`](./kg-access-and-human-review.md)
