# UPDATE_LOG: Proposal — NWIS site IDs are strings in nested timeSeries

**Date**: 2026-05-31
**Author (agent)**: cline-builder-agent
**Slug**: nwis-site-ids-are-strings-in-nested-timeseries
**Proposed node type**: knowledge
**Target graph**: domain-knowledge

---

## Justification (the "why")

Do not parse site codes as integers; walk timeSeries[].sourceInfo.siteCode[] structure.

## Source context

data/snapshots/d3-usgs-nwis-suwannee-24h.json

## Proposed node

```json
{
  "id": "knowledge:domain:nwis-site-ids-are-strings-in-nested-timeseries",
  "type": "concept",
  "data": {
    "title": "NWIS site IDs are strings in nested timeSeries",
    "description": "Do not parse site codes as integers; walk timeSeries[].sourceInfo.siteCode[] structure.",
    "category": "domain-proposed",
    "path": "docs/domain/proposed/nwis-site-ids-are-strings-in-nested-timeseries.md",
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
