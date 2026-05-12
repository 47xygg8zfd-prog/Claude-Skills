# Sentinel — CPO Strategic Framing
**Stage 1 of 20: Strategy**
**Date:** 2026-05-12
**Author:** CPO
**Status:** Approved — P1 this quarter

---

## Executive Summary

On-call burnout is the third most-cited reason engineers leave in exit interviews, behind compensation and growth trajectory. No product in the current market owns this problem end-to-end. PagerDuty owns alerting infrastructure. Confluence and Notion own documentation. Nothing bridges the two, and nothing makes institutional knowledge accessible at 2am when the engineer who wrote the original fix is asleep in a different timezone.

Sentinel is our bet on closing that gap. It is not an alerting product. It is not a documentation product. It is a **knowledge routing product** — moving the right resolution knowledge to the right engineer at the right moment.

This document establishes the strategic framing, investment rationale, and go/no-go conditions for the Sentinel initiative.

---

## Strategic Context

### Company OKR Alignment

**Company Objective**: Make our DevOps toolchain the platform of record for engineering teams at B2B SaaS companies.

| KR | Sentinel Contribution |
|---|---|
| KR1: Increase platform stickiness — raise 6-month retention from 61% to 75% | Sentinel adds a persistent data layer (runbooks, routing history) that is painful to migrate away from. High switching cost = high retention. |
| KR2: Expand to 3 new integrations adopted per customer by end of Q3 | PagerDuty and OpsGenie integrations give us a wedge into incident management workflows already used by 80%+ of target customers. |
| KR3: Reduce engineering-team churn in post-sale segments by 15% | Burnout reduction directly reduces churn. CS sees "on-call workload" in 40% of at-risk account notes. |

**Division Objective**: Retain engineering users by solving problems that happen at 2am, not just during planning.

- KR: Increase weekly active usage by ICs (not just managers) from 22% to 45%
- KR: Reduce "hero departure" churn events — accounts lost within 90 days of a key engineer leaving — from 18 incidents to <8

### Investment Tier

**P1 — This Quarter.**

Rationale:
1. Exit interview signal is clear and has been cited for 3 consecutive quarters without a mitigation strategy.
2. The competitive window is open — no incumbent owns this space. PagerDuty's new AI features focus on noise reduction, not knowledge transfer. This is a different problem.
3. The integration surface (PagerDuty/OpsGenie webhooks) is well-understood and low-risk to build against. We have existing internal expertise.
4. Two engineers is sufficient for an MVP that tests the core hypothesis. We are not making a large resource bet.

---

## The Opportunity

### Problem Statement

Engineering "heroes" — the 3–4 people who can resolve the hardest incidents — resolve approximately 65% of all incidents at a typical 50–200 engineer B2B SaaS company without a dedicated SRE team. When one hero leaves, MTTR triples within 60 days. The company does not lose alerting capability; it loses resolution knowledge.

This is not primarily an alerting problem. It is a knowledge transfer problem that masquerades as an alert fatigue problem.

### Insight That Changes the Frame

Most on-call tools optimize for *who gets paged* (rotation fairness) or *how many alerts are sent* (noise reduction). Neither addresses the actual cause of burnout: **the same people get called, over and over, because they are the only ones who know how to fix it.**

Alert volume is a symptom. Knowledge concentration is the disease.

If institutional resolution knowledge is captured systematically and made searchable, the pool of engineers who can resolve a given alert type expands. Hero dependency falls. Burnout follows.

### Target Customer

Engineering managers at B2B SaaS companies with:
- 50–200 engineers
- No dedicated SRE team (on-call falls on product engineers)
- PagerDuty or OpsGenie already in use
- Active pain: engineers citing on-call load in 1:1s, flight risk attributed to burnout

These customers have the pain, have the budget authority, and already use the infrastructure we integrate with. They are not startups who will accept rough tooling, and they are not enterprises who need security reviews before any new vendor.

---

## Constraints

| Constraint | Detail |
|---|---|
| **Team size** | 2 engineers (1 senior full-stack, 1 mid-level backend) |
| **Timeline** | 8-week sprint to MVP |
| **Integration requirement** | Must integrate with PagerDuty and OpsGenie via webhooks at launch. No other incident management tools in scope. |
| **Budget** | Standard P1 allocation. No additional headcount until post-MVP signal. |
| **Data privacy** | Runbook content may contain internal infrastructure details — must be stored in customer's own data boundary or with strict access controls. This will gate enterprise deals. |

---

## MVP Scope (Strategic View)

Three capabilities ship together as the MVP. They are interdependent — removing any one degrades the value of the others.

1. **Runbook Capture at Incident Close** — Auto-prompt engineer to document resolution steps before closing the incident. Low-friction structured capture, not a blank text field.

2. **Intelligent Routing** — When a new incident arrives, route to the engineer who last successfully resolved this alert type, not just whoever is on-call next in rotation. Fallback to standard rotation if no match exists.

3. **Hero Dependency Index Dashboard** — Manager-facing view showing what percentage of incidents are resolved by the top 3 engineers on the team. Target: reduce from ~65% baseline to <30%.

**Deferred to v2:** Rotation fairness scheduler, alert deduplication, Slack bot interface, mobile push, SLA tracking.

---

## Go/No-Go Conditions

Discovery must confirm the following before engineering begins:

| Condition | Evidence Required | Status |
|---|---|---|
| Runbook quality (not alert volume) is the primary blocker to MTTR improvement | >60% of interviewees identify "couldn't find resolution steps" or "had to call someone" as the primary delay — not "too many alerts" | Pending discovery |
| Engineers will engage with documentation prompts at incident close | Behavioral evidence that friction at close (not motivation) is the blocker — implying a well-designed prompt changes behavior | Pending discovery |
| Managers are willing to pay for visibility into hero dependency | Manager interviewees identify hero dependency as a reportable concern they'd act on, not just a known background problem | Pending discovery |
| Alert patterns are stable enough for routing | >70% of recurring alert types have resolved at least 3x in the past 6 months in target customer segment | Pending discovery |

**If discovery does not confirm conditions 1 and 2, this initiative does not proceed to build.** Conditions 3 and 4 affect feature prioritization but not go/no-go.

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Engineers route around the prompt (close incident without documenting) | High | High | Frictionless capture design; manager visibility creates accountability |
| PagerDuty changes webhook API mid-build | Low | Medium | Build against stable v2 API; no beta endpoints |
| Customers uncomfortable with runbook data stored outside their infra | Medium | High | Self-hosted option or per-customer encryption in roadmap; table stakes for enterprise |
| Alert patterns are too noisy for routing to be useful | Medium | High | Routing has graceful fallback to standard rotation; routing is a bonus, not a dependency |
| Hero Dependency Index perceived as surveillance | Medium | Medium | Dashboard is manager-only and opt-in; frame as team health, not individual performance |

---

## Decision

**Green light for discovery.** Engineering does not begin until discovery gate is cleared.

Next milestone: Discovery brief and interview synthesis due **2026-05-26**.
