# Behavior: KG Node IDs Are Unique

**ID**: `behavior:builder:kg-node-ids-are-unique`
**Category**: kg-integrity
**Priority**: critical
**Type**: structural-invariant
**Enforcement**: hard (Tier A)
**Validator**: `scripts/validators/kg_node_ids_are_unique.py`
**Status**: Active
**Created**: 2026-05-18

---

## Rule statement

Every node in **all** active KG files (`builder-{skills,knowledge,behaviors}-graph.json` + `domain-{skills,knowledge,behaviors}-graph.json`) must have an `id`. **No two nodes — across the entire KG corpus — may share the same `id`.**

---

## Rationale

KG links (`parent`, `links.related`, `links.implements`, `links.validator`-as-id, etc.) reference nodes by `id`. If two nodes share an `id`, every link to that ID becomes ambiguous: which one does the agent dereference? The integrity validator can detect orphans (links to non-existent IDs) but cannot detect *duplicates* — that's this behavior's job.

Cross-graph uniqueness (not just per-graph) matters because:
- The master graph composes multiple per-role graphs into a single addressable namespace
- The visualizer renders all nodes in one Cytoscape canvas; duplicates produce undefined rendering behavior
- Cross-role links (`role-domain`'s skill referencing a `role-builder` behavior) require global ID resolution

---

## When this applies

### ✅ Always applies when:
- Any KG file is committed
- A new node is added in any role's KG

### ❌ Never exempt — this rule has no exceptions

---

## Failure mode example

`builder-skills-graph.json` and `domain-skills-graph.json` both contain a node with `id: "skill:utilities:format-timestamp"`:

→ `[VIOLATION] duplicate id 'skill:utilities:format-timestamp' appears in: builder-skills-graph.json (line 142), domain-skills-graph.json (line 78)`

Fix: rename one to namespace it correctly (`skill:builder:format-timestamp` vs `skill:domain:format-timestamp`), or delete the duplicate if it was an accidental copy-paste.

---

## Implementation note

The validator collects every `id` from every `nodes` / `skills` / `behaviors` / `documents` array across the 6 active graphs, then checks for collisions. It deliberately does NOT include schema definitions or proposal staging files (`proposals/*.json`) — those are pre-canonical.

---

## Related behaviors

- The KG **integrity** validator (`scripts/kg/validate_kg_integrity.py`) catches orphan links (links pointing to non-existent IDs); this validator catches the dual problem (links pointing to ambiguous IDs).

## See also

- `docs/builder/architecture/kg-node-schema.md`
- `docs/builder/governance/governance-tiers.md`
