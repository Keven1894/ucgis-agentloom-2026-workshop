# Workshop documentation (UCGIS 2026)

**Workshop date**: 2026-06-15 (half-day)  
**Execution repo**: `ucgis-agentloom-2026`  
**Planning dossier**: `envistor-data/docs/research/workshop-ucgis-2026/`

## Read order

| Doc | Audience | Status |
|---|---|---|
| [`00-workshop-workflow.md`](./00-workshop-workflow.md) | **Start here** — full A→G checklist (W4 seed) | draft 2026-05-31 |
| [`kg-access-and-human-review.md`](./kg-access-and-human-review.md) | Architecture — two surfaces, who builds what | locked |
| [`cline-wrapper.md`](./cline-wrapper.md) | Cline + `.clinerules` setup (W1) | complete |
| [`cline-mcp-tools.md`](./cline-mcp-tools.md) | `.venv` + MCP config + tools (W2) | complete |
| [`welcome.html`](./welcome.html) | Browser onboarding cheat sheet | complete |
| [`cline-mcp-settings.example.json`](./cline-mcp-settings.example.json) | MCP template (`REPO_ROOT` + `.venv`) | complete |

## The two-surface model (TL;DR)

- **Agents** (Cline) read the KG via **MCP** and write proposals via **`propose_node.py`**.
- **Humans** review proposals via the **dashboard** (`make dashboard` → `:8000` Proposals tab) and accept via **`accept_proposal.py`**.
- W1 verified the agent propose path. W2 adds MCP + welcome page. The dashboard already exists.

**Who builds what:** framework infrastructure (MCP, dashboard, validators) → **operator + Cursor**. Cline smoke tests → **Cline**. Workshop domain work → **attendee + Cline**. Details: [`kg-access-and-human-review.md`](./kg-access-and-human-review.md) § Who builds what.

## Related plans

- W1 closed: `docs/plan/complete/2026-05-31-w1-cline-wrapper-complete.md`
- W2 todo: `docs/plan/todo/2026-05-31-w2-mcp-and-human-review.md`
- Workshop track: `docs/plan/todo/2026-05-23-workshop-track.md`
