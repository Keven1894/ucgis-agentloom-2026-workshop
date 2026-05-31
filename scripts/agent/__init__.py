"""agentloom.builder_agent — canonical reference builder agent.

The builder agent reads a task + a small data sample + the existing knowledge
graph context, and emits structured proposals for new knowledge nodes via the
existing propose-review CLI tooling. Any IDE/host integration (Cline, Cursor,
CI, MCP-based hosts) is conceptually a wrapper over this package.

Public entry points::

    from scripts.agent import BuilderAgent           # programmatic
    python -m scripts.agent.builder_agent ...        # CLI

The package is intentionally small. Everything intelligent happens through
the LLM call; the rest is plumbing that keeps the contract honest:
  - KG-as-context (kg_context.py)
  - LLM provider abstraction (llm_client.py)
  - Tolerant JSON output parsing + schema validation (proposal_io.py)
  - Per-run JSONL log for paper-grade reproducibility (run_log.py)
"""

from .builder_agent import BuilderAgent, AgentRunResult  # noqa: F401

__all__ = ["BuilderAgent", "AgentRunResult"]
