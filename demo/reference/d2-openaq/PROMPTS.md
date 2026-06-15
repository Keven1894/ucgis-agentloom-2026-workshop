# D2 — OpenAQ v3 — prompt pack (reference)

**Reference build** — captured while building the D2 reference catalog.

- **Snapshot**: `data/snapshots/d2-openaq-locations-page1.json` (100 locations, page 1)
- **Catalog dir**: `starter/openaq-catalog/`
- **Auth**: `X-API-Key` for live API; vendored snapshot works offline
- **Distinctive lesson**: coordinates as `{latitude, longitude}` object; two-call locations→measurements join; varying parameter units
- **Expected on map**: all locations with valid coordinates (~100 markers); sensor list in popup — **no** measurements time series wired

Append to every task:

```
Do NOT read agents/knowledge-graphs/*-graph.json directly.
Use MCP kg_search / kg_get_node / kg_list_proposals for KG context.
```

---

## Phase 2 — Discovery

```
Workshop main task — data source D2 (OpenAQ v3 locations). Discovery only.

1. Read docs/workshop/03-data-source-menu.md section D2.
2. Read the first 8000 bytes of data/snapshots/d2-openaq-locations-page1.json.
3. MCP kg_search: "openaq coordinates", "locations measurements join", "api key",
   "parameter units", "latitude longitude" with role=domain.
4. MCP kg_list_proposals — report count only.
5. Summarize in bullets:
   - top-level JSON shape (meta vs results)
   - how coordinates are represented (array vs object; nullable?)
   - what sensors[] contains vs what measurements would contain
   - auth / API key requirements for live refresh
   - gaps: what the domain KG does NOT yet know

Do NOT propose yet. Stop after summary.
```

**Reference nodes**:

| Slug | Why catalog code must know it |
| --- | --- |
| `openaq-coordinates-are-latitude-longitude-object` | `{ latitude, longitude }` object — not GeoJSON; can be null |
| `openaq-locations-then-measurements-two-call-join` | locations page ≠ measurements; second call per locationId |
| `openaq-parameter-units-vary` | µg/m³, ppm, ppb — do not assume one unit on one axis |

---

## Phase 4 — Catalog shell

```
Build starter/openaq-catalog/index.html — scaffolding only.

Requirements:
- HTML5 + Leaflet 1.9.4 (unpkg)
- Top bar + sidebar + div#map
- All 8 data-catalog-role sections (>=10 chars each)
- application/ld+json Schema.org Dataset
- Placeholder map; kg-link references accepted domain nodes by title

Do NOT copy external repos. Run scripts/validators/run_all.py until PASS.
```

---

## Phase 5 — Wire vendored data

```
Wire starter/openaq-catalog/index.html to data/snapshots/d2-openaq-locations-page1.json.

- Fetch ../../data/snapshots/d2-openaq-locations-page1.json
- Parse results[]: coordinates.latitude/longitude (filter nulls)
- Circle markers; popup with name, country, location id, sensors[] parameter list
- Document in processing that measurements need a second API call (per KG node)
- Update data-shape and processing sections to match actual JS

Run scripts/validators/run_all.py until PASS. Report location count on map.
```

**No Phase 5b/6** — locations-only snapshot; measurements join is KG-documented, not forced in catalog.

---

## Phase 5c — Narrative polish

Same story-map task as D1/D3 — propose `story-map-must-answer-four-viewer-questions` if missing; add At a glance panel with location/country counts.
