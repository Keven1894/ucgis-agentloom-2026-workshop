# Git repos — usage & deployment (operator runbook)

**Last updated**: 2026-05-31  
**Audience**: organizers (Keven + team) — not attendees  
**Status**: source of truth for **clone, push, snapshot, and tag** workflows  
**Related**: [`13-hosting-three-repos-and-dual-origin.md`](../../../envistor-data/docs/research/workshop-ucgis-2026/13-hosting-three-repos-and-dual-origin.md) (envistor copy)

---

## 1. Three repos at a glance

| Repo | Host | Who clones | Upstream for PRs |
| --- | --- | --- | --- |
| **ucgis-agentloom-2026** | Gitea `origin` + Bitbucket `backup` | FIU team only | — |
| **ucgis-agentloom-2026-workshop** | GitHub public | Attendees + friend test | `Keven1894/ucgis-agentloom-2026-workshop` |
| **AgentLoom** | GitHub public | Paper readers / framework adopters | `Keven1894/AgentLoom` |

**Golden rule**: workshop repo is **derived**. Never fix attendee-facing bugs only on GitHub — patch **dev `main` first**, then re-snapshot.

---

## 2. Dev repo — daily work

### 2.1 Clone (team)

```bash
git clone https://dpanther04devtemp.fiu.edu/gitea/fiugiscenter/ucgis-agentloom-2026.git
cd ucgis-agentloom-2026
git remote add backup https://bitbucket.org/fiugiscenter/ucgis-agentloom-2026.git   # if missing
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt   # Windows
```

Local path (operator): `C:\projects\ucgis-agentloom-2026`

### 2.2 Push both remotes

```bash
git push origin <branch>
git push backup <branch>
```

Branches: `main`, `d1`–`d4`, `feature/*`, experiment branches.

### 2.3 Tags (traceability)

After a workshop snapshot ships, tag dev at the source commit:

```bash
git tag workshop-day-rc2 <short-sha>    # e.g. 429aeeb
git push origin workshop-day-rc2
git push backup workshop-day-rc2
```

Final workshop tag: `workshop-day-2026-06-15` on dev + GitHub workshop `main`.

---

## 3. Workshop repo — snapshot & publish

### 3.1 When to snapshot

| Trigger | Action |
| --- | --- |
| Doc/script fix on dev `main` that attendees need | Re-snapshot → push GitHub `main` |
| Named milestone | Tag `workshop-day-rc1`, `rc2`, … |
| Workshop eve | Tag `workshop-day-2026-06-15` |

**Cadence**: ~Jun 7–10 RC2 (done 2026-05-31), final snapshot ~Jun 13–14.

### 3.2 Build snapshot (Windows)

Output directory **must not exist**. `make` is optional — validate with Python if `make` unavailable.

```bash
cd C:\projects\ucgis-agentloom-2026

# 1. Build to a fresh temp dir
.venv\Scripts\python scripts\build_workshop_snapshot.py --ref main --output C:\Users\<you>\AppData\Local\Temp\ws-snapshot-out

# 2. Validate (no make required)
cd C:\Users\<you>\AppData\Local\Temp\ws-snapshot-out
C:\projects\ucgis-agentloom-2026\.venv\Scripts\python scripts\validators\run_all.py
C:\projects\ucgis-agentloom-2026\.venv\Scripts\python scripts\kg\validate_all.py
```

**Excluded from snapshot** (by `build_workshop_snapshot.py`):

- `docs/plan/`, `docs/research/`, `runs/`, `starter/`, `scripts/domain/`
- Pending proposals (`agents/knowledge-graphs/proposals/*.json`)
- Operator-only docs: `W7-dress-rehearsal-runbook.md`, `dress-rehearsal-2026-05-31.md`

### 3.3 Publish to GitHub (recommended: fresh clone)

Avoid syncing into a tree with a live `.venv` (Windows file locks). Use a clean publish clone:

```bash
git clone --branch main https://github.com/Keven1894/ucgis-agentloom-2026-workshop.git C:\Temp\ws-publish
cd C:\Temp\ws-publish

# Replace all files except .git with snapshot tree (Python one-liner or manual copy)
# Write WORKSHOP-SNAPSHOT.txt:
#   source_repo=ucgis-agentloom-2026
#   source_ref=<dev-short-sha>
#   snapshot_tag=workshop-day-rc2

git add -A
git commit -m "Workshop snapshot RC2 from dev main @ <sha>"
git tag workshop-day-rc2
git push origin main
git push origin workshop-day-rc2
```

**Live URLs**

- Workshop: https://github.com/Keven1894/ucgis-agentloom-2026-workshop  
- Latest RC: tag `workshop-day-rc2` (2026-05-31, dev `@429aeeb`)

### 3.4 Attendee clone (what we tell them)

```bash
git clone https://github.com/<their-handle>/ucgis-agentloom-2026-workshop.git
cd ucgis-agentloom-2026-workshop
git checkout -b workshop-<handle>
```

Fork first on GitHub; PR upstream = `Keven1894/ucgis-agentloom-2026-workshop`.

### 3.5 Operator rehearsal branches

Organizer dry-runs (e.g. `workshop-keven-w7`) are **personal branches** on a fork or local clone. Do **not** merge rehearsal catalogs into public `main`. Evidence stays on the rehearsal branch for paper / friction logs.

---

## 4. AgentLoom repo (paper P5)

Framework IP lives at `Keven1894/AgentLoom`. Sync from dev `main` before SoftwareX submission (~Jun 7):

1. Copy builder agent package, validators, `.clinerules` discipline docs  
2. Tag `v3.0-ucgis` (pre-workshop) / `v4.0` (post-workshop)  
3. GitHub Release → Zenodo DOI  

Details: paper track [`docs/plan/todo/2026-05-23-paper-track.md`](../plan/todo/2026-05-23-paper-track.md) P5.

---

## 5. Cline MCP config (global, not in repo)

Cline stores MCP at:

```text
%APPDATA%\Code\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json
```

**Must point at the clone you have open** — `.venv/Scripts/python.exe` + `scripts/mcp_kg_server.py` paths. Switch when changing forks. Documented in [`01-setup.md`](./01-setup.md) Step 5b.

---

## 6. Checklist — snapshot release

| Step | Done? |
| --- | --- |
| Dev `main` validators green | ☐ |
| `build_workshop_snapshot.py --ref main` → temp dir | ☐ |
| `run_all.py` + `validate_all.py` PASS on snapshot | ☐ |
| `WORKSHOP-SNAPSHOT.txt` records dev SHA + tag | ☐ |
| Push GitHub workshop `main` | ☐ |
| Tag `workshop-day-rcN` on GitHub + dev | ☐ |
| Smoke: fresh clone + `test_mcp_kg_tools.py` PASS | ☐ |
| Announce tag in team channel / W8 friend test brief | ☐ |

---

## 7. What never goes in git

- `.env` with real API keys  
- `dist/` build artifacts (gitignored)  
- Attendee rehearsal catalogs on public `main`  
- Eval transcripts / pending proposals (stripped by snapshot script)

---

## Cross-links

| Doc | Role |
| --- | --- |
| [`01-setup.md`](./01-setup.md) | Attendee bootstrap |
| [`00-workshop-workflow.md`](./00-workshop-workflow.md) | Phases A–F |
| [`scripts/build_workshop_snapshot.py`](../../scripts/build_workshop_snapshot.py) | Snapshot implementation |
| envistor [`13-hosting-three-repos-and-dual-origin.md`](../../../envistor-data/docs/research/workshop-ucgis-2026/13-hosting-three-repos-and-dual-origin.md) | Hosting decisions |
