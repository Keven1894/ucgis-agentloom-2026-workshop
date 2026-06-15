#!/usr/bin/env python3
"""Capture catalog screenshots for docs/workshop/showcase.html.

Requires:
  - Catalog static server on :8766 (bash demo/reference/serve_demo.sh)
  - pip install playwright && playwright install chromium

Usage:
  python demo/reference/capture_screenshots.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MANIFEST = REPO / "demo" / "reference" / "manifest.json"


def main() -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Install playwright first: .venv/bin/pip install playwright && playwright install chromium")
        return 1

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    base = manifest.get("catalogBaseUrl", "http://127.0.0.1:8766").rstrip("/")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        for demo in manifest.get("demos", []):
            if demo.get("status") != "ready":
                print(f"  skip {demo.get('id')} (status={demo.get('status')})")
                continue
            starter = demo.get("starterDir")
            if not starter:
                continue
            url = f"{base}/starter/{starter}/"
            shot_rel = demo.get("screenshot", "")
            if not shot_rel:
                continue
            out = REPO / shot_rel
            out.parent.mkdir(parents=True, exist_ok=True)
            print(f"  {demo.get('id')}: {url} -> {out.relative_to(REPO)}")
            page.goto(url, wait_until="networkidle", timeout=120_000)
            page.wait_for_timeout(2500)
            page.screenshot(path=str(out), full_page=False)
        browser.close()
    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
