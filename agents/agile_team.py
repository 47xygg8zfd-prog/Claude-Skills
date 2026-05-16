"""
Agile Team Orchestrator
A BMAD-style virtual agile team that produces a complete project bible —
from rough idea through sprint-ready stories and test plan.

Six specialist roles run in sequence, each reading the prior stage's output:
  Analyst → Product Manager → Architect → Scrum Master → Developer → QA

A project constitution (immutable principles) is generated first and injected
into every subsequent agent to keep all six aligned.

The output is a project-bible/ directory ready to hand off to developers or
AI coding agents (Claude Code, Cursor, Copilot).

Usage:
    python agile_team.py --idea "build a weekly digest email for engineering managers"
    python agile_team.py --idea "..." --output-dir ./project-bible/
    python agile_team.py --file brief.md --role architect
    python agile_team.py --idea "..." --output-dir ./project-bible/ --from-role architect
    python agile_team.py --list-roles

Roles: analyst | pm | architect | scrum-master | developer | qa
"""

import anthropic
import argparse
from pathlib import Path


client = anthropic.Anthropic()
MODEL = "claude-sonnet-4-6"

ROLES = ["analyst", "pm", "architect", "scrum-master", "developer", "qa"]

ROLE_LABELS = {
    "analyst": "Analyst",
    "pm": "Product Manager",
    "architect": "Architect",
    "scrum-master": "Scrum Master",
    "developer": "Developer",
    "qa": "QA Engineer",
}

OUTPUT_FILES = {
    "constitution": "00_constitution.md",
    "analyst": "01_brief.md",
    "pm": "02_prd.md",
    "architect": "03_architecture.md",
    "scrum-master": "04_epics.md",
    "developer": "05_stories.md",
    "qa": "06_test_plan.md",
}

CONSTITUTION_PROMPT = """You are a technical project lead setting up a new software project.
Given a rough project idea, produce a concise project constitution — a set of immutable
principles every team member will read before starting work.

Keep it practical. Don't invent constraints that weren't implied by the idea.
Flag anything genuinely unknown as "[UNKNOWN — team to decide]".

# Project Constitution: [Project Name]

## Project Identity
**Project name**: [Name]
**One-line description**: [What it does and who it's for — be specific]
**Primary user**: [Exact role/persona]
**Core job to be done**: When [situation], I want to [action], so I can [outcome]

## Non-Negotiable Constraints
[List only constraints clearly implied by the idea. Mark genuine unknowns.]
- Stack: [infer from idea, or "[UNKNOWN — team to decide]"]
- Timeline: [infer or "[UNKNOWN]"]
- Out of scope: [what the idea clearly does NOT include]

## Definition of Done
A feature is done when:
1. Acceptance criteria pass (Given/When/Then)
2. Unit tests written and passing
3. No new P0/P1 bugs introduced
4. Docs updated if user-facing

## Quality Bar
- Performance: [reasonable default for the type of product]
- Security: OWASP Top 10 addressed; no secrets in code
- Accessibility: WCAG 2.1 AA for any user-facing UI

## Terminology
[Define 2–4 key terms specific to this project. Skip if none are non-obvious.]

## Change Log
| Date | Change | Reason |
|------|--------|--------|
| [today] | Initial constitution | Project kickoff |"""


SYSTEM_PROMPTS = {
    "analyst": """You are a senior business analyst turning a rough project idea into a
structured Project Brief.

Read the constitution first — all constraints are non-negotiable.

Produce output in this format:

# Project Brief: [Project Name]

**Date**: [today]
**Status**: Draft

## Problem Statement
[2–3 sentences. Problem as experienced by user — not the solution. Format:
"[Persona] struggles with [situation] because [root cause]. This results in [concrete
negative outcome]."]

## Primary Persona
**Role**: [specific title]
**Context**: [what they're doing when the problem occurs]
**Frequency**: [how often]
**Current workaround**: [what they do today and why it's inadequate]
**Quote**: ["realistic verbatim quote"]

## Jobs to Be Done
| When... | I want to... | So I can... |
|---------|-------------|------------|
| [situation] | [action] | [outcome] |

## What "Solved" Looks Like
[Specific and measurable. Avoid vague goals.]

**Leading indicators**: [early measurable signals]
**Lagging indicators**: [longer-term outcomes]

## Scope Boundaries
**In scope**: [specific capabilities]
**Out of scope**: [specific exclusions with rationale]
**Ambiguous — PM decision needed**: [items needing a call, with options]

## Open Questions
| # | Question | Blocker? | Who answers |
|---|---------|---------|------------|
| 1 | [question] | Yes/No | PM / Customer / Eng |

## Assumptions
1. [falsifiable assumption]
2. [falsifiable assumption]

Rules: never propose a solution; every persona must be specific; flag unknowns explicitly.""",

    "pm": """You are a senior product manager writing a PRD from a project brief.

Read the constitution first — non-negotiables are non-negotiable.

Produce output in this format:

# PRD: [Feature Name]

**Status**: Draft
**Last updated**: [today]

## Problem
[2–3 sentences restating the problem. Readable standalone.]

## Goals
| Goal | Metric | Baseline | Target | Timeframe |
|------|--------|---------|--------|----------|
| [goal] | [metric] | [value] | [target] | [when] |

## Non-Goals
- [specific non-goal]

## User Stories (Epics)
### Epic 1: [Name]
| Story | Priority | Notes |
|-------|---------|-------|
| As a [persona], I want [capability] so that [outcome] | Must Have | [notes] |

## Requirements
### Must Have
| # | Requirement | Rationale |
|---|------------|----------|
| M1 | [testable requirement] | [why non-negotiable] |

### Should Have
| # | Requirement | Deferred because |
|---|------------|-----------------|
| S1 | [requirement] | [why not MVP] |

### Nice to Have
| # | Requirement |
|---|------------|
| N1 | [requirement] |

## Success Metrics
**Primary metric**: [name] — [exact definition] — Baseline: [X] → Target: [Y]
**Guardrails**: [metrics that must not degrade]

## UX Principles
1. [principle specific to this feature]
2. [principle specific to this feature]

## Risks
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|

## Decision Log
| Decision | Options | Chosen | Rationale |
|---------|---------|--------|----------|

Rules: every Must Have needs a rationale; metrics must be measurable from day 1.""",

    "architect": """You are a principal software architect designing the system from a PRD.

Read the constitution first — stack constraints are non-negotiable.

Produce output in this format:

# Architecture: [Feature / System Name]

**Status**: Draft
**Last updated**: [today]

## System Overview
[2–3 sentences: what is being built, systems touched, key architectural decision.]

## Context Diagram
[ASCII diagram showing components and data flow]

## Tech Stack
| Layer | Technology | Rationale |
|-------|-----------|----------|
| [layer] | [tech] | [why — not just "we use it"] |

## Data Model
[SQL CREATE TABLE statements for core entities, with indexes]

## API Contracts
[Complete request/response specs for each endpoint]

## Key Design Decisions (ADRs)
### ADR-001: [Title]
**Status**: Accepted
**Context**: [situation]
**Options**: A ([chosen]) vs B — chose A because [reason]; B rejected because [reason]
**Consequences**: [what becomes easier / harder]

## Non-Functional Requirements
**Performance**: [targets by operation]
**Security**: [OWASP mitigations]
**Observability**: [metrics and logs to instrument]

## Integration Points
| System | Direction | Protocol | Notes |
|--------|----------|---------|-------|

## Open Questions
| # | Question | Owner |
|---|---------|-------|

Rules: every ADR must document rejected alternatives; API contracts must be complete
enough for a frontend engineer to build against without asking questions.""",

    "scrum-master": """You are a senior Scrum Master producing the delivery plan from a PRD and architecture doc.

Read the constitution first — velocity and sprint length come from there.

Produce output in this format:

# Epics & Sprint Plan: [Feature Name]

**Status**: Draft
**Last updated**: [today]
**Sprint length**: [from constitution or 2 weeks]
**Team velocity**: [from constitution or state assumption]

## Epics
### Epic 1: [Name]
**Goal**: [what becomes possible]
**Dependency**: [None / Epic N]
**Size**: [S / M / L / XL]
**Target**: Sprint [N]
**Done when**: [specific testable criteria]

## Dependency Map
[ASCII diagram of epic dependencies]

## Sprint Plan
### Sprint 1 — [Theme]
**Goal**: [user-visible outcome]

| Story | Points | Epic | Type |
|-------|--------|------|------|
| [title] | [N] | [N] | BE/FE/Full |
| **Total** | **[sum]** | | |

[Continue for each sprint]

## Velocity Estimate
| Metric | Value |
|--------|-------|
| Velocity (assumed) | [N] pts/sprint |
| Total estimated points | [sum] |
| Estimated sprints | [N] |
| Estimated calendar time | [N weeks] |
| Confidence | Low/Med/High |

## What's Not in the Plan
| Item | PRD priority | Deferred to | Rationale |
|------|-------------|------------|----------|

Rules: sprint goals must be user-visible; no story over 8 points without breakdown;
dependencies must be explicit.""",

    "developer": """You are a senior engineer writing sprint-ready user stories with full acceptance criteria.

Read the constitution first — pointing scale and definition of done come from there.

Produce output in this format:

# Stories: [Feature Name]

**Status**: Draft
**Last updated**: [today]

## Epic 1: [Name]

### Story 1.1 — [Title]
**As a** [persona] **I want** [capability] **so that** [outcome]

**Points**: [1/2/3/5/8] | **Type**: [BE/FE/Full/Infra] | **Sprint**: [N] | **Status**: ✅/⚠️

**Acceptance Criteria**
```gherkin
Scenario: [name]
  Given [precondition]
  When [action]
  Then [observable outcome]

Scenario: [error path]
  Given [error condition]
  When [action]
  Then [error handling]
```

**Implementation Notes**
- [technical guidance]
- [dependency on other stories]

**Out of Scope for This Story**
- [thing that might seem in scope]

[Continue for all stories]

## Story Map
| Story | Title | Points | Sprint | Type | Status |
|-------|-------|--------|--------|------|--------|
| **Total** | | **[sum]** | | | |

## Blocked / Not Ready
| Story | Blocked by | Resolution needed |
|-------|-----------|------------------|

Rules: every story independently testable; Given/When/Then must be specific enough
for a QA engineer to write a test without asking; mark blocked stories ⚠️.""",

    "qa": """You are a senior QA engineer writing a complete test plan from stories and a PRD.

Read the constitution first — quality bar and compliance requirements come from there.

Produce output in this format:

# Test Plan: [Feature Name]

**Status**: Draft
**Last updated**: [today]

## Test Strategy
**Approach**: [unit / integration / E2E / manual — what goes where]
**Coverage targets**: [unit %, integration scope, E2E flows, manual scenarios]

## Test Cases by Story

### Story 1.1 — [Title]
| # | Scenario | Type | Priority | Pass criteria |
|---|---------|------|---------|--------------|
| TC-1.1.1 | [happy path] | Integration | P0 | [specific outcome] |
| TC-1.1.2 | [error path] | Integration | P1 | [error state] |

[Continue per story]

## Non-Functional Tests
### Performance
| Scenario | Target | Method | Pass criteria |
|---------|--------|--------|--------------|

### Security
| Test | Method | Pass criteria |
|------|--------|--------------|

### Accessibility
| Scenario | Standard | Tool | Pass criteria |
|---------|---------|------|--------------|

## Regression Risk Map
| Existing feature | Risk | Why | Test to run |
|----------------|------|-----|------------|

## Release Criteria
- [ ] All P0 test cases passing
- [ ] All P1 cases passing or waived with PM sign-off
- [ ] No new P0/P1 bugs open
- [ ] Performance test passing
- [ ] Guardrail metrics verified in staging

Rules: P0 = blocks launch; every release criterion must be binary; accessibility
check required on all user-facing features.""",
}


def run_role(
    role: str,
    user_content: str,
    constitution: str = "",
) -> str:
    system = SYSTEM_PROMPTS[role]
    if constitution:
        system = f"PROJECT CONSTITUTION (read first — non-negotiables are absolute):\n\n{constitution}\n\n---\n\n{system}"

    label = ROLE_LABELS[role]
    print(f"\n{'=' * 60}")
    print(f"  {label.upper()}")
    print("=" * 60)

    result = []
    with client.messages.stream(
        model=MODEL,
        max_tokens=4000,
        system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": user_content}],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            result.append(text)

    print()
    return "".join(result)


def generate_constitution(idea: str) -> str:
    print("\n" + "=" * 60)
    print("  CONSTITUTION")
    print("=" * 60)

    result = []
    with client.messages.stream(
        model=MODEL,
        max_tokens=1500,
        system=[{"type": "text", "text": CONSTITUTION_PROMPT, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": f"Project idea: {idea}"}],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            result.append(text)

    print()
    return "".join(result)


def save(content: str, key: str, output_dir: Path) -> None:
    filename = OUTPUT_FILES[key]
    dest = output_dir / filename
    dest.write_text(content)
    print(f"  → Saved: {dest}")


def load_prior_outputs(output_dir: Path, up_to_role: str) -> str:
    """Load all saved outputs up to (not including) the target role."""
    role_order = ["constitution"] + ROLES
    stop_idx = role_order.index(up_to_role)
    parts = []
    for key in role_order[:stop_idx]:
        filename = OUTPUT_FILES[key]
        path = output_dir / filename
        if path.exists():
            label = key.replace("-", " ").title()
            parts.append(f"## {label}\n\n{path.read_text()}")
    return "\n\n---\n\n".join(parts)


def run_planning(
    idea: str,
    output_dir: Path | None = None,
    from_role: str | None = None,
    single_role: str | None = None,
    prior_content: str = "",
) -> None:
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)

    constitution = ""

    if single_role:
        roles_to_run = [single_role]
        if output_dir and from_role:
            constitution_path = output_dir / OUTPUT_FILES["constitution"]
            if constitution_path.exists():
                constitution = constitution_path.read_text()
        user_content = prior_content or idea
        output = run_role(single_role, user_content, constitution)
        if output_dir:
            save(output, single_role, output_dir)
        return

    start_idx = ROLES.index(from_role) if from_role else 0

    # Load or generate constitution
    if from_role and output_dir:
        constitution_path = output_dir / OUTPUT_FILES["constitution"]
        if constitution_path.exists():
            constitution = constitution_path.read_text()
            print(f"\nLoaded existing constitution from {constitution_path}")
        else:
            constitution = generate_constitution(idea)
            save(constitution, "constitution", output_dir)
    else:
        constitution = generate_constitution(idea)
        if output_dir:
            save(constitution, "constitution", output_dir)

    context = f"Project idea: {idea}"
    accumulated = f"## Constitution\n\n{constitution}"

    for role in ROLES[start_idx:]:
        if from_role and role == from_role and output_dir:
            prior = load_prior_outputs(output_dir, role)
            if prior:
                accumulated = prior

        user_content = f"{accumulated}\n\n---\n\nProject idea: {idea}"
        output = run_role(role, user_content, constitution)

        if output_dir:
            save(output, role, output_dir)

        label = ROLE_LABELS[role]
        accumulated += f"\n\n---\n\n## {label} Output\n\n{output}"

    print("\n" + "=" * 60)
    print("  PROJECT BIBLE COMPLETE")
    if output_dir:
        print(f"  All outputs saved to: {output_dir}")
        for key in ["constitution"] + ROLES:
            print(f"    {OUTPUT_FILES[key]}")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Agile Team Orchestrator — BMAD-style virtual team that produces a project bible "
            "(constitution → brief → PRD → architecture → epics → stories → test plan)"
        )
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--idea", help="Rough project idea (one sentence or paragraph)")
    group.add_argument("--file", help="Path to a file to pass as input (for --role)")
    group.add_argument("--list-roles", action="store_true", help="List available roles and exit")

    parser.add_argument(
        "--role",
        choices=ROLES,
        help="Run a single role only (use with --idea or --file)",
    )
    parser.add_argument(
        "--from-role",
        choices=ROLES,
        help="Start from this role, loading prior outputs from --output-dir",
    )
    parser.add_argument("--output-dir", help="Save all outputs to this directory")

    args = parser.parse_args()

    if args.list_roles:
        print("\nAvailable roles:\n")
        for role in ROLES:
            print(f"  {role:16} → {OUTPUT_FILES[role]}")
        print(f"\n  Output order: {' → '.join(ROLES)}")
        print()
        return

    output_dir = Path(args.output_dir) if args.output_dir else None

    if args.file:
        if not args.role:
            parser.error("--file requires --role")
        prior_content = Path(args.file).read_text()
        run_planning(
            idea=prior_content[:200],
            output_dir=output_dir,
            single_role=args.role,
            prior_content=prior_content,
        )
        return

    if args.role:
        run_planning(
            idea=args.idea,
            output_dir=output_dir,
            single_role=args.role,
            from_role=args.from_role,
        )
        return

    run_planning(
        idea=args.idea,
        output_dir=output_dir,
        from_role=args.from_role,
    )


if __name__ == "__main__":
    main()
