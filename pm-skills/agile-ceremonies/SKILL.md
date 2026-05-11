---
name: agile-ceremonies
description: >
  Facilitate and prepare for agile ceremonies: sprint planning, backlog refinement, retrospectives,
  standups, and sprint reviews. Use this skill whenever the user mentions running a retro, planning
  a sprint, doing refinement, grooming the backlog, or preparing for any agile ceremony. Also trigger
  for phrases like "help me run the retro", "what should we cover in planning", "create a retro board",
  "refinement agenda", or "sprint review template". Produces facilitation guides, agendas, talking
  points, and templates ready to use in the meeting.
---

# Agile Ceremonies Skill

Prepare and facilitate agile ceremonies with structure, talking points, and ready-to-use templates.

---

## Ceremonies Covered

1. [Sprint Planning](#sprint-planning)
2. [Backlog Refinement](#backlog-refinement)
3. [Retrospective](#retrospective)
4. [Daily Standup](#daily-standup)
5. [Sprint Review / Demo](#sprint-review--demo)

---

## Sprint Planning

**Goal**: Align the team on sprint goal and commit to a realistic set of work.

**Recommended Duration**: 1 hour per sprint week (2-week sprint = 2 hours max)

### Agenda Template
```
Sprint Planning — Sprint [#] | [Date]
Attendees: Dev team, PM, Scrum Master

[15 min] Sprint Goal Setting
  - PM presents priorities and business context
  - Team aligns on 1 sprint goal statement
  - Format: "By end of sprint, we will [outcome] so that [value]"

[20 min] Capacity Check
  - Each engineer states availability (days, PTO, etc.)
  - Calculate team capacity in story points or days
  - Account for ceremonies (~20% overhead)

[40 min] Story Walkthrough & Commitment
  - Walk top-priority stories from refined backlog
  - Team confirms understanding, asks questions
  - Pull stories until capacity is reached
  - Do NOT overcommit — leave 10–15% buffer

[10 min] Task Breakdown (optional)
  - Break committed stories into tasks
  - Assign owners

[5 min] Confirm Sprint Goal
  - Restate goal, confirm everyone is aligned
```

### PM Talking Points
- What changed since last sprint? (business context, priorities)
- What is the #1 thing we MUST ship this sprint?
- Are there any external dependencies or deadlines?
- What does "done" look like for the sprint?

---

## Backlog Refinement

**Goal**: Ensure the top of the backlog is ready to be pulled into a sprint — stories are estimated, understood, and unblocked.

**Recommended Duration**: 45–60 min, weekly or bi-weekly

### Agenda Template
```
Backlog Refinement | [Date]
Attendees: Dev team, PM, optionally Design

[5 min] Housekeeping
  - Review items from last refinement still needing work
  - Note any urgent stories that jumped the queue

[40 min] Story Review (work through backlog top-down)
  Per story:
  - PM reads story title and description
  - Team asks clarifying questions
  - Review / finalize acceptance criteria
  - Estimate (Planning Poker or T-shirt)
  - Flag blockers or dependencies
  - Mark "Ready" or add follow-up tasks

[10 min] Prioritization Check
  - Does the backlog order still reflect current priorities?
  - Any new stories to add based on recent decisions?

[5 min] Wrap Up
  - Confirm which stories are sprint-ready
  - Note any stories needing more info before next refinement
```

### Refinement Health Checklist
- [ ] Top 2 sprints of work are estimated
- [ ] Every "Ready" story has clear acceptance criteria
- [ ] No story in the top 10 is blocked
- [ ] Designs are available for UI stories
- [ ] Stories are sized ≤ 8 points (13+ = needs splitting)

---

## Retrospective

**Goal**: Inspect the last sprint and identify one meaningful improvement.

**Recommended Duration**: 60–90 min for a 2-week sprint

### Format Options

#### Mad / Sad / Glad (Default)
```
Categories:
  😡 Mad    — What frustrated us or slowed us down?
  😢 Sad    — What didn't go as hoped?
  😄 Glad   — What went well and should continue?

Process:
  1. Silent brainstorm (5 min) — everyone writes stickies
  2. Read aloud & group (10 min)
  3. Dot vote top themes (5 min)
  4. Discuss top 2–3 themes (20 min)
  5. Action items: 1–3 specific, owned actions (10 min)
```

#### Start / Stop / Continue
```
  Start  — Things we should begin doing
  Stop   — Things that aren't working, eliminate
  Continue — Things working well, protect them
```

#### 5 Whys (for deep-diving a recurring problem)
```
  State the problem clearly
  Ask "Why did this happen?" → answer
  Ask "Why?" again → go 5 levels deep
  Root cause = actionable improvement
```

#### 4Ls (Learning-focused)
```
  Liked     — What did we enjoy?
  Learned   — What did we discover?
  Lacked    — What was missing?
  Longed For — What do we wish we had?
```

### Action Item Template
```
Action: [Specific change to make]
Owner: [Named person, not "the team"]
By When: [Date, ideally before next retro]
How We'll Know: [Observable outcome]
```

### PM Facilitation Tips
- Start retros by reading last sprint's action items — did we follow through?
- Timebox discussion; don't let one item eat the whole retro
- Aim for 1–3 high-quality action items, not a laundry list
- Rotate formats to keep retros fresh
- Psychological safety: frame everything as systemic, not personal

---

## Daily Standup

**Goal**: 15-minute sync to surface blockers and coordinate — NOT a status report to the PM.

### Format
```
Each person answers:
1. What did I complete yesterday?
2. What am I working on today?
3. Is anything blocking me?

Parking Lot: Anything needing deeper discussion → take it offline
```

### PM Role in Standup
- Listen for blockers you can help unblock (stakeholders, decisions, dependencies)
- Note velocity signals — are things taking longer than estimated?
- Don't turn standup into a requirements discussion
- If you're speaking more than 10% of the time, you're doing it wrong

---

## Sprint Review / Demo

**Goal**: Showcase completed work to stakeholders and gather feedback.

**Recommended Duration**: 30–60 min

### Agenda Template
```
Sprint Review — Sprint [#] | [Date]
Attendees: Team, stakeholders, product leadership

[5 min] Sprint Summary
  - Sprint goal: did we achieve it? (Yes / Partial / No)
  - Stories completed vs. committed
  - Velocity: [points completed] / [points committed]

[30–40 min] Demos
  Per feature/story:
  - Context: why did we build this?
  - Demo: show working software (not slides)
  - Outcome: how does this move the needle?

[10 min] Stakeholder Q&A + Feedback
  - Open floor for questions
  - Capture feedback → feed into backlog

[5 min] What's Next
  - Preview next sprint priorities
  - Any upcoming milestones or decisions needed
```

### Demo Best Practices
- Demo in production or staging — never in local environments
- Show the user journey, not the code
- Lead with the problem solved, then show the solution
- Have a backup (screenshots/video) in case of live demo failures

---

## Quick Reference: Ceremony Cadence

| Ceremony | When | Duration | Who |
|----------|------|----------|-----|
| Sprint Planning | Sprint Day 1 | 1hr/sprint week | Full team |
| Daily Standup | Every day | 15 min | Dev team + PM |
| Refinement | Mid-sprint | 45–60 min | Dev team + PM |
| Retrospective | Sprint last day | 60–90 min | Dev team + PM |
| Sprint Review | Sprint last day | 30–60 min | Team + stakeholders |
