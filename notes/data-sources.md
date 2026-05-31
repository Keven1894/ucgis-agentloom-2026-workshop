# Data sources — quirks & decisions

Phase 0 deliverable. This file is the **seed for the domain knowledge nodes** built in Phase 1
(it gets converted to KG nodes like `data-source-patterns`, `crs-conventions`, `pagination-shapes`).

> **Heterogeneous-by-design**: 4 sources × 3 distinct shapes (event-stream points, time-series points
> across 2 schemas, static polygons) — this proves the AgentLoom workflow generalizes, not just
> "works for one cherry-picked feed."

## Source matrix

| ID | Name | Shape | Auth | Refresh cadence | Snapshot file |
| --- | --- | --- | --- | --- | --- |
| D1 | USGS Earthquakes (all_week) | Point + event | None | live (1 min) | `d1-usgs-earthquakes-week.geojson` |
| D2 | OpenAQ v3 locations | Point + time-series | **API key required** | live (15 min) | `d2-openaq-locations-page1.json` |
| D3 | USGS NWIS streamflow | Point + time-series | None | live (instantaneous) | `d3-usgs-nwis-suwannee-24h.json` |
| D4 | Natural Earth admin-0 | Polygon | None | static (yearly NE release) | `d4-natural-earth-admin0.geojson` |

## D1 — USGS Earthquakes

- **URL**: <https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson>
- **Format**: GeoJSON FeatureCollection. Each feature has `geometry.coordinates = [lon, lat, depth_km]`.
- **CRS**: WGS84 (EPSG:4326), depth in km positive-down.
- **Time semantics**: `properties.time` and `properties.updated` are **Unix epoch ms** (NOT seconds, NOT ISO 8601). This is a classic foot-gun.
- **ID stability**: feature `id` (e.g. `us7000abcd`) is stable across updates; the same event re-appears with `properties.updated` increased.
- **Volume**: ~1500–2500 features per week. Tiny.
- **Quirks**:
  - Coordinates can be `[lon, lat]` (2-tuple) for older entries — **always pad to 3 with `depth=null`**.
  - `properties.tsunami`, `properties.felt`, `properties.cdi`, `properties.mmi` are often `null`. Don't crash on them.
  - `properties.place` is human text (e.g. `"23 km W of Petrolia, CA"`) — useful for search, but parse-hostile.

## D2 — OpenAQ v3

- **URL**: <https://api.openaq.org/v3/>
- **🔑 API key required** since v3 launch (2024). v2 was open. Register: <https://explore.openaq.org/account>. Free tier is generous (10k req/day).
- **Auth header**: `X-API-Key: <key>`.
- **Pagination**: cursor-based via `page` + `limit` query params; `limit` max = 1000. Total in `meta.found`.
- **Two-level data model**: `locations` (where) ↔ `measurements` (what was measured when). **Joining requires a second call** keyed by `locationId`. **This is the canonical "API split" pattern** that the `add-data-source` skill needs to handle.
- **CRS**: WGS84.
- **Time semantics**: ISO 8601 with timezone, e.g. `"2026-05-17T12:34:56+00:00"`.
- **Quirks**:
  - Some stations report `coordinates: null` — filter them out before mapping.
  - `parameter.units` varies (`µg/m³`, `ppm`, `ppb`) — must canonicalize before plotting.
  - Rate limit: 60 req/min on free tier. Add backoff in fetcher.

## D3 — USGS NWIS instantaneous values

- **URL**: <https://waterservices.usgs.gov/nwis/iv/?format=json&sites=...&parameterCd=...&period=...>
- **Format**: JSON (waterML-1.1 also available; we use JSON).
- **Parameter codes** (5-digit, opaque): `00060` discharge cfs, `00065` gage height ft, `00010` water temp °C, `00045` precipitation in. Cheat-sheet must ship in the KG.
- **CRS**: WGS84.
- **Time semantics**: ISO 8601 with timezone offset; **values arrive at irregular intervals** (typically 15 min, sometimes gaps).
- **Same shape, different schema vs D2**: both are point + time-series, but D3 nests measurements 3 levels deep (`value.timeSeries[].values[].value[]`), D2 returns a flat array. The `add-data-source` skill must abstract this: the **same conceptual operation** ("ingest a sensor station with measurements") has two distinct JSON shapes. **This is the central pedagogical wedge** of D2+D3.
- **Quirks**:
  - `value=-999999` is the "no data" sentinel. Filter.
  - Site IDs (`sourceInfo.siteCode[0].value`) are 8–15 digits as **strings** — never cast to int.
  - Discharge is in **cfs** by default; metric users must convert.

## D4 — Natural Earth admin-0 countries

- **URL** (mirror): <https://datahub.io/core/geo-countries/r/countries.geojson>
- **Why mirror**: official site (<https://www.naturalearthdata.com/>) only ships shapefile zips, painful to consume from one-shot scripts. Mirror is GeoJSON-converted and stable.
- **Format**: GeoJSON FeatureCollection of polygons + multipolygons.
- **CRS**: WGS84.
- **Volume**: 258 features, ~14 MB (full-resolution geometry). Static — vendor once.
- **Quirks**:
  - Some properties have ISO codes (e.g. `ISO3166-1-Alpha-3 = "USA"`); name field is `name`. **No** `iso_a2` like the older mirrors.
  - Antarctica is one giant multi-polygon — slow to render at zoom 0; consider clipping in the viz layer.
  - **NOT a data source for events** — it's the basemap / spatial-join target for D1–D3. The KG should encode this: `D4` is consumed by the *aggregation* layer, not the *ingestion* layer.

## Cross-cutting decisions

1. **All ingestion normalizes to WGS84 GeoJSON Feature with `properties.timestamp_iso8601`** before hitting the app's storage layer. Time-zone math happens in the fetcher, not in the app.
2. **Vendored snapshots are the ground-truth for the workshop**, even when live APIs are reachable. Refresh weekly via `python scripts/vendor_snapshots.py`. The committed copy is what `make smoke` consumes.
3. **OpenAQ key is the only secret** in Phase 0. We mint **per-attendee** OpenAQ keys at workshop start (free tier, ~30 sec to register), or fall back to vendored snapshot if registration is flaky.
4. **D4's role differs from D1–D3** — and the KG must capture this asymmetry so the agent doesn't try to ingest country polygons as point events.

## Phase 0 status

- [x] D1 verified live + vendored
- [x] D2 verified live + vendored (key in `.env`; 20 locations in snapshot page-1)
- [x] D2 schema confirmed — top-level keys: `id, name, locality, timezone, country, owner, provider, isMobile`
- [x] D3 verified live + vendored
- [x] D4 verified live + vendored
- [x] `scripts/sanity_check_sources.py` exits 0 on all 4 sources (live + vendored)

**Phase 0 closed: 2026-05-18.**

## Open items → carry forward

| Item | Owner | Deadline | Notes |
| --- | --- | --- | --- |
| Decide D4 simplification (14 MB → ~2 MB via mapshaper) for in-browser rendering | Phase 1 | May 19 | Performance, not Phase 0 blocker |
| Vendor a D2 measurements page (not just locations) | Phase 1 | May 20 | The `add-data-source` skill must demonstrate the 2-call locations→measurements join |
