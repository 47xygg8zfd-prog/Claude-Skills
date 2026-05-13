# DACI Decision Framework

## What is DACI?

DACI is a framework for clarifying who owns a decision before you make it. The four roles:

- **Driver**: The person responsible for moving the decision forward — gathering input, running the process, writing the recommendation. There is exactly one Driver. If there are two, you have a coordination problem, not a Driver.
- **Approver**: The person with final sign-off authority. One person, not a committee. If you have multiple Approvers, the decision will either stall or default to whoever is most senior in the room — which is not a decision process, it's a power dynamic.
- **Contributor**: People whose input materially affects the decision. They advise; they don't veto. Contributors should be consulted before the Approver decides, not after.
- **Informed**: People who need to know the outcome but don't shape it. Informing this group is not optional — skipping it creates surprises downstream.

**DACI vs RACI**: RACI (Responsible, Accountable, Consulted, Informed) is designed for tasks and deliverables. DACI is designed for decisions. The key difference: DACI separates the person who drives the process (Driver) from the person who owns the outcome (Approver). This matters in product work because the PM often drives decisions they don't have authority to approve.

---

## When to Use DACI

Use DACI when:
- Multiple stakeholders have opinions and it's unclear who decides
- A decision crosses team or function boundaries
- You've been in the same meeting about the same topic for the second or third time
- Someone is about to make a major investment (engineering weeks, budget, design cycles) without agreement on who owns the call

You don't need DACI for every decision. Day-to-day sprint calls, copy tweaks, and minor design changes don't need a framework — they need a PM with good judgment. Save DACI for decisions with real stakes and real ambiguity.

---

## The Template

**Decision**: [One sentence — name the decision, not the problem]

**Context**: [2-3 sentences. What's the situation, what's the pressure to decide now, what are the constraints?]

**Options considered**:
1. [Option A] — [Brief description]
2. [Option B] — [Brief description]
3. [Option C / Do nothing] — [Brief description]

**Recommendation**: [Which option and why — the Driver's view, not a hedge]

**Decision date**: [When this must be resolved]

| Role | Name | Responsibility |
|------|------|---------------|
| Driver | | Owns the process, writes the recommendation |
| Approver | | Final sign-off |
| Contributor | | Consulted before decision |
| Contributor | | Consulted before decision |
| Informed | | Notified after decision |

**Decision made**: [Final call + date]
**Rationale**: [Why this option]

---

## Worked Example: Slack Integration vs. Mobile App

**Decision**: Should Pulse build a Slack integration or a native mobile app as the next platform investment?

**Context**: Pulse's digest-active WAU growth has plateaued at 44% (target: 52%). CS lead Morgan is fielding requests for both Slack notifications and a mobile app from ICP accounts. Engineering capacity allows one major platform project in Q3. We need a decision by May 20 to lock the Q3 roadmap.

**Options considered**:
1. **Slack integration** — Push digest summaries and key alerts into the manager's existing Slack workflow. Estimated 6-week build (Sam's estimate). Supports existing users; doesn't require app installation.
2. **Native mobile app (MVP)** — iOS-first, digest + key metrics. Estimated 14-week build. Opens a new use case (async mobile check-ins) but delays any Slack work indefinitely.
3. **Do nothing on platform** — Stay web-only, invest Q3 capacity in recommendation quality instead.

**Recommendation**: Build the Slack integration first. Mobile expands the surface area but doesn't fix the retention problem. The managers not opening the digest aren't avoiding Pulse because they're on mobile — they're avoiding it because it's not in their existing workflow. Slack is where they already live. A 6-week integration with measurable impact on digest open rate is a better Q3 bet than a 14-week mobile build with uncertain activation.

**Decision date**: May 20, 2026

| Role | Name | Responsibility |
|------|------|---------------|
| Driver | Jordan (PM) | Owns process, wrote recommendation |
| Approver | Sam (Eng Lead) | Approves feasibility and capacity commitment |
| Contributor | Priya (Design) | Input on UX scope and integration design |
| Contributor | Morgan (CS) | Input on customer signal and account risk |
| Contributor | Alex (Data) | Input on which metrics to surface in Slack |
| Informed | VP Product | Notified once decision is made |

**Decision made**: Slack integration. May 19, 2026.
**Rationale**: Aligned with Rec above. Morgan confirmed 3 ICP accounts specifically cited Slack as the missing touchpoint. Sam confirmed 6-week estimate holds if design scope is scoped to digest summary + two key alerts only.

---

## Common Failure Modes

**Too many Approvers**: If you list three Approvers, you don't have a decision process — you have a committee. Committees don't decide, they negotiate. Force the escalation: identify the single person who can say yes and own the consequences.

**Contributors who want to be Approvers**: This is a political problem, not a framework problem. If a Contributor is blocking progress because they feel their input wasn't weighted correctly, have the conversation directly — don't add them as a second Approver to smooth it over.

**Forgetting to inform the Informed group**: The most common failure. The Informed group exists because decisions have downstream effects. If CS lead Morgan isn't told about the Slack integration decision before it ships, she'll find out from a customer. Run the notification step as a task, not an afterthought.
