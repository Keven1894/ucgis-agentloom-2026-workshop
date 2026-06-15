# 02 — Quickstart (5-minute propose-review cycle)

**Time**: ~5–10 minutes · **After**: [`01-setup.md`](./01-setup.md)  
**Before main workshop task**: pick a real source in [`03-data-source-menu.md`](./03-data-source-menu.md)

This walkthrough uses a **toy dataset** (`data/workshop/quickstart-places.geojson`) — **not** D1–D4 — so your real catalog work still starts from zero.

---

## Goal

One full loop:

1. **Discover** — inspect sample data + search KG via MCP  
2. **Propose** — Cline files a domain knowledge node  
3. **Review** — you read the proposal on the dashboard  
4. **Accept** — you promote it into the live KG  
5. **Verify** — validators still green

---

## The sample data

```bash
# Windows
.venv\Scripts\python -c "import json; d=json.load(open('data/workshop/quickstart-places.geojson')); print(len(d['features']), 'features'); print(d['features'][0]['properties'])"

# macOS/Linux
.venv/bin/python -c "import json; d=json.load(open('data/workshop/quickstart-places.geojson')); print(len(d['features']), 'features'); print(d['features'][0]['properties'])"
```

You should see **3 point features** with `observed_at` as **ISO 8601 strings with timezone** (unlike D1's epoch milliseconds).

Read [`data/workshop/README.md`](../../data/workshop/README.md) for context.

---

## Step 1 — Cline discovers (MCP + file)

New Cline task. Paste:

```
Workshop quickstart task (NOT D1-D4).

1. Read the first 500 bytes of data/workshop/quickstart-places.geojson (shell or read_file).
2. Use MCP kg_search for "timestamp" or "iso 8601" with role=domain (or builder).
3. Use kg_list_proposals to see if any proposals already exist.
4. Summarize: what timestamp format does quickstart-places use, and what did the KG already know?

Do NOT read agents/knowledge-graphs/*-graph.json directly.
Stop after the summary — do not propose yet.
```

**Pass**: Cline used MCP tools; noted ISO 8601 in sample; did not open raw graph JSON.

---

## Step 2 — Cline proposes (CLI only)

Same or new task. Paste:

```
Propose ONE domain knowledge node capturing that workshop quickstart-places.geojson
uses properties.observed_at as ISO 8601 with timezone offset (not epoch ms).

Use scripts/kg/propose_node.py with:
  --type knowledge
  --target-role domain
  --slug quickstart-places-observed-at-iso8601
  --title "Quickstart places use ISO 8601 observed_at"
  --justification "Three-feature teaching sample; timestamps are ISO 8601 strings with offset for contrast with D1 epoch ms."
  --source-context "data/workshop/quickstart-places.geojson properties.observed_at"
  --path docs/domain/proposed/quickstart-places-observed-at-iso8601.md

Use .venv python. Do NOT run accept_proposal.py. Stop after propose succeeds.
```

**Pass**: new JSON under `agents/knowledge-graphs/proposals/`; Cline stopped without accepting.

Note the proposal filename (timestamp prefix), e.g. `20260531-153045-quickstart-places-observed-at-iso8601.json`.

---

## Step 3 — Human review (dashboard)

1. Open **http://127.0.0.1:8000** → **Proposals** tab  
2. Find your proposal; read title, justification, source context  
3. Decide: acceptable for a teaching sample?

---

## Step 4 — Human accept (CLI)

Replace `<proposal-file>` with the actual filename:

```bash
# Windows
.venv\Scripts\python scripts\kg\accept_proposal.py --proposal <proposal-file>.json

# macOS/Linux
.venv/bin/python scripts/kg/accept_proposal.py --proposal <proposal-file>.json

# Dry-run first (optional)
.venv\Scripts\python scripts\kg\accept_proposal.py --proposal <proposal-file>.json --dry-run   # Windows
.venv/bin/python scripts/kg/accept_proposal.py --proposal <proposal-file>.json --dry-run        # macOS/Linux
```

**Pass**: validators run during accept; proposal JSON removed; node appears in domain knowledge graph.

---

## Step 5 — Implement doc stub (you + Cline, ~2 min)

Create the markdown path referenced in the proposal:

```bash
# Ask Cline:
```

```
Create docs/domain/proposed/quickstart-places-observed-at-iso8601.md documenting:
- source file data/workshop/quickstart-places.geojson
- field properties.observed_at is ISO 8601 with timezone
- contrast with D1 USGS epoch milliseconds (mention only; do not build D1)

Keep it under 30 lines. Do not edit *-graph.json by hand.
```

---

## Step 6 — Verify governance floor

```bash
# Windows
.venv\Scripts\python scripts\kg\validate_all.py
.venv\Scripts\python scripts\validators\run_all.py

# macOS/Linux
.venv/bin/python scripts/kg/validate_all.py
.venv/bin/python scripts/validators/run_all.py
```

**Pass**: same 8/8 PASS as setup. You do **not** need a catalog app for this quickstart.

---

## Quickstart checklist

| # | Step | Pass? |
| --- | --- | --- |
| 1 | Inspected quickstart-places.geojson | ☐ |
| 2 | Cline used MCP search + list proposals | ☐ |
| 3 | Cline ran propose_node.py (no accept) | ☐ |
| 4 | Reviewed on dashboard Proposals tab | ☐ |
| 5 | You ran accept_proposal.py | ☐ |
| 6 | Doc stub created at proposed path | ☐ |
| 7 | Validators still PASS | ☐ |

---

## What you learned

| Role | Action |
| --- | --- |
| **Cline** | MCP read + `propose_node.py` |
| **You** | Dashboard review + `accept_proposal.py` |
| **Validators** | Gate every commit / PR |

Ready for the real build → [**03-data-source-menu.md**](./03-data-source-menu.md) → workshop Block 3 catalog.

---

## Optional: lecturer demo path

Organizer can project the same steps in ~5 min during Block 2 before attendees pick D1–D4.
