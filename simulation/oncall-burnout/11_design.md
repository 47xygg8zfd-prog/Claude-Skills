# Sentinel — Design Spec
**Version**: 1.0  
**Date**: 2026-05-12  
**Author**: Design Lead  
**Status**: Ready for Engineering Review

---

## Overview

Sentinel is an on-call intelligence platform. It reduces MTTR by surfacing relevant runbooks and suggesting resolvers at alert time, and reduces documentation debt by capturing runbooks at incident close.

**Primary user**: On-call engineer  
**Secondary user**: Engineering manager

---

## Jobs to Be Done

| User | Job | Success Condition |
|------|-----|-------------------|
| On-call engineer | When I get a page, help me resolve it fast | Suggested resolver + relevant runbook visible within 3 seconds of alert |
| On-call engineer | When I close an incident, make documenting take <2 minutes | Runbook capture modal pre-populated; submit in under 2 min |
| Engineering manager | Identify who is carrying disproportionate on-call load | HDI dashboard shows individual and team trends; alerts trigger at HDI > 50% |

---

## Design Principles

1. **Zero friction at 3am** — every interaction must work under cognitive load. No multi-step flows, no jargon, no decisions required.
2. **Pre-populate everything** — Sentinel detects context (services, commands, timeline) from the incident; engineers review and confirm, not compose from scratch.
3. **Passive by default** — nothing requires action from engineers except the runbook capture modal. All other surfaces are read-only.
4. **Explainable over clever** — routing suggestions show their reasoning ("resolved 4 similar incidents in the last 14 days"). No black boxes.

---

## Screen 1: Incident Response View

### Purpose
The primary working surface for an on-call engineer during an active incident. Appears when an engineer opens an incident in Sentinel (linked from PagerDuty/OpsGenie notification).

### User Goal
Understand the incident, identify who can best resolve it, and access prior resolution context — without switching tools.

### Layout

```
┌─────────────────────────────────────────────────────────────────┐
│ SENTINEL                                     ● ACTIVE INCIDENT  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  🔴  HIGH SEVERITY                                              │
│  payment-service: HighErrorRate                                 │
│  Triggered 4 minutes ago  ·  PagerDuty #INC-8841               │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  SUGGESTED RESOLVER                                      │   │
│  │                                                          │   │
│  │  ┌──────┐  Jamie Reyes                    89% match     │   │
│  │  │  JR  │  Senior SRE · payments team                   │   │
│  │  └──────┘                                               │   │
│  │                                                          │   │
│  │  Why: Resolved 6 similar incidents in the last 30 days  │   │
│  │  Most recent: 3 days ago · MTTR 12 min                  │   │
│  │  Status: ● On-call (primary)                            │   │
│  │                                                          │   │
│  │  [ Assign to Jamie ]      [ See all suggestions (3) ]   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  SIMILAR PAST INCIDENTS                                          │
│  ─────────────────────────────────────────────────────────────  │
│  ● INC-8712  payment-service: HighErrorRate           3d ago    │
│    Resolved by Jamie Reyes in 12 min  [ View runbook → ]        │
│                                                                  │
│  ● INC-8344  payment-service: HighErrorRate          11d ago    │
│    Resolved by Priya Nair in 34 min   [ View runbook → ]        │
│                                                                  │
│  ● INC-7901  checkout-service: ErrorBudgetBurn       18d ago    │
│    Resolved by Jamie Reyes in 18 min  [ View runbook → ]        │
│                                                                  │
│  INCIDENT DETAILS                                                │
│  ─────────────────────────────────────────────────────────────  │
│  Service       payment-service                                   │
│  Alert type    HighErrorRate                                     │
│  Severity      High                                              │
│  Environment   production                                        │
│  Runbook       No runbook attached                               │
│                                                                  │
│  RECENT COMMITS (payment-service, last 2h)                      │
│  ─────────────────────────────────────────────────────────────  │
│  a3f9c12  feat: add retry logic to payment processor  (42m ago) │
│           merged by @dana-kim → main                            │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│  [ Acknowledge ]  [ Escalate ]  [ Close Incident ]              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Component Specifications

**Suggested Resolver Card**
- Confidence score: integer 0–100, shown as percentage
- Confidence color: green ≥ 75, yellow 50–74, red < 50
- "Why" text: plain English summary of the top scoring factors (≤ 2 sentences)
- On-call status: pulled from PagerDuty Schedules API at render time (not cached)
- "See all suggestions": expands to show up to 3 ranked alternatives with scores
- Assign action: creates assignment in PagerDuty via API; does not re-route in Sentinel

**Similar Past Incidents**
- Shows top 3 by semantic similarity score (pgvector cosine similarity on alert name + service + description)
- Each row: incident ID, alert name, resolver name, MTTR, runbook link (if exists)
- "View runbook" opens runbook in a slide-over panel without leaving the page
- If no similar incidents: show "No similar incidents found. Be the first to document this alert type." with a link to create a runbook manually

**Recent Commits**
- GitHub integration: queries commits to the affected service's repo in the last 2 hours
- Shows: short SHA, commit message, author, time ago
- If GitHub integration not configured: section hidden entirely (not shown as error)
- Maximum 3 commits shown; "View all on GitHub →" link for more

**Action Bar**
- "Acknowledge": calls PagerDuty/OpsGenie acknowledge API
- "Escalate": opens escalation modal (out of scope for MVP; shown as disabled)
- "Close Incident": triggers Runbook Capture Modal (Screen 2)

### Error States
- **Routing suggestion unavailable**: "No routing suggestion available — insufficient history for this alert type." Suggestion card is shown with dimmed styling; assign-to field is a free-text search of engineers instead.
- **Similar incidents API timeout**: "Could not load similar incidents." with a retry button. Incident details and resolver suggestion still load independently.
- **PagerDuty assign fails**: Inline error in the suggestion card: "Assignment failed. Try assigning directly in PagerDuty." Do not block the rest of the page.

### Empty States
- **First-ever incident** (no historical data): Resolver card shows "No resolution history yet — routing suggestions will improve as your team resolves incidents." Full engineer directory search shown instead.
- **No runbooks in library**: Similar incidents panel shows "Your team hasn't documented any runbooks yet. Close an incident to create the first one."

### Accessibility
- Alert severity badge uses both color and text label (never color alone)
- Confidence score announced by screen reader as "89 percent confidence"
- "View runbook" links include descriptive aria-label: "View runbook for incident INC-8712"
- Keyboard navigation: Tab order follows visual flow; Assign button reachable without mouse
- Focus management: when "See all suggestions" expands, focus moves to the expanded list

---

## Screen 2: Runbook Capture Modal

### Purpose
Appears immediately when an engineer clicks "Close Incident." Captures resolution knowledge before context fades. Target completion time: under 2 minutes.

### User Goal
Document what happened and what fixed it with minimal effort. The system pre-populates everything it can detect; the engineer reviews, adjusts, and submits.

### Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  Close Incident: INC-8841                               [  ×  ] │
│  payment-service: HighErrorRate                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Before this incident is closed, capture what you learned.      │
│  This takes under 2 minutes and helps your future self.         │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  WHAT HAPPENED?                                          │   │
│  │  (Auto-detected from alert body and timeline)            │   │
│  │                                                          │   │
│  │  ┌───────────────────────────────────────────────────┐  │   │
│  │  │ Error rate on payment-service exceeded 5% for     │  │   │
│  │  │ 8 minutes. Root cause: retry logic added in       │  │   │
│  │  │ a3f9c12 caused thundering herd on payment         │  │   │
│  │  │ processor under load.                             │  │   │
│  │  └───────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  WHAT FIXED IT?  (Steps taken — add, remove, reorder)   │   │
│  │                                                          │   │
│  │  ✓  1. Checked error logs in Datadog                    │   │
│  │  ✓  2. Identified retry storm via payment-service logs  │   │
│  │  ✓  3. Rolled back commit a3f9c12 via kubectl           │   │
│  │       kubectl rollout undo deploy/payment-service       │   │
│  │  +  Add step                                            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  SERVICES AFFECTED  (Auto-detected)                      │   │
│  │  [payment-service ×]  [checkout-service ×]  [+ Add]     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  HOW WOULD YOU PREVENT THIS NEXT TIME?  (optional)       │   │
│  │  ┌───────────────────────────────────────────────────┐  │   │
│  │  │ Add load test for retry behavior before merging   │  │   │
│  │  │ payment-processor changes.                        │  │   │
│  │  └───────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  Resolution time: 22 minutes (auto-calculated)                  │
│  Resolver: You (Jamie Reyes)                                     │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  [ Close without saving ]      [ Save Runbook & Close ]         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Component Specifications

**What Happened (Auto-populated)**
- Source: alert body text + incident timeline events from PagerDuty
- If GitHub integration active: appends commit context for any commits to affected service in the incident window
- Editable freeform text; character limit 1000
- If auto-detection produces no content: field is blank with placeholder "Describe what went wrong."

**Steps Taken (Auto-populated)**
- Source: Sentinel detects command-like strings in Slack thread (if Slack integration active) and incident notes/comments from PagerDuty
- Each step is independently editable
- Engineer can: check/uncheck steps, reorder via drag, delete steps, add new steps
- Steps detected as commands (e.g., `kubectl`, `git rollout`, `psql`) are displayed in monospace and tagged as "command"
- Maximum 20 steps; if more detected, show first 20 with "Show X more" toggle

**Services Affected (Auto-populated)**
- Source: PagerDuty service field + any services mentioned in alert title/body that match known services in Sentinel
- Shown as removable chips; engineer can add from a typeahead of all known services
- Minimum 1 service required for submission

**Prevention (Optional)**
- Freeform text; character limit 500
- Placeholder: "What would prevent this from happening again?"
- This field is optional; does not block submission

**Footer**
- Resolution time: computed from incident trigger time to current time; shown read-only
- Resolver: defaults to currently authenticated user; can be changed via typeahead (for situations where another engineer resolved but is not logged in)
- "Close without saving": closes incident in PagerDuty/OpsGenie without creating a runbook; requires confirmation: "Are you sure? This incident will have no runbook. You can add one later from the Runbook Library."
- "Save Runbook & Close": disabled until "Services Affected" has at least one entry and "What Happened" is non-empty

### Error States
- **Save fails (network)**: "Failed to save runbook. Your notes are preserved — try again." The modal stays open; content is persisted in localStorage.
- **Incident already closed externally**: "This incident was closed in PagerDuty. You can still add a runbook retroactively." Save button text changes to "Save Runbook."
- **Auto-detection produces garbled output**: Each auto-populated field has an "Reset to blank" link below it, allowing the engineer to discard detection and start fresh.

### Empty States
- **No PagerDuty notes, no Slack, no GitHub**: All fields blank. Placeholder text only. Still functional — engineer writes from scratch.

### Accessibility
- Modal is aria-modal; focus trapped within modal while open
- Escape key closes modal (triggers "close without saving" confirmation)
- Drag-and-drop step reordering has keyboard alternative: up/down arrow buttons on each step
- Auto-populated content announced by screen reader: "Steps pre-filled from incident data. Review before submitting."
- Required fields labeled with both asterisk and aria-required

---

## Screen 3: Runbook Library

### Purpose
Searchable knowledge base of all captured runbooks. Engineers use it proactively before going on-call, and reactively during incidents. Managers use it to identify coverage gaps.

### Layout and Components

**Search Bar**
- Full-width at top of page
- Searches: alert name, service name, runbook body content, tags
- Powered by pgvector similarity search on the backend; returns fuzzy matches
- Typeahead suggests services and alert types as the user types

**Coverage Gap Banner**
- Shown when > 0 alert types have fired in the last 30 days with no associated runbook
- Text: "12 alert types have no runbook — [View gaps →]"
- "View gaps" filters the table to show only alerts with no runbook coverage

**Runbook Table**
| Column | Description |
|--------|-------------|
| Alert type | Name of the alert (e.g., `payment-service: HighErrorRate`) |
| Service | Affected service |
| Last updated | Date and author |
| Runbook coverage | Yes / No badge |
| Resolution success rate | % of incidents using this runbook that resolved without escalation |
| Avg MTTR with runbook | Minutes — compared inline to avg MTTR without runbook |
| Actions | View, Edit, Archive |

**MTTR Comparison**
- Each runbook entry shows: "MTTR: 14 min (with runbook) vs. 38 min (without runbook)"
- Color-coded: green if runbook reduces MTTR by >20%, yellow 0–20%, red if no improvement
- Calculated from `incident_resolutions` table; shown as "N/A" if fewer than 3 data points

**Runbook Detail View**
- Opens as full-page view (not modal)
- Shows: alert type, affected services, last updated by, resolution steps, "What happened" description, prevention notes
- Edit button: opens inline edit mode with same form fields as Runbook Capture Modal
- Version history: shows last 5 versions with diff and author name
- "Run Drill" button (future, shown as disabled in MVP): would allow team to practice runbook in a sandbox

### Error States
- **Search returns no results**: "No runbooks found for '[query]'. [Create a runbook for this alert type →]"
- **Library is empty**: "No runbooks yet. Runbooks are created automatically when engineers close incidents." with a link to manually create the first runbook.

### Empty States
- **New workspace, no incidents yet**: Full-page empty state with illustration; "Runbooks appear here after your first on-call incident is resolved."

### Accessibility
- Table is keyboard-navigable with proper `role="grid"` and row focus management
- MTTR comparison color coding supplemented with text labels ("improved", "no change", "worsened")
- Search results update announced via aria-live region

---

## Screen 4: Hero Dependency Index Dashboard

### Purpose
Gives engineering managers visibility into unequal on-call load distribution. Designed to prompt action, not just observation — triggers alerts when HDI exceeds 50%.

### Layout and Components

**Page Header**
- Team selector (if manager oversees multiple teams)
- Time range selector: 30 days / 60 days / 90 days (default 30 days)
- Last updated timestamp

**Team Health Score**
- Prominent card at top: "Team HDI: 64%" in large text
- Subtitle: "1 engineer resolved 64% of incidents in the last 30 days. Healthy target: <30%."
- Color: red > 50%, yellow 30–50%, green < 30%
- Trend arrow: up/down vs. previous period with percentage change

**HDI Bar Chart**
- X-axis: engineers on the team
- Y-axis: percentage of total incidents resolved (0–100%)
- Horizontal reference line at 30% (healthy threshold)
- Horizontal reference line at 50% (alert threshold)
- Bars color-coded by individual HDI: green < 30%, yellow 30–50%, red > 50%
- Hovering on a bar: tooltip shows engineer name, incident count, avg MTTR, top 3 alert types

**Trend Line (secondary chart)**
- Line chart showing team HDI score over the selected time period
- One line per top-5 engineers (by incident count)
- Helps manager see if load is converging or diverging over time

**Alert Banner**
- Shown when any engineer's HDI > 50% for the selected period
- "Jamie Reyes resolved 64% of incidents in the last 30 days. Consider redistributing on-call rotations or cross-training."
- Dismissible per engineer per period; re-surfaces if HDI stays elevated

**Incident Breakdown Table**
| Column | Description |
|--------|-------------|
| Engineer | Name |
| Incidents resolved | Count |
| % of team total | HDI contribution |
| Avg MTTR | Minutes |
| Most common alert type | Top alert by count |
| On-call weeks | Number of primary on-call weeks in period |

**Export**
- "Export CSV" button: exports the breakdown table for the selected time range and team

### Error States
- **No incident data for selected period**: "No incidents were recorded for this team in the last 30 days." Show empty chart with axes visible.
- **PagerDuty sync failed**: Banner at top: "Schedule data may be outdated. Last synced: 2 days ago." Chart still loads from cached data.

### Empty States
- **New team, no incidents**: "No on-call data yet. Connect PagerDuty or OpsGenie to start tracking incident distribution."

### Accessibility
- Charts use `<canvas>` with aria-label describing the chart and its key finding: "Bar chart: Jamie Reyes resolved 64% of team incidents in the last 30 days."
- All chart data available in the table below (not chart-only)
- Alert banner color supplemented with icon (warning triangle) and text
- Color-blind safe palette: uses blue/orange instead of red/green where possible; green/yellow/red retained for severity but paired with text labels

---

## Interaction Flows

### Critical Path: Engineer receives alert → resolves → documents

```
PagerDuty alert fires
        │
        ▼
Engineer opens Sentinel link (deep-link from PagerDuty notification)
        │
        ▼
Incident Response View loads (Screen 1)
  ├── Routing suggestion displayed (< 500ms)
  ├── Similar incidents loaded (< 200ms)
  └── GitHub commits loaded (async, < 2s)
        │
        ▼
Engineer reviews suggestion, assigns to Jamie (or self)
        │
        ▼
Incident is resolved (actions taken outside Sentinel, or acknowledged in-app)
        │
        ▼
Engineer clicks "Close Incident"
        │
        ▼
Runbook Capture Modal appears (Screen 2)
  ├── Fields pre-populated from incident data
  └── Engineer reviews, edits, submits (< 2 min target)
        │
        ▼
Runbook saved → Incident closed in PagerDuty/OpsGenie
        │
        ▼
Runbook appears in library (Screen 3)
HDI data updated for manager view (Screen 4)
```

---

## Design Tokens

| Token | Value | Usage |
|-------|-------|-------|
| `color-severity-high` | `#D93025` | High severity alerts |
| `color-severity-medium` | `#F29900` | Medium severity alerts |
| `color-severity-low` | `#1A73E8` | Low severity alerts |
| `color-hdi-healthy` | `#1E8E3E` | HDI < 30% |
| `color-hdi-warning` | `#F29900` | HDI 30–50% |
| `color-hdi-critical` | `#D93025` | HDI > 50% |
| `font-mono` | `JetBrains Mono, monospace` | Command display in runbooks |
| `border-radius-card` | `8px` | Cards and modals |
| `shadow-modal` | `0 8px 32px rgba(0,0,0,0.18)` | Modal overlay shadow |

---

*Next: Architecture Document (File 12)*
