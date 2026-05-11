# Pre-Mortem

## What It Is

A pre-mortem is a prospective failure analysis. Before a project launches, the team imagines it is some point in the future and the project has already failed — catastrophically, unambiguously, embarrassingly. The exercise: work backwards to explain why.

Developed by psychologist Gary Klein. The insight: groups are bad at generating failure scenarios before a decision because of optimism bias and social conformity. People who have reservations don't voice them because the group has already committed. A pre-mortem creates permission to voice failure scenarios by making failure the premise, not the fear.

A post-mortem asks "what went wrong?" A pre-mortem asks "what will go wrong?" The second is more valuable because there's still time to act.

---

## When to Use It

- Before any significant product launch
- Before a major architectural or technical decision
- At the start of a quarter, against the OKR plan
- Before a pricing change or major policy shift
- Any time the team feels dangerously aligned — consensus without dissent is a pre-mortem trigger

The threshold: if the failure of this project would be painful enough to warrant a post-mortem, it warrants a pre-mortem.

---

## How to Run It (PM Facilitation Guide)

**Time required**: 45–60 minutes  
**Participants**: Everyone who will work on the project, plus 1-2 skeptics from adjacent teams  
**Format**: Individual first, group second (prevents anchoring)

### Step 1: Set the premise (2 minutes)
"It is [date 6 months from now]. This project has failed. Not a small miss — a significant, visible failure. We're in a post-mortem. I want each of you to spend 5 minutes writing down the specific reasons it failed."

Key: make failure specific and vivid. "The project failed" is not specific. "We launched to 10,000 users, 8% complained about data quality, three enterprise accounts threatened churn, and the VP asked us to pull the feature" is specific.

### Step 2: Individual generation (5-7 minutes, silent)
Everyone writes their failure scenarios independently. No discussion. Silence is important — it prevents the loudest voice from anchoring the group.

### Step 3: Round-robin sharing (20-25 minutes)
Go around the room. Each person shares one failure scenario. No rebuttals during sharing — just capture. Continue until all unique scenarios are on the board.

### Step 4: Cluster and prioritize (10 minutes)
Group similar scenarios. Identify the top 3-5 by: (a) likelihood and (b) severity. These are your high-priority risks.

### Step 5: Convert to mitigations (10 minutes)
For each top risk: what specific action reduces its likelihood or impact? Assign an owner and a deadline. If no mitigation is possible, name the assumption you're accepting.

### Step 6: Document
Write up the pre-mortem findings. Keep them visible during the project — don't let them become a document that's filed and forgotten.

---

## Worked Example: Pulse Digest Launch Pre-Mortem

**Premise**: It is September 2026. The weekly digest launched in August and has been pulled after 3 weeks. Why did it fail?

**Failure scenarios generated:**

*Data quality*
- Collaboration scores were wrong for 340 small teams (shows 0), managers lost trust in the digest before it had a chance to build habit
- Team data was stale — managers saw metrics for employees who had left the company
- Digest sent to the wrong managers (account admin, not direct managers)

*Delivery*
- First send hit at 2pm instead of 9am — habit formation around "Monday morning" never happened
- Duplicate sends on the first week — same manager got 3 emails, immediately unsubscribed
- 18,000 simultaneous sends overwhelmed SendGrid; 40% delivered Tuesday

*User experience*
- Click-through goes to the homepage, not the relevant dashboard section — users can't find what the digest is pointing at
- No unsubscribe link — 12 spam complaints in week 1, SendGrid flagged the domain
- Mobile rendering broken on Outlook — 30% of enterprise users couldn't read it

*Business*
- Three large enterprise accounts got digests showing metrics they'd configured as private — security incident, legal review, feature pulled

**Top risks after clustering:**

| Risk | Likelihood | Severity | Mitigation | Owner |
|------|-----------|----------|------------|-------|
| Data quality errors erode trust | High | High | Data validation job before send; QA on 100 random digests before GA | Eng + PM |
| Delivery timing/duplication | Medium | High | Send window test at 100 users; idempotency on send job | Eng |
| No unsubscribe → spam flag | High | High | 1-click unsubscribe built and tested before GA | Eng |
| Private metric exposure | Low | Critical | Audit all metrics for privacy settings before including in digest template | PM + Legal |

**What changed in the PRD as a result:**
- Added "private metric audit" as a launch blocker
- Added 1-click unsubscribe as a hard requirement (not a nice-to-have)
- Added data validation job as a dependency for the send job
- Added send timing test (100 users, 1 week before GA) as a milestone

---

## Common Mistakes

**Making it a gripe session.**  
The pre-mortem is about failure scenarios, not about airing existing frustrations with the project. Facilitate toward specific, actionable risks.

**Only the PM participates.**  
Engineers, designers, and CS have different vantage points on failure. The exercise is most valuable when everyone contributes. Engineers see technical failure modes the PM won't.

**Generating risks and stopping there.**  
A pre-mortem without mitigations is just organized worry. Every high-priority risk needs an owner and a response, or the exercise was theater.

**Running it too late.**  
A pre-mortem two days before launch surfaces risks you can't mitigate. Run it at the PRD stage (when you still have design flexibility) and again at the sprint kickoff (when you have engineering context).

**Treating low-probability / high-severity risks as low-priority.**  
A 5% chance of a critical security incident deserves more attention than a 50% chance of a minor UX confusion. Weight severity, not just likelihood.

---

## Connections

- **[Inversion](second-order-thinking.md)** is the underlying cognitive mechanism of the pre-mortem
- **[Eigenquestions](eigenquestions.md)**: pre-mortems often surface the eigenquestion — the high-severity risk that keeps appearing in multiple scenarios is usually pointing at an unresolved foundational question
- The `ai-features/launch-checklist.md` is essentially a pre-mortem codified — the checklist items are the failure modes found in pre-mortems across many AI launches
- The `thinking/hard-decisions.md` "Shipping with a Known Bug" narrative is a real-time pre-mortem applied to a launch decision
