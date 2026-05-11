---
name: agile-stories
description: >
  Draft well-formed agile user stories, epics, tasks, and acceptance criteria following best practices.
  Use this skill whenever the user asks to write stories, epics, tickets, backlog items, or acceptance
  criteria. Also trigger for phrases like "break this down into stories", "create tickets for this",
  "write up the AC", "help me groom this", or "split this epic". Produces dev-ready stories with
  clear structure that engineers and QA can act on immediately.
---

# Agile Stories & Epics Skill

Draft clear, actionable agile artifacts: epics, stories, tasks, and acceptance criteria.

## Hierarchy

```
Initiative (Strategic goal, multi-quarter)
  └── Epic (Large feature or capability, 1–2 sprints+)
        └── Story (User-facing slice of value, fits in 1 sprint)
              └── Task (Technical sub-task, assigned to individual)
```

---

## Epic Template

```
Epic: [Epic Name]
Goal: [One sentence — what capability does this unlock?]
Why Now: [Business or user driver]
Success Metric: [How will we know this epic is done and successful?]
Estimated Size: [T-shirt: S / M / L / XL]
Dependencies: [Other epics, teams, or systems]
Stories Included: [List story titles or IDs]
```

**Epic writing tips:**
- An epic should represent a complete capability, not a project phase
- Name epics from the user's perspective when possible ("User can manage notifications" not "Notification System Refactor")
- Every epic needs a measurable success metric

---

## Story Template

```
Story ID: [e.g., PROJ-123]
Title: As a [persona], I want to [action], so that [benefit]
Epic: [Parent epic]
Priority: P0 / P1 / P2 / P3
Story Points: [1 / 2 / 3 / 5 / 8 / 13]
Sprint: [Target sprint if known]

Description:
[2–4 sentences expanding on the user need and context. What problem does this solve?]

Acceptance Criteria:
Given [context/precondition]
When [user action]
Then [expected outcome]
(Repeat for each scenario)

Out of Scope:
- [Explicit exclusions to prevent scope creep]

Technical Notes:
- [Any known implementation hints, API endpoints, or constraints]
- [Edge cases engineering should be aware of]

Dependencies:
- [Blocked by / blocks]

Definition of Done:
- [ ] Code reviewed and merged
- [ ] Unit tests written and passing
- [ ] AC verified by QA
- [ ] Feature flagged if needed
- [ ] Docs updated if applicable
```

---

## Story Pointing Guide

| Points | Complexity | Time Estimate |
|--------|-----------|---------------|
| 1 | Trivial — no unknowns, < 2 hours | < half day |
| 2 | Simple — clear path, minimal risk | ~1 day |
| 3 | Moderate — some unknowns | 1–2 days |
| 5 | Complex — multiple components | 2–3 days |
| 8 | High complexity — significant unknowns | 3–5 days |
| 13 | Too big — split this story | > 1 sprint |

If a story is 13 points, always suggest how to split it.

---

## Acceptance Criteria Patterns

Use **Given/When/Then** (Gherkin) format for precision:

```
Given I am a logged-in user with an active subscription
When I click "Export Report"
Then a CSV file downloads within 5 seconds
And the file contains all records from the selected date range

Given the export fails
When the system encounters an error
Then I see an error message with a retry option
And the error is logged for debugging
```

**Tips:**
- Write AC before writing the story body — it clarifies scope
- Each AC scenario should be independently testable
- Include happy path, edge cases, and error states
- Avoid vague language: "fast" → "within 3 seconds"; "correctly" → describe exactly what correct means

---

## Story Splitting Patterns

When a story is too large, split by:
1. **Workflow steps** — break the user journey into steps
2. **Data variations** — handle one data type per story
3. **User roles** — one story per persona
4. **Happy path first** — then edge cases in follow-on stories
5. **CRUD operations** — Create, Read, Update, Delete as separate stories
6. **Frontend / Backend** — with clear interface contracts

---

## Output Modes

| User says | Output |
|-----------|--------|
| "Write stories for [feature]" | 3–8 stories with full templates |
| "Break down this epic" | Epic template + story list |
| "Write AC for this story" | Given/When/Then scenarios only |
| "Is this story too big?" | Size assessment + split suggestions |
| "Groom this backlog item" | Rewrite with improvements + questions |

---

## Integration Points
- Use **prd** skill upstream to get requirements before breaking into stories
- Use **agile-ceremonies** skill for refinement session facilitation
