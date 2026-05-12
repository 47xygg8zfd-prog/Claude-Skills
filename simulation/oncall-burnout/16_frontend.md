# File 16 — Frontend Implementation Plan
**Product**: Sentinel — On-Call Intelligence Platform  
**Date**: 2026-05-12  
**Stack**: React (TypeScript), Recharts, custom hooks, REST + WebSocket  

---

## Component Tree

```
<App>
  ├── <AppShell>                        # Nav, sidebar, auth context
  │   ├── <IncidentResponseView>        # /incidents
  │   │   ├── <IncidentFeed>            # Real-time list, WebSocket-connected
  │   │   │   └── <IncidentCard>        # Per-incident row
  │   │   │       ├── <RoutingSuggestion>   # Suggested assignee + confidence
  │   │   │       └── <IncidentActions>     # Acknowledge / Close buttons
  │   │   └── <RunbookCaptureModal>     # Triggered on Close — blocks completion
  │   │       ├── <TemplateSelector>    # Dropdown: service-outage / perf / security / other
  │   │       ├── <CaptureForm>         # Controlled fields
  │   │       └── <SkipCapture>         # Explicit skip with required reason
  │   │
  │   ├── <RunbookLibraryView>          # /runbooks
  │   │   ├── <RunbookSearch>           # Debounced full-text + similarity search
  │   │   │   ├── <SearchInput>
  │   │   │   ├── <SimilarityResults>   # pgvector-ranked results
  │   │   │   └── <RunbookCard>         # Collapsed/expanded runbook entry
  │   │   └── <RunbookFilters>          # Service, tag, author, date filters
  │   │
  │   └── <HDIDashboardView>            # /hdi
  │       ├── <TeamHealthBadge>         # At-a-glance: Healthy / At Risk / Critical
  │       ├── <HDIBarChart>             # Recharts — per-engineer incident load
  │       ├── <TimeRangeSelector>       # 7d / 30d / 90d / custom
  │       └── <HDIBreakdownTable>       # Engineer × alert-type matrix
```

---

## Key Components

### `<IncidentCard>`

**Purpose**: Renders a single incident in the feed. Drives the resolution flow that leads to runbook capture.

**Props**:
```typescript
interface IncidentCardProps {
  incident: Incident;                  // Full incident object from API
  onAcknowledge: (id: string) => void;
  onClose: (id: string) => void;       // Opens RunbookCaptureModal; does NOT resolve until modal completes
  className?: string;
}
```

**State**:
```typescript
type IncidentCardState = 'loading' | 'active' | 'acknowledged' | 'resolving' | 'resolved';
```

| State | UI Behavior |
|-------|-------------|
| `loading` | Skeleton shimmer; no actions available |
| `active` | Red border, pulsing dot, "Acknowledge" CTA prominent |
| `acknowledged` | Amber border, assignee chip visible, "Close Incident" CTA |
| `resolving` | "Close Incident" spinner — modal open, card is dim/locked |
| `resolved` | Green checkmark, collapsed to summary row, timestamp |

**Child: `<RoutingSuggestion>`**

```typescript
interface RoutingSuggestionProps {
  suggestion: {
    engineer: Engineer;
    confidence: 'high' | 'medium' | 'low';
    reason: string;             // e.g. "Resolved 4 of 6 similar alerts in last 90d"
    alternatives: Engineer[];   // 1-2 fallbacks
  } | null;                     // null = no history available yet
  onAccept: (engineerId: string) => void;
  onOverride: (engineerId: string) => void;
}
```

Renders a chip showing suggested engineer name, confidence color (green/amber/red), and a one-line reason. Collapsible to save card space. If `suggestion` is null, renders "No routing history yet — assigning to on-call primary."

---

### `<RunbookCaptureModal>`

**Purpose**: The critical behavioral intervention. Surfaces at incident close. The engineer cannot dismiss this modal without either submitting a runbook OR explicitly choosing "Skip" with a reason. Silence is not an option.

**Props**:
```typescript
interface RunbookCaptureModalProps {
  incident: Incident;
  isOpen: boolean;
  onSubmit: (payload: RunbookPayload) => Promise<void>;
  onSkip: (reason: SkipReason, note: string) => Promise<void>;
  // No onDismiss prop — intentionally omitted. ESC key is intercepted.
}
```

**State** (internal):
```typescript
interface CaptureModalState {
  step: 'form' | 'skip-confirm' | 'submitting' | 'success' | 'error';
  formValues: RunbookFormValues;
  skipReason: SkipReason | null;
  skipNote: string;
  isDirty: boolean;             // Warn before accidental close if user has typed
  autoPopulated: {              // Fields pre-filled from incident data
    title: boolean;
    service: boolean;
    severity: boolean;
  };
}
```

**Auto-population logic**: On modal open, the following fields are pre-filled from the incident object:
- `title` → `"Resolved: {incident.title}"`
- `service` → `incident.service`
- `severity` → `incident.severity`
- `tags` → `incident.alertType` mapped to a tag set

**Skip reasons** (enum, required selection before skip is allowed):
- `duplicate` — "This is a duplicate; a runbook already exists"
- `one_off` — "This was a one-time incident, unlikely to recur"
- `no_value` — "I don't have time right now" *(tracked separately for follow-up)*
- `other` — requires free-text note (min 20 chars)

**Blocking logic**:
- ESC key is trapped while modal is open — fires `isDirty` check then shows "Are you sure? Your runbook will not be saved." with Cancel / Leave Anyway (which goes to skip-confirm, not silent dismiss).
- Clicking the overlay backdrop shows the same confirmation.
- "Close Incident" in the parent card remains disabled until `onSubmit` or `onSkip` resolves successfully.

**Submit states**:
- `submitting` — form fields disabled, spinner on Submit button, "Saving runbook…" text
- `success` — green checkmark, "Runbook saved. Incident closed." 1.5s display, then modal unmounts
- `error` — inline error banner, form re-enabled, retry available

---

### `<RunbookSearch>`

**Purpose**: Full-text and semantic similarity search over the runbook library. Primary use case: engineer paged for an unfamiliar alert looks for prior art.

**Props**:
```typescript
interface RunbookSearchProps {
  initialQuery?: string;        // Pre-populated when opened from IncidentCard
  onSelect?: (runbook: Runbook) => void;   // Used in capture modal to "copy from existing"
}
```

**Debounce**: 300ms on input. No search fired for queries under 3 characters.

**State machine**:
```
idle → loading → results | empty | error
         ↑___________________________|  (on new query)
```

| State | UI |
|-------|----|
| `idle` | Placeholder: "Search by symptom, service, or error message…" + recent searches chips |
| `loading` | Input spinner, skeleton result cards (3) |
| `results` | Ranked list. Similarity score shown as percentage badge. Exact text match highlighted. |
| `empty` | "No runbooks found for '{query}'. Be the first to write one." + CTA to create |
| `error` | "Search unavailable." + retry link. Graceful — does not block incident work. |

**Similarity results**: Results from pgvector are annotated with a relevance label ("Exact match", "Similar alert", "Same service") rather than raw cosine scores, which are not meaningful to engineers.

---

### `<HDIDashboard>`

**Purpose**: Shows Hero Dependency Index over time and per-engineer breakdown. Audience is engineering managers, not engineers — language and layout optimized for a weekly review, not real-time monitoring.

**Props**:
```typescript
interface HDIDashboardProps {
  teamId: string;
  initialTimeRange?: TimeRange;   // Default: '30d'
}
```

**`<TeamHealthBadge>`**:

| HDI Range | Label | Color | Icon |
|-----------|-------|-------|------|
| 0–30% | Healthy | Green | ✓ |
| 31–50% | At Risk | Amber | ⚠ |
| 51–100% | Critical | Red | ✗ |

Renders above the chart with plain-language context: "Your team's top engineer handled 64% of all incidents in the last 30 days. Teams below 30% rarely lose people to burnout."

**`<HDIBarChart>`** (Recharts `<BarChart>`):
- X-axis: engineer names (anonymized in screenshot exports)
- Y-axis: percentage of incidents handled
- Color: bars transition from green → amber → red based on individual load
- Reference line at 30% (target) and a second line at team average
- Hover tooltip: engineer name, count, percentage, top alert types handled
- Click-through: opens `<HDIBreakdownTable>` filtered to that engineer

**`<TimeRangeSelector>`**:
- Options: 7d, 30d, 90d, Custom (date picker)
- Changing range re-fetches via `useHDI` hook — chart re-renders with transition animation
- "Custom" triggers a `<DateRangePicker>` inline component; query fires on range selection, not on each date change

---

## Custom Hooks

### `useIncident(incidentId: string)`
```typescript
// Returns
{
  incident: Incident | null;
  isLoading: boolean;
  error: Error | null;
  acknowledge: () => Promise<void>;
  initiateClose: () => void;         // Opens modal, does not close incident
  confirmClose: (runbookId?: string) => Promise<void>;   // Final close after modal
}
```
Uses SWR with a 10s revalidation interval. WebSocket overlay for real-time state pushes during active incidents.

### `useRunbookCapture(incidentId: string)`
```typescript
// Returns
{
  autoPopulated: RunbookFormValues;
  submit: (values: RunbookFormValues) => Promise<{ runbookId: string }>;
  skip: (reason: SkipReason, note: string) => Promise<void>;
  isSubmitting: boolean;
  error: Error | null;
}
```
Optimistically marks incident as "closing" in SWR cache. Rolls back on error. Submission is idempotent — duplicate submissions within the same incident session are deduplicated server-side.

### `useRunbookSearch()`
```typescript
// Returns
{
  query: string;
  setQuery: (q: string) => void;     // Debounced internally
  results: RunbookSearchResult[];
  state: 'idle' | 'loading' | 'results' | 'empty' | 'error';
  retry: () => void;
}
```
Calls `GET /api/runbooks/search?q=...&limit=10`. Does not cache results (queries are too varied and runbook content changes frequently).

### `useHDI(teamId: string, timeRange: TimeRange)`
```typescript
// Returns
{
  hdiScore: number;                  // 0–100
  healthStatus: 'healthy' | 'at-risk' | 'critical';
  breakdown: EngineerHDI[];
  trend: HDITrendPoint[];            // For future sparkline
  isLoading: boolean;
  error: Error | null;
}
```
Cached with a 5-minute stale time (HDI doesn't need to be real-time). Cache key includes `teamId` and `timeRange`.

---

## API Integration Map

| Hook | Endpoint | Method | Auth | Notes |
|------|----------|--------|------|-------|
| `useIncident` | `/api/incidents/:id` | GET | Bearer | SWR + WS overlay |
| `useIncident.acknowledge` | `/api/incidents/:id/acknowledge` | POST | Bearer | Optimistic update |
| `useIncident.confirmClose` | `/api/incidents/:id/close` | POST | Bearer | Requires `runbookId` or `skipReason` |
| `useRunbookCapture.submit` | `/api/runbooks` | POST | Bearer | Returns runbook ID |
| `useRunbookCapture.skip` | `/api/incidents/:id/skip-runbook` | POST | Bearer | Logs skip reason |
| `useRunbookSearch` | `/api/runbooks/search` | GET | Bearer | `?q=&limit=` |
| `useHDI` | `/api/hdi/:teamId` | GET | Bearer | `?range=7d\|30d\|90d` |

Error handling: all hooks expose a typed `error` object. Network errors surface an inline banner (not a full-page error). 401s redirect to login. 503s show "Sentinel is temporarily unavailable — your incident is not affected."

---

## Accessibility Requirements

**Modal blocking logic (high-stress context)**:
- Full keyboard navigation: Tab cycles through form fields in logical order (template → title → steps → tags → submit).
- Skip flow is keyboard-accessible: Alt+S opens skip reason selector without mouse.
- Focus is trapped inside the modal while open — Tab does not escape to the dimmed incident card behind.
- First focusable element (template selector) receives focus automatically on modal open.
- Submit button is reachable via Enter on the last field.

**ARIA live regions**:
- `<IncidentFeed>` uses `aria-live="assertive"` for new P1/P0 incidents (interrupts screen reader immediately).
- P2/P3 new incidents use `aria-live="polite"` (announced after current speech ends).
- `<TeamHealthBadge>` status changes are announced via `aria-live="polite"`.

**Color independence**: HDI bar chart includes pattern fills in addition to color coding (for color-blind users). `<TeamHealthBadge>` icons are not color-only indicators.

**Minimum tap targets**: All interactive elements ≥ 44×44px (mobile/tablet use case — engineer may be on phone during incident).

---

## Implementation Order

| Phase | Work | Exit Criteria |
|-------|------|---------------|
| 1. Static components | Build all components with hardcoded fixture data. No API calls. | Design review sign-off on all 4 views. Modal blocking UX validated by team. |
| 2. Hooks + API | Implement all 4 custom hooks. Wire to real API endpoints. | Each hook tested independently with msw mocks. Incident feed updates in real time. |
| 3. Modal blocking logic | Implement ESC trap, backdrop intercept, skip flow, optimistic close. | Manual test: engineer cannot close incident without modal completion. E2E test passing. |
| 4. Accessibility | ARIA live regions, focus trap, keyboard navigation audit. | Axe-core zero violations. Screen reader walkthrough with VoiceOver + NVDA. |
| 5. Tests | Unit tests (Vitest + Testing Library), E2E (Playwright). | Coverage ≥80% on modal and HDI components. All P0 E2E scenarios passing. |

---

## Key UX Decision: Modal Blocking

The `RunbookCaptureModal` is the single most important behavioral intervention in the product. The modal **must block** incident close — not nudge, not suggest, not remind later.

Rationale: Post-incident context decays within minutes. An engineer who doesn't write the runbook now will not write it later. "Skip" is permitted but requires a conscious choice and a logged reason. This creates accountability without being draconian.

What we explicitly chose not to do:
- **No gentle reminder banner** — easy to ignore, proved ineffective in concierge test
- **No async "fill it in later" flow** — 94% of "later" tasks don't happen
- **No admin override to disable blocking** — would be used by managers to remove friction, eliminating the intervention entirely

The skip flow with reason logging serves a second purpose: it tells us which incident types generate low-value runbooks, so we can refine which alerts trigger capture prompts in a future sprint.
