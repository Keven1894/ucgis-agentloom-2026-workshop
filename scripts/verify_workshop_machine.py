#!/usr/bin/env python3
"""Pre-workshop machine check (lab + attendee self-service).

Usage (from repo root, after .venv optional):
  python scripts/verify_workshop_machine.py
  .venv/Scripts/python scripts/verify_workshop_machine.py
"""

from __future__ import annotations

import shutil
import socket
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MIN_PYTHON = (3, 11)


def ok(msg: str) -> None:
    print(f"[OK]  {msg}")


def fail(msg: str) -> None:
    print(f"[FAIL] {msg}")


def check_python() -> bool:
    if sys.version_info >= MIN_PYTHON:
        ok(f"Python {sys.version_info.major}.{sys.version_info.minor}")
        return True
    fail(f"Python >= {MIN_PYTHON[0]}.{MIN_PYTHON[1]} required (have {sys.version_info.major}.{sys.version_info.minor})")
    return False


def check_git() -> bool:
    if shutil.which("git"):
        ok("git on PATH")
        return True
    fail("git not found")
    return False


def check_requirements() -> bool:
    req = REPO / "requirements.txt"
    if not req.is_file():
        fail("requirements.txt missing")
        return False
    ok("requirements.txt present")
    return True


def check_port(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind(("127.0.0.1", port))
        except OSError:
            fail(f"port {port} already in use (dashboard needs 8000 free)")
            return False
    ok(f"port {port} available")
    return True


def check_venv_hint() -> bool:
    venv_py = REPO / ".venv" / ("Scripts" if sys.platform == "win32" else "bin") / "python"
    if venv_py.is_file():
        ok(f".venv found ({venv_py})")
        return True
    fail(".venv not found — run: python -m venv .venv && pip install -r requirements.txt")
    return False


def check_test_mcp() -> bool:
    script = REPO / "scripts" / "test_mcp_kg_tools.py"
    if not script.is_file():
        fail("scripts/test_mcp_kg_tools.py missing")
        return False
    py = sys.executable
    r = subprocess.run([py, str(script)], cwd=REPO, capture_output=True, text=True)
    if r.returncode == 0:
        ok("test_mcp_kg_tools.py PASS")
        return True
    fail("test_mcp_kg_tools.py FAIL")
    if r.stdout:
        print(r.stdout[-800:])
    if r.stderr:
        print(r.stderr[-400:], file=sys.stderr)
    return False


def main() -> int:
    print("UCGIS workshop machine verify\n")
    checks = [
        check_python(),
        check_git(),
        check_requirements(),
        check_port(8000),
        check_venv_hint(),
    ]
    if all(checks[:4]) and (REPO / ".venv").is_dir():
        checks.append(check_test_mcp())
    print()
    if all(checks):
        print("[OK] machine ready for workshop dry-run")
        return 0
    print("[FAIL] fix items above before hands-on blocks")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
