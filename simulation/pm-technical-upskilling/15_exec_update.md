# Exec Update: TechBridge — PM Technical Fluency Platform
**Stage**: CPO / Director PM Stakeholder Update | **Date**: 2026-05-12

---

## Status: Green

On track for a 6-week build with 2 engineers + 1 designer. No blockers. One open decision (freemium vs. paid) needs a call before launch prep begins, but it does not block engineering.

---

## What We're Shipping

- **A contextual explanation engine** for product managers: paste any Slack message, ticket, or design doc and get a plain-language explanation in PM terms — in the 60 seconds before a meeting
- **For**: Mid-level B2B SaaS PMs who feel technically outmatched in engineering conversations — a segment we've validated through discovery interviews and community research
- **Business outcome we're targeting**: 55% 8-week retention and 40% WAU from signups; both are the leading indicators of a habit-forming product that can sustain a PLG growth model

---

## Confidence Level

**Medium-High** — We have strong signal that the pain is real (recurring PM community feedback, confirmation from 3 discovery conversations), and the build is low-risk technically. Our main open question is whether PMs will use the tool habitually or treat it as a novelty — which is why we're running a 30-day experiment before expanding scope.

---

## Key Metrics We'll Watch

| Metric | Baseline | Target | How Measured |
|--------|----------|--------|-------------|
| Self-reported confidence score (1–5) | 2.3 (survey) | 3.8 at 30 days | In-app survey (day 0, 14, 30) |
| 8-week retention | 0 (new product) | 55% | WAU cohort analysis in Snowflake |
| Weekly Active Users | 0 | 40% of signups active in weeks 3–4 | `session_start` events |
| Explanation flag rate ("this is wrong") | 0 | <5% | `explanation_rated` event with `inaccurate` rating |

First meaningful read available at day 14 of the experiment (estimated: 2026-06-23).

---

## Risks

| Risk | Mitigation | Owner |
|------|-----------|-------|
| PMs use it once and don't return (novelty effect) | Confidence tracker and bookmarks create a reason to return; experiment measures day-14 retention as early signal | PM |
| Claude-generated explanations are wrong on niche topics | Weekly spot-check of flagged explanations; editorial review queue before scaling content | PM + Backend |
| Freemium pricing kills conversion | Monetization decision must be made before launch; experiment will give us conversion data to inform pricing | CEO + PM |
| Prompt injection in the explanation engine | System prompt hardening + QA-specific injection test cases (TC-020) before ship | Backend + QA |
| Content is thin at launch | 50 concepts minimum before launch; PM reviewing concept seed data in parallel with engineering sprint | PM |

---

## Launch Plan

- **Soft launch** (experiment): 200 users (100 treatment / 100 control), starting 2026-06-09; sourced from PM communities (Lenny's, Mind the Product)
- **Full launch**: After experiment readout on 2026-07-14, if decision criteria for "ship" are met
- **Full launch timing**: 2026-07-21 (estimated) — Product Hunt + Lenny's sponsorship
- **Rollback trigger**: Any of: explanation flag rate >5%, NPS <20, P0 QA failure in production

---

## Decisions Needed from This Group

1. **Freemium vs. paid-only**: We need this decision before launch copy is finalized (marketing is blocked on it). Recommendation: freemium with 10 free explanations/month, then $12/month. This gives us conversion data and mirrors our existing PLG motion. CEO to confirm.

2. **Content strategy**: 50 concepts at launch sourced from Claude + PM editorial review, versus human-written by former engineers. Recommendation: Claude-generated, PM-reviewed — 10x faster to produce, and our editorial bar is "accurate and useful to PMs," not "publishable in a journal." CPO to confirm.

---

## What's Not Changing

We are explicitly not building:
- Team analytics or manager dashboards (v1 non-goal)
- GitHub / Jira integrations (v1 non-goal)
- Certifications or assessments

These are on the roadmap for post-experiment, contingent on retention results showing that PMs return to the product over multiple weeks.

---

## Two-Week Checkpoint

Next update: 2026-05-26. By then we will have:
- Engineering sprint 1 complete (DB schema, auth, concepts API)
- 20 concept library entries reviewed and approved
- Freemium decision confirmed
- Experiment recruiting begun (target: 100 PMs confirmed by 2026-06-05)
