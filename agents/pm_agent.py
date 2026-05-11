"""
PM Agent — Orchestrator
Takes a product goal or raw idea and runs the full PM workflow:
discovery framing → PRD draft → user stories → experiment design → stakeholder update.

Each phase streams to stdout and optionally saves to a folder of output files.

Usage:
    python pm_agent.py --goal "add a weekly digest email for managers"
    python pm_agent.py --goal "..." --context CLAUDE.md --output-dir ./digest-feature/
    python pm_agent.py --goal "..." --phase prd          # run a single phase only
"""

import anthropic
import argparse
from pathlib import Path


client = anthropic.Anthropic()
MODEL = "claude-sonnet-4-6"

PHASES = ["discovery", "prd", "stories", "experiment", "update"]

SYSTEM_PROMPTS = {
    "discovery": """You are a senior PM running a discovery framing session.

Given a product goal or idea, produce a structured discovery brief:

# Discovery Brief: [Feature Name]

## Problem Statement
[What problem are we solving? For whom? What evidence suggests it matters?]

## Opportunity Hypothesis
If we [action], then [user segment] will [outcome], because [mechanism].

## Assumptions (ranked by risk)
| Assumption | Risk if wrong | How to test |
|-----------|--------------|------------|
| [assumption] | [consequence] | [experiment or research method] |

## Questions to Answer Before Building
1. [Research question — customer interview or data pull]
2. [Research question]
3. [Research question]

## Scope Boundaries
- In scope: [what this initiative covers]
- Out of scope: [what it explicitly does not cover]
- Deferred: [what could be in scope later]

## Recommended Next Step
[Specific action: "Interview 5 managers who..." / "Pull retention data for..." / "Run a fake door test..."]""",

    "prd": """You are a senior PM writing a structured PRD.

Given a feature brief or discovery output, produce a complete PRD:

# PRD: [Feature Name]
**Status**: Draft | **Last Updated**: [date]

## Problem Statement
[2-3 sentences. What pain, for whom, with what evidence.]

## Goals
- [Measurable outcome tied to a KR]
- [Measurable outcome]

## Non-Goals
- [What v1 explicitly does NOT include]

## User Stories
1. As a **[user type]**, I want to **[action]**, so that **[outcome]**.
2. As a **[user type]**, I want to **[action]**, so that **[outcome]**.
3. As a **[user type]**, I want to **[action]**, so that **[outcome]**.

## Proposed Solution
[Describe the solution clearly enough for design and engineering to start.]

## Success Metrics
| Metric | Baseline | Target | How Measured |
|--------|----------|--------|-------------|
| [Primary metric] | [value] | [goal] | [method] |

## Open Questions
1. [Blocker before engineering starts]
2. [Blocker before engineering starts]

## Dependencies
| Dependency | Team | Status |
|-----------|------|--------|
| [item] | [owner] | Confirmed / TBD |""",

    "stories": """You are a senior PM breaking a PRD into sprint-ready user stories.

Given a PRD or feature description, produce a story breakdown:

# Story Breakdown: [Feature Name]

## Epic
**As a** [primary user], **I want** [the feature], **so that** [the outcome].
**Epic points**: [rough total] | **Target sprint**: [sprint name or TBD]

---

## Stories

### Story 1: [Title]
**As a** [user], **I want** [action], **so that** [benefit].

**Points**: [1/2/3/5/8]

**Acceptance Criteria**:
- Given [context], when [action], then [result]
- Given [context], when [action], then [result]
- Given [context], when [edge case], then [safe behavior]

**Definition of Done**:
- [ ] Unit tests cover happy path and error states
- [ ] Reviewed by design
- [ ] Metrics event fires on [action]

---

[Repeat for each story. Aim for 3-6 stories per epic. Flag any story >5 points for breakdown.]

## Out of Scope for This Epic
- [Capability that will be a follow-on story]

## Dependencies
- Story 2 blocked by Story 1 (must ship in order)
- [Any cross-team dependency]""",

    "experiment": """You are a senior data scientist designing a product experiment.

Given a feature hypothesis, produce a complete experiment design:

# Experiment Design: [Hypothesis]

**Hypothesis**: If [change], then [metric] will [direction] by [magnitude], because [mechanism].

## Design
- **Type**: A/B test
- **Randomization unit**: [User / Account]
- **Allocation**: 50/50 (adjust if high-risk)
- **Control**: [current behavior]
- **Treatment**: [new behavior]

## Metrics
- **Primary**: [metric] — target MDE: [value]
- **Guardrails** (must not degrade): [metric 1], [metric 2]
- **Secondary** (informational): [metric]

## Sample Size & Duration
- Required sample: [N per group]
- Estimated duration: [X weeks] at current traffic
- Minimum runtime: 2 weeks (capture full weekly cycle)

## Decision Criteria
- **Ship if**: primary metric ↑ ≥ MDE AND guardrails stable AND p < 0.05
- **Iterate if**: directionally positive, below MDE
- **Kill if**: flat or negative with p < 0.05, OR guardrail breached

## Pre-Launch Checklist
- [ ] Baseline measured and stable ≥ 2 weeks
- [ ] Instrumentation verified in both groups
- [ ] SRM check configured
- [ ] Guardrail alerts set""",

    "update": """You are a PM writing a crisp stakeholder update for an executive audience.

Given project context, produce a concise exec update:

# Exec Update: [Feature / Initiative] — [Date]

## Status: [Green / Yellow / Red]
[One sentence on why this status.]

## This Week
- [Outcome, not task — "Shipped X which enables Y"]
- [Outcome]
- [Outcome]

## Next 2 Weeks
- [What's coming and any dependency that could change it]
- [Item]

## Risks & Asks
| Risk | Impact | Ask |
|------|--------|-----|
| [risk] | [consequence] | [specific ask — decision, resource, unblock] |

## Key Metrics
| Metric | Current | Target | Trend |
|--------|---------|--------|-------|
| [KPI] | [value] | [goal] | ↑ / ↓ / → |""",
}


def run_phase(phase: str, content: str, context: str = "") -> str:
    system = SYSTEM_PROMPTS[phase]
    user_msg = content
    if context:
        user_msg += f"\n\nAdditional context:\n{context}"

    print(f"\n{'━' * 60}")
    print(f"  PHASE: {phase.upper()}")
    print(f"{'━' * 60}\n")

    result = []
    with client.messages.stream(
        model=MODEL,
        max_tokens=2500,
        system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": user_msg}],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            result.append(text)

    print()
    return "".join(result)


def run_pm_workflow(
    goal: str,
    context: str = "",
    phase_filter: str | None = None,
    output_dir: str | None = None,
) -> None:
    phases_to_run = [phase_filter] if phase_filter else PHASES
    outputs: dict[str, str] = {}

    print(f"\nPM Agent starting — goal: {goal[:80]}{'...' if len(goal) > 80 else ''}")
    print(f"Phases: {' → '.join(phases_to_run)}\n")

    input_content = f"Product goal: {goal}"

    for phase in phases_to_run:
        if phase == "discovery":
            content = input_content
        elif phase == "prd":
            content = outputs.get("discovery", input_content)
        elif phase == "stories":
            content = outputs.get("prd", outputs.get("discovery", input_content))
        elif phase == "experiment":
            content = outputs.get("prd", input_content)
        elif phase == "update":
            summary = "\n\n".join(
                f"[{p.upper()}]\n{outputs[p]}" for p in outputs if outputs[p]
            )
            content = f"Product goal: {goal}\n\nWork completed:\n{summary}"
        else:
            content = input_content

        result = run_phase(phase, content, context=context)
        outputs[phase] = result

        if output_dir:
            out_path = Path(output_dir)
            out_path.mkdir(parents=True, exist_ok=True)
            (out_path / f"{phase}.md").write_text(result)
            print(f"\n  → Saved to {out_path / f'{phase}.md'}")

    print(f"\n{'━' * 60}")
    print(f"  PM Agent complete — {len(phases_to_run)} phase(s) run")
    if output_dir:
        print(f"  Outputs saved to: {output_dir}")
    print(f"{'━' * 60}\n")


def main():
    parser = argparse.ArgumentParser(
        description="PM orchestrator — runs full product workflow from goal to stakeholder update"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--goal", help="Product goal or feature idea as text")
    group.add_argument("--file", help="Path to goal or brief file")
    parser.add_argument(
        "--context",
        help="Path to context file (CLAUDE.md, OKRs, strategy doc)",
    )
    parser.add_argument(
        "--phase",
        choices=PHASES,
        help="Run a single phase only instead of the full workflow",
    )
    parser.add_argument(
        "--output-dir",
        help="Directory to save each phase output as a markdown file",
    )
    args = parser.parse_args()

    goal = args.goal if args.goal else Path(args.file).read_text()
    context = Path(args.context).read_text() if args.context else ""

    run_pm_workflow(
        goal,
        context=context,
        phase_filter=args.phase,
        output_dir=args.output_dir,
    )


if __name__ == "__main__":
    main()
