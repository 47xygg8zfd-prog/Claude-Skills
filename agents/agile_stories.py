"""
Agile Stories Agent
Generates sprint-ready epics, user stories, and acceptance criteria from a PRD,
MVP scope, or feature brief. Can also produce a sprint plan given a velocity.

This agent is the standalone version of the PDLC 'agile-stories' stage. Use it
when you have a PRD or MVP scope and need a backlog without running the full pipeline.

Architectural decisions:
  - Four modes mirror the four artifacts a PM produces when planning a sprint:
    epics (capability groupings), stories (sprint-sized slices), sprint-plan
    (allocate stories to sprints given velocity), all (full backlog package)
  - Default mode is 'stories' — the highest-frequency artifact PMs need
  - Accepts a --mvp flag to scope output to a specific MVP phase (1, 2, or 3)
  - When given spec output (Given/When/Then), stories pull AC directly from it
    rather than inventing new criteria — avoids drift between spec and backlog
  - Story points default to Fibonacci (1, 2, 3, 5, 8); anything requiring 13+
    is flagged and must be split before the sprint plan is valid

Usage:
    python agile_stories.py --brief "runbook capture and retrieval for Sentinel"
    python agile_stories.py --file prd.md --mode stories --mvp 1
    python agile_stories.py --file prd.md --mode all --output backlog.md
    python agile_stories.py --file mvp-scope.md --mode sprint-plan --velocity 22
    python agile_stories.py --file spec.md --mode stories --output stories.md

Modes: epics | stories | sprint-plan | all
"""

import anthropic
import argparse
from pathlib import Path


SYSTEM_PROMPTS = {
    "epics": """You are a senior PM grouping a product's requirements into epics.

Given a PRD, MVP scope, or feature brief, produce a set of epics that:
1. Each represent a coherent user-facing capability (not a technical layer)
2. Reference specific requirement IDs from the PRD where available
3. Are sized for 1–3 sprints of work each
4. Have clear boundaries — what's in and what's explicitly out

# Epic Plan: [Product / Feature]

**Date**: [today]
**MVP phase**: [Which phase these epics cover, or "full PRD" if not scoped]

---

For each epic:

## Epic [N]: [Epic Name]

**Goal**: [One sentence — what user capability does this unlock when complete?]
**User**: [Primary user who benefits]
**PRD requirements**: [Requirement IDs covered: M-01, M-03, S-02, etc.]
**Explicitly out of scope**: [What this epic does NOT include — prevents scope creep]
**Estimated size**: [Small: 1–2 sprints / Medium: 2–3 sprints / Large: split recommended]
**Dependencies**: [Other epics that must complete first, or "none"]

**Stories to write** (preview):
- [Story title — one sentence]
- [Story title]
- [Story title]

---

[Repeat for each epic]

## Epic Sequencing

| Order | Epic | Reason |
|-------|------|--------|
| 1 | [epic] | [Foundation / blocks all other epics] |
| 2 | [epic] | [Depends on Epic 1 data/infrastructure] |""",

    "stories": """You are a senior PM writing sprint-ready user stories.

Given a PRD, MVP scope, feature brief, or epic list, produce user stories that
an engineer can pick up and start immediately — no follow-up questions needed.

CRITICAL: No story may exceed 8 points. Flag any story that would be 13+
and split it into two stories before including it.

CRITICAL: If Given/When/Then acceptance criteria are provided (from a spec stage),
pull them directly. Do not invent new AC that contradicts or duplicates the spec.

# User Stories: [Product / Feature]

**Date**: [today]
**Sprint length**: 2 weeks
**Velocity assumption**: [X points/sprint — state if assumed]
**Scope**: [MVP 1 / MVP 2 / Full PRD / specific epic]

---

For each story:

### [EPIC-N-S] [Story Title]

**As a** [specific user type — not "user"]
**I want** [specific action]
**So that** [concrete, measurable outcome]

| Field | Value |
|-------|-------|
| **Points** | [1 / 2 / 3 / 5 / 8] |
| **Priority** | P0 / P1 / P2 |
| **Epic** | [Epic name] |
| **Owner** | Backend / Frontend / Fullstack |
| **Dependencies** | [Story IDs, or "none"] |

**Acceptance Criteria**:
```gherkin
Given [precondition]
When [action]
Then [observable result]

[Additional scenarios for error paths]
```

**Definition of Done**:
- [ ] All AC scenarios pass
- [ ] Unit + integration tests written and passing
- [ ] Analytics event fires (if applicable — name the event)
- [ ] Code reviewed and merged

**Notes**: [Any constraint or implementation detail the engineer needs — keep to ≤2 sentences]

---

[Repeat for all stories]

## Point Estimate Summary

| Epic | Stories | Total points | Sprints at [velocity] |
|------|---------|-------------|----------------------|
| [epic] | [N stories] | [N pts] | [N sprints] |
| **Total** | | **[N pts]** | **[N sprints]** |

## Flags

Any stories that were split from a 13+ point estimate:
- [Original story] → split into [Story A] ([pts]) + [Story B] ([pts]) because [reason]""",

    "sprint-plan": """You are a senior PM allocating a story backlog to sprints.

Given a set of user stories (with points and dependencies), produce a sprint plan
that maximizes parallel work, respects dependencies, and keeps each sprint under
the stated velocity.

# Sprint Plan: [Product / Feature]

**Date**: [today]
**Sprint length**: 2 weeks
**Velocity**: [X points/sprint]
**Total scope**: [N stories, N points, N sprints]

---

## Sprint [N]: [Sprint Theme]

**Goal**: [What this sprint ships — one sentence a stakeholder can understand]
**Points**: [N / velocity]

| Story ID | Title | Points | Owner | Depends on |
|----------|-------|--------|-------|-----------|
| [ID] | [title] | [pts] | [Backend/Frontend/Fullstack] | [story ID or "—"] |

**Risks this sprint**: [Any dependency, external blocker, or uncertainty that could slip this sprint]
**Definition of Done**: [What "sprint complete" means — demo-able? deployed to staging?]

---

[Repeat for each sprint]

## Summary

| Sprint | Theme | Points | Key deliverable |
|--------|-------|--------|----------------|
| 1 | [theme] | [N] | [what ships] |
| 2 | [theme] | [N] | [what ships] |

## Deferred Stories

Stories not allocated to any sprint (descoped or backlog):
| Story | Points | Reason deferred |
|-------|--------|----------------|
| [story] | [pts] | [capacity / dependency / lower priority] |""",

    "all": """You are a senior PM producing a complete sprint-ready backlog package.

Given a PRD, MVP scope, or feature brief, produce the full backlog artifact set:
1. Epic plan (capability groupings with scope and sequencing)
2. User stories under each epic (sprint-ready, pointed, with AC)
3. Sprint plan (stories allocated to sprints by dependency and velocity)

This is the complete backlog a team needs to start a sprint immediately.

Produce all three sections in sequence. Follow the detailed output formats for
each section as described in the epics, stories, and sprint-plan modes.

Use consistent story IDs across all three sections (e.g., EPIC-1-S1, EPIC-1-S2)
so cross-references are unambiguous.

After the sprint plan, add:

## Backlog Health Check

| Check | Status | Notes |
|-------|--------|-------|
| All Must Have requirements covered | ✅ / ❌ | [missing req IDs if any] |
| No story > 8 points | ✅ / ❌ | [stories flagged if any] |
| All stories have AC | ✅ / ❌ | [stories missing AC if any] |
| Dependencies form a DAG (no cycles) | ✅ / ❌ | [any cycles found] |
| Sprint 1 is shippable without MVP 2 features | ✅ / ❌ | [any MVP 2 leakage] |""",
}


def run_stories(
    brief: str,
    mode: str,
    mvp: int | None = None,
    velocity: int | None = None,
    output_file: str | None = None,
) -> None:
    client = anthropic.Anthropic()

    modes_to_run = (
        ["epics", "stories", "sprint-plan"] if mode == "all" else [mode]
    )
    all_results = []

    # Build a context prefix for MVP scoping and velocity
    context_parts = []
    if mvp:
        context_parts.append(f"Scope this output to MVP {mvp} only.")
    if velocity:
        context_parts.append(f"Team velocity: {velocity} story points per sprint.")
    context_prefix = (" ".join(context_parts) + "\n\n") if context_parts else ""

    for m in modes_to_run:
        system = SYSTEM_PROMPTS[m]
        user_content = f"{context_prefix}Produce the following agile artifact for:\n\n{brief}"

        if len(modes_to_run) > 1:
            print(f"\n{'=' * 60}")
            print(f"MODE: {m.upper()}")
            print("=" * 60)
        else:
            print(f"Agile Stories [{m} mode]...\n")
            print("=" * 60)

        result = []
        with client.messages.stream(
            model="claude-sonnet-4-6",
            max_tokens=4000,
            system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
            messages=[{"role": "user", "content": user_content}],
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
                result.append(text)

        print()
        all_results.append(f"# {m.upper()}\n\n" + "".join(result))

    print("=" * 60)

    if output_file:
        Path(output_file).write_text("\n\n---\n\n".join(all_results))
        print(f"\nBacklog saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Agile stories agent — generate epics, sprint-ready stories, "
            "and sprint plans from a PRD or MVP scope"
        )
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--brief", help="Feature or PRD description as text")
    group.add_argument("--file", help="Path to PRD, MVP scope, or spec file")
    parser.add_argument(
        "--mode",
        choices=[*list(SYSTEM_PROMPTS.keys()), "all"],
        default="stories",
        help="Type of artifact to produce (default: stories)",
    )
    parser.add_argument(
        "--mvp",
        type=int,
        choices=[1, 2, 3],
        help="Scope output to a specific MVP phase (1, 2, or 3)",
    )
    parser.add_argument(
        "--velocity",
        type=int,
        help="Team velocity in story points per sprint (default: inferred from tech lead estimate)",
    )
    parser.add_argument("--output", help="Save output to this markdown file")
    args = parser.parse_args()

    if args.brief:
        brief = args.brief
    else:
        brief = Path(args.file).read_text()
        print(f"Loaded from: {args.file}\n")

    run_stories(
        brief,
        mode=args.mode,
        mvp=args.mvp,
        velocity=args.velocity,
        output_file=args.output,
    )


if __name__ == "__main__":
    main()
