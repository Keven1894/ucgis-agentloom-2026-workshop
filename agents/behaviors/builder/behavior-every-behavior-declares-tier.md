# Behavior: Every Behavior Declares an Enforcement Tier

**ID**: `behavior:builder:every-behavior-declares-tier`
**Category**: kg-integrity
**Priority**: high
**Type**: structural-invariant
**Enforcement**: hard (Tier A)
**Validator**: `scripts/validators/every_behavior_declares_tier.py`
**Status**: Active
**Created**: 2026-05-18

---

## Rule statement

Every node in any `*-behaviors-graph.json` whose `type` field is `"rule"` **must** have an `enforcement` field whose value is one of:

- `"hard"` — Tier A, AST/regex/structural check
- `"test"` — Tier B, runtime/test-time check
- `"process"` — Tier C, CI/git/cross-system check
- `"soft"` — explicit no-validator (reviewer-judgement only)

Category / root nodes (`type` in `{"root", "category"}`) are exempt.

---

## Rationale

This is the load-bearing claim of AgentLoom: *every rule ships with its enforcement layer declared.* If we let behaviors omit the `enforcement` field, we revert to the markdown-soup state where it's unclear whether a rule is actually checked or merely suggested.

Worse: undeclared `enforcement` makes downstream behaviors (like `every-non-soft-behavior-has-validator`) impossible to evaluate, because they can't tell whether the absence of a `validator` link means "intentionally soft" or "was supposed to be hard but author forgot to wire the script".

Declaring tier explicitly forces the author to pick a side.

---

## When this applies

### ✅ Always applies when:
- A new behavior node is added
- An existing behavior node is edited
- Pre-commit hook runs

### ❌ Does not apply when:
- Node `type` is not `"rule"` (organizational nodes)

---

## Failure mode example

```json
{
  "id": "behavior:domain:always-cite-source",
  "type": "rule",
  "name": "Always cite the data source",
  "priority": "medium"
}
```

→ Validator fails: `[VIOLATION] domain-behaviors-graph.json :: behavior:domain:always-cite-source :: missing 'enforcement' field (must be hard|test|process|soft)`

Fix: add `"enforcement": "soft"` if it's genuinely guidance, or pick `"hard"`/`"test"`/`"process"` and author the corresponding validator.

---

## Related behaviors

- `behavior:builder:every-non-soft-behavior-has-validator` — checks the next link in the chain
- `behavior:builder:every-skill-must-have-script` — analogous structural check on skills

## See also

- `docs/builder/governance/governance-tiers.md` — full discussion of the tier model
- `docs/builder/concepts/validator-authoring-guide.md`
