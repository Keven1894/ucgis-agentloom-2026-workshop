# D1 — USGS Earthquakes — prompt pack (reference)

**Reference build** — captured while building the D1 reference catalog. Source of truth for
the public per-dataset prompt pack. Keep verbatim prompts here; the public pack uses the same
prompts with attendee-facing framing.

- **Snapshot**: `data/snapshots/d1-usgs-earthquakes-week.geojson` (GeoJSON FeatureCollection, ~1879 events)
- **Catalog dir**: `starter/earthquake-catalog/`
- **Auth**: none
- **Distinctive lesson**: epoch-millisecond timestamps; GeoJSON `[lon, lat, depth]` order; many nullable fields
- **Expected on map**: every event in the snapshot (no magnitude filter), circle markers sized by magnitude

Append to every task:

```
Do NOT read agents/knowledge-graphs/*-graph.json directly.
Use MCP kg_search / kg_get_node / kg_list_proposals for KG context.
```

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
   - timestamp format + units (epoch seconds? ms? ISO?)
   - coordinate order and how many elements
   - which properties are nullable / unreliable
   - gaps: what the domain KG does NOT yet know

Do NOT propose yet. Stop after summary.
```

**Pass**: 3–5 concrete foot-guns surfaced (epoch ms, lon-lat-depth order, nullable fields); MCP used; no `*-graph.json` reads.

---

## Phase 3 — Autonomous propose (Track B), repeat 2–3×

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

**Reference nodes proposed for D1** (Cline should converge on these, slugs may vary):

| Slug | Why catalog code must know it |
| --- | --- |
| `usgs-quake-time-is-epoch-milliseconds` | `properties.time` is epoch **ms** — pass to `new Date(ms)`, never ÷1000 |
| `usgs-quake-coords-are-lon-lat-depth` | `[lon, lat, depth_km]`, lon first; Leaflet wants `[lat, lon]`; pad 2-tuples |
| `usgs-quake-many-nullable-fields` | `felt/cdi/mmi/tsunami/alert` often null; `place` is free text |

**Human gate**: dashboard review → `accept_proposal.py` for each.

---

## Phase 4 — Catalog shell (new Cline task)

```
Build starter/earthquake-catalog/index.html — scaffolding only.

Requirements:
- HTML5 + Leaflet 1.9.4 (unpkg)
- Top bar + sidebar + div#map
- All 8 data-catalog-role sections (>=10 chars each): title, provenance, acquisition,
  data-shape, processing, kg-link, reuse, data-view
- data-view contains div#map
- One application/ld+json Schema.org Dataset (name, description, url, license, creator,
  distribution, dateModified)
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
- Convert properties.time (epoch MS) to a UTC string with new Date(ms) per accepted KG node
- Size circle markers by magnitude; tolerate null optional fields (use MCP kg_search)
- Update data-shape and processing sections to match the actual JS

Run scripts/validators/run_all.py until PASS. Report event count on map.

If fetch fails on file://, note: python -m http.server 8766 from repo root.
```

**Pass**: all snapshot events plotted; epoch-ms times render as readable UTC; validators green.

---

## Phase 5c — Narrative polish via KG (new Cline task)

Same as the generic pack: search/propose `story-map-must-answer-four-viewer-questions`,
add an "At a glance" panel answering: where from / what is it / how to reuse / what's on
screen now. Do NOT re-propose GeoJSON parsing rules — narrative only.

---

## Phase 7 — Close + PR

```bash
.venv/bin/python scripts/validators/run_all.py        # macOS/Linux  (Windows: .venv\Scripts\python ...)
git add starter/ docs/domain/ agents/knowledge-graphs/
git commit -m "UCGIS workshop: D1 earthquake catalog"
git push -u origin workshop-<handle>
```

---

## Build notes (reference only)

- Markers use `L.circleMarker` with `radius = clamp(3, 18, 3 + mag*2.2)` so M0 and M7+ both read.
- `worldCopyJump: true` + `fitBounds(..., maxZoom: 6)` keeps the global spread visible.
- No magnitude filter by design — contrast with D3 where sentinel filtering removes points.
- Validators confirmed green: `catalog_ui_must_tell_the_story` + `catalog_must_embed_dataset_jsonld` both exit 0.
