# Design Spec: TechBridge — PM Technical Fluency Platform
**Stage**: UI/UX Design | **Date**: 2026-05-12

## Design Brief

**User**: Mid-level PM at a B2B SaaS company
**JTBD**: Get a plain-language explanation of a technical thing I just encountered — fast, private, and without having to ask an engineer

**Principles**:
1. **Zero friction to value** — the explanation engine must be reachable in one tap from any screen; no onboarding wizard before first use
2. **Private by default** — the UI must feel like a private notebook, not a public forum; no social features, no activity feeds, no "X other PMs asked this"
3. **Mobile-first** — PMs read before meetings on their phones; every screen must work at 375px width without horizontal scroll

---

## Information Architecture

```
TechBridge
├── Home (Explain) — default landing
│     └── Paste or type technical content → get explanation
├── Concept Library
│     ├── Browse by workflow tag
│     └── Search
│           └── Concept detail page
├── Workflow Guides
│     └── Guide detail (step-by-step)
├── My Saved (bookmarks)
└── Account / Settings
      └── Confidence tracker (survey history)
```

---

## User Flow: Core Explanation (Happy Path)

1. **Entry** — user opens app; lands on Explain screen with a large input area
2. User pastes Slack message / ticket excerpt / design doc snippet → taps "Explain this"
3. Loading state (streamed response) — explanation appears word by word (< 3s p95)
4. Explanation displayed in three sections: **Plain English**, **Why engineers care**, **What to ask next**
5. User can: bookmark the explanation, copy it, start a new one, or tap a linked concept
6. After 3 uses: inline prompt "Rate your confidence after reading this" (1–5 stars, dismissible)

**Error states**:
- Input too short (< 10 chars): inline message "Paste at least a sentence to explain"
- API error: "Something went wrong — try again" with retry button; no error codes shown to user

---

## Screen Specifications

### Screen 1: Explain (Home)

**Layout**: Single-column. Top: logo + nav icon (right). Center: large textarea. Bottom: sticky CTA button.

**Components**:
- `TextareaInput`: placeholder "Paste a Slack message, ticket, or tech term…"; 6 lines min, expands; border highlights on focus
- `ExplainButton`: full-width primary CTA; label "Explain this"; disabled until ≥10 chars entered; loading spinner during API call
- `CharacterHint`: appears at 10 chars, disappears after — "You can paste a full paragraph"
- `RecentExplanations`: below the fold; last 3 explanations shown as collapsed cards (title only); tap to expand

**Copy**:
- Headline: "What does this mean?" (above textarea)
- Empty state below fold: "Your explanations will appear here"
- CTA: "Explain this"

**Behavior**:
- On submit: textarea locks (grayed), button shows spinner, explanation streams in below
- On error: textarea unlocks, error message replaces spinner, button returns to active state
- On success: new explanation card animates in at top of recent list

---

### Screen 2: Explanation Result

**Layout**: Full-screen card. Back button top-left. Bookmark icon top-right.

**Components**:
- `SectionBlock` × 3: "Plain English" / "Why engineers care" / "What to ask next"
- Each section has a label chip and collapsible body
- `ConceptLinks`: inline highlighted terms that link to concept library entries
- `ConfidencePrompt`: subtle card at bottom after 3+ explanations: "Did this help? [1] [2] [3] [4] [5]" — tap dismisses for 7 days
- `ActionBar`: Bookmark | Copy | New explanation

**Copy**:
- "Plain English" section label: "In plain English"
- "Why engineers care" label: "Why this matters to your engineers"
- "What to ask next" label: "Questions worth asking"
- Bookmark confirmation toast: "Saved to My Saved"

**Behavior**:
- Text streams in section by section; section labels appear immediately, body streams
- Bookmarking saves the full explanation + original input; toast confirms
- Tapping a concept link opens concept detail in a bottom sheet (not full navigation)

---

### Screen 3: Concept Library

**Layout**: Search bar pinned at top. Workflow tag filter chips (scrollable horizontal row). List of concept cards below.

**Components**:
- `SearchBar`: autofocus on screen entry; searches title + tags; debounced 300ms
- `TagFilterChip` (horizontal scroll): Sprint Planning | Architecture Review | Incident Debrief | Technical Debt | Writing Requirements | All
- `ConceptCard`: title, one-line description, workflow tag chip; tap opens detail
- `EmptyState` (search): "No concepts match '[query]' — try a simpler term"

**Copy**:
- Screen title: "Concept Library"
- Search placeholder: "Search by term or workflow…"
- Empty state (no filter): "Concepts are loading — check back shortly"

---

### Screen 4: Concept Detail

**Layout**: Scrollable single-column. Fixed header with back button + title + bookmark icon.

**Components**:
- `ConceptHero`: title (large), one-sentence definition
- `WorkflowContext`: "Where you'll see this" — which PM workflows this concept appears in
- `PlainExplanation`: the concept in PM terms
- `TechnicalDepth` (collapsible): the more technical version for PMs who want it
- `PMScript`: example of what to say to an engineer when this comes up
- `RelatedConcepts`: 2–3 linked concept cards

**Copy**:
- "Where you'll see this" section label (keeps it contextual, not academic)
- "What to say to your engineer" (for PMScript section)
- "Go deeper" (collapsible label for TechnicalDepth)

---

### Screen 5: Workflow Guide

**Layout**: Step-by-step reading experience. Progress bar at top. Previous/Next navigation at bottom.

**Components**:
- `ProgressBar`: N of M steps; fills as user advances
- `StepContent`: title, body text, optional callout box ("Watch out for…"), optional concept link
- `NavigationBar`: "← Previous" / "Next →" (or "Finish" on last step); always visible
- `GuideCompletionCard` (final screen): "You've finished [Guide Name]. Save this for your next [workflow]."

---

## Accessibility

- **Keyboard nav**: Tab → textarea → submit button → bookmark → concept links in order
- **ARIA**: `role="status"` on streaming explanation container (live region); `aria-label` on bookmark icon ("Save explanation"); concept link chips tagged `role="link"`
- **Color**: 4.5:1 minimum on all body text; confidence prompt stars use both color and icon (not color-only)
- **Motion**: explanation streaming respects `prefers-reduced-motion` — shows full text immediately instead of streaming

---

## Design Open Questions

1. **Streaming vs. instant**: Streaming text feels alive and fast but may feel slow on mobile over 4G. Do we stream or wait for full response and show instantly? Needs latency testing at p95.
2. **Confidence prompt timing**: After 3 uses feels right but may be too early for a PM who used the tool for 3 trivial things. Alternative: trigger after first use where input was ≥100 chars (implies a real technical document was pasted). Needs experiment.
3. **Concept Library content gate**: Do we show all concepts immediately (may feel sparse at launch with 50 concepts) or paginate/drip them by workflow? Dripping risks confusing users who look for a specific term.
