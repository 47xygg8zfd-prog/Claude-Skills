# Sentinel — PM Discovery Brief
**Stage 2 of 20: Discovery**
**Date:** 2026-05-12
**Author:** PM
**Status:** Active — interviews scheduled

---

## Problem Framing

### Problem Statement (Customer Language)

"Our on-call rotation is supposed to distribute the load, but in practice the same three people fix everything. Everyone else is technically on-call but effectively useless for anything hard. When one of those three people quit, we were in crisis mode for two months."

— Engineering Manager, Series B SaaS company, 110 engineers

### Structured Problem Statement

**Who:** Engineering managers at B2B SaaS companies (50–200 engineers) running on-call programs without a dedicated SRE team.

**What:** A small group of engineers ("heroes") resolves the majority of incidents because resolution knowledge lives in their heads, not in systems. When a hero leaves or burns out, MTTR spikes and remaining engineers face unsustainable load.

**When:** The problem is chronic (builds over months) but becomes acute when a hero churns or is unavailable.

**Why it matters now:** On-call burnout is the third most-cited reason engineers leave. The typical knowledge gap takes 60–90 days to manifest after a hero departs — just long enough that managers don't see it coming.

**Current workarounds:** Managers try runbook wikis in Confluence (abandoned after 3 months), Slack channels named #on-call-help (becomes ask-the-hero again), or PagerDuty escalation policies that route everything to the same senior engineers anyway.

---

## Opportunity Hypothesis

**If** we auto-capture runbooks at the moment of incident close (when the fix is freshest and the engineer is already in context),  
**then** any on-call engineer can resolve known incidents without needing to escalate to a hero,  
**because** the institutional knowledge that lived only in the hero's head becomes searchable and retrievable by whoever is paged next.

### Why "at incident close" specifically

This is the critical design decision. There are three candidate moments to capture knowledge:
1. During the incident (too much cognitive load)
2. After the incident, at a separate documentation session (doesn't happen — deferred indefinitely)
3. At incident close, before the engineer can mark it resolved (friction is lowest, context is highest)

Hypothesis: Option 3 is the minimum-viable friction point that actually produces documentation. This needs behavioral validation in interviews.

---

## Assumption Map

| # | Assumption | Why it matters | Confidence (pre-discovery) | How to test |
|---|---|---|---|---|
| 1 | Engineers will write runbooks when prompted at incident close | If false, core capture mechanic fails — we have no data | Low — we have counter-evidence (Confluence wikis fail) | Behavioral interview + show prototype prompt, observe reaction |
| 2 | Alert patterns are stable enough to build routing on | If false, routing sends engineers to wrong incidents — trust erodes | Medium — large customers likely have recurring alert types | Pull sample PagerDuty data from design partner; analyze alert repeat rate |
| 3 | Managers want visibility into hero dependency, not just individual fixes | If false, the dashboard has no buyer — managers may not surface this upward | Medium — exit interview data suggests managers know but don't measure | Ask managers directly: "If you had this metric, what would you do with it?" |
| 4 | The primary cause of slow MTTR is missing runbooks, not alert noise | If false, our whole frame is wrong — we should be building noise reduction | Medium — exit interview qualitative data supports this, but not structured | Quantitative: ask managers to estimate time lost to "finding who to ask" vs. "too many alerts" |

**Assumptions 1 and 4 are go/no-go gating assumptions.** If either fails, the initiative requires re-framing before continuing.

---

## Scope Decisions (Pre-Discovery)

### In Scope for MVP

| Feature | Rationale |
|---|---|
| Runbook capture at incident close | Core mechanic — if this doesn't work, nothing else matters |
| Intelligent routing (last resolver → first contact) | Reduces MTTR by getting the right engineer faster; builds on captured data |
| Hero Dependency Index dashboard | Creates manager-level accountability and gives Sentinel a visible, trackable north-star metric |

### Explicitly Deferred to v2

| Feature | Reason for Deferral |
|---|---|
| Rotation fairness scheduler | Valuable, but orthogonal to knowledge problem — solves fairness, not MTTR |
| Alert deduplication / noise reduction | Different problem (volume) than what we're solving (knowledge) |
| Slack bot interface | Nice UX, but adds integration complexity; validate core mechanic first |
| Mobile push / native app | Not on-call engineers' primary request; web-first is sufficient for MVP |
| SLA tracking and reporting | Manager request, but downstream of solving MTTR first |
| Multi-team / org-level rollup | Enterprise feature; premature for 50–200 engineer target segment |

---

## Interview Plan

### Research Questions (Primary)

1. Walk me through the last incident that took longer than it should have. What caused the delay?
2. When a new engineer gets paged for something they haven't seen before, what happens?
3. You have a wiki / runbook doc / Confluence space. When did someone last update it, and why?
4. Who are the 2–3 people on your team who get escalated to most? What happens when they're not available?
5. If you could see one metric about your on-call program every Monday morning, what would it be?
6. At the end of a long incident, what does the engineer do before they close it in PagerDuty?

### Research Questions (Assumption Validation)

7. [Assumption 1] If the incident tool asked you to answer 3 questions before closing, how often would you skip it?
8. [Assumption 2] Do your alerts repeat? Can you name 5 alerts that your team sees more than once a month?
9. [Assumption 3] If you could see that 70% of your incidents were resolved by 2 people, would you share that in your next leadership review?
10. [Assumption 4] If you had to split on-call burnout into "too many alerts" vs. "can't resolve without help", what's the ratio?

### Participant Targets

**Engineering Managers (6):**
- Must manage a team with active on-call rotation
- Company size 50–200 engineers, no dedicated SRE
- Using PagerDuty or OpsGenie
- Bonus: has experienced a hero departure in the last 12 months

**IC Engineers (4):**
- Active on-call participant (paged at least 2x/month)
- Not the team hero — ideally someone who *escalates to* the hero
- Mix of tenures: 1 senior (3+ years), 2 mid-level, 1 newer engineer on-call for first time

### Recruiting Approach

- CS team to identify 8–10 current customers matching profile
- PM personal network for 2–3 non-customer participants (avoids social desirability bias)
- LinkedIn outreach to 5 prospects for cold perspective
- Target: 10 participants total (6 managers + 4 ICs), complete within 10 business days

---

## Competitive Landscape Scan

| Product | What they solve | What they miss | Relevance to Sentinel |
|---|---|---|---|
| PagerDuty | Alert routing, escalation, on-call scheduling | Knowledge capture, runbook quality, hero dependency | Integration partner, not competitor |
| OpsGenie (Atlassian) | Similar to PagerDuty; stronger Jira integration | Same gaps | Integration partner |
| FireHydrant | Incident management workflow, retrospectives | Runbook retrieval at page time; routing intelligence | Closest competitor; targets same segment |
| Incident.io | Incident workflow, Slack-native | Runbooks are manual; no hero dependency analytics | Competitor in workflow space |
| Blameless | SRE platform, SLOs, postmortems | Requires dedicated SRE team to operate | Targets larger segment; not direct |
| Confluence/Notion | Documentation | Zero integration with incident tooling; purely pull | Where runbooks go to die |

**Key competitive gap:** No product automatically captures knowledge at resolution time and makes it retrievable at page time. This is Sentinel's primary white space.

---

## Outputs from Discovery Phase

- [ ] Interview synthesis (6 managers + 4 ICs)
- [ ] Assumption validation report (pass/fail on all 4 assumptions)
- [ ] Jobs-to-be-done statements (primary + supporting)
- [ ] Quantitative signal: estimate of MTTR delta attributable to knowledge gap vs. alert volume
- [ ] Design partner interest: 2+ customers willing to pilot MVP with real data
- [ ] Revised opportunity hypothesis or explicit go/no-go recommendation

**Due:** 2026-05-26
**Next stage:** UX Research Synthesis → Opportunity Solution Tree → PRD
