# UPDATE_LOG: Proposal — NWIS parameter codes are opaque 5-digit strings

**Date**: 2026-05-31
**Author (agent)**: cline-builder-agent
**Slug**: nwis-parameter-codes-are-opaque-5-digit-strings
**Proposed node type**: knowledge
**Target graph**: domain-knowledge

---

## Justification (the "why")

00060 discharge cfs etc.; catalog must label parameterCode not assume meaning from digits alone.

## Source context

data/snapshots/d3-usgs-nwis-suwannee-24h.json variable parameterCode

## Proposed node

```json
{
  "id": "knowledge:domain:nwis-parameter-codes-are-opaque-5-digit-strings",
  "type": "concept",
  "data": {
    "title": "NWIS parameter codes are opaque 5-digit strings",
    "description": "00060 discharge cfs etc.; catalog must label parameterCode not assume meaning from digits alone.",
    "category": "domain-proposed",
    "path": "docs/domain/proposed/nwis-parameter-codes-are-opaque-5-digit-strings.md",
    "tags": [
      "domain",
      "proposed"
    ]
  },
  "relationships": {
    "parent": "knowledge:domain:root",
    "children": []
  }
}
```

## Reviewer notes

_(none)_
