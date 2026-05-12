# File 19 — Exec Update: Sentinel MVP
**Product**: Sentinel — On-Call Intelligence Platform  
**Date**: 2026-05-12  
**Status**: 🟡 YELLOW — On track for core features; HDI dashboard may slip 1 week  
**Audience**: VP Product, CFO, CEO  
**Prepared by**: PM, Sentinel

---

## Summary

We are shipping Sentinel MVP on schedule with two of three features (runbook capture, intelligent routing). The HDI dashboard is at risk of a 1-week delay due to PagerDuty schedule API complexity identified in last week's tech lead review. We are not at risk of a full launch slip — soft launch proceeds to 5 beta customers as planned. The ask at the end of this update is narrow: approval to delay the HDI dashboard by one week, and introductions to 3 prospects who have mentioned on-call in discovery.

---

## What We're Shipping

| Feature | Status | Launch Date |
|---------|--------|-------------|
| Runbook capture at incident close | Green — on track | 2026-05-19 (soft launch) |
| Intelligent routing (heuristic) | Green — on track | 2026-05-19 (soft launch) |
| Hero Dependency Index dashboard | Yellow — 1-week slip risk | 2026-05-26 (revised from 2026-05-19) |

**Runbook Capture**: Blocking modal fires at incident close. Engineer must submit a runbook or explicitly choose "Skip" with a reason. The blocking behavior is the core intervention — it is intentional friction. Build is complete; in QA.

**Intelligent Routing**: Heuristic engine matches incoming alert type against resolution history and surfaces a suggested assignee. No ML — pattern matching over alert text + engineer resolution records. Routing suggestion p99 latency tested at 340ms (target: <500ms).

**HDI Dashboard**: Calculates what percentage of incidents in a period were handled by a single engineer. Complication: syncing on-call schedule data from PagerDuty's schedule API requires handling schedule overrides and escalation policy layers, which was not fully scoped in sprint planning. An additional 3-4 days of backend work is needed. Frontend is complete.

---

## Confidence Level: Medium

**What's working**:
- Concierge test (manual simulation with 6 engineers, 4 weeks, synthetic incidents) showed **52% MTTR reduction** when engineers used runbooks to resolve incidents. This exceeds our 30% threshold and is above the 47→28-minute target trajectory.
- Routing suggestions accepted 68% of the time in concierge test (no baseline exists; this is a positive early signal).

**What's not working yet**:
- Only **41% of engineers referenced a runbook** without a prompt during the concierge test. Our target for self-directed runbook use is 60%. This is below threshold.
- **Implication**: The runbook capture prompt is critical. If engineers skip capture, the library never grows, search returns nothing, and the system's value collapses. The "skip" scenario is therefore our highest product risk.
- Engineers who were prompted to use a runbook resolved incidents 52% faster. Engineers who weren't prompted defaulted to their own knowledge, with no improvement.

**What this means for launch**: We are launching. The concierge data is directionally positive. But the 41% self-directed use number suggests that the real metric to watch in beta is **capture completion rate**, not MTTR (which requires enough runbook coverage to be meaningful).

---

## Key Metrics to Watch

| Metric | Baseline | Target (60 days) | Current (concierge) | Watch Threshold |
|--------|----------|------------------|---------------------|-----------------|
| MTTR (median) | 47 min | 28 min | 39 min (when runbooks used) | > 42 min at 30 days = investigate |
| Hero Dependency Index | 64% | 30% | 51% (concierge, 4 weeks) | No change at 30 days = routing not working |
| Runbook capture completion rate | N/A | > 60% of closes include runbook | 41% (prompted); not measured unprompted | < 40% = skip behavior too high, reconsider modal UX |
| Routing suggestion acceptance rate | N/A | > 50% | 68% (concierge) | < 40% = suggestions aren't credible |
| Runbook search usage (incidents/week using search) | N/A | > 30% of incidents | Not yet measured | < 10% at 30 days = library not growing |

---

## Risks

### Risk 1: Runbook Quality — Engineers Write Low-Effort Entries
**Likelihood**: High (observed in concierge test)  
**Impact**: P1 — Low-quality runbooks reduce the value of search, slow routing improvement, and undermine manager confidence in the product  
**Current state**: In concierge test, approximately 40% of submitted runbooks were 1-2 sentences ("restarted the service"). These are technically compliant (the modal accepts any submission ≥1 step, ≥10 chars) but have near-zero utility.  
**Mitigation**: Structured templates added to capture form (sprint 4). Quality scoring retrofitted in sprint 5. For now, this is a known gap.  
**Ask**: None. Tracking.

### Risk 2: HDI Schedule Sync Complexity (PagerDuty API)
**Likelihood**: High (already surfaced in tech review)  
**Impact**: P1 — HDI dashboard delayed 1 week; customers see an incomplete product at soft launch  
**Current state**: PagerDuty's schedule API returns complex nested objects for overrides and escalation layers. Our initial sync implementation assumed a flat schedule model. Fixing requires 3-4 additional backend days.  
**Mitigation**: Soft launch proceeds without HDI dashboard; customers are told it's "coming in week 2." Full launch still includes HDI.  
**Ask**: Approval to shift HDI launch date from 2026-05-19 to 2026-05-26. (See asks below.)

### Risk 3: PagerDuty API Rate Limits at Scale
**Likelihood**: Low for beta (5 customers); Medium at scale (50+ customers)  
**Impact**: P2 — At high incident volume, our polling of the PagerDuty schedule API could hit their rate limit (600 req/min per token). At beta scale, this is not an issue.  
**Mitigation**: Implement exponential backoff and per-customer token management before full launch. Spike scheduled for sprint 5.  
**Ask**: None. Tracking.

---

## Launch Plan

**Soft launch (2026-05-19)**:
- 5 beta customers (selected: teams who mentioned on-call pain in discovery or renewal calls)
- Features available: runbook capture + routing
- HDI dashboard: not yet available; customers notified in advance
- CS on-call for first 2 weeks; weekly check-in calls scheduled
- Go/No-Go criteria: all P0 QA scenarios passing in staging

**Full launch (2026-06-02)**:
- All 3 features available (including HDI dashboard, after 1-week slip)
- Marketing email to waitlist
- AE team enabled with one-pager and demo script
- Public announcement on blog and LinkedIn

**What success looks like at 30 days**:
- ≥3 of 5 beta customers actively using runbook capture
- At least 10 runbooks submitted per beta customer
- At least one customer with measurable MTTR improvement (>15% vs. their baseline)
- Zero P0 bugs in production

---

## Asks

**Ask 1 — Approval to delay HDI dashboard by 1 week**  
The PagerDuty schedule API complexity requires 3-4 additional engineering days. Shipping an incomplete or inaccurate HDI dashboard at soft launch would undermine trust with beta customers. Requesting approval to shift HDI from 2026-05-19 to 2026-05-26. Runbook capture and routing ship as planned.

**Ask 2 — Introductions to 3 prospects who have mentioned on-call in discovery**  
Our beta cohort of 5 is full. For the full launch pipeline, we'd like warm introductions to prospects where on-call was mentioned as a pain point. AE team has flagged 5 candidates; asking leadership to review and facilitate 3 intros before 2026-05-26.

---

## Appendix: Concierge Test Summary

**Setup**: 6 engineers from one internal team; synthetic incidents triggered over 4 weeks; PM manually prompted runbook capture and routing suggestions.  
**MTTR result**: 52% reduction when runbooks were referenced (47 min → ~23 min). Note: this is a synthetic environment. Real-world improvement will be lower as runbook library grows from zero.  
**Self-directed runbook use**: 41% without prompt. Target is 60%. Gap is significant and informs the blocking modal design.  
**Routing acceptance**: 68% of routing suggestions accepted without override. Promising, but engineers in the test knew the suggestions were coming — real-world acceptance may vary.  
**Key takeaway**: The system works when engineers use it. The product risk is behavioral (will engineers use it without a prompt?), not technical.
