# North Star Metric — Pulse

## Definition: Digest-Active WAU

**Digest-active WAU** = the count of unique managers, in a rolling 7-day window, who both *opened* the weekly digest and *took at least one downstream action* (clicked an insight, acted on a recommendation, or navigated to the product from the digest).

A manager who opens the digest and closes it is not digest-active. The action requirement is load-bearing: it filters out passive open rates and captures whether Pulse actually influenced behavior that week.

**Measured as a percentage of total active accounts' managers** for comparability across account growth. Current baseline: 38%. Q2 2026 target: 52%.

---

## Why This Metric, Not These Others

| Alternative | Why It Was Rejected |
|---|---|
| **DAU / MAU** | Too broad. A login to edit a notification preference looks the same as a login to act on a sprint risk alert. Activity without value is noise. |
| **Revenue / ARR** | Lagging by 6–12 months. By the time churn shows up in ARR, the engagement signal was already there 3 months earlier. Revenue is an outcome metric, not a leading indicator. |
| **Logins** | Same problem as DAU. Doesn't capture whether the manager got value. Optimizing logins is how you get dark patterns, not product-market fit. |
| **Open rate alone** | Measures email deliverability and subject line quality as much as product value. A manager can open and not act. Half the metric, half the signal. |

The digest is Pulse's primary value-delivery mechanism. If a manager opens the digest and acts on it, Pulse worked this week. If they don't, it didn't — regardless of what else happened in the product.

---

## The North Star Equation

```
digest-active WAU % =
  (accounts_active / total_accounts)
  × managers_per_active_account
  × digest_open_rate
  × action_rate_given_open
```

Each term is a lever:

| Factor | What Moves It | Team Owner |
|---|---|---|
| `accounts_active` | Onboarding, CS health checks | CS / Growth |
| `managers_per_account` | Expansion, account-level activation | CS / PM |
| `digest_open_rate` | Subject lines, send time, relevance of content | PM / Growth |
| `action_rate_given_open` | Quality and specificity of recommendations | PM / Eng |

Improving one factor with the others flat increases the north star linearly. The compounding opportunity is improving two simultaneously — particularly open rate and action rate, which together define the digest's value proposition.

---

## Guardrail Metrics

While optimizing digest-active WAU, the following must not degrade:

| Guardrail | Threshold | Why It Matters |
|---|---|---|
| Unsubscribe rate | < 0.5% per send | Aggressive digest optimization can burn the list |
| Support ticket volume | No more than 10% increase QoQ | Activation shortcuts can create confusion debt |
| Sprint data accuracy rate | > 95% | Recommendations are only trustworthy if the underlying data is clean |
| Time-to-first-insight | Must improve (current: 8 days) | Can't optimize engagement if activation is still broken |

---

## How to Read the Metric

| Signal | Interpretation | Response |
|---|---|---|
| Rising consistently (>+2pp/week) | Digest is delivering value; habit formation is working | Stay the course; find the segment driving it and double down |
| Flat for 2+ weeks | Growth in accounts is offset by declining per-account engagement | Investigate action rate — likely a relevance problem in the digest content |
| Declining despite open rate holding | Recommendations aren't resonating; managers open but don't act | Audit recommendation specificity; consider digest personalization |
| Declining with open rate | Email deliverability or relevance problem; managers aren't even engaging with the surface | A/B test subject lines; check send-time segmentation |
| Spike followed by drop | One-time novelty effect (new feature, campaign) without sticky value | Look at week-2 retention of the cohort that spiked |
