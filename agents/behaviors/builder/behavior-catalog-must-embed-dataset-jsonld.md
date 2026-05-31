# Behavior: Catalog Must Embed Schema.org Dataset JSON-LD

**ID**: `behavior:builder:catalog-must-embed-dataset-jsonld`
**Category**: catalog-discipline
**Priority**: high
**Type**: ui-discipline-rule
**Enforcement**: hard (Tier A)
**Validator**: `scripts/validators/catalog_must_embed_dataset_jsonld.py`
**Status**: Active
**Created**: 2026-05-18

---

## Rule statement

Every `starter/<app>/index.html` MUST contain at least one `<script type="application/ld+json">` block whose JSON parses successfully and contains an object (or member of an array) with:

- `@context` set to `"https://schema.org/"` or `"http://schema.org/"`  
- `@type` set to `"Dataset"`
- All of: `name`, `description`, `url`, `license`, `creator`, `distribution`, `dateModified`

Recommended (validated by audit skill, NOT enforced here):
`temporalCoverage`, `spatialCoverage`, `keywords`, `version`, `identifier`.

---

## Rationale

The visible storytelling sections answer human questions. Schema.org JSON-LD answers machine questions: Google Dataset Search, federated FAIR registries, and academic citation tools all consume it.

Embedding a valid `Dataset` JSON-LD block in catalog HTML costs ~30 lines per app and turns every workshop catalog from "isolated demo" into "discoverable open-web resource". Without enforcement, attendees skip it; with enforcement, it becomes muscle memory.

See `knowledge:builder:dataset-jsonld-discovery` for the field-by-field reference.

---

## When this applies

### ✅ Always applies when:
- Any HTML file is added or modified under `starter/*/index.html`
- CI runs

### ❌ Does not apply when:
- The file contains the exact comment `<!-- jsonld-discovery: bootstrapping -->` (transitional exemption per hard-launch / paired-commit pattern)

---

## Failure mode examples

**No JSON-LD block at all**:
```
[VIOLATION] starter/my-app/index.html :: no <script type="application/ld+json"> block found.
```

**JSON-LD parses but wrong @type**:
```html
<script type="application/ld+json">{"@context":"https://schema.org/","@type":"WebPage"}</script>
```
→ `[VIOLATION] starter/my-app/index.html :: no JSON-LD object with @type=Dataset.`

**Dataset present but missing required fields**:
```
[VIOLATION] starter/my-app/index.html :: Dataset missing required fields: license, creator, distribution.
```

---

## Related behaviors

- `behavior:builder:catalog-ui-must-tell-the-story` — sister rule for visible storytelling sections; both must pass for a catalog to be CI-clean

## Uses knowledge

- `knowledge:builder:dataset-jsonld-discovery` — full reference + worked example
- `knowledge:builder:governance-tiers`

## See also

- Schema.org Dataset: https://schema.org/Dataset
- Google Dataset Search structured data: https://developers.google.com/search/docs/data-types/dataset
