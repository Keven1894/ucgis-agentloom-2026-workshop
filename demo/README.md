# Demo reference builds (UCGIS 2026 workshop)

Finished **D1–D4 reference catalogs** and their domain KG snapshots — what attendees
build during the workshop, completed by the organizers. Use these to **practice the
workflow** and **compare your outcome** against a validators-green finish line.

## Layout

```
demo/
├── reference/           # D1–D4 finished builds (catalog HTML + domain KG + PROMPTS drafts)
│   ├── manifest.json    # showcase hub metadata
│   ├── serve_demo.sh    # stage catalogs → starter/ and serve :8766
│   └── d1-earthquakes/ … d4-natural-earth/
└── serve/
    ├── serve-all.sh     # stage + start :8766 static + :8000 dashboard
    └── README.md
```

## Quick start (browse demos)

From the repo root, with `.venv` installed:

```bash
bash demo/serve/serve-all.sh
```

Then open:

- **Showcase hub:** http://127.0.0.1:8766/docs/workshop/showcase.html
- **Dashboard:** http://127.0.0.1:8000/ (use `?ref=d1-earthquakes` etc. for KG overlay)

Full server guide: [`docs/workshop/start-workshop-servers.md`](../docs/workshop/start-workshop-servers.md)

`serve-all.sh` stages `demo/reference/*/index.html` into `starter/` (gitignored) so
live catalog links work over HTTP.

## Practice on your own

1. Fork this repo and clone **your fork** into a separate directory (not this demo tree).
2. Follow [`docs/workshop/01-setup.md`](../docs/workshop/01-setup.md) and pick a prompt pack (D1–D4).
3. Build your catalog + domain KG nodes from scratch.
4. Compare against the matching folder under `demo/reference/<id>/`.

Your fork's committed KG stays **root-only** — the demo domain graphs are read-only overlays
via dashboard `?ref=`, not copied into `agents/knowledge-graphs/`.

## Maintainer notes

- Re-capture screenshots: `demo/reference/capture_screenshots.py` (needs Playwright + `:8766` server)
- Stage only: `bash demo/reference/serve_demo.sh stage`
- Clean staged catalogs: `bash demo/reference/serve_demo.sh clean`
