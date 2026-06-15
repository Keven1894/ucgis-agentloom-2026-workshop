#!/usr/bin/env bash
# Start the workshop's two local servers from a Terminal session.
#
# WHY a script instead of launchd: macOS TCC blocks launchd-spawned
# processes from reading ~/Documents, so http.server / uvicorn started by a
# LaunchAgent return empty listings / 404. Processes started from Terminal
# inherit Terminal's Documents access and work fine.
#
#   static  : http://127.0.0.1:8766  (showcase + catalogs, repo root)
#   dashboard: http://127.0.0.1:8000 (KG dashboard + /api/reference-demos)
#
# Usage (from repo root):
#   bash demo/serve/serve-all.sh          # start (kills stale first)
#   bash demo/serve/serve-all.sh stop     # stop both
#   bash demo/serve/serve-all.sh status   # show status

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
STATIC_PORT=8766
DASH_PORT=8000
VENV_PY="$REPO/.venv/bin/python"
LOG_DIR="/tmp"

kill_port() {
  local port="$1"
  local pids
  pids=$(lsof -nP -iTCP:"$port" -sTCP:LISTEN -t 2>/dev/null || true)
  if [ -n "$pids" ]; then
    echo "  freeing :$port (pids: $pids)"
    # shellcheck disable=SC2086
    kill $pids 2>/dev/null || true
    sleep 1
  fi
}

status() {
  echo "=== status ==="
  for p in "$STATIC_PORT" "$DASH_PORT"; do
    if lsof -nP -iTCP:"$p" -sTCP:LISTEN -t >/dev/null 2>&1; then
      echo "  :$p  LISTEN"
    else
      echo "  :$p  down"
    fi
  done
  echo "  showcase: $(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:$STATIC_PORT/docs/workshop/showcase.html 2>/dev/null || echo ERR)"
  echo "  api     : $(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:$DASH_PORT/api/reference-demos 2>/dev/null || echo ERR)"
}

stop() {
  echo "=== stopping ==="
  kill_port "$STATIC_PORT"
  kill_port "$DASH_PORT"
  echo "stopped."
}

start() {
  echo "=== starting (from Terminal context, TCC-safe) ==="
  kill_port "$STATIC_PORT"
  kill_port "$DASH_PORT"

  echo "  staging demo catalogs into starter/ ..."
  bash "$REPO/demo/reference/serve_demo.sh" stage >/dev/null

  echo "  static  :$STATIC_PORT  -> $LOG_DIR/agentloom-static.log"
  nohup /usr/bin/python3 -m http.server "$STATIC_PORT" \
    --bind 127.0.0.1 --directory "$REPO" \
    >"$LOG_DIR/agentloom-static.log" 2>&1 &

  if [ -x "$VENV_PY" ]; then
    DASH_PY="$VENV_PY"
  else
    echo "  (warning: $VENV_PY not found, falling back to /usr/bin/python3)"
    DASH_PY="/usr/bin/python3"
  fi
  echo "  dashboard:$DASH_PORT  -> $LOG_DIR/agentloom-dashboard.log"
  ( cd "$REPO" && nohup "$DASH_PY" -m uvicorn server.dashboard.app:app \
      --host 127.0.0.1 --port "$DASH_PORT" \
      >"$LOG_DIR/agentloom-dashboard.log" 2>&1 & )

  sleep 3
  status
}

case "${1:-start}" in
  start) start ;;
  stop)  stop ;;
  status) status ;;
  *) echo "usage: $0 [start|stop|status]"; exit 1 ;;
esac
