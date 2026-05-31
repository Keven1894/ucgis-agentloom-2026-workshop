# Behavior: Every Non-Soft Behavior Has a Validator

**ID**: `behavior:builder:every-non-soft-behavior-has-validator`
**Category**: kg-integrity
**Priority**: critical
**Type**: structural-invariant
**Enforcement**: hard (Tier A)
**Validator**: `scripts/validators/every_non_soft_behavior_has_validator.py`
**Status**: Active
**Created**: 2026-05-18

---

## Rule statement

Every behavior node where `enforcement` is **not** `"soft"` (i.e. `"hard"`, `"test"`, or `"process"`) **must** have a `links.validator` field whose value is a relative path to a file that exists on disk.

`enforcement: "soft"` behaviors are exempt — by definition they have no validator.

---

## Rationale

This is **the** central invariant of the framework. Without it, "executable validators" is a marketing line, not a contract.

The chain of trust is:

1. Author claims a rule is enforced (`enforcement` ≠ `soft`)
2. Therefore there must exist a validator script
3. Therefore that script must exist on disk
4. Therefore CI / pre-commit can run it
5. Therefore the rule is *actually* enforced

If step 3 silently breaks, steps 4–5 silently fail, and the framework's whole pitch collapses. This validator slams the door at step 3.

---

## When this applies

### ✅ Always applies when:
- A new behavior node is added with `enforcement` ≠ `soft`
- An existing behavior's `enforcement` is changed away from `soft`
- An existing behavior's `links.validator` is edited
- Any commit touches `*-behaviors-graph.json`

### ❌ Does not apply when:
- `enforcement` is `"soft"`
- Node `type` is not `"rule"`

---

## Failure mode examples

**Missing `links.validator`**:
```json
{
  "id": "behavior:domain:must-validate-crs",
  "type": "rule",
  "enforcement": "test",
  "links": {}
}
```
→ `[VIOLATION] ... :: missing links.validator (enforcement=test requires a validator path)`

**Validator path doesn't exist**:
```json
{
  "id": "behavior:domain:must-validate-crs",
  "type": "rule",
  "enforcement": "test",
  "links": {"validator": "scripts/validators/must_validate_crs.py"}
}
```
With no file at that path → `[VIOLATION] ... :: links.validator points to non-existent file: scripts/validators/must_validate_crs.py`

---

## Edge cases handled

- A relative path is resolved relative to the repo root
- A validator file that exists but is empty or has no `if __name__ == "__main__"` is **not** caught here — that's a Tier-B concern (test that running it produces meaningful output). For Phase 1, file-exists is sufficient.

---

## Related behaviors

- `behavior:builder:every-behavior-declares-tier` — establishes the `enforcement` field this behavior depends on
- `behavior:builder:every-skill-must-have-script` — analogous "the link must resolve" check for skills

## See also

- `docs/builder/governance/governance-tiers.md`
- `docs/builder/concepts/validator-authoring-guide.md`
