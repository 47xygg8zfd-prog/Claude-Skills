---
name: analytics
description: >
  Define, validate, and audit product analytics instrumentation. Use this skill when
  the user needs to define which events to track, validate that a metric is measurable
  given current instrumentation, audit an event schema for completeness, write analytics
  queries, or troubleshoot missing or incorrect data. Also trigger when the user says things
  like "what events should we track", "is this metric measurable", "our numbers look wrong",
  "validate our instrumentation plan", "write a query for", or "what data do we have on X".
  Works from a PRD, spec, event schema, or raw SQL/event log.
---

# Analytics Skill

Define what to measure, verify it's measurable, and write the queries to prove it.
Good instrumentation is a product requirement, not an afterthought.

## When to Use

- During PRD or spec review — to validate that success metrics have a clear event path
- Before a sprint starts — to confirm instrumentation is spec'd before engineers build
- After launch — to audit whether events are firing correctly
- When metrics look wrong — to trace a number back to its source event
- When writing a measurement plan — to produce an instrumentation table and SQL

---

## The Metrics Validation Protocol

Before accepting any metric as measurable, run it through these four checks:

**1. Event exists?**
Is there an event (or will there be one) that fires when this behavior occurs?
If no: the metric is unmeasurable. Add the event to the spec before writing SQL.

**2. Properties sufficient?**
Does the event carry all the properties needed to calculate this metric?
(user_id for per-user metrics, account_id for account-level, timestamp always)
If no: spec the missing properties. They can't be added retroactively to historical data.

**3. Firing correctly?**
Does the event fire on all platforms (web, iOS, Android) and in all relevant flows?
Events that only fire on web will undercount mobile-heavy features by 40-60%.

**4. Deduplication story?**
Can the same event fire twice for the same action? (double-taps, retries, page reloads)
If yes: define the deduplication key before writing the query.

---

## Output Formats

### 1. Instrumentation Plan (`instrumentation`)
For each metric in the PRD, produce:

| Metric | Event name | Fires when | Required properties | Platform coverage | Dedup key |
|--------|-----------|-----------|-------------------|-----------------|---------|
| [metric] | `event_name` | [specific trigger] | `user_id`, `[prop]: type` | Web / iOS / Android | `(user_id, session_id)` |

Flag any metric that fails the validation protocol:
```
UNMEASURABLE: [metric name]
Missing: [event / property / platform coverage]
Fix: [what needs to be added to the spec or implementation]
```

### 2. SQL Queries (`sql`)
For each metric, write exact SQL with:
- Table and column names from the known data model
- A comment explaining what the query measures
- A "Caveats" comment listing limitations (timezone, dedup assumptions, etc.)
- A "Sanity check" query to verify the result is plausible

```sql
-- [Metric name]
-- Measures: [what this captures and for which user population]
-- Caveats: [UTC timezone; counts page_view not unique sessions; etc.]
SELECT
    DATE_TRUNC('week', event_time) AS week,
    COUNT(DISTINCT user_id)        AS [metric_name]
FROM events
WHERE event_type = 'event_name'
  AND event_time >= '2026-01-01'
GROUP BY 1
ORDER BY 1;

-- Sanity check: this should be within 20% of your manual estimate
SELECT COUNT(DISTINCT user_id) FROM events WHERE event_type = 'event_name';
```

### 3. Audit Report (`audit`)
Given a list of events or an existing schema, flag issues:

| Issue | Severity | Event | Problem | Fix |
|-------|---------|-------|---------|-----|
| Missing user_id | P0 | `explanation_generated` | Can't attribute to a user | Add `user_id` property |
| Fires on retry | P1 | `form_submitted` | Counts can be inflated | Deduplicate by `(user_id, form_id, day)` |
| Mobile not firing | P0 | `session_start` | 40% undercount on mobile | Add SDK call to mobile app |

### 4. Metric Dictionary (`dictionary`)
A reference document for a team's core metrics:

**[Metric Name]**
- **Definition**: [Exact calculation — numerator / denominator / window]
- **Owner**: [Team responsible for accuracy]
- **Source event**: `event_name`
- **SQL**: [Link or inline]
- **Baseline**: [Current value]
- **Last validated**: [Date]
- **Known issues**: [Any known data quality gaps]

---

## Analytics Quality Rules

- A metric without a source event is a wish, not a metric
- Every property must have a type (`string`, `integer`, `boolean`, `uuid`) — untyped schemas produce inconsistent data
- Backfilling is expensive and often impossible — get instrumentation right before launch, not after
- If a metric requires a JOIN across more than 3 tables, it's probably not a primary metric — reconsider the definition
- Test events in staging before launch: fire the event manually, verify it appears in the event stream with correct properties

---

## Integration Points

- Use after the **PRD** skill to validate that success metrics are actually measurable
- Use alongside **spec-driven-dev** to ensure events are in the spec before engineers build
- Use with **data-scientist** to connect instrumentation to measurement plans and SQL
- Use with **experiment-design** to verify baseline data exists before committing to a test
