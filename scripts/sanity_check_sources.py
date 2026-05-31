"""Phase 0 sanity check — verify all 4 data sources are reachable + parseable.

Usage:
    python scripts/sanity_check_sources.py            # live mode (hits the internet)
    python scripts/sanity_check_sources.py --vendored # uses data/snapshots only

Exits 0 if all sources OK, 1 otherwise.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import urllib.request
import urllib.error

REPO_ROOT = Path(__file__).resolve().parent.parent
SNAPSHOTS = REPO_ROOT / "data" / "snapshots"
TIMEOUT = 30


def _load_dotenv() -> None:
    """Minimal .env loader (no third-party dep). Does not overwrite existing env vars."""
    env_path = REPO_ROOT / ".env"
    if not env_path.exists():
        return
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        if k and k not in os.environ:
            os.environ[k] = v


_load_dotenv()


@dataclass
class SourceResult:
    name: str
    ok: bool
    record_count: int
    schema_keys: list[str]
    error: str | None = None
    note: str | None = None


def _fetch_json(url: str, *, headers: dict[str, str] | None = None) -> Any:
    req = urllib.request.Request(url, headers=headers or {"User-Agent": "ucgis-agentloom-2026/0.1"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8"))


def check_d1_usgs_earthquakes(*, vendored: bool) -> SourceResult:
    """D1: USGS Earthquakes — GeoJSON, points, events, no auth."""
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson"
    snapshot = SNAPSHOTS / "d1-usgs-earthquakes-week.geojson"
    try:
        if vendored:
            data = json.loads(snapshot.read_text(encoding="utf-8"))
            note = f"vendored {snapshot.name}"
        else:
            data = _fetch_json(url)
            note = "live"
        feats = data.get("features", [])
        first_props = list(feats[0]["properties"].keys()) if feats else []
        return SourceResult(
            name="D1 USGS Earthquakes",
            ok=True,
            record_count=len(feats),
            schema_keys=first_props[:8],
            note=note,
        )
    except Exception as e:  # noqa: BLE001
        return SourceResult(
            name="D1 USGS Earthquakes", ok=False, record_count=0, schema_keys=[], error=str(e)
        )


def check_d2_openaq(*, vendored: bool) -> SourceResult:
    """D2: OpenAQ v3 — JSON paginated, point + timeseries, **API key now REQUIRED** (as of 2025).

    Set ``OPENAQ_API_KEY`` env var with a free key from https://explore.openaq.org/account.
    """
    url = "https://api.openaq.org/v3/locations?limit=20"
    snapshot = SNAPSHOTS / "d2-openaq-locations-page1.json"
    try:
        if vendored:
            data = json.loads(snapshot.read_text(encoding="utf-8"))
            note = f"vendored {snapshot.name}"
        else:
            api_key = os.environ.get("OPENAQ_API_KEY")
            if not api_key:
                return SourceResult(
                    name="D2 OpenAQ",
                    ok=False,
                    record_count=0,
                    schema_keys=[],
                    error="OPENAQ_API_KEY not set — register free key at https://explore.openaq.org/account, then `export OPENAQ_API_KEY=...` (or run with --vendored)",
                )
            data = _fetch_json(url, headers={"X-API-Key": api_key, "User-Agent": "ucgis-agentloom-2026/0.1"})
            note = "live (key from $OPENAQ_API_KEY)"
        results = data.get("results", [])
        first_keys = list(results[0].keys()) if results else []
        return SourceResult(
            name="D2 OpenAQ", ok=True, record_count=len(results), schema_keys=first_keys[:8], note=note
        )
    except Exception as e:  # noqa: BLE001
        return SourceResult(name="D2 OpenAQ", ok=False, record_count=0, schema_keys=[], error=str(e))


def check_d3_usgs_nwis(*, vendored: bool) -> SourceResult:
    """D3: USGS NWIS streamflow — JSON IV, point + timeseries, no auth."""
    # Sample: discharge (00060) for site 02320500 (Suwannee River) over last day
    url = (
        "https://waterservices.usgs.gov/nwis/iv/?format=json&sites=02320500"
        "&parameterCd=00060&period=PT24H"
    )
    snapshot = SNAPSHOTS / "d3-usgs-nwis-suwannee-24h.json"
    try:
        if vendored:
            data = json.loads(snapshot.read_text(encoding="utf-8"))
            note = f"vendored {snapshot.name}"
        else:
            data = _fetch_json(url)
            note = "live"
        ts_list = data.get("value", {}).get("timeSeries", [])
        if ts_list:
            first_ts = ts_list[0]
            keys = list(first_ts.keys())
            value_count = sum(len(v.get("value", [])) for v in first_ts.get("values", []))
        else:
            keys = []
            value_count = 0
        return SourceResult(
            name="D3 USGS NWIS",
            ok=True,
            record_count=value_count,
            schema_keys=keys[:8],
            note=note,
        )
    except Exception as e:  # noqa: BLE001
        return SourceResult(name="D3 USGS NWIS", ok=False, record_count=0, schema_keys=[], error=str(e))


def check_d4_natural_earth(*, vendored: bool) -> SourceResult:
    """D4: Natural Earth admin-0 countries — GeoJSON (mirrored), polygons, static, no auth."""
    # We use Datahub.io's Natural Earth GeoJSON mirror — official site is shapefile-only and harder
    # to consume from a one-shot script. A vendored snapshot is the canonical source for D4 in any
    # case (it's static).
    url = "https://datahub.io/core/geo-countries/r/countries.geojson"
    snapshot = SNAPSHOTS / "d4-natural-earth-admin0.geojson"
    try:
        if vendored:
            data = json.loads(snapshot.read_text(encoding="utf-8"))
            note = f"vendored {snapshot.name}"
        else:
            data = _fetch_json(url)
            note = "live (datahub mirror of Natural Earth)"
        feats = data.get("features", [])
        first_props = list(feats[0]["properties"].keys()) if feats else []
        return SourceResult(
            name="D4 Natural Earth",
            ok=True,
            record_count=len(feats),
            schema_keys=first_props[:8],
            note=note,
        )
    except Exception as e:  # noqa: BLE001
        return SourceResult(
            name="D4 Natural Earth", ok=False, record_count=0, schema_keys=[], error=str(e)
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--vendored",
        action="store_true",
        help="Use vendored snapshots from data/snapshots/ instead of hitting the network",
    )
    args = parser.parse_args()

    results = [
        check_d1_usgs_earthquakes(vendored=args.vendored),
        check_d2_openaq(vendored=args.vendored),
        check_d3_usgs_nwis(vendored=args.vendored),
        check_d4_natural_earth(vendored=args.vendored),
    ]

    print("\n=== Phase 0 sanity check — data sources ===\n")
    width_name = max(len(r.name) for r in results)
    for r in results:
        status = "OK " if r.ok else "FAIL"
        print(f"[{status}] {r.name:<{width_name}}  records={r.record_count:>6}  ({r.note or r.error})")
        if r.ok and r.schema_keys:
            print(f"          schema_keys: {r.schema_keys}")
        if not r.ok:
            print(f"          ERROR: {r.error}")
    print()

    return 0 if all(r.ok for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
