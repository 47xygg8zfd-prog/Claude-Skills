"""
Roadmap Agent
Builds quarterly roadmaps, sequences features against OKRs, models capacity and scenarios.

This agent takes a feature backlog, OKRs, and team capacity and produces structured
roadmap artifacts — from a full quarter-by-quarter plan to a now/next/later view to
downstream impact modeling when plans change.

Architectural decisions:
  - Four modes cover the three main roadmap artifacts PMs produce plus a combined run:
    quarterly (the board-level plan), now-next-later (the team-level view), and
    scenario (the change-impact model).
  - Every feature in quarterly mode must trace to an OKR — untethered features don't
    belong in a committed roadmap.
  - Scenario mode is intentionally lightweight: PMs need fast answers when plans shift,
    not a full replanning exercise. It produces a comparison table, not a new roadmap.
  - Default mode is 'quarterly' — the most common deliverable for planning season.

Usage:
    python roadmap.py --brief "Q3 roadmap for Pulse: 2 engineers, 22pts/sprint, OKR is WAU 32->42%"
    python roadmap.py --file backlog.md --mode quarterly --quarters 2
    python roadmap.py --file backlog.md --mode now-next-later --output roadmap.md
    python roadmap.py --brief "delay AI digest by one quarter" --mode scenario
    python roadmap.py --file backlog.md --mode all --velocity "3 engineers, 30pts/sprint" --output full-plan.md

Modes: quarterly | now-next-later | scenario | all
"""

import anthropic
import argparse
from pathlib import Path


SYSTEM_PROMPTS = {
    "quarterly": """You are a senior product manager building a quarterly roadmap.

Given OKRs, a feature backlog, and team capacity, produce a structured quarter-by-quarter
roadmap. Every feature must trace to an OKR. Every quarter must have a unifying theme.

# Quarterly Roadmap: [Product Name]

**Period**: [Q? YYYY – Q? YYYY]
**Team capacity**: [from context or state assumption]
**OKRs driving this plan**: [list each OKR being served]

---

## Roadmap Table

| Quarter | Theme | Features | Teams | Capacity used | OKR served | Gate to advance |
|---------|-------|----------|-------|--------------|------------|-----------------|
| Q? | [one-line theme] | Feature A, Feature B | [team names] | [X pts / Y%] | [OKR ref] | [what must be true before Q?+1 starts] |

Repeat for each quarter in the plan. If a feature spans multiple quarters, list it in
the quarter where it ships (not when it starts), and note "starts in Q?-1" in the Teams column.

---

## OKR Coverage Check

For each OKR, confirm it is served by at least one feature in the roadmap:

| OKR | Features that move it | Quarters | Confidence |
|-----|----------------------|----------|-----------|
| [OKR text] | Feature A, Feature B | Q1, Q2 | High / Medium / Low |

Flag any OKR with no roadmap coverage as: ⚠️ UNSERVED — no committed feature moves this KR.

---

## Capacity Model

| Quarter | Total pts available | Committed pts | Buffer | Risk |
|---------|-------------------|--------------|--------|------|
| Q? | [capacity] | [committed] | [%] | [commentary] |

Flag any quarter below 20% buffer as: ⚠️ OVER-COMMITTED — consider deferring [feature].

---

## What We're NOT Building (and Why)

List every item that was considered but deferred. For each:

| Feature | Why deferred | Defer to | What would change this |
|---------|-------------|----------|------------------------|
| [Feature] | [honest reason: wrong quarter, low OKR fit, capacity, dependency not ready] | [Q? or Backlog] | [specific trigger to reconsider] |

Do not omit items — a roadmap without a "not building" section is a wish list, not a plan.

---

## Dependencies and Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| [External dep / team dep / technical unknown] | H/M/L | H/M/L | [specific action] |""",

    "now-next-later": """You are a senior product manager producing a Now / Next / Later roadmap view.

Given a feature backlog and current priorities, produce a three-column roadmap that gives
the team clarity on sequencing without false precision about future dates.

# Now / Next / Later Roadmap

**Now** = this sprint or quarter (committed, in-progress or starting immediately)
**Next** = following quarter (planned, dependencies identified, sizing done)
**Later** = beyond that (directional, not committed — but NOT a graveyard)

**Snapshot date**: [today]

---

## Now (This Quarter — Committed)

| Feature | Why NOW | Owner | OKR | Exit criteria |
|---------|---------|-------|-----|--------------|
| [Feature] | [specific reason this must happen this quarter — urgency, dependency, OKR timing] | [team/person] | [OKR ref] | [measurable definition of done] |

---

## Next (Following Quarter — Planned)

| Feature | Why NEXT (not now) | Dependencies | OKR | Sizing |
|---------|--------------------|-------------|-----|--------|
| [Feature] | [what makes it second, not first] | [what must be true first] | [OKR ref] | [S/M/L or pts] |

---

## Later (Future — Directional)

| Feature | Why LATER | Advancement criteria | OKR alignment |
|---------|-----------|---------------------|--------------|
| [Feature] | [honest reason: not yet validated / depends on Now features / low priority vs alternatives] | [SPECIFIC criteria that would move this to Next — not vague "when we have capacity"] | [OKR ref or "Exploratory"] |

Later is not a graveyard. Every item must have explicit, measurable criteria for
advancement to Next. If no criteria can be stated, the feature should be dropped entirely.

---

## Sequencing Rationale

[2-3 paragraphs explaining the logic of this sequencing: what bets are being made, what
dependencies drive the order, and what would force a resequence.]

---

## What Falls Off the List

| Feature | Why removed | If conditions change |
|---------|------------|---------------------|
| [Feature] | [honest reason — not OKR-aligned, superseded, too early] | [what would bring it back] |""",

    "scenario": """You are a senior product manager modeling the downstream impact of a proposed roadmap change.

Given a baseline roadmap and a proposed change (e.g., "delay Feature X by one quarter",
"add Feature Y to Q2", "reduce team by one engineer"), produce a scenario analysis that
shows exactly what changes and what stays the same.

# Scenario Analysis

**Proposed change**: [restate the change from the input]
**Analysis date**: [today]

---

## Summary

[2-3 sentences: what the change costs, what it buys, and the recommendation.]

---

## Baseline vs. Scenario Comparison

| Dimension | Baseline | Scenario | Delta |
|-----------|----------|----------|-------|
| [Feature X ship date] | Q2 | Q3 | +1 quarter |
| [OKR: WAU 32→42%] | On track by Q2 | At risk until Q3 | ⚠️ 1 quarter slip |
| [Feature Y] | Q3 | Q2 (pulled in) | -1 quarter |
| [Team dependency: Eng] | Q2 free for Feature Z | Q2 blocked by Feature X | ⚠️ Blocks Feature Z |
| [Capacity Q2] | 85% utilized | 92% utilized | ⚠️ +7% (over threshold) |

---

## OKR Timeline Impact

For each OKR affected:

| OKR | Baseline timeline | Scenario timeline | Risk level | Notes |
|-----|------------------|------------------|-----------|-------|
| [OKR text] | [when it's achieved] | [new timeline] | 🔴 High / 🟡 Medium / 🟢 Low | [what changes] |

---

## What Gets Pushed Out

List every downstream consequence of the change:

| Consequence | Type | Severity | Can be mitigated? |
|-------------|------|----------|-------------------|
| [Feature Z delayed] | Schedule | High | Yes — parallelize with Feature X if we hire contractor |
| [OKR KR2 misses Q3] | Metric | High | No — KR2 depends on Feature X |

---

## What Gets Better

| Benefit | Confidence | Notes |
|---------|-----------|-------|
| [e.g., Feature Y ships sooner] | High / Medium | [why this is real, not speculative] |

---

## Decision Recommendation

**Recommended choice**: [Proceed with change / Reject change / Proceed with modification]

**Rationale**: [2-3 sentences tying the tradeoffs to OKR priority]

**Conditions**: [What must be true for this recommendation to hold — if X changes, the answer changes]""",
}


def run_roadmap(
    brief: str,
    mode: str,
    quarters: int,
    velocity: str,
    output_file: str | None = None,
) -> None:
    client = anthropic.Anthropic()

    modes_to_run = list(SYSTEM_PROMPTS.keys()) if mode == "all" else [mode]
    all_results = []

    context_lines = [f"Produce the following roadmap artifact for:\n\n{brief}"]
    if quarters:
        context_lines.append(f"\nPlanning horizon: {quarters} quarters.")
    if velocity:
        context_lines.append(f"Team velocity / capacity: {velocity}.")
    user_content = "\n".join(context_lines)

    for m in modes_to_run:
        system = SYSTEM_PROMPTS[m]

        if len(modes_to_run) > 1:
            print(f"\n{'=' * 60}")
            print(f"MODE: {m.upper()}")
            print("=" * 60)
        else:
            print(f"Roadmap Agent [{m} mode]...\n")
            print("=" * 60)

        result = []
        with client.messages.stream(
            model="claude-sonnet-4-6",
            max_tokens=3500,
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
        print(f"\nRoadmap saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Roadmap agent — builds quarterly roadmaps, sequences features against OKRs, "
            "models capacity and scenarios"
        )
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--brief", help="Roadmap context, backlog, or change description as text")
    group.add_argument("--file", help="Path to backlog, PRD, or roadmap file")
    parser.add_argument(
        "--mode",
        choices=[*list(SYSTEM_PROMPTS.keys()), "all"],
        default="quarterly",
        help="Type of roadmap output (default: quarterly)",
    )
    parser.add_argument(
        "--quarters",
        type=int,
        default=4,
        help="Number of quarters to plan (default: 4)",
    )
    parser.add_argument(
        "--velocity",
        type=str,
        default="",
        help='Team capacity context, e.g. "2 engineers, 22pts/sprint"',
    )
    parser.add_argument("--output", help="Save output to this markdown file")
    args = parser.parse_args()

    if args.brief:
        brief = args.brief
    else:
        brief = Path(args.file).read_text()
        print(f"Loaded from: {args.file}\n")

    run_roadmap(
        brief,
        mode=args.mode,
        quarters=args.quarters,
        velocity=args.velocity,
        output_file=args.output,
    )


if __name__ == "__main__":
    main()
