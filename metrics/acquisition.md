# Acquisition Metrics

## Metrics Overview

| Metric | Definition | Typical Reporting Cadence |
|--------|------------|--------------------------|
| New signups | Distinct new accounts created | Daily / Weekly |
| Signup conversion rate | Signups / unique visitors to signup page | Weekly |
| Lead-to-trial conversion | Trials started / marketing qualified leads | Weekly |
| Trial-to-paid conversion | Paid accounts / trials started (same cohort) | Monthly (cohort) |
| CAC | Total sales + marketing spend / new customers acquired | Monthly |
| CAC payback period | CAC / (ACV / 12) | Quarterly |
| Channel mix | % of signups by acquisition source | Weekly |

---

## Metric Definitions

### New Signups
Accounts where `created_at` falls within the period. Count at the **account** level, not the user level — one company signing up is one signup regardless of seat count.

**Pitfall**: Don't include internal test accounts (`is_internal = TRUE`) or accounts created by your sales team on behalf of customers without genuine intent.

---

### Signup Conversion Rate
`signups / unique_visitors_to_signup_page`

**Pitfall**: Use unique visitors, not sessions. One person visiting the signup page 3 times and converting counts as 1 conversion from 1 visitor, not 33%.

**Benchmark (B2B SaaS)**: 2–5% visitor-to-trial is typical. Above 8% suggests strong intent-based traffic or a very simple signup flow.

---

### Trial-to-Paid Conversion
Measure as a cohort: of accounts that started a trial in month M, what % converted to paid by M+1 (or M+3 for longer sales cycles)?

**Pitfall**: Don't measure this as "paid conversions this month / trials active this month" — that mixes cohorts and overstates conversion during growth periods.

**Benchmark (B2B SaaS PLG)**: 15–25% trial-to-paid within 30 days is healthy. Below 10% usually signals an activation problem, not an acquisition problem.

---

### CAC
`(sales_spend + marketing_spend) / new_customers_acquired`

Calculate blended CAC (all channels) and by-channel CAC separately. Blended hides channel efficiency; by-channel hides shared overhead.

**Pitfall**: Use the same time period for spend and customers — but offset for sales cycle length. If your average sales cycle is 45 days, attribute this month's customers to spend from 45 days ago.

---

## Snowflake SQL

### New signups by week
```sql
SELECT
    DATE_TRUNC('week', created_at)  AS week_start,
    plan_tier,
    COUNT(*)                         AS new_accounts
FROM accounts
WHERE
    created_at >= DATEADD(day, -90, CURRENT_DATE)
    AND is_internal = FALSE
    AND is_test = FALSE
GROUP BY 1, 2
ORDER BY 1 DESC, 2
;
```

### Trial-to-paid conversion by cohort (30-day window)
```sql
WITH trials AS (
    SELECT
        account_id,
        DATE_TRUNC('month', trial_started_at)   AS cohort_month,
        trial_started_at,
        converted_at
    FROM accounts
    WHERE trial_started_at IS NOT NULL
      AND is_internal = FALSE
)

SELECT
    cohort_month,
    COUNT(*)                                                        AS trials_started,
    COUNT(CASE WHEN converted_at <= DATEADD(day, 30, trial_started_at)
               THEN 1 END)                                          AS converted_30d,
    ROUND(converted_30d / NULLIF(trials_started, 0) * 100, 1)      AS conversion_rate_pct
FROM trials
WHERE cohort_month <= DATEADD(month, -1, DATE_TRUNC('month', CURRENT_DATE))
GROUP BY 1
ORDER BY 1 DESC
;
```

### Signups by acquisition channel (last 30 days)
```sql
SELECT
    COALESCE(utm_source, 'direct / unknown')    AS channel,
    COUNT(DISTINCT account_id)                   AS new_accounts,
    ROUND(COUNT(DISTINCT account_id) * 100.0
        / SUM(COUNT(DISTINCT account_id)) OVER(), 1) AS pct_of_total
FROM accounts
WHERE
    created_at >= DATEADD(day, -30, CURRENT_DATE)
    AND is_internal = FALSE
GROUP BY 1
ORDER BY 2 DESC
;
```
