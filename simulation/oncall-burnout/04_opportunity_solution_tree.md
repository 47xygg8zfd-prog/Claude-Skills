# Sentinel — Opportunity Solution Tree
**Stage 4 of 20: Opportunity Solution Tree**
**Date:** 2026-05-12
**Author:** PM
**Status:** Draft — under review before PRD

---

## Desired Outcome

**Reduce Hero Dependency Index from 65% to <30% within 90 days of adoption.**

This is the north star metric for Sentinel. It is chosen because:
- It is directly observable from incident data (no instrumentation required beyond what PagerDuty/OpsGenie already captures)
- It is a team-health metric, not an individual performance metric — managers can act on it without HR implications
- A reduction from 65% to <30% is a meaningful enough change to justify the product investment (roughly doubling the effective on-call pool)
- It is a lagging indicator of the behaviors we are changing: runbook capture → routing accuracy → hero dependency falls as more engineers can self-serve

**Supporting metrics** (move these to validate Sentinel is working before HDI shifts):
- MTTR: 47 min baseline → 28 min target
- Runbook coverage rate: % of recurring alert types with a validated runbook — target: 70% within 60 days
- Escalation rate: % of incidents requiring a human escalation outside the assigned on-call — target: reduce by 40%

---

## OST Diagram

```
DESIRED OUTCOME
Reduce Hero Dependency Index from 65% to <30% within 90 days

│
├── OPPORTUNITY 1: "I can't resolve this without calling [specific person]"
│   (Knowledge concentration — institutional knowledge lives in 3-4 heads)
│   │
│   ├── Solution 1a: Runbook capture at incident close [v1 — PRIORITIZED]
│   │   Auto-prompt structured form before engineer can close alert;
│   │   3–5 guided fields; <90 sec to complete; attached to alert type
│   │
│   ├── Solution 1b: Intelligent routing to last resolver [v1 — PRIORITIZED]
│   │   When new incident arrives, surface the engineer who last resolved
│   │   this alert type; show their runbook inline; route notification first
│   │
│   └── Solution 1c: Expert directory — who knows what [v2]
│       Profile-based knowledge map: which engineers have resolved which
│       alert types and how many times; searchable by alert name
│
├── OPPORTUNITY 2: "I spent 45 minutes on something that should take 5"
│   (Undocumented procedures — repeat incidents solved from scratch)
│   │
│   ├── Solution 2a: Runbook retrieval at page time [v1 — PRIORITIZED]
│   │   When engineer receives page, auto-surface the most relevant
│   │   runbook using pgvector similarity search on alert title + body
│   │
│   ├── Solution 2b: Runbook staleness signal [v1 — PRIORITIZED]
│   │   Surface "last validated N months ago / X incidents ago" warning
│   │   on runbooks; flag runbooks not validated in 6+ months
│   │
│   └── Solution 2c: Guided runbook templates by alert category [v2]
│       Pre-structured templates for common alert types (DB, infra,
│       network); reduce blank-page problem for new runbook creation
│
├── OPPORTUNITY 3: "I was paged 8 times last week; my teammate got paged once"
│   (Unfair rotation — load imbalance causes individual burnout)
│   │
│   ├── Solution 3a: Hero Dependency Index dashboard [v1 — PARTIAL]
│   │   Show manager % of incidents resolved by top N engineers;
│   │   does not fix distribution but makes it visible and actionable
│   │
│   ├── Solution 3b: Rotation fairness scheduler [v2 — DEFERRED]
│   │   Intelligent rotation that factors in incident complexity, not
│   │   just calendar slots; balances actual load not just turns
│   │
│   └── Solution 3c: Load alerts for managers [v2 — DEFERRED]
│       Automated Slack/email alert to manager when one engineer's
│       incident count exceeds team mean by 2x in a rolling week
│
└── OPPORTUNITY 4: "I don't know who to escalate to without bothering everyone"
    (Unclear escalation paths — no structured knowledge of who to call)
    │
    ├── Solution 4a: Intelligent routing surfaces escalation contact [v1 — PARTIAL]
    │   Routing already solves this for known alert types; the engineer
    │   receives a named contact, not a Slack channel to broadcast to
    │
    ├── Solution 4b: Escalation path visualizer [v2]
    │   Visual tree showing who escalates to whom for each service area;
    │   built from historical escalation patterns in PagerDuty/OpsGenie
    │
    └── Solution 4c: On-call context card [v2]
        When engineer is paged, show a card: primary on-call, secondary,
        SME for this service, manager — all one click to contact
```

---

## Opportunity Nodes — Detail

### Opportunity 1: Knowledge Concentration
*"I can't resolve this without calling [specific person]"*

**Research evidence:**
- 8/10 participants reported weekly incidents that required escalation to a specific named engineer
- P7 (senior IC): "There are 4 alerts in our system where I'm the only person who knows the fix. Every time one fires on someone else's shift, they call me."
- P1 (EM): after hero departure, team MTTR went from 23 minutes to 71 minutes in 60 days; still at 58 minutes 8 weeks later
- P10 (junior IC): called a senior engineer at 2:30am for a Redis timeout that had a known fix; total MTTR was 47 minutes; the engineer who took the call fixed it in 4 minutes

**Why it's an opportunity, not a solution:** The underlying job is resolution confidence — the engineer needs to believe they can handle what they're paged for. The current state (call the hero) is a workaround, not a solution. Multiple solution directions exist.

**Frequency:** Very high — reported as weekly or more by 8/10 participants  
**Severity:** Critical — directly determines whether incidents are self-resolved or escalated  
**Addressability:** High — runbook capture + routing directly addresses the mechanism

---

### Opportunity 2: Undocumented Procedures
*"I spent 45 minutes on something that should take 5"*

**Research evidence:**
- P4 data: 23% of alerts were exact repeats; of those, 61% had no associated runbook
- P7: "I've fixed the same Kafka consumer lag alert at least six times. My fix is in my personal notes. When I'm on vacation, someone else spends an hour on it."
- P9: "I have 47 open Jira tickets tagged TODO:runbook. I look at them every sprint and close the tab."
- P2: Confluence audit showed 60% of runbook pages last edited >12 months ago; 3 runbooks actively caused longer MTTRs because they described infrastructure that had since changed

**Why this is distinct from Opportunity 1:** Opportunity 1 is about *access to knowledge*. Opportunity 2 is about *existence of knowledge*. You can have perfect routing and still arrive at an empty or broken runbook. Both must be solved.

**Frequency:** High — 7/10 participants confirmed repeat incidents solved from scratch  
**Severity:** High — pure waste; quantifiable MTTR cost  
**Addressability:** High — capture mechanic at incident close directly creates the missing runbooks

---

### Opportunity 3: Unfair Rotation
*"I was paged 8 times last week; my teammate got paged once"*

**Research evidence:**
- P3: "Two of my five on-call engineers are paged 3x as often as the other three. Not because of the rotation — because they get escalated to when the others can't resolve."
- P6: "We have fairness in the calendar. We don't have fairness in outcomes. The same people get called on other people's shifts constantly."
- P1: Hero departure was preceded by 6 months of escalation data showing the departing engineer was receiving 68% of all escalation calls

**Why it's deferred (mostly):** Rotation fairness requires calendar integration, on-call schedule management, and a fundamentally different product surface. It is a valid problem but a separate product problem. The Hero Dependency Index (v1) gives managers visibility without Sentinel needing to manage the rotation itself. The scheduler is v2.

**Frequency:** Medium — 5/10 participants raised this  
**Severity:** High — primary driver of individual engineer burnout (distinct from MTTR)  
**Addressability for v1:** Partial — dashboard makes it visible; full solution is v2

---

### Opportunity 4: Unclear Escalation Paths
*"I don't know who to escalate to without bothering the whole team"*

**Research evidence:**
- P10: "I send a message to #engineering-oncall and wait. Usually 3 people respond but I don't know who actually knows the answer. The average time to useful response is 15 minutes."
- P8: "I've been in situations where I was escalating to the wrong person for 20 minutes because I didn't know who owned that service."
- P4 data: Average escalation time in OpsGenie data = 18 minutes; estimated 60% of that is identifying who to contact

**Why it's partially addressed by v1:** Intelligent routing (Solution 1b) already tells the engineer who last resolved this alert type. For known, recurring alerts, this largely solves Opportunity 4 automatically. The gap is for novel alerts with no routing history — escalation path visualizer (v2) covers that case.

**Frequency:** High — 9/10 participants described unclear escalation as common  
**Severity:** Medium — extends MTTR but is rarely the primary cause  
**Addressability for v1:** Partial — covered for recurring alerts by routing; novel alerts remain a gap

---

## Solution Prioritization for v1

| Solution | Opportunity | Priority | Rationale |
|----------|-------------|----------|-----------|
| Runbook capture at incident close | Opp 1, Opp 2 | v1 — Must Have | Core mechanic; nothing else works without this data |
| Runbook retrieval at page time | Opp 2 | v1 — Must Have | Closes the loop — capture is only useful if retrieval is instant |
| Intelligent routing to last resolver | Opp 1, Opp 4 | v1 — Must Have | Reduces escalation time; surfaces named contact instead of Slack broadcast |
| Runbook staleness signal | Opp 2 | v1 — Should Have | Prevents P-2 pain (wrong runbook erodes trust); low implementation cost |
| Hero Dependency Index dashboard | Opp 3 | v1 — Should Have | Manager buy-in metric; necessary for the north star measurement |
| Expert directory | Opp 1 | v2 | Valuable but requires enough data to populate; circular dependency on v1 capture |
| Rotation fairness scheduler | Opp 3 | v2 | Calendar integration scope; separate product problem |
| On-call context card | Opp 4 | v2 | Useful but Opp 4 is partially covered by routing |
| Load alerts for managers | Opp 3 | v2 | Good feature; lower priority than core resolution mechanics |
| Escalation path visualizer | Opp 4 | v2 | Solves novel alert gap but requires historical escalation data; time-gated |

---

## Assumption Map

| # | Assumption | Opportunity | Confidence (post-research) | Smallest Test |
|---|---|---|---|---|
| A1 | Engineers will complete the structured capture form at incident close | Opp 1, Opp 2 | **High** — 7/10 said yes with design constraints met; P5 gave explicit design requirements | Ship with first 3 design partner customers; measure form completion rate. Target: >60% within 2 weeks. |
| A2 | Alert similarity search (pgvector) will match the right runbook >70% of the time | Opp 2 | **Medium** — alert naming is inconsistent across customers; similarity matching is unproven on real data | Offline test: take P4's PagerDuty export, run embedding similarity on alert titles, manually validate top match. Before writing routing logic. |
| A3 | Engineers will trust and act on routing suggestions | Opp 1, Opp 4 | **Medium** — depends on routing accuracy and transparency of "why" explanation | A/B test in design partner: routing with explanation vs. routing without; measure whether suggested contact is actually reached |
| A4 | Managers will use HDI dashboard in 1:1s and QBRs without being prompted | Opp 3 | **Medium** — 5/6 managers said they would; intent ≠ behavior | Track weekly active sessions on dashboard during first 30 days of design partner. Target: 3+ sessions/manager/month. |
| A5 | The "last successful resolver" heuristic is better than random rotation for MTTR | Opp 1 | **Medium** — intuitively correct but not yet proven at our target customer scale | Compare MTTR for routed incidents vs. non-routed incidents in design partner data at 30-day mark. |
| A6 | Runbook content will not contain secrets/credentials that create a data privacy blocker | Opp 1, Opp 2 | **Low** — P4 raised this concern explicitly; infra runbooks often reference internal hostnames, creds | Add a data handling FAQ to design partner onboarding; add credential scrubbing regex to capture form pre-storage. Validate with 1 security-conscious customer before broad rollout. |

**A6 is the highest-risk unvalidated assumption.** If enterprise customers cannot store runbooks in Sentinel's cloud due to data privacy requirements, the TAM narrows significantly. Mitigation: self-hosted deployment option added to roadmap.

---

## PRD Traceability Table

This table ensures every PRD requirement can be traced back to a specific opportunity and research evidence.

| PRD Requirement | Opportunity | Research Evidence | Solution Node |
|----------------|-------------|-------------------|---------------|
| Structured runbook capture form (3–5 fields, <90 sec) | Opp 2 | P5: "Give me checkboxes... I'll fill that in"; P7, P9 confirmed 90-sec threshold | Solution 2a capture |
| Form triggered at incident close, before mark-resolved is available | Opp 1, Opp 2 | Behavioral evidence: "I'll add the runbook later" pattern across 8/10 participants | Solution 1a |
| Runbook surfaced inline when engineer receives page | Opp 2 | P10: 47-min MTTR for 4-min fix; P8: searched Slack back 8 months | Solution 2a retrieval |
| Routing notification shows "last resolved by [name] on [date]" | Opp 1, Opp 4 | P10: called wrong person for 20 min; P4 data: avg 18-min escalation time | Solution 1b |
| Runbook staleness warning after 6 months or 10 incidents without re-validation | Opp 2 | P2: Confluence audit showing 40% follow-and-fail rate for old runbooks | Solution 2b |
| Hero Dependency Index: % of incidents resolved by top 3 engineers | Opp 3 | P3: "I can't prove it to finance"; P1: HDI was 68% for departing engineer 6 mo before churn | Solution 3a |
| HDI dashboard is manager-only, no individual naming visible to ICs | Opp 3 | P5: surveillance concern; research design constraint | Solution 3a |
| Graceful fallback to standard rotation when no routing match exists | Opp 1 | P6: new microservice deployments create new alert types quarterly | Solution 1b |
| PagerDuty and OpsGenie webhook integration | All | All participants used one or the other; no other tools in scope | Architecture |
