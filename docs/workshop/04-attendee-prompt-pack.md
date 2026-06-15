# 04 — Attendee prompt pack (Track B — workshop day)

**Last updated**: 2026-06-02  
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

## D3 three-act flow (workshop day)

| Act | Snapshot | Sites | Domain KG |
| --- | --- | --- | --- |
| **Discovery + propose** | `d3-usgs-nwis-suwannee-24h.json` | 1 (small, easy to read) | 2–3 nodes on schema foot-guns |
| **Phase 5 wire** | same Suwannee file | 1 marker | reuse accepted nodes |
| **Phase 5b scale enrich** | `d3-usgs-nwis-fl-stations-24h.json` | 6 markers | **no new KG required** — same rules, wider data |
| **Phase 5c narrative polish** | same multi-site UI | readable story map | **propose + accept** `story-map-must-answer-four-viewer-questions` |

**Lecturer line (5b)**: "The memory layer paid off in Phase 2–3. Scaling to six stations is one snapshot swap — not a new prompt."

**Lecturer line (5c)**: "Validators green ≠ a stranger understands the page. Capture the narrative rule in KG, then polish."

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

## Phase 5 — Wire vendored data (single site, new Cline task)

```
Wire starter/streamflow-catalog/index.html to data/snapshots/d3-usgs-nwis-suwannee-24h.json.

- Fetch with relative path from starter/streamflow-catalog/
- Parse sites, lat/lon, parameterCode, values; filter sentinels per accepted domain KG (use MCP kg_search)
- Leaflet markers + sidebar list
- Update data-shape and processing sections to match actual JS

Run scripts/validators/run_all.py until PASS. Report site count on map (expect 1).

If fetch fails on file://, note: python -m http.server 8766 from repo root.
```

**Pass**: map shows 1 NWIS site; validators green.

---

## Phase 5b — Scale enrich (new Cline task, ~5 min)

```
D3 scale enrich — swap snapshot only (no new domain KG unless you found a NEW foot-gun).

In starter/streamflow-catalog/index.html:
1. Change fetch URL to ../../data/snapshots/d3-usgs-nwis-fl-stations-24h.json
2. Keep the same parser — value.timeSeries[] already loops per site
3. Update provenance, acquisition, JSON-LD distribution contentUrl, and title if needed
4. Report site count (expect 6) and confirm map fitBounds shows all Florida markers

Run scripts/validators/run_all.py until PASS.
```

**Pass**: 6 sites plotted; same 3 domain KG nodes still apply; validators green.

---

## Phase 5c — Narrative polish via KG (new Cline task, ~10 min)

**When**: catalog works and maps render, but a human still asks "what am I looking at?"

```
Workshop Track B — narrative polish (story map).

1. MCP kg_search "story map viewer questions catalog narrative" role=domain and role=builder.
2. If knowledge:domain:story-map-must-answer-four-viewer-questions is missing, propose ONE node:
   - Four plain-language questions: where from, what is it, how to reuse, what is on screen NOW
   - Justification: behavior:builder:catalog-ui-must-tell-the-story is structural only;
     first-time viewers need at-a-glance answers without JSON paths
   - path docs/domain/proposed/story-map-must-answer-four-viewer-questions.md
3. Human accepts on dashboard.
4. Polish starter/streamflow-catalog/index.html:
   - Add an "At a glance" panel (populate from loaded data where possible)
   - Rewrite provenance / data-shape / reuse in plain language
   - Link the new node in kg-link
5. run_all.py PASS.

Do NOT propose NWIS parsing rules again — this phase is narrative only.
```

**Pass**: four viewer questions answerable without reading code; new KG node accepted; validators green.

---

## Phase 6 — Optional normalize script

```
Optional: scripts/domain/d3_nwis_to_iso.py → dist/d3-normalized.iso.json (UTC-Z).
Use d3-usgs-nwis-fl-stations-24h.json as input if Phase 5b done.
Wire catalog to prefer dist/ when present. run_all.py PASS.
```

---

## Phase 7 — Close + PR

Human:

```bash
.venv/Scripts/python scripts/validators/run_all.py   # Windows
.venv/bin/python scripts/validators/run_all.py        # macOS/Linux
git add starter/ docs/domain/ agents/knowledge-graphs/ dist/
git commit -m "UCGIS workshop: D3 streamflow catalog"
git push -u origin workshop-<handle>
```

Open PR to upstream: https://github.com/Keven1894/ucgis-agentloom-2026-workshop

---

## Cross-links

- Operator rehearsal (Track C): [`W7-dress-rehearsal-runbook.md`](./W7-dress-rehearsal-runbook.md) — dev repo only, not in public snapshot  
- Slides: [`06-slides-outline-draft.md`](./06-slides-outline-draft.md)
