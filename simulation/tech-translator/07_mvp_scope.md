# MVP Scope: Bridge — Technical Translator for PMs
**Date:** 2026-05-13
**Author:** PM, Bridge
**Status:** Scope draft — pending design kickoff approval

---

## Core Hypothesis

PMs who paste technical content into Bridge and receive context-aware explanations will return weekly and recommend Bridge to other PMs, because in-the-moment technical clarity is not available from any existing tool in their workflow.

The hypothesis has two testable components:
1. **Behavioral return**: PMs who get a useful explanation come back the next time they hit a technical term they don't understand.
2. **Referral**: PMs who see value tell other PMs — either by sharing an explanation (S-03) or by word of mouth.

The hypothesis is falsified if week-4 retention is below 35% among activated users, even if satisfaction scores are high. Satisfaction without return means the product is nice-to-have, not a habit.

---

## MVP 1 — Hypothesis Validation (Weeks 1–8)

### What we're testing

Can we prove that PMs return to Bridge after their first useful explanation, without workflow integration, without team features, and without integrations? If yes, we have proof the core explanation loop has standalone value and we can invest in integrations. If no, we need to understand whether the problem is explanation quality, product friction, or the deeper trust problem (see Devil's Advocate File 06).

### Requirements included

| Req ID | Requirement | Rationale for inclusion |
|--------|-------------|--------------------------|
| M-01 | Paste any technical content → receive plain English explanation | Core loop — no test is possible without it |
| M-02 | Context-aware explanations (PM role framing, decision-relevant summary, suggested follow-up question) | Differentiates from ChatGPT; PM role framing must be structural, not just a system prompt |
| M-03 | "Go Deeper" toggle for progressive technical detail | Required to serve both novice PMs and "accidental technical PMs" without overwhelming either |
| M-04 | Confidence indicator on all explanations | Non-negotiable trust and safety feature; wrong explanations acted on in sprint planning are brand-destroying |
| M-05 | Conversation mode for follow-up Q&A | Required to measure whether PMs build working knowledge vs. just getting one-off answers |

### What is explicitly excluded

- Browser extension (S-01): requires browser store approvals and additional build time; keeping it out of MVP 1 is a deliberate scope decision, not a deferral of the core product
- Explanation history and search (S-02): useful but not required to test the return hypothesis; a PM who returns to Bridge for a new explanation is demonstrating retention even without searchable history
- Team sharing (S-03): social trust barrier must be understood before we build sharing UX (see Devil's Advocate File 06, Assumption 3)
- Jira integration (C-02): adds significant integration complexity; workflow-embedded value can be partially validated by whether standalone web app generates returns without it

### Additional MVP 1 requirement (not in PRD tiers)

**Behavioral outcome prompt**: After a PM receives an explanation, prompt once per session (not on every explanation) with a lightweight question: "Did you use this? Yes — I sent a message, rewrote a ticket, or asked a follow-up. Still thinking about it. No — I wasn't confident enough to act on it." This single data point is the leading indicator for whether quality or trust is the bottleneck. It must ship in MVP 1 even though it is not in the original requirements list, because it determines the MVP 2 design direction.

### Success gate (all must be met to proceed to MVP 2)

| Metric | Threshold | Measurement window |
|--------|-----------|-------------------|
| Week-4 retention (activated users) | ≥ 35% | Weeks 5–8 of closed beta |
| Explanation satisfaction (thumbs up rate) | ≥ 65% | All explanations, MVP 1 window |
| Behavioral outcome ("used it") rate | ≥ 40% of prompted sessions | MVP 1 window |
| NPS from design partners | ≥ 30 | End of week 8 |
| Confidence flag rate (low confidence surfaced and not hidden) | Calibration check — at least 15% of explanations show non-maximum confidence | MVP 1 window |

Note on the confidence flag rate: this is not a PM-facing success metric — it is an internal calibration check. If 95%+ of explanations show maximum confidence, the confidence indicator has been calibrated to be reassuring rather than honest. That is a product integrity failure.

### Risk if we stop at MVP 1

If MVP 1 succeeds and we stop, we have validated standalone PM adoption but built nothing that is defensible against ChatGPT or the first well-funded competitor who ships a Jira integration. The standalone web app is a testing instrument, not the product. Stopping here means a small, loyal user base with no structural moat and no enterprise path. The correct risk is not stopping at MVP 1 — the correct risk is interpreting MVP 1 success as proof the product is done.

---

## MVP 2 — Workflow Integration (Weeks 9–16)

### Unlock criteria

MVP 2 begins only when MVP 1 hits all five success gate thresholds. If the behavioral outcome rate ("used it") is below 40%, MVP 2 scope changes: instead of adding integrations, the team investigates the trust gap identified in the Devil's Advocate review (File 06, Assumption 3) before building anything new. Adding integrations to a product that PMs cannot confidently act on does not fix the core problem.

### What we're testing

Does bringing Bridge into the PM's existing workflow (GitHub, Jira, Linear) convert occasional use into daily habit? Does in-context availability remove the "I forgot to check Bridge" failure mode?

### Requirements included

| Req ID | Requirement | Rationale |
|--------|-------------|-----------|
| M-01 through M-05 | Carry forward from MVP 1 | Core explanation loop, refined based on MVP 1 feedback |
| S-01 | Browser extension for in-context explanations on GitHub/Jira/Linear | The primary differentiation hypothesis — this is the feature that answers "why not just use ChatGPT?" |
| S-02 | Explanation history and search | Required for the extension to feel like a persistent tool, not a stateless lookup; also the precondition for team sharing |

### Browser extension scope note

S-01 covers GitHub, Jira, and Linear. In MVP 2, ship Jira only. Jira is where the ICP PM spends the most time during sprint cycles, and Jira's extension surface is more predictable than GitHub's (where PR review UX is complex and developer-audience concerns arise). GitHub extension follows in MVP 3 or as a mid-MVP 2 addition if Jira extension adoption exceeds 50% of active users within the first two weeks.

### New measurement: extension adoption rate

The browser extension lives or dies on install rate. Track separately:
- Extension install rate among active web app users (target: ≥ 50% of active users within 4 weeks of extension availability)
- Explanation trigger rate from extension vs. web app (if extension is the right product, extension-triggered explanations should exceed web app volume by week 4 of MVP 2)
- Session start context: did the PM's session begin from the extension or from the web app? This tells us whether the extension is the entry point or a supplementary surface.

### Success gate (all must be met to proceed to MVP 3)

| Metric | Threshold | Measurement window |
|--------|-----------|-------------------|
| Extension install rate among active users | ≥ 50% | Weeks 13–16 |
| Extension-triggered explanations vs. web app | Extension ≥ 40% of all explanations | Week 14–16 |
| Week-8 retention (full MVP 2 cohort) | ≥ 45% | End of week 16 |
| Explanation history use rate | ≥ 30% of weekly active users search or revisit history at least once | Weeks 13–16 |
| Design partner expansion | ≥ 3 design partners have added a second PM seat | End of week 16 |

The expansion signal (second seat added by design partners) is the earliest indicator of organic team growth, which is the premise of MVP 3. If no design partner has expanded by week 16, the team product hypothesis has not been validated and MVP 3 scope should be narrowed.

### Risk if we stop at MVP 2

MVP 2 with history and browser extension is a credible standalone product — potentially fundable and acquirable. The risk of stopping here is leaving the defensibility question unanswered: individual tools churn when engineers change companies, teams change, or ChatGPT ships a Jira plugin. The team product (MVP 3) is what creates switching cost. But stopping at MVP 2 is not a failure — it is an honest strategic option if expansion signals don't materialize.

---

## MVP 3 — Team and Platform (Weeks 17–24)

### Unlock criteria

MVP 3 begins only when the design partner expansion signal has materialized: at least 3 accounts have added a second active PM seat, and at least one account has asked unprompted about team-level features (shared glossary, shared history, or admin-level usage visibility). If expansion is not happening organically, MVp 3 must be re-scoped to investigate why before building team infrastructure.

### What we're testing

Does shared technical vocabulary across a product team create a durable reason to stay that individual explanations cannot? Does the team glossary (C-01) reduce onboarding time for new PMs at a company, and does that reduction become a case study for enterprise sales?

### Requirements included

| Req ID | Requirement | Rationale |
|--------|-------------|-----------|
| M-01 through M-05 | Core explanation loop, fully refined | Foundation of all team features |
| S-01 | Browser extension (Jira + GitHub) | Extension must cover both surfaces before team adoption scales |
| S-02 | Explanation history and search | Required for team sharing to be useful — you cannot share what you cannot find |
| S-03 | Team sharing of saved explanations | Creates the shared vocabulary and reduces repeated lookups for the same terms |
| C-01 | Proactive glossary building from company/team vocabulary | The long-term moat: a glossary that is specific to a company's codebase, team language, and product context cannot be replicated by a generic AI tool |
| C-02 | Jira integration — auto-suggest explanations in tickets | Completes the workflow loop: Bridge suggests explanations in the ticket view without the PM needing to trigger it |

### What MVP 3 proves

If MVP 3 succeeds — team adoption, glossary engagement, Jira auto-suggest driving passive explanations — Bridge has answered the ChatGPT inertia problem structurally: it is not a better place to get an explanation, it is the place where your team's technical vocabulary lives. That is not replicated by a generic AI tool and cannot be easily ported if a PM changes companies.

### Full vision north star

By the end of MVP 3, a Bridge account should contain: every technical term that has appeared in the team's Jira tickets over the past six months, with PM-authored notes on which explanations were most useful; a team glossary that new PMs are invited to review on their first day; and an explanation history that surfaces recurring technical concepts so the PM can recognize when the same trade-off is being discussed again six sprints later. The product has become the team's institutional technical memory.

### Success gate

| Metric | Threshold | Measurement window |
|--------|-----------|-------------------|
| Team accounts (3+ active seats) | ≥ 20 accounts | End of week 24 |
| Glossary terms created per active account | ≥ 10 terms in first 30 days | Weeks 17–24 |
| Jira auto-suggest click-through rate | ≥ 25% of surfaced suggestions are opened | Weeks 21–24 |
| 30-day team retention | ≥ 60% of team accounts active in month 2 | End of week 24 |
| NPS (paid users) | ≥ 45 | End of week 24 |

---

## Phase Summary Table

| Phase | Weeks | Requirements | Key Bet | Success Gate |
|-------|-------|-------------|---------|-------------|
| MVP 1 — Hypothesis Validation | 1–8 | M-01 through M-05 | Standalone explanation loop drives return | 35% week-4 retention; 40% behavioral outcome rate; NPS ≥ 30 |
| MVP 2 — Workflow Integration | 9–16 | MVP 1 + S-01 (Jira only), S-02 | In-context extension converts occasional use to daily habit | 50% extension install; 45% week-8 retention; 3 design partners expand |
| MVP 3 — Team and Platform | 17–24 | MVP 2 + S-01 (GitHub), S-03, C-01, C-02 | Shared vocabulary creates defensible moat | 20 team accounts; 60% 30-day team retention; NPS ≥ 45 |

---

## Experiment Scope Note

MVP 1 is not just a build phase — it is an experiment with a specific falsification condition. If week-4 retention is below 35% among activated users, the experiment result is: the standalone explanation loop does not produce habitual return. Before proceeding to MVP 2, the team must run a structured root cause analysis:

- **If explanation quality scores are low** (thumbs up < 65%): the LLM quality or prompt engineering is the bottleneck. Investigate model selection, prompt structure, and confidence calibration before building any new features.
- **If quality scores are high but behavioral outcome rate is low** (< 40% of users report acting on explanations): the bottleneck is trust-to-act, not explanation quality. Revisit the social trust framing identified in the Devil's Advocate review (File 06, Assumption 3). The next experiment is a UX change, not a feature addition.
- **If both scores are high but retention is still low**: the product is perceived as useful in the moment but not worth returning to. This is the ChatGPT inertia problem (File 06, Assumption 1) in its most direct form. The next experiment is the browser extension — does removing the need to "remember to open Bridge" change the retention pattern?

Each failure mode has a different next action. Treating them as the same ("retention is low, we need to improve the product") wastes a sprint on the wrong intervention.
