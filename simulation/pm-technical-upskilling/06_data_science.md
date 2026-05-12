# Data Science Brief: TechBridge — PM Technical Fluency Platform
**Stage**: Measurement Plan | **Date**: 2026-05-12

## North Star Metric

**Metric**: Monthly Technically Fluent PMs (MTFP)
**Definition**: Count of distinct users who (a) generated ≥3 contextual explanations in the calendar month AND (b) self-reported a confidence score ≥3.5 on their most recent in-app survey. Both conditions must be true.
**Baseline**: 0 (pre-launch)
**Target**: 250 MTFPs by month 3 post-launch

The dual condition matters: pure usage without confidence gain means we're a dictionary, not a learning tool. Confidence gain without usage means we got a survey response from someone who signed up and churned. We want both.

---

## Metric Hierarchy

| Level | Metric | Definition | Why it matters |
|-------|--------|-----------|---------------|
| North Star | MTFP | ≥3 explanations + confidence ≥3.5 in a calendar month | Proves workflow integration AND learning outcome |
| Primary (engagement) | WAU | Distinct users with ≥1 session in 7-day rolling window | Leading indicator of habit formation |
| Primary (outcome) | Confidence delta | (Day 30 score) − (Day 0 score) per user | Direct measure of the product's core promise |
| Leading indicator | Explanations per active user/week | Total explanations / WAU in that week | Reveals whether users return to the tool repeatedly |
| Leading indicator | Day-7 retention | Users active in days 1–7 who return in days 8–14 | Early churn signal before 30-day outcome data is available |
| Guardrail | Explanation flag rate | % of explanations flagged "this is wrong" by user | Protects trust in content quality; trigger at >5% |
| Guardrail | Survey abandonment | % of day-14/day-30 survey prompts dismissed | If >60%, our confidence data becomes unreliable |
| Guardrail | Support contact rate | Support tickets / MAU | Caps at 8%; above that means UX is broken |

---

## Instrumentation Plan

All events fire client-side via the analytics SDK and are stored in `techbridge_events` in Snowflake.

| Event | Trigger | Key Properties |
|-------|---------|---------------|
| `user_signed_up` | Account creation complete | `user_id`, `seniority` (junior/mid/senior), `company_size`, `source` (utm_source), `has_cs_degree` |
| `survey_submitted` | User completes confidence survey | `user_id`, `survey_day` (0/14/30), `confidence_score` (1–5), `sub_scores` (5 dimensions JSON) |
| `explanation_generated` | User receives an explanation | `user_id`, `session_id`, `input_type` (slack_msg/ticket/design_doc/other), `input_char_count`, `category_detected` (estimation/architecture/debt/requirements/other) |
| `explanation_rated` | User submits thumbs up/down or flags | `explanation_id`, `rating` (helpful/unhelpful/inaccurate), `user_id` |
| `concept_viewed` | User opens a concept library entry | `user_id`, `concept_id`, `concept_tag`, `referrer` (search/browse/explanation_link) |
| `concept_bookmarked` | User saves a concept | `user_id`, `concept_id` |
| `workflow_guide_started` | User opens a workflow guide | `user_id`, `guide_id`, `guide_name` |
| `workflow_guide_completed` | User reaches end of guide | `user_id`, `guide_id`, `completion_pct` |
| `session_start` / `session_end` | Session boundary | `user_id`, `session_id`, `platform` (web/mobile), `duration_sec` |

---

## Experiment Readiness (for validation experiment)

- **Baseline stable?** No — pre-launch, no historical baseline. Requires 2 weeks of soft-launch data before the experiment confidence metrics are meaningful.
- **MDE at current traffic**: With 200 signups (100/100 split), we can detect a 0.8-point confidence lift with 80% power at α=0.05. Smaller lifts (< 0.5 pts) require ≥400 users per arm.
- **Recommended experiment duration**: 30 days minimum (confidence surveys at day 0, 14, 30). Do not call the experiment early.
- **Confound risks**:
  - Novelty effect — users rate confidence higher because the tool is new, not because they learned. Mitigation: weight day-30 score more heavily than day-14 in analysis.
  - Social desirability bias — PMs over-report confidence improvement. Mitigation: include a behavioral proxy (# of technical questions asked in the tool, concept bookmark rate) to cross-validate.

---

## Key SQL

```sql
-- North Star: Monthly Technically Fluent PMs
WITH usage AS (
  SELECT
    user_id,
    DATE_TRUNC('month', event_time) AS month,
    COUNT(*) AS explanations_generated
  FROM techbridge_events
  WHERE event_type = 'explanation_generated'
  GROUP BY 1, 2
),
confidence AS (
  SELECT
    user_id,
    DATE_TRUNC('month', event_time) AS month,
    MAX(confidence_score) AS latest_confidence
  FROM techbridge_events
  WHERE event_type = 'survey_submitted'
  GROUP BY 1, 2
)
SELECT
  u.month,
  COUNT(DISTINCT u.user_id) AS mtfp
FROM usage u
JOIN confidence c USING (user_id, month)
WHERE u.explanations_generated >= 3
  AND c.latest_confidence >= 3.5
GROUP BY 1
ORDER BY 1;
```

```sql
-- Confidence delta per cohort (30-day change)
SELECT
  s0.user_id,
  s0.confidence_score AS day_0_score,
  s30.confidence_score AS day_30_score,
  s30.confidence_score - s0.confidence_score AS confidence_delta
FROM techbridge_events s0
JOIN techbridge_events s30 USING (user_id)
WHERE s0.event_type = 'survey_submitted' AND s0.survey_day = 0
  AND s30.event_type = 'survey_submitted' AND s30.survey_day = 30;
```

```sql
-- Weekly retention funnel
SELECT
  week_number,
  COUNT(DISTINCT user_id) AS active_users,
  COUNT(DISTINCT user_id) / FIRST_VALUE(COUNT(DISTINCT user_id)) OVER (ORDER BY week_number) AS retention_rate
FROM (
  SELECT user_id, DATEDIFF('week', MIN(event_time) OVER (PARTITION BY user_id), event_time) AS week_number
  FROM techbridge_events
  WHERE event_type = 'session_start'
)
GROUP BY 1
ORDER BY 1;
```

---

## Data Risks

1. **Survey response rate below 50%**: Confidence metric becomes unreliable. Mitigation: enforce in-app survey prompt on day 14/30 login; gate a feature (e.g., bookmarks) behind survey completion without making it feel coercive.
2. **Explanation flag rate spikes early**: Claude-generated explanations may be confidently wrong in niche technical areas. Mitigation: weekly manual spot-check of 20 flagged explanations; editorial review queue before scaling content.
3. **Seniority data missing**: Without seniority at signup, we can't segment confidence gains by experience level, which is a key open question from the PRD. Mitigation: make seniority a required signup field (3 options, not free text).
4. **Mobile vs. web session stitching**: PMs may sign up on desktop and use on mobile. If sessions aren't stitched by `user_id`, we'll undercount engagement. Mitigation: require login (no anonymous sessions); ensure SDK fires on both platforms with the same `user_id`.
