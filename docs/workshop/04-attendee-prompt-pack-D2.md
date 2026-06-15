# 04 (D2) — Attendee prompt pack: OpenAQ v3 (Track B — workshop day)

**Last updated**: 2026-06-14
**Audience**: attendees + lecturer
**Use with**: [`03-data-source-menu.md`](./03-data-source-menu.md) · Cline Act mode · gpt-5.2 @ 0.2
**Default pack**: [`04-attendee-prompt-pack.md`](./04-attendee-prompt-pack.md) (D3 streamflow). This file is the **D2 sibling** — same flow, OpenAQ-specific prompts.

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

## D2 at a glance (workshop day)

| | |
| --- | --- |
| **Snapshot** | `data/snapshots/d2-openaq-locations-page1.json` (locations page 1) |
| **Catalog dir** | `starter/openaq-catalog/` |
| **Auth** | `X-API-Key` header for live API; vendored JSON works offline |
| **Distinctive lesson** | `{ latitude, longitude }` coordinate object; **two-call** locations→measurements join; varying units |
| **Expected on map** | every location with valid coordinates (~100 markers); sensor **parameters** in popup — not measurement time series |

**Contrast with D3**: D2 is flat location records + nested `sensors[]` metadata, not deeply nested NWIS time series. **Contrast with D1**: coordinates are an object, not GeoJSON `[lon, lat]`.

**Lecturer line**: "Same protocol — different foot-guns. OpenAQ teaches API joins and nullable coordinates, not sentinels or epoch-ms quakes."

---

## Phase 0 — Already done in Block 0

See [`01-setup.md`](./01-setup.md). Pass = `test_mcp_kg_tools.py` PASS + dashboard Proposals tab loads.

---

## Phase 1 — Quickstart (Block 2, all room)

If not done: complete [`02-quickstart.md`](./02-quickstart.md) Steps 1–6 once.

---

## Phase 2 — Discovery (new Cline task)

```
Workshop main task — data source D2 (OpenAQ v3 locations). Discovery only.

1. Read docs/workshop/03-data-source-menu.md section D2.
2. Read the first 8000 bytes of data/snapshots/d2-openaq-locations-page1.json.
3. MCP kg_search for several queries: "openaq coordinates", "locations measurements join",
   "api key", "parameter units", "latitude longitude" with role=domain.
4. MCP kg_list_proposals — report count only.
5. Summarize in bullets:
   - top-level JSON shape (meta vs results[])
   - how coordinates are represented (nullable? object vs array?)
   - what sensors[] contains vs what a measurements response would contain
   - auth requirements for live refresh
   - gaps: what the domain KG does NOT yet know

Do NOT propose yet. Stop after summary.
```

**Pass**: 3–5 concrete foot-guns (coordinate object, two-call join, API key, units, null coords); MCP used; no `*-graph.json` reads.

---

## Phase 3 — Autonomous propose (Track B)

**One Cline task per proposal** (recommended). Cline must derive slug/title/justification from Phase 2.

### Task template (repeat 2–3×)

```
Workshop Track B — propose ONE domain knowledge node from your D2 discovery summary.

Pick the next highest-risk gap not yet proposed (coordinate object, two-call join,
API key, parameter units, nullable coordinates, etc.).

1. MCP kg_search to confirm the topic is not already covered.
2. Run scripts/kg/propose_node.py (.venv python) with:
   --type knowledge --target-role domain
   --slug <kebab-case you choose>
   --title "<short title>"
   --justification "<one sentence why catalog code must know this>"
   --source-context "data/snapshots/d2-openaq-locations-page1.json + your observation"
   --path docs/domain/proposed/<same-slug>.md
3. Write docs/domain/proposed/<slug>.md stub (~20 lines) with evidence from the snapshot.

Do NOT run accept_proposal.py. Stop after one successful propose.
```

**Human gate**: dashboard review → `accept_proposal.py` for each proposal.

**Lecturer reference — D2 nodes** (Cline should converge on these; slugs may vary):

| Slug | Why catalog code must know it |
| --- | --- |
| `openaq-coordinates-are-latitude-longitude-object` | `coordinates: { latitude, longitude }` — not GeoJSON; filter nulls before map |
| `openaq-locations-then-measurements-two-call-join` | locations JSON ≠ measurements; second call per `locationId` |
| `openaq-parameter-units-vary` | `sensors[].parameter.units` includes µg/m³, ppm, ppb — normalize before comparing |

**Anti-pattern (Track C — do not use on workshop day)**:

```
❌ Operator pastes full --slug openaq-coordinates-are-latitude-longitude-object …
```

---

## Phase 4 — Catalog shell (new Cline task)

```
Build starter/openaq-catalog/index.html — scaffolding only.

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
Wire starter/openaq-catalog/index.html to data/snapshots/d2-openaq-locations-page1.json.

- Fetch with relative path from starter/openaq-catalog/ (../../data/snapshots/...)
- Parse results[]: coordinates.latitude and coordinates.longitude (skip rows with null coords)
- Circle markers; popup: name, country, location id, list of sensors[] parameters/units
- processing section: document that measurements need GET /v3/locations/{id}/measurements (per KG)
- Update data-shape and processing sections to match the actual JS

Run scripts/validators/run_all.py until PASS. Report location count on map.

If fetch fails on file://, note: python -m http.server 8766 from repo root.
```

**Pass**: all valid locations plotted; popups show sensor parameters; validators green.

> **Note**: D2 has **no Phase 5b** (locations-only snapshot — no scale-enrich) and **no Phase 6** (no normalize script). Do **not** force-wire measurements unless you vendored a measurements page — document the join in KG instead.

---

## Phase 5c — Narrative polish via KG (new Cline task, ~10 min)

**When**: catalog works and markers render, but a human still asks "what am I looking at?"

```
Workshop Track B — narrative polish (story map).

1. MCP kg_search "story map viewer questions catalog narrative" role=domain and role=builder.
2. If knowledge:domain:story-map-must-answer-four-viewer-questions is missing, propose ONE node:
   - Four plain-language questions: where from, what is it, how to reuse, what is on screen NOW
   - Justification: behavior:builder:catalog-ui-must-tell-the-story is structural only;
     first-time viewers need at-a-glance answers without JSON paths
   - path docs/domain/proposed/story-map-must-answer-four-viewer-questions.md
3. Human accepts on dashboard.
4. Polish starter/openaq-catalog/index.html:
   - Add an "At a glance" panel (location count, country sample from loaded data)
   - Rewrite provenance / data-shape / reuse in plain language
   - Link the new node in kg-link
5. run_all.py PASS.

Do NOT re-propose coordinate/join rules — this phase is narrative only.
```

**Pass**: four viewer questions answerable without reading code; validators green.

---

## Phase 7 — Close + PR

Human:

```bash
.venv/Scripts/python scripts/validators/run_all.py   # Windows
.venv/bin/python scripts/validators/run_all.py        # macOS/Linux
git add starter/ docs/domain/ agents/knowledge-graphs/
git commit -m "UCGIS workshop: D2 OpenAQ catalog"
git push -u origin workshop-<handle>
```

Open PR to upstream: https://github.com/Keven1894/ucgis-agentloom-2026-workshop

---

## Cross-links

- Default pack (D3): [`04-attendee-prompt-pack.md`](./04-attendee-prompt-pack.md)
- D1 sibling: [`04-attendee-prompt-pack-D1.md`](./04-attendee-prompt-pack-D1.md)
- Data source menu: [`03-data-source-menu.md`](./03-data-source-menu.md)
- Slides: [`06-slides-outline-draft.md`](./06-slides-outline-draft.md)
