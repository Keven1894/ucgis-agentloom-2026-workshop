"""Tolerant LLM-output JSON parsing + structural validation + delegation
to the existing propose_node.py CLI.

Three-layer parsing fallback:
  1. strict json.loads
  2. strip ```json``` / ``` markdown code fences then strict
  3. find first balanced {...} substring then strict
After parsing, every proposal is validated against a small Python schema
(NOT pulled from the JSON-schema files — those describe the *accepted*
node shape; the LLM emits a more compact proposal record). Then we shell
out to scripts/kg/propose_node.py per proposal so all the existing
schema/validator pipeline applies untouched.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

WORKSPACE = Path(__file__).resolve().parents[2]


class ProposalParseError(Exception):
    pass


@dataclass
class ParsedProposal:
    type: str            # 'knowledge' (v1 only)
    target_role: str     # 'domain' | 'builder'
    slug: str
    title: str
    node_subtype: str
    justification: str
    source_context: str
    links_uses: list[str]
    confidence: str


@dataclass
class ParsedAgentOutput:
    reasoning: str
    proposals: list[ParsedProposal]


# ----- parsing -----------------------------------------------------------

_FENCE_RE = re.compile(r"```(?:json)?\s*(.*?)```", re.DOTALL | re.IGNORECASE)


def _strip_fence(s: str) -> str | None:
    m = _FENCE_RE.search(s)
    if m:
        return m.group(1).strip()
    return None


def _first_balanced_brace(s: str) -> str | None:
    """Find the first balanced {...} substring (handles nested braces +
    string-aware so braces inside JSON strings don't fool the counter)."""
    start = s.find("{")
    if start == -1:
        return None
    depth = 0
    in_str = False
    escape = False
    for i in range(start, len(s)):
        c = s[i]
        if escape:
            escape = False
            continue
        if in_str:
            if c == "\\":
                escape = True
            elif c == '"':
                in_str = False
            continue
        if c == '"':
            in_str = True
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return s[start:i + 1]
    return None


def parse_agent_json(raw: str) -> dict[str, Any]:
    """Three-layer tolerant parse. Raises ProposalParseError if all fail."""
    candidates: list[str] = [raw.strip()]
    fenced = _strip_fence(raw)
    if fenced:
        candidates.append(fenced)
    balanced = _first_balanced_brace(raw)
    if balanced:
        candidates.append(balanced)
    last_err: Exception | None = None
    for c in candidates:
        try:
            obj = json.loads(c)
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError as e:
            last_err = e
    raise ProposalParseError(
        f"could not parse JSON from LLM output ({len(raw)} chars). "
        f"last error: {last_err}"
    )


# ----- structural validation ---------------------------------------------

_REQUIRED_TOP = {"reasoning", "proposals"}
_REQUIRED_PROPOSAL = {
    "type", "target_role", "slug", "title", "node_subtype",
    "justification", "source_context", "confidence",
}
_VALID_TYPES = {"knowledge"}                  # v1 scope
_VALID_ROLES = {"domain", "builder"}
_VALID_CONFIDENCE = {"high", "medium", "low"}
_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$")


def validate_agent_output(obj: dict[str, Any], existing_ids: set[str]) -> ParsedAgentOutput:
    """Structurally validate the parsed JSON. Drops malformed proposals with a
    warning rather than crashing the whole run, so partial successes still log.
    """
    missing = _REQUIRED_TOP - obj.keys()
    if missing:
        raise ProposalParseError(f"agent JSON missing top-level keys: {missing}")

    proposals_raw = obj.get("proposals") or []
    if not isinstance(proposals_raw, list):
        raise ProposalParseError("'proposals' must be a list")

    out: list[ParsedProposal] = []
    for i, p in enumerate(proposals_raw):
        if not isinstance(p, dict):
            print(f"[validate] proposals[{i}] not a dict, skipping", file=sys.stderr)
            continue
        miss = _REQUIRED_PROPOSAL - p.keys()
        if miss:
            print(f"[validate] proposals[{i}] missing fields {miss}, skipping",
                  file=sys.stderr)
            continue
        ptype = str(p.get("type"))
        role = str(p.get("target_role"))
        slug = str(p.get("slug"))
        if ptype not in _VALID_TYPES:
            print(f"[validate] proposals[{i}] type={ptype!r} not in {_VALID_TYPES}, skipping",
                  file=sys.stderr)
            continue
        if role not in _VALID_ROLES:
            print(f"[validate] proposals[{i}] target_role={role!r} not in {_VALID_ROLES}, skipping",
                  file=sys.stderr)
            continue
        if not _SLUG_RE.match(slug):
            print(f"[validate] proposals[{i}] slug={slug!r} not kebab-case, skipping",
                  file=sys.stderr)
            continue
        future_id = f"{ptype}:{role}:{slug}"
        if future_id in existing_ids:
            print(f"[validate] proposals[{i}] {future_id!r} already exists in KG, skipping",
                  file=sys.stderr)
            continue
        confidence = str(p.get("confidence", "medium"))
        if confidence not in _VALID_CONFIDENCE:
            confidence = "medium"
        links_uses_raw = p.get("links_uses") or []
        if not isinstance(links_uses_raw, list):
            links_uses_raw = []
        # filter links_uses to existing IDs only — agent tends to hallucinate
        links_uses = [
            str(x) for x in links_uses_raw
            if isinstance(x, str) and str(x) in existing_ids
        ]
        out.append(ParsedProposal(
            type=ptype,
            target_role=role,
            slug=slug,
            title=str(p.get("title", "")).strip(),
            node_subtype=str(p.get("node_subtype", "concept")).strip() or "concept",
            justification=str(p.get("justification", "")).strip(),
            source_context=str(p.get("source_context", "")).strip(),
            links_uses=links_uses,
            confidence=confidence,
        ))
    return ParsedAgentOutput(reasoning=str(obj.get("reasoning", "")).strip(), proposals=out)


# ----- shell-out to propose_node.py --------------------------------------

def submit_proposal(p: ParsedProposal, *, author: str = "builder-agent",
                    dry_run: bool = False, md_path: str | None = None) -> dict[str, Any]:
    """Run scripts/kg/propose_node.py for one proposal. Returns a result
    dict with stdout/stderr/returncode for the run log.
    """
    cmd = [
        sys.executable, "scripts/kg/propose_node.py",
        "--type", p.type,
        "--target-role", p.target_role,
        "--slug", p.slug,
        "--title", p.title,
        "--justification", p.justification,
        "--source-context", p.source_context,
        "--node-subtype", p.node_subtype,
        "--author", author,
    ]
    if md_path:
        cmd += ["--path", md_path]
    if p.links_uses:
        cmd += ["--links-json", json.dumps({"uses": p.links_uses})]

    if dry_run:
        return {"dry_run": True, "cmd": cmd, "returncode": 0,
                "stdout": "[dry-run] would run propose_node.py", "stderr": ""}
    res = subprocess.run(cmd, capture_output=True, text=True, cwd=WORKSPACE)
    return {
        "dry_run": False,
        "cmd": cmd,
        "returncode": res.returncode,
        "stdout": res.stdout,
        "stderr": res.stderr,
    }
