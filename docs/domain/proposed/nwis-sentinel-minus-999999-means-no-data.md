# NWIS -999999 means no data

**Node ID**: `knowledge:domain:nwis-sentinel-minus-999999-means-no-data`
**Type**: concept
**Category**: data-quality
**Created**: 2026-05-31

---

## Convention

USGS NWIS Instantaneous Values (IV) JSON encodes missing observations using a numeric sentinel value.

In the NWIS IV time-series payload, the sentinel is declared per-variable as:

- `timeSeries[].variable.noDataValue: -999999.0`

Individual observations under `timeSeries[].values[].value[]` may use this sentinel for the `value` field when an observation is unavailable.

---

## Why this matters

Ingest and visualization code must treat sentinel values as **missing**, not as real measurements.

If `-999999` is not filtered/converted to null/NaN before downstream processing, it can:

- break summary statistics (min/mean/max)
- distort chart scales and map color ramps
- create false outliers that look like extreme hydrologic events

---

## Observed evidence (snapshot)

From `data/snapshots/d3-usgs-nwis-suwannee-24h.json`:

- `value.timeSeries[0].variable.noDataValue` is `-999999.0`.

---

## Implementation notes (non-procedural)

- Prefer representing missing values as `null` (JSON) / `None` (Python) / `NaN` (pandas) depending on the ingest envelope and downstream consumer.
- Do not assume the sentinel will never appear as a **string**: in the same payload, many numeric fields (e.g., observation `value`) are often serialized as strings.
