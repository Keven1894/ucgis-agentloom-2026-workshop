# Git repo — usage & deployment (operator runbook)

**Last updated**: 2026-06-14
**Audience**: organizers (Keven + team) — not attendees
**Status**: source of truth for **clone, edit, push, and tag** of the workshop repo

---

## 1. The repo

| Repo | Host | Who clones | Upstream for PRs |
| --- | --- | --- | --- |
| **ucgis-agentloom-2026-workshop** | GitHub (public) | Organizers + attendees | `Keven1894/ucgis-agentloom-2026-workshop` |

There is **one** workshop repo. We edit a local clone and push directly to GitHub `main`.
Attendees fork that GitHub repo. There is **no separate dev/source repo and no snapshot
build step** — what is on GitHub `main` is what attendees get.

> The AgentLoom framework itself lives in its own public repos
> (`Keven1894/AgentLoom`, `Keven1894/agentloom-runtime`); those are managed separately and
> are out of scope for this runbook.

---

## 2. Daily work (organizers)

### 2.1 Clone

```bash
git clone https://github.com/Keven1894/ucgis-agentloom-2026-workshop.git
cd ucgis-agentloom-2026-workshop

# macOS/Linux
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# Windows
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

Local path (this machine): `~/Documents/projs/01_agentloom/ucgis-agentloom-2026-workshop`

### 2.2 Edit → commit → push

Changes to attendee-facing docs/scripts go straight onto `main`:

```bash
git add <files>
git commit -m "<message>"
git push origin main
```

Use feature branches for larger or in-progress work, then merge to `main` when ready.

### 2.3 Tags (optional, for traceability)

Tag milestones so you can point friend-testers / attendees at a known-good state:

```bash
git tag workshop-day-2026-06-15
git push origin workshop-day-2026-06-15
```

---

## 3. Attendee flow (what we tell them)

```bash
# 1. Fork on GitHub: Keven1894/ucgis-agentloom-2026-workshop
# 2. Clone YOUR fork
git clone https://github.com/<their-handle>/ucgis-agentloom-2026-workshop.git
cd ucgis-agentloom-2026-workshop
git checkout -b workshop-<handle>
```

PRs go upstream to `Keven1894/ucgis-agentloom-2026-workshop`.

**Framework-only**: the attendee fork ships the framework, **not** finished catalogs or a
pre-filled domain KG. Attendees build their own catalog and propose their own KG nodes. Keep
it that way — see §5.

---

## 4. What never goes in git

Already ignored by `.gitignore`:

- `.venv/`, `venv/`
- `.env`, `.env.local` (real API keys)
- `starter/` — **your** staged catalogs while building or demo staging copies. Never commit.
- `dist/` — build artifacts (except intentional normalized outputs you choose to vendor)
- `*.log`

⚠️ **Not ignored — do not commit by reflex**:

- `docs/plan/` — operator planning notes (if present locally). Prefer keeping these outside the repo.

**Now public on `main`:**

- `demo/reference/` — finished D1–D4 reference builds (catalog HTML, domain KG snapshots, PROMPTS drafts, screenshots). Attendees compare against these; they still build their own catalog in a separate fork checkout.

Prefer `git add <explicit paths>` over `git add -A` so `starter/` doesn't sneak in.

Stage demo catalogs locally with `bash demo/reference/serve_demo.sh stage` (or `bash demo/serve/serve-all.sh`).
Clean with `bash demo/reference/serve_demo.sh clean`.

---

## 5. Keep the teaching closure intact

Attendees still **build their own catalog and propose their own domain KG nodes** in their fork.
The public `demo/reference/` builds are for **comparison and browsing**, not a shortcut into
`agents/knowledge-graphs/` or `starter/`.

On public `main`:

- **Domain KG stays root-only** in `agents/knowledge-graphs/`. `test_mcp_kg_tools.py` asserts this.
  Demo domain graphs live under `demo/reference/<id>/` and appear only via dashboard `?ref=` overlay.
- **Do not commit `starter/`** — practice catalogs and demo staging stay local/gitignored.
- **Rehearsal catalogs on personal branches** — do not merge attendee practice work into public
  `main` unless intentionally curating showcase examples.

---

## 6. Cline MCP config (global, not in repo)

Cline stores MCP server config **outside** the repo, globally:

```text
# macOS/Linux
~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json

# Windows
%APPDATA%\Code\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json
```

It must point at the clone you have open (`.venv` python + `scripts/mcp_kg_server.py` paths).
Update it when you switch clones/forks. See [`01-setup.md`](./01-setup.md) Step 5b.

---

## 7. Release checklist

| Step | Done? |
| --- | --- |
| `starter/` empty, `docs/plan/` not staged | ☐ |
| Validators green: `.venv/bin/python scripts/validators/run_all.py` | ☐ |
| KG check: `.venv/bin/python scripts/kg/validate_all.py` | ☐ |
| Commit + push GitHub `main` | ☐ |
| (optional) Tag the milestone on GitHub | ☐ |
| Smoke: fresh clone + `test_mcp_kg_tools.py` PASS | ☐ |
| Announce to team / friend-test brief | ☐ |

---

## Cross-links

| Doc | Role |
| --- | --- |
| [`01-setup.md`](./01-setup.md) | Attendee bootstrap |
| [`00-workshop-workflow.md`](./00-workshop-workflow.md) | Phases A–F |
| [`README.md`](./README.md) | Doc index |
