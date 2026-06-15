# 04 (D4) — Attendee prompt pack: Natural Earth Admin-0 (Track B — workshop day)

**Last updated**: 2026-06-14
**Audience**: attendees + lecturer
**Use with**: [`03-data-source-menu.md`](./03-data-source-menu.md) · Cline Act mode · gpt-5.2 @ 0.2
**Default pack**: [`04-attendee-prompt-pack.md`](./04-attendee-prompt-pack.md) (D3 streamflow). This file is the **D4 sibling** — same flow, Natural Earth-specific prompts.

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

## D4 at a glance (workshop day)

| | |
| --- | --- |
| **Snapshot** | `data/snapshots/d4-natural-earth-admin0.geojson` (GeoJSON FeatureCollection) |
| **Catalog dir** | `starter/boundaries-catalog/` |
| **Auth** | none |
| **Distinctive lesson** | hyphenated ISO property keys; **basemap/join layer** (not event points); MultiPolygon + large file |
| **Expected on map** | all ~258 country polygons; click for name + ISO Alpha-2/3 |

**Contrast with D1/D2/D3**: D4 is polygon context for choropleth/joins — you do **not** ingest boundaries as if they were sensor readings or earthquake events.

**Lecturer line**: "Same protocol — different geometry role. Natural Earth teaches property-name foot-guns and basemap thinking."

---

## Phase 0 — Already done in Block 0

See [`01-setup.md`](./01-setup.md). Pass = `test_mcp_kg_tools.py` PASS + dashboard Proposals tab loads.

---

## Phase 1 — Quickstart (Block 2, all room)

If not done: complete [`02-quickstart.md`](./02-quickstart.md) Steps 1–6 once.

---

## Phase 2 — Discovery (new Cline task)

```
Workshop main task — data source D4 (Natural Earth Admin 0). Discovery only.

1. Read docs/workshop/03-data-source-menu.md section D4.
2. Read the first 8000 bytes of data/snapshots/d4-natural-earth-admin0.geojson.
3. MCP kg_search for several queries: "natural earth iso", "admin 0", "multipolygon",
   "basemap join", "geojson properties" with role=domain.
4. MCP kg_list_proposals — report count only.
5. Summarize in bullets:
   - geometry types (Polygon vs MultiPolygon)
   - exact property keys for country name and ISO codes
   - file size / first-load performance
   - how this dataset differs from point/event feeds (D1/D2/D3)
   - gaps: what the domain KG does NOT yet know

Do NOT propose yet. Stop after summary.
```

**Pass**: 3–5 concrete foot-guns (hyphenated ISO keys, basemap role, MultiPolygon, file size); MCP used; no `*-graph.json` reads.

---

## Phase 3 — Autonomous propose (Track B)

**One Cline task per proposal** (recommended). Cline must derive slug/title/justification from Phase 2.

### Task template (repeat 2–3×)

```
Workshop Track B — propose ONE domain knowledge node from your D4 discovery summary.

Pick the next highest-risk gap not yet proposed (ISO property spelling, basemap vs events,
MultiPolygon complexity, large GeoJSON load, etc.).

1. MCP kg_search to confirm the topic is not already covered.
2. Run scripts/kg/propose_node.py (.venv python) with:
   --type knowledge --target-role domain
   --slug <kebab-case you choose>
   --title "<short title>"
   --justification "<one sentence why catalog code must know this>"
   --source-context "data/snapshots/d4-natural-earth-admin0.geojson + your observation"
   --path docs/domain/proposed/<same-slug>.md
3. Write docs/domain/proposed/<slug>.md stub (~20 lines) with evidence from the snapshot.

Do NOT run accept_proposal.py. Stop after one successful propose.
```

**Human gate**: dashboard review → `accept_proposal.py` for each proposal.

**Lecturer reference — D4 nodes** (Cline should converge on these; slugs may vary):

| Slug | Why catalog code must know it |
| --- | --- |
| `natural-earth-iso-property-names-hyphenated` | use `ISO3166-1-Alpha-3` / `-Alpha-2` — not legacy `iso_a2` |
| `natural-earth-is-basemap-not-event-stream` | boundaries are join/context layer — not time-series ingestion |
| `natural-earth-multipolygon-complexity` | expect MultiPolygon (e.g. Antarctica); ~15 MB GeoJSON; HTTP serve required |

**Anti-pattern (Track C — do not use on workshop day)**:

```
❌ Operator pastes full --slug natural-earth-iso-property-names-hyphenated …
```

---

## Phase 4 — Catalog shell (new Cline task)

```
Build starter/boundaries-catalog/index.html — scaffolding only.

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
Wire starter/boundaries-catalog/index.html to data/snapshots/d4-natural-earth-admin0.geojson.

- Fetch with relative path from starter/boundaries-catalog/ (../../data/snapshots/...)
- L.geoJSON with styled polygon fills; onEachFeature popup with name, ISO3166-1-Alpha-3, ISO3166-1-Alpha-2
- fitBounds after layer loads; show loading badge while fetching (~15 MB)
- Use bracket notation for hyphenated property keys per accepted KG node
- Update data-shape and processing sections to match the actual JS

Run scripts/validators/run_all.py until PASS. Report feature count.

If fetch fails on file://, note: python -m http.server 8766 from repo root.
```

**Pass**: all countries render; popups show correct ISO codes; validators green.

> **Note**: D4 has **no Phase 5b** and **no Phase 6**. Optional stretch: join another dataset by ISO — not required for workshop pass.

---

## Phase 5c — Narrative polish via KG (new Cline task, ~10 min)

**When**: choropleth renders, but a human still asks "what am I looking at?"

```
Workshop Track B — narrative polish (story map).

1. MCP kg_search "story map viewer questions catalog narrative" role=domain and role=builder.
2. If knowledge:domain:story-map-must-answer-four-viewer-questions is missing, propose ONE node:
   - Four plain-language questions: where from, what is it, how to reuse, what is on screen NOW
   - Justification: behavior:builder:catalog-ui-must-tell-the-story is structural only;
     first-time viewers need at-a-glance answers without JSON paths
   - path docs/domain/proposed/story-map-must-answer-four-viewer-questions.md
3. Human accepts on dashboard.
4. Polish starter/boundaries-catalog/index.html:
   - Add an "At a glance" panel (feature count, MultiPolygon note)
   - Rewrite provenance / data-shape / reuse in plain language — emphasize basemap/join role
   - Link the new node in kg-link
5. run_all.py PASS.

Do NOT re-propose ISO key rules — this phase is narrative only.
```

**Pass**: four viewer questions answerable without reading code; validators green.

---

## Phase 7 — Close + PR

Human:

```bash
.venv/Scripts/python scripts/validators/run_all.py   # Windows
.venv/bin/python scripts/validators/run_all.py        # macOS/Linux
git add starter/ docs/domain/ agents/knowledge-graphs/
git commit -m "UCGIS workshop: D4 Natural Earth catalog"
git push -u origin workshop-<handle>
```

Open PR to upstream: https://github.com/Keven1894/ucgis-agentloom-2026-workshop

---

## Cross-links

- Default pack (D3): [`04-attendee-prompt-pack.md`](./04-attendee-prompt-pack.md)
- D1 sibling: [`04-attendee-prompt-pack-D1.md`](./04-attendee-prompt-pack-D1.md)
- D2 sibling: [`04-attendee-prompt-pack-D2.md`](./04-attendee-prompt-pack-D2.md)
- Data source menu: [`03-data-source-menu.md`](./03-data-source-menu.md)
- Slides: [`06-slides-outline-draft.md`](./06-slides-outline-draft.md)
