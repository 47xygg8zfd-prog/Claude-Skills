# Engagement Metrics

## Metrics Overview

| Metric | Definition | Typical Reporting Cadence |
|--------|------------|--------------------------|
| DAU | Distinct users with qualifying activity on a given day | Daily |
| WAU | Distinct users with qualifying activity in a rolling 7-day window | Weekly |
| MAU | Distinct users with qualifying activity in a rolling 28-day window | Monthly |
| DAU/MAU (stickiness) | Ratio of daily to monthly actives — habit formation proxy | Weekly |
| Feature adoption rate | % of active accounts using a given feature | Weekly |
| Session depth | Median meaningful actions per session | Weekly |
| Power users | % of users in the top engagement decile | Monthly |

---

## Metric Definitions

### DAU / WAU / MAU
Count of distinct users who performed at least one **qualifying action** in the window.

**Define "qualifying action" explicitly.** Passive events (email opens, page loads from a redirect) should not count. Meaningful actions (dashboard load, filter applied, export, comment posted) should.

**Pitfall**: Don't count internal users (`is_internal = TRUE`), deactivated users, or bot traffic.

---

### Stickiness (DAU/MAU)
`DAU / MAU` — measures what fraction of monthly users engage daily.

A stickiness of 0.20 means the average monthly active user comes back on 20% of days (about once per week). A stickiness of 0.50+ indicates daily habit formation.

**Benchmark (B2B SaaS)**: 0.15–0.25 is typical for a weekly-use work tool. Consumer apps aim higher (0.40+). Compare within your category, not against consumer benchmarks.

**Pitfall**: Stickiness is artificially high when MAU is low (early stage). Focus on trends over time, not absolute values.

---

### Feature Adoption Rate
`accounts_using_feature_at_least_once_in_period / total_active_accounts`

Measure at the **account** level for B2B — one power user on a team doesn't mean the feature is adopted.

**Pitfall**: "Ever used" overstates adoption. Use a rolling 30-day window. A feature used once in 6 months isn't adopted.

---

### Session Depth
Median number of distinct meaningful event types per session. Tracks whether users are doing more than one thing per visit.

A session with depth 1 (land → look at one thing → leave) is a sign of narrow habit or poor navigation. Depth 3+ suggests the product is becoming a workflow tool.

---

## Snowflake SQL

### WAU and stickiness trend (last 12 weeks)
```sql
WITH daily_active AS (
    SELECT
        e.event_timestamp::DATE         AS activity_date,
        e.user_id
    FROM events e
    JOIN users u ON e.user_id = u.user_id
    JOIN accounts a ON u.account_id = a.account_id
    WHERE
        e.event_type IN ('dashboard_load','filter_applied','export',
                         'comment_posted','report_created')
        AND a.is_internal = FALSE
        AND e.event_timestamp >= DATEADD(day, -90, CURRENT_DATE)
),
weekly AS (
    SELECT
        DATE_TRUNC('week', d.activity_date)     AS week_start,
        COUNT(DISTINCT d.user_id)               AS wau
    FROM daily_active d
    GROUP BY 1
),
monthly AS (
    SELECT
        DATE_TRUNC('week', d.activity_date)     AS week_start,
        COUNT(DISTINCT d.user_id)               AS mau_rolling_28
    FROM daily_active d
    WHERE d.activity_date >= DATEADD(day, -28, DATE_TRUNC('week', d.activity_date))
    GROUP BY 1
)

SELECT
    w.week_start,
    w.wau,
    m.mau_rolling_28,
    ROUND(w.wau / NULLIF(m.mau_rolling_28, 0), 3)  AS stickiness
FROM weekly w
JOIN monthly m USING (week_start)
ORDER BY 1 DESC
;
```

### Feature adoption rate (last 30 days)
```sql
WITH active_accounts AS (
    SELECT DISTINCT u.account_id
    FROM events e
    JOIN users u ON e.user_id = u.user_id
    JOIN accounts a ON u.account_id = a.account_id
    WHERE e.event_timestamp >= DATEADD(day, -30, CURRENT_DATE)
      AND a.is_internal = FALSE
),
feature_users AS (
    SELECT DISTINCT u.account_id
    FROM events e
    JOIN users u ON e.user_id = u.user_id
    WHERE e.event_type = 'weekly_digest_opened'  -- replace with your feature event
      AND e.event_timestamp >= DATEADD(day, -30, CURRENT_DATE)
)

SELECT
    COUNT(DISTINCT aa.account_id)                           AS active_accounts,
    COUNT(DISTINCT fu.account_id)                           AS feature_accounts,
    ROUND(COUNT(DISTINCT fu.account_id) * 100.0
        / NULLIF(COUNT(DISTINCT aa.account_id), 0), 1)     AS adoption_rate_pct
FROM active_accounts aa
LEFT JOIN feature_users fu USING (account_id)
;
```

### Session depth distribution
```sql
WITH sessions AS (
    SELECT
        s.session_id,
        u.account_id,
        COUNT(DISTINCT e.event_type)    AS distinct_event_types
    FROM sessions s
    JOIN users u ON s.user_id = u.user_id
    JOIN accounts a ON u.account_id = a.account_id
    JOIN events e ON s.session_id = e.session_id
        AND e.event_type NOT IN ('page_view','session_start','session_end')
    WHERE
        s.started_at >= DATEADD(day, -30, CURRENT_DATE)
        AND a.is_internal = FALSE
    GROUP BY 1, 2
)

SELECT
    MEDIAN(distinct_event_types)                                    AS median_session_depth,
    PERCENTILE_CONT(0.25) WITHIN GROUP
        (ORDER BY distinct_event_types)                             AS p25_depth,
    PERCENTILE_CONT(0.75) WITHIN GROUP
        (ORDER BY distinct_event_types)                             AS p75_depth,
    COUNT(CASE WHEN distinct_event_types = 1 THEN 1 END) * 100.0
        / COUNT(*)                                                  AS pct_single_action_sessions
FROM sessions
;
```
