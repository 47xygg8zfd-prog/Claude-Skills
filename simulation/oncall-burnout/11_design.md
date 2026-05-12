# Sentinel — Design Spec
**Version**: 1.0
**Date**: 2026-05-12
**Author**: Design Lead
**Status**: Ready for Engineering Review

---

## Overview

Sentinel is an on-call intelligence platform. Its primary users are on-call engineers who need to resolve incidents faster, and engineering managers who need visibility into team health and hero dependency. This document specifies the four core screens of the MVP.

**Design principles:**
- Minimize friction during an active incident — the engineer is stressed, time matters
- Documentation must feel like it takes less than 2 minutes or engineers will skip it
- Manager views surface patterns, not surveillance — frame as team health, not individual accountability
- Every screen has a meaningful empty state — the product is new, sparse data is normal

**User personas:**
- **Alex (On-Call Engineer)**: Mid-level SWE, on-call rotation every 3rd week. Gets paged at 2am. Wants to resolve and go back to sleep. Hates filling out postmortems.
- **Jordan (Engineering Manager)**: EM for a 12-person team. Worried about burnout on 2-3 engineers who handle 70% of incidents. Wants to build knowledge redundancy.

---

## Screen 1: Incident Response View

### Purpose
When an engineer receives a page, Sentinel surfaces everything they need to start investigating: what fired, who has resolved this before, and what runbook they used. This is the "first 90 seconds" screen.

### Jobs to be Done
"When I get paged, show me who fixed this last time and what they did, so I don't start from zero."

### Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│ SENTINEL                                    🔴 ACTIVE INCIDENT       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │ [HIGH] payments-service — High Error Rate                    │    │
│  │ Alert: error_rate > 5% for 3min  │  Service: payments-svc    │    │
│  │ Triggered: 2026-05-12 02:14 UTC  │  Env: production          │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                       │
│  SUGGESTED RESOLVER                                                   │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  ● Priya Kapoor                          Confidence: 91%     │    │
│  │    Senior SWE — Payments Team                                │    │
│  │    On-call: YES (primary)                                    │    │
│  │    Resolved this alert type 7× (last: 3 days ago)           │    │
│  │                                                              │    │
│  │    [Assign to Priya]          [Assign to Someone Else ↓]    │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                       │
│  SIMILAR PAST INCIDENTS                                              │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  INC-4821  │  2026-05-09  │  Resolved by Priya K.  │  18min │    │
│  │  ▶ View runbook: "payments-svc high error rate — DB pool"   │    │
│  ├─────────────────────────────────────────────────────────────┤    │
│  │  INC-4703  │   2026-04-28  │  Resolved by Marcus T. │  34min │    │
│  │  ▶ View runbook: "payments-svc error spike — deploy rollbk" │    │
│  ├─────────────────────────────────────────────────────────────┤    │
│  │  INC-4441  │   2026-04-01  │  Resolved by Priya K.  │  22min │    │
│  │  ▶ View runbook: "payments-svc high error rate — DB pool"   │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                       │
│  RELATED COMMITS (last 24h on payments-svc)                         │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  a3f92c1  deploy: bump connection pool max (Marcus T., 6h)  │    │
│  │  c881de4  fix: retry logic on payment processor timeout      │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                       │
│                              [Close Incident]  [Escalate]           │
└─────────────────────────────────────────────────────────────────────┘
```

### Component Breakdown

**Alert Header**
- Alert title, severity badge (HIGH/MEDIUM/LOW, color-coded: red/amber/green)
- Service name, environment, trigger condition, time since firing
- Pulls from PagerDuty/OpsGenie incident payload

**Suggested Resolver Card**
- Name, role, team
- On-call status: YES/NO with schedule source ("primary" or "secondary")
- Resolution history for this exact alert type (count + recency)
- Confidence score: percentage, derived from routing engine weighted score
- Two CTAs: assign to suggested resolver, or open a dropdown to override
- Override dropdown lists team members sorted by routing score descending

**Similar Past Incidents**
- Up to 5 most similar incidents (by alert type + service)
- Each row: incident ID, date, resolver name, MTTR
- Inline runbook link — opens runbook in a side panel (not a full navigation away)
- "Last resolved by [name] 3 days ago — view runbook" pattern for the top match

**Related Commits**
- GitHub integration: commits to this service's repo in the last 24 hours
- Short SHA, commit message, author, time ago
- Links to GitHub diff
- If no commits: section is hidden (not shown as empty)

### States

| State | Behavior |
|---|---|
| No routing history | Suggestion card shows "No history yet — assign manually" with full team dropdown |
| Engineer not on-call | Confidence score shown but badge reads "Not currently on-call" |
| No similar incidents | Section replaced with "No similar past incidents found. This may be a new alert type." |
| No GitHub integration | Related commits section not rendered |
| Incident already assigned | Shows "Assigned to [name]" with option to reassign |

### Accessibility
- Severity badge conveys meaning with both color and text label (not color alone)
- Confidence percentage has aria-label: "Routing confidence: 91 percent"
- Side panel for runbook view is keyboard-accessible (Tab, Escape to close)
- All interactive elements meet 4.5:1 contrast ratio minimum
- Focus returns to "View runbook" trigger when side panel closes

---

## Screen 2: Runbook Capture Modal

### Purpose
Appears when the engineer clicks "Close Incident." Captures structured knowledge before the incident fades from memory. Must be completable in under 2 minutes. Pre-population reduces friction.

### Jobs to be Done
"When I close an incident, let me quickly document what I did so the next engineer doesn't start from scratch — without it feeling like a postmortem."

### Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│  ╔═══════════════════════════════════════════════════════════════╗  │
│  ║  Document This Incident                              [✕ Skip] ║  │
│  ║  INC-4901 — payments-service High Error Rate                  ║  │
│  ║  Resolved in: 23 min                                          ║  │
│  ╠═══════════════════════════════════════════════════════════════╣  │
│  ║                                                               ║  │
│  ║  What caused this?                                            ║  │
│  ║  ┌─────────────────────────────────────────────────────────┐ ║  │
│  ║  │ DB connection pool exhausted after deploy a3f92c1       │ ║  │
│  ║  │ bumped max_connections without updating pool config.    │ ║  │
│  ║  └─────────────────────────────────────────────────────────┘ ║  │
│  ║                                                               ║  │
│  ║  Steps you took  (auto-detected from terminal session)        ║  │
│  ║  ┌─────────────────────────────────────────────────────────┐ ║  │
│  ║  │ ✓ kubectl get pods -n payments                          │ ║  │
│  ║  │ ✓ kubectl describe pod payments-svc-7d9f-x2k            │ ║  │
│  ║  │ ✓ psql -c "SELECT count(*) FROM pg_stat_activity"       │ ║  │
│  ║  │ ✓ Updated POOL_MAX_SIZE env var → 25                    │ ║  │
│  ║  │ ✓ kubectl rollout restart deployment/payments-svc       │ ║  │
│  ║  │                                                         │ ║  │
│  ║  │ + Add step                                              │ ║  │
│  ║  └─────────────────────────────────────────────────────────┘ ║  │
│  ║                                                               ║  │
│  ║  Services affected                                            ║  │
│  ║  ┌─────────────────────────────────────────────────────────┐ ║  │
│  ║  │ ● payments-svc  ● checkout-api  + Add service           │ ║  │
│  ║  └─────────────────────────────────────────────────────────┘ ║  │
│  ║                                                               ║  │
│  ║  How to prevent this next time?  (optional)                   ║  │
│  ║  ┌─────────────────────────────────────────────────────────┐ ║  │
│  ║  │ Add pool config to deploy checklist. Alert on pool      │ ║  │
│  ║  │ utilization > 80% before exhaustion.                    │ ║  │
│  ║  └─────────────────────────────────────────────────────────┘ ║  │
│  ║                                                               ║  │
│  ║  ┌───────────────┐                                            ║  │
│  ║  │ Runbook type  │  ○ New runbook  ◉ Update existing         ║  │
│  ║  │               │  Updating: "payments-svc high error rate" ║  │
│  ║  └───────────────┘                                            ║  │
│  ║                                                               ║  │
│  ║               [Save & Close Incident]   [Skip for now]        ║  │
│  ╚═══════════════════════════════════════════════════════════════╝  │
└─────────────────────────────────────────────────────────────────────┘
```

### Component Breakdown

**Modal Header**
- Incident title and ID
- Time-to-resolution shown as positive reinforcement ("Resolved in: 23 min")
- Skip option is visible but not prominent — we want completion, not guilt

**What caused this? (required)**
- Free-text, 3-line textarea
- Character limit: 1000. Counter shows at 800.
- Placeholder: "Briefly describe the root cause"

**Steps you took (required, pre-populated)**
- Ordered list of steps
- Auto-detection: Sentinel receives terminal commands via a lightweight browser extension (future scope). At MVP, engineer types or pastes steps.
- At MVP launch: field pre-populated with empty ordered list (3 blank entries) to prompt structured thinking
- Each step is editable inline. Drag to reorder. Delete icon per step.
- "+ Add step" button appends a new empty row

**Services affected (required, pre-populated)**
- Pills/chips for services
- Auto-populated from: (1) services in the original alert payload, (2) services mentioned in related commits
- Engineer can add or remove
- Backed by autocomplete from the `services` catalog

**How to prevent this next time? (optional)**
- Free-text, 3-line textarea
- Explicitly labeled optional to reduce anxiety
- If filled, this field is indexed separately for "prevention" queries in runbook search

**Runbook type**
- Radio: "New runbook" or "Update existing"
- Default: if pgvector finds an existing runbook with similarity score > 0.85, default to "Update existing" and show the matched runbook title
- If "Update existing" selected, shows diff preview before save (future scope — v1.1)

**Save & Close CTA**
- Primary button: saves runbook, closes incident in Sentinel, fires `incident.closed` event back to PagerDuty/OpsGenie via API
- "Skip for now": closes incident without runbook. Logs `runbook_skipped` event. After 3 skips, a nudge appears: "3 incidents without runbooks — your team is missing context."

### States

| State | Behavior |
|---|---|
| Existing similar runbook found | "Update existing" pre-selected, matched runbook title shown |
| No similar runbook | "New runbook" pre-selected |
| Steps auto-detected (future) | Steps list pre-filled with detected commands, each with a checkbox to include/exclude |
| Form validation error | Inline error below the offending field. Save button disabled until resolved. |
| Save in progress | Save button shows spinner, text changes to "Saving…" |
| Save successful | Modal closes. Toast: "Runbook saved. INC-4901 closed." |
| Save failed | Error banner at top of modal: "Failed to save. Try again or skip." |

### Accessibility
- Modal traps focus while open (focus ring on first input on open)
- Escape key triggers "Skip for now" behavior with a confirmation: "Skip documentation for this incident?"
- All form fields have associated `<label>` elements
- Step list is `<ol>` with `role="list"` — screen reader announces "Step 1 of 5"
- "Skip for now" is a secondary button, not a link, so it appears in tab order
- Error messages are `role="alert"` so screen readers announce them immediately

---

## Screen 3: Runbook Library

### Purpose
Central searchable knowledge base for the team. Engineers look here before diving into an unfamiliar incident. Managers use it to audit knowledge coverage.

### Jobs to be Done
"When I'm facing an alert I haven't seen before, let me find what my teammates already know about it."

### Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│ SENTINEL  /  Runbook Library                                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌─────────────────────────────────────────────┐  [+ New Runbook]   │
│  │ 🔍  Search runbooks...                       │                    │
│  └─────────────────────────────────────────────┘                    │
│  Filter by:  [Service ▼]  [Alert Type ▼]  [Author ▼]  [Clear]      │
│                                                                       │
│  ⚠️  Coverage gaps: 12 alert types have no runbook  [View gaps →]   │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │ payments-svc — High Error Rate (DB Pool)                    │    │
│  │ Service: payments-svc  │  Alert type: high_error_rate       │    │
│  │ Last updated: 2026-05-12 by Priya K.  │  Used 7×           │    │
│  │ Avg MTTR with runbook: 19 min  vs  without: 41 min          │    │
│  │ Resolution success rate: 86%                                │    │
│  │                                          [View]  [Edit]     │    │
│  ├─────────────────────────────────────────────────────────────┤    │
│  │ auth-service — Token Validation Failures                    │    │
│  │ Service: auth-svc  │  Alert type: validation_failure_spike  │    │
│  │ Last updated: 2026-04-30 by Marcus T.  │  Used 3×           │    │
│  │ Avg MTTR with runbook: 24 min  vs  without: 55 min          │    │
│  │ Resolution success rate: 100%                               │    │
│  │                                          [View]  [Edit]     │    │
│  ├─────────────────────────────────────────────────────────────┤    │
│  │ order-service — Queue Depth Spike               ⚠️ STALE   │    │
│  │ Service: order-svc  │  Alert type: queue_depth_critical     │    │
│  │ Last updated: 2025-11-14 by Dana L.  │  Used 12×           │    │
│  │ Avg MTTR with runbook: 31 min  vs  without: 62 min          │    │
│  │ Resolution success rate: 58%  ← low                        │    │
│  │                                          [View]  [Edit]     │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                       │
│  Showing 1–20 of 47 runbooks   [< Prev]  Page 1 of 3  [Next >]      │
└─────────────────────────────────────────────────────────────────────┘
```

### Component Breakdown

**Search Bar**
- Full-text search across: runbook title, body content, service name, alert type, prevention notes
- Backed by `pg_trgm` trigram search at MVP; pgvector semantic search added in v1.1
- Results update on keypress with 300ms debounce
- Search highlights matching terms in results

**Filters**
- Service: dropdown, multi-select, populated from services catalog
- Alert type: dropdown, multi-select, populated from distinct alert types seen in incident history
- Author: dropdown, populated from engineers table
- Active filters shown as removable chips above results
- Filter state is persisted in URL query params for shareability

**Coverage Gap Banner**
- Shown only when gaps exist
- "12 alert types have no runbook" — count updates in real time
- "View gaps" links to a filtered view showing alert types with incident history but no associated runbook
- Banner dismisses per-user for 7 days if clicked away

**Runbook Card**
- Title: runbook name (editable)
- Service + alert type tags
- Last updated: date + author name
- Usage count: number of incidents this runbook was opened during
- MTTR comparison: "with runbook" vs "without runbook" — this is the headline metric, shows value of documentation
- Resolution success rate: % of incidents where this runbook was used and resolved without escalation
- Stale badge: shown if last updated > 180 days ago
- Low success rate indicator: shown if success rate < 65%

**Runbook Detail (side panel, opened via View)**
- Full markdown render of runbook content
- Structured sections: Root Cause, Steps, Services Affected, Prevention
- Edit button opens inline edit mode (markdown editor)
- Version history link (v1.1)

### States

| State | Behavior |
|---|---|
| No runbooks yet | Empty state: illustration + "No runbooks yet. They'll appear here after engineers close their first incidents." + [Create Runbook manually] button |
| Search returns no results | "No runbooks match '[query]'. Try different keywords or [create one manually]." |
| All alert types have runbooks | Coverage gap banner is hidden |
| Runbook has never been used in an incident | Usage count shows "0×" with tooltip "This runbook hasn't been linked to a resolved incident yet" |

### Accessibility
- Search results region has `aria-live="polite"` for screen reader announcements
- Stale badge has tooltip with full explanation on hover/focus
- Cards are keyboard-navigable with Tab; Enter opens detail panel
- Filter dropdowns follow ARIA combobox pattern

---

## Screen 4: Hero Dependency Index Dashboard

### Purpose
Manager-facing view showing how evenly incident resolution load is distributed across the team. Primary goal: identify engineer burnout risk before it becomes attrition.

### Jobs to be Done
"When I'm running a team review, show me if we have a hero dependency problem and who is carrying disproportionate load — before they burn out."

### Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│ SENTINEL  /  Team Health  /  Hero Dependency Index                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Time range:  [Last 30 days ▼]   Team:  [Payments Team ▼]          │
│                                                                       │
│  ┌───────────────────────────────┐  ┌────────────────────────────┐  │
│  │  Hero Dependency Index        │  │  Team Health Score         │  │
│  │                               │  │                            │  │
│  │         64%                   │  │        ● AT RISK           │  │
│  │    ⚠️  HIGH                   │  │                            │  │
│  │                               │  │  HDI above 50% threshold   │  │
│  │  Target: < 30%                │  │  2 engineers resolving     │  │
│  │  Last period: 71%  ▼ -7pp     │  │  68% of all incidents      │  │
│  └───────────────────────────────┘  └────────────────────────────┘  │
│                                                                       │
│  INCIDENT RESOLUTIONS BY ENGINEER  (last 30 days)                   │
│                                                                       │
│   Priya K.  ████████████████████████████████████  42  (38%)  ⚠️    │
│   Marcus T. ████████████████████████  30  (27%)  ⚠️               │
│   Dana L.   █████████████  16  (14%)                               │
│   Sam R.    ██████████  12  (11%)                                   │
│   Yuki M.   ███████  8   (7%)                                       │
│   Amir C.   ████  4   (4%)  ← joined 3 weeks ago                  │
│                                                                       │
│  TREND — HDI over time                                               │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  %                                                           │    │
│  │  80 ┤                                                        │    │
│  │  70 ┤  ●────●                                               │    │
│  │  60 ┤          ●────●────●                                  │    │
│  │  50 ┤ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ threshold                     │    │
│  │  40 ┤                          ●────●                       │    │
│  │  30 ┤                                  ●  ← target          │    │
│  │  20 ┤                                                        │    │
│  │     └──┬──────┬──────┬──────┬──────┬──────┬──────┬─────    │    │
│  │       Nov    Dec    Jan    Feb    Mar    Apr    May          │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                       │
│  RUNBOOK COVERAGE BY ENGINEER                                        │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │ Engineers who contributed runbooks this period:  3 of 6     │    │
│  │ Priya K.: 5 runbooks  Marcus T.: 2 runbooks  Dana L.: 1     │    │
│  │                                                             │    │
│  │ Tip: Low runbook contribution from Sam, Yuki, Amir may      │    │
│  │ indicate they haven't been primary resolver on complex       │    │
│  │ incidents yet — or that runbook capture needs encouragement. │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                       │
│                               [Export CSV]  [Share Dashboard Link]  │
└─────────────────────────────────────────────────────────────────────┘
```

### Component Breakdown

**Controls**
- Time range selector: Last 30 days / Last 60 days / Last 90 days / Custom range
- Team selector: populated from PagerDuty/OpsGenie team/service hierarchy
- Selections update all panels simultaneously

**Hero Dependency Index Card**
- Definition: HDI = percentage of total incidents resolved by the top N engineers, where N = 20% of team (rounded up). For a 6-person team, top 2 engineers. For a 10-person team, top 2 engineers.
- Current value displayed large (64%)
- Severity label: LOW (<30%), MODERATE (30–50%), HIGH (>50%), CRITICAL (>70%)
- Target threshold: 30% (configurable by org admin in settings)
- Period-over-period delta: "Last period: 71% ▼ -7pp" — improvement framed positively

**Team Health Score Card**
- Qualitative summary: HEALTHY / AT RISK / CRITICAL
- Derived from HDI + trend direction + runbook coverage
- Plain English explanation of the score (not a black box)

**Incident Resolutions Bar Chart**
- Horizontal bars, sorted descending by count
- Each bar: engineer name, bar (width proportional to % of total), count, percentage
- Warning icon for engineers above the threshold (top 20% of team carrying >50%)
- Contextual annotation for new hires: "joined 3 weeks ago" to avoid misinterpretation
- Tooltip on hover: breakdown by alert type for that engineer

**HDI Trend Line Chart**
- Line chart, one data point per week
- Dashed horizontal line at threshold (30% target)
- Goal line at 30%
- Hovering a data point shows: exact HDI%, week range, top resolver that week

**Runbook Coverage Panel**
- Count of engineers who contributed runbooks in the period
- Names and counts
- Framing tip: contextualizes low contribution as potentially structural, not personal — avoids the dashboard becoming a performance tool

### States

| State | Behavior |
|---|---|
| Team just connected, no data | Empty state: "No incident data yet. Sentinel needs at least 10 resolved incidents to calculate HDI. Come back in a few days." |
| HDI > 70% | HDI card turns red. Page-level alert banner: "Critical hero dependency detected. Consider immediate rotation review." |
| HDI < 30% | HDI card turns green. Celebratory micro-copy: "Great distribution. Keep it up." |
| Single engineer team | HDI not calculated. Notice: "HDI requires at least 3 engineers on the rotation." |
| Custom time range with insufficient data | Warning: "Fewer than 10 incidents in this range. HDI may not be statistically meaningful." |

### Accessibility
- Color coding is supplemented by text labels (HIGH, AT RISK) — never color alone
- Bar chart has `role="img"` with comprehensive `aria-label` summary
- All chart data is also available as a summary table below the chart (visually hidden by default, shown via "View as table" toggle)
- Export CSV ensures data is accessible outside the visual interface
- Dashboard link shares state via URL params (time range + team)

---

## Design Tokens

| Token | Value | Usage |
|---|---|---|
| `--color-critical` | `#D32F2F` | HDI critical, high severity alerts |
| `--color-warning` | `#F57C00` | HDI high, stale runbooks, warning states |
| `--color-success` | `#388E3C` | HDI healthy, incident resolved |
| `--color-info` | `--204A8F` | Suggestions, informational banners |
| `--color-surface` | `#F8F9FA` | Card backgrounds |
| `--radius-card` | `8px` | All cards and modals |
| `--font-mono` | `JetBrains Mono, monospace` | Command steps in runbooks |

---

## Open Questions

1. **Runbook auto-population at MVP**: We spec'd manual entry for steps. Do we ship with the browser extension skeleton at launch, even if it's opt-in? Blocking question for eng scope.
2. **HDI definition edge cases**: What happens when an engineer is on an incident as secondary/observer — does that count toward their resolution count? Recommend: only primary resolver counts.
3. **Skip friction**: Three skips before the nudge — is that the right threshold? CS team input needed.
4. **Runbook diff view**: Deferred to v1.1. Need to confirm design for the diff experience before that sprint.
