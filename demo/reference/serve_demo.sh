#!/usr/bin/env bash
# Reference demo launcher — stages demo catalogs and optionally serves the repo.
#
# Stages reference catalogs into starter/<name>/ so relative fetch paths work.
# KG review uses dashboard ?ref= overlays — does NOT mutate *-graph.json.
#
# Usage:
#   bash demo/reference/serve_demo.sh          # stage + serve catalogs + print URLs
#   bash demo/reference/serve_demo.sh stage    # stage only (for serve-all.sh)
#   bash demo/reference/serve_demo.sh clean    # remove staged starter/
#
# Hub:       http://127.0.0.1:8766/docs/workshop/showcase.html
# Dashboard: .venv/bin/python -m uvicorn server.dashboard.app:app --port 8000

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
REF_DIR="$REPO_ROOT/demo/reference"
CATALOG_PORT="${CATALOG_PORT:-8766}"
DASHBOARD_PORT="${DASHBOARD_PORT:-8000}"

stage_from_manifest() {
  mkdir -p "$REPO_ROOT/starter"
  REPO_ROOT="$REPO_ROOT" python3 - <<'PY'
import json, os, shutil
from pathlib import Path
repo = Path(os.environ["REPO_ROOT"])
manifest = json.loads((repo / "demo/reference/manifest.json").read_text())
for demo in manifest.get("demos", []):
    ref_id = demo["id"]
    starter = demo["starterDir"]
    src = repo / "demo/reference" / ref_id / "index.html"
    if not src.is_file():
        continue
    dst_dir = repo / "starter" / starter
    dst_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst_dir / "index.html")
    print(f"  staged starter/{starter}/  ({ref_id})")
PY
  if [ -f "$REF_DIR/d3-streamflow/d3-normalized.iso.json" ]; then
    mkdir -p "$REPO_ROOT/dist"
    cp "$REF_DIR/d3-streamflow/d3-normalized.iso.json" "$REPO_ROOT/dist/"
  fi
}

clean() {
  rm -rf "$REPO_ROOT/starter"
  echo "  removed staged starter/"
}

print_urls() {
  echo ""
  echo "=== Open in browser ==="
  echo "  Showcase hub:  http://127.0.0.1:$CATALOG_PORT/docs/workshop/showcase.html"
  echo "  Dashboard KG:  http://127.0.0.1:$DASHBOARD_PORT/  (use ?ref= on each demo)"
  echo ""
  REPO_ROOT="$REPO_ROOT" CATALOG_PORT="$CATALOG_PORT" DASHBOARD_PORT="$DASHBOARD_PORT" python3 - <<'PY'
import json, os
from pathlib import Path
repo = Path(os.environ["REPO_ROOT"])
m = json.loads((repo / "demo/reference/manifest.json").read_text())
base = m.get("catalogBaseUrl", f"http://127.0.0.1:{os.environ['CATALOG_PORT']}").rstrip("/")
dash = m.get("dashboardBaseUrl", f"http://127.0.0.1:{os.environ['DASHBOARD_PORT']}").rstrip("/")
for d in m.get("demos", []):
    ref = d.get("id")
    s = d.get("starterDir")
    kg = (repo / "demo/reference" / ref / "domain-knowledge-graph.json").is_file()
    cat = d.get("status") == "ready" and (repo / "starter" / s / "index.html").is_file()
    if cat:
        print(f"  {d.get('label')} catalog: {base}/starter/{s}/")
    if kg:
        print(f"  {d.get('label')} KG:       {dash}/?ref={ref}#graph")
PY
}

case "${1:-}" in
  clean) clean; exit 0 ;;
  stage)
    echo "Staging reference catalogs into starter/ ..."
    stage_from_manifest
    print_urls
    exit 0
    ;;
esac

echo "Staging reference catalogs into starter/ ..."
stage_from_manifest
print_urls

echo ""
echo "Serving repo root on :$CATALOG_PORT  (Ctrl+C to stop) ..."
cd "$REPO_ROOT"
exec python3 -m http.server "$CATALOG_PORT" --bind 127.0.0.1
