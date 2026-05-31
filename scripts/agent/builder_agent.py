"""builder_agent.py — canonical reference builder agent (CLI + library).

Reads:
  - the canonical system prompt KG node (docs/builder/concepts/builder-agent-system-prompt.md)
  - the existing KG (compact id+title summary)
  - a task description + a small data sample
Calls one LLM completion. Parses the LLM's structured proposals output.
Shells out to scripts/kg/propose_node.py for each valid proposal.
Writes a JSONL run log to runs/agent/<ts>-<model>-<task>.jsonl.

Library use:

    from scripts.agent import BuilderAgent

    agent = BuilderAgent(model="gpt-5.2")
    result = agent.run(
        task="Ingest USGS NWIS streamflow into catalog",
        snapshot_path="data/snapshots/d3-usgs-nwis-fl-stations-24h.json",
        dry_run=True,
    )
    for p in result.parsed.proposals:
        print(p.slug, p.confidence)

CLI use:

    python -m scripts.agent.builder_agent \\
        --task "Ingest USGS NWIS streamflow into catalog" \\
        --snapshot data/snapshots/d3-usgs-nwis-fl-stations-24h.json \\
        --model gpt-5.2 \\
        --dry-run
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

WORKSPACE = Path(__file__).resolve().parents[2]
if str(WORKSPACE) not in sys.path:
    sys.path.insert(0, str(WORKSPACE))

from scripts.agent.kg_context import (  # noqa: E402
    load_node_stubs,
    existing_ids,
    render_kg_summary,
    load_system_prompt,
    truncate_snapshot,
)
from scripts.agent.llm_client import LLMClient, LLMResponse  # noqa: E402
from scripts.agent.proposal_io import (  # noqa: E402
    parse_agent_json,
    validate_agent_output,
    submit_proposal,
    ParsedAgentOutput,
    ProposalParseError,
)
from scripts.agent.run_log import RunLog  # noqa: E402


@dataclass
class AgentRunResult:
    parsed: ParsedAgentOutput
    llm: LLMResponse
    submissions: list[dict[str, Any]]
    log_path: Path
    prompt_version: str


class BuilderAgent:
    def __init__(
        self,
        *,
        model: str = "gpt-5.2",
        api_key: str | None = None,
        base_url: str | None = None,
        env_path: Path | None = None,
        log_dir: Path | None = None,
    ) -> None:
        self.client = LLMClient(
            model=model,
            api_key=api_key,
            base_url=base_url,
            env_path=env_path or (WORKSPACE / ".env"),
        )
        self.log = RunLog(log_dir=log_dir)
        self.system_prompt, self.prompt_version = load_system_prompt()

    def build_user_message(self, task: str, kg_summary: str, snapshot_excerpt: str,
                           snapshot_name: str) -> str:
        return (
            f"TASK: {task}\n\n"
            f"DATA SOURCE: {snapshot_name}\n"
            f"DATA SAMPLE (truncated to keep context bounded):\n"
            f"```\n{snapshot_excerpt}\n```\n\n"
            f"{kg_summary}\n"
            "Now: read the task, read the data sample, read the existing KG, and "
            "decide what (if any) new knowledge nodes the domain knowledge graph "
            "should contain. Respond with the JSON object the system prompt's "
            "OUTPUT CONTRACT specifies, and nothing else."
        )

    def run(
        self,
        *,
        task: str,
        snapshot_path: str | Path,
        max_snapshot_bytes: int = 2048,
        temperature: float = 0.2,
        dry_run: bool = False,
        author: str = "builder-agent",
    ) -> AgentRunResult:
        snap_path = Path(snapshot_path)
        if not snap_path.is_absolute():
            snap_path = WORKSPACE / snap_path
        if not snap_path.exists():
            raise FileNotFoundError(f"snapshot not found: {snap_path}")

        stubs = load_node_stubs()
        ids_now = existing_ids(stubs)
        kg_summary = render_kg_summary(stubs)
        snap_excerpt = truncate_snapshot(snap_path, max_bytes=max_snapshot_bytes)
        user_msg = self.build_user_message(
            task=task, kg_summary=kg_summary,
            snapshot_excerpt=snap_excerpt, snapshot_name=snap_path.name,
        )

        log_path = self.log.open(
            model=self.client.model, task=task, snapshot_name=snap_path.name,
            prompt_version=self.prompt_version, base_url=self.client.base_url,
            dry_run=dry_run,
        )

        self.log.write({"kind": "kg_summary",
                        "node_count": len(stubs),
                        "summary_first_400_chars": kg_summary[:400]})

        try:
            llm = self.client.complete(
                system=self.system_prompt, user=user_msg, temperature=temperature,
            )
        except Exception as e:  # noqa: BLE001
            self.log.write({"kind": "llm_error", "error": str(e)})
            self.log.close(status="llm_error")
            raise

        self.log.write({
            "kind": "llm_call",
            "model": llm.model, "base_url": llm.base_url,
            "elapsed_seconds": llm.elapsed_seconds,
            "prompt_tokens": llm.prompt_tokens, "completion_tokens": llm.completion_tokens,
            "finish_reason": llm.finish_reason,
            "system_prompt_chars": len(self.system_prompt),
            "user_prompt_chars": len(user_msg),
            "raw_response": llm.raw_text,
        })

        try:
            parsed_obj = parse_agent_json(llm.raw_text)
        except ProposalParseError as e:
            self.log.write({"kind": "parse_error", "error": str(e),
                            "raw_response_first_400": llm.raw_text[:400]})
            self.log.close(status="parse_error")
            raise

        parsed = validate_agent_output(parsed_obj, existing_ids=ids_now)
        self.log.write({"kind": "parsed_output",
                        "reasoning": parsed.reasoning,
                        "proposal_count": len(parsed.proposals),
                        "proposals": parsed.proposals})

        submissions: list[dict[str, Any]] = []
        for p in parsed.proposals:
            res = submit_proposal(p, author=author, dry_run=dry_run)
            self.log.write({"kind": "submission",
                            "future_id": f"{p.type}:{p.target_role}:{p.slug}",
                            "result": res})
            submissions.append({"proposal": p, "result": res})

        self.log.close(status="ok", stats={
            "submission_count": len(submissions),
            "submission_succeeded": sum(1 for s in submissions if s["result"]["returncode"] == 0),
        })

        return AgentRunResult(
            parsed=parsed, llm=llm, submissions=submissions,
            log_path=log_path, prompt_version=self.prompt_version,
        )


def _cli() -> int:
    p = argparse.ArgumentParser(
        description="AgentLoom builder agent — propose knowledge nodes from a data sample"
    )
    p.add_argument("--task", required=True, help="task description for the agent")
    p.add_argument("--snapshot", required=True, help="path to a vendored data snapshot")
    p.add_argument("--model", default="gpt-5.2",
                   help="LLM model id (default: gpt-5.2)")
    p.add_argument("--base-url", default=None,
                   help="OpenAI-compatible base URL (default: openai.com). "
                        "Set to https://openrouter.ai/api/v1 etc. to swap providers")
    p.add_argument("--api-key", default=None, help="override OPENAI_API_KEY")
    p.add_argument("--max-snapshot-bytes", type=int, default=2048)
    p.add_argument("--temperature", type=float, default=0.2)
    p.add_argument("--dry-run", action="store_true",
                   help="parse and validate the LLM output but DON'T shell out to "
                        "propose_node.py — useful for prompt iteration without "
                        "polluting the proposals queue")
    args = p.parse_args()

    agent = BuilderAgent(
        model=args.model, api_key=args.api_key, base_url=args.base_url,
    )
    try:
        result = agent.run(
            task=args.task,
            snapshot_path=args.snapshot,
            max_snapshot_bytes=args.max_snapshot_bytes,
            temperature=args.temperature,
            dry_run=args.dry_run,
        )
    except ProposalParseError as e:
        print(f"[builder-agent] LLM output unparseable: {e}", file=sys.stderr)
        return 2

    print()
    print(f"[builder-agent] model         : {result.llm.model} via {result.llm.base_url}")
    print(f"[builder-agent] prompt_version: {result.prompt_version}")
    print(f"[builder-agent] tokens        : {result.llm.prompt_tokens} in / "
          f"{result.llm.completion_tokens} out (elapsed {result.llm.elapsed_seconds:.1f}s)")
    print(f"[builder-agent] reasoning     : {result.parsed.reasoning[:200]}"
          f"{'...' if len(result.parsed.reasoning) > 200 else ''}")
    print(f"[builder-agent] proposals     : {len(result.parsed.proposals)}")
    for p in result.parsed.proposals:
        future = f"{p.type}:{p.target_role}:{p.slug}"
        print(f"  - [{p.confidence}] {future} :: {p.title}")
    print(f"[builder-agent] log file      : {result.log_path}")
    if args.dry_run:
        print("[builder-agent] dry-run mode — proposals NOT written to "
              "agents/knowledge-graphs/proposals/")
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
