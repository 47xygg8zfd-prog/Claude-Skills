# Sentinel — Devil's Advocate Review
**Date:** 2026-05-12  
**Reviewer role:** Internal red-team / product critic  
**PRD under review:** Sentinel MVP PRD (v1.0)  
**Purpose:** Surface the three most dangerous assumptions before engineering begins. These are not nitpicks — each one is capable of sinking the product.

---

## How to read this document

Each section names the assumption as it appears in the PRD, presents the strongest possible case against it, proposes a concrete alternative, and estimates the downstream impact if we ship and the assumption turns out to be wrong. A required-responses table closes the document and forces the PRD author to reply in writing before the design phase begins.

---

## Assumption 1: "Engineers will write runbooks when prompted at incident close"

### What the PRD says
The runbook capture prompt appears at incident close. The engineer fills in the resolution steps. Over time, a corpus of high-quality runbooks accumulates, and subsequent responders can resolve the same alert type faster by following documented steps.

### The challenge

This assumption treats a human at 2am, after a 45-minute page-out, as a willing and capable knowledge worker. That is not who is at the keyboard.

Consider the actual sequence of events: the engineer acknowledges the page, investigates, applies a fix, confirms the service is healthy, and wants to go back to sleep. At that moment, a modal appears asking them to document what they did. The path of least resistance is to type something — anything — that makes the modal go away. The result is not a runbook. It is a legal minimum:

> "checked logs, restarted the auth service"

That string passes any completeness check that does not involve a human reading it. It tells the next responder nothing they did not already know. No root cause. No diagnostic path. No commands. No signals that differentiate this restart from the one that did not work.

The failure mode is not that engineers refuse to comply. It is that they comply in a way that produces zero signal. Runbook coverage (the quantity metric) will look great in the dashboard. Runbook utility — the quality metric that actually reduces MTTR — will be near zero. The team will spend a sprint wiring up a sophisticated pgvector similarity search over a corpus of useless one-liners, and the MTTR needle will not move.

There is also a secondary failure mode: the engineers who care — the ones who would actually write a useful runbook — are disproportionately the heroes the HDI dashboard is already flagging. Prompting them for documentation adds one more obligation to the people we are supposed to be protecting.

The behavioral economics are unfavorable in a structural way. The reward for writing a good runbook accrues to someone else, at a future incident, on a different shift. The cost — time, cognitive effort at 2am — is paid right now. Present-bias makes this a losing proposition for quality output.

### What to do instead

Do not ask the engineer to write. Capture what they did automatically, then ask them to review.

During the incident, structured signals are already being produced: Slack messages sent in the incident channel, GitHub commits or deploys in the 30-minute window before the alert, PagerDuty activity log entries, and — if the engineer uses a shell integration — terminal commands run during the incident window. Synthesize these into a draft runbook with a title, a probable root cause section, and a "steps taken" section populated from those signals.

Present the engineer with: "Here is what we recorded. Does this look right? Add anything we missed." That is a 90-second review task, not a 10-minute writing task. The quality ceiling is higher because the draft is machine-generated from real actions, not recalled from memory under fatigue. The cognitive load is lower because editing is easier than composing from scratch.

This requires Slack channel access and GitHub integration — the former is already in planned scope. A delayed-send option (Slack message 4 hours after incident close, or at 9am the following morning with the auto-generated draft) removes the 2am timing problem entirely without requiring any additional engineering.

### Impact if wrong

Runbook coverage rate reaches 80%+ within 60 days. The metric looks excellent in the dashboard. The experiment runs and shows no MTTR improvement. Engineers start ignoring the runbook panel because it has never helped them. The routing system routes future incidents to engineers who have "resolved this alert type before" but gives them a useless runbook as context. Hero dependency persists because the heroes are still the only ones who actually know what to do — they just now have a log of the one-liners they filed.

**Risk level: High. This is the most dangerous assumption in the PRD.**

---

## Assumption 2: "Alert patterns are stable enough to build ML routing on"

### What the PRD says
The routing engine uses pgvector similarity search on historical incident data to identify which engineer last resolved an alert of this type and routes the new incident to that engineer. The assumption is that "alert type" is a meaningful, stable category across time.

### The challenge

At a 100-engineer B2B SaaS company with continuous deployment, "last week's alert" and "this week's alert" can share a name but have completely different root causes, resolution paths, and required expertise.

Concrete example: an `api-latency-p99` alert fires. Six weeks ago, the last time it fired, the root cause was a misconfigured database index introduced in a specific PR. The engineer who resolved it (call her Alex) did so by reverting that PR. Alex is now flagged by the routing system as the expert for `api-latency-p99` incidents. This week, the same alert fires. The root cause is a new caching layer introduced three weeks ago. Alex has never touched the caching layer. The routing system sends her the page anyway, because the alert type string matches. Alex takes 20 minutes to figure out she is in the wrong part of the codebase before she escalates or reassigns. MTTR increases.

The broader structural problem is that routing systems trained on historical patterns assume the system being monitored is stationary. Fast-growing companies violate this assumption constantly. Every significant architectural change, every new service, every major dependency upgrade makes prior routing signals partially or fully stale. A model that does not know a major refactor happened last Tuesday will confidently route based on patterns that no longer reflect reality.

There is also a feedback loop risk: if the routing system consistently sends alerts to the same engineers because they resolved those alert types historically, those engineers continue to resolve them because they have no choice, which reinforces their "expertise" score, which means the routing system continues to send them those alerts. This is a mechanism for locking in hero dependency, not breaking it.

### What to do instead

Pair the similarity signal with two explicit decay mechanisms.

First, a **recency decay**: weight prior resolutions by how recently they occurred. A resolution from 6 weeks ago should count for significantly less than one from last week. A resolution from 90+ days ago should contribute near-zero routing weight. This is standard in recommendation systems and is not complex to implement.

Second, a **deployment-triggered invalidation**: when a major deployment is detected via the GitHub webhook integration (already in planned scope), flag alert types historically correlated with that service as "stale." For those alert types, reduce routing confidence and surface a visible warning in the UI rather than silently routing to a potentially wrong engineer.

Third, capture routing overrides explicitly. When an engineer reassigns away from the suggested responder, that is a direct signal that the routing was wrong. Feed those override signals back into the model and surface a "routing confidence" indicator in the dashboard. A low-confidence route should be presented as a suggestion, not an assignment.

None of this requires abandoning the routing feature. It requires building it with appropriate epistemic humility about the quality of its own signal.

### Impact if wrong

The routing feature ships. In the first 30 days, on teams that have been relatively stable, it performs reasonably — alert types that have not changed route correctly and MTTR improves. The feature is declared a success. Six months later, the teams that have grown fastest and deployed most aggressively see MTTR plateau or increase. Engineers report frustration with incorrect routing. The feedback is attributed to "adoption issues" rather than model staleness. The core assumption was wrong and the product is now trusted with routing decisions it is not equipped to make.

**Risk level: Medium-High. Likely to work on the initial cohort; likely to degrade silently on the most important long-term customers.**

---

## Assumption 3: "Hero Dependency Index (HDI) is the right north star metric"

### What the PRD says
HDI measures the percentage of incidents resolved by the top 20% of resolvers. Baseline is 64%. Target is 30%. Reducing HDI means knowledge and on-call load is spreading more evenly across the team, reducing burnout risk for heroes and building organizational resilience.

### The challenge

HDI measures concentration of incident resolution. It does not measure whether incidents are being resolved well, whether the people now resolving them are burning out, or whether the distribution is happening for the right reasons.

Consider the simplest path to improving HDI: mandate rotation. Force every engineer to take equal on-call shifts regardless of their familiarity with the systems that alert most frequently. The engineer who was previously resolving 40% of incidents now resolves 12%. HDI improves dramatically. But the engineer who now resolves those incidents takes twice as long per incident, produces low-quality runbooks because she does not know the system, and accumulates growing anxiety about pages she cannot handle. Burnout has been redistributed, not reduced.

This is not hypothetical. Engineering managers under pressure to hit a metric find the path of least resistance. If the metric is HDI and the lever is rotation scheduling, that lever will be pulled. We will have built a product that makes dashboards look good while making the underlying problem worse.

The deeper issue is that HDI is a structural metric — it tells you something about the shape of the load distribution. It says nothing about the subjective experience of carrying that load. An engineer who resolves 8% of incidents but every single one is a 3am page involving a nightmare legacy service she does not understand may be more burned out than the hero who resolves 35% of incidents because she genuinely enjoys the work and does it efficiently.

HDI also has a measurement blind spot: it requires knowing who was on rotation, not just who resolved the incident. An engineer who is on the rotation and never gets paged should still count as a "participating resolver" for HDI purposes — their presence reduces the dependency even if they are not called. Measuring only actual resolutions overstates dependency for well-designed systems. (This also has instrumentation implications — see File 10.)

### What to do instead

Retain HDI as a structural health indicator — it is genuinely useful for that purpose. But elevate MTTR to the primary north star, because MTTR measures whether the system is getting better at resolving incidents, which is the actual job Sentinel is hired to do.

Add a companion metric: **MTTR variance by engineer cohort** (rolling 30-day window). This measures whether the engineers who are now resolving incidents as HDI improves are doing so at comparable speed and quality to the previous heroes. If HDI improves and MTTR variance stays low, the knowledge transfer is working. If HDI improves but MTTR variance increases, the distribution is happening without knowledge transfer — the load has been spread but the capability has not.

Consider the quadrants this creates:

| | HDI Low (concentrated) | HDI High (distributed) |
|---|---|---|
| **Satisfaction High** | Heroes are coping, but structure is fragile | Target state |
| **Satisfaction Low** | Classic burnout — Sentinel's primary ICP | Load distributed but nobody is happy; rotation gaming likely |

A single metric (HDI) cannot distinguish between the top-right and bottom-right quadrants. Two metrics (HDI + satisfaction) can. The on-call satisfaction guardrail already in the PRD is doing exactly this work — it should be elevated from a guardrail to a co-primary dashboard metric.

### Impact if wrong

Customers hit their HDI targets at 6 months. Churn begins at 12 months when they realize their on-call satisfaction scores have not improved — or have declined — and senior engineers are citing on-call burden in exit interviews. The product was optimizing for the wrong thing. This damage is slow-moving, which is the worst kind: it will not show up in the 90-day retention metric, only in the 18-month cohort.

**Risk level: Medium. HDI is not a bad metric — it is an incomplete one. The risk is in treating it as sufficient.**

---

## Required PRD Responses

The PRD author must respond to each item in writing before design begins. Unanswered items block the design kickoff.

| # | Assumption challenged | Specific question | Blocks design kickoff? |
|---|---|---|---|
| 1a | Runbook quality at 2am | How will we measure runbook *quality*, not just coverage? What is the minimum acceptable format for a runbook to be counted as valid in the MTTR analysis? | Yes |
| 1b | Capture adds load to heroes | How do we ensure the capture step does not increase on-call burden score for the engineers already flagged as heroes? What is the fallback if satisfaction scores decline after runbook capture is enabled? | Yes |
| 1c | Auto-capture is not in MVP scope | Is auto-draft from Slack/GitHub signals a V1.1 commitment or genuinely out of scope? If out of scope, how is runbook quality risk communicated to stakeholders? | No — needs roadmap entry |
| 2a | Alert patterns go stale post-deploy | Will the MVP routing engine include recency decay, or is it pure historical similarity? If no decay, what is the commitment timeline for adding it? | Partial — routing can ship with override tracking, but decay must be on the V1.1 roadmap |
| 2b | Routing feedback loop reinforces heroes | How are routing overrides captured and fed back into the model? Is `routing_override` event instrumentation in MVP scope? | Yes |
| 2c | Routing confidence is not surfaced | Will engineers see a confidence indicator, or just a suggested assignee? How do they know when to trust the system? | No — UX decision, but must be resolved before launch |
| 3a | HDI gameable via forced rotation | What companion metric tracks whether new resolvers are actually more capable, not just more numerous? | No — recommend MTTR variance addition |
| 3b | HDI measures structure, not suffering | When does on-call satisfaction score move from a guardrail to a co-primary dashboard metric? | No — recommend before public launch |
| 3c | HDI requires rotation schedule data | Does Sentinel have access to PagerDuty rotation schedules, not just resolution records? If not, HDI is unmeasurable as specified. (See also File 10.) | Yes — instrumentation dependency |

---

## One thing this PRD gets right

The guardrail on on-call engineer satisfaction score is the right call, and the PRD team deserves credit for including it. Most product teams building operational tooling optimize purely for business metrics — MTTR, incident volume, coverage rate — and treat the engineers as inputs to those numbers. The explicit commitment that satisfaction must not decrease, and that this functions as a kill switch rather than a nice-to-have, shows that the team understands who the actual customer is.

If that guardrail holds through execution — if it is measured honestly and acted on when it trips — it will prevent the worst-case outcomes described in Assumptions 1 and 3 above. The risk is that it gets quietly deprioritized when it creates tension with launch timelines. Keep it visible, keep it binding, and make sure it is instrumented before the experiment runs, not after.
