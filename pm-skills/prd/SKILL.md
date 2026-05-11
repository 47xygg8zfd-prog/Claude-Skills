---
name: prd
description: >
  Generate, structure, and refine Product Requirements Documents (PRDs) following PM best practices.
  Use this skill whenever the user mentions writing a PRD, product spec, requirements doc, feature brief,
  or asks to document a product initiative, new feature, or problem statement. Also trigger when the user
  says things like "help me write up this feature", "I need to spec this out", or "document the requirements
  for X". Produces a complete, stakeholder-ready PRD with all standard sections.
---

# PRD Skill

Produce clear, complete, stakeholder-ready Product Requirements Documents.

## When to Use
- User asks for a PRD, product spec, feature brief, or requirements doc
- User wants to "write up" or "spec out" a feature or initiative
- User has a rough idea and needs it structured for engineering and stakeholders

## PRD Structure

Always produce PRDs with these sections in order:

### 1. Header Block
```
Product: [Product/Feature Name]
Author: [PM Name if provided]
Status: Draft | In Review | Approved
Last Updated: [Date]
Stakeholders: [List if provided]
```

### 2. Problem Statement
- What problem are we solving?
- Who is affected (user persona / customer segment)?
- What is the impact of NOT solving this?

### 3. Goals & Success Metrics
- **Goals**: 2–4 specific, outcome-oriented goals
- **Success Metrics**: Quantifiable KPIs (e.g., "Reduce churn by 10% in 90 days")
- **Non-Goals**: Explicitly state what this PRD does NOT cover

### 4. Background & Context
- How did we get here? (data, research, customer feedback, exec ask)
- Related prior work or dependencies
- Assumptions being made

### 5. User Stories (Summary)
- List 3–6 high-level user stories in "As a [user], I want to [action], so that [benefit]" format
- Reference the agile-stories skill for detailed story breakdown

### 6. Requirements
Break into:
- **Functional Requirements** — what the system must do
- **Non-Functional Requirements** — performance, security, scalability
- **Out of Scope** — explicit exclusions

Use MoSCoW prioritization: Must Have / Should Have / Could Have / Won't Have

### 7. Design & UX Considerations
- Link to designs if available
- Key UX principles or constraints
- Accessibility requirements

### 8. Technical Considerations
- Known technical constraints or dependencies
- Integration points (APIs, services, data)
- Flag items to validate with engineering

### 9. Risks & Mitigations
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| ...  | High/Med/Low | High/Med/Low | ... |

### 10. Timeline & Milestones
- Target launch date (if known)
- Key milestones (design complete, eng kickoff, beta, GA)
- Dependencies on other teams

### 11. Open Questions
- Numbered list of unresolved decisions
- Owner and target resolution date for each

### 12. Appendix (optional)
- Research links, data sources, customer quotes

---

## Output Guidelines

- **Tone**: Clear, direct, professional — no fluff
- **Length**: As long as needed, but every section should earn its place
- **Formatting**: Use tables for comparisons/risks, bullets for requirements, headers for navigation
- **If information is missing**: Fill what you can, clearly mark `[TBD]` or `[NEEDS INPUT]` for gaps
- **Ask before writing** if the problem statement is unclear — a bad PRD starts with a vague problem

## Quick Mode

If the user provides minimal context, produce a "Starter PRD" with the skeleton filled in as far as possible, then list the top 5 questions to complete it.

## Integration Points

- After PRD is drafted, suggest using **agile-stories** skill to break requirements into stories/epics
- For slide version, suggest using the **pptx** skill to turn the PRD into an exec-ready deck
- For Word doc output, suggest using the **docx** skill
