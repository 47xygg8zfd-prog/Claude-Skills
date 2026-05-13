# PRD — Pulse Weekly Digest Email (v1)

**Author**: Jordan  
**Eng lead**: Sam  
**Design lead**: Priya  
**Status**: Approved  
**Last updated**: 2026-02-10  

---

## Problem Statement

Pulse's in-app metrics are underused because managers have no reliable prompt to review team health data on a regular cadence. 71% of sessions are initiated via external alert links, not organic re-engagement. We need a forcing function that meets managers in their existing weekly review workflow.

---

## Goals & Success Metrics

| Metric | Baseline | Q2 2026 Target | Measurement |
|--------|----------|----------------|-------------|
| Weekly digest open rate | 61% | 75% | Mailgun open events, 28-day rolling avg |
| Digest-active WAU | 38% | 52% | `digest_sends` + session join in Snowflake |
| 30-day retention | 64% | 78% | Cohort retention table in `pulse_analytics.users` |
| Time-to-first-insight | 8 days | 3 days | First `insight_click` event after account creation |

---

## Non-Goals (v1)

- No Slack delivery. Slack integration is Q3 work; v1 is email only.
- No per-manager frequency customization. Monday 9am local time only.
- No digest content for teams with fewer than 5 data-connected members.
- No org-level rollup view in the digest. Single-team scope only.
- No AI-generated narrative prose. Recommendations come from a fixed rule engine.

---

## User Stories

1. **As Maya (new EM)**, I want to receive a Monday email that tells me the one thing I should act on this week, so I build a consistent review habit without already knowing what to look for.

2. **As Carlos (experienced EM)**, I want a digest I can skim in under 3 minutes with a clear team health signal, so I can prepare for my Friday skip-level without opening Pulse separately.

3. **As any EM**, I want each metric in the digest to be one click away from the full Pulse view, so I can drill in when something needs attention without navigating manually.

4. **As any EM**, I want to be able to pause the digest for a week (e.g., during a company all-hands week), so I don't mark it as spam when I know I'll ignore it.

5. **As Morgan (CS lead)**, I want digest send/open/click data available in the CS dashboard, so I can use low engagement as an early churn signal.

---

## Requirements (MoSCoW)

### Must Have

| # | Requirement | Why (from research): |
|---|-------------|----------------------|
| M1 | Digest sends every Monday at 9am manager's local time | Managers cite Monday morning as their planning window; 8 of 12 churned accounts said they'd use a Monday brief |
| M2 | Digest surfaces sprint predictability (4-sprint trend), top 3 aged PRs, and one prioritized recommendation | Exit interviews: these three data points were cited by 10/12 churned accounts as the most decision-relevant |
| M3 | Every data point in the email links to the corresponding Pulse view with a pre-applied filter | Session replay shows 68% of users drop off when they can't find the in-app data that matched the alert they clicked |
| M4 | Unsubscribe and one-week pause links present in every send | Legal requirement; also reduces spam-mark risk which degrades deliverability for all accounts |
| M5 | Open, click, and unsubscribe events written to `digest_sends` table within 5 minutes of event | CS team needs near-real-time engagement data for churn signals; current 24hr lag is too slow for weekly workflows |

### Should Have

| # | Requirement |
|---|-------------|
| S1 | Subject line A/B tested across 3 variants at launch (personalized name vs. team name vs. generic) |
| S2 | Digest suppressed automatically for accounts with incomplete Jira or GitHub data connections |
| S3 | Preview text optimized per email client (Gmail, Outlook, Apple Mail cover 94% of our user base) |

### Could Have

| # | Requirement |
|---|-------------|
| C1 | Manager health score trend included as a secondary module |
| C2 | "What's new in Pulse" module for feature announcements |

### Will Not Have (v1)

- Digest content in languages other than English
- Custom send-time per manager
- Digest forwarding to direct reports

---

## Open Questions

| Question | Owner | Due | Consequence if unresolved |
|----------|-------|-----|---------------------------|
| Does Mailgun or SendGrid give us better deliverability to Outlook-heavy enterprise accounts? | Sam | 2026-02-17 | Blocks infrastructure decision; delays build start |
| Can we reliably infer manager timezone from Jira profile, or do we need to collect it at onboarding? | Alex | 2026-02-17 | If unreliable, default to 9am UTC and accept degraded open rate for non-US accounts |
| Should the digest suppress if a manager has logged in within the last 24 hours (to avoid redundancy)? | Jordan | 2026-02-24 | Affects send volume estimate and open rate denominator definition |
| Legal: Does the one-week pause satisfy CAN-SPAM and GDPR re-consent obligations, or do we need a permanent opt-out flow? | Legal/Morgan | 2026-02-24 | Could require redesign of preference center before launch |
