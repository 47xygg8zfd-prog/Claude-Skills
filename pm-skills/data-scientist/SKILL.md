---
name: data-scientist
description: >
  Define metrics, design analyses, interpret experiment results, scope ML models,
  and turn data into product decisions. Use this skill when the user asks for a
  measurement plan, wants to interpret A/B test results, needs SQL for a data
  analysis, wants to scope a machine learning feature, or needs to turn data
  findings into a clear narrative. Also trigger when the user says things like
  "what does this data tell us", "how should we measure this", "interpret these
  results", "is this statistically significant", "should we build a model for",
  or "write the analysis plan". Works from raw data questions, experiment results,
  or a PRD.
---

# Data Scientist Skill

Define what to measure, design rigorous analyses, interpret results honestly, and
translate data into decisions that move the product forward.

## When to Use
- Defining success metrics before a feature ships
- Designing an A/B experiment (complement to the experiment-design skill)
- Interpreting experiment results — significance, effect size, what to do next
- Scoping a machine learning feature — what's feasible, what data is needed
- Building an analysis plan for a product question
- Turning a data finding into a narrative that drives a decision

---

## Output Formats

### 1. Measurement Plan
Define how a product outcome will be measured before building.

```
# Measurement Plan: [Feature / Initiative]

**Date**: [today]
**Owner**: Data Science / Analytics

---

## North Star Metric for This Feature
[The one metric that best captures whether this feature is working]
- **Definition**: [Exact calculation — who, what action, over what window]
- **Baseline**: [Current value — or "requires measurement before launch"]
- **Target**: [Goal and timeframe]
- **Measurement method**: [Tool, query, dashboard]

---

## Supporting Metrics

| Metric | Type | Definition | Baseline | Target |
|--------|------|-----------|----------|--------|
| [metric] | Leading / Lagging | [exact calculation] | [value] | [goal] |

---

## Instrumentation Requirements

Events to add before this feature ships:

| Event name | Trigger | Properties | Owner |
|-----------|---------|-----------|-------|
| `[event_name]` | [when it fires] | `{ [key]: [type] }` | [eng] |

---

## Guardrail Metrics (must not degrade)

| Metric | Current | Acceptable floor | Action if breached |
|--------|---------|-----------------|-------------------|
| [metric] | [value] | [threshold] | [kill switch / investigate] |

---

## Data Availability

| Data needed | Source | Available? | Gap |
|------------|--------|-----------|-----|
| [data] | [table / tool] | Yes / No / Partial | [what's missing] |

---

## Dashboard / Reporting

- **Where**: [Snowflake view / QuickSight dashboard / Amplitude / Mixpanel]
- **Cadence**: [Daily / Weekly / Real-time]
- **Audience**: [Who reviews this and how often]
- **Alerts**: [What triggers a Slack/PagerDuty alert]
```

### 2. Analysis Plan
A structured plan for answering a specific product question with data.

```
# Analysis Plan: [Question]

**Question**: [The specific, answerable question this analysis addresses]
**Requestor**: [PM / Exec / Team]
**Deadline**: [date]
**Analyst**: [name or TBD]

---

## Hypothesis

[State the hypothesis being tested. If exploratory (no prior hypothesis), say so explicitly.]

Null hypothesis: [H₀ — what we'd see if nothing is happening]
Alternative hypothesis: [H₁ — what we'd see if the effect exists]

---

## Methodology

**Type**: Descriptive / Diagnostic / Predictive / Causal
**Approach**: [cohort analysis / funnel analysis / regression / segmentation / time series]

**Unit of analysis**: [user / session / account / event]
**Time window**: [date range and rationale — why this window?]
**Segmentation**: [cuts to run — by cohort, plan, geo, device]

---

## Data Sources

| Table / Source | Fields needed | Join key | Notes |
|---------------|--------------|---------|-------|
| [table] | [fields] | [key] | [caveats] |

---

## SQL Sketch

```sql
-- [Brief description of what this query does]
SELECT
  [dimensions],
  [metrics]
FROM [table]
WHERE [filters]
GROUP BY [dimensions]
ORDER BY [metric] DESC
```

---

## Expected Output

[What the analysis will produce — a table, a chart, a number, a segmentation]

---

## Caveats and Limitations

- [Known data quality issue]
- [Selection bias risk]
- [Confounding variable to acknowledge]

---

## How Results Will Be Used

[What decision this analysis informs — and what we'll do if results go each way]
```

### 3. Experiment Results Interpretation
Interpret A/B test results and make a clear ship / iterate / kill recommendation.

```
# Experiment Results: [Test Name]

**Test ran**: [start date] – [end date] ([N days])
**Sample**: [N control] / [N treatment]
**Analyst**: [name]

---

## Sanity Checks

| Check | Result | Pass? |
|-------|--------|-------|
| Sample ratio mismatch (SRM) | [observed split vs. expected] | ✓ / ✗ |
| Pre-experiment baseline stable | [variance check] | ✓ / ✗ |
| No instrumentation gaps | [event coverage check] | ✓ / ✗ |

[If any sanity check fails: stop here, investigate before interpreting results]

---

## Primary Metric Results

| Metric | Control | Treatment | Relative lift | p-value | Significant? |
|--------|---------|-----------|--------------|---------|-------------|
| [primary] | [value] | [value] | [+X%] | [p] | Yes / No |

**Effect size**: [Cohen's d or equivalent — is this practically significant, not just statistically?]
**Confidence interval**: [[lower, upper] — what range of true effects is plausible]

---

## Guardrail Metric Results

| Metric | Control | Treatment | Change | Breached? |
|--------|---------|-----------|--------|----------|
| [metric] | [value] | [value] | [+/-X%] | No / Yes — [action] |

---

## Segmentation

| Segment | Lift | Significant? | Interpretation |
|---------|------|-------------|---------------|
| [segment] | [+X%] | Yes / No | [what this means] |

[Heterogeneous treatment effects — did the feature work better for some users?]

---

## Interpretation

**Primary finding**: [The result in one sentence — specific numbers, not "positive trend"]

**What's driving it**: [Mechanism hypothesis — why did treatment move the metric?]

**What's NOT clear**: [What the data can't tell us]

**Novelty effect risk**: [Is the lift likely to persist or decay? Evidence?]

---

## Recommendation

**Decision**: Ship / Iterate / Kill

**Rationale**: [The argument in 2-3 sentences — data + judgment]

**If Ship**: [Any monitoring to set up post-launch]
**If Iterate**: [Specific hypothesis for the next test]
**If Kill**: [What we learned and what it rules out]

---

## Caveats

- [Any data quality issue that affects confidence]
- [External factors during the test window]
- [Population that wasn't covered by the test]
```

### 4. ML Feature Scoping
Evaluate feasibility and define requirements for a machine learning feature.

```
# ML Feature Scoping: [Feature Name]

**Date**: [today]

---

## The Problem

[What prediction, classification, ranking, or generation task are we solving?]

**Input**: [What data does the model receive?]
**Output**: [What does the model produce?]
**User value**: [How does this output improve the user experience?]

---

## Feasibility Assessment

| Dimension | Assessment | Notes |
|-----------|-----------|-------|
| Training data available | Yes / Partial / No | [volume, quality, labels] |
| Signal-to-noise ratio | High / Med / Low / Unknown | [evidence] |
| Latency requirement | [Xms — online / batch] | [feasible with current infra?] |
| Interpretability need | High / Low | [is "why" needed for trust?] |
| Regulatory constraint | None / Some / Significant | [PII, fairness, audit] |

**Verdict**: Feasible now / Feasible with investment / Not feasible yet / Buy vs. build

---

## Data Requirements

| Data | Volume needed | Quality bar | Currently available |
|------|--------------|-------------|-------------------|
| [feature data] | [N rows / events] | [label accuracy %] | Yes / No / Partial |

**Label strategy**: [How do we get ground truth? Human labels / implicit feedback / proxy metric]

---

## Model Approach

**Recommended approach**: [Rule-based / Classic ML / Deep learning / LLM / Retrieval]
**Rationale**: [Why this — complexity vs. performance vs. maintainability tradeoff]
**Alternative considered**: [What else was evaluated and why rejected]

---

## Evaluation Framework

**Offline metric**: [Precision@K / AUC-ROC / RMSE / etc. — and why this metric]
**Online metric**: [What A/B test metric proves the model is adding user value]
**Baseline**: [What we're beating — rule-based / random / current behavior]
**Minimum bar to ship**: [Specific threshold — e.g., "AUC > 0.75 and online CTR +5%"]

---

## Risks

| Risk | Mitigation |
|------|-----------|
| [Training / serving skew] | [feature pipeline validation] |
| [Model bias / fairness] | [disaggregated evaluation by segment] |
| [Cold start] | [fallback strategy] |
| [Concept drift] | [monitoring and retraining cadence] |

---

## Build vs. Buy

| Option | Cost | Quality | Time to value | Recommendation |
|--------|------|---------|--------------|---------------|
| Build in-house | [eng-weeks] | [expected quality] | [timeline] | |
| API (OpenAI / Anthropic / etc.) | [$/call] | [quality estimate] | [days] | |
| OSS model fine-tuned | [eng-weeks + GPU] | [quality estimate] | [timeline] | |

**Recommended**: [Option — with rationale]

---

## Success Criteria and Timeline

| Milestone | Target | Date |
|-----------|--------|------|
| Prototype / offline eval | [metric threshold] | [date] |
| A/B test launch | [traffic %] | [date] |
| Full rollout | [online metric threshold] | [date] |
```

### 5. Data Storytelling
Turn analysis findings into a narrative that drives a decision.

```
# Data Story: [Question / Decision]

**Prepared for**: [Audience — PM / Exec / Board]
**Date**: [today]

---

## The Question We Answered

[One sentence. Specific and answerable.]

---

## The Answer

[The conclusion — upfront. Don't make the reader wait for the punchline.]

---

## The Evidence

**Finding 1**: [Specific metric + number]
[1-2 sentences of context. What makes this number meaningful?]

**Finding 2**: [Specific metric + number]
[Context]

**Finding 3**: [Specific metric + number]
[Context]

---

## What This Means for the Product

[The "so what" — what does the data imply we should do? Specific action or decision.]

---

## What We Ruled Out

[Alternative hypotheses that the data allows us to eliminate]

---

## What We're Still Uncertain About

[Questions the data can't answer — and what we'd need to answer them]

---

## Recommended Action

[One clear recommendation — not "it depends" or "we should monitor"]
```

---

## Output Guidelines

- **Lead with the answer** — never make executives read to the end to find the conclusion
- **Distinguish statistical significance from practical significance** — a p<0.05 result with a 0.1% lift is meaningless; say so
- **Quantify uncertainty** — confidence intervals are more honest than point estimates
- **Flag data quality issues** — a caveat up front is better than a credibility problem after
- **One recommendation** — if the data supports multiple interpretations, pick the most defensible one and state your reasoning
- **Avoid "more data needed"** as a conclusion — it's almost always true and rarely helpful

## Integration Points

- Use after the **experiment-design** skill has defined the test — data science interprets the results
- Feed findings into the **prd** skill — data evidence belongs in the requirements document
- Use the **HEART framework** to structure the metric hierarchy before writing a measurement plan
- The `pdlc_orchestrator.py` runs data science as stage 6 — between experiment and design
