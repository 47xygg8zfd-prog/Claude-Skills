"""
OKR Drafter Agent
Takes strategic context, goals, or a product brief and produces a complete
OKR set with objectives, key results, scoring guidance, and alignment checks.

Usage:
    python okr_drafter.py --context "grow WAU, reduce churn, launch mobile"
    python okr_drafter.py --file strategy.md --quarter "Q3 2026"
    python okr_drafter.py --context "..." --team "growth" --output okrs.md
"""

import anthropic
import argparse
from pathlib import Path


SYSTEM_PROMPT = """You are a senior product leader drafting quarterly OKRs.

Given strategic context or goals, produce a complete OKR set in this format:

# OKRs: [Team / Product Name] — [Quarter]

**Drafted**: [today's date]
**Owner**: [leave blank unless provided]

---

## How to Use This Document

- Score each KR at the end of the quarter on a 0.0–1.0 scale
- Target score: 0.7 (hitting 1.0 means the target was too easy)
- Review KRs weekly; update the Objective score as a weighted average of its KRs

---

## Objective 1: [Verb + outcome + timeframe]

> [1-sentence rationale — why does this objective matter this quarter?]

| # | Key Result | Baseline | Target | Score |
|---|-----------|----------|--------|-------|
| KR1 | [Measurable outcome — not an activity] | [current value] | [goal] | — |
| KR2 | [Measurable outcome] | [current value] | [goal] | — |
| KR3 | [Measurable outcome] | [current value] | [goal] | — |

**Leading indicators** (check weekly):
- [Metric that predicts KR1 before the quarter ends]
- [Metric that predicts KR2]

**Risks**:
- [What could prevent this objective from being achieved?]

---

[Repeat for Objective 2, Objective 3 — typically 3 objectives max per team]

---

## Alignment Check

| KR | Maps to Company OKR | Conflict? |
|----|-------------------|-----------|
| [KR] | [Company objective or north star] | None / [describe conflict] |

---

## What's NOT in These OKRs (and Why)

[List 2-3 things the team considered but excluded — and the reason. Shows intentional prioritization.]

---

## Scoring Guide

| Score | Meaning |
|-------|---------|
| 0.0 | No progress |
| 0.3 | Started but missed significantly |
| 0.5 | Meaningful progress; fell short of target |
| 0.7 | Target achieved (the expected outcome) |
| 1.0 | Exceeded target — recalibrate next quarter |

---

Rules:
- Objectives must be qualitative, inspirational, and time-bound — not metrics
- Key Results must be measurable and binary-scorable (you either hit the number or you don't)
- No activity-based KRs: "launch X" is an output, not an outcome. Use "X achieves Y" instead
- Each objective should have 2–4 KRs; never more than 4
- Baselines must be real or marked [NEEDS BASELINE: how to measure]
- Targets should be ambitious but achievable — 70% confidence of hitting 0.7
- Flag any KR that requires infrastructure not yet in place as [DEPENDENCY: what's needed]"""


def draft_okrs(
    context: str,
    quarter: str = "",
    team: str = "",
    output_file: str | None = None,
) -> None:
    client = anthropic.Anthropic()

    user_content = "Draft OKRs based on the following context:\n\n" + context
    if quarter:
        user_content += f"\n\nQuarter: {quarter}"
    if team:
        user_content += f"\nTeam: {team}"

    print("Drafting OKRs...\n")
    print("=" * 60)

    result = []

    with client.messages.stream(
        model="claude-sonnet-4-6",
        max_tokens=2500,
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": user_content}],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            result.append(text)

    print("\n" + "=" * 60)

    if output_file:
        Path(output_file).write_text("".join(result))
        print(f"\nOKRs saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Draft OKRs from strategic context")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--context", help="Strategic goals or context as text")
    group.add_argument("--file", help="Path to strategy or context file")
    parser.add_argument("--quarter", help="Quarter label (e.g., 'Q3 2026')")
    parser.add_argument("--team", help="Team or product name")
    parser.add_argument("--output", help="Save OKRs to this markdown file")
    args = parser.parse_args()

    if args.context:
        context = args.context
    else:
        context = Path(args.file).read_text()
        print(f"Loaded context from: {args.file}\n")

    draft_okrs(
        context,
        quarter=args.quarter or "",
        team=args.team or "",
        output_file=args.output,
    )


if __name__ == "__main__":
    main()
