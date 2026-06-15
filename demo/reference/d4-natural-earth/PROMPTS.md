# D4 — Natural Earth Admin-0 — prompt pack (reference)

**Reference build** — captured while building the D4 reference catalog.

- **Snapshot**: `data/snapshots/d4-natural-earth-admin0.geojson` (~258 countries, ~15 MB)
- **Catalog dir**: `starter/boundaries-catalog/`
- **Auth**: none
- **Distinctive lesson**: hyphenated ISO property names; basemap/join layer (not point ingestion); MultiPolygon complexity
- **Expected on map**: all country polygons with popups (name + ISO Alpha-2/3)

Append to every task:

```
Do NOT read agents/knowledge-graphs/*-graph.json directly.
Use MCP kg_search / kg_get_node / kg_list_proposals for KG context.
```

---

## Phase 2 — Discovery

```
Workshop main task — data source D4 (Natural Earth Admin 0). Discovery only.

1. Read docs/workshop/03-data-source-menu.md section D4.
2. Read the first 8000 bytes of data/snapshots/d4-natural-earth-admin0.geojson.
3. MCP kg_search: "natural earth iso", "admin 0", "multipolygon", "basemap join",
   "geojson properties" with role=domain.
4. MCP kg_list_proposals — report count only.
5. Summarize in bullets:
   - geometry types (Polygon vs MultiPolygon)
   - property keys for country name and ISO codes (exact spelling)
   - file size / performance implications
   - role of this layer vs event/point datasets (D1/D2/D3)
   - gaps: what the domain KG does NOT yet know

Do NOT propose yet. Stop after summary.
```

**Reference nodes**:

| Slug | Why catalog code must know it |
| --- | --- |
| `natural-earth-iso-property-names-hyphenated` | `ISO3166-1-Alpha-3` / `-Alpha-2` — not `iso_a2` |
| `natural-earth-is-basemap-not-event-stream` | join/context layer — not sensor readings |
| `natural-earth-multipolygon-complexity` | Antarctica etc.; large GeoJSON; slow first load OK with HTTP |

---

## Phase 4 — Catalog shell

```
Build starter/boundaries-catalog/index.html — scaffolding only.

Requirements:
- HTML5 + Leaflet 1.9.4 (unpkg)
- Top bar + sidebar + div#map
- All 8 data-catalog-role sections (>=10 chars each)
- application/ld+json Schema.org Dataset
- Placeholder map; kg-link references accepted domain nodes

Run scripts/validators/run_all.py until PASS.
```

---

## Phase 5 — Wire vendored data

```
Wire starter/boundaries-catalog/index.html to data/snapshots/d4-natural-earth-admin0.geojson.

- Fetch ../../data/snapshots/d4-natural-earth-admin0.geojson (~15 MB — show loading state)
- L.geoJSON with styled fills; onEachFeature popup: name, ISO3166-1-Alpha-3, ISO3166-1-Alpha-2
- fitBounds after load
- processing section: basemap role, hyphenated property keys, MultiPolygon note

Run scripts/validators/run_all.py until PASS. Report feature count.
```

**No Phase 5b/6**.

---

## Phase 5c — Narrative polish

Same story-map task — At a glance with feature count and MultiPolygon note.
