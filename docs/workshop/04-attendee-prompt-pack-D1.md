# 04 (D1) — Attendee prompt pack: USGS Earthquakes (Track B — workshop day)

**Last updated**: 2026-06-14
**Audience**: attendees + lecturer
**Use with**: [`03-data-source-menu.md`](./03-data-source-menu.md) · Cline Act mode · gpt-5.2 @ 0.2
**Default pack**: [`04-attendee-prompt-pack.md`](./04-attendee-prompt-pack.md) (D3 streamflow). This file is the **D1 sibling** — same flow, earthquake-specific prompts.

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

## D1 at a glance (workshop day)

| | |
| --- | --- |
| **Snapshot** | `data/snapshots/d1-usgs-earthquakes-week.geojson` (GeoJSON FeatureCollection) |
| **Catalog dir** | `starter/earthquake-catalog/` |
| **Auth** | none |
| **Distinctive lesson** | epoch-**millisecond** timestamps; GeoJSON `[lon, lat, depth]` order; many nullable fields |
| **Expected on map** | every event in the snapshot (~1.5k–2.5k), circle markers sized by magnitude — **no** magnitude filter |

**Contrast with D3**: D1 is a single GeoJSON file (no scale-enrich Phase 5b, no normalize Phase 6). Its foot-guns are timestamps + coordinate order + nulls, not nested time-series + sentinels.

**Lecturer line**: "Same protocol as D3 — different foot-guns. The framework didn't change; the KG nodes did."

---

## Phase 0 — Already done in Block 0

See [`01-setup.md`](./01-setup.md). Pass = `test_mcp_kg_tools.py` PASS + dashboard Proposals tab loads.

---

## Phase 1 — Quickstart (Block 2, all room)

If not done: complete [`02-quickstart.md`](./02-quickstart.md) Steps 1–6 once.

---

## Phase 2 — Discovery (new Cline task)

```
Workshop main task — data source D1 (USGS Earthquakes, all_week GeoJSON). Discovery only.

1. Read docs/workshop/03-data-source-menu.md section D1.
2. Read the first 8000 bytes of data/snapshots/d1-usgs-earthquakes-week.geojson.
3. MCP kg_search for several queries: "epoch milliseconds", "geojson coordinates",
   "longitude latitude order", "nullable fields", "timestamp" with role=domain.
4. MCP kg_list_proposals — report count only.
5. Summarize in bullets:
   - GeoJSON structure (where coordinates, magnitude, place, time live)
   - timestamp format + units (epoch seconds? ms? ISO 8601?)
   - coordinate order and how many elements per coordinate
   - which properties are nullable / unreliable
   - gaps: what the domain KG does NOT yet know

Do NOT propose yet. Stop after summary.
```

**Pass**: 3–5 concrete foot-guns surfaced (epoch ms, lon-lat-depth order, nullable fields); MCP used; no `*-graph.json` reads.

---

## Phase 3 — Autonomous propose (Track B)

**One Cline task per proposal** (recommended). Cline must derive slug/title/justification from Phase 2.

### Task template (repeat 2–3×)

```
Workshop Track B — propose ONE domain knowledge node from your D1 discovery summary.

Pick the next highest-risk gap not yet proposed (epoch-ms time, lon/lat/depth coordinate
order, nullable optional fields, etc.).

1. MCP kg_search to confirm the topic is not already covered.
2. Run scripts/kg/propose_node.py (.venv python) with:
   --type knowledge --target-role domain
   --slug <kebab-case you choose>
   --title "<short title>"
   --justification "<one sentence why catalog code must know this>"
   --source-context "data/snapshots/d1-usgs-earthquakes-week.geojson + your observation"
   --path docs/domain/proposed/<same-slug>.md
3. Write docs/domain/proposed/<slug>.md stub (~20 lines) with evidence from the snapshot.

Do NOT run accept_proposal.py. Stop after one successful propose.
```

**Human gate**: dashboard review → `accept_proposal.py` for each proposal.

**Lecturer reference — D1 nodes** (Cline should converge on these; slugs may vary):

| Slug | Why catalog code must know it |
| --- | --- |
| `usgs-quake-time-is-epoch-milliseconds` | `properties.time` is epoch **ms** — pass to `new Date(ms)`, never ÷1000 |
| `usgs-quake-coords-are-lon-lat-depth` | `[lon, lat, depth_km]`, lon first; Leaflet wants `[lat, lon]`; pad 2-tuples to depth=null |
| `usgs-quake-many-nullable-fields` | `felt/cdi/mmi/tsunami/alert` often null; `mag` can be null/negative; `place` is free text |

**Anti-pattern (Track C — do not use on workshop day)**:

```
❌ Operator pastes full --slug usgs-quake-time-is-epoch-milliseconds …
```

---

## Phase 4 — Catalog shell (new Cline task)

```
Build starter/earthquake-catalog/index.html — scaffolding only.

Requirements:
- HTML5 + Leaflet 1.9.4 (unpkg)
- Top bar + sidebar + div#map
- All 8 data-catalog-role sections (>=10 chars each): title, provenance, acquisition, data-shape, processing, kg-link, reuse, data-view
- data-view contains div#map
- One application/ld+json Schema.org Dataset (name, description, url, license, creator, distribution, dateModified)
- Placeholder world map; no data fetch yet
- kg-link references accepted domain nodes by title

Do NOT copy external repos. Run scripts/validators/run_all.py until PASS.
```

---

## Phase 5 — Wire vendored data (new Cline task)

```
Wire starter/earthquake-catalog/index.html to data/snapshots/d1-usgs-earthquakes-week.geojson.

- Fetch with relative path from starter/earthquake-catalog/ (../../data/snapshots/...)
- Parse features[]: geometry.coordinates [lon,lat,depth] (swap to [lat,lon] for Leaflet),
  properties.mag, properties.place, properties.time
- Convert properties.time (epoch MS) to a readable UTC string with new Date(ms) per the accepted KG node
- Size circle markers by magnitude; tolerate null optional fields (use MCP kg_search)
- Update data-shape and processing sections to match the actual JS

Run scripts/validators/run_all.py until PASS. Report event count on map.

If fetch fails on file://, note: python -m http.server 8766 from repo root.
```

**Pass**: all snapshot events plotted; epoch-ms times render as readable UTC; validators green.

> **Note**: D1 has **no Phase 5b** (single file — nothing to scale-enrich) and **no Phase 6** (no normalize script needed). Go straight to narrative polish.

---

## Phase 5c — Narrative polish via KG (new Cline task, ~10 min)

**When**: catalog works and the map renders, but a human still asks "what am I looking at?"

```
Workshop Track B — narrative polish (story map).

1. MCP kg_search "story map viewer questions catalog narrative" role=domain and role=builder.
2. If knowledge:domain:story-map-must-answer-four-viewer-questions is missing, propose ONE node:
   - Four plain-language questions: where from, what is it, how to reuse, what is on screen NOW
   - Justification: behavior:builder:catalog-ui-must-tell-the-story is structural only;
     first-time viewers need at-a-glance answers without JSON paths
   - path docs/domain/proposed/story-map-must-answer-four-viewer-questions.md
3. Human accepts on dashboard.
4. Polish starter/earthquake-catalog/index.html:
   - Add an "At a glance" panel (populate from loaded data where possible: count, max magnitude, time span)
   - Rewrite provenance / data-shape / reuse in plain language
   - Link the new node in kg-link
5. run_all.py PASS.

Do NOT propose GeoJSON parsing rules again — this phase is narrative only.
```

**Pass**: four viewer questions answerable without reading code; new KG node accepted; validators green.

---

## Phase 7 — Close + PR

Human:

```bash
.venv/Scripts/python scripts/validators/run_all.py   # Windows
.venv/bin/python scripts/validators/run_all.py        # macOS/Linux
git add starter/ docs/domain/ agents/knowledge-graphs/
git commit -m "UCGIS workshop: D1 earthquake catalog"
git push -u origin workshop-<handle>
```

Open PR to upstream: https://github.com/Keven1894/ucgis-agentloom-2026-workshop

---

## Cross-links

- Default pack (D3): [`04-attendee-prompt-pack.md`](./04-attendee-prompt-pack.md)
- Data source menu: [`03-data-source-menu.md`](./03-data-source-menu.md)
- Operator rehearsal (Track C): [`W7-dress-rehearsal-runbook.md`](./W7-dress-rehearsal-runbook.md) — dev repo only, not in public snapshot
- Slides: [`06-slides-outline-draft.md`](./06-slides-outline-draft.md)
