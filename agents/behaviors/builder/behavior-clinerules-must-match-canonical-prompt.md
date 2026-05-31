# Behavior: Cline rules must match canonical system-prompt KG node

**ID**: `behavior:builder:clinerules-must-match-canonical-prompt`
**Category**: kg-integrity
**Priority**: critical
**Type**: structural-invariant
**Enforcement**: hard (Tier A)
**Validator**: `scripts/validators/clinerules_must_match_system_prompt_kg_node.py`
**Status**: Active
**Created**: 2026-05-24

---

## Rule statement

The file `.clinerules/01-builder-agent-prompt.md` MUST be a verbatim, byte-for-byte re-rendering of the canonical system-prompt KG node body (the `<!-- BEGIN-PROMPT -->` … `<!-- END-PROMPT -->` span of `docs/builder/concepts/builder-agent-system-prompt.md`), as produced by `scripts/sync_clinerules.py`.

Hand-edits to `.clinerules/01-builder-agent-prompt.md` are not allowed. Any change must originate in the KG node and be propagated via `python scripts/sync_clinerules.py`.

---

## Rationale

The AgentLoom framework's "host-agnostic" claim (one builder agent, three Layer-3 hosts: standalone Python package, Cursor, Cline) is operational, not just rhetorical: all three hosts must consume the *same* system prompt for cross-host runs to be comparable.

Concretely:

- The standalone `agentloom.builder_agent` Python package loads the prompt directly from the KG node.
- Cursor consumes the same KG node when configured to use it as a system-prompt source.
- Cline reads the prompt from `.clinerules/01-builder-agent-prompt.md`, which is a **generated mirror** of the KG node.

If the mirror drifts, Cline's runs are no longer comparable to the other hosts'. The paper §Method claim about prompt-equivalence-across-hosts (and the `prompt_version` SHA equality that backs it) becomes untrue. The workshop's "you're using the same builder agent regardless of host" promise also breaks.

---

## When this applies

### ✅ Always applies when:
- The KG node `docs/builder/concepts/builder-agent-system-prompt.md` is committed.
- Any file in `.clinerules/01-builder-agent-prompt.md` is committed.
- A PR is opened touching either file.
- `python scripts/validators/run_all.py` is invoked.

### ❌ Never exempt — this rule has no exceptions

If you have a Cline-specific addition to make to the prompt, propose a change to the KG node so all three hosts pick it up. There is no Cline-only carve-out.

---

## Failure mode example

A maintainer hand-edits `.clinerules/01-builder-agent-prompt.md` to add a Cline-specific instruction (e.g. "When proposing a node, also call the `cline-context-recorder` tool"). The Cursor and standalone hosts know nothing about this tool; the cross-host comparability claim breaks silently.

→ Validator output:

```
[sync_clinerules] FAIL: drift detected between KG node and .clinerules/.
--- .clinerules\01-builder-agent-prompt.md
+++ docs/builder/concepts/builder-agent-system-prompt.md (BEGIN-PROMPT body)
@@ -42,3 +42,5 @@
 ## Output contract — what you MUST emit
+
+When proposing a node, also call the `cline-context-recorder` tool.
```

Fix:
1. Revert the hand-edit: `python scripts/sync_clinerules.py`.
2. If the addition is genuinely needed, propose it as a change to the KG node, accept it through the normal flow, then re-run sync.

---

## Implementation note

The validator (`scripts/validators/clinerules_must_match_system_prompt_kg_node.py`) is a thin shim over `scripts/sync_clinerules.py --check`. It does not duplicate the comparison logic; both paths use `agentloom.builder_agent.kg_context.load_system_prompt()` to extract the canonical body and SHA. Drift is detected by exact byte-equality after the generation header is prepended.

The generation header pinned in `.clinerules/01-builder-agent-prompt.md` includes the current `prompt_version` SHA so reviewers can spot at a glance which prompt revision is in effect.

---

## Related behaviors

- `behavior:builder:kg-node-ids-are-unique` — sister rule for KG-level integrity.
- `behavior:builder:every-non-soft-behavior-has-validator` — meta-rule that this behavior itself must satisfy (it does: validator path declared in `links.validator`).

## See also

- `docs/plan/complete/2026-05-24-w1-wave-a-complete.md` — wave-A summary that introduced `.clinerules/` + sync script.
- `docs/builder/concepts/builder-agent-system-prompt.md` — the canonical KG node.
- `scripts/sync_clinerules.py` — the generator.
