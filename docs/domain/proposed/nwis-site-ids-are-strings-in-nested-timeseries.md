# NWIS site IDs are strings in nested timeSeries

**Node ID**: `knowledge:domain:nwis-site-ids-are-strings-in-nested-timeseries`
**Type**: concept
**Category**: identifiers
**Created**: 2026-05-31

---

## Convention

USGS NWIS Instantaneous Values (IV) JSON nests site metadata under each `timeSeries[]` entry. Site identifiers appear as **strings** in:

- `timeSeries[].sourceInfo.siteCode[].value`

Do **not** parse site codes as integers — leading zeros and non-numeric suffixes are valid.

---

## Why this matters

- Catalog code must walk the nested `timeSeries` array rather than assuming a flat site list at the root.
- Map popups and sidebar keys should use `String(siteId)` for stable joins and display.
- Lat/lon live under `sourceInfo.geoLocation.geogLocation` (also nested per series).

---

## Observed evidence (snapshot)

From `data/snapshots/d3-usgs-nwis-suwannee-24h.json`:

- `value.timeSeries[0].sourceInfo.siteCode[0].value` is `"02320500"` (string).
- One series entry per site/parameter combination in this vendored snapshot.
