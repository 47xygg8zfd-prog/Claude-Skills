# Frontend Plan: TechBridge — PM Technical Fluency Platform
**Stage**: Frontend Implementation | **Date**: 2026-05-12

## Component Tree

```
<App>
  ├── <AuthProvider>          ← Auth0 React SDK wrapper
  └── <Router>
        ├── /explain           → <ExplainScreen>
        │     ├── <TextareaInput>
        │     ├── <ExplainButton>
        │     ├── <ExplanationResult>    ← renders streaming chunks
        │     │     ├── <SectionBlock> × 3
        │     │     ├── <ConceptLinks>
        │     │     └── <ConfidencePrompt>
        │     └── <RecentExplanations>
        │           └── <ExplanationCard> × N
        ├── /concepts          → <ConceptLibraryScreen>
        │     ├── <SearchBar>
        │     ├── <TagFilterChips>
        │     └── <ConceptList>
        │           └── <ConceptCard> × N
        ├── /concepts/:id      → <ConceptDetailScreen>
        │     ├── <ConceptHero>
        │     ├── <WorkflowContext>
        │     ├── <PlainExplanation>
        │     ├── <TechnicalDepth>       ← collapsible
        │     ├── <PMScript>
        │     └── <RelatedConcepts>
        ├── /saved             → <SavedScreen>
        │     └── <BookmarkList>
        └── /account           → <AccountScreen>
              └── <ConfidenceHistory>
```

---

## Key Components

### `<ExplainScreen>`

Top-level screen. Manages: input state, submission, streaming state, recent explanations list.

**States**:
- `idle` — empty textarea, button disabled
- `ready` — textarea has ≥10 chars, button enabled
- `streaming` — textarea locked, button shows spinner, `<ExplanationResult>` animates in
- `complete` — explanation fully rendered, bookmark available
- `error` — error message shown, textarea unlocked, retry available

**Props**: none (uses `useExplain` hook internally)

---

### `<ExplanationResult>`

Renders streaming text with section parsing. The hardest component in the app.

**Props**:
```typescript
interface ExplanationResultProps {
  chunks: string[];        // accumulated chunks from the stream
  isStreaming: boolean;
  explanationId: string | null;
  onBookmark: (id: string) => void;
}
```

**States**: `streaming` (shows partial text) / `complete` (shows actions) / `error`

**Section parsing**: The Claude response is expected to contain the headers "In plain English", "Why your engineers care", and "What to ask next". Parse by scanning accumulated text for these markers as chunks arrive; render each section in a `<SectionBlock>` as soon as the header is detected.

**Accessibility**: Wraps streaming text in `<div role="status" aria-live="polite" aria-atomic="false">` so screen readers announce updates without re-reading the whole block.

---

### `useExplain` — Custom Hook

Manages the SSE stream from `POST /explain`.

```typescript
function useExplain() {
  const [chunks, setChunks] = useState<string[]>([]);
  const [status, setStatus] = useState<'idle' | 'streaming' | 'complete' | 'error'>('idle');
  const [explanationId, setExplanationId] = useState<string | null>(null);

  async function submit(content: string, context?: string) {
    setStatus('streaming');
    setChunks([]);

    const response = await fetch('/v1/explain', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
      body: JSON.stringify({ content, context }),
    });

    if (!response.ok) {
      setStatus('error');
      return;
    }

    const reader = response.body!.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const text = decoder.decode(value, { stream: true });
      // Parse SSE lines: "data: {...}\n\n"
      for (const line of text.split('\n')) {
        if (!line.startsWith('data: ')) continue;
        const event = JSON.parse(line.slice(6));
        if (event.done) {
          setExplanationId(event.explanation_id);
          setStatus('complete');
        } else if (event.error) {
          setStatus('error');
        } else {
          setChunks(prev => [...prev, event.chunk]);
        }
      }
    }
  }

  return { chunks, status, explanationId, submit };
}
```

**Why `fetch` + `ReadableStream` instead of `EventSource`**: `EventSource` only supports GET; we need POST to send the input body. `fetch` with streaming gives full control over error handling and auth headers.

---

### `<ConceptLibraryScreen>`

**States**: `loading` / `loaded` / `empty` / `error`

**Search behavior**: Debounce 300ms on input change. On submit or after debounce: call `GET /concepts?q=...&tag=...`. Show skeleton cards during load. Preserve filter state in URL params so back-navigation works.

---

### `<TagFilterChips>`

**Props**: `tags: string[]`, `selected: string | null`, `onChange: (tag: string | null) => void`

Horizontal scrollable row. Active chip has filled background. Tap active chip to deselect (show all).

---

## API Integration

All API calls go through a centralized `apiClient` module that:
- Reads the Auth0 token from the `useAuth0` hook
- Attaches `Authorization: Bearer <token>` header
- Handles 401 by redirecting to login
- Handles 429 by surfacing a user-readable message from the `detail` field

Custom hooks per resource:
- `useExplain()` — streaming (above)
- `useConcepts(params)` — paginated list
- `useConcept(id)` — single concept
- `useBookmarks()` — list + create
- `useSurvey()` — submit survey, check if already submitted for a given day

---

## State Management

**Local state** for: textarea value, streaming chunks, UI toggle states (collapsible sections, filter chips)

**React Query** (`@tanstack/react-query`) for: concepts list, concept detail, bookmarks list, account data — handles caching, background refetch, and loading/error states consistently.

**No global store** (Redux/Zustand) — the app is small enough that prop drilling + React Query covers all cases. Revisit if team layer (future) introduces cross-screen shared state.

---

## Accessibility

- **Keyboard nav**: Tab order on Explain screen: textarea → submit button → recent explanations (each focusable). In concept detail: back button → bookmark → section headers (navigable as `<h2>` within a scrollable region).
- **ARIA**:
  - Streaming container: `role="status" aria-live="polite"`
  - Bookmark button: `aria-label="Save explanation"` / `aria-label="Saved"` (toggled)
  - Tag filter chips: `role="group" aria-label="Filter by workflow"`, each chip is a `<button>`
  - Confidence prompt stars: `role="radiogroup"`, each star is `role="radio"`
- **Reduced motion**: Streaming is replaced with instant render when `prefers-reduced-motion: reduce`
- **Focus management**: After submitting an explanation, focus moves to the `<ExplanationResult>` container so keyboard users don't have to tab past the textarea

---

## Test Cases

**Component — `<ExplainScreen>`**
- Renders with empty textarea; submit button is disabled
- After typing 10+ chars: submit button enables
- On submit: textarea locks, button shows spinner
- On stream complete: explanation renders with 3 sections visible
- On error: error message shows, textarea unlocks

**Component — `<ExplanationResult>`**
- Chunks `["In plain English", ", this means"]` → renders partial text in Plain English section
- When `isStreaming=false` and `explanationId` set → bookmark button visible
- Screen reader: `role="status"` region updates as chunks arrive

**Hook — `useExplain`**
- Successful stream → status transitions: idle → streaming → complete
- `event.error` in stream → status transitions to `error`
- Non-2xx response → status transitions to `error`

**Integration — Explain flow (Playwright)**
- User logs in → lands on Explain screen → pastes text → taps submit → explanation streams → bookmark icon visible → taps bookmark → toast "Saved to My Saved" → navigates to /saved → explanation appears

**Integration — Concept search (Playwright)**
- User navigates to /concepts → types "refactor" → list updates within 500ms → taps first result → concept detail loads with all sections

---

## Implementation Order

1. **Auth setup** (day 1): Auth0 React SDK; login/logout; token available in `apiClient`
2. **Routing + shell** (day 1): React Router; nav bar; screen skeletons
3. **Concept library** (days 2–3): `useConcepts` hook; list screen; detail screen; search and filter — these use simple REST, good for initial dev before SSE is ready
4. **Bookmarks + Survey** (days 3–4): Bookmark create/list; confidence prompt; My Saved screen
5. **Explain screen + streaming** (days 4–7): `useExplain` hook; `<ExplanationResult>` streaming render; section parsing; error states
6. **Analytics** (days 7–8): Wire Segment SDK; fire `session_start`, `session_end`, `concept_viewed`
7. **Accessibility pass** (day 8): Audit tab order; add ARIA labels; test with VoiceOver
8. **Mobile polish** (day 9): Test at 375px; fix any overflow or tap-target issues
