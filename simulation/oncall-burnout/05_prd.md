# Sentinel — Product Requirements Document
**Stage 5 of 20: PRD**
**Date:** 2026-05-12
**Author:** PM
**Status:** Draft v1.0 — pending eng estimate and design review
**Reviewers:** Eng Lead, Design Lead, CPO
**Review due:** 2026-05-19

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-05-08 | PM | Initial skeleton from OST |
| 1.0 | 2026-05-12 | PM | Full draft after research synthesis sign-off |

---

## 1. Problem Statement

### Customer Problem

Engineering managers at B2B SaaS companies (50–200 engineers, no dedicated SRE team) are losing on-call coverage resilience because incident resolution knowledge is concentrated in 3–4 engineers — "heroes." When a hero is unavailable or leaves the company, MTTR triples and remaining engineers face unsustainable escalation volume.

The root cause is not alert volume. It is knowledge debt: resolution procedures exist only in the heroes' heads because existing documentation workflows (Confluence wikis, PagerDuty notes) have too much friction at the wrong moment. Engineers defer documentation until after the incident and never return to it.

The impact is concrete and compounding: engineer satisfaction falls, burnout accelerates, and knowledge gaps widen with every departure.

### Why Existing Solutions Fail

| Existing Approach | Why It Fails |
|---|---|
| Confluence runbook wikis | Written in advance, go stale, no integration with incident workflow — not consulted at 2am |
| PagerDuty escalation policies | Routes to the hero faster but does not reduce hero dependency |
| #on-call-help Slack channels | Asks the same heroes by a different channel; no knowledge capture or searchability |
| Post-incident retrospectives | Valuable for systemic improvements; does not solve in-incident knowledge retrieval |
| On-call rotation fairness | Distributes page count evenly; does not distribute resolution capability |

### The Insight

The intervention must happen at incident close — not before, not after. This is the only moment where:
1. Context is fresh enough to document accurately
2. The engineer is still in the tooling context
3. A structured prompt adds friction proportional to the value created

Auto-capture at close transforms the act of resolving an incident into an act of knowledge production. Sentinel is a knowledge routing product, not an alerting product.

---

## 2. Goals and Success Metrics

### Primary Goal

Reduce Hero Dependency Index (HDI) — the percentage of incidents resolved by the top 3 engineers on a team — from a typical baseline of 65% to below 30% within 90 days of a team adopting Sentinel.

### Metrics

| Metric | Baseline | Target | Measurement Method | Timeline |
|--------|---------|--------|-------------------|----------|
| **Hero Dependency Index** | 64% | <30% | (Incidents resolved by top 3 engineers) / (total incidents) — from PagerDuty/OpsGenie data via Sentinel | 90 days post-adoption |
| **MTTR** | 47 min | ≤28 min | Mean time from incident open to resolved, aggregated across all incidents | 60 days post-adoption |
| **Runbook coverage rate** | ~15% of recurring alert types have a current runbook | ≥70% | (Alert types with a runbook <6 months old) / (alert types that fired ≥3x in last 90 days) | 60 days post-adoption |
| **Escalation rate** | ~38% of incidents require escalation outside assigned on-call | ≤23% | % of incidents with a secondary responder added after initial page | 60 days post-adoption |
| **Runbook capture rate** | 0% (no systematic capture) | ≥65% | % of recurring-alert-type incidents closed with a Sentinel runbook attached | 30 days post-adoption |

### Guardrail Metric

**On-call engineer satisfaction score must not decrease.**

This is a non-negotiable guardrail. Sentinel must not increase cognitive burden or perceived surveillance. Measured via:
- Quarterly pulse survey (3 questions, 1–5 scale): "Sentinel makes my on-call shifts easier", "I feel comfortable with what Sentinel records about my incidents", "I would recommend Sentinel to a peer on another team"
- Minimum acceptable score: 3.5/5.0 average across all three questions
- If satisfaction drops below 3.5, product changes are required before further rollout

**Rationale:** If Sentinel solves the hero dependency problem but makes on-call engineers feel surveilled or overburdened, we have shifted the problem without solving it. IC buy-in is also a commercial requirement — an unpopular tool will be routed around, which destroys data quality and makes the whole system fail.

### What Success Is Not

- A reduction in total alert volume (not our problem to solve)
- Perfect runbook coverage (90-day target is 70%, not 100%)
- Zero hero incidents (some incidents will always require a specialist — the goal is reducing dependency, not eliminating expertise)

---

## 3. Target User

### Primary: Engineering Manager

**Profile:** Manages a team of 8–20 engineers, owns the on-call rotation, has experienced at least one period of elevated MTTR caused by hero unavailability.

**Jobs to be done:**
- Monitor team on-call health without individually reviewing every incident
- Make the case to leadership for on-call rotation improvements with data, not anecdote
- Reduce the flight risk of engineers citing on-call burden in 1:1s

**How they use Sentinel:** Weekly review of Hero Dependency Index dashboard. Acting on alerts when HDI exceeds threshold. Reviewing runbook coverage for their service area.

### Secondary: On-Call IC Engineer

**Profile:** Software engineer participating in active on-call rotation; paged at least 2x/month; not the team hero but regularly escalates to one.

**Jobs to be done:**
- Find what worked last time, fast, at 2am
- Know who to contact without broadcasting to Slack
- Close incidents without being forced into lengthy documentation sessions

**How they use Sentinel:** Receives runbook suggestions inline when paged. Completes structured capture form at incident close. Receives routing suggestions with named escalation contact.

---

## 4. User Stories

### Epic 1: Runbook Capture

**US-01 — Capture prompt at incident close**
> As an on-call engineer, when I resolve an incident and attempt to close it, I want to be shown a structured form asking what happened and how I fixed it, so that the next engineer who faces this alert has a head start.

**Acceptance criteria:**
- Form is triggered when engineer clicks "Resolve" in PagerDuty/OpsGenie
- Form contains exactly 4 fields: (1) What triggered this alert? (2) What was the root cause? (3) What steps did you take to fix it? (4) What should the next engineer check first? — all free text, no required character minimum
- Form has a "Skip for now" option that records a skip event (not hidden — visible to manager in HDI dashboard)
- Estimated completion time: <90 seconds for a typical incident
- Form data is stored associated with the alert type (not the specific incident ID), so future similar alerts can surface it

**Why (from research):** Behavioral evidence from 8/10 participants showed the "I'll add it later" pattern. P5's explicit requirement: "Give me checkboxes and a 'what commands did you run' field — I'll fill that in. Don't give me a Confluence page." The 90-second constraint came independently from P5, P7, and P9.

---

**US-02 — Skip tracking and manager visibility**
> As an engineering manager, when an engineer skips the runbook capture form, I want to see that skip recorded in the HDI dashboard, so that I can identify which alert types consistently lack documentation.

**Acceptance criteria:**
- Skip events are recorded per-engineer per-alert-type
- Manager dashboard shows "coverage gap" indicator on alert types with ≥3 skips and no current runbook
- Individual skip counts are not shown per-engineer in IC-visible views
- Coverage gap indicator links to that alert type's runbook (or empty state with "no runbook yet")

**Why (from research):** P3 explicitly stated: "I can't prove it to finance." Without skip tracking, coverage gaps are invisible. P5's surveillance concern is addressed by aggregating skip data at the alert-type level rather than showing individual skip counts to peers.

---

**US-03 — Runbook editing and version history**
> As an on-call engineer, when I open a runbook that was captured by a previous engineer, I want to be able to edit it and have my changes tracked, so that the runbook improves over time and I know which version was used when.

**Acceptance criteria:**
- Runbook entries are editable by any engineer on the team (not just the original author)
- Each edit is versioned with timestamp and editor name
- Most recent version is displayed by default; full history is accessible
- Edit history is visible to managers; not used for performance assessment (surfaced in manager tooltip)

**Why (from research):** P2's Confluence audit showed 40% follow-and-fail rate for runbooks older than 6 months. Stale runbooks cause active harm. Version history creates accountability for updates without blaming individuals.

---

### Epic 2: Runbook Retrieval

**US-04 — Runbook suggestion at page time**
> As an on-call engineer, when I receive a page, I want to see the most relevant runbook for this alert inline in the notification, so that I can start resolving without opening a separate documentation tool.

**Acceptance criteria:**
- Runbook suggestion appears in the Sentinel sidebar/overlay, visible within the PagerDuty/OpsGenie incident view
- Similarity matching uses alert title + first 200 characters of alert body
- Top match is shown by default; second match is accessible via "see other runbooks" link
- Match confidence score is shown ("85% match") so engineer can assess reliability
- If no runbook exists for this alert type, show: "No runbook yet — you'll be prompted to create one when you resolve."
- Runbook retrieval latency: <2 seconds from incident open to suggestion displayed

**Why (from research):** P10: 47-minute MTTR for a 4-minute fix — the fix was in someone else's personal notes. P8 searched Slack history back 8 months during a 3am page. Primary JTBD: "When I get paged at 2am, I want to find what worked last time."

---

**US-05 — Runbook staleness warning**
> As an on-call engineer, when I access a runbook, I want to see a clear warning if it hasn't been validated recently, so that I know whether to trust it or proceed with caution.

**Acceptance criteria:**
- Staleness threshold: 6 months without a revalidation, or last validated >10 incidents ago (whichever is sooner)
- Warning banner: "This runbook was last validated 8 months ago. Proceed with caution and update it if the steps are still accurate."
- Engineer can click "Validate" to confirm it's still accurate — this resets the staleness clock without requiring a full edit
- Stale runbooks shown with visual distinction (amber border) in all runbook lists

**Why (from research):** P2: Confluence runbook for Postgres failover was 14 months old through three infra changes. P4: "Team stopped trusting the wiki after two incidents where following it made things worse." Eroded trust in documentation is worse than no documentation — it creates false confidence.

---

### Epic 3: Intelligent Routing

**US-06 — Route to last successful resolver**
> As an on-call engineer, when I receive a page for an alert type that has been resolved by another engineer before, I want to receive a routing suggestion naming that engineer, so that I know who to contact immediately instead of broadcasting to Slack.

**Acceptance criteria:**
- Routing suggestion appears alongside the runbook at page time
- Routing shows: name, "resolved this alert type [N] times", last resolution date, current on-call status (available/unavailable/in another incident)
- If the suggested engineer is unavailable, show second-best match with same information
- Routing is a suggestion, not a mandatory re-assignment — engineer can dismiss and handle themselves
- If no routing match exists (novel alert type), show standard on-call rotation; do not show empty routing widget

**Why (from research):** P10: "I called a senior engineer at 2:30am for a Redis timeout that had a known fix. The total MTTR was 47 minutes. The person I called fixed it in 4 minutes." P4 data: average escalation time 18 minutes, estimated 60% of that is identifying who to contact.

---

**US-07 — Routing transparency**
> As an on-call engineer, when I receive a routing suggestion, I want to understand why I'm being shown that specific person, so that I can decide whether to follow the suggestion with confidence.

**Acceptance criteria:**
- Routing suggestion includes explanation text: "Suggested because [Name] last resolved '[Alert Type]' on [Date] and wrote the attached runbook."
- Engineer can see resolver's resolution history for this alert type (date + MTTR for each past resolution)
- No silent routing — if Sentinel routes a notification, the routing logic is always displayed

**Why (from research):** Design constraint surfaced in UX research synthesis: "Routing must have transparent fallback. Engineers need to know why they were routed to a specific incident." Silent routing that feels arbitrary erodes trust and leads to the tool being bypassed.

---

**US-08 — Graceful fallback routing**
> As an on-call engineer, when Sentinel has no routing data for an alert type, I want to receive the standard on-call rotation assignment without any degradation of the current on-call experience, so that Sentinel never makes things worse than the baseline.

**Acceptance criteria:**
- Fallback to PagerDuty/OpsGenie's native on-call schedule when no routing match exists
- Fallback does not require any Sentinel-specific configuration — it inherits the customer's existing rotation
- Fallback state is distinguishable: "No routing history for this alert — assigned per standard rotation."
- Fallback incidents prompt runbook capture at close, starting the knowledge accumulation for future routing

**Why (from research):** P6: "New microservice deployments create new alert types every quarter." A routing system that degrades or errors on novel alerts will lose engineer trust permanently. Graceful fallback is a non-negotiable reliability requirement.

---

### Epic 4: Hero Dependency Index Dashboard

**US-09 — Manager view: Hero Dependency Index**
> As an engineering manager, I want to see what percentage of my team's incidents were resolved by the top 3 engineers over the past 30/60/90 days, so that I can identify hero dependency before it becomes a crisis.

**Acceptance criteria:**
- Dashboard shows HDI as a single percentage with time period selector (30/60/90 days)
- Trend line showing HDI over time (weekly data points)
- Breakdown: "Your top 3 resolvers handled X% of incidents in the past 30 days" — engineers named at this level for manager view only
- Benchmark line: target <30% shown as a horizontal reference line
- Export to CSV for inclusion in leadership reports

**Why (from research):** P3: "I've been trying to make this argument for 6 months. If Sentinel can give me the number, I can have the headcount conversation." P1, P3, P6 all used the phrase "I know who it is, but I can't prove it." The dashboard converts qualitative awareness into quantifiable evidence.

---

**US-10 — Manager view: Runbook coverage heatmap**
> As an engineering manager, I want to see which of my team's most common alert types have current runbooks and which do not, so that I can prioritize runbook creation for the alerts that fire most frequently.

**Acceptance criteria:**
- Table showing top 20 alert types by frequency in the past 90 days
- Per alert type: frequency count, runbook status (current / stale / missing), last resolver name, last MTTR
- Filter by: runbook status (show only "missing" or "stale"), service area
- "Request runbook" action that sends an in-app nudge to the engineer who last resolved that alert type
- "Request runbook" does not send an email or Slack — Sentinel in-app only; no communication tool integrations in v1

**Why (from research):** P2: "We literally have a rule that you're supposed to add a runbook link before closing. We have no runbooks." Coverage heatmap gives managers a prioritized list — they can direct attention to the highest-frequency, highest-risk gaps rather than guessing.

---

**US-11 — IC view: My on-call history**
> As an on-call engineer, I want to see a summary of my recent on-call incidents, including which ones I resolved via a runbook vs. from scratch, so that I can understand my own patterns without feeling surveilled.

**Acceptance criteria:**
- Shows only the viewing engineer's own history — no peer comparison
- Fields: incident date, alert type, MTTR, runbook used (yes/no), escalation made (yes/no), runbook captured at close (yes/no)
- No manager view of individual IC history detail — managers see aggregated HDI, not individual incident logs
- Time range: last 90 days

**Why (from research):** P7 (hero engineer): "I'm exhausted. I don't need to see a scoreboard, I need to see that things are getting better." Individual history without peer comparison gives ICs useful self-awareness without creating competitive anxiety or surveillance perception. This also addresses P5's concern directly.

---

## 5. MoSCoW Requirements

### Must Have

| ID | Requirement | Why (from research) |
|----|-------------|---------------------|
| M-01 | Structured runbook capture form triggered at incident close, before mark-resolved action is available | Core mechanic — removes the "I'll do it later" escape hatch while keeping friction minimal. Direct response to 8/10 participants describing the behavioral pattern of deferred documentation. |
| M-02 | Form must be completable in <90 seconds with 4 guided fields; no blank text fields as primary input | P5, P7, P9 independently cited 90-second threshold. Blank fields produce blank submissions (observed in every Confluence audit referenced by P2 and P4). |
| M-03 | "Skip" option with skip event recording | Managers need to see coverage gaps; engineers must not feel trapped. Skip tracking without individual shaming is the balance. |
| M-04 | Runbook surfaced inline at page time using similarity search | Primary JTBD: find what worked last time at 2am. P10's 47-minute MTTR for a 4-minute fix is the canonical failure case to eliminate. |
| M-05 | Routing suggestion showing last resolver with transparency text ("suggested because...") | P4 data: 18-minute average escalation time. Named contact vs. Slack broadcast is the core UX improvement. Transparency text required to maintain trust (design constraint from research synthesis). |
| M-06 | Graceful fallback to standard PagerDuty/OpsGenie rotation when no routing match | P6: new alert types created quarterly. Sentinel must never degrade baseline on-call experience. |
| M-07 | Hero Dependency Index dashboard for managers — % of incidents resolved by top 3 engineers | P3: "I can't prove it to finance." P1: could have seen the hero departure signal 6 months early. Manager buy-in requires a visible, actionable north-star metric. |
| M-08 | PagerDuty webhook integration | 7/10 participants use PagerDuty. Blocking integration requirement from CPO strategy. |
| M-09 | OpsGenie webhook integration | 3/10 participants use OpsGenie. Blocking integration requirement from CPO strategy. |
| M-10 | Manager-only access to HDI with named engineers; IC view is aggregate-only | P5 raised surveillance concern. Design constraint: frame as team health, not individual performance. IC trust is a guardrail requirement. |

### Should Have

| ID | Requirement | Rationale |
|----|-------------|-----------|
| S-01 | Runbook staleness warning (amber indicator for runbooks >6 months or >10 incidents old without re-validation) | P2's Confluence audit showed 40% follow-and-fail rate on stale runbooks. Trust erosion from bad runbooks is worse than no runbooks. |
| S-02 | "Validate" button on runbooks that resets staleness clock without requiring full edit | Reduces friction to maintaining accuracy. One-click revalidation is the minimum viable maintenance action. |
| S-03 | Runbook version history with editor name and timestamp | Accountability for runbook quality without blame; enables rollback if an edit degrades a runbook. |
| S-04 | Runbook coverage heatmap for managers (top 20 alert types by frequency × runbook status) | Gives managers a prioritized action list rather than an undifferentiated gap count. |
| S-05 | Match confidence score displayed with runbook suggestion ("85% match") | Engineers need to calibrate trust in auto-surfaced runbooks. Confidence score is the minimum transparency requirement. |
| S-06 | IC on-call history view (own incidents only, no peer comparison) | P7 needs to see improvement without feeling surveilled. Self-service data reduces manager burden for 1:1 prep. |
| S-07 | "Request runbook" action in coverage heatmap (in-app nudge to last resolver) | Gives managers a lightweight lever to close specific coverage gaps without email/Slack overhead. |

### Could Have

| ID | Requirement | Rationale for Deferral |
|----|-------------|------------------------|
| C-01 | Second runbook match accessible via "see other runbooks" link at page time | Value is real but secondary; primary match covers >80% of cases. Adds scope for marginal gain. |
| C-02 | Resolver history shown in routing suggestion (date + MTTR for each past resolution) | Useful for confidence calibration; but name + last date may be sufficient signal. |
| C-03 | HDI trend line (weekly data points over 90 days) | Value for tracking improvement over time, but requires 90 days of data to be meaningful; day-one customers won't see it. |
| C-04 | HDI export to CSV | Useful for leadership reporting but not core to product value. Google Sheets screenshot achieves same goal short-term. |
| C-05 | Credential scrubbing regex on runbook content pre-storage | Important for enterprise customers; not blocking for design partner pilots who can self-govern. Move to roadmap with clear date. |

### Won't Have (v1)

| ID | Feature | Reason |
|----|---------|--------|
| W-01 | **Rotation fairness scheduler** | Calendar integration scope; orthogonal to knowledge problem; separate product problem for v2 |
| W-02 | **Alert deduplication / noise reduction** | Different problem (volume, not knowledge); PagerDuty already solves for many customers; dilutes Sentinel's positioning |
| W-03 | **Slack bot interface** | Integration complexity; core mechanic must be validated in PagerDuty/OpsGenie interface first; adds scope without proven incremental value |
| W-04 | **Mobile push / native app** | Web-first is sufficient for MVP; engineers use desktop during incident response |
| W-05 | **Postmortem automation** | Different use case (systemic improvement vs. in-incident resolution); valuable but distinct product surface |
| W-06 | **SLA tracking and reporting** | Downstream of solving MTTR; premature before Sentinel has baseline MTTR data |
| W-07 | **Multi-team / org-level rollup** | Enterprise feature; premature for 50–200 engineer target segment |
| W-08 | **Email / Slack notifications from Sentinel** | Communication tool integrations in v1 create scope risk and privacy complexity; in-app only |
| W-09 | **SSO / SCIM provisioning** | Enterprise requirement; target segment can use email/OAuth; add to roadmap for enterprise tier |
| W-10 | **Self-hosted / on-prem deployment** | Required for enterprise, but design partner pilots can use cloud; add to roadmap with clear timeline |

---

## 6. Architecture Notes (For Engineering)

This section contains PM-level context for the technical design. Engineering Lead owns the implementation decisions.

**Integration surface:**
- PagerDuty: webhooks V3 (stable); incident lifecycle events (acknowledged, resolved, assigned)
- OpsGenie: REST API + alert webhooks; auth via API key per customer

**Core data model (simplified):**
- `incidents` — linked to PagerDuty/OpsGenie ID; alert type; timestamps; resolver engineer; MTTR
- `alert_types` — normalized alert type identifier; embedding vector for similarity search; linked runbooks
- `runbooks` — structured fields (4 capture fields); version history; staleness metadata; alert_type foreign key
- `engineers` — linked to PagerDuty/OpsGenie user ID; resolution history per alert type
- `teams` — manager relationship; HDI calculation materialized view

**Similarity search:** pgvector on alert title + body embeddings. Embedding model: OpenAI text-embedding-3-small (cost-effective, sufficient semantic resolution for alert titles). Offline validation required before go-live (Assumption A2).

**Data privacy consideration (flagged open question):** Runbook content may contain internal hostnames, environment variables, and command-line strings. PII / credential scrubbing in v1 is a Could Have (C-05); design partners must be informed of this limitation explicitly.

---

## 7. Open Questions

| # | Question | Owner | Target Date | Consequence if Unresolved |
|---|----------|-------|-------------|--------------------------|
| OQ-1 | Will pgvector similarity search match alert types accurately enough to surface the right runbook >70% of the time? | Eng Lead | 2026-05-19 | If accuracy is <70%, retrieval is unreliable — engineers will ignore suggestions and trust erodes. May require additional matching signals (service name, alert source). |
| OQ-2 | Does PagerDuty's V3 webhook deliver enough alert body content for useful embedding, or do we need to call the PagerDuty API for full alert detail? | Eng Lead | 2026-05-19 | If webhook payload is insufficient, we need an API polling fallback — adds complexity and rate-limit risk. |
| OQ-3 | Will design partner customers allow runbook content (which may include infra details) to be stored in Sentinel's cloud? | PM | 2026-05-21 | If not, we cannot collect real runbook data for pilot. Need to scope credential scrubbing (C-05) as Must Have or offer local storage option. This is the highest-risk open question. |
| OQ-4 | How do we handle multi-service incidents where the alert type maps to multiple services? | Eng Lead | 2026-05-26 | Routing and retrieval logic may surface wrong runbook if alert type alone is ambiguous. May need service-tag signal from PagerDuty to disambiguate. |
| OQ-5 | Should the "Skip" option on the capture form be time-limited (e.g., engineer must complete within 24 hours or it auto-closes as skipped)? | PM + Design | 2026-05-26 | A 24-hour window could recover some "I'll do it after I sleep" intent. But it adds notification complexity. Needs UX input on whether reminder is more annoying than helpful. |
| OQ-6 | What is the engineering cost of OpsGenie integration vs. PagerDuty only? | Eng Lead | 2026-05-19 | If OpsGenie integration doubles the integration scope, consider shipping PagerDuty-only for first design partner and adding OpsGenie as v1.1. |
| OQ-7 | How should HDI be calculated for teams that use escalation policies that route through a non-team engineer (e.g., a shared platform team)? | PM | 2026-06-02 | If cross-team escalations are counted in team HDI, the metric may be misleading for teams with legitimate platform dependencies. Need to define "in-team resolution" clearly. |

---

## 8. Non-Goals

The following are explicitly out of scope for Sentinel v1. They are called out here because they may appear in feedback and should have a documented response.

| Non-Goal | Why It's Out of Scope | v2 Roadmap? |
|----------|----------------------|-------------|
| **Rotation fairness scheduler** | Solves load distribution, not knowledge distribution. Requires calendar integration and adds significant scope. The HDI dashboard makes the problem visible; fixing it is a separate product problem. | Yes — v2 Q4 |
| **Alert deduplication / noise reduction** | This is a volume problem; Sentinel solves a knowledge problem. PagerDuty's Event Intelligence already addresses this for most target customers. Building our own deduplication would position us as a PagerDuty competitor, which conflicts with our integration strategy. | No — not Sentinel's problem |
| **Slack bot interface** | Adding Slack as an interaction surface doubles the integration test matrix and creates conversational UX design work that is premature before the core mechanic is validated. "Slack-native" is a positioning choice we should make after MVP, not before. | Yes — v2 Q3 |
| **Postmortem / retrospective automation** | Valuable but distinct use case. Postmortems are about systemic improvement after the fact; Sentinel's core loop is about in-incident resolution in the moment. The user, timing, and product surface are different. | Possibly — evaluate after v1 |
| **Mobile push / native mobile app** | Incident response happens at a keyboard, not on mobile. Engineers use their laptops when paged. Mobile is a nice-to-have that adds development cost without addressing a real usage pattern identified in research. | Backlog — low priority |
| **SLA tracking and reporting** | Downstream of establishing MTTR baselines. We need 60 days of MTTR data before SLA tracking is meaningful. Adding it to v1 puts a metric in front of customers before it has enough data to be useful. | Yes — v1.5 or v2 |

---

## 9. Success Criteria for MVP

The MVP is considered successful if, at the end of the first 90-day design partner period:

1. Hero Dependency Index has moved from baseline toward <30% for at least 1 of 2 design partners (leading indicator; full 90-day target may not be achieved in 8-week sprint)
2. Runbook capture rate ≥50% of recurring-alert-type incidents (lower than 65% target due to ramp time)
3. At least 1 engineering manager reports using HDI data in a leadership conversation
4. On-call engineer satisfaction score ≥3.5/5.0 on guardrail survey
5. MTTR trend is directionally improving (even if 28-minute target not reached within sprint window)
6. 0 data privacy incidents involving runbook content (OQ-3 must be resolved before launch)

---

## 10. Dependencies and Timeline

| Milestone | Owner | Target Date | Dependency |
|-----------|-------|-------------|------------|
| Design partner selection (2 customers) | CS + PM | 2026-05-19 | Required for real alert data to validate assumption A2 |
| OQ-1 through OQ-3 resolved | Eng Lead + PM | 2026-05-21 | Gates engineering kickoff |
| Engineering kickoff | Eng Lead | 2026-05-22 | PRD final approval |
| PagerDuty webhook integration working | Eng | 2026-05-30 | All incident-linked features blocked until complete |
| Alpha: runbook capture form (M-01, M-02, M-03) | Eng + Design | 2026-06-06 | First testable user flow |
| Alpha: runbook retrieval at page time (M-04) | Eng | 2026-06-10 | Requires at least 10 captured runbooks in design partner data |
| Alpha: intelligent routing (M-05, M-06) | Eng | 2026-06-13 | Requires runbook capture to be generating data |
| Alpha: HDI dashboard (M-07, M-10) | Eng + Design | 2026-06-17 | Requires 2+ weeks of incident data from design partner |
| Design partner pilot begins | PM + CS | 2026-06-20 | All Must Have requirements complete |
| MVP review / go/no-go for broader rollout | CPO + PM | 2026-07-11 | 3 weeks of design partner data |
