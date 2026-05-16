# Agile Team — BMAD-Style Planning Orchestrator

A virtual agile team of six specialist AI agents that takes a rough idea from brief
through a shippable project bible — ready to hand off to developers or AI coding agents.

Inspired by [BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD). Built on
the Anthropic SDK. Every role is a first-class artifact you can use standalone or
chain with the orchestrator.

---

## The Two-Phase Model

```
PHASE 1 — PLANNING (this repo)
    Rough idea
        └── Analyst        → Project Brief (problem, personas, constraints)
                └── PM             → PRD (requirements, epics, success metrics)
                        └── Architect      → Architecture doc (stack, ADRs, data model)
                                └── Scrum Master   → Epics + sprint plan
                                        └── Developer      → Sprint-ready stories with AC
                                                └── QA             → Test plan

PHASE 2 — IMPLEMENTATION (hand off to devs or AI coding agents)
    Project Bible (all Phase 1 outputs)
        └── AI coding agent (Claude Code, Cursor, Copilot)
                └── Running software
```

Phase 1 is the full focus of this repo. Phase 2 is intentionally out of scope —
the project bible is the handoff artifact.

---

## The Constitution

Every project starts with a **constitution** — a set of immutable principles that
every agent reads before producing output. It prevents scope creep, resolves
ambiguity without re-asking the user, and keeps all six agents aligned.

See [`constitution-template.md`](./constitution-template.md).

---

## Roles

| Role | Produces | Reads |
|------|---------|-------|
| [Analyst](./roles/analyst.md) | Project Brief | Rough idea + constitution |
| [Product Manager](./roles/product-manager.md) | PRD | Brief + constitution |
| [Architect](./roles/architect.md) | Architecture doc | PRD + constitution |
| [Scrum Master](./roles/scrum-master.md) | Epics + sprint plan | PRD + architecture + constitution |
| [Developer](./roles/developer.md) | Sprint-ready stories with AC | Epics + architecture + constitution |
| [QA Engineer](./roles/qa.md) | Test plan | Stories + PRD + constitution |

Each role card is a standalone prompt — paste it into Claude, Cursor, or any LLM
to activate that role without running the full orchestrator.

---

## Usage

```bash
pip install anthropic
export ANTHROPIC_API_KEY=your-key-here

# Full planning run — brief through test plan
python ../agents/agile_team.py --idea "build a weekly digest email for engineering managers"

# Save all outputs to a project-bible directory
python ../agents/agile_team.py --idea "..." --output-dir ./project-bible/

# Run a single role (e.g., just the architect)
python ../agents/agile_team.py --file ./project-bible/02_prd.md --role architect

# Start from a specific role (uses prior outputs from --output-dir)
python ../agents/agile_team.py --idea "..." --output-dir ./project-bible/ --from-role architect

# List all roles
python ../agents/agile_team.py --list-roles
```

---

## Output: The Project Bible

After a full run, `--output-dir` contains:

```
project-bible/
├── 00_constitution.md     # Immutable project principles
├── 01_brief.md            # Analyst: problem, personas, constraints, unknowns
├── 02_prd.md              # PM: requirements, epics, success metrics
├── 03_architecture.md     # Architect: stack, ADRs, data model, API contracts
├── 04_epics.md            # Scrum Master: epics, sprint plan, velocity estimate
├── 05_stories.md          # Developer: sprint-ready stories with Given/When/Then AC
└── 06_test_plan.md        # QA: test cases, coverage map, risk matrix
```

Hand this directory to Claude Code, Cursor, or a dev team. Every decision is
documented. Every handoff has context. No Slack DMs needed to understand why.

---

## Design Principles

1. **Constitution first** — every agent reads it before producing output; scope is settled before anyone writes code
2. **Role cards are first-class** — each role works standalone or in the chain
3. **Planning only** — no quality gates, no retries, no 24 stages; the goal is a complete project bible, fast
4. **Explicit handoff format** — output is designed to be consumed by AI coding agents, not just humans
5. **Single-file agents** — no framework dependencies beyond the Anthropic SDK
