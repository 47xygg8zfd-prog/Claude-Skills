# Sentinel — Data Science Measurement Plan
**Date:** 2026-05-12  
**Document type:** Metrics translation and instrumentation spec  
**Product:** Sentinel — On-Call Intelligence Platform  
**Status:** Draft — requires instrumentation engineering review  
**Owner:** Data/Analytics  
**Inputs:** PRD metrics (MTTR, HDI, runbook coverage rate, routing accuracy), experiment design (File 07)

---

## Purpose

This document does not redefine the product metrics. Those are specified in the PRD. This document answers a different question: **what events must be instrumented, and what SQL must be written, to actually measure those metrics at experiment time?**

Every metric the PRD cites must trace to a specific event, a specific database table, and a specific query. If that chain cannot be completed, the metric is unmeasurable and must be flagged as a blocking instrumentation gap before the experiment begins.

---

## From PRD Metrics to Instrumentation

### Metric translation table

| PRD metric | What it actually requires | Instrumentation dependency |
|-----------|--------------------------|--------------------------|
| MTTR | Timestamps for incident open and incident close, per incident, with resolver identity | `incident_opened`, `incident_closed` events |
| HDI (Hero Dependency Index) | % of incidents resolved by top 20% of resolvers — requires knowing the *full rotation*, not just who resolved | `incident_closed` + PagerDuty rotation schedule API (not covered by events alone — see Flag below) |
| Runbook coverage rate | % of closed incidents with an attached, non-trivially-complete runbook | `runbook_created` event with `incident_id` foreign key and `word_count` property |
| Routing accuracy | % of routing suggestions that are accepted (not overridden) by the engineer who receives the alert | `routing_override` event (absence of override = acceptance) |
| On-call satisfaction score | Weekly survey response, 1–5 scale | External survey tool — not an instrumented event; must be joined to team_id |

---

## Instrumentation Plan

### Events required

All events are emitted from the Sentinel Node.js incident service and written to the `sentinel_events` table in Postgres. Every event shares a common envelope.

**Common event envelope:**

| Field | Type | Notes |
|-------|------|-------|
| `event_id` | UUID | Primary key |
| `event_type` | VARCHAR | One of the event types below |
| `team_id` | UUID | Foreign key to `teams` table |
| `user_id` | UUID | Engineer who triggered the event; nullable for system events |
| `incident_id` | UUID | Foreign key to `incidents` table; nullable for non-incident events |
| `occurred_at` | TIMESTAMPTZ | When the event happened (client-reported, server-validated) |
| `received_at` | TIMESTAMPTZ | When the server received the event |
| `sentinel_version` | VARCHAR | App version for debugging |

---

### Event specifications

#### `incident_opened`

Fired when Sentinel receives a webhook from PagerDuty or OpsGenie indicating a new incident has been triggered.

| Property | Type | Required | Notes |
|----------|------|----------|-------|
| `incident_id` | UUID | Yes | Sentinel internal ID |
| `external_incident_id` | VARCHAR | Yes | PagerDuty/OpsGenie incident ID |
| `alert_type` | VARCHAR | Yes | Normalized alert name (lowercase, whitespace-stripped) |
| `alert_source` | ENUM | Yes | `pagerduty` or `opsgenie` |
| `severity` | ENUM | Yes | `critical`, `high`, `medium`, `low` |
| `service_name` | VARCHAR | Yes | Service tag from PagerDuty/OpsGenie |
| `routing_source` | ENUM | Yes | `manual` (on-call schedule) or `system` (Sentinel routing suggestion accepted) |
| `suggested_resolver_user_id` | UUID | Nullable | If routing suggestion was made; null if `routing_source = manual` |
| `assigned_resolver_user_id` | UUID | Nullable | Actual assigned engineer at open time; may be null if unassigned |
| `occurred_at` | TIMESTAMPTZ | Yes | Timestamp from PagerDuty/OpsGenie webhook |

---

#### `incident_closed`

Fired when the incident is marked resolved in PagerDuty/OpsGenie and that webhook is received by Sentinel.

| Property | Type | Required | Notes |
|----------|------|----------|-------|
| `incident_id` | UUID | Yes | Must match a prior `incident_opened` event |
| `duration_ms` | BIGINT | Yes | Computed server-side: `closed_at − opened_at`. Source of truth for MTTR. |
| `resolver_user_id` | UUID | Yes | Engineer who closed the incident |
| `routing_source` | ENUM | Yes | `manual` or `system` — was Sentinel routing used for this incident? |
| `runbook_id` | UUID | Nullable | If a runbook was attached at close; null if no runbook |
| `runbook_word_count` | INTEGER | Nullable | Word count of runbook body at time of close; null if no runbook |
| `alert_type` | VARCHAR | Yes | Denormalized for query convenience |
| `service_name` | VARCHAR | Yes | Denormalized |
| `occurred_at` | TIMESTAMPTZ | Yes | Timestamp of close event from PagerDuty/OpsGenie webhook |

**Critical note on `routing_source`:** This field must distinguish between:
1. Sentinel suggested an engineer and the suggestion was accepted (`system`)
2. The engineer was assigned through normal on-call rotation with no Sentinel involvement (`manual`)
3. Sentinel suggested an engineer, the suggestion was overridden, and a different engineer resolved it — in this case `routing_source = manual` and a corresponding `routing_override` event must exist

---

#### `runbook_created`

Fired when an engineer submits the runbook capture form at incident close.

| Property | Type | Required | Notes |
|----------|------|----------|-------|
| `runbook_id` | UUID | Yes | |
| `incident_id` | UUID | Yes | The incident this runbook documents |
| `alert_type` | VARCHAR | Yes | Denormalized |
| `author_user_id` | UUID | Yes | Engineer who wrote the runbook |
| `word_count` | INTEGER | Yes | Word count of runbook body at creation time |
| `time_to_create_ms` | BIGINT | Yes | Milliseconds from when capture prompt appeared to when engineer submitted |
| `draft_was_prefilled` | BOOLEAN | Yes | Was this a system-generated draft that the engineer edited? (Future feature flag) |
| `occurred_at` | TIMESTAMPTZ | Yes | |

**Note on `time_to_create_ms`:** This is a secondary quality signal. A runbook completed in <30 seconds is almost certainly a click-through with minimal content. We should not exclude these from coverage metrics, but we should track them separately to understand the quality-floor problem.

---

#### `runbook_viewed`

Fired when an engineer opens a runbook while an incident is active.

| Property | Type | Required | Notes |
|----------|------|----------|-------|
| `runbook_id` | UUID | Yes | |
| `incident_id` | UUID | Yes | The incident being worked at the time of view |
| `viewer_user_id` | UUID | Yes | |
| `view_duration_ms` | BIGINT | Yes | How long the runbook was open before closed/navigated away; proxy for engagement |
| `view_context` | ENUM | Yes | `during_active_incident` or `browsing` (outside an active incident) |
| `occurred_at` | TIMESTAMPTZ | Yes | |

---

#### `routing_override`

Fired when an engineer receives a Sentinel routing suggestion and explicitly reassigns the incident to a different engineer (or to themselves if the suggestion was for someone else).

| Property | Type | Required | Notes |
|----------|------|----------|-------|
| `incident_id` | UUID | Yes | |
| `suggested_user_id` | UUID | Yes | Who Sentinel suggested |
| `actual_user_id` | UUID | Yes | Who the engineer reassigned to |
| `overriding_user_id` | UUID | Yes | Who performed the override (may be different from either above — e.g., a manager) |
| `override_reason` | ENUM | Nullable | `not_available`, `not_expert`, `wrong_rotation`, `preference`, `other` — presented as a quick-select in the UI |
| `routing_confidence_score` | FLOAT | Yes | Sentinel's internal confidence score for the suggestion at time of override (0–1) |
| `occurred_at` | TIMESTAMPTZ | Yes | |

**Why this event is critical:** The `routing_override` event is the only signal that routing was wrong. Without it, we can only measure routing acceptance by absence — an incident with no override was "accepted." But absence of override does not mean the routing was correct; it may mean the engineer did not notice the suggestion or did not know they could override. The override UI must be prominent and the event must fire reliably.

---

#### `rotation_schedule_synced`

Fired daily by the scheduled PagerDuty API sync job. This is required for HDI computation. See Flag section below.

| Property | Type | Required | Notes |
|----------|------|----------|-------|
| `team_id` | UUID | Yes | |
| `schedule_date` | DATE | Yes | The calendar date this schedule applies to |
| `on_call_user_ids` | UUID[] | Yes | All engineers scheduled to be on call on this date |
| `schedule_source` | VARCHAR | Yes | PagerDuty schedule ID |
| `sync_succeeded` | BOOLEAN | Yes | Whether the API call succeeded |
| `occurred_at` | TIMESTAMPTZ | Yes | When the sync ran |

---

## Measurement SQL

The following queries are written for Postgres. All reference the `sentinel_events` table plus the `incidents` and `teams` tables.

### Query 1: MTTR (median, by team, by week)

```sql
-- Weekly median MTTR per team
-- Used as primary experiment metric
SELECT
    team_id,
    DATE_TRUNC('week', occurred_at) AS week_start,
    COUNT(*) AS incident_count,
    PERCENTILE_CONT(0.5) WITHIN GROUP (
        ORDER BY (properties->>'duration_ms')::BIGINT
    ) / 60000.0 AS median_mttr_minutes,
    PERCENTILE_CONT(0.25) WITHIN GROUP (
        ORDER BY (properties->>'duration_ms')::BIGINT
    ) / 60000.0 AS p25_mttr_minutes,
    PERCENTILE_CONT(0.75) WITHIN GROUP (
        ORDER BY (properties->>'duration_ms')::BIGINT
    ) / 60000.0 AS p75_mttr_minutes
FROM sentinel_events
WHERE
    event_type = 'incident_closed'
    AND (properties->>'duration_ms')::BIGINT > 0
    AND (properties->>'duration_ms')::BIGINT < 86400000  -- exclude >24h outliers
GROUP BY 1, 2
ORDER BY 1, 2;
```

**Outlier handling:** Incidents with `duration_ms > 86400000` (24 hours) are excluded from the MTTR computation. These are typically incidents that were left open by accident or represent multi-day outages that are not representative of the operational baseline. They should be flagged for manual review but not distort the median.

---

### Query 2: Hero Dependency Index (HDI)

**Important prerequisite:** HDI requires knowing the full on-call rotation, not just who resolved incidents. This query can only run if `rotation_schedule_synced` events are available. See Flag section.

```sql
-- HDI: % of incidents resolved by engineers who are NOT scheduled on-call
-- (i.e., hero resolutions — incidents handled by people who stepped in outside rotation)
-- Computed monthly per team

WITH scheduled_on_call AS (
    -- Who was scheduled on each date?
    SELECT
        team_id,
        schedule_date,
        UNNEST((properties->'on_call_user_ids')::UUID[]) AS scheduled_user_id
    FROM sentinel_events
    WHERE event_type = 'rotation_schedule_synced'
        AND (properties->>'sync_succeeded')::BOOLEAN = TRUE
),

incident_resolutions AS (
    SELECT
        team_id,
        (properties->>'resolver_user_id')::UUID AS resolver_user_id,
        DATE_TRUNC('month', occurred_at) AS month,
        occurred_at::DATE AS incident_date
    FROM sentinel_events
    WHERE event_type = 'incident_closed'
),

labeled_resolutions AS (
    SELECT
        ir.team_id,
        ir.month,
        ir.resolver_user_id,
        CASE
            WHEN soc.scheduled_user_id IS NOT NULL THEN 'scheduled'
            ELSE 'hero'  -- resolved by someone not on the rotation
        END AS resolver_type
    FROM incident_resolutions ir
    LEFT JOIN scheduled_on_call soc
        ON ir.team_id = soc.team_id
        AND ir.incident_date = soc.schedule_date
        AND ir.resolver_user_id = soc.scheduled_user_id
)

SELECT
    team_id,
    month,
    COUNT(*) AS total_incidents,
    SUM(CASE WHEN resolver_type = 'hero' THEN 1 ELSE 0 END) AS hero_resolved,
    ROUND(
        100.0 * SUM(CASE WHEN resolver_type = 'hero' THEN 1 ELSE 0 END) / COUNT(*),
        1
    ) AS hero_dependency_index_pct
FROM labeled_resolutions
GROUP BY 1, 2
ORDER BY 1, 2;
```

**Note:** If `rotation_schedule_synced` data is unavailable, HDI must fall back to a concentration-based approximation: % of incidents resolved by the top-20% of resolvers by volume. This is an imperfect proxy (it does not account for rotation schedule) and should be labeled as "HDI (approximate)" in the dashboard to avoid misleading stakeholders.

---

### Query 3: Runbook coverage rate

```sql
-- % of closed incidents with an attached runbook (word count >= 50)
-- Computed weekly per team

WITH closed_incidents AS (
    SELECT
        team_id,
        (properties->>'incident_id')::UUID AS incident_id,
        (properties->>'runbook_id')::UUID AS runbook_id,
        (properties->>'runbook_word_count')::INTEGER AS runbook_word_count,
        DATE_TRUNC('week', occurred_at) AS week_start
    FROM sentinel_events
    WHERE event_type = 'incident_closed'
)

SELECT
    team_id,
    week_start,
    COUNT(*) AS total_incidents_closed,
    SUM(CASE
        WHEN runbook_id IS NOT NULL AND runbook_word_count >= 50 THEN 1
        ELSE 0
    END) AS incidents_with_valid_runbook,
    ROUND(
        100.0 * SUM(CASE
            WHEN runbook_id IS NOT NULL AND runbook_word_count >= 50 THEN 1
            ELSE 0
        END) / NULLIF(COUNT(*), 0),
        1
    ) AS runbook_coverage_pct,

    -- Quality sub-metric: coverage of fast-completed runbooks (possible click-throughs)
    SUM(CASE
        WHEN runbook_id IS NOT NULL
            AND runbook_word_count >= 50
            AND (properties->>'time_to_create_ms')::BIGINT < 30000  -- under 30 seconds
        THEN 1 ELSE 0
    END) AS suspicious_runbooks
FROM closed_incidents
GROUP BY 1, 2
ORDER BY 1, 2;
```

**`suspicious_runbooks` note:** A runbook completed in under 30 seconds with ≥50 words is flagged as suspicious — likely pre-filled from a template or pasted. This column is not used in the primary coverage metric but should be reviewed as a quality signal. If `suspicious_runbooks / incidents_with_valid_runbook > 30%`, escalate for manual quality review.

---

### Query 4: Routing accuracy (acceptance rate)

```sql
-- Routing acceptance rate: % of routed incidents where the suggested engineer resolved it
-- (no routing_override event fired)

WITH routed_incidents AS (
    -- Incidents where Sentinel made a routing suggestion
    SELECT
        team_id,
        (properties->>'incident_id')::UUID AS incident_id,
        (properties->>'suggested_resolver_user_id')::UUID AS suggested_user_id,
        DATE_TRUNC('week', occurred_at) AS week_start
    FROM sentinel_events
    WHERE event_type = 'incident_opened'
        AND properties->>'routing_source' = 'system'
        AND properties->>'suggested_resolver_user_id' IS NOT NULL
),

overrides AS (
    SELECT DISTINCT (properties->>'incident_id')::UUID AS incident_id
    FROM sentinel_events
    WHERE event_type = 'routing_override'
)

SELECT
    ri.team_id,
    ri.week_start,
    COUNT(*) AS routed_incidents,
    SUM(CASE WHEN o.incident_id IS NULL THEN 1 ELSE 0 END) AS accepted,
    SUM(CASE WHEN o.incident_id IS NOT NULL THEN 1 ELSE 0 END) AS overridden,
    ROUND(
        100.0 * SUM(CASE WHEN o.incident_id IS NULL THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0),
        1
    ) AS routing_acceptance_rate_pct
FROM routed_incidents ri
LEFT JOIN overrides o ON ri.incident_id = o.incident_id
GROUP BY 1, 2
ORDER BY 1, 2;
```

---

## Flag: HDI Is Not Measurable From Events Alone

**This is a blocking instrumentation gap.**

The PRD defines HDI as: "percentage of incidents resolved by the top 20% of resolvers." This definition is ambiguous and creates a measurement problem.

**Problem 1 — The denominator is undefined:** 20% of what population? If a 10-person team has 3 people resolve all incidents, are those 3 people "the top 30%" or "heroes"? The 20% threshold was designed for large teams. At small teams (3–7 engineers, which is our ICP), the math produces unstable and uninterpretable results.

**Problem 2 — Rotation schedule is required:** A more precise and meaningful version of HDI measures: "% of incidents resolved by engineers who were NOT scheduled to be on call." This identifies true hero behavior (stepping in outside rotation) rather than just concentration. But computing this requires knowing who was scheduled on call — information that lives in the PagerDuty rotation schedule, not in incident resolution records.

**Problem 3 — Sentinel does not currently pull rotation schedule data:** The planned integrations (PagerDuty/OpsGenie webhooks, Slack, GitHub) do not include a daily PagerDuty schedule sync. Without it, HDI can only be approximated from resolution concentration, which overstates hero dependency on small teams and misses it on teams where heroes volunteer for extra shifts.

**Fix required:**

1. Implement a daily scheduled job that calls the PagerDuty `/schedules/{id}/users` API for each connected team and writes a `rotation_schedule_synced` event to `sentinel_events`.
2. Add the `rotation_schedule_synced` event spec to the instrumentation plan (defined above).
3. HDI computation (Query 2) depends on this job being live and backfilled before the experiment begins.

**Estimated engineering effort:** 2–3 story points (API integration + scheduled job + event schema). This must be on the sprint before the pre-period begins, or HDI cannot be measured in the experiment.

**Interim fallback:** If the schedule sync is not ready before pre-period start, use the concentration-based HDI approximation (% of incidents resolved by top-20% resolvers by volume). Label it clearly as "HDI (estimated — rotation schedule integration pending)" in all dashboards and reports. Do not present it as equivalent to schedule-based HDI.

---

## Experiment Readiness Assessment

### Baseline stability

**Baseline is NOT stable yet.**

To establish a reliable MTTR baseline, we need 4 weeks of pre-period data with the following characteristics:
- No major product changes to Sentinel during the pre-period (instrumentation must be stable)
- No major infrastructure changes on participant teams (deployment churn distorts MTTR)
- Minimum 15 incidents per team in the pre-period (below this, median MTTR has too much variance for reliable comparison)

**Recommended sequence:**
1. Weeks -6 to -5: Instrumentation live and validated (see File 10)
2. Weeks -4 to -1: Pre-period data collection. Concierge test running in parallel.
3. Week 0: Experiment start. Pre-period baseline confirmed.

**Do not start the experiment without 4 weeks of stable pre-period data.** A 2-week pre-period is insufficient — MTTR has weekly variation (weekday vs. weekend incidents, sprint deployment cycles) that requires at least 4 weeks to smooth.

---

## Confounds

These are variables that may affect MTTR independently of Sentinel's features and must be accounted for in the analysis.

| Confound | Measurement approach | Mitigation |
|---------|---------------------|-----------|
| **Team size** | Engineer count from team onboarding | Stratify randomization by team size (3–7 vs. 8–20). Include as covariate in regression. |
| **Deploy frequency** | GitHub webhook: count of `push` events to main branch per week | Track as a covariate. Flag teams with >20 deploys/week for subgroup analysis (high-churn routing signal). |
| **Incident complexity** | Alert severity (`critical` vs. `high` vs. `medium`) + `duration_ms` distribution | Stratify MTTR analysis by severity. Do not pool `critical` incidents with `medium` incidents in the primary MTTR metric. |
| **Pre-period MTTR variance** | Compute per-team MTTR standard deviation in pre-period | Exclude teams with pre-period standard deviation > 2.5x cohort median. Include pre-period MTTR as covariate in analysis. |
| **Incident volume** | Count of `incident_opened` events per week | High-volume teams have more routing signal; low-volume teams have noisier MTTR estimates. Run subgroup analysis. |
| **Engineering experience level** | Proxy: years on team (from user onboarding data, if available) | If data available, include as team-level covariate (% of senior engineers). |
| **Concurrent tooling changes** | Screened at eligibility (no other runbook tooling in prior 90 days) | Ongoing: monitor for tool adoption events during experiment period. |
| **Hawthorne effect** | Treated teams know they are using a new product | Cannot be fully eliminated in a product experiment. Acknowledge in report. Pre-period data provides some baseline for comparison. |
