# Activation Metrics

## Metrics Overview

| Metric | Definition | Typical Reporting Cadence |
|--------|------------|--------------------------|
| Onboarding completion rate | % of new accounts completing the onboarding flow | Weekly |
| Time-to-first-value (TTFV) | Median days from signup to first "aha moment" event | Weekly |
| Aha moment event rate | % of new accounts reaching the defined aha moment | Weekly (cohort) |
| Setup completion rate | % of accounts completing key setup steps | Weekly |
| Day-1 / Day-7 retention | % of new users who return on day 1 / day 7 | Weekly (cohort) |

---

## Metric Definitions

### Onboarding Completion Rate
`accounts_completing_all_onboarding_steps / accounts_starting_onboarding`

**Pitfall**: Define "completion" precisely before measuring. "Viewed the last onboarding screen" is not the same as "completed the key setup action." Use a behavioral definition, not a UI state.

**Benchmark (B2B SaaS)**: 40–60% completion is common. Below 30% usually means the flow is too long or asks for something users don't have ready.

---

### Time-to-First-Value (TTFV)
Median (not mean) days between `account.created_at` and the first occurrence of your defined "aha moment" event.

Use median because a small number of accounts that never activate will skew the mean heavily. Median shows what a typical activating account experiences.

**Defining the aha moment**: The single event most correlated with 90-day retention. Run a retention correlation analysis on your event data to find it — don't guess.

**Benchmark**: Varies widely by product complexity. Simple PLG tools: <1 day. Complex B2B tools: 3–14 days is typical. If it's >30 days, activation is your biggest lever.

---

### Day-1 / Day-7 Retention
Of users who signed up on day 0, what % performed any meaningful action on day 1 / day 7?

**Pitfall**: Use "day N" windows, not "within N days." Day-1 retention = returned on calendar day 1 (24–48 hours after signup). "Used within 7 days" is a different (easier) metric.

**Benchmark (B2B SaaS)**: Day-1 >40%, Day-7 >25% is healthy for a tool used in a work context. Consumer benchmarks are much higher and don't apply.

---

## Snowflake SQL

### Onboarding completion rate by week
```sql
WITH onboarding AS (
    SELECT
        u.account_id,
        DATE_TRUNC('week', a.created_at)            AS cohort_week,
        MAX(CASE WHEN e.event_type = 'onboarding_step_1_complete'
                 THEN 1 ELSE 0 END)                 AS step_1,
        MAX(CASE WHEN e.event_type = 'onboarding_step_2_complete'
                 THEN 1 ELSE 0 END)                 AS step_2,
        MAX(CASE WHEN e.event_type = 'onboarding_step_3_complete'
                 THEN 1 ELSE 0 END)                 AS step_3
    FROM accounts a
    JOIN users u ON a.account_id = u.account_id
    LEFT JOIN events e
        ON u.user_id = e.user_id
        AND e.event_timestamp <= DATEADD(day, 14, a.created_at)
    WHERE
        a.created_at >= DATEADD(day, -90, CURRENT_DATE)
        AND a.is_internal = FALSE
    GROUP BY 1, 2
)

SELECT
    cohort_week,
    COUNT(*)                                            AS new_accounts,
    SUM(CASE WHEN step_1 = 1 AND step_2 = 1
              AND step_3 = 1 THEN 1 ELSE 0 END)        AS completed_onboarding,
    ROUND(completed_onboarding / NULLIF(COUNT(*), 0)
          * 100, 1)                                     AS completion_rate_pct
FROM onboarding
GROUP BY 1
ORDER BY 1 DESC
;
```

### Median time-to-first-value by cohort month
```sql
WITH aha_events AS (
    SELECT
        u.account_id,
        a.created_at                                    AS signup_date,
        DATE_TRUNC('month', a.created_at)               AS cohort_month,
        MIN(e.event_timestamp)                          AS first_aha_at
    FROM accounts a
    JOIN users u ON a.account_id = u.account_id
    JOIN events e ON u.user_id = e.user_id
        AND e.event_type = 'aha_moment_event'  -- replace with your event
    WHERE a.is_internal = FALSE
    GROUP BY 1, 2, 3
)

SELECT
    cohort_month,
    COUNT(*)                                            AS accounts_activated,
    MEDIAN(DATEDIFF(day, signup_date, first_aha_at))    AS median_days_to_value,
    PERCENTILE_CONT(0.75) WITHIN GROUP
        (ORDER BY DATEDIFF(day, signup_date, first_aha_at)) AS p75_days_to_value
FROM aha_events
GROUP BY 1
ORDER BY 1 DESC
;
```

### Day-1 and Day-7 retention by signup week
```sql
WITH signups AS (
    SELECT DISTINCT
        u.user_id,
        DATE_TRUNC('week', u.created_at)    AS cohort_week,
        u.created_at::DATE                  AS signup_date
    FROM users u
    JOIN accounts a ON u.account_id = a.account_id
    WHERE u.created_at >= DATEADD(day, -60, CURRENT_DATE)
      AND a.is_internal = FALSE
),
activity AS (
    SELECT DISTINCT user_id, event_timestamp::DATE AS active_date
    FROM events
    WHERE event_type NOT IN ('page_view')  -- exclude passive events
)

SELECT
    s.cohort_week,
    COUNT(DISTINCT s.user_id)                                           AS new_users,
    COUNT(DISTINCT CASE WHEN a1.active_date = DATEADD(day,1,s.signup_date)
                        THEN s.user_id END)                             AS day_1_retained,
    COUNT(DISTINCT CASE WHEN a7.active_date = DATEADD(day,7,s.signup_date)
                        THEN s.user_id END)                             AS day_7_retained,
    ROUND(day_1_retained / NULLIF(new_users,0) * 100, 1)               AS day_1_retention_pct,
    ROUND(day_7_retained / NULLIF(new_users,0) * 100, 1)               AS day_7_retention_pct
FROM signups s
LEFT JOIN activity a1
    ON s.user_id = a1.user_id
    AND a1.active_date = DATEADD(day, 1, s.signup_date)
LEFT JOIN activity a7
    ON s.user_id = a7.user_id
    AND a7.active_date = DATEADD(day, 7, s.signup_date)
WHERE s.cohort_week <= DATEADD(week, -1, DATE_TRUNC('week', CURRENT_DATE))
GROUP BY 1
ORDER BY 1 DESC
;
```
