# Local web stack (showcase + dashboard)

Two local servers for browsing reference demos:

| Service   | Port | What |
| ---       | ---  | --- |
| static    | 8766 | showcase + staged catalogs (repo root) |
| dashboard | 8000 | uvicorn KG dashboard + `/api/reference-demos` |

## TL;DR — from repo root

```bash
bash demo/serve/serve-all.sh          # start (stages demos + both servers)
bash demo/serve/serve-all.sh status   # check
bash demo/serve/serve-all.sh stop      # stop both
```

Open: http://127.0.0.1:8766/docs/workshop/showcase.html

Logs: `/tmp/agentloom-static.log`, `/tmp/agentloom-dashboard.log`

## Why Terminal, not launchd

macOS TCC blocks `launchd`-spawned processes from reading `~/Documents` → 404 on
static files. Run from Terminal (inherits Documents access). See `com.agentloom.*.plist`
files here as a **record only** — do not load them without Full Disk Access or moving
the repo out of `~/Documents`.

## Stage catalogs only

```bash
bash demo/reference/serve_demo.sh stage   # copy demo HTML → starter/
bash demo/reference/serve_demo.sh clean   # remove starter/
```
