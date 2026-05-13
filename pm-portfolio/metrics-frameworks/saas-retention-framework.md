# SaaS Retention Framework — Pulse

## Why Retention Analysis Is Different from Engagement Analysis

Engagement metrics tell you what's happening this week. Retention tells you whether it's compounding. A product with high weekly engagement but flat retention is a treadmill — you're generating activity but not building a habit. For Pulse, the goal isn't that a manager opens the digest once; it's that opening the digest every Monday becomes automatic.

Retention analysis starts with cohorts, not averages. Averages hide the shape of the curve.

---

## Cohort Retention Table Template

Track weekly cohorts by signup week. Columns = weeks since signup. Cells = % of cohort still digest-active.

| Cohort | W0 | W1 | W2 | W3 | W4 | W6 | W8 | W10 | W12 |
|--------|----|----|----|----|----|----|-----|-----|-----|
| Jan W1 | 100% | 71% | 58% | 51% | 48% | 44% | 41% | 40% | 39% |
| Jan W2 | 100% | 69% | 55% | 49% | 46% | 42% | 39% | — | — |
| Jan W3 | 100% | 73% | 59% | 52% | 49% | 45% | — | — | — |
| Feb W1 | 100% | 68% | 53% | 44% | 41% | — | — | — | — |
| Feb W2 | 100% | 65% | 50% | — | — | — | — | — | — |

*(Example values — replace with actuals from Snowflake query below)*

**What to look for in the shape:**
- The W0→W1 drop reveals onboarding effectiveness
- The W2→W4 slope reveals whether value was delivered before the habit window closed
- The W8+ floor reveals true product-market fit retention — the "smile" flattening

---

## How to Read a Retention Curve

**B2B SaaS benchmarks (weekly digest-based product):**

| Retention Point | Weak | Acceptable | Strong |
|---|---|---|---|
| Week 1 | < 50% | 55–65% | > 70% |
| Week 4 | < 30% | 40–50% | > 55% |
| Week 8 | < 25% | 35–45% | > 50% |
| Week 12 (floor) | < 20% | 30–40% | > 45% |

For context: good SMB SaaS typically retains 40%+ at week 8. Pulse's current 30-day (roughly week 4) retention of 64% is strong on its face — but 30-day retention is measured against all accounts, not against the subset that reached first insight. Adjusting for TTV lag, effective week-4 retention for *activated* accounts may look weaker than 64%.

---

## The 3 Retention Failure Modes

### Failure Mode 1: Bad Fit — Drop in Weeks 1–2

**Pattern**: W0→W2 retention collapses to < 40%. The curve starts steep.

**Cause**: The manager signed up but didn't match the ICP. Their Jira setup is too custom for Pulse's ingestion layer, or they own a team of 3 engineers where sprint predictability isn't a pain point, or sales oversold the use case.

**Fix**: Improve ICP qualification pre-signup; add a fit-check during onboarding that surfaces a warning before the manager invests setup time.

### Failure Mode 2: Value Gap — Drop in Weeks 3–6

**Pattern**: W1 retention looks decent (60%+), but the curve drops sharply between weeks 3 and 6. Managers explore, don't find sustained value, leave.

**Cause**: The product delivered a first impression but not a habit-forming value loop. Recommendations were too generic. The digest felt repetitive by week 3. The manager didn't see anything they couldn't see in Jira.

**Fix**: Increase recommendation specificity; introduce new digest signal types in weeks 3–5 (e.g., trend-over-time alerts, peer benchmarking) to maintain novelty during the critical habit window.

### Failure Mode 3: Habit Not Formed — Drop in Weeks 6–12

**Pattern**: Retention holds through week 6 but then gradually erodes rather than flattening. No stable floor.

**Cause**: Value was delivered, but it wasn't anchored to a recurring behavior. The manager used Pulse reactively when there was a problem, not proactively as a weekly habit. The digest was relevant but not *expected*.

**Fix**: Introduce behavioral anchoring — connect digest delivery to an existing ritual (Monday standup prep; sprint review); add social proof ("3 other managers on your team read this week's digest").

---

## Pulse Hypothesis: Which Failure Mode Are We In?

The evidence points to **Failure Mode 2 (Value Gap)**, driven by a pre-cursor problem in activation.

With TTV at 8 days, many managers receive their first digest before they've seen their first insight. This means the digest is sending recommendations based on incomplete data and managers are evaluating Pulse's value before the product has had a chance to demonstrate it. The week-3 to week-6 drop isn't primarily a recommendation relevance problem — it's that the manager's trust threshold was never cleared in week 1.

**The intervention**: Fix TTV first. Get managers to their first insight before the first digest arrives. Then focus on recommendation specificity for weeks 3–6 retention.

*Prediction*: If TTV drops to 3 days, week-4 retention improves by 8–12pp. Retention at week 8 follows by ~4–6pp with a 6-week lag.

---

## SQL: Cohort Retention Query (Snowflake)

```sql
-- Pulse cohort retention: digest-active rate by week since signup
-- Schema: pulse_analytics
-- Tables: users, accounts, digest_sends, events

WITH cohorts AS (
    SELECT
        u.user_id,
        u.account_id,
        DATE_TRUNC('week', u.created_at) AS cohort_week,
        u.created_at AS signup_ts
    FROM pulse_analytics.users u
    JOIN pulse_analytics.accounts a
        ON u.account_id = a.account_id
    WHERE u.role = 'manager'
      AND a.is_icp = TRUE
      AND u.created_at >= '2025-10-01'   -- adjust lookback window
),

digest_activity AS (
    SELECT
        ds.user_id,
        ds.sent_at,
        -- digest-active = opened AND took an action
        MAX(CASE WHEN ds.opened = TRUE
                  AND EXISTS (
                      SELECT 1
                      FROM pulse_analytics.events e
                      WHERE e.user_id = ds.user_id
                        AND e.event_type IN ('insight_click', 'recommendation_action', 'digest_cta_click')
                        AND e.occurred_at BETWEEN ds.sent_at AND DATEADD('day', 7, ds.sent_at)
                  )
             THEN 1 ELSE 0 END) AS is_digest_active
    FROM pulse_analytics.digest_sends ds
    GROUP BY ds.user_id, ds.sent_at
),

weekly_activity AS (
    SELECT
        c.user_id,
        c.cohort_week,
        DATEDIFF('week', c.cohort_week, DATE_TRUNC('week', da.sent_at)) AS weeks_since_signup,
        MAX(da.is_digest_active) AS active_this_week
    FROM cohorts c
    JOIN digest_activity da ON c.user_id = da.user_id
    GROUP BY c.user_id, c.cohort_week, weeks_since_signup
)

SELECT
    cohort_week,
    COUNT(DISTINCT user_id)                                        AS cohort_size,
    -- Retention by week
    AVG(CASE WHEN weeks_since_signup = 1 THEN active_this_week END) AS w1_retention,
    AVG(CASE WHEN weeks_since_signup = 2 THEN active_this_week END) AS w2_retention,
    AVG(CASE WHEN weeks_since_signup = 4 THEN active_this_week END) AS w4_retention,
    AVG(CASE WHEN weeks_since_signup = 6 THEN active_this_week END) AS w6_retention,
    AVG(CASE WHEN weeks_since_signup = 8 THEN active_this_week END) AS w8_retention,
    AVG(CASE WHEN weeks_since_signup = 12 THEN active_this_week END) AS w12_retention
FROM weekly_activity
GROUP BY cohort_week
ORDER BY cohort_week ASC;
```

**Notes on this query:**
- `is_icp = TRUE` filters to accounts matching the ICP definition — without this, bad-fit churn pollutes the cohort analysis
- The `is_digest_active` definition matches the north star: opened + downstream action, not just open
- Run at account level (aggregate `MAX(active_this_week)` by `account_id`) to get account-level retention for CS reporting; keep at user level for product analysis
- Extend the `weeks_since_signup` range to 24 for annual cohort views
