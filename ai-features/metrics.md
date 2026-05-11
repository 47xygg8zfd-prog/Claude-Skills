# AI Feature Metrics

How to measure whether your AI feature is working in production.

---

## The Three Layers of AI Metrics

Measure AI features at three levels simultaneously:

```
Layer 1: Model quality     — Is the AI output good?
Layer 2: User behavior     — Are users acting on the output?
Layer 3: Business outcome  — Is the feature moving the metric we care about?
```

Most teams only measure Layer 3 and wonder why they can't improve the feature. All three layers are required.

---

## Layer 1: Model Quality Metrics

| Metric | Definition | How to Measure |
|--------|------------|----------------|
| Pass rate | % of outputs meeting quality bar | Automated eval (LLM-as-judge) on sampled production traffic |
| Error rate by type | % of outputs with factual errors / wrong format / wrong tone | Sampled human review (weekly) |
| Hallucination rate | % of outputs containing information not in the input | Human review of flagged outputs |
| Latency (p50 / p95) | Time from request to first token / full response | Server-side instrumentation |
| Token usage | Input + output tokens per request | API response metadata |

**Sampling strategy**: Review 50–100 production outputs per week manually. Bias your sample toward edge cases and outputs users flagged or edited.

---

## Layer 2: User Behavior Metrics

| Metric | Definition | Signal |
|--------|------------|--------|
| Acceptance rate | % of AI suggestions accepted without editing | High = users trust the output |
| Edit rate | % of accepted outputs that users then edit | High = output is useful but imprecise |
| Edit distance | How much users change the output (word diff %) | Low = model is on target |
| Rejection rate | % of suggestions dismissed or ignored | High = quality problem or wrong use case |
| Re-generation rate | % of outputs where user requests a new version | High = first output isn't hitting |
| Time-to-action | Time between seeing AI output and taking action | Low = output is actionable |

**The acceptance rate trap**: High acceptance rate is good but can be misleading — users sometimes accept a mediocre output because editing feels like more work. Pair acceptance rate with downstream task completion to validate.

---

## Layer 3: Business Outcome Metrics

These depend on what problem the AI feature solves. Map your feature to the right outcome:

| AI Feature Type | Business Metric to Watch |
|----------------|--------------------------|
| Productivity / speed (e.g. draft generation) | Time-on-task reduction, throughput increase |
| Quality improvement (e.g. better summaries) | Downstream decision quality, error rate reduction |
| Engagement / habit (e.g. digest, recommendations) | WAU lift, session depth, retention delta |
| Conversion (e.g. onboarding assistant) | Activation rate, time-to-first-value |
| Support deflection (e.g. AI answers) | Ticket volume, resolution time, CSAT |

**Always run an A/B test** for the first 4–8 weeks after launch. Compare the business metric for users who see the AI feature vs. those who don't. This is the only way to attribute business impact to the feature rather than to ambient trends.

---

## Dashboard Setup

Track these metrics weekly on a single dashboard:

### Model Health Panel
- Pass rate (7-day rolling avg) — with alert if drops >5 points
- p95 latency — with alert if exceeds SLA
- Error rate by type (bar chart, last 30 days)
- Token cost per request (trend)

### User Behavior Panel
- Acceptance rate (trend)
- Edit rate (trend)
- Re-generation rate (trend)
- Feature engagement rate (% of eligible users using it)

### Business Impact Panel
- Primary business metric (A/B split: feature ON vs. OFF)
- Secondary metric (leading indicator)
- Cumulative impact estimate (extrapolated from A/B)

---

## Alerting

Set up alerts for:

| Condition | Alert Threshold | Who to Notify |
|-----------|----------------|---------------|
| Pass rate drop | >5 points in 48 hours | PM + Eng |
| p95 latency spike | >2× normal baseline | Eng on-call |
| Error rate spike | >10% of sampled outputs | PM + Eng |
| Acceptance rate drop | >15 points week-over-week | PM |
| Cost per request spike | >50% increase | PM + Eng |
