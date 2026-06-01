# 04 — Attendee prompt pack (Track B — workshop day)

**Last updated**: 2026-05-31  
**Audience**: attendees + lecturer  
**Use with**: [`03-data-source-menu.md`](./03-data-source-menu.md) · Cline Act mode · gpt-5.2 @ 0.2

---

## Track A vs Track B vs Track C

| Track | Who | Propose step | Purpose |
| --- | --- | --- | --- |
| **A** | Attendee | Follow [`02-quickstart.md`](./02-quickstart.md) scripted tutorial | Learn CLI once |
| **B** | Attendee | **Cline discovers → autonomously proposes** | **Workshop day canonical** |
| **C** | Operator rehearsal | Operator pastes full `propose_node.py` args | Plumbing / timing test only |

**Rule (all tracks)**: Cline never runs `accept_proposal.py`. Human accepts on dashboard.

**Rule (Track B)**: Do **not** paste slug/title/justification unless Cline already proposed them from discovery. If Cline asks what to propose, reply: "Use your discovery summary — pick the highest-risk foot-guns and propose 1–3 knowledge nodes yourself."

Append to every task:

```
Do NOT read agents/knowledge-graphs/*-graph.json directly.
Use MCP kg_search / kg_get_node / kg_list_proposals for KG context.
```

---

## Phase 0 — Already done in Block 0

See [`01-setup.md`](./01-setup.md). Pass = `test_mcp_kg_tools.py` PASS + dashboard Proposals tab loads.

---

## Phase 1 — Quickstart (Block 2, all room)

If not done: complete [`02-quickstart.md`](./02-quickstart.md) Steps 1–6 once.

---

## Phase 2 — Discovery (new Cline task)

Replace `D3` / `D2` / `D4` and paths per your source from [`03-data-source-menu.md`](./03-data-source-menu.md).

```
Workshop main task — data source D3 (USGS NWIS streamflow). Discovery only.

1. Read docs/workshop/03-data-source-menu.md section D3.
2. Read the first 8000 bytes of data/snapshots/d3-usgs-nwis-suwannee-24h.json.
3. MCP kg_search for several queries: "sentinel", "nwis", "streamflow", "parameter code", "site id" with role=domain.
4. MCP kg_list_proposals — report count only.
5. Summarize in bullets:
   - JSON nesting (where site id, parameter code, values live)
   - sentinel / no-data values observed
   - timestamp / timezone quirks
   - gaps: what the domain KG does NOT yet know

Do NOT propose yet. Stop after summary.
```

**Pass**: 3–5 concrete foot-guns; MCP used; no `*-graph.json` reads.

---

## Phase 3 — Autonomous propose (Track B)

**One Cline task per proposal** (recommended). Cline must derive slug/title/justification from Phase 2.

### Task template (repeat 2–3×)

```
Workshop Track B — propose ONE domain knowledge node from your D3 discovery summary.

Pick the next highest-risk gap not yet proposed (sentinel values, parameter codes, nesting, timestamps, etc.).

1. MCP kg_search to confirm the topic is not already covered.
2. Run scripts/kg/propose_node.py (.venv python) with:
   --type knowledge --target-role domain
   --slug <kebab-case you choose>
   --title "<short title>"
   --justification "<one sentence why catalog code must know this>"
   --source-context "data/snapshots/d3-usgs-nwis-suwannee-24h.json + your observation"
   --path docs/domain/proposed/<same-slug>.md
3. Write docs/domain/proposed/<slug>.md stub (~20 lines) with evidence from the snapshot.

Do NOT run accept_proposal.py. Stop after one successful propose.
```

**Human gate**: dashboard review → `accept_proposal.py` for each proposal.

**Anti-pattern (Track C — do not use on workshop day)**:

```
❌ Operator pastes full --slug nwis-sentinel-minus-999999-means-no-data …
```

---

## Phase 4 — Catalog shell (new Cline task)

```
Build starter/streamflow-catalog/index.html — scaffolding only.

Requirements:
- HTML5 + Leaflet 1.9.4 (unpkg)
- Top bar + sidebar + div#map
- All 8 data-catalog-role sections (>=10 chars each): title, provenance, acquisition, data-shape, processing, kg-link, reuse, data-view
- data-view contains div#map
- One application/ld+json Schema.org Dataset (name, description, url, license, creator, distribution, dateModified)
- Placeholder map (Florida center); no data fetch yet
- kg-link references accepted domain nodes by title

Do NOT copy external repos. Run scripts/validators/run_all.py until PASS.
```

---

## Phase 5 — Wire vendored data (new Cline task)

```
Wire starter/streamflow-catalog/index.html to data/snapshots/d3-usgs-nwis-suwannee-24h.json.

- Fetch with relative path from starter/streamflow-catalog/
- Parse sites, lat/lon, parameterCode, values; filter sentinels per accepted domain KG (use MCP kg_search)
- Leaflet markers + sidebar list
- Update data-shape and processing sections to match actual JS

Run scripts/validators/run_all.py until PASS. Report site count on map.

If fetch fails on file://, note: python -m http.server 8766 from repo root.
```

---

## Phase 6 — Optional normalize script

```
Optional: scripts/domain/d3_nwis_to_iso.py → dist/d3-normalized.iso.json (UTC-Z).
Wire catalog to prefer dist/ when present. run_all.py PASS.
```

---

## Phase 7 — Close + PR

Human:

```bash
.venv/Scripts/python scripts/validators/run_all.py
git add starter/ docs/domain/ agents/knowledge-graphs/
git commit -m "UCGIS workshop: D3 streamflow catalog"
git push -u origin workshop-<handle>
```

Open PR to `Keven1894/ucgis-agentloom-2026-workshop`.

---

## Cross-links

- Operator rehearsal (Track C): [`W7-dress-rehearsal-runbook.md`](./W7-dress-rehearsal-runbook.md) — dev repo only, not in public snapshot  
- Slides: [`06-slides-outline-draft.md`](./06-slides-outline-draft.md)
