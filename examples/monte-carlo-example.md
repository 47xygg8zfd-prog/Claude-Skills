# Example Output: Monte Carlo Skill

**Prompt used:** "When will we finish the digest feature? We have 18 story points left, our last 4 sprints averaged 11, 9, 13, and 10 points, and we're targeting an August 4 launch."

---

## Monte Carlo Forecast: Weekly Digest Feature

**Input Data**
- Remaining scope: 18 story points
- Sprint length: 2 weeks
- Historical throughput (last 4 sprints): 11, 9, 13, 10 pts
- Target launch date: August 4, 2026

---

## Throughput Analysis

| Metric | Value |
|--------|-------|
| Mean throughput | 10.75 pts/sprint |
| Std deviation | 1.71 pts/sprint |
| Min observed | 9 pts/sprint |
| Max observed | 13 pts/sprint |

---

## Simulated Completion Distribution (10,000 runs)

| Probability | Sprints Needed | Projected Completion |
|-------------|---------------|----------------------|
| 50% (likely) | 1.7 sprints | **~July 21, 2026** |
| 75% (confident) | 2.0 sprints | **~Aug 4, 2026** |
| 85% (safe) | 2.2 sprints | **~Aug 11, 2026** |
| 95% (very safe) | 2.6 sprints | **~Aug 25, 2026** |

*Simulation assumes throughput drawn from a normal distribution based on historical data. No scope changes assumed.*

---

## Summary

**The August 4 target is achievable but tight — there's a 75% chance of hitting it.**

At your historical average pace, you'll finish in approximately 1.7 sprints (~July 21), which actually gives you a small buffer. However, one slow sprint (like the 9-point sprint two cycles ago) would push you to the edge of the window.

**Recommendation**: Treat August 4 as a firm deadline and protect scope. If any new stories are added before completion, re-run this forecast — even 3 additional points shifts the 75% confidence date to August 11.

---

## Risk Factors Not Modeled

- Vacations or team availability changes in sprints ahead
- Dependency on ML recommendation model (external team — estimated 3 weeks, not yet confirmed)
- SendGrid contract resolution (could affect end-to-end testing)

**If the ML model slips by 1 week**, add approximately 4 story points of rework/integration to remaining scope. Reforecast would shift the 75% date to ~August 18.
