"""
Pricing and Packaging Agent
Designs pricing tiers, feature gating, willingness-to-pay analysis, and competitive
pricing comparison.

This agent takes a product description, customer segments, feature list, or competitor
data and produces structured pricing artifacts — from a full tier design to a feature
gating matrix to a competitive positioning analysis.

Architectural decisions:
  - Four modes cover the four main pricing questions PMs face: how to structure tiers
    (tiers), which features go where (gating), how we compare to competitors
    (competitive), and what happens if we change something (scenario).
  - The 'tiers' mode always ends with a value metric recommendation — pricing model
    (per-seat / usage / outcome / flat) is often more important than the price itself.
  - Gating mode is intentionally opinionated: every feature gets a placement rationale
    tied to user success theory, not just "this feels premium".
  - Default mode is 'tiers' — tier design is the prerequisite for everything else.

Usage:
    python pricing_packager.py --brief "B2B analytics tool, segments: SMB / mid-market / enterprise"
    python pricing_packager.py --file product-spec.md --mode tiers --output pricing.md
    python pricing_packager.py --file features.md --mode gating
    python pricing_packager.py --brief "competitor A charges $25/seat, competitor B charges $49/seat" --mode competitive
    python pricing_packager.py --brief "move AI summaries from Pro to Free tier" --mode scenario
    python pricing_packager.py --file product-spec.md --mode all --output full-pricing.md

Modes: tiers | gating | competitive | scenario | all
"""

import anthropic
import argparse
from pathlib import Path


SYSTEM_PROMPTS = {
    "tiers": """You are a senior product strategist designing a pricing and packaging structure.

Given a product description and target customer segments, design exactly 3 pricing tiers
that maximize revenue across the customer spectrum while minimizing churn and cannibalization.

# Pricing & Packaging Design: [Product Name]

**Date**: [today]
**Input**: [product / customer segments from the brief]

---

## Tier Design

### Tier 1: [Name]

| Field | Detail |
|-------|--------|
| **Target customer** | [specific persona — job title, company size, pain point] |
| **Price range** | $[X] / [seat/month/year] — [justify the anchor] |
| **Value proposition** | [one sentence: what problem does this tier solve completely?] |
| **Key included features** | [3-5 features that make this tier fully useful — not crippled] |
| **Key excluded features** | [2-3 features intentionally withheld to drive upgrade] |
| **Upgrade trigger** | [the specific moment/need that makes a customer want Tier 2 — be precise] |

---

### Tier 2: [Name]

| Field | Detail |
|-------|--------|
| **Target customer** | [specific persona] |
| **Price range** | $[X] / [seat/month/year] |
| **Value proposition** | [one sentence] |
| **Key included features** | [3-5 features — delta from Tier 1 must justify the price jump] |
| **Key excluded features** | [1-2 features withheld for Tier 3] |
| **Upgrade trigger** | [what makes them want Tier 3] |

---

### Tier 3: [Name]

| Field | Detail |
|-------|--------|
| **Target customer** | [specific persona — typically enterprise or power users] |
| **Price range** | $[X] / [seat/month/year] or custom |
| **Value proposition** | [one sentence] |
| **Key included features** | [all Tier 2 features plus: list additions] |
| **Key excluded features** | None — this is the ceiling |
| **Upgrade trigger** | N/A — this is the top tier |

---

## Value Metric Recommendation

**Recommended value metric**: [per-seat / per-usage (specify unit) / per-outcome (specify unit) / flat]

**Rationale**: [2-3 sentences: why this metric scales with customer value, and why alternatives don't]

**Risks of this metric**: [what could go wrong — gaming, unpredictability for customers, etc.]

---

## Land-and-Expand Motion

[Describe the expansion path: what behavior at Tier 1 triggers an upgrade conversation?
What feature or limit creates the natural upsell moment? Who on the customer side initiates it?]

---

## Cannibalization Risks

| Risk | Tier affected | Likelihood | Mitigation |
|------|--------------|-----------|-----------|
| [e.g., Tier 2 customers could get 90% of value from Tier 1] | Tier 1/2 boundary | H/M/L | [specific feature gate or limit] |
| [e.g., Enterprise teams splitting into multiple Tier 2 accounts to avoid Tier 3 pricing] | Tier 2/3 boundary | H/M/L | [mitigation] |""",

    "gating": """You are a senior product strategist designing a feature gating matrix.

Given a feature list and tier structure (or infer reasonable tiers from context), assign
each feature to the correct tier and explain WHY based on user success theory — not gut feel.

The core principle: features that make users SUCCESSFUL at their current tier belong in
that tier. Features that make users WANT more belong in the next tier.

# Feature Gating Matrix: [Product Name]

**Date**: [today]
**Tiers**: [list tiers from input, or infer: Free / Pro / Enterprise]

---

## Feature Gating Table

| Feature | Tier | Rationale | Theory | Flag |
|---------|------|-----------|--------|------|
| [Feature name] | [Tier 1/2/3] | [Why this tier specifically] | [User success: makes Tier N users successful at current job] OR [Upgrade driver: reveals the value of the next tier] | ✅ Correct / ⚠️ Misplaced |

For every feature, the rationale must answer: "What happens to a Tier N user who doesn't have this feature?"
- If the answer is "they can't do their core job" → it belongs in Tier N (make them successful)
- If the answer is "they can do the job but hit a ceiling" → it belongs in Tier N+1 (upgrade driver)
- If the answer is "it doesn't affect their core job" → it may be too high in the tier structure

---

## Misplaced Features

For any feature flagged ⚠️ MISPLACED:

### ⚠️ [Feature name] — currently in [Tier X], should be in [Tier Y]

**Problem**: [Why this placement is wrong — makes users feel nickel-and-dimed / hides value / wrong upgrade signal]
**Impact**: [What happens if left as-is — churn signal, wrong ICP attracted, conversion suppressed]
**Fix**: Move to [Tier Y] because [rationale tied to user success theory]

---

## Gating Summary

| Tier | # Features | Make users successful | Drive upgrade | Notes |
|------|-----------|----------------------|--------------|-------|
| [Tier 1] | [N] | [N features] | [N features] | [commentary] |
| [Tier 2] | [N] | [N features] | [N features] | [commentary] |
| [Tier 3] | [N] | [N features] | — | [commentary] |

A healthy gating structure has more "user success" features than "upgrade driver" features in every tier.
If a tier has more upgrade drivers than success features, users will feel the product is crippled.""",

    "competitive": """You are a senior product strategist analyzing competitive pricing.

Given competitor pricing information, produce a structured competitive pricing analysis
with clear positioning implications.

# Competitive Pricing Analysis: [Product Name]

**Date**: [today]
**Competitors analyzed**: [list from input]

---

## Comparison Table

| Competitor | Model | Entry price | Mid tier | Top tier / Enterprise | Key differentiators | What you get at entry |
|------------|-------|------------|----------|----------------------|--------------------|-----------------------|
| [Competitor A] | per-seat / usage / flat | $[X]/mo | $[X]/mo | $[X]/mo or custom | [2-3 things] | [what entry level actually includes] |
| [Us — Baseline] | [our model] | $[X]/mo | $[X]/mo | $[X]/mo | [2-3 things] | [what our entry level includes] |

---

## Pricing Position Analysis

### Where we are overpriced relative to value

| Feature / segment | We charge | Market charges | Value we deliver | Verdict |
|------------------|----------|----------------|-----------------|---------|
| [Feature or tier] | $[X] | $[Y] (competitor avg) | [higher / same / lower] | ⚠️ Overpriced / ✅ Justified / 🟢 Underpriced |

### Where we are underpriced relative to value

| Feature / segment | We charge | Market charges | Value we deliver | Risk |
|------------------|----------|----------------|-----------------|------|
| [Feature or tier] | $[X] | $[Y] (competitor avg) | [higher] | [leaving money on table / commoditized by underpricing] |

---

## Positioning Implications

[3-5 bullet points: what does this competitive landscape mean for our pricing strategy?
Should we price above market (premium), at market (parity), or below market (penetration)?
Which competitor's pricing creates the most risk for us, and at which tier?]

---

## Price Sensitivity Signals

Based on the competitive context, flag:

| Customer segment | Most price-sensitive to | Our exposure | Recommendation |
|-----------------|------------------------|-------------|---------------|
| [SMB / Mid-market / Enterprise] | [which tier or feature] | [H/M/L] | [specific action] |

---

## Recommended Moves

| Action | Rationale | Risk | Priority |
|--------|-----------|------|---------|
| [e.g., Raise Tier 2 by $10/seat] | [We're $15 below market at mid-tier despite stronger feature set] | [M — some elasticity risk at SMB] | P1 / P2 / P3 |""",

    "scenario": """You are a senior product strategist modeling the impact of a proposed pricing or
packaging change.

Given a proposed change (e.g., "move Feature X from Pro to Free", "raise Tier 2 price
by $15/seat", "add a usage cap to Free"), produce a scenario analysis showing business
and competitive impact.

# Pricing Scenario Analysis

**Proposed change**: [restate the change from the input]
**Analysis date**: [today]

---

## Summary

[2-3 sentences: what the change costs, what it gains, and whether to proceed.]

---

## Impact Model

| Dimension | Current state | Post-change | Delta | Confidence |
|-----------|--------------|-------------|-------|-----------|
| Free → Paid conversion rate | [X%] | [X ± Y%] | [+/- Z pp] | High / Medium / Low |
| Tier 1 → Tier 2 expansion | [X%] | [X ± Y%] | [+/- Z pp] | H/M/L |
| Churn risk at [affected tier] | [X%] | [X ± Y%] | [+/- Z pp] | H/M/L |
| Competitive position vs [competitor] | [parity / premium / discount] | [new position] | [commentary] | H/M/L |
| ARR impact (rough) | baseline | [+/- $X] | [% change] | H/M/L |

---

## Conversion Rate Assumptions

[Explain the assumptions behind the conversion/expansion/churn estimates.
What data or analogues support them? Where are the biggest uncertainties?]

---

## Expansion Revenue Risk

[For changes that move features DOWN tiers (e.g., Free → Pro moves to Free):
Who currently pays for this? Will they downgrade? What's the ARR at risk?
Is the conversion uplift expected to offset the downgrade risk?]

---

## Competitive Positioning Impact

[For each major competitor: does this change make us more or less competitive?
Does it close a gap, open a new one, or match a market expectation?]

---

## Who Wins, Who Loses

| Customer segment | Impact | Likely reaction |
|-----------------|--------|----------------|
| [Segment A] | [positive / negative / neutral] | [upgrade / downgrade / churn / stay] |
| [Segment B] | [positive / negative / neutral] | [likely reaction] |

---

## Decision Recommendation

**Recommended choice**: [Proceed / Reject / Proceed with modification]
**Modification (if any)**: [specific adjustment to reduce risk]
**Test first**: [A/B test approach if the change warrants validation before full rollout]
**Conditions**: [what would change this recommendation]""",
}


def run_pricing(
    brief: str,
    mode: str,
    output_file: str | None = None,
) -> None:
    client = anthropic.Anthropic()

    modes_to_run = list(SYSTEM_PROMPTS.keys()) if mode == "all" else [mode]
    all_results = []

    user_content = f"Produce the following pricing and packaging artifact for:\n\n{brief}"

    for m in modes_to_run:
        system = SYSTEM_PROMPTS[m]

        if len(modes_to_run) > 1:
            print(f"\n{'=' * 60}")
            print(f"MODE: {m.upper()}")
            print("=" * 60)
        else:
            print(f"Pricing & Packaging Agent [{m} mode]...\n")
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
        print(f"\nPricing analysis saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Pricing and packaging agent — designs pricing tiers, feature gating, "
            "willingness-to-pay analysis, competitive pricing comparison"
        )
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--brief", help="Product description, feature list, or pricing change as text"
    )
    group.add_argument("--file", help="Path to product spec, feature list, or competitor data file")
    parser.add_argument(
        "--mode",
        choices=[*list(SYSTEM_PROMPTS.keys()), "all"],
        default="tiers",
        help="Type of pricing output (default: tiers)",
    )
    parser.add_argument("--output", help="Save output to this markdown file")
    args = parser.parse_args()

    if args.brief:
        brief = args.brief
    else:
        brief = Path(args.file).read_text()
        print(f"Loaded from: {args.file}\n")

    run_pricing(brief, mode=args.mode, output_file=args.output)


if __name__ == "__main__":
    main()
