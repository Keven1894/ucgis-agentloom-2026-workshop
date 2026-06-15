# Cline wrapper — running the AgentLoom builder agent in VS Code

**Last updated**: 2026-05-31  
**Audience**: workshop attendees and operators  
**Status**: W1 complete — operationally verified (Wave C Tier 1, 2026-05-31)  
**Related**: `.clinerules/` (repo root), `docs/workshop/kg-access-and-human-review.md`, `docs/research/agent-eval/2026-05-31-d4-from-cline-wave-c.md`

## What this is

Cline is **Layer-3 host #3** for the AgentLoom builder agent. It **proposes** KG nodes; it does not build the live KG by itself. A human accepts proposals via `accept_proposal.py` after reviewing them on the **dashboard** (see § Human review below).

It sits alongside:

| Host | How the prompt loads |
|---|---|
| **builder-agent CLI** (`scripts/agent/`) | reads KG node directly |
| **Cursor** | project rules / `.cursor/rules/` |
| **Cline** (this doc) | `.clinerules/` directory at repo root |

All three share the same canonical system prompt (`docs/builder/concepts/builder-agent-system-prompt.md`, prompt_version `52e196219a`), the same propose/accept CLIs, and the same JSON output contract. Cline is **not** a fork of the builder agent — it is a wrapper that loads the same instructions and shells out to the same tools.

## Prerequisites

| Tool | Minimum | Notes |
|---|---|---|
| VS Code | 1.95+ | Windows / macOS / Linux |
| Python | 3.11+ | **repo `.venv` required** — see Step 0 below |
| Cline extension | 3.86+ tested | publisher: **saoudrizwan** (cline.bot) — not Copilot Chat |
| OpenAI API key | gpt-5.2 access | workshop may use a pooled proxy (W5) instead of BYOK |

Clone or open the repo at its **root**. Do not open a copy on Desktop/Documents — Cline checkpoints are disabled there.

## Quick setup

Full checklist: [`00-workshop-workflow.md`](./00-workshop-workflow.md).

### 0 — Create `.venv` (required)

```bash
# Windows
cd C:/projects/ucgis-agentloom-2026
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt
.venv/Scripts/python scripts/test_mcp_kg_tools.py

# macOS/Linux
cd ~/path/to/ucgis-agentloom-2026-workshop
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/test_mcp_kg_tools.py
```

VS Code → **Python: Select Interpreter** → `.venv/Scripts/python.exe` (Windows) or `.venv/bin/python` (macOS/Linux).

Optional: `.vscode/settings.json.example` → `.vscode/settings.json`.

### 1 — Install Cline

VS Code → Extensions → search **Cline** → install **saoudrizwan.claude-dev** → restart VS Code.

Verify: `Ctrl+Shift+P` → `Cline: New Task` appears.

### 2 — Configure the LLM provider

Open settings via **`Ctrl+Shift+P` → `Cline: Settings`**.

> **Common mistakes**
> - Cursor "Agent Customizations" is **not** Cline.
> - VS Code Extensions → Cline → gear → Extension Settings is **empty by design** — use Cline's in-panel Settings instead.
> - The right-side **CHAT** panel is GitHub Copilot Chat, not Cline. Use the **left Cline panel**.

| Field | Workshop default |
|---|---|
| API Provider | `OpenAI` (BYOK) or `OpenAI Compatible` (pooled proxy, W5) |
| API Key | your key or workshop-issued key |
| Model | `gpt-5.2` |
| Temperature | `0.2` |

Skip the "Meet Cline" walkthrough if it errors (`walkthrough/step3.md` missing) — go straight to Settings.

### 3 — Open the workspace

`File → Open Folder…` → select the repo root.

Confirm `.clinerules/` exists (four files: `00`–`03`).

### 4 — Sanity-check rules are loaded

Many models refuse to quote a hidden system prompt. Use a **file read** instead:

```
Quote the first 200 characters of .clinerules/01-builder-agent-prompt.md verbatim
(the file on disk, not your hidden system prompt).
```

**Pass**: output mentions `DO NOT HAND-EDIT`, `sync_clinerules.py`, and `builder-agent-system-prompt.md`.

Optional follow-up:

```
According to .clinerules/, what is your role and which node types may you propose in v1?
```

**Pass**: AgentLoom **builder agent**; v1 proposes **knowledge only**.

### 5 — Configure MCP (human pastes JSON)

See [`cline-mcp-tools.md`](./cline-mcp-tools.md). Cline does **not** self-configure MCP.

Use `.venv/Scripts/python.exe` (Windows) or `.venv/bin/python` (macOS/Linux) as `command` in `cline_mcp_settings.json`. Reload window; confirm 3 tools on `agentloom-kg`.

### 6 — Allow shell commands (one-time)

When Cline first runs `python scripts/kg/propose_node.py …`, approve the prompt. Prefer **"Always allow" for that command pattern only**.

### 7 — Confirm CLI + dashboard

```bash
# Windows
.venv/Scripts/python scripts/kg/propose_node.py --help
.venv/Scripts/python -m uvicorn server.dashboard.app:app --port 8000 --host 127.0.0.1

# macOS/Linux
.venv/bin/python scripts/kg/propose_node.py --help
.venv/bin/python -m uvicorn server.dashboard.app:app --port 8000 --host 127.0.0.1
```

Dashboard → `http://127.0.0.1:8000` · open [`welcome.html`](./welcome.html)

### 8 — Start a Cline task (left panel)

Click **+** (New Task) in the Cline panel — not Copilot CHAT. Paste your workshop task (propose domain knowledge for a snapshot, build catalog UI, etc.).

---

## What Cline reads automatically

Cline concatenates every `.md` / `.txt` file in `.clinerules/` at workspace open:

| File | Role |
|---|---|
| `00-README.md` | orientation |
| `01-builder-agent-prompt.md` | **GENERATED** canonical prompt — never hand-edit |
| `02-cline-host-adaptation.md` | CLI paths, KG reading discipline, snapshot quirks |
| `03-workshop-discipline.md` | paired-commit, no agent-side accept, validators green |

Regenerate after KG prompt changes:

```bash
python scripts/sync_clinerules.py
python scripts/sync_clinerules.py --check   # CI mode — must exit 0
```

Drift is enforced by Tier-A validator `clinerules_must_match_system_prompt_kg_node.py`.

---

## The propose-review loop (attendee workflow)

```mermaid
sequenceDiagram
    participant You
    participant Cline
    participant CLI as propose_node.py
    participant Queue as proposals/
    participant Human as Human reviewer

    You->>Cline: Task (inspect snapshot, propose KG nodes)
    Cline->>Cline: Read KG + snapshot (selectively)
    Cline->>CLI: python scripts/kg/propose_node.py …
    CLI->>Queue: JSON + UPDATE_LOG
    Cline->>You: "Proposals filed; stopping here"
    Human->>Human: Review on dashboard Proposals tab
    Human->>CLI: python scripts/kg/accept_proposal.py …
    Note over Cline: Cline must NEVER call accept_proposal.py
```

**Cline's job**: read evidence, emit the JSON contract, call `propose_node.py` once per proposal, stop.

**Your job**: review on the **dashboard** (plain language), accept or reject via CLI, implement downstream work (catalog UI, etc.), keep validators green.

---

## Human review (dashboard — not JSON)

Cline files proposals as JSON under `agents/knowledge-graphs/proposals/`. **Do not review by opening those files** unless debugging — use the dashboard:

```bash
make dashboard    # → http://127.0.0.1:8000
```

| Tab | Use when |
|---|---|
| **Proposals** | Review pending items — titles, justifications, UPDATE_LOG snippets |
| **Graph** | See accepted nodes in context after accept |
| **Timeline** | Audit trail of past accepts/rejects |

After you approve a proposal in the browser, run in terminal:

```bash
python scripts/kg/accept_proposal.py --proposal agents/knowledge-graphs/proposals/<filename>.json
```

Refresh the dashboard — accepted nodes move from Proposals to Graph/Timeline.

> **W2** adds MCP (agent KG search) + a welcome HTML page linking Cline and this dashboard. Architecture: `docs/workshop/kg-access-and-human-review.md`.

### Example propose invocation

Cline runs this; you approve:

```bash
python scripts/kg/propose_node.py \
  --type knowledge \
  --target-role domain \
  --slug my-dataset-shape \
  --title "My dataset top-level shape" \
  --justification "Observed X in snapshot line Y …" \
  --source-context "workshop D4, attendee fork" \
  --priority high \
  --author cline-builder-agent
```

---

## Reading the KG

**Today (W1 verified)**: Cline reads KG json files directly via its file-read tool. Follow selective-reading rules in `02-cline-host-adaptation.md`:

- Read only graphs for the target role (`domain-*` for domain proposals).
- Skim ids/titles first; fetch full markdown bodies only for related nodes.
- Never load 14 MB GeoJSON snapshots in full — sample the first 8 KB.

**Coming (W2)**: lightweight MCP server with `kg/search`, `kg/get_node`, `kg/list_proposals`. Prefer MCP when installed — same discipline, less context burn.

---

## Saving your run (reproducibility)

Cline v3.86+ **Export** (History → select task → Export) opens a folder, not a markdown file:

| Windows path | `%APPDATA%\Code\User\globalStorage\saoudrizwan.claude-dev\tasks\{taskId}\` |
|---|---|
| Key files | `api_conversation_history.json`, `ui_messages.json`, `task_metadata.json` |

Copy into `runs/agent/` with a UTC timestamp prefix, e.g.:

```
runs/agent/20260531T014730Z-cline-d4-wave-c.api_conversation_history.json
```

Reference run: `runs/agent/20260531T014730Z-cline-d4-wave-c.*` (Wave C smoke test).

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| Walkthrough `step3.md` missing | Skip walkthrough; use `Cline: Settings` directly or reinstall extension |
| Empty Extension Settings page | Expected — use Command Palette `Cline: Settings` |
| SESSIONS list, no ⚙️ | Start New Task or `Cline: Open In New Tab` |
| Generic AI persona, no AgentLoom | Open repo root; reload window; verify `.clinerules/` on branch |
| Yellow checkpoint warning (Desktop) | Move repo under `C:\projects\` or similar |
| Cline stalls reading huge files | Remind it: first 8 KB only; point to `02-cline-host-adaptation.md` |
| Cline calls `accept_proposal.py` | **Stop session** — violates D8; escalate to instructor |

---

## Verification evidence (operator)

Wave C smoke test (D4 Natural Earth admin0, 2026-05-31):

- **Tier 1** — 5 proposals filed via `propose_node.py`, no auto-accept
- **3/4** fuzzy topic overlap with gpt-5.2 baseline (+ 1 novel grounded find)
- **8/8** Tier-A validators green at review time
- Full write-up: `docs/research/agent-eval/2026-05-31-d4-from-cline-wave-c.md`

---

## What's next in the workshop track

| Item | Status |
|---|---|
| W1 Cline wrapper | ✅ complete — agent propose path verified |
| W2 MCP + human-review onboarding | planned — MCP tools + welcome page → dashboard |
| W3 workshop starter repo | planned — clean fork target |
| W4 attendee setup docs | planned — trinity: Cline + MCP + dashboard |

See `docs/workshop/README.md` for doc index.
