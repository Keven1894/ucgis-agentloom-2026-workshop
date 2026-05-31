# Behavior: Catalog UI Must Tell the Full Story

**ID**: `behavior:builder:catalog-ui-must-tell-the-story`
**Category**: catalog-discipline
**Priority**: high
**Type**: ui-discipline-rule
**Enforcement**: hard (Tier A)
**Validator**: `scripts/validators/catalog_ui_must_tell_the_story.py`
**Status**: Active
**Created**: 2026-05-18

---

## Rule statement

Every `starter/<app>/index.html` MUST contain eight elements carrying these `data-catalog-role` attribute values:

`title`, `provenance`, `acquisition`, `data-shape`, `processing`, `kg-link`, `reuse`, `data-view`

Each section must have non-empty inner content (not just empty tags or HTML comments).

---

## Rationale

A catalog without provenance is a museum exhibit with no plaque. A catalog without acquisition is a black box. A catalog without `kg-link` hides the framework that produced it. A catalog without `reuse` is dead-end content. The eight sections together force every workshop catalog to answer the questions a real data consumer asks BEFORE staring at the map.

This is the framework's UI-level companion to the data-level rule `behavior:domain:all-timestamps-must-be-utc-iso8601`. Both encode "do the right thing or CI fails."

See `knowledge:builder:data-catalog-ui-storytelling` for the full taxonomy + design principles.

---

## When this applies

### ✅ Always applies when:
- Any HTML file is added or modified under `starter/*/index.html`
- CI runs

### ❌ Does not apply when:
- The file contains the exact comment `<!-- catalog-storytelling: bootstrapping -->` (transitional exemption — must be removed in the next commit per the hard-launch / paired-commit pattern)
- The path is not `starter/*/index.html` (this rule scopes only to canonical catalog apps)

---

## Failure mode example

A `starter/my-app/index.html` containing only:

```html
<h1>My App</h1>
<div id="map"></div>
```

→ violations:
```
[VIOLATION] starter/my-app/index.html :: missing data-catalog-role: title (only <h1> not in a marked section)
[VIOLATION] starter/my-app/index.html :: missing data-catalog-role: provenance
[VIOLATION] starter/my-app/index.html :: missing data-catalog-role: acquisition
... and 5 more
```

Fix: wrap content in 8 `<section data-catalog-role="…">` blocks per the storytelling taxonomy.

---

## Related behaviors

- `behavior:builder:catalog-must-embed-dataset-jsonld` — sister rule for machine-readable metadata
- `behavior:builder:every-skill-must-have-script` — unrelated structural rule

## Uses knowledge

- `knowledge:builder:data-catalog-ui-storytelling` — defines the eight sections
- `knowledge:builder:governance-tiers` — defines what Tier A means
