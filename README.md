# ucgis-agentloom-2026-workshop

**UCGIS 2026 — From Prompts to Protocols** (June 15, 2026, University of Maryland)

Build a public-data geospatial catalog — search, filter, map, FAIR metadata — using **AgentLoom** on VSCode + **Cline**, with executable behavior validators. You fork this repo, propose knowledge into the KG, implement a catalog for one heterogeneous data source, and open a PR.

> This is the **attendee-facing workshop edition**. Framework development and paper evidence live in the private FIU dev repo `ucgis-agentloom-2026` (Gitea + Bitbucket dual-origin — not a public GitHub fork target).

## Relationship to AgentLoom

| Repo | Role |
| --- | --- |
| [**Keven1894/AgentLoom**](https://github.com/Keven1894/AgentLoom) | Long-lived **framework** home (dual-helix KG + validators). SoftwareX paper cites this repo @ v3.0+. |
| `ucgis-agentloom-2026` | **Dev / evidence** (FIU private, Gitea + Bitbucket). D1–D4 case studies and eval transcripts — organizers only. |
| **This repo** | **Workshop starter** — framework-only snapshot for attendees to fork-and-PR on June 15. |

This repo is **not** a GitHub fork of AgentLoom. It is a clean, derived edition built from the UCGIS sprint framework floor. Framework improvements flow **workshop → dev repo → AgentLoom** (v3/v4 sync), not the other way around.

If you want the general AgentLoom framework beyond this workshop, start at [AgentLoom](https://github.com/Keven1894/AgentLoom).

## What you get

| Piece | Purpose |
| --- | --- |
| Builder-KG + validators | Governance floor — `make validate-all` must pass from commit 1 |
| Propose / accept CLIs | Agents propose; **you** accept (`accept_proposal.py`) |
| Dashboard (`:8000`) | Read-only human review — Proposals tab |
| MCP server (`agentloom-kg`) | Cline reads the KG without opening JSON files |
| 4 vendored snapshots | Pick D1–D4 (or BYO) — see `notes/data-sources.md` |
| `.clinerules/` | Cline host adaptation for this repo |

## Quickstart (workshop day)

```bash
git clone https://github.com/<your-handle>/ucgis-agentloom-2026-workshop
cd ucgis-agentloom-2026-workshop
git checkout -b workshop-<your-handle>
python -m venv .venv
# Windows:
.venv\Scripts\pip install -r requirements.txt
# macOS/Linux:
# source .venv/bin/activate && pip install -r requirements.txt

make validate-all    # expect all PASS
make dashboard       # open http://127.0.0.1:8000
```

Then follow the workshop docs:

1. [`docs/workshop/welcome.html`](docs/workshop/welcome.html) — open in browser
2. [`docs/workshop/00-workshop-workflow.md`](docs/workshop/00-workshop-workflow.md) — full A→G checklist
3. [`docs/workshop/cline-mcp-tools.md`](docs/workshop/cline-mcp-tools.md) — wire MCP into Cline

## Toolchain

```
Required:                 Provided on arrival:
  VSCode                    OpenAI / OpenRouter API key
  Cline extension
  git, Python 3.11

NOT required:
  Cursor / Claude Code
  Docker on your laptop
  FIU account / VPN
```

## Repo layout

```
├── agents/knowledge-graphs/   6 KG files + SCHEMA.md
├── .clinerules/               Cline rules (synced from builder prompt)
├── scripts/kg/                propose_node.py, accept_proposal.py, validators
├── scripts/mcp_kg_server.py   MCP stdio server for Cline
├── server/dashboard/          Human review UI
├── data/snapshots/            D1–D4 sample data (offline-friendly)
├── notes/data-sources.md      Source quirks — seed for your domain KG nodes
└── docs/workshop/             Setup + workflow docs
```

There is **no** `starter/<source>/` directory yet — you create it.

## Contributing (fork-and-PR)

See [`CONTRIBUTING.md`](CONTRIBUTING.md). Every PR runs `make validate-all` in GitHub Actions.

## License

MIT — see [`LICENSE`](LICENSE).
