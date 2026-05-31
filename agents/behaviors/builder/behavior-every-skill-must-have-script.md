# Behavior: Every Skill Must Have a Script

**ID**: `behavior:builder:every-skill-must-have-script`
**Category**: kg-integrity
**Priority**: high
**Type**: structural-invariant
**Enforcement**: hard (Tier A)
**Validator**: `scripts/validators/every_skill_must_have_script.py`
**Status**: Active
**Created**: 2026-05-18

---

## Rule statement

Every node in any `*-skills-graph.json` whose `type` field is `"skill"` (i.e. it is an actual capability, not a category root or grouping node) **must** have a non-empty `path` field, **and** the file at that path must exist on disk.

Category / root / grouping nodes (`type` in `{"root", "category"}`) are exempt — they exist only to organize the tree.

---

## Rationale

A skill node without a `path` is a lie. The agent cannot read its description, the human cannot review its content, the dashboard cannot link to it. We've watched this exact failure mode in markdown-soup frameworks (Anthropic Skills, Cline `.clinerules`) — orphan skill references that point nowhere and silently produce no behavior.

Forcing `path` to be both present and resolvable closes that hole at commit time.

---

## When this applies

### ✅ Always applies when:
- A new skill node is added (via `propose_node.py` or `kg_editor.add_skill`)
- An existing skill node is edited
- Pre-commit hook runs
- CI runs `make kg-validate` (the integrity validator already enforces path existence for knowledge graphs; this validator extends the same check to skills graphs)

### ❌ Does not apply when:
- Node `type` is `"root"` or `"category"` (organizational nodes)
- The graph file does not yet exist (e.g. fresh clone before bootstrap)

---

## Failure mode example

```json
{
  "id": "skill:builder:something-aspirational",
  "type": "skill",
  "name": "Something the agent should be able to do",
  "path": ""
}
```

→ Validator fails: `[VIOLATION] builder-skills-graph.json :: skill:builder:something-aspirational :: empty 'path' field`

Fix: either author the MD file at the right location and set `path`, or change `type` to `"category"` if it was meant as a placeholder.

---

## Related behaviors

- `behavior:builder:every-non-soft-behavior-has-validator` — the analogue for behavior nodes
- `behavior:builder:kg-node-ids-are-unique` — broader KG hygiene

## See also

- `docs/builder/architecture/kg-node-schema.md` — the field definitions
- `docs/builder/concepts/validator-authoring-guide.md` — how this validator was authored
