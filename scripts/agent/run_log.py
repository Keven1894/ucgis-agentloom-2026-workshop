"""Per-run JSONL log writer.

Captures everything needed for paper-grade reproducibility of any agent
run: which prompt version, which model, which provider, full text of the
prompt + LLM response, parsed proposals, validation outcomes, propose_node
shell-out results.

A run log is a single JSONL file under runs/agent/, one record per LLM
call (v1 = always 1 record per run; v2 multi-turn would be N records).
The first record always carries the run header; subsequent records are
turn details. Names are <UTC-Z timestamp>-<model>-<task-slug>.jsonl.
"""

from __future__ import annotations

import datetime as dt
import json
import re
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

WORKSPACE = Path(__file__).resolve().parents[2]
DEFAULT_LOG_DIR = WORKSPACE / "runs" / "agent"


def _slugify(s: str, maxlen: int = 40) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s[:maxlen] or "untitled"


def _utc_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _safe(obj: Any) -> Any:
    if is_dataclass(obj) and not isinstance(obj, type):
        return {k: _safe(v) for k, v in asdict(obj).items()}
    if isinstance(obj, dict):
        return {str(k): _safe(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_safe(v) for v in obj]
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    return str(obj)


class RunLog:
    def __init__(self, log_dir: Path | None = None):
        self.log_dir = log_dir or DEFAULT_LOG_DIR
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.path: Path | None = None
        self.opened = False

    def open(self, *, model: str, task: str, snapshot_name: str | None,
             prompt_version: str, base_url: str, dry_run: bool) -> Path:
        ts = _utc_iso().replace(":", "").replace("-", "")
        slug = _slugify(f"{model}-{task}")
        self.path = self.log_dir / f"{ts}-{slug}.jsonl"
        self.write({
            "kind": "run_header",
            "started_at": _utc_iso(),
            "model": model,
            "base_url": base_url,
            "prompt_version": prompt_version,
            "task": task,
            "snapshot": snapshot_name,
            "dry_run": dry_run,
        })
        self.opened = True
        return self.path

    def write(self, record: dict[str, Any]) -> None:
        if self.path is None:
            raise RuntimeError("RunLog.write called before .open()")
        line = json.dumps(_safe(record), ensure_ascii=False)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(line + "\n")

    def close(self, *, status: str, stats: dict[str, Any] | None = None) -> None:
        if not self.opened:
            return
        self.write({
            "kind": "run_footer",
            "ended_at": _utc_iso(),
            "status": status,
            "stats": stats or {},
        })
