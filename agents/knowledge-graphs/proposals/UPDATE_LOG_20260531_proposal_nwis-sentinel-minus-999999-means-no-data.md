# UPDATE_LOG: Proposal — NWIS -999999 means no data

**Date**: 2026-05-31
**Author (agent)**: cline-builder-agent
**Slug**: nwis-sentinel-minus-999999-means-no-data
**Proposed node type**: knowledge
**Target graph**: domain-knowledge

---

## Justification (the "why")

Streamflow IV JSON uses -999999 as missing-data sentinel; must filter before stats/map coloring.

## Source context

data/snapshots/d3-usgs-nwis-suwannee-24h.json timeSeries values

## Proposed node

```json
{
  "id": "knowledge:domain:nwis-sentinel-minus-999999-means-no-data",
  "type": "concept",
  "data": {
    "title": "NWIS -999999 means no data",
    "description": "Streamflow IV JSON uses -999999 as missing-data sentinel; must filter before stats/map coloring.",
    "category": "domain-proposed",
    "path": "docs/domain/proposed/nwis-sentinel-minus-999999-means-no-data.md",
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
