# Skill: Experiment Design

## Trigger Phrases
- "design an A/B test for"
- "run an experiment on"
- "how do I test whether"
- "set up an experiment to"
- "sample size for"
- "how long should we run this test"
- "interpret these A/B results"
- "what's the minimum detectable effect"

## Description
Design statistically valid experiments, calculate required sample sizes, define success criteria, and interpret results. Covers A/B tests, multivariate tests, holdout groups, and pre/post analyses. Flags underpowered tests before they waste time.

## Behavior

### Step 0: Validate the experiment type (always run this first)

Before designing an A/B test, ask: **is a controlled experiment actually the right approach?**

| Situation | Right method | Why not A/B |
|-----------|-------------|------------|
| Testing whether the problem exists | Fake door / smoke test | No product to A/B yet |
| Testing willingness to pay | Fake door or pricing page variant | Need real payment signal, not usage |
| Need an answer in < 1 week | Pre/post or manual test | A/B needs minimum 2 weeks |
| Can't split traffic (single-player) | Pre/post or cohort comparison | No treatment/control possible |
| New feature with no baseline | Concierge test or dogfood first | Can't define MDE without baseline |
| Enough traffic for a valid test | A/B test | Standard case |

Only proceed to A/B design if a controlled experiment is the right call. If not, route to
the appropriate method and explain why.

### Mode 1: Design an Experiment

When triggered, ask for:
1. What you're testing (feature, copy, flow, price)
2. The metric you're measuring (and its current baseline value)
3. The minimum effect size you care about (smallest change worth acting on)
4. Available traffic / weekly volume

Then produce:

**Experiment Brief**

| Field | Value |
|-------|-------|
| Hypothesis | If we [change], then [metric] will [direction] by [amount] because [reason] |
| Primary metric | [Metric + baseline] |
| Secondary metrics | [What else to watch] |
| Guardrail metrics | [What must not get worse] |
| Unit of randomization | User / Session / Account |
| Traffic split | [50/50 or unequal — justify if unequal] |
| Required sample size | [N per variant] |
| Estimated run time | [Weeks at current traffic] |
| Minimum detectable effect | [MDE] |
| Statistical significance | 95% (two-tailed) |
| Statistical power | 80% |

**Sample Size Calculation**
Show the calculation clearly:
- Baseline conversion: [X]%
- MDE: [Y]% relative change (i.e., [X × Y/100]% absolute)
- Required n per variant: [formula result]
- At [weekly volume] users/week: [N weeks to run]

Flag if run time exceeds 8 weeks — test should likely be redesigned or MDE reconsidered.

---

### Mode 2: Interpret Results

When given results, produce:

**Results Summary**

| Variant | n | Metric | vs. Control | p-value | Significant? |
|---------|---|--------|-------------|---------|-------------|
| Control | | | — | — | — |
| Treatment | | | +X% | 0.0X | ✅ / ❌ |

**Decision**: Ship / Don't ship / Extend test / Investigate further

**Interpretation**:
- Was the result statistically significant? (p < 0.05)
- Was the result practically significant? (did it exceed MDE?)
- Did any guardrail metrics move negatively?
- Are there segment differences worth investigating (mobile vs desktop, new vs returning)?

**Pitfalls to flag**:
- Peeking: was the test stopped early when results looked good?
- Novelty effect: could engagement be from newness rather than value?
- Simpson's paradox: could segment mix shifts be masking the true effect?

---

### Mode 3: Pre/Post Analysis (no A/B)

When a proper A/B isn't possible, produce a pre/post analysis framework:
- Define the pre period and post period
- Identify a control group or comparable metric to account for trends
- Calculate the difference-in-differences
- State the confidence level and key assumptions
- Flag that pre/post is weaker evidence than a randomized test

## Output Style
- Show the math — don't just give the number, show how you got it
- Always flag underpowered tests before the team commits to running them
- Be direct about when a result is inconclusive — "not significant" is a valid finding

## Customization Tips
- Add your standard significance threshold if it differs from 95% (some orgs use 90% for low-stakes tests)
- Add your standard test duration policy (e.g., "minimum 2 weeks regardless of sample size reached")
- Add your primary product metrics so Claude can auto-populate baseline values
