# NWIS parameter codes are opaque 5-digit strings

**Node ID**: `knowledge:domain:nwis-parameter-codes-are-opaque-5-digit-strings`
**Type**: concept
**Category**: identifiers
**Created**: 2026-05-31

---

## Convention

USGS NWIS identifies observed variables using *parameter codes* (`parameterCd`) that are **opaque 5-digit strings**.

In NWIS IV JSON responses, the parameter code appears under:

- `timeSeries[].variable.variableCode[].value`

Example observed in the D3 snapshot:

- `"00060"` — streamflow / discharge (cubic feet per second)

---

## Why this matters

- Catalog UIs should display the parameter code explicitly (e.g., `00060`) and pair it with a human label sourced from NWIS metadata (`variableName`, `variableDescription`, and/or a curated lookup table).
- Do **not** assume you can infer semantics from the digits alone (e.g., by slicing, casting to int, or applying numeric ranges). Treat the code as an identifier.

---

## Observed evidence (snapshot)

From `data/snapshots/d3-usgs-nwis-suwannee-24h.json`:

- `value.timeSeries[0].variable.variableCode[0].value` is `"00060"`.
- The same object provides meaning in adjacent fields:
  - `variableName`: `"Streamflow, ft&#179;/s"`
  - `variableDescription`: `"Discharge, cubic feet per second"`
  - `unit.unitCode`: `"ft3/s"`
