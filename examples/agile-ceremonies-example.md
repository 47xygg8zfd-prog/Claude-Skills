# Example Output: Agile Ceremonies Skill

**Prompt used:** "Run the sprint retrospective for our digest feature sprint"

---

## Sprint Retrospective — Pulse Team
**Sprint**: 24 (Weekly Digest v1 — Sprint 1)  
**Date**: 2026-05-08  
**Facilitator**: Claude  
**Format**: Start / Stop / Continue + Action Items

---

### What We Shipped
- Digest data aggregation job (Story 2) ✅
- Email template (Story 3) ✅
- Admin opt-in setting (Story 1) — carried over (80% complete) 🔶

---

### Start

> Things we should begin doing

- **Writing acceptance criteria before sprint starts, not during.** Story 1 lost 2 days because edge cases around multi-timezone orgs weren't defined until mid-sprint.
- **Scheduling a design + eng sync at kickoff.** The email template went through 3 revision cycles because design feedback came in async after implementation had started.
- **Adding a "spike" story for unknowns.** The email provider rate limit question caused unplanned research. A scoped spike would have surfaced this in planning.

---

### Stop

> Things we should stop doing

- **Pulling in scope mid-sprint.** The analytics tracking story (Story 5) was partially started this sprint outside the committed scope, pulling focus from the carry-over story.
- **Skipping standup when async updates are posted.** Three standups were skipped. Issues that needed unblocking sat for a full day as a result.

---

### Continue

> Things working well that we should keep doing

- **Pairing on backend data jobs.** The aggregation job was the most complex story and the pair-programming approach caught two edge cases early.
- **Using the PRD as the source of truth in reviews.** Referencing the PRD success metrics during demo kept the review focused on outcomes, not just features.
- **Short async design reviews in Slack before full review.** Cut the formal design review from 60 to 30 minutes.

---

### Action Items

| Action | Owner | Due |
|--------|-------|-----|
| Add "AC must be complete before sprint starts" to our Definition of Ready | Sarah (PM) | Before Sprint 25 planning |
| Schedule design + eng kickoff as recurring 30-min at sprint start | Eng lead | This week |
| Add spike story template to Jira | Scrum master | Before Sprint 25 planning |
| Revisit and close Story 1 carry-over as first priority in Sprint 25 | Dev team | Sprint 25 Day 1 |

---

### Team Health Check (1–5)

| Dimension | Score | Notes |
|-----------|-------|-------|
| Clarity of goals | 4 | PRD helped; AC gaps hurt |
| Team collaboration | 4 | Pairing worked well |
| Process efficiency | 3 | Mid-sprint scope creep and skipped standups |
| Technical quality | 4 | Good test coverage on data job |
| Overall sprint satisfaction | 3.5 | Carry-over stings, but good progress |
