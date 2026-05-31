"""skill:builder:audit-catalog-ui — developer-facing audit tool.

Walks starter/<app>/index.html (or one file via --file) and runs both:
  1. The 8-section visible storytelling check
  2. The Schema.org Dataset JSON-LD check

Prints grouped, human-readable output. Defers the actual checking to the
two CI validators by importing them; if anything diverges, the validators
remain the source of truth (this skill is a humans-friendly view).

Exit codes:
  0 — all checks passed
  1 — at least one required check failed
  2 — internal error (file unreadable, etc.)
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[2]
VALIDATORS_DIR = WORKSPACE / "scripts" / "validators"


def _load(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {file_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sections_validator = _load(
    "_v_sections", VALIDATORS_DIR / "catalog_ui_must_tell_the_story.py"
)
jsonld_validator = _load(
    "_v_jsonld", VALIDATORS_DIR / "catalog_must_embed_dataset_jsonld.py"
)

REQUIRED_ROLES = sections_validator.REQUIRED_ROLES
REQUIRED_JSONLD_FIELDS = jsonld_validator.REQUIRED_FIELDS

RECOMMENDED_JSONLD_FIELDS = [
    "temporalCoverage",
    "spatialCoverage",
    "keywords",
    "version",
    "identifier",
]


GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
DIM = "\033[2m"
RESET = "\033[0m"


def _color(s: str, c: str, use_color: bool) -> str:
    return f"{c}{s}{RESET}" if use_color else s


def audit_one(path: Path, strict: bool, use_color: bool) -> int:
    rel = path.relative_to(WORKSPACE).as_posix()
    print(f"\n=== {rel} ===\n")
    if not path.exists():
        print(_color(f"[ERROR] file does not exist", RED, use_color))
        return 2

    text = path.read_text(encoding="utf-8")
    n_fail = 0

    print("Visible sections (8 required):")
    if sections_validator.EXEMPT_MARKER in text:
        print(_color("  [EXEMPT] catalog-storytelling: bootstrapping marker present", YELLOW, use_color))
    else:
        section_violations = sections_validator.check_file(path)
        present = set(REQUIRED_ROLES) - {
            v.split(": ", 1)[1] for v in section_violations
            if v.startswith("missing data-catalog-role: ")
        }
        for role in REQUIRED_ROLES:
            if role in present and not any(role in v and "too short" in v for v in section_violations):
                print(f"  {_color('✓', GREEN, use_color)} {role}")
            else:
                detail = next(
                    (v for v in section_violations if role in v),
                    "section missing.",
                )
                print(f"  {_color('✗', RED, use_color)} {role:<13} — {detail}")
                n_fail += 1
        for v in section_violations:
            if "unknown data-catalog-role" in v:
                print(_color(f"  ! {v}", YELLOW, use_color))

    print("\nSchema.org Dataset JSON-LD:")
    if jsonld_validator.EXEMPT_MARKER in text:
        print(_color("  [EXEMPT] jsonld-discovery: bootstrapping marker present", YELLOW, use_color))
    else:
        jsonld_violations = jsonld_validator.check_file(path)
        if not jsonld_violations:
            print(f"  {_color('✓', GREEN, use_color)} valid Dataset JSON-LD with all required fields")
            if strict:
                blocks = jsonld_validator.JSONLD_PATTERN.findall(text)
                import json as _json
                for raw in blocks:
                    try:
                        parsed = _json.loads(raw)
                    except _json.JSONDecodeError:
                        continue
                    ds = jsonld_validator._find_dataset(parsed)
                    if ds:
                        for f in RECOMMENDED_JSONLD_FIELDS:
                            if f not in ds or not ds[f]:
                                print(_color(f"  ~ recommended field missing: {f}", YELLOW, use_color))
                        break
        else:
            for v in jsonld_violations:
                print(f"  {_color('✗', RED, use_color)} {v}")
                n_fail += 1
            print(_color(
                f"\n    Required fields: {', '.join(REQUIRED_JSONLD_FIELDS)}",
                DIM, use_color,
            ))

    print()
    if n_fail == 0:
        print(_color(f"PASS — catalog tells the full story.", GREEN, use_color))
    else:
        print(_color(f"FAIL — {n_fail} violation(s). See:", RED, use_color))
        print("  - knowledge:builder:data-catalog-ui-storytelling")
        print("  - knowledge:builder:dataset-jsonld-discovery")
    return 0 if n_fail == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    ap.add_argument("--file", type=str, help="single index.html to audit")
    ap.add_argument("--strict", action="store_true",
                    help="also flag recommended-but-not-required JSON-LD fields")
    ap.add_argument("--no-color", action="store_true")
    args = ap.parse_args()
    use_color = not args.no_color and sys.stdout.isatty()

    if args.file:
        return audit_one(Path(args.file).resolve(), args.strict, use_color)

    starter_dir = WORKSPACE / "starter"
    if not starter_dir.exists():
        print(f"[INFO] {starter_dir} not found")
        return 0
    targets = sorted(starter_dir.glob("*/index.html"))
    if not targets:
        print("[INFO] no starter/<app>/index.html files found")
        return 0
    overall = 0
    for f in targets:
        rc = audit_one(f, args.strict, use_color)
        overall = max(overall, rc)
    return overall


if __name__ == "__main__":
    sys.exit(main())
