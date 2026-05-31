# 03 — Data source menu (pick your catalog)

**When**: after [`02-quickstart.md`](./02-quickstart.md) · workshop Block 3  
**Deep reference**: [`notes/data-sources.md`](../../notes/data-sources.md) (quirks, URLs, foot-guns)

Pick **one** source (or BYO with organizer approval). Build `starter/<your-choice>/` and domain KG nodes until **`make validate-all`** passes with your catalog.

---

## At a glance

| ID | Name | Shape | Auth | Snapshot | Difficulty | Distinctive lesson |
| --- | --- | --- | --- | --- | --- | --- |
| **D1** | USGS Earthquakes | Point events | None | `data/snapshots/d1-usgs-earthquakes-week.geojson` | ★★☆ | Epoch **milliseconds** (not ISO); GeoJSON quirks |
| **D2** | OpenAQ v3 air quality | Point + measurements | **API key** | `data/snapshots/d2-openaq-locations-page1.json` | ★★★ | Two-call **locations → measurements** join |
| **D3** | USGS NWIS streamflow | Point + time series | None | `data/snapshots/d3-usgs-nwis-suwannee-24h.json` | ★★★ | Deeply nested JSON; **sentinel -999999** |
| **D4** | Natural Earth admin-0 | Polygons | None | `data/snapshots/d4-natural-earth-admin0.geojson` | ★★☆ | Static boundaries; ISO property names; map-heavy |

**Not listed**: `data/workshop/quickstart-places.geojson` — teaching sample only ([`02-quickstart.md`](./02-quickstart.md)).

---

## D1 — USGS Earthquakes (GeoJSON events)

**Good if you want**: classic GeoJSON FeatureCollection, map + filter by magnitude/time.

| | |
| --- | --- |
| Live URL | https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson |
| Vendored | `data/snapshots/d1-usgs-earthquakes-week.geojson` |
| Volume | ~1.5k–2.5k features / week |

**Foot-guns to encode in domain KG:**

- `properties.time` is **Unix epoch milliseconds** — not seconds, not ISO 8601  
- Coordinates may be 2- or 3-element; depth optional  
- Many nullable fields (`tsunami`, `felt`, …)

**Workshop note**: lecturer may demo a completed D1 catalog from organizer checkout — **your fork does not include it**. Build your own.

---

## D2 — OpenAQ v3 (nested sensor JSON)

**Good if you want**: API integration story + air-quality semantics.

| | |
| --- | --- |
| API base | https://api.openaq.org/v3/ |
| Vendored | `data/snapshots/d2-openaq-locations-page1.json` |
| Auth | Header `X-API-Key` — workshop key or personal free tier |

**Foot-guns:**

- **Two-level model**: locations page, then measurements per `locationId`  
- `coordinates: null` on some stations — filter before map  
- Units vary (`µg/m³`, ppm, …) — normalize in KG + ingest

**Pedagogy**: same “sensor + time series” story as D3, **different JSON shape** — proves the framework generalizes.

---

## D3 — USGS NWIS streamflow (WaterML-ish JSON)

**Good if you want**: hydrology time series without API keys.

| | |
| --- | --- |
| Live pattern | `https://waterservices.usgs.gov/nwis/iv/?format=json&sites=...` |
| Vendored | `data/snapshots/d3-usgs-nwis-suwannee-24h.json` |
| Alt snapshot | `data/snapshots/d3-usgs-nwis-fl-stations-24h.json` (if present) |

**Foot-guns:**

- Parameter codes are opaque 5-digit strings (`00060` = discharge cfs)  
- `value=-999999` means no data  
- Site IDs are **strings** — do not cast to int  
- Measurements nested 3 levels deep vs D2's flat array

---

## D4 — Natural Earth admin-0 (polygons)

**Good if you want**: boundaries, choropleth, attribute join — not event streams.

| | |
| --- | --- |
| Vendored | `data/snapshots/d4-natural-earth-admin0.geojson` |
| Volume | ~258 countries; ~14 MB geometry |

**Foot-guns:**

- ISO codes in properties (e.g. hyphenated `ISO3166-1-Alpha-3`) — not old `iso_a2` mirrors  
- Multipolygon complexity (Antarctica) — consider zoom/clipping  
- **Role**: basemap / join layer — often consumed **with** point sources, not instead of ingestion

---

## Choosing

| You are… | Consider |
| --- | --- |
| New to geospatial APIs | **D1** or **D4** |
| Want API + join challenge | **D2** |
| Want time series without keys | **D3** |
| Already know earthquake feeds | **Avoid D1** — pick D2/D3/D4 |

Organizer recommendation: **avoid the source you know best** — the workshop tests the **protocol**, not your domain expertise.

---

## After you pick

1. **Cline + MCP**: `kg_search` for conventions related to your source shape  
2. **Propose** domain knowledge nodes (timestamps, CRS, sentinels, API joins)  
3. **You accept** via dashboard review + `accept_proposal.py`  
4. **Build** `starter/<short-name>/` (catalog UI + ingest)  
5. **Verify** `make validate-all` before every commit  
6. **PR** to workshop repo (see [`CONTRIBUTING.md`](../../CONTRIBUTING.md))

---

## Offline check

Vendored snapshots work without live API (except D2 live refresh):

```bash
.venv\Scripts\python scripts\sanity_check_sources.py --vendored
```

**Pass**: 4/4 sources OK against committed snapshots.

---

## Cross-links

- Full quirks: [`notes/data-sources.md`](../../notes/data-sources.md)  
- Main loop: [`00-workshop-workflow.md`](./00-workshop-workflow.md) Phase F  
- Half-day schedule: envistor [`06-attendee-flow.md`](../../../envistor-data/docs/research/workshop-ucgis-2026/06-attendee-flow.md)
