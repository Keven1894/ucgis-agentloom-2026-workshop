#!/usr/bin/env python3
"""Build the attendee-facing workshop repo from a dev-repo ref.

Usage:
  python scripts/build_workshop_snapshot.py --output ../ucgis-agentloom-2026-workshop
  python scripts/build_workshop_snapshot.py --ref feature/builder-agent --dry-run
  python scripts/build_workshop_snapshot.py --output /tmp/ws --validate

See docs/plan/todo/2026-05-31-w3-workshop-starter-repo.md
"""

from __future__ import annotations

import argparse
import fnmatch
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OVERLAY = REPO_ROOT / "docs" / "workshop" / "snapshot-overlay"

# Top-level or subtree paths excluded from the workshop edition.
EXCLUDE_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    "docs/plan",
    "docs/research",
    "docs/workshop/snapshot-overlay",
    "runs",
    "starter",
    "scripts/domain",
    "dist",
}

EXCLUDE_FILES = {
    "PLAN.md",
    "scripts/compare_cline_to_baseline.py",
}

# Glob patterns relative to repo root (applied to files only).
EXCLUDE_GLOBS = [
    "agents/knowledge-graphs/proposals/*.json",
    "agents/knowledge-graphs/proposals/UPDATE_LOG_*.md",
]


def _run_git(args: list[str], cwd: Path) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def list_tracked_files(ref: str, repo: Path) -> list[str]:
    """Return repo-relative paths at ``ref`` (includes untracked when ref=WORKTREE)."""
    if ref == "WORKTREE":
        out = _run_git(["ls-files", "-co", "--exclude-standard"], repo)
        return [line for line in out.splitlines() if line.strip()]
    out = _run_git(["ls-tree", "-r", "--name-only", ref], repo)
    return [line for line in out.splitlines() if line.strip()]


def should_exclude(rel: str) -> bool:
    parts = Path(rel).parts
    for ex in EXCLUDE_DIRS:
        ex_parts = Path(ex).parts
        if len(parts) >= len(ex_parts) and parts[: len(ex_parts)] == ex_parts:
            return True
    if rel.replace("\\", "/") in EXCLUDE_FILES:
        return True
    norm = rel.replace("\\", "/")
    for pattern in EXCLUDE_GLOBS:
        if fnmatch.fnmatch(norm, pattern):
            return True
    return False


def materialize_ref(ref: str, repo: Path, staging: Path) -> None:
    """Copy tracked files at ref into staging (or working tree when WORKTREE)."""
    files = [f for f in list_tracked_files(ref, repo) if not should_exclude(f)]
    for rel in files:
        src = repo / rel
        dst = staging / rel
        if ref == "WORKTREE":
            if not src.is_file():
                continue
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
        else:
            blob = _run_git(["show", f"{ref}:{rel}"], repo)
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(blob, encoding="utf-8", newline="\n")


def apply_overlay(staging: Path) -> None:
    if not OVERLAY.is_dir():
        raise SystemExit(f"Overlay directory missing: {OVERLAY}")
    for src in OVERLAY.rglob("*"):
        if src.is_dir():
            continue
        rel = src.relative_to(OVERLAY)
        if rel.name == "WORKSHOP-README.md":
            dst = staging / "README.md"
        else:
            dst = staging / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def ensure_proposals_gitkeep(staging: Path) -> None:
    prop = staging / "agents" / "knowledge-graphs" / "proposals"
    prop.mkdir(parents=True, exist_ok=True)
    for p in prop.iterdir():
        if p.name != ".gitkeep":
            p.unlink()
    keep = prop / ".gitkeep"
    if not keep.exists():
        keep.write_text("", encoding="utf-8")


def copy_untracked_workshop_extras(repo: Path, staging: Path, ref: str) -> None:
    """When building from WORKTREE, include new W1/W2 files not yet committed."""
    if ref != "WORKTREE":
        return
    extras = [
        "scripts/kg/kg_index.py",
        "scripts/mcp_kg_server.py",
        "scripts/test_mcp_kg_tools.py",
        "docs/workshop",
        ".vscode/settings.json.example",
    ]
    for rel in extras:
        src = repo / rel
        if not src.exists():
            continue
        dst = staging / rel
        if src.is_dir():
            if dst.exists():
                shutil.rmtree(dst)

            def _ignore(dirpath: str, names: list[str]) -> set[str]:
                ignored = set(shutil.ignore_patterns("__pycache__", "*.pyc")(dirpath, names))
                if Path(dirpath).name == "workshop" and "snapshot-overlay" in names:
                    ignored.add("snapshot-overlay")
                return ignored

            shutil.copytree(src, dst, ignore=_ignore)
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)


def validate_snapshot(staging: Path) -> None:
    print("Running make validate-all in snapshot …")
    subprocess.run(
        ["make", "validate-all"],
        cwd=staging,
        check=True,
    )


def write_snapshot_manifest(staging: Path, ref: str) -> None:
    manifest = staging / "WORKSHOP-SNAPSHOT.txt"
    manifest.write_text(
        f"source_repo=ucgis-agentloom-2026\nsource_ref={ref}\n",
        encoding="utf-8",
    )


def build_snapshot(
    *,
    ref: str,
    output: Path,
    dry_run: bool,
    validate: bool,
    use_worktree_extras: bool,
) -> None:
    effective_ref = "WORKTREE" if use_worktree_extras else ref
    files = [f for f in list_tracked_files(effective_ref, REPO_ROOT) if not should_exclude(f)]
    print(f"Ref: {effective_ref}")
    print(f"Files to copy: {len(files)}")
    if dry_run:
        for f in sorted(files)[:30]:
            print(f"  {f}")
        if len(files) > 30:
            print(f"  … and {len(files) - 30} more")
        print("Overlay: docs/workshop/snapshot-overlay/ → README.md, CONTRIBUTING, .github/")
        return

    if output.exists():
        raise SystemExit(
            f"Output already exists: {output}\n"
            "Remove it or choose a different --output path."
        )

    with tempfile.TemporaryDirectory(prefix="ws-snapshot-") as tmp:
        staging = Path(tmp) / "tree"
        staging.mkdir()
        materialize_ref(effective_ref, REPO_ROOT, staging)
        if use_worktree_extras:
            copy_untracked_workshop_extras(REPO_ROOT, staging, effective_ref)
        apply_overlay(staging)
        ensure_proposals_gitkeep(staging)
        write_snapshot_manifest(staging, effective_ref)
        if validate:
            validate_snapshot(staging)
        shutil.copytree(staging, output)
    print(f"Snapshot written to {output.resolve()}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--ref",
        default="main",
        help="Git ref to snapshot (default: main). Ignored when --include-uncommitted.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=REPO_ROOT.parent / "ucgis-agentloom-2026-workshop",
        help="Output directory (must not exist)",
    )
    parser.add_argument("--dry-run", action="store_true", help="List files only")
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Run make validate-all inside snapshot before writing output",
    )
    parser.add_argument(
        "--include-uncommitted",
        action="store_true",
        help="Use working tree (includes uncommitted W1/W2 files). For pre-merge builds.",
    )
    args = parser.parse_args()

    if args.include_uncommitted:
        dirty = _run_git(["status", "--porcelain"], REPO_ROOT)
        if dirty:
            print("Note: working tree has uncommitted changes; they will be included.", file=sys.stderr)

    build_snapshot(
        ref=args.ref,
        output=args.output,
        dry_run=args.dry_run,
        validate=args.validate,
        use_worktree_extras=args.include_uncommitted,
    )


if __name__ == "__main__":
    main()
