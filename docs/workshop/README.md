# Workshop documentation (UCGIS 2026)

**Workshop date**: 2026-06-15 (half-day)  
**Attendee repo**: [ucgis-agentloom-2026-workshop](https://github.com/Keven1894/ucgis-agentloom-2026-workshop)

## Read order (attendees)

| # | Doc | Purpose |
| --- | --- | --- |
| 1 | [`01-setup.md`](./01-setup.md) | `.venv`, Cline, MCP, dashboard, validators |
| 2 | [`02-quickstart.md`](./02-quickstart.md) | 5-min propose-review cycle (toy sample) |
| 3 | [`03-data-source-menu.md`](./03-data-source-menu.md) | Pick D1–D4 for your catalog |
| 4 | [`04-attendee-prompt-pack.md`](./04-attendee-prompt-pack.md) | **Track B** Cline prompts (workshop day) |
| — | [`06-slides.html`](./06-slides.html) | **Projector slides** (browser, ← → navigate) |
| — | [`A5-cheat-sheet.html`](./A5-cheat-sheet.html) | **Print cheat sheet** (browser → Print) |
| — | [`00-workshop-workflow.md`](./00-workshop-workflow.md) | Full A→G checklist (operators) |
| — | [`welcome.html`](./welcome.html) | Browser cheat sheet |

## Operators (not in public snapshot)

| Doc | Purpose |
| --- | --- |
| [`git-repos-deployment.md`](./git-repos-deployment.md) | Clone, snapshot, push, tags |
| [`06-slides-outline-draft.md`](./06-slides-outline-draft.md) | W6 slides draft for review |
| [`06-slides.html`](./06-slides.html) | W6 projector slides (HTML) |
| [`A5-cheat-sheet.html`](./A5-cheat-sheet.html) | Print cheat sheet |
| [`lab-rehearsal-2026-06-02-runbook.md`](./lab-rehearsal-2026-06-02-runbook.md) | Lab dry-run facilitator script (operator) |
| [`W7-dress-rehearsal-runbook.md`](./W7-dress-rehearsal-runbook.md) | Track C operator rehearsal |
| [`dress-rehearsal-2026-05-31.md`](./dress-rehearsal-2026-05-31.md) | W7 friction log |

## Reference

| Doc | Purpose |
| --- | --- |
| [`kg-access-and-human-review.md`](./kg-access-and-human-review.md) | Two surfaces, who builds what |
| [`cline-wrapper.md`](./cline-wrapper.md) | Cline + `.clinerules` |
| [`cline-mcp-tools.md`](./cline-mcp-tools.md) | MCP config |
| [`cline-mcp-settings.example.json`](./cline-mcp-settings.example.json) | MCP template |

## TL;DR

- **Cline** reads KG via MCP, proposes via `propose_node.py`
- **You** review on dashboard `:8000`, accept via `accept_proposal.py`
- **Validators** must PASS on every commit / PR
