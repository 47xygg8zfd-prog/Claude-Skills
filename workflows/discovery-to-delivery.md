# Workflow: Discovery to Delivery

How to chain PM skills from raw customer insight through to a shipped feature.

---

## Overview

```
Customer Research Synthesis
        ↓
Feature Prioritization
        ↓
      PRD
        ↓
  Agile Stories
        ↓
Agile Ceremonies (Sprint Planning)
        ↓
   Monte Carlo
        ↓
  Tech Translation  ←→  Data Queries
        ↓
  Release Notes
        ↓
Stakeholder Updates
```

---

## Step 1: Customer Research Synthesis

**Skill**: `customer-research-synthesis`  
**Input**: Interview notes, survey responses, support tickets, NPS comments  
**Output**: Themes, JTBD statements, opportunity statements

**Prompt to start**:
```
Synthesize these [N] customer interviews about [topic].
Research goal: [what question you were investigating]
Segment: [who you talked to]
[Paste notes]
```

**What to take to the next step**: The top 2-3 opportunity statements. These become the "Problem Statement" in your PRD and the justification for prioritization.

---

## Step 2: Feature Prioritization

**Skill**: `feature-prioritization`  
**Input**: List of candidate features, opportunity statements from Step 1  
**Output**: RICE-ranked feature list with rationale

**Prompt to start**:
```
Prioritize these features for [quarter] using RICE.
Context: Our primary OKR is [OKR]. Our team velocity is ~[N] points/sprint.
Features:
1. [Feature]
2. [Feature]
...
```

**What to take to the next step**: The #1 or #2 ranked feature. That's your PRD subject.

---

## Step 3: PRD

**Skill**: `prd`  
**Input**: Opportunity statement (Step 1), prioritization rationale (Step 2)  
**Output**: Full PRD with problem, goals, user stories, success metrics, open questions

**Prompt to start**:
```
Write a PRD for [feature name].
Problem: [paste opportunity statement from Step 1]
Goals: tie to [paste relevant OKR KRs]
Constraints: [team size, timeline, dependencies]
```

**What to take to the next step**: User stories and success metrics sections. Stories feed directly into agile ticketing; metrics define your data queries later.

---

## Step 4: Agile Stories

**Skill**: `agile-stories`  
**Input**: PRD user stories section, non-goals, dependencies  
**Output**: Sprint-ready tickets with AC and story points

**Prompt to start**:
```
Break this PRD into sprint-ready tickets.
[Paste PRD user stories + non-goals + dependencies]
Team velocity: ~[N] points/sprint.
Flag anything that needs a spike before estimation.
```

**What to take to the next step**: The full ticket list with points. This feeds Monte Carlo and Sprint Planning.

---

## Step 5: Monte Carlo Forecast

**Skill**: `monte-carlo`  
**Input**: Total story points (Step 4), historical velocity (last 4 sprints), target date  
**Output**: Probability distribution of completion dates

**Prompt to start**:
```
Forecast delivery for [feature].
Remaining points: [N]
Historical velocity (last 4 sprints): [N, N, N, N]
Target date: [date]
Sprint length: [N] weeks
```

**What to take to the next step**: The 75% confidence date. Use this in your stakeholder update and sprint planning.

---

## Step 6: Sprint Planning (Agile Ceremonies)

**Skill**: `agile-ceremonies`  
**Input**: Ticket list (Step 4), capacity, forecast (Step 5)  
**Output**: Sprint goal, committed scope, risks

**Prompt to start**:
```
Run sprint planning for Sprint [N].
Goal: ship [milestone] toward [feature]
Velocity: ~[N] points. Capacity this sprint: [any absences?]
Tickets to pull from:
[Paste ticket list with points]
```

---

## Step 7: Tech Translation (ongoing during build)

**Skill**: `tech-translation`  
**Input**: Engineering terms, architecture decisions, tradeoff discussions  
**Output**: Plain-English explanations, questions to ask, decisions to surface

**Use this whenever**: Engineers say something in standup or Slack that you don't fully understand, or when you need to explain a technical constraint to a stakeholder.

---

## Step 8: Data Queries (post-launch measurement)

**Skill**: `data-queries`  
**Input**: Success metrics from PRD (Step 3)  
**Output**: Snowflake SQL and/or Splunk queries to measure them

**Prompt to start**:
```
Write Snowflake SQL to measure [metric] from the PRD.
Tables available: [list tables]
Definition: [how the metric is calculated]
Grain: [daily/weekly, by segment]
```

---

## Step 9: Release Notes

**Skill**: `release-notes`  
**Input**: Shipped tickets, PRD feature description  
**Output**: Audience-tailored release notes (users, eng, sales, exec)

**Prompt to start**:
```
Write release notes for [version/feature].
What shipped: [bullet list of tickets or features]
Audiences needed: [end users / internal / sales / exec]
Any bugs fixed: [list]
```

---

## Step 10: Stakeholder Update

**Skill**: `stakeholder-updates`  
**Input**: Launch status, metric results (Step 8), any blockers  
**Output**: Status update, or escalation memo if needed

**Prompt to start**:
```
Write a post-launch status update for [feature].
Status: [On Track / At Risk]
What shipped: [summary]
Early metrics: [any data from Step 8]
Next milestone: [what's next]
```

---

## Tips

- **Don't skip Step 1.** Features prioritized without customer evidence get deprioritized in the next cycle. Evidence from synthesis is your justification.
- **Loop back often.** After sprint planning, re-run Monte Carlo if scope changed. After launch, feed metric results back into the next prioritization cycle.
- **CLAUDE.md accelerates everything.** If you've filled in `CLAUDE.md` with your OKRs, team, and ICP, every prompt above gets shorter — Claude already has the context.
