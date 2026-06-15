# Starting the local servers (showcase + dashboard)

How to bring up the two local web servers to browse reference demos and run the KG dashboard.

## TL;DR

From **your clone root**:

```bash
bash demo/serve/serve-all.sh
```

**Leave that Terminal window open** while browsing. Then open:

> http://127.0.0.1:8766/docs/workshop/showcase.html

To keep the laptop from sleeping (run in another tab):

```bash
caffeinate -dimsu &
```

## What it starts

| Service   | URL | What |
| ---       | --- | --- |
| static    | http://127.0.0.1:8766 | showcase + staged catalogs (serves repo root) |
| dashboard | http://127.0.0.1:8000 | KG dashboard + `/api/reference-demos` |

Key links:

- Showcase hub: http://127.0.0.1:8766/docs/workshop/showcase.html
- Dashboard: http://127.0.0.1:8000/

`serve-all.sh` stages `demo/reference/*/index.html` into gitignored `starter/` before starting servers.

## Script commands

```bash
bash demo/serve/serve-all.sh          # start (stages demos, kills stale ports first)
bash demo/serve/serve-all.sh status   # show port + HTTP status
bash demo/serve/serve-all.sh stop      # stop both
```

Logs: `/tmp/agentloom-static.log`, `/tmp/agentloom-dashboard.log`

## Verify it's healthy

```bash
bash demo/serve/serve-all.sh status
# expect:
#   :8766  LISTEN
#   :8000  LISTEN
#   showcase: 200
#   api     : 200
```

## Why a Terminal script and NOT launchd / auto-start

macOS TCC denies `launchd`-spawned processes read access to `~/Documents`, so a
LaunchAgent `http.server` returns empty listings + 404. Start from **Terminal** instead.

More detail: [`demo/serve/README.md`](../../demo/serve/README.md) (launchd plist notes, stage-only commands).

## Troubleshooting

- **404 on :8766** — run `serve-all.sh stop` then `serve-all.sh start` from Terminal.
- **`Address already in use`** — `serve-all.sh start` kills stale listeners first; or:
  `lsof -nP -iTCP:8766 -sTCP:LISTEN -t | xargs kill`
- **Practice on a second clone** — use a different dashboard port, e.g.
  `.venv/bin/python -m uvicorn server.dashboard.app:app --port 8001 --host 127.0.0.1`
  and open http://127.0.0.1:8001 ( `:8000` may already be in use).
