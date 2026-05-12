# Sentinel — Tech Lead Brief
**Version**: 1.0
**Date**: 2026-05-12
**Author**: Tech Lead
**Status**: Pre-Sprint Review

---

## 1. Overall Assessment

**Complexity**: Medium.

The product is well-scoped. Three distinct value surfaces (incident routing, runbook capture, HDI dashboard) with clean data flow between them. None of the individual components is technically exotic — Express API, Postgres, React. The integration surface is the main risk: two webhook providers (PagerDuty, OpsGenie), GitHub, and an external embeddings API, each with its own auth, failure mode, and rate limit behavior.

The **routing engine** is the riskiest piece of this sprint. Not because it's technically hard to build — weighted heuristics are simple code — but because "what counts as a match" is a judgment call that bakes itself into the schema and the scoring function. If we get the alert_type normalization wrong (e.g., `high_error_rate` vs `HighErrorRate` vs `error_rate_high`), the entire matching logic produces garbage. This needs to be defined and agreed before any code is written, not discovered in code review.

**Runbook quality** is the parallel risk on the product side. The system is only as good as what engineers document. If runbook capture is annoying, engineers skip it. If enough engineers skip it, the routing suggestions have no signal and the runbook library is empty. The 2-minute target for the capture modal is a hard UX constraint, not a nice-to-have.

---

## 2. What I'd Change

These are not blockers to starting the sprint. They are architectural decisions I'd revisit before writing the affected code.

### 2.1 Routing Engine: Log the Signal Before You Tune the Weights

**The stated approach**: Weighted heuristics with fixed weights `(0.4 × alert_type_match) + (0.3 × recency) + (0.3 × on_call_status)`.

**My concern**: The risk is not starting with heuristics — that's the right call. The risk is that we ship fixed weights and never revisit them. Six months from now, nobody knows whether 0.4/0.3/0.3 is right, and there's no data to argue for a change.

**What I'd do instead**: Ship the heuristics exactly as specced, but add an `routing_events` table on day 1 that logs every suggestion plus its outcome:

```sql
routing_events (
  id UUID PRIMARY KEY,
  incident_id UUID NOT NULL,
  suggested_engineer_id UUID NOT NULL,
  suggestion_rank INT NOT NULL,          -- 1 = top suggestion
  was_accepted BOOL,                     -- did the engineer accept or override?
  override_engineer_id UUID,             -- if overridden, who was assigned?
  final_mttr_seconds INT,               -- filled in at incident resolution
  weights_snapshot JSONB NOT NULL,       -- the weights used at compute time
  score_breakdown JSONB NOT NULL,        -- per-component scores
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

`weights_snapshot` is important: it lets us compare outcomes under different weight configurations even if we change the weights mid-flight. After 200+ suggestions, we'll have enough data to see if on_call_status is being over- or under-weighted relative to alert_type_match. This is an extra 30 lines of code at implementation time and saves months of guesswork later.

**This is already in the architecture spec (`routing_events` table) — I want to make sure it's in the Definition of Done for the routing engine ticket, not just as a "nice to have."**

### 2.2 pgvector: Start with pg_trgm, Add pgvector After You Validate the Need

**The stated approach**: pgvector for runbook similarity search with `text-embedding-3-small` embeddings at launch.

**My concern**: Embeddings bake in two assumptions: (1) `text-embedding-3-small` is the right model, and (2) semantic similarity is meaningfully better than keyword match for this use case. If we ship pgvector at launch, we've committed to a model and added an external API dependency (OpenAI) to the runbook save flow before we've validated that keyword search is insufficient.

Concretely: at launch, we have near-zero runbooks. A user searching for "connection pool" will find "DB connection pool exhaustion" via keyword match just fine. The case for semantic search (finding "resource contention leading to service saturation" as similar to "DB pool exhausted") only matters when the library is large and heterogeneous. We don't have that problem yet.

**What I'd do instead**: Launch with `pg_trgm` trigram search + full-text search on a `tsvector` column. This is already built into Postgres, requires no external API call on the read path, and covers the MVP use case. Add pgvector only after we see evidence of poor recall in user sessions — specifically, when engineers report "I searched for X and the runbook I wanted didn't show up" in user feedback.

**Concretely**: Add `embedding vector(1536)` column to the `runbooks` table at launch (nullable), so we don't need a migration when we add it. Add the HNSW index in a later migration. The embedding generation job is in the queue infrastructure from day 1, just disabled. Turning it on is a config flag, not a code change.

**Risk if I'm wrong**: If keyword search recall is genuinely bad at launch, we add pgvector in sprint 4 instead of sprint 1. The data schema already supports it. The delay is ~2 weeks of implementation time, not months.

### 2.3 PagerDuty Schedule Sync: Real-Time API Call, Not Daily Cron

**The stated approach (original)**: Sync rotation schedules from PagerDuty daily via cron job.

**My concern**: A cron job that syncs daily will always be up to 23h59m stale. Schedule changes (swaps, overrides, emergency rotations) happen exactly when incidents are most likely — during an incident. An engineer manually swapping out of an on-call shift mid-incident will still be suggested as primary for the next hour if we rely on a stale sync.

**What I'd do instead**: For the routing suggestion compute step, make a live API call to PagerDuty's `/oncalls` endpoint for the affected service at the moment of routing computation. This adds one external HTTP call (~50–80ms, p95) per routing suggestion. Mitigate burst cost by caching the on-call result per service for 5 minutes — an acceptable staleness window given that schedule changes within a 5-minute window are vanishingly rare.

The `rotation_schedules` table still exists for audit/history but is not used in the hot path. It's populated by the daily sync for reference.

**This change is reflected in `12_architecture.md` section 3.4. Confirming alignment here so the backend implementation plan uses the live API approach.**

---

## 3. Work Breakdown

| # | Task | Owner | Points | Depends On |
|---|---|---|---|---|
| 1 | DB migrations (all tables, indexes, pgvector extension) | Backend | 3 | — |
| 2 | PagerDuty webhook receiver (signature validation, normalization, idempotency log, queue publish) | Backend | 5 | 1 |
| 3 | OpsGenie webhook receiver (same pattern as PagerDuty) | Backend | 2 | 2 |
| 4 | Routing engine (scoring function, PagerDuty Schedules API live call, routing_events logging) | Backend | 5 | 1, 2 |
| 5 | Runbook CRUD + pg_trgm search + similarity matching for capture modal | Backend | 5 | 1 |
| 6 | Dashboard API — HDI aggregation query + endpoint | Backend | 3 | 1 |
| 7 | React: Incident Response View + Routing Suggestion card | Frontend | 5 | 4 |
| 8 | React: Runbook Capture Modal + close-incident flow | Frontend | 5 | 5 |
| 9 | React: Runbook Library + search + coverage gap banner | Frontend | 3 | 5 |
| 10 | React: HDI Dashboard (bar chart, trend line, controls) | Frontend | 5 | 6 |
| 11 | Auth: OAuth flow (PagerDuty + OpsGenie), JWT issuance, middleware | Shared | 3 | — |
| 12 | GitHub webhook receiver + commit enrichment on incident | Backend | 2 | 2 |
| 13 | Integration tests: webhook → routing suggestion → runbook capture | Backend | 3 | 4, 5 |
| 14 | Contract tests (Pact): React SPA ↔ API | Shared | 2 | 7, 8, 9, 10 |

**Total estimate**: 51 points across ~3 sprints (assuming ~18 points/sprint for a 3-engineer team)

**Sprint 1 target (18 pts)**: Tasks 1, 2, 3, 11, 12 → Infrastructure + webhook ingestion + auth. End of sprint: incidents flowing into Sentinel, routable via API.

**Sprint 2 target (18 pts)**: Tasks 4, 5, 6, 7 → Routing engine + Runbook CRUD + Incident Response View. End of sprint: engineer can see routing suggestion on incident.

**Sprint 3 target (15 pts)**: Tasks 8, 9, 10, 13, 14 → Runbook capture + Library + HDI dashboard + tests. End of sprint: full MVP.

---

## 4. Backend Owns / Frontend Owns / Shared

### Backend Owns
- All Express routes and middleware
- Webhook normalization and idempotency
- Routing engine scoring logic and `routing_events` logging
- Runbook service: pg_trgm search, embedding pipeline (queued, disabled at launch)
- Dashboard aggregation queries
- Database migrations (Knex)
- Bull/Redis queue setup and worker management
- PagerDuty Schedules API integration (live on-call lookup)
- OpenAI embeddings API integration (async, for v1.1 readiness)

### Frontend Owns
- All React components (screens 1–4 per design spec)
- React Query data fetching layer and cache invalidation
- Zustand local state (modal open/close, filter state)
- Recharts integration for HDI trend + bar chart
- OAuth redirect flow (frontend initiates, backend handles callback)
- Error boundaries and toast notification system
- Accessibility implementation (ARIA, focus management, keyboard navigation)

### Shared
- OpenAPI spec (source of truth for the contract — both sides own keeping it honest)
- Auth: backend issues JWT, frontend stores and sends it. Both own their half.
- Pact contract tests: frontend writes consumer tests, backend runs provider verification
- Alert type normalization dictionary (backend implements, frontend displays — both need to agree on the canonical names)
- Feature flags: both sides need consistent flag names (LaunchDarkly or env-based)

---

## 5. Definition of Done

A feature is done when ALL of the following are true:

- [ ] All acceptance criteria in `13_spec.md` pass (automated or manually verified)
- [ ] Unit tests cover business logic (routing engine scoring, HDI calculation, webhook normalization)
- [ ] Integration test covers the happy path end-to-end (webhook → routing suggestion, incident close → runbook saved)
- [ ] Contract tests pass (Pact provider verification green)
- [ ] All API endpoints return the schemas defined in the OpenAPI spec (validated via `ajv` in tests)
- [ ] `routing_events` is populated for every routing suggestion (verified in integration test)
- [ ] Runbook save does NOT block on embedding generation (embedding is async, test confirms 201 returned before embedding job completes)
- [ ] Error states have explicit handling: invalid webhook signature → 401, missing required fields → 422 with field-level detail, not 500
- [ ] No hardcoded credentials or API keys in source code (verified by `git-secrets` pre-commit hook)
- [ ] Performance: routing suggestion endpoint responds in < 500ms p99 under load test (k6, 50 concurrent users)
- [ ] Accessibility: Incident Response View and Runbook Capture Modal pass automated axe-core scan with zero violations
- [ ] Code reviewed by at least one other engineer (not the author)

---

## 6. Risks Flagged

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| PagerDuty API rate limits during burst incident | Medium | High — routing suggestions fail for multiple simultaneous incidents | Cache on-call status per service (5-min TTL). If PagerDuty rate limit hit (429), fall back to last-known on-call from `rotation_schedules` table. Log fallback events for monitoring. |
| pgvector extension not available on production DB | Medium | Medium — runbook semantic search (v1.1) blocked | Confirm `CREATE EXTENSION vector` works on the managed RDS instance in sprint 1, not sprint 3. AWS RDS for Postgres 15+ supports pgvector as of 2024; confirm version with infra before sprint 1. If unavailable, use pg_trgm-only path indefinitely until DB is upgraded. |
| Runbook quality: garbage data from low-effort captures | High | Medium — routing suggestion surfaces poor runbooks, erodes engineer trust | Three mitigations: (1) require `root_cause` and at least one `step` to save (enforced in API validation), (2) show MTTR impact per runbook in the library so low-quality runbooks are visible, (3) track `runbook_skipped` events — if skip rate > 40%, escalate to PM for UX review. |
| Alert type normalization drift across providers | Medium | High — PagerDuty and OpsGenie use different alert key formats; if normalized inconsistently, routing match scores are wrong | Define a normalization dictionary (`alert_type_map.ts`) in sprint 1 and treat it as a shared config file. Both webhook receivers use the same normalization function. Log `alert_type_raw` alongside `alert_type` in the incidents table so normalization can be audited and corrected. |
| OpsGenie webhook format changes | Low | Medium — webhook receiver breaks silently | Pin the OpsGenie integration API version in the webhook URL. Add schema validation on inbound payloads; if unknown fields appear, log a warning but continue processing. |
| Engineer adoption: runbook capture feels like overhead | High | High — product fails if engineers don't capture runbooks | This is not an engineering risk — it's a PM/CS risk. Flag for CS to prepare a rollout communication strategy. Engineering mitigation: make "Skip for now" as easy as "Save" in the UI, but surface skip rate data to managers in the HDI dashboard so adoption gaps are visible. |

---

## 7. Questions That Must Be Answered Before Sprint 1

1. **Alert type normalization**: Who owns defining the canonical alert type dictionary? Engineering or PM? What happens when a new alert type appears that isn't in the dictionary? (Proposed: log the raw value, use it as-is, flag for manual review in a `unmapped_alert_types` dashboard.)

2. **HDI team boundary**: Does HDI calculate per PagerDuty team (as defined in PagerDuty's team hierarchy) or per Sentinel-defined team? This affects the team syncing logic in sprint 1.

3. **Multi-provider support at launch**: Is it PagerDuty OR OpsGenie at launch (single provider per org), or do we support orgs that use both simultaneously? Supporting both simultaneously means an engineer could appear in PagerDuty's on-call schedule AND OpsGenie's — the routing engine needs to deduplicate. Recommended: single provider per org at MVP, multi-provider in v1.1.

4. **Runbook visibility**: Are runbooks visible across teams (org-wide) or team-scoped? The architecture specs team_id filtering on all queries, but the PM should confirm this is the right default. Cross-team runbook sharing is a meaningful feature for platform/infra teams.

5. **PagerDuty `resolved` event vs. Sentinel close**: When an engineer clicks "Close Incident" in Sentinel, should Sentinel resolve the incident in PagerDuty via the PagerDuty API? Or is Sentinel purely read from PagerDuty, never writing back? Proposed: write back to PagerDuty on close, to keep the source of truth consistent. Confirm before sprint 1.
