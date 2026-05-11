---
name: data-queries
description: >
  Generate, explain, debug, and optimize Snowflake SQL and Splunk SPL queries for product and
  business analysis. Use this skill whenever the user wants to query data, write SQL, write SPL,
  analyze logs, build a report from raw data, or understand query results. Also trigger for phrases
  like "write me a query for", "how do I query X in Snowflake", "Splunk search for", "debug this SQL",
  "explain what this query does", "help me find X in our logs", or "run this against our data".
  Produces ready-to-run queries with explanations tailored for a PM audience.
---

# Data Queries Skill

Generate, explain, and debug Snowflake SQL and Splunk SPL queries — optimized for PM-level analysis.

---

## Platform Detection

**Snowflake** → Use SQL with Snowflake-specific functions
**Splunk** → Use SPL (Search Processing Language)

If unclear, ask: "Are you querying Snowflake (structured data/warehouse) or Splunk (logs/events)?"

---

## Snowflake SQL

### Common PM Query Patterns

#### Daily Active Users (DAU)
```sql
SELECT
  DATE_TRUNC('day', event_timestamp) AS day,
  COUNT(DISTINCT user_id) AS dau
FROM events
WHERE event_timestamp >= DATEADD('day', -30, CURRENT_DATE)
GROUP BY 1
ORDER BY 1;
```

#### Feature Adoption Rate
```sql
SELECT
  DATE_TRUNC('week', first_used_at) AS cohort_week,
  COUNT(DISTINCT user_id) AS users_adopted,
  ROUND(COUNT(DISTINCT user_id) / total_users.total * 100, 2) AS adoption_pct
FROM feature_usage
CROSS JOIN (SELECT COUNT(DISTINCT user_id) AS total FROM users WHERE is_active = TRUE) total_users
GROUP BY 1, total_users.total
ORDER BY 1;
```

#### Funnel Analysis
```sql
SELECT
  COUNT(DISTINCT CASE WHEN step = 'view_product' THEN user_id END) AS step_1_view,
  COUNT(DISTINCT CASE WHEN step = 'add_to_cart' THEN user_id END) AS step_2_cart,
  COUNT(DISTINCT CASE WHEN step = 'checkout_start' THEN user_id END) AS step_3_checkout,
  COUNT(DISTINCT CASE WHEN step = 'purchase_complete' THEN user_id END) AS step_4_purchase
FROM funnel_events
WHERE event_date >= DATEADD('day', -7, CURRENT_DATE);
```

#### Retention Cohort (Week-over-Week)
```sql
WITH cohorts AS (
  SELECT
    user_id,
    DATE_TRUNC('week', MIN(created_at)) AS cohort_week
  FROM users
  GROUP BY 1
),
activity AS (
  SELECT DISTINCT
    user_id,
    DATE_TRUNC('week', event_timestamp) AS active_week
  FROM events
)
SELECT
  c.cohort_week,
  DATEDIFF('week', c.cohort_week, a.active_week) AS weeks_since_signup,
  COUNT(DISTINCT c.user_id) AS retained_users
FROM cohorts c
JOIN activity a ON c.user_id = a.user_id
GROUP BY 1, 2
ORDER BY 1, 2;
```

#### Revenue by Segment
```sql
SELECT
  customer_segment,
  DATE_TRUNC('month', transaction_date) AS month,
  SUM(revenue) AS total_revenue,
  COUNT(DISTINCT customer_id) AS paying_customers,
  ROUND(SUM(revenue) / COUNT(DISTINCT customer_id), 2) AS arpu
FROM transactions
WHERE transaction_date >= DATEADD('month', -6, CURRENT_DATE)
GROUP BY 1, 2
ORDER BY 2, 1;
```

### Snowflake PM Tips
- Use `DATE_TRUNC('day'/'week'/'month', col)` for time bucketing
- Use `DATEADD('day', -N, CURRENT_DATE)` for rolling windows
- `COUNT(DISTINCT user_id)` for unique users, not `COUNT(*)`
- Use CTEs (`WITH`) to make complex queries readable
- Add `LIMIT 1000` when exploring to avoid accidentally scanning huge tables
- `EXPLAIN` before running expensive queries on large tables

---

## Splunk SPL

### Common PM Query Patterns

#### Error Rate by Service
```
index=app_logs level=ERROR
| timechart span=1h count BY service
| eval error_rate = count / total_requests * 100
```

#### Latency Percentiles
```
index=app_logs sourcetype=access_combined
| stats p50(response_time_ms) AS p50,
        p95(response_time_ms) AS p95,
        p99(response_time_ms) AS p99
  BY endpoint
| sort - p95
```

#### User Journey / Session Trace
```
index=app_logs user_id="u_12345"
| sort _time
| table _time, action, page, status_code, session_id
```

#### Feature Flag Usage
```
index=app_logs feature_flag="new_checkout"
| timechart span=1d
    count(eval(flag_value="enabled")) AS enabled_users,
    count(eval(flag_value="disabled")) AS control_users
```

#### 5xx Error Spike Detection
```
index=web_logs status>=500
| timechart span=5m count AS errors
| eval is_spike = if(errors > 100, "SPIKE", "normal")
| where is_spike="SPIKE"
```

#### Deployment Impact
```
index=app_logs
| eval deployment = if(_time >= relative_time(now(), "-2h"), "post_deploy", "pre_deploy")
| stats avg(response_time_ms) AS avg_latency,
        count(eval(status_code>=500)) AS errors
  BY deployment
```

### Splunk PM Tips
- Always filter by `index=` and `sourcetype=` first — it speeds up searches dramatically
- Use `| head 100` when exploring to preview results fast
- Time picker is your friend — use relative times like `-24h`, `-7d`, `-30d`
- `| stats count BY field` for quick distribution analysis
- `| timechart span=1h count` for any time-series visualization
- Save useful searches as Reports; share dashboards from there

---

## Explaining Queries to Stakeholders

When asked to explain a query, use this structure:

1. **What it answers**: Plain English question this query addresses
2. **Data sources**: Which tables/indexes and date range
3. **Key logic**: The main filter or calculation in plain language
4. **Caveats**: Any known limitations (sampling, null handling, timezone)

Example:
> This query counts unique users who logged in each day over the last 30 days. It pulls from the `events` table, filters to login events only, and deduplicates by user_id so each person only counts once per day. Note: this excludes users who authenticate via SSO — those are in a separate table.

---

## Query Debugging Checklist

When a query returns unexpected results:
- [ ] Check date filters — are timezone conversions correct?
- [ ] Verify `DISTINCT` — are you double-counting joins?
- [ ] Check for NULLs in key columns — may need `COALESCE`
- [ ] Validate row counts against known totals
- [ ] Check if filters are too aggressive (try removing one at a time)
- [ ] For Splunk: confirm the right `index` and `sourcetype`

---

## Integration Points
- Use **quicksight-dashboards** skill to turn query results into visualizations
- Use **monte-carlo** skill to model uncertainty in metric projections
