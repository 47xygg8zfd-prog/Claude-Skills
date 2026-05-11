---
name: quicksight-dashboards
description: >
  Design, build, and optimize Amazon QuickSight dashboards for product and business analytics.
  Use this skill whenever the user wants to create a dashboard, visualize metrics, build a KPI
  board, turn query results into charts, or share data with stakeholders via QuickSight. Also
  trigger for phrases like "build a dashboard for", "visualize this data", "track this metric in
  QuickSight", "create a KPI view", "add a chart for", or "set up a QuickSight analysis". Produces
  dashboard designs, dataset connection guidance, calculated field formulas, and visualization
  recommendations ready for QuickSight implementation.
---

# QuickSight Dashboards Skill

Design and build Amazon QuickSight dashboards for PM-level product analytics and stakeholder reporting.

---

## Dashboard Design Workflow

```
1. Define the audience & question
2. Identify data sources (Snowflake, S3, RDS)
3. Design the layout (KPIs → Trends → Details)
4. Build dataset + calculated fields
5. Publish & schedule refresh
```

---

## Step 1: Define the Dashboard

Before opening QuickSight, answer these:

| Question | Why It Matters |
|----------|---------------|
| Who is the audience? | Execs want KPIs; ops teams want drill-downs |
| What decision does this support? | Determines which metrics matter |
| What time range is primary? | Daily, weekly, monthly? |
| How often will it refresh? | Hourly, daily, weekly SPICE refresh |
| Will it be published or embedded? | Affects sharing permissions |

---

## Step 2: Connect Your Data Source

### Snowflake Connection

In QuickSight → Datasets → New Dataset → Snowflake

**Connection settings:**
```
Data source name: [descriptive name, e.g., "Prod Snowflake — Analytics"]
Instance ID:      [your Snowflake account identifier]
Database:         [db name]
Warehouse:        [compute warehouse]
Username / Password or IAM role
```

**Best practices:**
- Use a dedicated read-only QuickSight service account
- Point to a reporting schema or views, not raw tables
- Use Direct Query for real-time; SPICE for performance on large datasets

### Custom SQL Dataset

For complex queries (joins, cohorts, funnels), use Custom SQL:

```sql
-- Example: Feature Adoption Dashboard Dataset
SELECT
  DATE_TRUNC('week', e.event_date)   AS week,
  u.segment                           AS user_segment,
  COUNT(DISTINCT e.user_id)           AS active_users,
  COUNT(DISTINCT CASE WHEN e.feature = 'feature_x'
        THEN e.user_id END)           AS feature_x_users,
  ROUND(
    COUNT(DISTINCT CASE WHEN e.feature = 'feature_x'
          THEN e.user_id END) * 100.0
    / NULLIF(COUNT(DISTINCT e.user_id), 0), 1
  )                                   AS adoption_pct
FROM events e
JOIN users u ON e.user_id = u.id
WHERE e.event_date >= DATEADD('month', -3, CURRENT_DATE)
GROUP BY 1, 2
ORDER BY 1, 2
```

---

## Step 3: Calculated Fields

Common PM metrics as QuickSight calculated field formulas:

### Growth Rate (Week-over-Week)
```
// WoW Growth %
(sum({current_week_users}) - sum({prior_week_users}))
/ nullIf(sum({prior_week_users}), 0) * 100
```

### Conversion Rate
```
// Funnel conversion: Step A → Step B
sum({step_b_users}) / nullIf(sum({step_a_users}), 0) * 100
```

### Rolling 7-Day Average
```
// Use a window function in Snowflake SQL dataset;
// QuickSight doesn't support window functions natively in calc fields
// Recommended: compute in SQL, bring in as a column
```

### Health Status RAG Label
```
// Red / Amber / Green status field
ifelse(
  {adoption_pct} >= 80, "Green",
  {adoption_pct} >= 50, "Amber",
  "Red"
)
```

### Time Since Last Event (Days)
```
dateDiff("DAY", {last_active_date}, now())
```

---

## Step 4: Dashboard Layout Patterns

### Standard PM Dashboard Layout (top → bottom)

```
┌─────────────────────────────────────────────────────┐
│  [Date Range Filter]  [Segment Filter]  [Refresh: X] │
├──────────┬──────────┬──────────┬────────────────────┤
│  KPI: DAU │ KPI: WAU │ KPI: MAU │  KPI: Adoption %   │  ← KPI Row (scorecards)
├──────────┴──────────┴──────────┴────────────────────┤
│                                                      │
│         Line Chart: DAU Trend (30/60/90 days)        │  ← Primary Trend
│                                                      │
├───────────────────────┬──────────────────────────────┤
│  Bar: Feature Adoption │  Funnel: Conversion Steps    │  ← Feature Analysis
│  by Segment            │                              │
├───────────────────────┴──────────────────────────────┤
│         Table: Top 10 Users / Segments / Events       │  ← Drill-down Detail
└─────────────────────────────────────────────────────┘
```

### Visualization Type Guide

| Metric Type | Best Visual | Notes |
|------------|-------------|-------|
| Single KPI | KPI / Scorecard | Show delta vs prior period |
| Trend over time | Line chart | Use multiple series for segments |
| Comparison across groups | Clustered bar or horizontal bar | Horizontal if many categories |
| Part-of-whole (%) | Donut / Pie | Only for ≤5 segments |
| Funnel / conversion | Funnel visual or horizontal bars | Show absolute + % |
| Distribution | Histogram | Good for latency, session length |
| Correlation | Scatter plot | Two numeric dimensions |
| Detailed breakdown | Pivot table | Good for segment × metric grids |

---

## Step 5: Common Dashboard Templates

### Product Health Dashboard
**Audience**: PM, Engineering, Leadership
**Refresh**: Daily (SPICE)
**Metrics**:
- DAU / WAU / MAU (scorecards with WoW delta)
- DAU trend line (90 days)
- Feature adoption by segment (bar chart)
- Error rate trend (line chart)
- Top feature usage table

### Sprint / Delivery Dashboard
**Audience**: PM, Scrum Master, Engineering Manager
**Refresh**: Daily
**Metrics**:
- Stories completed this sprint vs. committed
- Cumulative flow (stories by status over time)
- Velocity trend (last 10 sprints, bar chart)
- Open bugs by severity (stacked bar)
- Days until sprint end (KPI scorecard)

### Executive / OKR Dashboard
**Audience**: VP, C-suite
**Refresh**: Weekly
**Metrics**:
- OKR progress bars (% to target)
- Revenue / ARR trend
- Key leading indicator trends
- Risks / flags (RAG table)
- Keep it to 1 page, no more than 6 visuals

### Funnel / Conversion Dashboard
**Audience**: PM, Marketing, Growth
**Refresh**: Daily
**Metrics**:
- Funnel visual (each step + conversion %)
- Step-by-step drop-off by segment
- Trend: conversion rate over time
- Segment comparison (cohort table)

---

## Step 6: Publishing & Sharing

### Share Options
| Option | Use Case |
|--------|---------|
| Share → Specific users | Stakeholders with QuickSight accounts |
| Publish as Dashboard | Read-only view, no editing |
| Embed (URL/iframe) | Insert into Confluence, Notion, internal portals |
| Email report (scheduled) | Weekly digest to leadership |
| Export to PDF | Ad-hoc reporting, board packets |

### Scheduling Refreshes (SPICE)
- Go to Datasets → select dataset → Schedule Refresh
- Recommended: daily at 6 AM before business hours
- Alert threshold: set up "Anomaly Detection" alerts on key KPIs

---

## Troubleshooting Common Issues

| Issue | Fix |
|-------|-----|
| Blank visuals after filter | Check field type — string filters won't match numeric columns |
| Slow dashboard (Direct Query) | Switch to SPICE, or optimize upstream SQL |
| SPICE refresh failing | Check Snowflake credentials, IP whitelist, warehouse auto-resume |
| Calculated field error | Use `nullIf(denominator, 0)` to avoid divide-by-zero |
| Dates not grouping correctly | Ensure date field is `Date` type, not string |
| Can't drill down | Enable "Enable drill-down" in visual menu |

---

## QuickSight ↔ PM Workflow

```
Snowflake Query (data-queries skill)
        ↓
QuickSight Custom SQL Dataset
        ↓
Dashboard Design (this skill)
        ↓
Published Dashboard → Stakeholders
        ↓
Anomaly Alerts → PM Notified → Investigation
```

## Integration Points
- Use **data-queries** skill to write the Snowflake SQL backing your datasets
- Use **monte-carlo** skill to model forecast ranges and display them as reference lines
- Use **pm-presentations** skill to export dashboard screenshots into exec slide decks
