# Example Output: QuickSight Dashboards Skill

**Prompt used:** "Design a QuickSight dashboard for tracking weekly digest adoption and engagement"

---

## Dashboard Design: Weekly Digest Adoption & Engagement

**Dashboard name**: Digest Health  
**Audience**: PM, Growth, CS  
**Refresh cadence**: Daily (data as of previous day)  
**Data source**: `pulse_analytics` Snowflake schema via QuickSight SPICE

---

## Layout (3 rows)

---

### Row 1: Executive KPI Strip (4 KPI tiles)

| Tile | Metric | Calculation | Target | Conditional Formatting |
|------|--------|-------------|--------|----------------------|
| Digest Enabled (Orgs) | % of orgs with digest ON | `digest_enabled_orgs / total_orgs` | 60% | Red <30%, Yellow 30–59%, Green ≥60% |
| This Week's Send | Total emails sent (last Monday) | Count of `digest_sends` WHERE `week = current_week` | 18,000 | Red <2k (cap issue), Green otherwise |
| Open Rate | Opens / Sends (last send) | `opens / sends` | 45% | Red <30%, Yellow 30–44%, Green ≥45% |
| Click-Through Rate | CTA clicks / Opens (last send) | `cta_clicks / opens` | 20% | Red <10%, Yellow 10–19%, Green ≥20% |

---

### Row 2: Trend Charts (2 charts side by side)

**Chart 1: Weekly Send Volume & Open Rate (line + bar combo)**
- X-axis: Week (last 12 weeks)
- Bar: Total sends per week
- Line: Open rate % per week
- Filter: Plan tier (All / Starter / Pro / Enterprise)

**Chart 2: Digest Adoption by Cohort**
- X-axis: Account signup month (cohort)
- Y-axis: % of accounts in cohort with digest enabled
- Lines: One per cohort, trailing 6 months
- Purpose: Shows whether new accounts are adopting digest faster than older ones

---

### Row 3: Drill-Down Tables (2 tables side by side)

**Table 1: Top 20 Accounts by Engagement**
| Column | Source |
|--------|--------|
| Account name | `accounts.name` |
| Plan tier | `accounts.plan_tier` |
| Managers receiving digest | `COUNT(digest_recipients)` |
| Last send open rate | `opens / sends` |
| Avg CTA clicks/send | `AVG(cta_clicks)` |

Sorted by: Open rate DESC  
Use case: CS proactive outreach to high-engagement accounts for expansion

**Table 2: At-Risk Accounts (digest enabled, low engagement)**
| Column | Source |
|--------|--------|
| Account name | `accounts.name` |
| Weeks since last open | `DATEDIFF(week, last_open_date, CURRENT_DATE)` |
| Sends with 0 opens | `COUNT(sends WHERE opens = 0)` |
| CS owner | `accounts.cs_owner` |

Filter: Accounts with digest enabled AND open rate <15% over last 4 sends  
Use case: CS intervention to improve digest content or disable to avoid spam flagging

---

## Filters (applied globally)

- Date range (default: last 90 days)
- Plan tier (multi-select)
- Account segment (SMB / Mid-Market / Enterprise)
- CS owner (for CS team view)

---

## Implementation Notes

- All digest metrics require `tag = 'weekly_digest'` in SendGrid event data
- SPICE refresh: Schedule daily at 6am UTC (before Monday send window review)
- Row-level security: CS owners should only see their assigned accounts in Table 2
- QuickSight dataset: Join `digest_sends`, `digest_events` (opens/clicks), and `accounts` on `account_id`
