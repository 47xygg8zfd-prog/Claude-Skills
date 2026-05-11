"""
Experiment Designer Agent
Takes a feature hypothesis and produces a complete experiment design:
primary metric, guardrail metrics, sample size, duration, and analysis plan.

Usage:
    python experiment_designer.py --hypothesis "sending a weekly digest increases WAU"
    python experiment_designer.py --feature "digest email" --metric "WAU" --baseline 0.32
    python experiment_designer.py --hypothesis "..." --output experiment.md
"""

import anthropic
import argparse
from pathlib import Path


SYSTEM_PROMPT = """You are a senior data scientist designing product experiments.

Given a feature hypothesis, produce a complete experiment design in this format:

# Experiment Design: [Hypothesis Short Name]

**Status**: Draft
**Last Updated**: [today's date]
**Hypothesis**: [restate clearly as "If [change], then [metric] will [direction] by [magnitude], because [mechanism]"]

---

## Hypothesis Breakdown

| Element | Value |
|---------|-------|
| Independent variable | [what you're changing] |
| Dependent variable | [primary metric] |
| Mechanism | [why you believe this change causes that outcome] |
| Direction | Increase / Decrease / Change |
| Minimum detectable effect | [smallest change worth acting on] |

---

## Experiment Design

**Type**: A/B test / Multivariate / Holdout / Switchback / Pre-post
**Randomization unit**: User / Session / Account / [other]
**Allocation**: [e.g., 50% control / 50% treatment, or 80/20 for high-risk]

**Control group**: [exactly what control receives — no change, or current default]
**Treatment group(s)**:
- Treatment A: [description]
- Treatment B (if multivariate): [description]

**Targeting**:
- Include: [who is eligible — segment, cohort, geography]
- Exclude: [who to exclude and why — new users, power users, etc.]

---

## Metrics

### Primary Metric
**Metric**: [name]
**Definition**: [exact calculation — e.g., "WAU: distinct user_ids with at least 1 session in the 7-day window"]
**Baseline**: [current value or "requires measurement"]
**MDE**: [minimum detectable effect — smallest change worth shipping]
**Direction**: Increase is good / Decrease is good

### Guardrail Metrics (must not degrade)
| Metric | Baseline | Acceptable threshold | Why it matters |
|--------|----------|---------------------|---------------|
| [e.g., Unsubscribe rate] | [value] | Must not increase by >X% | [rationale] |
| [e.g., Support tickets] | [value] | Must not increase | [rationale] |

### Secondary Metrics (informational, not decision-driving)
| Metric | What it tells us |
|--------|----------------|
| [metric] | [insight] |

---

## Sample Size & Duration

**Required sample size**: [calculate or state formula]
- Assumed baseline conversion: [value]
- MDE: [value]
- Statistical power: 80%
- Significance threshold: p < 0.05 (two-tailed)

**Estimated ramp time**: [how long to reach required sample at current traffic]
**Recommended duration**: [total runtime — typically ≥ 2 weeks to capture weekly cycles]
**Minimum runtime**: [never stop before this regardless of results]

[If baseline/traffic not provided: flag as [NEEDS DATA: measure baseline first]]

---

## Pre-Experiment Checklist

- [ ] Baseline metric measured and stable for ≥ 2 weeks
- [ ] Instrumentation confirmed — metric fires correctly in both groups
- [ ] Randomization verified — no selection bias in assignment
- [ ] SRM (sample ratio mismatch) check configured
- [ ] Guardrail alerts set up
- [ ] Stakeholder sign-off on MDE and primary metric

---

## Analysis Plan

**Decision criteria**:
- Ship if: primary metric improves by ≥ MDE AND no guardrail degraded AND p < 0.05
- Iterate if: directionally positive but below MDE — re-examine UX and retest
- Kill if: primary metric flat or negative with p < 0.05, OR any guardrail breached

**Segmentation cuts** (run after primary result):
- By [segment e.g., new vs. returning users]
- By [segment e.g., account size]
- By [segment e.g., platform]

**Statistical method**: [t-test / Mann-Whitney / chi-square — based on metric type]

**Novelty effect check**: Compare week 1 vs. week 2+ performance in treatment group

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| [e.g., Interference between groups] | Low | High | [e.g., Randomize at account level, not user level] |
| [e.g., Insufficient sample before deadline] | Med | Med | [e.g., Expand eligibility criteria] |
| [e.g., Novelty effect inflates early results] | Med | Med | [e.g., Run ≥ 4 weeks; analyze by week] |

---

## Open Questions

1. [What needs confirmation before experiment launches]
2. [Statistical or product question that affects design]

---

Rules:
- Every experiment must have exactly one primary metric — not a composite
- Guardrail metrics are mandatory — if none are obvious, derive them
- Duration must be ≥ 2 full business cycles (for most B2B products: 2 weeks minimum)
- Mark any assumption about baseline or traffic with [ASSUMPTION: validate before launch]
- If the hypothesis is not falsifiable, rewrite it until it is"""


def design_experiment(
    hypothesis: str,
    metric: str = "",
    baseline: str = "",
    output_file: str | None = None,
) -> None:
    client = anthropic.Anthropic()

    user_content = f"Design an experiment to test the following:\n\n{hypothesis}"
    if metric:
        user_content += f"\n\nPrimary metric: {metric}"
    if baseline:
        user_content += f"\nCurrent baseline: {baseline}"

    print("Designing experiment...\n")
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
        print(f"\nExperiment design saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate a full experiment design from a hypothesis"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--hypothesis", help="Hypothesis as text (e.g., 'digest email increases WAU')"
    )
    group.add_argument(
        "--feature", help="Feature name — will be combined with --metric to form hypothesis"
    )
    parser.add_argument("--metric", help="Primary metric (required with --feature)")
    parser.add_argument(
        "--baseline", help="Current baseline value for the primary metric"
    )
    parser.add_argument("--output", help="Save experiment design to this markdown file")
    args = parser.parse_args()

    if args.hypothesis:
        hypothesis = args.hypothesis
    else:
        if not args.metric:
            parser.error("--feature requires --metric")
        hypothesis = f"The feature '{args.feature}' will improve {args.metric}"

    design_experiment(
        hypothesis,
        metric=args.metric or "",
        baseline=args.baseline or "",
        output_file=args.output,
    )


if __name__ == "__main__":
    main()
