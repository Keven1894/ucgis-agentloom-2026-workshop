# 01 — Setup (attendee)

**UCGIS 2026 workshop** · ~20 minutes · do this once after forking  
**Prerequisite**: fork [`ucgis-agentloom-2026-workshop`](https://github.com/Keven1894/ucgis-agentloom-2026-workshop), clone locally, workshop API key in hand  
**Next**: [`02-quickstart.md`](./02-quickstart.md) · full checklist: [`00-workshop-workflow.md`](./00-workshop-workflow.md)

---

## What you are wiring

| Surface | Tool | Your job |
| --- | --- | --- |
| Python env | Repo **`.venv`** | Create once; all CLIs + MCP use this |
| Agent | VS Code + **Python** + **Cline** + `.clinerules/` | Install extensions + API key |
| KG read | MCP **`agentloom-kg`** | Paste JSON config (human once; **global** — see Step 5) |
| KG review | Dashboard **`:8000`** | Run server in a **dedicated terminal**; read Proposals tab |
| KG write | `propose_node.py` / `accept_proposal.py` | Cline proposes; **you** accept |

Cline does **not** configure MCP for you. See [`cline-mcp-tools.md`](./cline-mcp-tools.md).

**No separate “build KG” step** — MCP reads committed `agents/knowledge-graphs/*.json`. Domain KG starts **root-only**; you add nodes via propose-review.

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

**Pass**:

- `test_mcp_kg_tools.py` prints **PASS** (on a cold fork you may see `[OK] Domain KG is root-only` for iso 3166 — that is expected)
- `propose_node.py --help` shows usage
- Builder `catalog storytelling` search returns hits; `knowledge:domain:root` is found

---

## Step 2 — VS Code Python extension + interpreter

**Open the repo as a folder**: **File → Open Folder** → your `ucgis-agentloom-2026-workshop` clone (not a single file).

### 2a — Install Python extension (required)

Without this extension, **Python: Select Interpreter** will not appear in the command palette.

1. `Ctrl+Shift+X` → **Extensions**
2. Search **Python** → install **Python** by **Microsoft** (`ms-python.python`)
3. Reload window if prompted (Pylance / `ms-python.vscode-pylance` is installed automatically with Python)

**Pass**: Extensions panel shows Python as **Installed**.

### 2b — Select repo `.venv`

1. `Ctrl+Shift+P` → **Python: Select Interpreter**
2. Choose **`.venv/Scripts/python.exe`** (Windows) or **`.venv/bin/python`** (macOS/Linux)  
   If missing from the list: **Enter interpreter path…** → browse to that file under your clone.

**Pass**: VS Code status bar (bottom-right) shows something like `Python 3.x.x ('.venv': venv)`.

**Alternative (no command palette)**: create `.vscode/settings.json` in the repo root:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe"
}
```

On macOS/Linux use `"${workspaceFolder}/.venv/bin/python"`.

Optional template: copy [`.vscode/settings.json.example`](../../.vscode/settings.json.example) → `.vscode/settings.json` (adjust path if needed).

**Note**: Cline and MCP still use explicit `.venv` paths in Step 5 — Step 2 helps the integrated terminal and Python tooling stay aligned.

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

### 5a — Paste config (human once)

1. Cline → **MCP Servers** → Configure → **Configure MCP Servers**
2. Open the template for your OS:
   - Windows → [`cline-mcp-settings.example.json`](./cline-mcp-settings.example.json)
   - macOS/Linux → [`cline-mcp-settings.macos-linux.example.json`](./cline-mcp-settings.macos-linux.example.json)
3. Replace every `REPO_ROOT` with your **absolute** fork path  
   Example Windows: `C:/projects/02_research-agents/2026-ucgis/ucgis-agentloom-2026-workshop`  
   Example macOS: `/Users/<you>/projs/01_agentloom/ucgis-agentloom-2026-workshop`
4. Ensure `command` is **`REPO_ROOT/.venv/Scripts/python.exe`** (Windows) or **`REPO_ROOT/.venv/bin/python`** (macOS/Linux)
5. Save → Done → **Developer: Reload Window**

Use **forward slashes** in paths (even on Windows).

### 5b — Cline MCP is global (not per repo)

This JSON lives in **Cline user settings** (VS Code `globalStorage`), **not** in your fork. **All VS Code projects share one MCP config.**

| Implication | What to do |
| --- | --- |
| Paths must match **this clone** | `command` + `args` → **your fork’s** `.venv` python and `mcp_kg_server.py` |
| You open a different clone later | **Edit MCP JSON again** or you will read another repo’s KG |
| Cold-start fork | Step 5c functional test: `kg_list_proposals` → **count 0** until you propose |

Organizer dev checkout vs attendee fork: same wiring rule — **MCP paths must match the repo you have open.**

### 5c — Connection check

**Pass**: MCP panel shows **agentloom-kg** **connected** (green indicator, toggle on).

**Tool names may not appear** under the server row — known Cline + FastMCP UI quirk ([cline#1272](https://github.com/cline/cline/issues/1272)). Use Step 5d, not the tool list, as the pass criterion.

Troubleshooting: [`cline-mcp-tools.md`](./cline-mcp-tools.md)

### 5d — MCP functional test (Cline)

New Cline task (**Act** mode). Paste:

```
Use MCP kg_search for "catalog storytelling" with role=builder.
Use MCP kg_list_proposals.
Do NOT read agents/knowledge-graphs/*-graph.json directly.
Report hit count and stop.
```

**Pass**:

- Cline invokes MCP tools (tool-use in transcript)
- Builder search → **≥1 hit**
- Proposals count reported (**0** on cold fork is OK)

---

## Step 6 — Dashboard (human review)

Open a **new, dedicated terminal tab** and keep it open for the whole session. Do not run other commands in this tab.

**Recommended (no file watcher — stable on Windows):**

```bash
# Windows
.venv\Scripts\python -m uvicorn server.dashboard.app:app --port 8000 --host 127.0.0.1

# macOS/Linux
.venv/bin/python -m uvicorn server.dashboard.app:app --port 8000 --host 127.0.0.1
```

Or: `make dashboard` if `make` is available.

**Pass**: terminal **stays running** (prompt does **not** return to `PS>`); browser **http://127.0.0.1:8000** loads; **Proposals** tab opens.

**Quick check** (second terminal): `curl http://127.0.0.1:8000/api/health` → `{"ok":true,...}`

Optional: `--reload` for dashboard development — on Windows it watches the whole repo; IDE/Cline saves may restart the server. If the process exits immediately, drop `--reload` and use the command above.

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
| 3 | Python extension installed (`ms-python.python`) | ☐ |
| 4 | VS Code interpreter = `.venv` | ☐ |
| 5 | Cline installed + API configured | ☐ |
| 6 | `.clinerules` sanity quote test | ☐ |
| 7 | MCP JSON paths → **this fork** (global config) | ☐ |
| 8 | MCP `agentloom-kg` connected (green) | ☐ |
| 9 | MCP functional test (Step 5d) — Cline calls `kg_search` | ☐ |
| 10 | Dashboard `:8000` Proposals tab (dedicated terminal) | ☐ |
| 11 | `validate_all` + `run_all` → PASS | ☐ |

All checked → continue to [**02-quickstart.md**](./02-quickstart.md).

---

## Troubleshooting

| Issue | Fix |
| --- | --- |
| No **Python: Select Interpreter** | Install **Python** (`ms-python.python`); open repo as **folder**; reload window |
| `test_mcp` FAIL only on `iso 3166` (old snapshot) | Update workshop repo; or confirm builder search + domain root OK — cold fork has no ISO3166 yet |
| MCP connected but **no tools listed** | UI-only ([cline#1272](https://github.com/cline/cline/issues/1272)); run Step 5d. Ensure `mcp_kg_server.py` uses `log_level=ERROR` |
| MCP reads **wrong repo** / proposals count surprising | Cline MCP is **global** — fix absolute paths in MCP JSON to match **open fork** |
| MCP "Connection closed" | Absolute paths; MCP `command` must be **this fork’s** `.venv` python |
| Dashboard **starts then stops** / prompt returns | Use dedicated terminal tab; omit `--reload`; do not Ctrl+C; check `netstat` for port 8000 |
| Cline uses wrong Python | Re-select interpreter; reload window |
| Port 8000 in use | Stop other service or change port in uvicorn command |
| Empty VS Code extension settings for Cline | Expected — use **Cline: Settings** from command palette |

Architecture: [`kg-access-and-human-review.md`](./kg-access-and-human-review.md)
