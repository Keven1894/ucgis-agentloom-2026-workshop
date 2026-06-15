# ucgis-agentloom-2026-workshop

**UCGIS 2026 — From Prompts to Protocols** (June 15, 2026, University of Maryland)

Build a public-data geospatial catalog — search, filter, map, FAIR metadata — using **AgentLoom** on VSCode + **Cline**, with executable behavior validators. Fork this repo, propose knowledge into the KG, implement a catalog for one heterogeneous data source, and open a PR.

After the workshop, this repo also ships **finished reference demos** under [`demo/`](demo/) so you can **practice the workflow** and **compare your outcome** against validators-green examples for D1–D4.

## Relationship to AgentLoom

| Repo | Role |
| --- | --- |
| [**Keven1894/AgentLoom**](https://github.com/Keven1894/AgentLoom) | Long-lived **framework** home (dual-helix KG + validators). SoftwareX paper cites this repo @ v3.0+. |
| **This repo** | **Workshop edition** — framework + docs + **public reference demos** (D1–D4). Fork, practice, PR. |

This repo is **not** a GitHub fork of AgentLoom. It is a derived edition built from the UCGIS sprint framework floor.

If you want the general AgentLoom framework beyond this workshop, start at [AgentLoom](https://github.com/Keven1894/AgentLoom).

## Two ways to use this repo

| Goal | What to do |
| --- | --- |
| **Browse reference demos** | Clone as-is → [`demo/serve/serve-all.sh`](demo/serve/serve-all.sh) → [showcase](http://127.0.0.1:8766/docs/workshop/showcase.html) |
| **Practice the workshop** | Fork → clone **your fork** into a **separate directory** → follow [`docs/workshop/01-setup.md`](docs/workshop/01-setup.md) → build your own catalog → compare against [`demo/reference/`](demo/reference/) |

Your practice fork starts **framework-only** (empty domain KG, no `starter/` catalogs). The committed demos live in `demo/` — they do not replace the work you do in your fork.

## What you get

| Piece | Purpose |
| --- | --- |
| Builder-KG + validators | Governance floor — `make validate-all` must pass from commit 1 |
| Propose / accept CLIs | Agents propose; **you** accept (`accept_proposal.py`) |
| Dashboard (`:8000`) | Read-only human review — Proposals tab; `?ref=` overlays demo KG |
| MCP server (`agentloom-kg`) | Cline reads the KG without opening JSON files |
| 4 vendored snapshots | Pick D1–D4 (or BYO) — see `notes/data-sources.md` |
| **`demo/reference/`** | Finished D1–D4 catalogs + domain KG snapshots + organizer PROMPTS drafts |
| `.clinerules/` | Cline host adaptation for this repo |

## Quickstart (practice)

```bash
git clone https://github.com/<your-handle>/ucgis-agentloom-2026-workshop
cd ucgis-agentloom-2026-workshop
git checkout -b workshop-<your-handle>
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

make validate-all    # expect all PASS
make dashboard       # open http://127.0.0.1:8000
```

Then follow the workshop docs:

1. [`docs/workshop/01-setup.md`](docs/workshop/01-setup.md) — **start here** (venv, Cline, MCP, dashboard)
2. [`docs/workshop/02-quickstart.md`](docs/workshop/02-quickstart.md) — 5-minute propose-review practice
3. [`docs/workshop/03-data-source-menu.md`](docs/workshop/03-data-source-menu.md) — pick D1–D4 for your catalog
4. Prompt pack for your dataset: [`04-attendee-prompt-pack-D1.md`](docs/workshop/04-attendee-prompt-pack-D1.md) · [D2](docs/workshop/04-attendee-prompt-pack-D2.md) · [D3 (default)](docs/workshop/04-attendee-prompt-pack.md) · [D4](docs/workshop/04-attendee-prompt-pack-D4.md)
5. Compare finish line: [`demo/reference/`](demo/reference/) and [showcase](docs/workshop/showcase.html)

## Browse reference demos (no fork required)

```bash
git clone https://github.com/Keven1894/ucgis-agentloom-2026-workshop.git
cd ucgis-agentloom-2026-workshop
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
bash demo/serve/serve-all.sh
```

Open http://127.0.0.1:8766/docs/workshop/showcase.html — live catalogs, KG overlays via `?ref=d1-earthquakes`, etc.

See [`demo/README.md`](demo/README.md) for layout and maintainer notes.

## Toolchain

```
Required:                 For LLM calls:
  VSCode                    OpenAI / OpenRouter API key (BYOK)
  Cline extension
  git, Python 3.11+

Also works in production:
  Cursor, Antigravity, Claude Code — same MCP + KG + validators
```

## Repo layout

```
├── agents/knowledge-graphs/   6 KG files + SCHEMA.md (domain root-only in your fork)
├── demo/reference/             D1–D4 finished builds (compare / browse)
├── demo/serve/                 Local showcase + dashboard launcher
├── .clinerules/                Cline rules
├── scripts/kg/                 propose_node.py, accept_proposal.py, validators
├── scripts/mcp_kg_server.py    MCP stdio server for Cline
├── server/dashboard/           Human review UI + demo KG overlay
├── data/snapshots/             D1–D4 sample data (offline-friendly)
├── notes/data-sources.md       Source quirks — seed for your domain KG nodes
└── docs/workshop/              Setup + workflow docs + showcase.html
```

`starter/` is **gitignored** — created when you build your catalog (or when staging demos).

## Contributing (fork-and-PR)

See [`CONTRIBUTING.md`](CONTRIBUTING.md). Every PR runs `make validate-all` in GitHub Actions.

We may write a future paper based on this repo — your work might be acknowledged (with permission).

## License

MIT — see [`LICENSE`](LICENSE).
