# Metric Tree — Pulse

## Visual Hierarchy

```
                        DIGEST-ACTIVE WAU (38% → 52%)
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                       │
  ACQUISITION           ACTIVATION              ENGAGEMENT / RETENTION
  New Accounts          TTV, First Insight      Open Rate, Action Rate,
                        Rate                    30/60/90d Retention
        │                      │                       │
   ┌────┴────┐           ┌─────┴─────┐          ┌──────┴──────┐
 Sign-up   ICP          Onboard    First       Digest    Recom-    30d
 Conv.     Fit          Compl.     Insight     Engage.   mendation Retention
 Rate      Score        Rate       Latency     Rate      CTR       Rate
```

---

## Layer 2 — Growth Levers

### Acquisition

| Metric | Definition | Baseline | Target | Owner | Type |
|---|---|---|---|---|---|
| New ICP accounts / week | Accounts onboarded where manager owns 8–30 eng on Jira + GitHub + Slack | ~12/week | ~18/week | Growth/Sales | Lagging |
| ICP fit rate | % of new accounts that meet ICP definition | 68% | 80% | Sales / PM | Leading |

### Activation

| Metric | Definition | Baseline | Target | Owner | Type |
|---|---|---|---|---|---|
| Time-to-first-insight (TTV) | Days from account creation to manager viewing first non-empty insight | 8 days | 3 days | PM / Eng | Leading |
| First-insight rate (7-day) | % of new accounts where at least one manager views an insight within 7 days of signup | ~45% | ~70% | PM / CS | Leading |
| Onboarding completion rate | % of accounts that complete all 3 setup steps (Jira connect, GitHub connect, team config) | ~62% | ~85% | PM / Eng | Leading |

### Engagement

| Metric | Definition | Baseline | Target | Owner | Type |
|---|---|---|---|---|---|
| Digest open rate | % of digest sends opened by the primary manager | 61% | 75% | PM / Growth | Leading |
| Digest click-through rate | % of opened digests where manager clicks at least one insight or recommendation | ~42% | ~60% | PM | Leading |
| Recommendation action rate | % of surfaced recommendations marked "done" or linked to a Jira action within 7 days | ~28% | ~40% | PM / Eng | Lagging |

### Retention

| Metric | Definition | Baseline | Target | Owner | Type |
|---|---|---|---|---|---|
| 30-day retention | % of accounts still digest-active at day 30 | 64% | 78% | PM / CS | Lagging |
| 60-day retention | % of accounts still digest-active at day 60 | ~48% | ~65% | PM / CS | Lagging |
| 90-day churn rate | % of accounts churned by day 90 | ~22% | ~15% | CS / PM | Lagging |

---

## Layer 3 — Drivers per Metric

### TTV Drivers

| Driver | Definition | Owner |
|---|---|---|
| Onboarding step completion rate | % of accounts completing each setup step (Jira, GitHub, team config) without CS intervention | PM / Eng |
| Data pipeline latency | Time from integration connect to first event ingested | Eng |
| Insight generation latency | Time from first event to first rendered insight in the UI | Eng / PM |

### Digest Open Rate Drivers

| Driver | Definition | Owner |
|---|---|---|
| Subject line CTR | Open rate by subject line variant (A/B) | Growth / PM |
| Send-time match rate | % of digests sent within ±1hr of manager's peak email engagement window | Growth / Eng |
| Spam/deliverability rate | % of sends reaching primary inbox vs. spam/promotions | Eng / Growth |

### Recommendation Action Rate Drivers

| Driver | Definition | Owner |
|---|---|---|
| Recommendation specificity score | Internal score: does recommendation name a person, a sprint, a specific metric? | PM / Data |
| Jira deep-link rate | % of recommendations that include a direct Jira link | PM / Eng |
| Recommendation relevance rating | % of managers who rate a recommendation "relevant" (optional thumbs feedback) | PM |

---

## Where to Focus Right Now

Given current baselines, three input metrics have the highest leverage on digest-active WAU in Q2 2026:

**1. TTV (8 days → 3 days) — Highest leverage**

TTV is the gating constraint. A manager who doesn't reach first insight in the first week is unlikely to form a digest habit. At 8 days median TTV, roughly half of new managers experience their first digest *before* they've seen a meaningful insight — which means the digest is sending recommendations without context. Fixing TTV unlocks the value of every downstream engagement metric. This is the highest-ROI investment right now.

*Hypothesis*: If TTV drops from 8 to 3 days, 7-day first-insight rate rises from 45% to 70%, which increases the cohort available to become digest-active in week 2 by ~55%. Model suggests +6–8pp on 30-day retention.

**2. Recommendation Action Rate (28% → 40%) — Highest multiplier on action_rate term**

Action rate is the denominator gap in the north star equation. Open rate at 61% is decent; action rate at 28% means we're losing more than half the value on the table post-open. The primary failure mode is recommendation vagueness — Pulse says "sprint velocity is declining" without naming who, what, or what to do. Specificity improvements here have compounding returns because they also improve future open rates (managers who acted last week are more likely to open next week).

*Hypothesis*: Increasing recommendation specificity (adding person-level attribution and Jira deep-links) will increase action rate by 8–12pp within 6 weeks of shipping.

**3. Digest Open Rate (61% → 75%) — Volume multiplier**

Open rate is a volume multiplier on everything downstream. A 14pp improvement in open rate means 14% more managers reach the action-rate stage. This is achievable through send-time personalization and subject line testing, which are relatively low-eng investments. However, do not prioritize this *over* TTV — improving open rate for managers who haven't reached first insight yet is delivering an empty experience at higher frequency.

*Priority order*: TTV first, recommendation action rate in parallel, open rate as a fast-follow.
