# Experiment Design — Weekly Digest A/B Test

**Feature**: Pulse Weekly Digest Email  
**Test period**: 2026-03-10 — 2026-04-07 (4 weeks)  
**Decision date**: 2026-04-10  

---

## Hypothesis

If we send a curated weekly digest email to engineering managers every Monday morning, then weekly digest open rate will increase from 61% to at least 72%, and digest-active WAU will increase by at least 8 percentage points, because managers currently lack a reliable re-engagement trigger and our research shows Monday is their primary planning window.

---

## Experiment Design

| Parameter | Detail |
|-----------|--------|
| Randomization unit | Account (not individual user) — digest is team-scoped; manager experience must be consistent per account |
| Control | No digest email; existing in-app notification only |
| Treatment | Weekly digest email sent Monday 9am local time with sprint predictability trend, top 3 aged PRs, one recommendation, and deep links |
| Traffic allocation | 50/50 (sufficient power given account count; see sample size below) |
| Eligible accounts | Active accounts with ≥5 data-connected team members and at least one sprint completed in the last 30 days |

---

## Primary Metric

**Weekly digest open rate** (treatment group only — proportion of sent digests opened within 48 hours of delivery)

**Minimum Detectable Effect (MDE)**: 8 percentage points (61% → 69%)

**Rationale**: An 8pp lift is the minimum improvement meaningful to the business given our 75% Q2 target. Smaller lifts would not close the gap in the remaining quarter even at full rollout. We chose open rate as primary (vs. digest-active WAU) because it is a leading indicator we can measure within days rather than weeks, and it is fully attributable to the email send.

---

## Guardrail Metrics

| Metric | Acceptable threshold | Why |
|--------|---------------------|-----|
| Unsubscribe rate | < 2% of sends | Above 2% signals spam perception; damages deliverability |
| In-app session rate (control vs. treatment) | No statistically significant drop in control group | Ensures digest doesn't cannibalize in-app engagement |
| Support tickets mentioning "too many emails" | < 5 per week during test | Qualitative signal of email fatigue |
| Bounce rate | < 0.5% | Protects sender reputation with Mailgun |

---

## Sample Size Calculation

- Baseline open rate: 61%
- MDE: 8pp (target: 69%)
- Alpha: 0.05 (two-tailed)
- Power (1 - beta): 0.80

Using the standard two-proportion z-test formula:

```
n = (Z_alpha/2 + Z_beta)^2 * [p1(1-p1) + p2(1-p2)] / (p1 - p2)^2

Z_alpha/2 = 1.96, Z_beta = 0.84
p1 = 0.61, p2 = 0.69

n = (1.96 + 0.84)^2 * [0.61*0.39 + 0.69*0.31] / (0.08)^2
n = 7.84 * [0.2379 + 0.2139] / 0.0064
n = 7.84 * 0.4518 / 0.0064
n ≈ 553 accounts per arm
```

**Required**: 553 accounts per arm, 1,106 total.  
**Available**: ~1,400 eligible accounts at test start.  
**Conclusion**: Adequately powered at 50/50 split with 4 weeks to accumulate ~4 digest send events per account.

---

## Decision Criteria

| Outcome | Criteria | Decision |
|---------|----------|----------|
| Ship | Open rate lift ≥ 8pp, p < 0.05; no guardrail breached | Roll out to 100% of eligible accounts |
| Iterate | Lift is 4–7pp OR a guardrail is breached | Investigate root cause; run follow-up test with revised design (e.g., subject line, send time) |
| Kill | Lift < 4pp AND p > 0.10; OR unsubscribe rate > 2% | Do not ship; revisit channel strategy (Slack, in-app) |

---

## What We Learned

The experiment ran cleanly from March 10 to April 7. Treatment accounts received four digest sends each; 1,389 eligible accounts were randomized (693 control, 696 treatment).

**Results**:

| Metric | Control | Treatment | Delta | p-value |
|--------|---------|-----------|-------|---------|
| Weekly digest open rate | 61% | 73% | +12pp | 0.003 |
| Digest-active WAU | 38% | 49% | +11pp | 0.008 |
| Unsubscribe rate | — | 0.9% | — | — |
| In-app session rate | 1.31 sessions/user/wk | 1.29 sessions/user/wk | -0.02 | 0.41 (ns) |

**Decision**: Ship. Open rate exceeded MDE by 4pp. Digest-active WAU improved by 11pp — above the 8pp threshold. Unsubscribe rate held well below the 2% guardrail. In-app sessions were not cannibalized (non-significant).

**Secondary finding**: The single most-clicked element in the digest was the recommendation CTA ("Here's what to do this week"), accounting for 44% of all clicks. Sprint predictability trend was second at 31%. The aged PR list drove only 12% of clicks despite taking significant vertical space — flagged for v2 deprioritization.

Full rollout completed April 14. Six-week post-rollout open rate stabilized at 73%, confirming the test result was not a novelty effect.
