# Post-Launch Retrospective — Weekly Digest Email

**Date**: 2026-05-12 (6 weeks post-full-rollout)  
**Participants**: Jordan (PM), Sam (Eng), Priya (Design), Alex (Data), Morgan (CS)  

---

## Metrics Check-In

| Metric | Baseline | Target | Actual (Week 6) | Status |
|--------|----------|--------|-----------------|--------|
| Weekly digest open rate | 61% | 75% | 73% | Near miss — 2pp short |
| Digest-active WAU | 38% | 52% | 49% | Near miss — 3pp short |
| 30-day retention | 64% | 78% | 76% | Near miss — 2pp short |
| Time-to-first-insight | 8 days | 3 days | 3.2 days | Near miss — 0.2 days over |

All four metrics moved significantly in the right direction. None fully hit Q2 targets, but three are within margin of doing so by end of quarter if the current trend holds for the remaining three weeks.

---

## What We Got Wrong

### 1. We overestimated how much the recommendation module would drive action — not just clicks

We assumed that a manager clicking the recommendation CTA meant they acted on it. Post-launch CS interviews with 18 treatment accounts revealed that 40% of managers who clicked said they "read it, found it useful, but didn't change anything that week." The CTA drove engagement with the email; it did not reliably drive behavior change. We conflated the two in our success framing.

**Impact**: Digest-active WAU is 3pp short of target. Some of that gap may be attributable to managers who open and click but don't take the action Pulse surfaced.

### 2. Timezone inference from Jira profiles was unreliable for 23% of accounts

Alex's investigation found that 23% of Jira profiles had no timezone set or had a timezone inconsistent with the manager's actual location (common in accounts where Jira was set up by IT, not the manager). These accounts defaulted to 9am UTC, meaning some managers received the digest at 2am or 4am local time. Open rates for affected accounts were 14pp below the overall average.

**Impact**: Depressed overall open rate, likely accounting for most of the gap between our 73% actual and 75% target.

### 3. We didn't account for the "Monday all-hands" pattern at enterprise accounts

Several CS-flagged accounts have company-wide all-hands on Monday mornings. Managers at these accounts muted email during that window and stopped engaging with the digest entirely after a few weeks. One account paused and never re-enabled. We had no suppression logic or re-engagement flow for lapsed digesters.

**Impact**: Contributed to slower-than-expected retention improvement; currently 2pp below the 78% target.

---

## What We'd Do Differently

### 1. Collect send-time preference at onboarding, not infer it

We should add a single-question send-time preference screen to the onboarding flow (default: Monday 9am, option to pick day and time). This adds one step but eliminates the timezone inference failure entirely. Estimated cost: 1 sprint. Estimated impact: +3–5pp open rate for affected accounts.

### 2. Define "acted on recommendation" as a first-class metric before shipping

We needed a behavioral signal — not just a click — to measure whether recommendations were driving action. The `insight_click` event was too coarse. Before v2, we should instrument a `recommendation_acted` event (e.g., manager adds a Jira comment, schedules a 1:1, resolves a flagged PR within 72 hours of digest open). This would have let us optimize recommendations by action rate, not click rate.

### 3. Build a re-engagement flow for accounts that skip two consecutive digests

A two-week lapse in opens should trigger a CS alert and a modified digest with a simplified subject line ("Your team health this week — 2 things to know"). We had no such flow at launch. Given that 6% of accounts went dark within four weeks, a lightweight re-engagement path was an obvious gap we deprioritized too aggressively in v1 scoping.

---

## v2 Recommendation

Based on the experiment results and retrospective findings, v2 should focus on three things:

1. **Personalization of the recommendation module**: The recommendation CTA drove 44% of all digest clicks but only ~60% of those clicks led to a behavioral signal. v2 should use manager health score and historical recommendation response patterns to serve contextually relevant recommendations — not a single rule-engine output for all managers.

2. **Send-time customization with timezone fix**: As above. One sprint, high ROI.

3. **Digest re-engagement flow**: Two-miss trigger → CS alert + simplified digest. Directly addresses the retention gap and the Monday all-hands edge case.

The aged PR list should be removed or collapsed in v2 based on its low click share (12%). That space should go to the recommendation module or to a new "team spotlight" module (positive signal for managers who want to recognize performance, not just flag risk).
