.PHONY: help check check-offline vendor kg-validate kg-validate-schemas kg-validate-integrity validate-behaviors validate-all kg-bootstrap dashboard mcp test-mcp install smoke clean

help:
	@echo "Targets:"
	@echo "  install            - pip install -r requirements.txt"
	@echo "  check              - sanity-check all 4 data sources (live; OPENAQ_API_KEY needed for D2)"
	@echo "  check-offline      - same, against vendored snapshots only"
	@echo "  vendor             - re-download vendored snapshots into data/snapshots/"
	@echo "  kg-validate        - run BOTH KG validators (schemas + relational integrity)"
	@echo "  kg-validate-schemas    - JSON-schema validation for all 6 KG files"
	@echo "  kg-validate-integrity  - relational integrity for the 2 knowledge graphs (parent/child, orphans, cycles)"
	@echo "  validate-behaviors - run every Tier-A behavior validator under scripts/validators/"
	@echo "  validate-all       - kg-validate + validate-behaviors (full governance gate)"
	@echo "  kg-bootstrap       - (re-)populate the 3 builder KGs with the 15 meta-nodes (idempotent upsert)"
	@echo "  dashboard          - launch read-only KG dashboard at http://127.0.0.1:8000 (Cytoscape + proposals + timeline)"
	@echo "  mcp                - print MCP server launch command (stdio; Cline spawns this)"
	@echo "  test-mcp           - smoke test kg_index tools without Cline"
	@echo "  smoke              - (Phase 3) full local stack: ingest snapshots -> server -> webapp"
	@echo ""
	@echo "Source-specific targets (d1-pipeline, d1-viewer, etc.) live on the dN branches."
	@echo "This branch (main) is framework-only. See 'git branch -a' for source branches."

install:
	pip install -r requirements.txt

check:
	python scripts/sanity_check_sources.py

check-offline:
	python scripts/sanity_check_sources.py --vendored

vendor:
	python scripts/vendor_snapshots.py

kg-validate:
	python scripts/kg/validate_all.py

kg-validate-schemas:
	python scripts/kg/validate_schemas.py

kg-validate-integrity:
	python scripts/kg/validate_kg_integrity.py --all

validate-behaviors:
	python scripts/validators/run_all.py

validate-all: kg-validate validate-behaviors

kg-bootstrap:
	python scripts/kg/bootstrap_builder_kg.py

dashboard:
	python -m uvicorn server.dashboard.app:app --reload --port 8000 --host 127.0.0.1

mcp:
	@echo "stdio MCP server (Cline spawns this process):"
	@echo "  python scripts/mcp_kg_server.py"
	@echo "Configure via docs/workshop/cline-mcp-settings.example.json"

test-mcp:
	python scripts/test_mcp_kg_tools.py

smoke:
	@echo "Not yet implemented — Phase 3 deliverable (target date May 29, 2026)"
	@exit 1

clean:
	rm -rf __pycache__ */__pycache__ .pytest_cache
