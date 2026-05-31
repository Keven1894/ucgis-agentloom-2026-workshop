# Contributing — UCGIS 2026 workshop fork-and-PR flow

Workshop day goal: leave with a **working catalog** you built and an **open PR** back to this repo.

## 1. Fork and branch

1. Fork `Keven1894/ucgis-agentloom-2026-workshop` on GitHub.
2. Clone your fork locally.
3. Create a branch: `workshop-<github-handle>` (e.g. `workshop-jdoe`).

```bash
git checkout -b workshop-jdoe
```

## 2. Governance floor (non-negotiable)

From your **first commit**, these must pass locally and in CI:

```bash
make validate-all
```

- Tier-A behavior validators are executable — not suggestions.
- Paired-commit discipline: KG changes and code changes stay in sync.
- Agents **propose** KG nodes; humans **accept** via `accept_proposal.py`.

## 3. Typical workflow

| Step | Who | Action |
| --- | --- | --- |
| Discover | You + Cline (MCP) | `kg_search`, read `notes/data-sources.md` |
| Propose | Cline | `python scripts/kg/propose_node.py ...` |
| Review | You | `make dashboard` → Proposals tab |
| Accept | You | `python scripts/kg/accept_proposal.py <id>` |
| Implement | You + Cline | Build `starter/<your-source>/`, wire validators |
| Verify | You | `make validate-all` |
| Ship | You | Push branch, open PR |

Full checklist: [`docs/workshop/00-workshop-workflow.md`](docs/workshop/00-workshop-workflow.md).

## 4. Opening a PR

Use the PR template. Include:

- Which data source (D1–D4 or BYO)
- Screenshot or short note that dashboard shows your accepted nodes
- Confirmation that `make validate-all` passes

CI runs validators on every PR. Fix failures before asking for review.

## 5. What not to do

- Do not edit `*-graph.json` directly — use propose/accept.
- Do not commit API keys (use `.env`, gitignored).
- Do not copy a completed catalog from the dev repo — build from the framework floor.

## Questions on workshop day

Ask organizers or refer to [`docs/workshop/kg-access-and-human-review.md`](docs/workshop/kg-access-and-human-review.md).
