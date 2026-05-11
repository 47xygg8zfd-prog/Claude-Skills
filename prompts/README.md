# PM Prompt Library

Copy-paste Claude prompts for one-off tasks that don't need a full skill. Organized by category.

---

## Backlog & Tickets

| Prompt | Use When |
|--------|----------|
| [Rewrite ticket title](#rewrite-ticket-title) | Title is vague or task-framed |
| [Generate AC from a description](#generate-ac-from-description) | Ticket has a description but no acceptance criteria |
| [Split an oversized story](#split-an-oversized-story) | Story is 8+ points and needs breaking down |
| [Write a spike story](#write-a-spike-story) | There's an unknown that needs time-boxed research |
| [Definition of Ready checklist](#definition-of-ready-checklist) | Pre-sprint ticket review |

## Meetings & Communication

| Prompt | Use When |
|--------|----------|
| [Meeting agenda](#meeting-agenda) | Any recurring or ad-hoc meeting |
| [Action items from notes](#action-items-from-notes) | Post-meeting cleanup |
| [Summarize a long Slack thread](#summarize-a-long-slack-thread) | Thread went sideways and you need the TL;DR |
| [Decision log entry](#decision-log-entry) | Recording a key decision and its rationale |

## Research & Analysis

| Prompt | Use When |
|--------|----------|
| [5 hypotheses from data](#5-hypotheses-from-data) | You have a metric change and need to explain it |
| [Pro/con table](#procon-table) | Comparing two approaches before making a call |
| [Reframe feedback as opportunity](#reframe-feedback-as-opportunity) | Turning negative customer feedback into product direction |
| [Devil's advocate](#devils-advocate) | Stress-testing a decision before you commit |

## Writing & Editing

| Prompt | Use When |
|--------|----------|
| [Tighten this copy](#tighten-this-copy) | Any PM writing that's too long |
| [Rewrite for a non-technical audience](#rewrite-for-non-technical-audience) | Engineering output going to execs or customers |
| [Generate 3 alternatives](#generate-3-alternatives) | Stuck on one framing and want options |

---

## Prompts

### Rewrite ticket title
```
Rewrite this Jira ticket title to be outcome-oriented and specific.
Current title: "[PASTE TITLE]"
Rules: start with a verb, describe the outcome not the task, under 60 characters.
Give me 3 options.
```

---

### Generate AC from description
```
Write acceptance criteria for this ticket.
Description: "[PASTE DESCRIPTION]"
Format: checkbox list. Each item should be testable and binary (pass/fail).
Include happy path, at least one edge case, and any error state that matters.
```

---

### Split an oversized story
```
This story is too large for one sprint. Split it into 2-4 smaller stories
that each deliver independent value and could ship separately.
Original story: "[PASTE STORY]"
For each new story, give: title, one-line description, and estimated points (1/2/3/5).
```

---

### Write a spike story
```
Write a spike story for this unknown: "[DESCRIBE THE UNKNOWN]"
Format:
- Title: "Spike: [topic]"
- Goal: what question this spike answers
- Timebox: [X] hours
- Output: what artifact or decision comes out of the spike
- Out of scope: what we are NOT solving in this spike
```

---

### Definition of Ready checklist
```
Review this ticket against our Definition of Ready and flag anything missing.
Ticket: "[PASTE TICKET TITLE + DESCRIPTION]"
Definition of Ready:
- [ ] Outcome-oriented title
- [ ] Clear problem statement or user story
- [ ] Acceptance criteria defined
- [ ] Dependencies identified
- [ ] Estimated (points assigned)
- [ ] Design attached or not required
- [ ] No open blockers
Flag each item as PASS, FAIL, or N/A with a one-line note.
```

---

### Meeting agenda
```
Write a focused agenda for this meeting.
Meeting: "[MEETING NAME]"
Duration: [X] minutes
Goal: "[What decision or output do we need by the end?]"
Attendees: [list roles, not names]
Context: "[Any relevant background]"
Format: time-boxed items with owner and desired outcome per item.
```

---

### Action items from notes
```
Extract action items from these meeting notes.
Notes: "[PASTE NOTES]"
Format each action item as:
- [ ] [Action] — Owner: [Name/Role] — Due: [Date or "next meeting"]
Group by owner. Flag any items with no clear owner as "UNASSIGNED".
```

---

### Summarize a long Slack thread
```
Summarize this Slack thread in 3-5 bullet points.
Thread: "[PASTE THREAD]"
Include: the core question or topic, key positions or options raised,
any decision reached, and any open items or next steps.
```

---

### Decision log entry
```
Write a decision log entry for this decision.
Decision: "[WHAT WAS DECIDED]"
Context: "[WHY THIS CAME UP]"
Alternatives considered: "[OTHER OPTIONS WE LOOKED AT]"
Rationale: "[WHY WE CHOSE THIS]"
Format it for a Confluence decision log. Include date, decision owner, and a "revisit if" trigger condition.
```

---

### 5 hypotheses from data
```
Generate 5 hypotheses to explain this metric change.
Metric: "[METRIC NAME]"
Change: "[e.g. dropped 18% week-over-week]"
Context: "[Any recent changes — releases, campaigns, incidents]"
For each hypothesis: state the hypothesis, what data would confirm it,
and what data would rule it out.
```

---

### Pro/con table
```
Build a pro/con table comparing these two options.
Option A: "[DESCRIBE OPTION A]"
Option B: "[DESCRIBE OPTION B]"
Evaluate on: customer impact, engineering effort, speed to market, risk, reversibility.
End with a one-sentence recommendation and the key tradeoff.
```

---

### Reframe feedback as opportunity
```
Reframe this customer feedback as a product opportunity statement.
Feedback: "[PASTE FEEDBACK]"
Format: "How might we help [user type] [achieve goal] without [current frustration]?"
Give 2-3 versions at different levels of specificity.
```

---

### Devil's advocate
```
Play devil's advocate on this decision.
Decision: "[WHAT WE'RE PLANNING TO DO]"
Give me the 3 strongest arguments against it, the most likely way it fails,
and the one thing we should validate before committing.
Be direct — I want the real objections, not softened ones.
```

---

### Tighten this copy
```
Edit this for conciseness. Cut anything that doesn't add meaning.
Target: reduce word count by ~30% without losing any key information.
Text: "[PASTE TEXT]"
Return the edited version only, no commentary.
```

---

### Rewrite for non-technical audience
```
Rewrite this for a non-technical audience (executives or customers).
Remove jargon. Lead with the business impact, not the technical detail.
Original: "[PASTE TEXT]"
Audience: [e.g. C-suite / customers / sales team]
```

---

### Generate 3 alternatives
```
Give me 3 alternative ways to frame this.
Current framing: "[PASTE CURRENT VERSION]"
Context: "[What it's for and who will read it]"
Make each alternative meaningfully different — not just word swaps.
```
