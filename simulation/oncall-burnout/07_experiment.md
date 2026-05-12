# Sentinel — Experiment Design
**Date:** 2026-05-12  
**Document type:** A/B Test Specification  
**Product:** Sentinel — On-Call Intelligence Platform  
**Status:** Draft — requires data science sign-off before instrumentation begins  
**Owner:** PM  
**Stakeholders:** Eng lead, Data/Analytics, CS lead

---

## Purpose

This document specifies the experiment that will determine whether Sentinel's two core MVP features — runbook capture at incident close and intelligent alert routing — measurably reduce MTTR. It defines the hypothesis, unit of randomization, metrics, sample size, and decision criteria in enough detail that any engineer or analyst can implement it without additional clarification.

---

## Hypothesis

**If** on-call engineers are prompted to document resolution steps before closing an incident, and subsequent incidents of the same type are routed to the engineer who most recently resolved that type,  
**then** MTTR for subsequent identical incidents will decrease by at least 30%,  
**because** the next responder can follow documented resolution steps rather than troubleshoot from scratch, and routing ensures the most contextually relevant engineer receives the alert.

This is a compound hypothesis (two features, one measurement). The tradeoff is acknowledged: we cannot isolate which feature drives the effect. We will run a follow-up factorial experiment post-launch if results are significant.

---

## Experiment Type

**Design:** Parallel A/B test (two-arm)  
**Assignment:** Cluster-randomized by engineering team  
**Duration:** 4 weeks (active measurement), preceded by 4-week pre-period for baseline establishment  

| Arm | Name | Treatment |
|-----|------|-----------|
| A (Control) | Standard workflow | Current PagerDuty/OpsGenie workflow with no changes. No runbook prompts, no routing suggestions. |
| B (Treatment) | Sentinel full | Runbook capture prompt at incident close + intelligent routing suggestion at incident open. |

**Why cluster-randomized?** Routing affects the entire team — you cannot route to engineer A on treatment and engineer B on control within the same team. Randomizing by individual engineer would contaminate both arms. The team is the natural unit.

---

## Unit of Randomization

**Unit:** Engineering team (organization + team identifier)  
**Eligibility criteria:**
- Uses PagerDuty or OpsGenie as primary alerting tool
- Minimum 3 on-call engineers in rotation
- Minimum 15 incidents per month (lower volume produces unstable MTTR estimates)
- Has completed Sentinel onboarding (webhook integration live, ≥3 days of data)
- Has not used any runbook tooling in the prior 90 days (to avoid contamination from prior documentation investments)

**Ineligible:**
- Teams with dedicated SRE function (these are not our ICP and their baseline MTTR is already low)
- Teams with fewer than 3 engineers (routing degrades to near-random at this size)
- Teams that have recently undergone a major architecture migration (alert pattern instability — see File 06, Assumption 2)

---

## Metrics

### Primary metric
**MTTR (Mean Time to Resolution)**  
- Definition: `incident_closed.timestamp − incident_opened.timestamp`, in minutes, per incident
- Aggregation: Median MTTR per team per week (median is more robust to the long tail of complex incidents than mean)
- Baseline: 47 minutes (from pre-period measurement)
- Minimum detectable effect (MDE): 14-minute reduction (30% relative lift)
- Direction: Decrease is good

### Secondary metrics
| Metric | Definition | Direction | Notes |
|--------|-----------|-----------|-------|
| Runbook coverage rate | % of closed incidents with an attached runbook (non-empty, ≥50 words) | Increase is good | Quality floor enforced by word count threshold; not a perfect proxy for quality |
| Routing acceptance rate | % of routing suggestions accepted (not overridden) by the assigned engineer | Increase is good | Measures whether engineers trust the system |
| Repeat incident rate | % of incidents that are a repeat of an alert type seen in the prior 30 days | Decrease is good | Proxy for whether runbooks prevent recurrence |

### Guardrail metrics (must not move negatively)
| Metric | Definition | Threshold | Action if breached |
|--------|-----------|-----------|-------------------|
| Acknowledgement time | Time from incident open to first acknowledgement, in minutes | Must not increase by >20% vs control | Pause experiment; review routing UX |
| On-call satisfaction score | Weekly survey, 1–5 scale ("How would you rate your on-call experience this week?") | Must not decrease by >0.5 points vs baseline | Pause experiment; escalate to PM and CS lead |
| Incident volume | Count of incidents opened per team per week | Must not increase vs control | Escalate; investigate alert noise amplification |

### Excluded metrics
- HDI (Hero Dependency Index): 4 weeks is insufficient time to meaningfully move HDI; it is a lagging structural metric. HDI will be tracked post-experiment in the 90-day followup cohort.
- Runbook quality score: No automated quality signal exists yet. This is the subject of the concierge test (see File 08). Do not use word count as a quality proxy in the primary analysis — use it only as the completeness floor.

---

## Sample Size

### Calculation inputs
- Baseline MTTR: 47 minutes (median)
- Target MTTR reduction: 14 minutes (30% relative)
- Estimated MTTR standard deviation: 22 minutes (estimated from typical on-call distributions; to be confirmed from pre-period data)
- Power: 80%
- Significance level (α): 0.05 (two-tailed)
- MTTR distribution: right-skewed; analysis will use Mann-Whitney U test on weekly median MTTR per team

### Required sample
- **30 teams per arm, 60 teams total**
- At estimated incident volume of ~25 incidents/team/month, this yields approximately 1,500 incidents in the treatment arm over 4 weeks — sufficient to estimate median MTTR with reasonable precision
- If pre-period data shows higher MTTR variance than assumed, the experiment may require extension to 6 weeks. This decision should be made at the 2-week check-in using observed variance.

### Recruitment plan
- Target: 80 eligible teams from early-access waitlist (buffer for ineligibility and dropout)
- Randomization: stratified by team size (3–7 engineers vs. 8–20 engineers) to ensure balance
- Assignment: computed at experiment start; fixed for the duration of the experiment (no crossover)

---

## Analysis Plan

### Pre-period
- 4 weeks of baseline measurement before experiment start
- Confirm MTTR distribution shape and variance
- Identify any teams with anomalous incident patterns (>3 standard deviations from cohort mean — exclude before randomization)
- Establish runbook coverage baseline (expected: ~0% in control cohort for eligible teams)

### Primary analysis
- **Unit:** Team-week (one observation per team per week)
- **Test:** Mann-Whitney U test on median MTTR, treatment vs. control, pooled across all 4 weeks
- **Covariate adjustment:** Regression on pre-period MTTR to reduce variance and improve power
- **Significance threshold:** p < 0.05 (two-tailed)
- **Effect size:** Report Hodges-Lehmann estimator (rank-based effect size for non-parametric test)

### Secondary analyses
- Subgroup analysis: teams with high pre-period incident volume (>30/month) vs. lower volume — routing has more signal in high-volume teams
- Subgroup analysis: repeat incident rate — compute MTTR separately for first-occurrence vs. repeat incidents; the hypothesis predicts the effect should be concentrated in repeat incidents
- Routing override rate analysis: Is MTTR lower in teams with higher routing acceptance rates? This tests whether routing quality is a mediator.

### Guardrail monitoring
- Acknowledgement time and satisfaction score checked weekly throughout the experiment
- Automated alert if either guardrail breaches threshold; experiment pause requires PM + Eng lead approval

---

## Decision Criteria

The primary decision is made at experiment end (week 4 + pre-period). Three outcomes are possible:

### Ship
**Criteria (all must be met):**
- MTTR reduction ≥14 minutes, p < 0.05
- Neither guardrail metric has breached threshold during the experiment
- Routing acceptance rate ≥50% (engineers are accepting more than they override — system is trusted)

**Action:** Proceed to GA launch. Begin HDI tracking cohort for 90-day followup.

### Iterate
**Criteria (any of the following):**
- MTTR reduction is positive but <14 minutes (effect exists but below MDE: 5–14 minute reduction, p < 0.05)
- MTTR reduction ≥14 minutes but routing acceptance rate <50% (feature is working but not trusted — UX problem)
- Runbook coverage rate <40% in treatment arm (capture prompt is not converting — behavior problem)
- One guardrail metric breached threshold but has since recovered

**Action:** Do not ship. Run a focused iteration sprint on the specific failing component. Rerun experiment on the revised feature with a new cohort (no cross-contamination with prior participants).

### Kill
**Criteria (any of the following):**
- MTTR reduction is null or negative at week 4 (no effect or harm, p > 0.10 for any positive effect)
- Either guardrail metric breached threshold and did not recover
- Routing acceptance rate <20% (engineers are systematically overriding — the system is actively unwanted)

**Action:** Halt experiment. Conduct qualitative review with 5–10 teams to understand failure mode. Write retrospective. Present findings to stakeholders before deciding whether to pivot or sunset.

---

## Riskiest assumption

The most dangerous assumption this experiment cannot directly test: **runbook quality**.

The experiment measures MTTR. It does not measure whether runbooks are actually useful. It is possible to see MTTR improvement for reasons unrelated to runbook quality (e.g., routing alone drives the effect, or Hawthorne effect on treated teams). It is also possible to see no MTTR improvement even though runbooks are high quality, if the routing is systematically wrong.

The specific risk: engineers write runbooks that are formally complete (≥50 words, passes the coverage filter) but contain no actionable information. The system accumulates a corpus of "checked logs, restarted service" entries. The routing engine routes a new engineer to a historical resolver who documented nothing useful. The new engineer sees the runbook, learns nothing, and solves the incident through personal investigation — exactly as they would have without Sentinel. MTTR does not change. Runbook coverage looks healthy. The product has created the appearance of knowledge management without the substance.

This assumption should be tested before the A/B experiment begins. See File 08 (Assumption Test Spec) for the concierge test design that kills this assumption in 4 weeks at zero engineering cost.

**Recommendation:** Run the concierge test concurrently with pre-period baseline collection. The 4-week concierge test timeline aligns with the 4-week pre-period. If the concierge test fails (runbooks are not useful even when produced at high quality), kill the runbook capture feature before the A/B experiment begins and respecify the experiment to test routing in isolation.

---

## Timeline

| Week | Activity |
|------|----------|
| -6 to -4 | Instrumentation validation complete (see File 10). Baseline event data confirmed flowing. |
| -4 to 0 | Pre-period: baseline MTTR measurement. Concierge test running in parallel (File 08). Cohort recruited and randomized. |
| 0 | Experiment start. Treatment teams receive Sentinel with runbook capture + routing enabled. |
| 2 | Mid-point check-in. Review guardrail metrics. Confirm MTTR variance estimate. Decide whether to extend to 6 weeks. |
| 4 | Experiment end. Primary analysis run. Decision criteria applied. |
| 5 | Results socialized. Ship/Iterate/Kill decision made and communicated to stakeholders. |
| 6+ | If Ship: GA launch + 90-day HDI tracking cohort begins. |

---

## Open questions before experiment start

1. **Satisfaction survey instrument:** Who owns the weekly on-call satisfaction survey? Does it go through Slack (bot), email, or the Sentinel dashboard? Response rate target: ≥60% per team per week. Below 40%, the guardrail is unmeasurable.
2. **Runbook quality review:** Will a human spot-check runbook quality at week 2 (midpoint)? If the concierge test is not run and runbook quality is poor, the only way to catch it before experiment end is a manual review of a sample of treatment-arm runbooks.
3. **PagerDuty schedule access:** HDI tracking post-experiment requires rotation schedule data from PagerDuty API, not just resolution records. Has this integration been scoped? (See File 10 for instrumentation implications.)
4. **Multi-product contamination:** If a treatment-arm team also uses another incident management tool (e.g., Rootly, FireHydrant) in parallel with PagerDuty, MTTR measurement will be incomplete. Eligibility screening must confirm PagerDuty/OpsGenie is the sole incident tool.
