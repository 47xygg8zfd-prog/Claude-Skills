# Sentinel — Assumption Test Spec
**Date:** 2026-05-12  
**Document type:** Pre-experiment assumption validation  
**Product:** Sentinel — On-Call Intelligence Platform  
**Status:** Approved for execution — no engineering required  
**Owner:** PM  
**Participants:** 2 engineering teams (volunteer)  
**Duration:** 4 weeks (concurrent with pre-period baseline collection)

---

## Purpose

Before running the A/B experiment (File 07), we must kill the assumptions that could invalidate the experiment's results even if the numbers come out positive. This document specifies the three most dangerous assumptions from the experiment design and proposes concrete, low-cost tests to validate or falsify each one.

The guiding principle: spend four weeks and zero engineering cycles answering questions that would otherwise cost four months and full engineering investment to learn.

---

## Top 3 Assumptions from the Experiment Design

| # | Assumption | Source | Risk level |
|---|-----------|--------|-----------|
| 1 | Engineers produce runbooks that are genuinely useful to future responders | Experiment hypothesis, File 07 "Riskiest assumption" | Critical |
| 2 | Future responders actually use runbooks when available | Implicit in the MTTR reduction mechanism | High |
| 3 | Routing to the "last resolver" is accepted by engineers as a credible suggestion, not an annoyance | Experiment guardrail: routing acceptance rate ≥50% | Medium |

---

## Assumption 1: "Runbooks produced at incident close are useful to future responders"

### Why this is the riskiest assumption

The entire MTTR reduction mechanism in Sentinel depends on a future on-call engineer arriving at an incident, finding a runbook from a prior resolver, following it, and resolving the incident faster than they would have otherwise. This chain has two links, and the first link — runbook quality — is the most fragile.

The prompt-based capture model (an engineer types what they did at incident close) is vulnerable to:
- Fatigue-driven minimalism at 2am ("restarted auth service")
- Recall degradation (what exactly did I do 45 minutes ago?)
- Organizational norm collapse (if the first few runbooks are low quality, norms around quality collapse quickly)

A high-quality runbook for our purposes means: a future engineer with no prior knowledge of this alert type could follow the documented steps and resolve the incident at least 20% faster than baseline. That is a high bar. We do not know whether prompt-based capture can meet it. This test finds out.

### Test design: Concierge test

**What it is:** A human-mediated version of the runbook capture feature, run manually by a PM or UX researcher. No engineering required. The researcher acts as the "runbook system" — capturing, structuring, and delivering runbooks by hand.

**Participants:** 2 volunteer engineering teams from the early-access cohort. Both teams must meet experiment eligibility criteria (PagerDuty or OpsGenie, ≥3 on-call engineers, ≥15 incidents/month). Teams are not randomized — this is not an experiment, it is a validity check.

**Protocol (per incident):**

1. When an incident closes on either team, the researcher is notified via PagerDuty webhook (manual webhook configuration, no Sentinel code required).
2. The researcher contacts the resolving engineer within 30 minutes of close via Slack: "Got a minute to walk me through what happened? I'm helping build the runbook library."
3. The researcher conducts a structured 10-minute interview using this script:
   - "What was the first thing you noticed that told you something was wrong?"
   - "What did you check first, and what did you find?"
   - "What was the actual fix? Can you walk me through the commands or actions, in order?"
   - "What do you think the root cause was?"
   - "Is there anything you tried that didn't work? That's important context too."
   - "If this fires again at 2am and you're not on call, what would you want the next engineer to know?"
4. The researcher transcribes the interview into a structured runbook template (see below) within 2 hours.
5. The completed runbook is stored in a shared Notion page, indexed by alert type.

**Runbook template:**

```
## [Alert type] Runbook
**Last updated:** [date]  
**Documented by:** [researcher, based on interview with: engineer name]  
**Incident date:** [date]  

### What this alert means
[1-2 sentences on what system behavior triggers this alert]

### Diagnostic path
1. [First thing to check]
2. [Second thing to check]
3. [How to distinguish root cause A from root cause B]

### Resolution steps
1. [Step 1 — include exact commands where applicable]
2. [Step 2]
3. [Verification: how do you know it worked?]

### Things that did NOT work
- [Failed approach 1, and why it didn't work]

### Escalation path
If not resolved in [X] minutes: escalate to [person/team/channel]

### Root cause notes
[What actually caused this and whether it's likely to recur]
```

6. When the next incident of the same alert type occurs on either team, the researcher sends the runbook to the responding engineer via Slack before they begin investigating: "Hey — this alert type fired [N] days ago. Here's the runbook from that resolution. Might help."
7. The researcher observes the incident from the Slack thread (does the engineer reference the runbook? ask questions about it? ignore it?) and records the actual MTTR.

**Duration:** 4 weeks. Target: capture runbooks for ≥15 distinct incidents, observe ≥8 repeat incidents.

**Researcher time commitment:** Approximately 3–4 hours/week (assuming 3–5 incidents/week across both teams). This is the total cost of the test.

---

### What we are measuring

**Primary measure: MTTR for incidents where a runbook was available vs. baseline**
- For each repeat incident where a runbook was delivered, record MTTR
- Compare to the team's baseline MTTR for the same alert type in the prior 60 days (where available) or to the overall team baseline (47 min)
- We are looking for ≥20% reduction on median, across ≥8 data points

**Secondary measure: Runbook utilization**
- Did the engineer reference the runbook at any point in the incident thread?
- Did the engineer ask any follow-up questions about the runbook content?
- Did the engineer's resolution approach match the documented steps, or did they do something different?
- After the incident: "Did the runbook help? What was missing?"

**Secondary measure: Runbook quality assessment (researcher judgment)**
- After each interview, the researcher rates the captured runbook on a 1–5 quality scale:
  - 5: Another engineer could follow this runbook with no prior knowledge of the system
  - 3: Another engineer would need to do some investigation, but this would save significant time
  - 1: This runbook contains no actionable information for a future responder
- Track quality distribution across all captured runbooks
- Target: Median quality score ≥3.5

---

### Pass / fail thresholds

**Pass (proceed to A/B experiment with runbook capture feature as designed):**
- ≥60% of follow-on incidents where a runbook was delivered show ≥20% MTTR reduction vs. baseline for that alert type
- Median runbook quality score ≥3.5 out of 5
- ≥50% of engineers reference the runbook during the incident (utilization signal)

**Fail threshold 1 — Runbooks are not useful (quality problem):**
- <30% of follow-on incidents show any MTTR reduction
- OR median runbook quality score <2.5
- **Implication:** The runbook capture feature as designed (prompt-based, free-text) cannot produce useful runbooks. Do not build the prompt. Re-scope to auto-capture with human review (structured draft from Slack/GitHub signals).

**Fail threshold 2 — Runbooks are not used (adoption problem):**
- <30% of engineers reference the runbook during the incident
- AND post-incident interviews reveal engineers felt the runbook was not relevant or trustworthy
- **Implication:** The problem is not quality — engineers have low confidence in peer-authored runbooks as a source of truth. Investigate alternative delivery (inline in PagerDuty vs. Slack message vs. dashboard panel) before proceeding.

**Ambiguous result (proceed to A/B with scope adjustment):**
- Runbooks are high quality (score ≥3.5) but utilization is low (<30% referencing)
- **Implication:** Quality is achievable. The delivery mechanism, not the content, is the problem. Run A/B experiment but treat runbook delivery UX as a secondary test variable.

---

## Assumption 2: "Future responders use runbooks when available"

### Why this matters

Even if runbooks are high quality, they are useless if the engineer resolving the next incident does not open them. This is a separate behavioral assumption from quality — an engineer could have access to a perfect runbook and ignore it if:
- They do not know it exists (discoverability problem)
- They do not trust it (credibility problem — "this was written by someone else, I don't know if it applies to my situation")
- They prefer to investigate themselves (autonomy/expertise bias — "I know what I'm doing")
- The incident is time-sensitive enough that reading feels slower than trying (urgency bias)

This assumption is partially tested by the concierge test (Assumption 1, secondary measure: runbook utilization). The data from the concierge test will tell us the utilization rate when the runbook is proactively delivered to the engineer via Slack.

### Lightweight validation within the concierge test

At the end of each follow-on incident where a runbook was available, the researcher conducts a brief 5-minute debrief:

1. "Did you look at the runbook I sent? When in the incident?"
2. "Was it useful? What would have made it more useful?"
3. "If the runbook had been in PagerDuty rather than Slack, would you have found it?"
4. "If the runbook had been shorter — just bullet points, no narrative — would that be better or worse?"

The goal: understand the delivery format and timing that maximizes utilization, so the A/B experiment tests the right UX, not a straw-man version.

**Pass threshold:** ≥50% of engineers reference the runbook during the incident. (Same as Assumption 1 secondary measure — these are deliberately linked.)

**Fail threshold:** <30% reference rate, AND debrief reveals the cause is discoverability or format, not content. **Action:** redesign the runbook delivery UX (notification timing, format, in-product vs. Slack) before the A/B experiment.

---

## Assumption 3: "Routing suggestions are accepted, not ignored or resented"

### Why this matters

The routing feature proposes that Sentinel suggests an engineer to receive the next incident, based on historical resolution patterns. The experiment guardrail requires ≥50% acceptance rate. But we do not know whether engineers experience routing suggestions as helpful or as unwanted micro-management.

Specific risks:
- Engineers with strong on-call autonomy norms may feel routed alerts are a removal of agency
- Engineers who are routed to alerts outside their scheduled on-call shift may feel Sentinel is extending their on-call burden without consent
- Engineering managers may feel routing undermines their ability to manage team workload

### Test design: 5-question pre-experiment survey

This does not require a separate experiment. Run a targeted survey with 20–30 engineers from the early-access waitlist, before they have seen Sentinel.

**Survey instrument:**

> "We are building a feature that would suggest which engineer should receive an incoming alert, based on who has resolved that alert type most recently. We would like your honest reaction to this concept."

1. "If PagerDuty showed a 'Suggested responder: [name]' label when an alert fires, how would you feel about that?" (1–5: Very uncomfortable → Very comfortable)
2. "Would you expect to follow the suggestion, or would you typically reassign based on your own judgment?" (Always follow / Usually follow / Usually override / Always override)
3. "Under what circumstances would routing suggestions be most useful to you?" (open text)
4. "Under what circumstances would routing suggestions feel unhelpful or frustrating?" (open text)
5. "If routing suggestions went to engineers outside their scheduled on-call shift, how would you feel about that?" (1–5: Very uncomfortable → Very comfortable)

**Pass threshold:** ≥60% of respondents score ≥3 on Q1 (comfortable with routing suggestions). Q5 mean score ≥2.5 (some acceptance of off-rotation routing).

**Fail threshold:** <40% comfortable with routing suggestions, OR Q4 reveals a consistent pattern of concerns that the current routing UX design does not address.

**Action if fail:** The routing feature needs significant UX changes before the A/B experiment — at minimum, framing as "suggested" (not "assigned"), adding a low-friction override, and an explicit preference for in-rotation engineers. Delay A/B experiment until UX revision is complete.

**Timeline:** Survey runs week 1 of the pre-period. Results analyzed by week 2. If changes required, UX revision sprint in weeks 3–4 of pre-period before experiment start.

---

## Recommendation

Run the concierge test and the routing survey concurrently with the 4-week pre-period baseline collection. This is a zero-engineering-cost, 4-week commitment that answers three questions that the A/B experiment cannot answer on its own:

1. Are good runbooks achievable via prompt-based capture? (Concierge test)
2. Will engineers use runbooks when available? (Concierge test, secondary measure)
3. Is routing UX acceptable to engineers? (Pre-experiment survey)

If all three pass, proceed to A/B experiment with confidence that the mechanism works — the experiment then answers only whether the effect is large enough. If any one fails, the finding is more valuable than the A/B experiment would have been: it tells us exactly what needs to change before we spend engineering cycles on the wrong thing.

**Estimated total investment:** 12–16 hours of PM/researcher time over 4 weeks. No engineering required. The pre-period baseline data collection runs in parallel at no additional cost.

---

## Concierge test logistics

| Item | Owner | Due |
|------|-------|-----|
| Identify and confirm 2 volunteer teams | PM + CS lead | Week -4 (pre-period start) |
| Configure PagerDuty webhook to notify researcher on incident close | Eng lead (30-min task) | Week -4 |
| Create Notion runbook repository with template | PM | Week -4 |
| Draft and distribute routing survey to waitlist | PM | Week -4 |
| Weekly researcher debrief with PM | PM + researcher | End of weeks 1, 2, 3, 4 |
| Concierge test readout and go/no-go recommendation | PM | End of week 4 (pre-period) |
