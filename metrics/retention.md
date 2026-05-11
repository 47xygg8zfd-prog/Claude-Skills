# Retention Metrics

## Metrics Overview

| Metric | Definition | Typical Reporting Cadence |
|--------|------------|--------------------------|
| Logo churn rate | % of accounts that churned in a period | Monthly |
| Revenue churn rate | % of MRR lost to churn in a period | Monthly |
| Net Revenue Retention (NRR) | MRR retained + expansion / starting MRR | Monthly |
| Cohort retention curve | % of a signup cohort still active at N months | Monthly (cohort) |
| Resurrection rate | % of churned users who reactivate | Monthly |
| At-risk accounts | Accounts with declining engagement signals | Weekly |

---

## Metric Definitions

### Logo Churn Rate
`accounts_churned_in_period / accounts_at_start_of_period`

**Pitfall**: Don't include accounts that churned and then re-subscribed — count them separately as resurrections. Double-counting inflates churn.

**Benchmark (B2B SaaS)**: <5% annual logo churn is strong. 10–15% is average. Above 20% signals a retention problem that will compound.

---

### Revenue Churn Rate
`MRR_lost_to_churn / MRR_at_start_of_period`

Distinguish **gross revenue churn** (lost MRR only) from **net revenue churn** (lost MRR minus expansion MRR). Always report both — companies can hide logo churn behind expansion revenue.

**Benchmark**: <1% monthly gross revenue churn (<12% annual) is healthy for B2B SaaS. Negative net churn (expansion > churn) is the goal at scale.

---

### Net Revenue Retention (NRR)
`(starting_MRR - churned_MRR - contracted_MRR + expansion_MRR) / starting_MRR`

The single most important retention metric for B2B SaaS. An NRR > 100% means the business grows even with zero new customer acquisition.

**Benchmark**: 100–110% is good, 120%+ is excellent (common in best-in-class enterprise SaaS), <90% means you're leaking a bucket.

---

### Cohort Retention Curve
For each monthly signup cohort: what % of accounts are still active (paying or engaging) at month 1, 2, 3... N?

Plot these curves overlaid — improving retention shows up as newer cohort curves sitting higher than older ones.

**Pitfall**: Define "active" consistently. For revenue retention: still paying. For product retention: logged in within the month. These tell different stories.

---

### At-Risk Accounts
Accounts showing early warning signals before churn:
- WAU dropped >40% vs. prior 4-week average
- No login in 14+ days (for a tool used weekly)
- Support ticket volume spike
- Key user (admin) went inactive

Proactive CS outreach to at-risk accounts is the highest-ROI retention intervention.

---

## Snowflake SQL

### Monthly logo churn rate
```sql
WITH monthly_base AS (
    SELECT
        DATE_TRUNC('month', CURRENT_DATE)   AS month,
        COUNT(*)                             AS accounts_at_start
    FROM accounts
    WHERE
        created_at < DATE_TRUNC('month', CURRENT_DATE)
        AND (churned_at IS NULL OR churned_at >= DATE_TRUNC('month', CURRENT_DATE))
        AND is_internal = FALSE
),
churned AS (
    SELECT COUNT(*) AS accounts_churned
    FROM accounts
    WHERE
        churned_at >= DATE_TRUNC('month', CURRENT_DATE)
        AND churned_at < DATEADD(month, 1, DATE_TRUNC('month', CURRENT_DATE))
        AND is_internal = FALSE
)

SELECT
    mb.month,
    mb.accounts_at_start,
    c.accounts_churned,
    ROUND(c.accounts_churned * 100.0 / NULLIF(mb.accounts_at_start, 0), 2)
        AS logo_churn_rate_pct
FROM monthly_base mb, churned c
;
```

### Net Revenue Retention (trailing 12 months)
```sql
WITH mrr_12mo_ago AS (
    SELECT
        account_id,
        mrr AS starting_mrr
    FROM account_mrr_snapshots
    WHERE snapshot_month = DATEADD(month, -12, DATE_TRUNC('month', CURRENT_DATE))
      AND mrr > 0
),
mrr_current AS (
    SELECT
        account_id,
        mrr AS current_mrr
    FROM account_mrr_snapshots
    WHERE snapshot_month = DATE_TRUNC('month', CURRENT_DATE)
)

SELECT
    SUM(s.starting_mrr)                                         AS starting_mrr,
    SUM(COALESCE(c.current_mrr, 0))                             AS retained_mrr,
    SUM(GREATEST(COALESCE(c.current_mrr, 0) - s.starting_mrr, 0))  AS expansion_mrr,
    SUM(GREATEST(s.starting_mrr - COALESCE(c.current_mrr, 0), 0))  AS churned_mrr,
    ROUND(SUM(COALESCE(c.current_mrr, 0)) * 100.0
        / NULLIF(SUM(s.starting_mrr), 0), 1)                   AS nrr_pct
FROM mrr_12mo_ago s
LEFT JOIN mrr_current c USING (account_id)
;
```

### Cohort retention curve (monthly, last 6 cohorts)
```sql
WITH cohorts AS (
    SELECT
        account_id,
        DATE_TRUNC('month', created_at)     AS cohort_month
    FROM accounts
    WHERE is_internal = FALSE
      AND created_at >= DATEADD(month, -7, DATE_TRUNC('month', CURRENT_DATE))
),
monthly_active AS (
    SELECT DISTINCT
        u.account_id,
        DATE_TRUNC('month', e.event_timestamp)  AS active_month
    FROM events e
    JOIN users u ON e.user_id = u.user_id
),
retention AS (
    SELECT
        c.cohort_month,
        DATEDIFF(month, c.cohort_month, ma.active_month)    AS months_since_signup,
        COUNT(DISTINCT c.account_id)                         AS retained_accounts
    FROM cohorts c
    LEFT JOIN monthly_active ma ON c.account_id = ma.account_id
    WHERE ma.active_month >= c.cohort_month
    GROUP BY 1, 2
),
cohort_sizes AS (
    SELECT cohort_month, COUNT(*) AS cohort_size
    FROM cohorts
    GROUP BY 1
)

SELECT
    r.cohort_month,
    r.months_since_signup,
    cs.cohort_size,
    r.retained_accounts,
    ROUND(r.retained_accounts * 100.0 / NULLIF(cs.cohort_size, 0), 1)
        AS retention_rate_pct
FROM retention r
JOIN cohort_sizes cs USING (cohort_month)
ORDER BY 1, 2
;
```

### At-risk accounts (engagement drop signal)
```sql
WITH recent_wau AS (
    SELECT
        u.account_id,
        COUNT(DISTINCT CASE
            WHEN e.event_timestamp >= DATEADD(day, -7, CURRENT_DATE)
            THEN e.user_id END)             AS wau_last_7d,
        COUNT(DISTINCT CASE
            WHEN e.event_timestamp BETWEEN DATEADD(day, -35, CURRENT_DATE)
                                       AND DATEADD(day, -8, CURRENT_DATE)
            THEN e.user_id END) / 4.0       AS avg_wau_prior_4wk
    FROM events e
    JOIN users u ON e.user_id = u.user_id
    JOIN accounts a ON u.account_id = a.account_id
    WHERE
        e.event_timestamp >= DATEADD(day, -35, CURRENT_DATE)
        AND a.is_internal = FALSE
        AND a.churned_at IS NULL
    GROUP BY 1
)

SELECT
    a.account_id,
    a.account_name,
    a.plan_tier,
    a.cs_owner,
    r.wau_last_7d,
    ROUND(r.avg_wau_prior_4wk, 1)           AS avg_wau_prior_4wk,
    ROUND((r.wau_last_7d - r.avg_wau_prior_4wk)
        / NULLIF(r.avg_wau_prior_4wk, 0) * 100, 0) AS wau_change_pct
FROM recent_wau r
JOIN accounts a USING (account_id)
WHERE
    r.avg_wau_prior_4wk > 0
    AND r.wau_last_7d < r.avg_wau_prior_4wk * 0.6  -- dropped >40%
ORDER BY wau_change_pct ASC
;
```
