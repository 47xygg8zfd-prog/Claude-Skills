# Sentinel — UX Research Synthesis
**Stage 3 of 20: UX Research**
**Date:** 2026-05-12
**Author:** PM / UX Research Lead
**Status:** Complete — synthesis approved, ready for OST

---

## Research Overview

**Method:** Semi-structured interviews, 45–60 minutes each  
**Participants:** 10 total (6 engineering managers, 4 senior ICs)  
**Recruitment:** 7 current customers, 3 non-customers via PM network  
**Dates conducted:** 2026-04-28 through 2026-05-09  
**Sessions recorded:** Yes (consent obtained). Notes in Confluence: PROD/SENTINEL/ux-research-sessions  

---

## Participant Table

| ID | Role | Company Stage | Team Size | On-Call Setup | Hero Departure in 12 mo? | Notes |
|----|------|---------------|-----------|---------------|--------------------------|-------|
| P1 | Engineering Manager | Series B | 120 engineers | PagerDuty, 6-person rotation | Yes — 1 senior SRE left | Described 8-week MTTR spike post-departure |
| P2 | Engineering Manager | Series C | 180 engineers | OpsGenie, 9-person rotation | No | Proactively showed us their Confluence runbook space — 60% pages last edited >1 year ago |
| P3 | Engineering Manager | Series A | 55 engineers | PagerDuty, 4-person rotation | Yes — 2 of 4 on-call engineers left within 6 months | Team in active crisis; participated hoping for solutions |
| P4 | Engineering Manager | Late Stage (pre-IPO) | 160 engineers | OpsGenie, two independent on-call rotations | No | Most data-mature participant; could provide PagerDuty exports |
| P5 | Engineering Manager | Series B | 95 engineers | PagerDuty, 5-person rotation | No | Most skeptical participant; pressed hard on "will engineers actually document?" |
| P6 | Engineering Manager | Series B | 75 engineers | PagerDuty, 5-person rotation | Yes — 1 hero left 4 months ago | MTTR still elevated; described it as "organizational scar tissue" |
| P7 | Senior Software Engineer (IC) | Series C | 180 engineers | Same team as P4 | N/A | Self-described hero; exhausted; participated with explicit permission from manager |
| P8 | Mid-Level Software Engineer (IC) | Series B | 95 engineers | Same team as P5 | N/A | Non-hero; described the experience of being paged and having no idea what to do |
| P9 | Senior Software Engineer (IC) | Series B | 120 engineers | Same team as P1 | N/A | Recently promoted to senior; inheriting hero burden |
| P10 | Mid-Level Software Engineer (IC) | Series A | 55 engineers | Same team as P3 | N/A | On-call for the first time; most visceral account of 2am escalation experience |

---

## Behavioral Evidence: The "I'll Add It Later" Pattern

The single most consistent behavioral observation across all 10 participants was a pattern of deferred documentation that is structural, not motivational.

**Observed behavior:** When an engineer closes an incident in PagerDuty or OpsGenie, they add a comment variant of "fixed — will document in Confluence" and close the ticket. The documentation does not happen.

This was described, in nearly identical terms, by 8 of 10 participants. Representative quotes:

> "We literally have a rule that you're supposed to add a runbook link before closing. We have no runbooks. The rule has been there for two years."
> — P2

> "I do it too. I close the alert and I think 'I'll write it up tomorrow.' I never do. I'm not lazy, I'm just exhausted and I know the next shift starts in six hours."
> — P7 (self-described hero)

> "I've started adding 'TODO: runbook' to Jira tickets after incidents. There are 47 of those open right now. Nobody goes back to them."
> — P9

> "My manager sends a Slack message every Friday asking who updated Confluence this week. We're all quiet. It's become a joke."
> — P8

**Key distinction from PM interviews:** P5 (the most skeptical participant) framed this precisely: *"It's not that engineers don't care about documentation. It's that documentation has zero payoff at the moment you need to write it, and high payoff later when you can't remember the context. The incentive gradient is backwards."*

This is the structural problem. The intervention has to change *when* documentation happens, not how much engineers are reminded to do it.

---

## Root Cause Hypothesis

**Knowledge debt is created at the moment of resolution.**

The incident close moment has three properties that make it uniquely wrong for traditional documentation workflows and uniquely right for Sentinel's approach:

1. **Cognitive exhaustion is highest.** The engineer just fixed something under pressure, possibly at 2am. The last thing they want is to open Confluence.
2. **Context is highest.** The exact steps taken, commands run, and root cause understood are at peak clarity. Waiting 24 hours degrades this rapidly.
3. **Motivation is at a local minimum.** The crisis is over. The urgency that drove action is gone. There is no social or system pressure remaining.

Traditional documentation workflows assume engineers will return to the documented state after the emotional energy of the incident subsides. They do not. **The right intervention is at incident close, not at a separate documentation session.** The engineering equivalent of a surgical checklist: do it at the moment of action, or it doesn't happen.

This was our primary design hypothesis going in, and it was confirmed by every participant.

---

## Jobs-To-Be-Done

### Primary JTBD

> **"When** I get paged at 2am for an alert I don't recognize, **I want to** find exactly what worked the last time this happened, **so I can** resolve it in under 10 minutes and go back to sleep without having to call anyone."

This statement came from P10 (mid-level IC, first on-call experience) but was validated verbatim by P7, P8, and P9 when read back to them.

### Supporting JTBDs

| # | Job | Who | Context |
|---|-----|-----|---------|
| J2 | When I'm reviewing on-call health in a 1:1, I want to show which engineers are carrying disproportionate load so I can make the case for redistributing it. | Engineering Manager (P1, P3, P6) | Weekly 1:1 with direct reports or skip-levels |
| J3 | When a new engineer joins my on-call rotation, I want them to be able to handle common incidents independently within 30 days so I'm not worried every time they're paged. | Engineering Manager (P2, P4, P5) | Onboarding new on-call participants |
| J4 | When I get paged for the same alert I fixed last month, I want to pull up exactly what I did so I'm not debugging the same thing from scratch again. | Senior IC (P7, P9) | Repeat alert scenario |
| J5 | When I need to escalate, I want to know which specific person to call — not send a message to the whole team Slack channel — so I can get an answer in 2 minutes instead of 15. | All ICs (P7–P10) | Escalation under time pressure |

---

## Pain Points Table

| # | Pain | Behavioral Evidence | Frequency | Intensity (1–5) | Supporting Participants |
|---|------|---------------------|-----------|-----------------|------------------------|
| P-1 | **No runbook available for active incident.** Engineer pages hero or spends 20–40 min in Slack history digging for prior fix. | P8 described searching #infra-incidents Slack channel back 8 months during a 3am page. P10 called senior engineer at 2:30am for a Redis timeout that had a known fix. | 8/10 participants report this as weekly occurrence | 5 — directly extends MTTR and triggers escalation | P7, P8, P9, P10; managers P1, P3, P6 confirm from above |
| P-2 | **Documentation exists but is wrong or outdated.** Engineer follows runbook, it fails, now they've lost 15 minutes and eroded confidence in the documentation system. | P2 showed Confluence runbook for Postgres failover last updated 14 months ago — three infra changes ago. P4 said team stopped trusting the wiki after two incidents where following it made things worse. | 5/10 participants; affects teams with any documentation | 4 — worse than no runbook in some ways (false confidence) | P2, P4, P9; manager P6 |
| P-3 | **Escalation path is unclear.** On-call engineer doesn't know who to contact without broadcasting to Slack, which creates noise for the whole team. | P10: "I send a message to #engineering-oncall and wait. Usually 3 people respond but I don't know who actually knows the answer." Average observed escalation time in P4's PagerDuty data: 18 minutes. | 9/10 participants describe unclear escalation as a common blocker | 4 — extends MTTR, creates guilt around "bothering" people | P7, P8, P9, P10 unanimously |
| P-4 | **Hero burnout is visible but not measurable.** Managers know it's happening but can't show the data to justify headcount or rotation changes. | P1, P3, P6 all used the phrase "I know who it is, but I can't prove it" when describing hero dependency. P3 tried to get headcount approved for on-call relief but couldn't quantify the problem to finance. | 6/10 managers experience this; less visible to ICs | 4 — limits manager's ability to take corrective action | P1, P3, P5, P6 |
| P-5 | **Repeat incidents solved from scratch.** Same alert fires monthly; each time the on-call engineer investigates as if new. | P7 described fixing the same Kafka consumer lag alert "at least six times in the past year. I've written the fix in my personal notes. Nobody else has it." P4 pulled data showing 23% of alerts were exact repeats. | 7/10 participants describe this for at least 1 known alert type | 5 — pure waste; most actionable problem for Sentinel to solve | P7, P9 (IC experience); P4 (data confirmation) |

---

## Assumption Validation Results

| # | Assumption | Pre-Discovery Confidence | Finding | Post-Discovery Verdict |
|---|---|---|---|---|
| 1 | Engineers will write runbooks when prompted at incident close | Low | 7/10 participants said they would complete a short (3–5 field) structured form at close if it took less than 90 seconds. Resistance was to *length and blank text fields*, not to documentation itself. P5 said: "Give me checkboxes and a 'what commands did you run' field — I'll fill that in. Don't give me a Confluence page." | **PASS — with design constraint: form must be structured and take <90 seconds** |
| 2 | Alert patterns are stable enough to build routing on | Medium | P4 provided a PagerDuty export: 68% of alerts in the past 6 months were repeats of a type seen at least 3x before. P1 and P3 confirmed anecdotally. One counterpoint: P6 said new microservices deployments create new alert types every quarter — routing needs graceful fallback. | **PASS — with caveat: graceful fallback to standard rotation required** |
| 3 | Managers want visibility into hero dependency | Medium | 5/6 managers said they would share a Hero Dependency Index in quarterly reviews if it existed. P3 said: "I've been trying to make this argument for 6 months. If Sentinel can give me the number, I can have the headcount conversation." P5 was the outlier — concerned engineers would feel surveilled. | **PASS — with design constraint: frame as team health metric, not individual performance; manager-only access** |
| 4 | The primary cause of slow MTTR is missing runbooks, not alert volume | Medium | Strong confirmation. 9/10 participants ranked "couldn't find resolution steps / had to escalate" as a larger MTTR driver than "too many alerts." P4 estimated 60% of their MTTR came from escalation and investigation, vs. ~15% from alert noise. | **PASS — core frame confirmed. Alert volume is real but secondary.** |

**All four assumptions passed. Go/no-go gate: CLEARED.**

---

## Key Design Constraints from Research

These are non-negotiable UX requirements derived directly from participant evidence:

1. **Runbook capture form must be structured, not a blank text field.** Blank fields produce blank submissions or abandonment. Use guided fields: "What triggered this?" / "What commands did you run?" / "What was the root cause?" / "What should the next engineer check first?"

2. **Capture form must complete in under 90 seconds.** The 90-second threshold came up independently from P5, P7, and P9. Exceeding it will cause engineers to route around the form.

3. **Routing must have transparent fallback.** Engineers need to know *why* they were routed to a specific incident. "You're receiving this because you resolved 3 similar incidents" is acceptable. Silent routing that feels arbitrary will erode trust.

4. **Hero Dependency Index must be opt-in and manager-only.** P5's concern about individual surveillance was a minority position, but it was principled. The dashboard must not show individual engineer names to other ICs — only aggregate team health to managers.

5. **Runbook quality degrades rapidly.** P2's Confluence data showed runbooks older than 6 months had a 40% "follow-and-fail" rate. The system needs a staleness signal — "last validated: N months ago" — to warn engineers before they trust outdated steps.

---

## Synthesis: What Sentinel Must Solve First

Based on the pain points table, behavioral evidence, and JTBD mapping, the following hierarchy guides v1 prioritization:

**Problem 1 (P-5 + P-1):** Repeat incidents solved from scratch / no runbook available — this is the highest-intensity, highest-frequency pain. Runbook capture and retrieval at page time directly addresses this.

**Problem 2 (P-3):** Unclear escalation path — intelligent routing addresses this by surfacing *who to call* before the engineer has to broadcast to Slack.

**Problem 3 (P-4):** Hero burnout not measurable — Hero Dependency Index gives managers the metric they've been missing.

Problems P-2 (wrong runbooks) and the full rotation fairness problem are valid but secondary. P-2 is partially addressed by surfacing runbook age; rotation fairness is deferred to v2.

---

## What We Are Not Solving in v1

Confirmed out-of-scope based on research:

- **Alert deduplication / noise reduction.** Participants raised alert volume as a real problem but ranked it secondary to knowledge gaps. Two participants (P2, P4) already use PagerDuty's noise reduction features. This is not Sentinel's job.
- **Rotation scheduling fairness.** Raised by 4/10 participants but always as a "also this" rather than the primary driver. Fairness scheduling requires calendar integration and is a separate product problem.
- **Slack bot interface.** P7 and P8 mentioned this as a "would be nice" but not a must-have. Core mechanic should be validated in the PagerDuty/OpsGenie interface before adding Slack complexity.
- **Postmortem automation.** Raised by P4 and P6. Interesting future direction but a different use case from in-incident resolution. Would dilute focus.

---

## Recommended Next Step

Proceed to Opportunity Solution Tree. Use the following as inputs:

- **North star outcome:** Reduce Hero Dependency Index from 65% to <30%
- **Primary JTBD:** Find what worked last time at 2am, without calling anyone
- **Top 2 opportunities for v1:** Knowledge concentration (can't resolve without the hero) and undocumented procedures (solved same thing from scratch again)
- **Critical design constraint:** Capture must be <90 seconds, structured, at incident close
- **Go/no-go:** All 4 assumptions cleared. Proceed to OST and PRD.
