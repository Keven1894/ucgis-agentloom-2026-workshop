"""Download canonical snapshots of D1/D2/D3/D4 into data/snapshots/.

Run once (and refresh ~weekly leading up to workshop). The committed snapshots
are what attendees fall back to if upstream APIs are down on workshop day or
they're behind a hotel WiFi captive portal.

Usage:
    python scripts/vendor_snapshots.py            # all sources
    python scripts/vendor_snapshots.py --only d1 d3 d4
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SNAPSHOTS = REPO_ROOT / "data" / "snapshots"
SNAPSHOTS.mkdir(parents=True, exist_ok=True)


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

UA = {"User-Agent": "ucgis-agentloom-2026/0.1"}
TIMEOUT = 60


def _download(url: str, out: Path, *, headers: dict[str, str] | None = None) -> int:
    h = dict(UA)
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        body = resp.read()
    out.write_bytes(body)
    return len(body)


def vendor_d1() -> None:
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson"
    out = SNAPSHOTS / "d1-usgs-earthquakes-week.geojson"
    n = _download(url, out)
    print(f"  D1 -> {out.name} ({n:,} bytes)")


def vendor_d2() -> None:
    api_key = os.environ.get("OPENAQ_API_KEY")
    if not api_key:
        print("  D2 SKIPPED — OPENAQ_API_KEY not set; register at https://explore.openaq.org/account")
        return
    url = "https://api.openaq.org/v3/locations?limit=100"
    out = SNAPSHOTS / "d2-openaq-locations-page1.json"
    n = _download(url, out, headers={"X-API-Key": api_key})
    print(f"  D2 -> {out.name} ({n:,} bytes)")


def vendor_d3() -> None:
    # Suwannee River discharge — 24h. Small, fast, demonstrates time-series shape.
    url = (
        "https://waterservices.usgs.gov/nwis/iv/?format=json&sites=02320500"
        "&parameterCd=00060&period=PT24H"
    )
    out = SNAPSHOTS / "d3-usgs-nwis-suwannee-24h.json"
    n = _download(url, out)
    print(f"  D3 -> {out.name} ({n:,} bytes)")


def vendor_d4() -> None:
    # Natural Earth admin-0 countries via datahub mirror (official site is shapefile-only).
    url = "https://datahub.io/core/geo-countries/r/countries.geojson"
    out = SNAPSHOTS / "d4-natural-earth-admin0.geojson"
    n = _download(url, out)
    print(f"  D4 -> {out.name} ({n:,} bytes)")


SOURCES = {"d1": vendor_d1, "d2": vendor_d2, "d3": vendor_d3, "d4": vendor_d4}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--only", nargs="*", choices=list(SOURCES.keys()), help="Subset of sources")
    args = p.parse_args()
    targets = args.only or list(SOURCES.keys())
    print(f"Vendoring {len(targets)} sources to {SNAPSHOTS}\n")
    failed = []
    for k in targets:
        try:
            SOURCES[k]()
        except Exception as e:  # noqa: BLE001
            failed.append((k, str(e)))
            print(f"  {k.upper()} FAILED: {e}")
    print()
    if failed:
        print(f"Done — {len(failed)} failure(s).")
        return 1
    print("Done — all OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
