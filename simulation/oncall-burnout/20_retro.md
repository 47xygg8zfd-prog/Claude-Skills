# File 20 — Retrospective: Sentinel MVP
**Product**: Sentinel — On-Call Intelligence Platform  
**Date**: 2026-05-12  
**Sprint range**: Sprints 1–4 (8 weeks, 2026-03-17 to 2026-05-09)  
**Participants**: PM, Eng Lead, Design Lead, QA Lead, Tech Lead  
**Format**: Honest review — what the data says, not what we wish it said

---

## Status Check Before We Start

The product shipped. That matters. Beta customers are live. Runbook capture and routing are working. But "we shipped" is not the same as "we hit our targets." This retro treats those as separate questions.

---

## What We Got Wrong

| # | Assumption We Made | What Actually Happened | Severity | Implication |
|---|-------------------|------------------------|----------|-------------|
| 1 | Engineers would write quality runbooks when prompted by the modal | In concierge testing, ~40% of submissions were 1-2 sentences ("restarted the service," "cleared the queue"). Technically compliant, operationally useless. | High | We built a capture mechanism without defining what "captured" means. The runbook library is growing in volume but not in quality. Search returns results that don't help. |
| 2 | Heuristic routing would be straightforward — match `alertType` to resolution history | Alert names for the same underlying failure arrived in 5 different text formats from different services (e.g., "payment-service timeout," "payment_svc: conn timeout," "CRIT: payments/timeout," "SLO breach: payment latency," "payment-processor down"). Exact-match heuristics gave near-zero routing quality on these. We had to add fuzzy normalization that wasn't scoped. | High | Added 4 days to the routing implementation. The "simple heuristic" assumption was the biggest scope error of the project. |
| 3 | HDI was a metric managers would understand immediately | In beta testing, 3 of 5 managers asked "what does 64% mean — is that bad?" One asked "64% of what exactly?" The number alone means nothing without context about what a healthy HDI looks like for their team size. | Medium | We shipped a number without a benchmark. The `<HDIExplainerCard>` we added in sprint 4 helps, but we should have baked benchmarks (e.g., "teams under 30 engineers typically see HDI of 40–55%) into v1 and didn't. |

### What We Should Have Done

1. **Runbook quality**: We should have defined a "runbook quality score" — minimum fields, minimum step length, structural requirements — before building the capture form. Now we have to retrofit quality checks onto a form that already exists, and we have weeks of low-quality data we can't easily improve retroactively. The template selector was added late; it should have been the default.

2. **Heuristic routing**: We should have spiked alert name normalization before sprint 1. The devil's advocate review flagged "routing complexity" as a risk (it's documented in file 06). We correctly decided to simplify to heuristics. We incorrectly assumed heuristics meant no text processing. Those are not the same thing.

3. **HDI benchmarking**: A metric that requires explanation to every user is a metric that won't be used. We knew managers weren't data people. We should have built the benchmark context ("is this good or bad for my team size?") in from day one — not as an explainer card bolted on at the end.

---

## What Slowed Us Down

### pgvector Setup — Lost 3 Days in Sprint 2

**What happened**: The Postgres instance on our production DB tier (Standard tier) did not have the `pgvector` extension available. It requires the Advanced tier. We discovered this when the backend engineer attempted to enable the extension during sprint 2 deployment. Tier upgrade required a 24-hour window for the infrastructure team plus configuration changes.

**Impact**: 3 engineering days lost. Runbook search was pushed from sprint 2 to sprint 3. Sprint 3 was compressed.

**Why we didn't catch it earlier**: We verified pgvector availability on our local dev Postgres instances and on the staging environment, which was already on Advanced tier from an earlier unrelated upgrade. We didn't check the production tier until we were ready to deploy.

**Prevention**: Infrastructure requirements (DB extensions, min tier, OS packages) belong on a pre-sprint infra checklist, signed off before sprint kickoff. We did not have this checklist. We do now.

### Alert Name Normalization — Added 4 Days in Sprint 3

Covered above under "What We Got Wrong." The scope of normalization work was discovered mid-sprint, not at planning. This was an information gap, not a process gap — we couldn't have known without the spike we should have run earlier.

### HDI Schedule API — Blocked 1 Week (Ongoing)

PagerDuty's schedule API is significantly more complex than documented. Overrides, escalation layers, and multi-timezone on-call rotations each require separate handling. Tech lead identified this in sprint 4 review. We are managing it by delaying HDI launch 1 week, not by cutting scope.

---

## What We'd Do Differently

### 1. Run the Concierge Test and Spike the Routing Engine Before Sprint 1 Starts

The concierge test gave us the most useful signal of the entire project. We ran it in week 3. If we had run it in week 0 (before sprint 1), we would have:
- Seen the low runbook quality problem before designing the capture form
- Discovered the alert name normalization problem before sizing routing work
- Had actual MTTR and capture rate baselines to design against

The routing engine spike would have taken 2 days. It would have saved 4 days of mid-sprint scope expansion.

**Concrete change**: Future MVPs — concierge test and critical-path tech spikes are required to complete before sprint 1 planning. Not "nice to have." Gate.

### 2. Define "Runbook Quality Score" Before Building Runbook Capture

We built a form before we knew what a good form output looked like. This is backwards. Before the next sprint that touches the capture flow, we need to:
- Interview 5 engineers about what makes a runbook actually useful
- Define minimum quality criteria (e.g., ≥3 steps, each ≥20 chars; at least one field for "root cause"; at least one field for "verify resolution")
- Build the quality score into the DB schema and API from the start

Right now, we have a quality problem we can only fix by retrofitting. That retrofit is sprint 5 work that didn't need to be sprint 5 work.

### 3. Build HDI Benchmarks Into v1

"What's a good HDI?" is the first question every manager asks. We should have answered it before launch, not after.

For the next iteration, HDI benchmarks should be built into the dashboard display:
- Industry percentile (once we have enough customers)
- Team-size-adjusted benchmark ("teams of 8-12 typically see HDI 40-60%")
- Target range shown directly on the chart (not just a reference line)

This is not technically complex. It requires research (what's a healthy HDI distribution?) that we should have done during discovery, not post-launch.

---

## What Worked

### Devil's Advocate Review Caught the Routing Engine Complexity Early Enough to Matter

In sprint 1 planning, the devil's advocate review (file 06) flagged "routing complexity" and "alert name variability" as risks. We made a deliberate decision to constrain the routing engine to heuristics instead of ML. That decision was correct and saved us from a much larger scope explosion.

We didn't fully scope the heuristic work correctly — but we would have been in a much worse position if we'd tried to ship an ML routing engine. The devil's advocate review was worth the hour it took. We're formalizing it as a standing pre-sprint ritual.

### QA Race Condition Test Caught a Real Bug Before Beta

The P0 race condition test (two simultaneous webhooks for the same alert type, filed in the QA plan) caught a genuine concurrency bug in sprint 2. Two concurrent routing computations against the same incident history were reading an uncommitted DB write, causing both suggestions to recommend the same engineer regardless of load. This would have been embarrassing in a live beta.

The test was added by the QA lead as a "gut feel" P0 — not derived from the spec. This is exactly the kind of judgment-driven QA addition that matters. The bug would not have been caught by spec-derived tests alone.

### Blocking Modal Design Was Right

The debate about whether to make the runbook capture modal truly blocking (vs. a persistent nudge or reminder) happened in sprint 2 design review and was contentious. The "no dismiss without action" approach felt harsh. We shipped it anyway because the concierge data showed that a non-blocking prompt had ~0% completion.

The beta data so far supports the decision. Capture completion rate in the first week of soft launch is 61%. This is above our 60% target. We don't know yet if quality is high, but the behavior intervention is working.

---

## Metrics Check-In

These are honest numbers. We are not at target. We are tracking in the right direction.

| Metric | Baseline | Target (60 days) | Current (beta, week 1) | Status |
|--------|----------|------------------|------------------------|--------|
| MTTR (median) | 47 min | 28 min | 39 min | Below target — expected at this stage (low runbook coverage) |
| Hero Dependency Index | 64% | 30% | 51% | Progress but far from target — expected, needs time |
| Runbook capture completion rate | N/A | > 60% | 61% | On target — early positive signal |
| Routing suggestion acceptance | N/A | > 50% | 63% | On target |
| Runbooks with ≥3 steps (quality proxy) | N/A | > 70% | 38% | Off target — quality problem confirmed |

**Honest read on MTTR**: 47 → 39 minutes is an 17% improvement. Our target is 40%. We're directionally correct. But 39 minutes is the MTTR when engineers use a runbook. The overall MTTR, including incidents resolved without a runbook, is likely higher. We don't have the full picture yet. We need 30+ days of beta data to get a clean number.

**Honest read on HDI**: 64% → 51% in 4 weeks of beta is meaningful movement. But 51% is still "Critical" on our own health scale. We set a 90-day target for a reason — this metric requires routing and knowledge distribution to accumulate. We should not be alarmed by 51%, but we should not present it as success either.

**The thing we're most worried about**: The runbook quality number (38% of submissions have ≥3 steps). The rest of the product only works if the runbook library is actually useful. Search returns junk if runbooks are junk. Routing improves only if the runbooks it references are complete enough to matter. Quality is the keystone problem for sprint 5.

---

## Next Discovery Questions

These feed directly into the next discovery cycle. Each question has a method and priority.

| # | Question | Why It Matters | Method | Priority |
|---|----------|---------------|--------|----------|
| 1 | Why do 59% of engineers skip the runbook capture prompt? | This is the highest-leverage question we have. If we understand why engineers skip, we can either reduce friction on the capture side, better target which incidents should require capture, or redesign the skip flow to gather more signal. Right now "skip" is a black box. | 5-7 engineer interviews (beta cohort); filter to engineers who skipped ≥3 times | P0 |
| 2 | What runbook structure do engineers actually find useful when resolving an unfamiliar incident? | We built the capture form before understanding the read use case. The question is: when an engineer is paged for an alert they've never seen, what information do they actually need in a runbook? Steps? Root causes? Verification commands? Links? We don't know. | 5-user study: give engineers a live (or simulated) unfamiliar alert; observe what they look for in the runbook library; where do they get stuck? | P0 |
| 3 | Do managers use the HDI dashboard proactively (weekly review habit) or only reactively (after an incident or someone complains about on-call load)? | If proactive, the dashboard's job is to be part of a weekly ritual — we should integrate with calendar/Slack reminders. If reactive, the dashboard's job is to surface at the right trigger moment — we should consider HDI alerts ("your HDI crossed 60% this week"). These are different products. | Pull beta usage data: session timestamps vs. incident timestamps for HDI dashboard views. Supplement with 2-3 manager interviews. | P1 |

---

## One Thing We'd Tell the Team

We shipped something that works. The concierge test showed 52% MTTR improvement when the product is used correctly. The blocking modal is driving 61% capture completion. The routing suggestions are being accepted 63% of the time.

But "works when used correctly" is a fragile foundation. The product's value depends on runbook quality, and runbook quality depends on engineers doing something that takes more than 10 seconds. That's the real problem in front of us, and sprint 5 needs to treat it as the primary objective — not a cleanup task.

The ship is in the water. Now we have to make it actually go somewhere.
