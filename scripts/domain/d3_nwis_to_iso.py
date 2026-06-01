"""d3_nwis_to_iso — normalize NWIS IV timestamps to strict UTC ISO-8601 (Z).

Reads the vendored D3 multi-station snapshot:
  data/snapshots/d3-usgs-nwis-fl-stations-24h.json

Writes a normalized output to:
  dist/d3-normalized.iso.json

Goals:
- Preserve enough structure for the streamflow catalog to render markers + latest values.
- Convert observation timestamps from offset form (e.g. 2026-05-17T00:00:00.000-04:00)
  to strict UTC Z form (e.g. 2026-05-17T04:00:00Z).
- Emit timestamp keys that the Tier-B validator recognizes (e.g. "datetime").

This script is intentionally small and dependency-free.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
INPUT_PATH = WORKSPACE / "data/snapshots/d3-usgs-nwis-fl-stations-24h.json"
OUTPUT_PATH = WORKSPACE / "dist/d3-normalized.iso.json"


def _to_utc_z(dt: str) -> str:
    """Parse ISO-8601 datetime with offset and return UTC '...Z' without milliseconds."""
    # NWIS provides e.g. '2026-05-17T00:00:00.000-04:00'
    # datetime.fromisoformat supports offset parsing in Python 3.11.
    d = datetime.fromisoformat(dt)
    if d.tzinfo is None:
        # Defensive: treat naive as UTC.
        d = d.replace(tzinfo=timezone.utc)
    d_utc = d.astimezone(timezone.utc)
    return d_utc.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _num(v: Any) -> float | None:
    try:
        if v is None:
            return None
        return float(v)
    except Exception:
        return None


@dataclass(frozen=True)
class NormalizedObservation:
    datetime: str
    value: float
    qualifiers: list[str]


def main() -> int:
    payload = json.loads(INPUT_PATH.read_text(encoding="utf-8"))
    time_series = payload.get("value", {}).get("timeSeries", [])

    out_series: list[dict[str, Any]] = []
    for series in time_series:
        source = series.get("sourceInfo", {})
        site_code0 = (source.get("siteCode") or [{}])[0]
        site_id = site_code0.get("value")
        site_name = source.get("siteName")
        geo = source.get("geoLocation", {}).get("geogLocation", {})
        lat = _num(geo.get("latitude"))
        lon = _num(geo.get("longitude"))

        var = series.get("variable", {})
        parameter_code = ((var.get("variableCode") or [{}])[0]).get("value")
        unit_code = (var.get("unit") or {}).get("unitCode")
        no_data_value = _num(var.get("noDataValue"))

        obs_raw = ((series.get("values") or [{}])[0]).get("value") or []
        observations: list[dict[str, Any]] = []
        for o in obs_raw:
            dt = o.get("dateTime")
            v = _num(o.get("value"))
            if not dt or v is None:
                continue
            if no_data_value is not None and v == no_data_value:
                continue
            observations.append(
                {
                    "datetime": _to_utc_z(dt),
                    "value": v,
                    "qualifiers": o.get("qualifiers") or [],
                }
            )

        if not site_id or lat is None or lon is None:
            # Skip incomplete entries rather than emitting invalid points.
            continue

        out_series.append(
            {
                "site_id": str(site_id),
                "site_name": site_name,
                "latitude": lat,
                "longitude": lon,
                "parameter_code": str(parameter_code) if parameter_code is not None else None,
                "unit": unit_code,
                "no_data_value": no_data_value,
                "observations": observations,
            }
        )

    out = {
        "source": "USGS NWIS IV (vendored snapshot)",
        "generated_at": datetime.now(tz=timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "series": out_series,
    }

    OUTPUT_PATH.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"[OK] Wrote {OUTPUT_PATH.relative_to(WORKSPACE)} with {len(out_series)} series")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
