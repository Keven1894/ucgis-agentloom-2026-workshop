# Story map must answer four viewer questions at a glance

**Node ID**: `knowledge:domain:story-map-must-answer-four-viewer-questions`  
**Type**: concept · **Category**: domain-proposed  
**Created**: 2026-06-02

---

## Rule

After a geospatial story-map / data-catalog UI loads real data, a **first-time viewer** (not the builder agent) must be able to answer these four questions **without reading JSON paths, file paths, or code**:

| # | Question | Typical section | Must include |
| --- | --- | --- | --- |
| 1 | **Where is this data from?** | `provenance` | Organization name, upstream feed, snapshot vs live, license |
| 2 | **What is it?** | `title` + `data-shape` | Variable measured, units, geography, time window — in plain language |
| 3 | **How can I use it?** | `reuse` | Citation hint, license, download/remix path |
| 4 | **What am I looking at right now?** | `title` or live panel | Live counts, map extent, date range of values on screen, active filters |

Structural compliance (`behavior:builder:catalog-ui-must-tell-the-story`) is **necessary but not sufficient**. A page with eight ≥10-char sections that only mention `value.timeSeries[]` fails this rule.

---

## When to apply

- **Phase 5c (polish)**, after data wiring (Phase 5) and optional scale enrich (Phase 5b).
- Propose this node when the catalog **works** but a human says "I still don't know what I'm looking at."

Do **not** propose during Phase 2 discovery on schema foot-guns — that is a different concern (D7 one concept per node).

---

## Evidence (D3 streamflow, 2026-06-02)

Before polish: sidebar listed NWIS JSON nesting and relative paths; map showed markers with no plain-language summary.

After polish: an **At a glance** panel fills from loaded data (6 Florida gages, discharge cfs, 24 h window, latest observation times).

---

## Anti-patterns

- ❌ Only developer jargon in provenance/data-shape ("fetch `../../data/snapshots/...`")
- ❌ Map + sparklines with no sentence explaining what the dots represent
- ❌ Burying all narrative in JSON-LD while sidebar stays empty

---

## Related framework nodes

- `knowledge:builder:data-catalog-ui-storytelling` — eight required sections (structural)
- `behavior:builder:catalog-ui-must-tell-the-story` — Tier-A structural validator

This domain node adds **narrative quality** on top of structural storytelling for geospatial catalog / story-map UIs.
