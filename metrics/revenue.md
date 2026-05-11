# Revenue Metrics

## Metrics Overview

| Metric | Definition | Typical Reporting Cadence |
|--------|------------|--------------------------|
| MRR | Total monthly recurring revenue | Monthly (daily for fast-growth) |
| ARR | MRR × 12 | Monthly |
| New MRR | MRR from new customers this period | Monthly |
| Expansion MRR | MRR added from existing customers (upsell/cross-sell) | Monthly |
| Contraction MRR | MRR lost from downgrades (not full churn) | Monthly |
| Churned MRR | MRR lost from full cancellations | Monthly |
| Net New MRR | New + Expansion − Contraction − Churned | Monthly |
| ACV | Annual contract value per customer | Deal / Monthly |
| LTV | Predicted lifetime revenue per customer | Quarterly |
| LTV:CAC | Ratio of lifetime value to acquisition cost | Quarterly |

---

## Metric Definitions

### MRR Components (the MRR waterfall)
Track MRR as a waterfall every month:

```
Starting MRR
+ New MRR          (new customers)
+ Expansion MRR    (upsells, seat additions, plan upgrades)
- Contraction MRR  (downgrades, seat reductions)
- Churned MRR      (full cancellations)
= Ending MRR
```

**Pitfall**: Don't report only "net new MRR." Blending expansion and churn hides whether growth is healthy (new customers + expansion) or artificial (expansion masking high churn).

---

### ARR
`MRR × 12`

Only valid for true monthly recurring contracts. For annual contracts with variable months, sum the annualized value of each active contract instead.

**Pitfall**: Including one-time fees (implementation, professional services) in ARR inflates the number and obscures the true recurring baseline.

---

### LTV
`ARPA / Churn Rate` (simplified)

Where ARPA = average revenue per account per month, and Churn Rate = monthly logo churn rate.

**Example**: ARPA = $500/mo, monthly churn = 2% → LTV = $500 / 0.02 = $25,000

For a more accurate model: use a cohort-based LTV that accounts for expansion over time.

---

### LTV:CAC
`LTV / CAC`

The fundamental unit economics ratio. At 3:1 you're spending $1 to get $3 back — acceptable. At 5:1+ you may be underinvesting in growth. Below 2:1, the business model is under strain.

**Pitfall**: LTV:CAC is a lagging indicator — it takes 12–24+ months to validate. Use CAC payback period as the leading indicator (target: <12 months for SMB, <18 months for enterprise).

---

## Snowflake SQL

### MRR waterfall (last 6 months)
```sql
WITH monthly_mrr AS (
    SELECT
        snapshot_month,
        account_id,
        mrr,
        LAG(mrr) OVER (PARTITION BY account_id ORDER BY snapshot_month) AS prior_mrr
    FROM account_mrr_snapshots
    WHERE snapshot_month >= DATEADD(month, -7, DATE_TRUNC('month', CURRENT_DATE))
),
classified AS (
    SELECT
        snapshot_month,
        account_id,
        mrr,
        prior_mrr,
        CASE
            WHEN prior_mrr IS NULL AND mrr > 0        THEN 'new'
            WHEN prior_mrr = 0 AND mrr > 0            THEN 'resurrected'
            WHEN prior_mrr > 0 AND mrr = 0            THEN 'churned'
            WHEN mrr > prior_mrr                      THEN 'expansion'
            WHEN mrr < prior_mrr AND mrr > 0          THEN 'contraction'
            ELSE 'retained'
        END AS mrr_type,
        mrr - COALESCE(prior_mrr, 0)                  AS mrr_delta
    FROM monthly_mrr
)

SELECT
    snapshot_month,
    SUM(CASE WHEN mrr_type = 'new'         THEN mrr        ELSE 0 END) AS new_mrr,
    SUM(CASE WHEN mrr_type = 'expansion'   THEN mrr_delta  ELSE 0 END) AS expansion_mrr,
    SUM(CASE WHEN mrr_type = 'contraction' THEN mrr_delta  ELSE 0 END) AS contraction_mrr,
    SUM(CASE WHEN mrr_type = 'churned'     THEN -prior_mrr ELSE 0 END) AS churned_mrr,
    SUM(CASE WHEN mrr_type = 'resurrected' THEN mrr        ELSE 0 END) AS resurrected_mrr,
    new_mrr + expansion_mrr + contraction_mrr + churned_mrr + resurrected_mrr
                                                                        AS net_new_mrr
FROM classified
WHERE snapshot_month > DATEADD(month, -6, DATE_TRUNC('month', CURRENT_DATE))
GROUP BY 1
ORDER BY 1 DESC
;
```

### ARR and growth rate (monthly)
```sql
SELECT
    snapshot_month,
    SUM(mrr) * 12                           AS arr,
    LAG(SUM(mrr) * 12) OVER
        (ORDER BY snapshot_month)           AS prior_month_arr,
    ROUND((SUM(mrr) * 12 - LAG(SUM(mrr) * 12)
        OVER (ORDER BY snapshot_month))
        / NULLIF(LAG(SUM(mrr) * 12)
        OVER (ORDER BY snapshot_month), 0) * 100, 1)
                                            AS mom_growth_pct,
    LAG(SUM(mrr) * 12, 12) OVER
        (ORDER BY snapshot_month)           AS same_month_last_year_arr,
    ROUND((SUM(mrr) * 12 - LAG(SUM(mrr) * 12, 12)
        OVER (ORDER BY snapshot_month))
        / NULLIF(LAG(SUM(mrr) * 12, 12)
        OVER (ORDER BY snapshot_month), 0) * 100, 1)
                                            AS yoy_growth_pct
FROM account_mrr_snapshots
WHERE mrr > 0
GROUP BY 1
ORDER BY 1 DESC
;
```

### ARPA and estimated LTV by plan tier
```sql
WITH current_mrr AS (
    SELECT
        a.plan_tier,
        COUNT(DISTINCT a.account_id)        AS account_count,
        SUM(s.mrr)                          AS total_mrr,
        AVG(s.mrr)                          AS arpa
    FROM account_mrr_snapshots s
    JOIN accounts a ON s.account_id = a.account_id
    WHERE
        s.snapshot_month = DATE_TRUNC('month', CURRENT_DATE)
        AND s.mrr > 0
        AND a.is_internal = FALSE
    GROUP BY 1
),
churn_rates AS (
    SELECT
        a.plan_tier,
        COUNT(CASE WHEN a.churned_at >= DATEADD(month,-1,DATE_TRUNC('month',CURRENT_DATE))
                    AND a.churned_at < DATE_TRUNC('month', CURRENT_DATE)
                   THEN 1 END) * 1.0
        / NULLIF(COUNT(CASE WHEN a.created_at < DATEADD(month,-1,DATE_TRUNC('month',CURRENT_DATE))
                            THEN 1 END), 0)     AS monthly_churn_rate
    FROM accounts a
    WHERE is_internal = FALSE
    GROUP BY 1
)

SELECT
    m.plan_tier,
    m.account_count,
    ROUND(m.arpa, 0)                                            AS arpa_monthly,
    ROUND(cr.monthly_churn_rate * 100, 2)                       AS monthly_churn_pct,
    ROUND(m.arpa / NULLIF(cr.monthly_churn_rate, 0), 0)         AS estimated_ltv
FROM current_mrr m
LEFT JOIN churn_rates cr USING (plan_tier)
ORDER BY estimated_ltv DESC
;
```
