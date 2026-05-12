# Experiment Design: TechBridge Onboarding & Engagement

**Stage**: Experiment Design | **Date**: 2026-05-12
**Owner**: PM | **Status**: Ready for review

## Hypothesis

If we give PMs a contextual explanation engine that lets them paste in technical content and get a plain-language explanation, then their self-reported confidence in technical conversations will increase by at least 1.0 points (on a 1–5 scale) within 30 days, because the tool addresses the moment-of-need rather than requiring advance study.

## Why This Experiment

The PRD targets a self-reported confidence score of 3.8 (from baseline 2.3) at 30 days. Before committing to the full concept library and workflow guides, we want to validate the core mechanic: does contextual explanation actually move confidence? The contextual explanation engine is the cheapest feature to build first and the riskiest assumption to validate — if PMs don't trust the explanations or don't use the tool in real situations, nothing else matters.

## What We're Testing

**Feature**: Contextual Explanation Engine (MVP — paste technical content, get a PM-specific explanation)

**Control group**: Waitlist users who receive a weekly "PM Tech Tip" email newsletter (static content, equivalent effort to produce)

**Treatment group**: Active access to the contextual explanation engine web app

## Primary Metric

- **Self-reported confidence score** (1–5 scale, same 5-question survey used for baseline)
- Measured at: signup, day 14, day 30
- Target lift: +1.0 points by day 30 in the treatment group vs. control

## Secondary Metrics

| Metric | Why It Matters | Target |
|--------|---------------|--------|
| Weekly Active Users (WAU) | Validates workflow integration (not just novelty) | ≥40% of signups active in week 3 and 4 |
| Explanations generated per active user per week | Proxy for habit formation | ≥3/week by week 2 |
| Day-7 retention | Early signal on whether tool survives novelty phase | ≥60% |
| Session length | Are PMs actually reading? | ≥2 min per session |

## Guardrail Metrics (do not cross)

- NPS < 20: Stop and diagnose — explanations may be wrong or untrusted
- Explanation error rate > 5% (user-reported "this is wrong"): Pause — model quality issue
- Support contacts > 10%: UX is too confusing to ship

## Sample Size & Duration

- **Target**: 200 signups (100 treatment, 100 control)
- **Duration**: 30 days from first user activation
- **Power calculation**: To detect a 0.8-point lift (80% confidence interval, two-tailed) with baseline σ ≈ 0.9 (estimated from similar self-reported skill surveys), we need ~80 per group. 100/100 gives us buffer for attrition.
- **Expected attrition**: 20–25% dropout from both groups (PMs are busy). Still above minimum.

## Recruiting & Segmentation

- **Source**: Direct outreach to PM communities (Lenny's, Mind the Product), LinkedIn PM groups, internal network
- **Screening criteria**: Must be at a B2B SaaS company, manage a product with a dedicated engineering team, not have a computer science or software engineering degree
- **Randomization**: Coin-flip at signup; stratified by seniority (junior / mid / senior) to prevent imbalance
- **Blinding**: Control group is not told they're on a waitlist — framed as "different onboarding track"

## Instrumentation Plan

| Event | When | Properties |
|-------|------|------------|
| `signup_complete` | Account created | seniority, company_size, source |
| `survey_submitted` | Day 0 / 14 / 30 | confidence_score (1–5), 5 sub-questions |
| `explanation_generated` | Each use | input_length, output_length, category (tech_term / ticket / design_doc) |
| `explanation_rated` | After each | helpful (thumbs) / inaccurate (flag) |
| `session_start` / `session_end` | Each session | duration, page_count |
| `concept_bookmarked` | (if feature enabled) | concept_id |

## Decision Criteria

| Outcome | Signal | Decision |
|---------|--------|----------|
| +1.0 point confidence lift, WAU ≥40% | Strong | Ship to all. Proceed to concept library + workflow guides. |
| +0.5–1.0 point lift, WAU ≥30% | Moderate | Ship with investment in retention hooks. Do not expand scope yet. |
| +0.5 point lift, WAU <25% | Weak habit | Pause. UX problem or wrong audience. Diagnose before spending on content. |
| <0.5 lift regardless of usage | Miss | Kill or pivot. Either the explanation quality is too low or PMs don't feel the gap we hypothesized. |

## Risks

1. **Survey response rate**: PMs won't complete day-14/30 surveys. Mitigation: in-app prompt + $10 gift card incentive at each survey, not just at the end.
2. **Content quality variance**: Claude-generated explanations may be inconsistent. Mitigation: define quality rubric before launch; spot-check 20 explanations/week.
3. **Control group contamination**: Control users discover the tool via social media. Mitigation: no public launch during experiment; soft waitlist framing only.
4. **Selection bias**: Only highly motivated PMs sign up, inflating confidence gains. Mitigation: note in analysis; don't generalize to passive learners.

## Timeline

| Milestone | Date |
|-----------|------|
| Experiment design approved | 2026-05-19 |
| MVP explanation engine built | 2026-06-02 |
| Instrumentation validated | 2026-06-04 |
| First 100 users recruited | 2026-06-09 |
| Mid-point check (day 14) | 2026-06-23 |
| Experiment complete | 2026-07-09 |
| Analysis & decision | 2026-07-14 |
