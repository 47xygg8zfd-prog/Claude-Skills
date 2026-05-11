"""
Feature Prioritizer Agent
Takes a list of features or backlog items and produces a RICE-scored,
ranked backlog with prioritization rationale and explicit trade-offs.

Usage:
    python feature_prioritizer.py --features features.txt
    python feature_prioritizer.py --features features.json --context context.md
    python feature_prioritizer.py --features backlog.txt --method rice --output prioritized.md
"""

import anthropic
import argparse
from pathlib import Path


SYSTEM_PROMPT = """You are a senior product manager prioritizing a feature backlog.

Given a list of features or backlog items, produce a prioritized backlog in this format:

# Prioritized Backlog — [Date]

**Method**: RICE (Reach × Impact × Confidence ÷ Effort)
**Context**: [summarize any product context provided]

---

## Scoring Key

| Dimension | Scale | Notes |
|-----------|-------|-------|
| **Reach** | # users affected per quarter | Estimate from context; flag if unknown |
| **Impact** | 0.25 / 0.5 / 1 / 2 / 3 | 3 = massive impact on primary metric |
| **Confidence** | 20% / 50% / 80% / 100% | How confident are we in the estimates? |
| **Effort** | Person-weeks | Total engineering + design time |
| **RICE Score** | (R × I × C) ÷ E | Higher = prioritize first |

---

## Ranked Backlog

| Rank | Feature | Reach | Impact | Confidence | Effort | RICE | Category |
|------|---------|-------|--------|-----------|--------|------|---------|
| 1 | [Name] | [#] | [score] | [%] | [weeks] | [score] | [Must Have / Growth / Debt / Delight] |
| 2 | ... | | | | | | |

---

## Feature Analyses

For each feature (top 5 in detail, remainder summarized):

### [Feature Name]
**One-line description**: [what it does]
**Reach**: [estimate] — [reasoning]
**Impact**: [score] — [why this score]
**Confidence**: [%] — [what we know vs. don't know]
**Effort**: [weeks] — [assumptions]
**RICE Score**: [calculated]

**Risks if we ship this**:
- [risk 1]

**Risks if we DON'T ship this**:
- [risk 1]

**Recommended sprint**: [Now / Next / Later / Never]

---

## Portfolio View

Across the full backlog, the current allocation is:

| Category | Count | % of Effort |
|----------|-------|-------------|
| Must Have (bugs, reliability, commitments) | [n] | [%] |
| Growth (adoption, engagement, retention) | [n] | [%] |
| Technical Debt | [n] | [%] |
| Delighters (new value creation) | [n] | [%] |

**Recommendation**: [1-2 sentences on whether the portfolio balance looks right]

---

## What's NOT Prioritized (and Why)

| Feature | Why Deprioritized |
|---------|------------------|
| [name] | [RICE score too low / blocked / wrong quarter / wrong audience] |

---

## Key Trade-offs

[2-3 explicit trade-offs the team is making with this prioritization]

1. **[Trade-off]**: By prioritizing [A], we're deferring [B]. This means [consequence].
2. ...

---

Rules:
- Every feature must have a RICE score — estimate if data is missing, flag the assumption
- Mark estimates with [EST] so the team knows what to validate
- Don't hide low-priority items — explain WHY they're low, so stakeholders understand the logic
- RICE is a tool, not a verdict — call out where qualitative judgment should override the score
- Effort estimates should assume an average engineer; adjust if team context is provided"""


def prioritize_features(
    features: str,
    context: str = "",
    method: str = "rice",
    output_file: str | None = None,
) -> None:
    client = anthropic.Anthropic()

    user_content = f"Prioritize the following features:\n\n{features}"
    if context:
        user_content += f"\n\nProduct context:\n{context}"
    if method != "rice":
        user_content += f"\n\nUse the {method.upper()} prioritization method instead of RICE."

    print("Prioritizing backlog...\n")
    print("=" * 60)

    result = []

    with client.messages.stream(
        model="claude-sonnet-4-6",
        max_tokens=3000,
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
        print(f"\nPrioritized backlog saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Prioritize a feature list using RICE scoring"
    )
    parser.add_argument(
        "--features", required=True, help="Path to feature list file (text or JSON)"
    )
    parser.add_argument(
        "--context",
        help="Path to product context file (CLAUDE.md, OKRs, strategy doc)",
    )
    parser.add_argument(
        "--method",
        choices=["rice", "ice", "moscow", "impact-effort"],
        default="rice",
        help="Prioritization method (default: rice)",
    )
    parser.add_argument(
        "--output", help="Save prioritized backlog to this markdown file"
    )
    args = parser.parse_args()

    features = Path(args.features).read_text()
    print(f"Loaded features from: {args.features}\n")

    context = ""
    if args.context:
        context = Path(args.context).read_text()
        print(f"Loaded context from: {args.context}\n")

    prioritize_features(
        features,
        context=context,
        method=args.method,
        output_file=args.output,
    )


if __name__ == "__main__":
    main()
