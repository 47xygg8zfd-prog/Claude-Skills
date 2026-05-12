# Sentinel — Devil's Advocate Review
**Document type**: Pre-build assumption challenge  
**Product**: Sentinel — On-Call Intelligence Platform  
**Reviewed by**: [Devil's Advocate / PM Peer Review]  
**Date**: 2026-05-12  
**PRD version**: v1.0  
**Status**: Required reading before engineering kickoff

---

## Purpose

This document challenges the three most load-bearing assumptions in the Sentinel PRD. The goal is not to kill the product — it is to stress-test the reasoning before we spend engineering capital on the wrong thing. Each assumption is argued against as forcefully as the evidence allows.

If these challenges cannot be answered satisfactorily, the corresponding feature should be de-scoped or redesigned before development begins.

---

## Assumption 1: "Engineers will write runbooks when prompted at incident close"

### The Assumption (as stated in the PRD)
When an on-call engineer closes an incident in PagerDuty or OpsGenie, a Sentinel prompt appears asking them to document what they did. This creates a growing library of runbooks that reduce MTTR for future incidents.

### The Challenge

This assumption conflates *willingness* with *presence*. Engineers will be present at incident close — they will not be willing.

Consider the conditions: It is 2:17am. The engineer has been on a call for 45 minutes. They just got a Kubernetes pod back up by restarting a deployment they've restarted twelve times before. They are exhausted, possibly still in a Slack thread, possibly woken from sleep. The close button is right there.

The prompt appears. What do they write?

> "checked logs, restarted service"

That is not a runbook. That is a log entry. It tells the next engineer nothing they didn't already know: something broke, someone restarted something. No root cause. No diagnostic path. No commands. No signals that differentiate *this* restart from the one that didn't work. Useless.

The behavioral economics here are unfavorable. The engineer has just discharged their anxiety (the incident is resolved). The reward for writing a good runbook accrues to someone else, at a future incident, on a different shift. The cost — time, cognitive effort at 2am — is paid right now. Standard present-bias: the prompt gets clicked through.

There is also a quality floor problem. Even motivated engineers, documenting in the moment, will produce inconsistent runbooks. Some will write three paragraphs. Some will write one sentence. Without structure, the runbook corpus becomes a search problem: you have a library where 80% of the books are too vague to act on, and you cannot easily tell which are which until a human reads them.

Runbook *quantity* will grow. Runbook *quality* — the variable that actually drives MTTR reduction — will not.

### What to Do Instead

Do not ask engineers to write. Ask them to confirm.

Sentinel has access to the incident timeline: acknowledgement timestamp, resolution timestamp, all Slack messages in the incident thread (via integration), all PagerDuty activity log entries. From these signals, the system can draft a structured runbook automatically:

- **Alert type**: from PagerDuty alert metadata
- **Duration**: computed
- **Services touched**: from GitHub deployment events and PagerDuty service tags
- **Likely resolution action**: inferred from Slack thread keywords and PagerDuty status changes
- **Commands run**: if engineers are in a shared terminal session (optional tmux/SSH log integration), capture directly

The engineer's job at close is not to *write* — it is to review a pre-filled form, correct what's wrong, and approve. Three fields, two minutes. This is cognitively achievable at 2am. Authoring from scratch is not.

Secondary option: delay the prompt. Rather than requiring documentation at close, send the engineer a Slack message 4 hours later (or at 9am the next morning) with the auto-generated draft: "Here's what we captured from last night's incident — does this look right?" Asynchronous confirmation is far more likely to produce quality documentation than synchronous authoring under duress.

### Impact If Wrong

Runbook coverage rate (count) increases as a vanity metric. The MTTR improvement does not materialize. Engineers at subsequent incidents see runbooks like "checked logs, restarted service" and stop opening them — they learn quickly that runbooks are noise, not signal.

HDI does not improve. The same heroes still get called because routing alone, without quality runbooks, does not help a non-hero engineer close an incident faster.

The product ships, the metrics look soft, and the team spends Q2 debugging why runbook coverage is 70% but MTTR is flat. The root cause — a bad assumption about human behavior under stress — takes six months to surface.

---

## Assumption 2: "Alert patterns are stable enough to build ML routing on"

### The Assumption (as stated in the PRD)
Sentinel routes incoming alerts to the engineer who most recently and most successfully resolved that alert type. The routing uses pgvector similarity on alert metadata and historical resolution records.

### The Challenge

This assumes that "alert type X resolved by Engineer A" is a persistent, transferable signal. In a fast-moving SaaS startup deploying multiple times per day, it is not.

Alert patterns at growing B2B SaaS companies are not stable. They are volatile. Here is why:

**The deployment churn problem**: A team shipping 5–10 deploys per day will introduce new alert triggers every week. The `high_memory_usage` alert on the payments service today fires for a different reason than it did three weeks ago — because the payments service was refactored. The engineer who resolved it three weeks ago resolved a different problem with the same label.

**The system change problem**: Infrastructure migrations — moving from EC2 to Fargate, Postgres to Aurora, monolith to microservices — invalidate *all* historical routing signals simultaneously. The day after a major migration, Sentinel's routing model is working entirely from stale data about a system that no longer exists.

**The label inflation problem**: Alert names in most small engineering orgs are maintained poorly. Teams copy-paste alert configs. "High CPU" fires across fifteen different services with fifteen different causes and fifteen different expert engineers. Routing on label similarity alone collapses them into one bucket and systematically misdirects.

**The cold start problem**: A new engineer joins the team. They have no historical resolution records. Sentinel never routes to them. They never build resolution history. They never become the "expert" on anything. HDI improves on paper (one more person shares load), but new engineers are perpetually undertrained on the real system behavior.

The deeper issue: similarity on alert *metadata* is not the same as similarity on alert *cause*. Two alerts can have identical names and different root causes. Two alerts can have different names and identical root causes. Routing based on name similarity is a proxy for a proxy.

### What to Do Instead

Routing needs a relevance decay signal that is time-weighted and deployment-aware.

Specifically:

1. **Recency weighting**: A resolution event older than 30 days (configurable per team) should have its routing weight halved. Older than 90 days: near-zero weight. This forces the model to favor recent expertise over historical expertise.

2. **Deployment invalidation signal**: When Sentinel detects a GitHub deployment event to the service associated with the alert, it marks that service's routing history as "pending revalidation." The next resolution for that alert type becomes the new anchor point. This prevents routing on stale context post-deploy.

3. **Override tracking**: Track `routing_override` events — when a suggested routee reassigns the alert to someone else. A high override rate for a specific alert type is a signal that routing is wrong. Surface this in the dashboard: "Routing confidence: Low (42% override rate in last 30 days)."

4. **Fallback to on-call schedule**: When routing confidence is low (no recent resolutions, high override rate, recent deployment), fall back to the scheduled on-call engineer rather than the historical expert. Do not route to someone off-rotation just because they last resolved this alert — that creates its own burnout.

The product can still use pgvector for runbook similarity. The routing layer needs explicit recency logic that the ML similarity model alone does not provide.

### Impact If Wrong

Sentinel routes to the wrong engineers. Alert acknowledgement time increases because the routed engineer is not the right person and either reassigns or fumbles. MTTR increases instead of decreases.

The on-call satisfaction guardrail trips: engineers start receiving alerts outside their scheduled rotation because the system thinks they are experts on alerts they resolved once six months ago on a codebase that no longer exists.

Churn in the product: engineering managers look at the routing recommendations, see them miscalibrated, and disable the feature. Sentinel becomes a passive dashboard rather than an active intervention tool.

---

## Assumption 3: "Hero Dependency Index (HDI) is the right north star metric"

### The Assumption (as stated in the PRD)
HDI measures what percentage of incidents are resolved by a small subset of engineers (the "heroes"). Reducing HDI from 64% to 30% is the north star goal, indicating more distributed incident response.

### The Challenge

HDI measures structural concentration. It does not measure suffering.

The core problem: a team can reduce HDI without reducing burnout. In fact, the most direct path to HDI improvement is to make the hero *less available*, not to make non-heroes more capable.

Consider these two HDI improvement strategies:

**Strategy A (correct)**: Train non-hero engineers through runbooks and shadowing so they can resolve incidents that previously required the hero. Hero resolves 40% fewer incidents. HDI drops from 64% to 32%. Non-hero engineers are more capable. MTTR may increase slightly in the short term as non-heroes ramp, but decreases long-term.

**Strategy B (gaming)**: Force rotation — explicitly take the hero off on-call schedule for two weeks. Incidents that would have gone to the hero now go to non-heroes. HDI drops from 64% to 32%. Non-hero engineers are no more capable than before. MTTR increases significantly. The hero returns and is now deluged with backlogged incidents.

HDI cannot distinguish between these strategies. Both produce the same metric improvement. One actually helps. One is harmful.

There is a second, more subtle gaming vector: an engineering manager who wants to hit the HDI target could simply reassign incidents *after resolution* to distribute the credit. The routing log shows more engineers, but the same person did the work. Sentinel has no way to detect this without correlation between routing events and actual resolution activity.

HDI also has a structural blind spot around on-call *availability*, not just resolution. An engineer who is on-call but never gets paged is not a hero dependency problem — they are a well-designed system. An engineer who is on-call and gets paged 3x per week for 4 weeks straight is burning out, regardless of whether other engineers also get paged sometimes. HDI averages across the team; individual suffering is invisible in the average.

### What to Do Instead

HDI should remain as a **structural health metric** — it tells you whether the team's incident resolution is dangerously concentrated. It should not be the north star.

The north star should be **MTTR** (mean time to resolution), because it measures whether the system is getting *better at resolving incidents*, which is the actual job. If MTTR is falling and HDI is flat, Sentinel is still working — heroes are becoming faster, or better-documented systems are helping heroes resolve faster. That is a valid outcome.

Add two companion metrics to catch the gaming and suffering signals that HDI misses:

1. **Resolution variance by engineer** (per 30-day rolling window): The standard deviation of incidents-resolved per on-call engineer. A healthy team has low variance. A team gaming HDI with forced rotation may have declining HDI but *increasing* variance as the hero accumulates catch-up incidents outside their rotation window.

2. **On-call load score** (per engineer per week): Incidents × average MTTR × time-of-day penalty (2x weight for off-hours incidents). This is the individual suffering signal. An engineer whose load score exceeds 2 standard deviations above the team median for two consecutive weeks should trigger an alert to their manager.

HDI is a useful diagnostic. It should not be the thing the team optimizes for directly.

---

## PRD Responses Table

| Assumption | Challenge strength | PRD must answer | Blocks shipping? |
|---|---|---|---|
| Engineers write quality runbooks at close | High — strong behavioral economics case against | How does Sentinel ensure runbook quality, not just coverage? What is the minimum viable runbook format? | Yes — needs redesign before build |
| Alert patterns stable enough for ML routing | Medium-High — deployment churn is real; cold start is real | How does routing handle post-deployment signal decay? What is the fallback when confidence is low? | Partial — routing v1 can ship with manual override, but confidence decay must be on the roadmap before v2 |
| HDI is the right north star | Medium — gamability argument is strong; MTTR argument is stronger | Why is HDI north star rather than MTTR? What prevents gaming? | No — HDI can stay as a secondary metric; MTTR elevation to north star recommended, not blocking |

---

## One Thing This PRD Gets Right

The guardrail.

Explicitly requiring that on-call engineer satisfaction score must not decrease is the most honest and self-aware constraint in this document. Most products that claim to reduce burnout have no mechanism to detect if they are making it worse. Sentinel's PRD bakes in a protection metric that directly measures the human experience it claims to improve.

If the team ships, measures that guardrail honestly, and kills or pivots features that violate it, Sentinel will not do harm — even if the MTTR and HDI improvements underperform. That is a meaningful commitment, and the rest of the product should be held to the same standard of honesty.
