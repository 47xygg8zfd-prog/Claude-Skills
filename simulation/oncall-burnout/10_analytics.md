# Sentinel — Analytics Instrumentation Validation
**Date:** 2026-05-12  
**Document type:** Instrumentation validation protocol  
**Product:** Sentinel — On-Call Intelligence Platform  
**Status:** Pre-launch checklist — all BLOCKED items must be resolved before pre-period begins  
**Owner:** Data/Analytics + Engineering  
**Input:** Measurement plan (File 09)

---

## Purpose

An experiment is only as good as its instrumentation. This document runs a 4-check validation protocol against every metric in the measurement plan (File 09) and identifies all blocking gaps before a single line of experiment data is collected.

The four checks are:
1. **Measurability** — Can this metric be computed from existing or planned events?
2. **Reliability** — Will the event fire consistently, or are there conditions under which it can be missed or duplicated?
3. **Validity** — Does the event actually measure what we think it measures?
4. **Timeliness** — Will the data be available when we need it for the experiment decision?

---

## 4-Check Validation Table

| Metric | Check 1: Measurable? | Check 2: Reliable? | Check 3: Valid? | Check 4: Timely? | Status |
|--------|---------------------|-------------------|----------------|-----------------|--------|
| **MTTR** | Yes — `incident_closed.duration_ms` | Medium — depends on PagerDuty webhook reliability; missed close events leave incidents "open" indefinitely | Medium — `duration_ms` is server-computed from webhook timestamps, not from actual engineer work time; acknowledging and immediately re-acknowledging inflates duration | Yes — available at incident close | **NEEDS VALIDATION** |
| **HDI** | **No** — requires rotation schedule, not available from events alone | N/A until schedule sync is implemented | N/A | N/A | **BLOCKED** |
| **Runbook coverage rate** | Yes — `runbook_created.word_count ≥ 50` + `incident_closed.runbook_id` | Medium — if engineer submits runbook *after* the incident is closed (e.g., async review), the `incident_closed` event fires without `runbook_id`; runbook is uncounted | Low — word count is not a quality proxy; a 50-word runbook can be useless | Yes | **NEEDS THRESHOLD DECISION** |
| **Routing accuracy** | Yes — absence of `routing_override` for `routing_source = system` incidents | Medium — override UI must be visible and friction-free; silent non-use is counted as acceptance | Medium — acceptance ≠ correct routing; engineer may accept wrong suggestion and resolve slower | Yes | **NEEDS UX VALIDATION** |
| **On-call satisfaction score** | Yes — external survey, joined to `team_id` | Low — survey response rates may be insufficient (target: ≥60% per team per week) | High — direct self-report | Yes — if survey runs weekly | **NEEDS SURVEY INSTRUMENT FINALIZED** |

---

## Flag: HDI Is Unmeasurable From Events Alone

**Severity: Blocking**

This is the most significant instrumentation gap in the entire Sentinel measurement plan and must be resolved before the pre-period begins.

### The problem

HDI as specified in the PRD requires knowing two things:
1. Who *resolved* each incident (available from `incident_closed.resolver_user_id`)
2. Who *was scheduled to be on call* at the time of each incident (NOT available from any current or planned event)

Without (2), HDI can only be approximated as a concentration metric: "what fraction of incidents were resolved by the top-N% of resolvers by volume?" This approximation overstates hero dependency in two ways:

- A senior engineer who volunteers for extra shifts appears as a "hero" even though they were scheduled
- A junior engineer who resolves many low-severity incidents during business hours appears as a "hero" by volume, even though their incidents are trivial

More fundamentally: HDI measures whether heroes are *carrying load they were not scheduled to carry*. You cannot compute that without knowing what they were scheduled to carry.

### The fix

**Step 1: Add a daily PagerDuty schedule sync job**

The Sentinel Node.js service must run a daily scheduled job (cron at 00:01 UTC) that:
1. For each team with a connected PagerDuty account, calls `GET /schedules/{scheduleId}/users?since=<today>&until=<today+1>`
2. Parses the list of engineers scheduled on call for that calendar day
3. Writes a `rotation_schedule_synced` event to `sentinel_events` with the full list of `on_call_user_ids`

**Step 2: Backfill pre-period rotation data**

Before the pre-period begins, run the sync job retroactively for the prior 60 days to establish a historical baseline for HDI computation. PagerDuty's schedule API supports historical queries.

**Step 3: OpsGenie equivalent**

OpsGenie exposes rotation schedules via `GET /v2/schedules/{identifier}/rotations`. The same daily sync pattern applies.

**Estimated engineering effort:** 3 story points (PagerDuty integration) + 2 story points (OpsGenie integration) + 1 story point (backfill job) = **6 story points total**.

This work must be completed before the pre-period starts. If it slips, HDI cannot be reported with integrity in the experiment results. Use the concentration-based approximation as a fallback, labeled explicitly.

---

## Detailed Metric Validation Notes

### MTTR — Additional reliability concerns

**Webhook delivery guarantees:** PagerDuty webhooks are delivered at-least-once. Sentinel must implement idempotent event ingestion (deduplication on `external_incident_id + event_type + occurred_at`) to prevent double-counting. If a webhook is lost, the incident never closes in Sentinel's records. This creates "ghost incidents" — open incidents in the Sentinel database that were resolved in PagerDuty.

**Mitigation:** Implement a daily reconciliation job that queries the PagerDuty REST API for incidents closed in the prior 24 hours and compares to `sentinel_events`. Any incident closed in PagerDuty but open in Sentinel should trigger a synthetic `incident_closed` event with a `source: reconciliation` flag. These should be excluded from the primary MTTR analysis (they indicate instrumentation failure, not real MTTR) but tracked as an instrumentation health metric.

**Validity note on `duration_ms`:** `duration_ms` is computed from the PagerDuty timestamps: `resolved_at − triggered_at`. This includes:
- Time before the engineer acknowledged the alert
- Time spent waiting for the system to recover after the fix was applied
- Any time the incident was manually "snoozed" in PagerDuty

It does NOT include incidents that were resolved before Sentinel received the webhook (sub-second resolution). It DOES include incidents where the engineer stepped away mid-investigation and returned. For our purposes, this is acceptable — MTTR as a product metric includes all of this time, and the treatment/control comparison will be subject to the same definition.

---

### Runbook coverage rate — Threshold decision required

The 50-word minimum for a "valid" runbook is a pragmatic choice, not a principled one. The data science team must decide and document the threshold before the pre-period begins, because it affects what percentage of the treatment arm is counted as having "coverage."

**Options:**

| Option | Threshold | Pros | Cons |
|--------|-----------|------|------|
| A | Word count ≥ 50 | Simple, automatable | Does not filter junk content |
| B | Word count ≥ 50 AND `time_to_create_ms ≥ 60000` (1 minute) | Filters likely click-throughs | Penalizes fast typists; arbitrary threshold |
| C | Word count ≥ 100 | Higher quality floor | Reduces coverage rate significantly; may fail experiment |
| D | Structured fields completion (3 of 5 required fields non-empty) | Most meaningful | Requires structured form, not free text |

**Recommendation:** Start with Option A for the pre-period and experiment. Track Option B (`suspicious_runbooks`) as a secondary diagnostic. Commit to building Option D in V1.1 — the structured form is the right long-term solution and is aligned with the "auto-draft for human review" recommendation in File 06.

**Action required:** PM and Data/Analytics must agree on the threshold before instrumentation is finalized. Document the decision in this file as an amendment.

---

### Routing accuracy — UX validation required

The routing acceptance rate metric is computed as: (incidents routed by Sentinel where no `routing_override` was fired) / (total incidents routed by Sentinel).

This metric has a significant **validity problem**: an engineer who receives a routing suggestion and does not know how to override it — or does not see the override option — will be counted as "accepting" the suggestion. If the override UI is not prominent, the acceptance rate measures UI friction, not genuine satisfaction with the routing decision.

**Required UX validation (pre-launch):**

Before the experiment begins, run a usability test with 3–5 engineers from the pilot cohort:
1. Show them a routing suggestion in the Sentinel UI
2. Ask them to override it and reassign to a different engineer
3. Measure: Can they find the override option without assistance? How long does it take?

Pass threshold: ≥4 out of 5 engineers can complete the override within 30 seconds without assistance.

**If usability test fails:** The override affordance is not visible enough. This must be fixed before the experiment — otherwise routing acceptance rate is a measure of "could not figure out how to override" rather than "this routing decision was correct."

---

### On-call satisfaction score — Survey instrument required

The satisfaction guardrail is the most important metric in the experiment. If it is not measured reliably, the experiment can cause harm that goes undetected until engineers quit.

**Current state:** No survey instrument exists. This is a blocking gap.

**Requirements:**
- **Frequency:** Weekly, sent every Monday morning
- **Delivery:** Slack DM from the Sentinel bot (not email — response rates for Slack surveys are consistently higher in engineering populations)
- **Length:** ≤3 questions (longer surveys in operational contexts have <20% response rates)
- **Instrument:**

> "Quick on-call check-in from Sentinel (takes 60 seconds):"
> 
> 1. How would you rate your on-call experience this week? (1 = Very stressful, 5 = Manageable)
> 2. Did you feel you had the context you needed to resolve incidents this week? (Yes / Mostly / No)
> 3. One thing that would have made on-call better this week (optional, free text):

- **Response rate target:** ≥60% per team per week. Below 40%, the guardrail is unmeasurable.
- **Enforcement:** If a team's response rate falls below 40% for two consecutive weeks, they are excluded from the guardrail analysis for that period and flagged for CS follow-up.

**Action required:** Engineering must build the Slack survey bot before the pre-period begins. Estimated effort: 3 story points (Slack bot + weekly cron + survey response storage). This is not optional — the satisfaction guardrail cannot function without it.

---

## Event Specs: Final Validated Versions

### `incident_closed` (final spec)

```json
{
  "event_type": "incident_closed",
  "team_id": "uuid",
  "user_id": "uuid (resolver)",
  "incident_id": "uuid",
  "occurred_at": "timestamptz",
  "received_at": "timestamptz",
  "sentinel_version": "string",
  "properties": {
    "incident_id": "uuid",
    "external_incident_id": "string (PagerDuty/OpsGenie ID)",
    "alert_type": "string (normalized)",
    "service_name": "string",
    "severity": "enum: critical|high|medium|low",
    "duration_ms": "bigint (server-computed: closed_at - opened_at)",
    "resolver_user_id": "uuid",
    "routing_source": "enum: manual|system",
    "runbook_id": "uuid|null",
    "runbook_word_count": "integer|null",
    "alert_source": "enum: pagerduty|opsgenie",
    "source": "enum: webhook|reconciliation (default: webhook)"
  }
}
```

**Validation rules:**
- `duration_ms` must be positive; reject events where `duration_ms ≤ 0`
- `runbook_id` and `runbook_word_count` must either both be present or both be null
- `resolver_user_id` must correspond to a user in the `users` table; reject if user not found (likely means user has not completed Sentinel onboarding)
- `routing_source = system` requires a matching `incident_opened` event with `routing_source = system`; orphaned `system` closes should be flagged

---

### `runbook_created` (final spec)

```json
{
  "event_type": "runbook_created",
  "team_id": "uuid",
  "user_id": "uuid (author)",
  "incident_id": "uuid",
  "occurred_at": "timestamptz",
  "received_at": "timestamptz",
  "sentinel_version": "string",
  "properties": {
    "runbook_id": "uuid",
    "incident_id": "uuid",
    "alert_type": "string (normalized)",
    "author_user_id": "uuid",
    "word_count": "integer",
    "time_to_create_ms": "bigint",
    "draft_was_prefilled": "boolean (default: false)",
    "character_count": "integer",
    "has_code_block": "boolean",
    "has_numbered_list": "boolean"
  }
}
```

**Added fields `has_code_block` and `has_numbered_list`:** These are lightweight structural quality signals that can be computed at the application layer before the event fires. A runbook with at least one code block or numbered list is more likely to be actionable than one that is entirely prose. These fields are not used in the primary coverage metric but will be valuable for the quality analysis.

---

### `runbook_viewed` (final spec)

```json
{
  "event_type": "runbook_viewed",
  "team_id": "uuid",
  "user_id": "uuid (viewer)",
  "incident_id": "uuid",
  "occurred_at": "timestamptz",
  "received_at": "timestamptz",
  "sentinel_version": "string",
  "properties": {
    "runbook_id": "uuid",
    "incident_id": "uuid",
    "viewer_user_id": "uuid",
    "view_duration_ms": "bigint",
    "view_context": "enum: during_active_incident|browsing",
    "runbook_alert_type": "string",
    "incident_alert_type": "string",
    "alert_types_match": "boolean"
  }
}
```

**Added field `alert_types_match`:** Flags whether the runbook being viewed was written for the same alert type as the current incident. A view where `alert_types_match = false` may indicate the engineer is exploring related runbooks (positive signal) or that the routing logic surfaced an irrelevant runbook (negative signal). Tracking this distinguishes the two cases.

---

## Pre-Launch Checklist

This checklist must be completed and signed off before the pre-period data collection begins. "Pre-period" means the 4-week baseline window before the experiment starts. Items marked **BLOCKING** must be resolved or the pre-period cannot begin.

### Instrumentation

- [ ] **BLOCKING** — `incident_opened` event firing reliably from PagerDuty webhook handler. Verified with 10+ test incidents in staging.
- [ ] **BLOCKING** — `incident_closed` event firing reliably. `duration_ms` verified against manual calculation on test incidents.
- [ ] **BLOCKING** — `routing_override` event fires when engineer uses override UI. Verified in staging with 5+ override scenarios.
- [ ] **BLOCKING** — `runbook_created` event fires with all required properties. `time_to_create_ms` correctly measures prompt appearance to submit.
- [ ] **BLOCKING** — `runbook_viewed` event fires when runbook panel is opened during active incident. `view_duration_ms` stops on close/navigate-away.
- [ ] **BLOCKING** — `rotation_schedule_synced` daily job running. Verified against known PagerDuty schedule for a test team.
- [ ] **BLOCKING** — PagerDuty schedule backfill job run for prior 60 days on all pilot teams.
- [ ] Webhook idempotency: duplicate webhook delivery does not create duplicate events. Verified with forced duplicate test.
- [ ] Daily reconciliation job running. Verified it catches a manually-created "ghost incident" in staging.
- [ ] `sentinel_version` field is populated on all events. Verified.

### Metrics validation

- [ ] **BLOCKING** — MTTR query (File 09, Query 1) returns expected results on 30 days of staging data. Compared to manual calculation on 5 incidents. Match within 1%.
- [ ] **BLOCKING** — HDI query (File 09, Query 2) returns expected results when rotation schedule data is present. Verified against manually constructed test case.
- [ ] **BLOCKING** — Runbook coverage rate query returns expected results. Verified 50-word threshold is applied correctly.
- [ ] Routing acceptance rate query verified. Tested scenario where no overrides exist (100% acceptance) and scenario where all are overridden (0% acceptance).
- [ ] MTTR outlier exclusion (>24h) verified: incidents left open for >24h are excluded from MTTR metric.

### Survey instrument

- [ ] **BLOCKING** — Weekly satisfaction survey built and sending via Slack bot. Test send confirmed on Monday morning cron.
- [ ] **BLOCKING** — Survey responses stored with `team_id` and `user_id` and joinable to experiment arm assignment.
- [ ] Response rate monitoring dashboard exists. PM and CS lead can see response rates per team per week.

### Experiment setup

- [ ] **BLOCKING** — Randomization assignment table created. 60 teams assigned to treatment or control. Assignment is deterministic (same team always gets same arm).
- [ ] Treatment flag is enforced: control-arm teams see no runbook prompts and no routing suggestions. Verified in staging.
- [ ] Treatment flag is enforced: treatment-arm teams see both features. Verified in staging.
- [ ] Pre-period flag is set: no treatment features are active during the pre-period for any team.
- [ ] Guardrail monitoring alerts configured: automated notification to PM + Eng lead if acknowledgement time increases >20% or satisfaction score decreases >0.5 points week-over-week.

### Data access

- [ ] Analytics team has SELECT access to `sentinel_events` in production read replica.
- [ ] All 5 measurement queries (File 09) run successfully against production read replica on pre-period data.
- [ ] Dashboard showing weekly MTTR, HDI, coverage rate, routing acceptance, and satisfaction score per team is live and verified against raw SQL output.

### Documentation

- [ ] This checklist is complete. All blocking items are resolved.
- [ ] Measurement plan (File 09) is finalized and has data science sign-off.
- [ ] Experiment design (File 07) is finalized and has PM, Eng lead, and Data sign-off.
- [ ] Devil's advocate PRD responses (File 06 responses table) are completed by PRD author.
- [ ] Concierge test (File 08) is running or scheduled to begin at pre-period start.

---

## Sign-off

| Role | Name | Sign-off date | Notes |
|------|------|--------------|-------|
| PM | | | |
| Eng lead | | | |
| Data/Analytics | | | |
| CS lead | | | |

**Pre-period start date is blocked until all BLOCKING items are checked and this table is signed.**
