# Example Output: PRD Skill

**Prompt used:** "Write a PRD for a Slack digest feature that summarizes team activity weekly"

---

# PRD: Weekly Team Digest

**Product**: Pulse  
**Author**: Sarah Kim  
**Status**: Draft  
**Last Updated**: 2026-05-11  
**Target Release**: Q3 2026

---

## Problem Statement

Pulse users have rich activity data but no passive way to stay informed. Today, managers must log in and navigate dashboards to understand team trends — most don't. As a result, 68% of Pulse users log in fewer than twice per week, and churned customers cite "not enough habit formation" as a top-3 reason for leaving.

## Goals

- Increase weekly active users (WAU) by 20% within 90 days of launch
- Reduce time-to-insight for managers from ~8 minutes (active navigation) to ~2 minutes (digest scan)
- Improve 90-day retention by 10 points for accounts that enable the digest

## Non-Goals

- Real-time alerts or notifications (covered by the Alerts feature)
- Individual contributor digests (manager-facing only in v1)
- Custom digest scheduling (weekly cadence only in v1)

## User Stories

1. As a **manager**, I want a weekly email summarizing my team's Pulse activity so I can stay informed without logging in daily.
2. As a **manager**, I want to click through from the digest to the relevant dashboard section so I can investigate anything that catches my attention.
3. As an **admin**, I want to enable or disable the digest org-wide so I can control communication volume for my company.

## Proposed Solution

A weekly email digest delivered every Monday at 9am (user's local time) containing:

- **Headline metric**: The single most significant change vs. last week (up or down), with a plain-language explanation
- **Top 3 highlights**: Trend callouts ranked by magnitude of change
- **1 suggested action**: A recommendation based on the data (e.g., "Response time is up 22% — consider reviewing your SLA targets")
- **CTA**: "View full dashboard" deep-link to the relevant Pulse view

### Digest Sections (v1)
| Section | Data Source | Trigger for Inclusion |
|---------|-------------|----------------------|
| Team velocity | Sprint metrics | Always included |
| Response time | Ticket data | Always included |
| Collaboration score | Activity graph | Included if changed >10% |
| At-risk members | Engagement model | Included if any member flagged |

## Success Metrics

| Metric | Baseline | Target | Measurement |
|--------|----------|--------|-------------|
| WAU | 32% of seats | 38% of seats | Product analytics |
| Digest open rate | — | >45% | Email platform |
| Digest click-through rate | — | >20% | Email platform |
| 90-day retention (digest-enabled) | 71% | 78% | CRM cohort analysis |

## Open Questions

1. Should digest delivery time be configurable per user, or set at the admin level?
2. Do we generate the digest even for teams with no meaningful activity that week?
3. How do we handle managers with multiple teams — one digest or one per team?

## Dependencies

- Email delivery infrastructure (currently used by Alerts — confirm capacity)
- ML recommendation model for "suggested action" (data science team, est. 3 weeks)
- Unsubscribe/preference center (legal requirement before sending any new email type)

## Timeline

| Milestone | Date |
|-----------|------|
| Design review | June 2 |
| Engineering kickoff | June 9 |
| Internal beta | July 14 |
| Limited GA (25% rollout) | Aug 4 |
| Full GA | Aug 25 |
