---
name: ux-researcher
description: >
  Plan, conduct, and synthesize user research. Use this skill when the user asks
  for an interview guide, a usability test plan, a research synthesis, persona
  development, a journey map, or an analysis of user feedback. Also trigger when
  the user says things like "help me understand what users need", "synthesize
  these interviews", "write a discussion guide", "map the user journey", "create
  a persona", or "what did users say about X". Works from raw notes, transcripts,
  or a feature brief.
---

# UX Researcher Skill

Plan rigorous user research, synthesize findings into actionable insights, and
translate user evidence into product decisions.

## When to Use
- Before writing a PRD — to validate the problem and understand the user
- After a discovery sprint — to synthesize interview notes into themes
- Before a redesign — to map the current journey and identify friction
- When qualitative feedback is piling up and needs structure
- When the team disagrees about what users want — research resolves opinion with evidence

---

## Research Methods

Choose the right method for the question:

| Question type | Best method |
|--------------|------------|
| What problems do users have? | Discovery interviews |
| Can users complete this task? | Usability test |
| Why are users churning? | Exit interviews + behavioral data |
| What do users think of this concept? | Concept test / prototype test |
| How do users think about this domain? | Card sort / mental model interview |
| What's the full experience across touchpoints? | Journey mapping |

---

## Output Formats

### 1. Research Plan
When the user needs to plan a study before conducting it.

```
# Research Plan: [Study Name]

## Research Question
[The one question this study will answer. Not multiple questions — one.]

## Method
[Why this method fits this question]

## Participants
- **Who**: [Role, company type, usage pattern]
- **How many**: [N — typically 5-8 for qualitative; explain the rationale]
- **Recruiting criteria**: [Inclusion / exclusion criteria]
- **How to find them**: [Panel, CSM referrals, in-app intercept, etc.]

## Session Design
- **Format**: [Moderated remote / Moderated in-person / Unmoderated]
- **Duration**: [X minutes]
- **Recording**: [With consent — what will be recorded]
- **Incentive**: [Amount and type]

## Timeline
| Milestone | Date |
|-----------|------|
| Recruiting complete | [date] |
| Sessions run | [date range] |
| Synthesis complete | [date] |
| Readout to team | [date] |

## Success Criteria
[How will we know the research answered the question?]
```

### 2. Discussion Guide
A structured interview or usability test script.

```
# Discussion Guide: [Study Name]

**Session length**: [X minutes]
**Moderator**: [Name or TBD]
**Observer notes**: [What to capture]

---

## Introduction (5 min)
[Script — introduce yourself, explain purpose, get consent, set expectations]
"Thanks for joining. I'm [name], a [researcher / PM] at [company]. 
We're spending [X] minutes today to understand [topic — not the solution].
There are no right or wrong answers — I'm here to learn from you.
With your permission, I'd like to record this session. Is that okay?"

## Warm-up (5 min)
[Background questions — role, team size, tools, relevant context]
- "Tell me about your role and what a typical week looks like."
- "How do you currently [relevant workflow]?"
- "What tools do you use for [topic]?"

## Core Questions ([X] min)
[The main research questions — open-ended, non-leading]
- "Walk me through the last time you [key task]. Start from the beginning."
- "What was the hardest part of that?"
- "What did you do when [problem scenario]?"
- "How does that make you feel?"
- "If you could change one thing about how you [task], what would it be?"

[For usability tests, replace core questions with tasks:]
- "Without me helping, please [task description]. Talk me through what you're thinking."

## Closing (5 min)
- "Is there anything about [topic] we haven't covered that you think is important?"
- "If you could wave a magic wand and change one thing, what would it be?"
- "Is there anyone else you think I should talk to?"

---

Moderator notes:
- Don't explain; ask "what would you expect to happen?"
- If participant goes off-topic, redirect: "That's helpful — let me ask you about..."
- Silence is okay. Count to 5 before filling it.
```

### 3. Research Synthesis
When notes or transcripts exist and need to be turned into insights.

```
# Research Synthesis: [Study Name]

**Sessions completed**: [N]
**Date range**: [start – end]
**Synthesized by**: [name]

---

## Key Findings

[3-7 findings. Each is a complete sentence — a claim, not a topic.
Supported by at least 2 participants unless flagged as notable outlier.]

### Finding 1: [Headline — the insight, not the observation]
**Evidence**: 
- [P1]: "[Quote or paraphrased observation]"
- [P2]: "[Quote]"
- [P3]: "[Observation]"

**Implication**: [What this means for the product — specific, not vague]

[Repeat for each finding]

---

## Jobs to Be Done

| When... | I want to... | So I can... |
|---------|-------------|------------|
| [situation] | [motivation] | [outcome] |

---

## Pain Points (ranked by frequency × intensity)

| Pain | Frequency | Intensity | Workaround users have today |
|------|-----------|-----------|----------------------------|
| [pain] | [N/N participants] | High/Med/Low | [how they cope] |

---

## Opportunities

[From the pains and JTBD, what are the product opportunities?]

1. **[Opportunity]**: [1-2 sentences — what to solve and for whom]
   - Evidence: [findings that support this]
   - Size: [how many participants experienced this]

---

## Surprising or Contradictory Findings

[Anything that contradicts existing assumptions or prior research]

---

## What We Still Don't Know

[Open questions the research didn't answer — candidates for follow-on studies]
```

### 4. Persona
A research-grounded user archetype (not a fictional composite).

```
# Persona: [Name]

**Based on**: [N interviews, [date range]]
**Represents**: [% or type of user base this archetype covers]

---

[Name], [Title]
[Company type, size, context]

"[A quote that captures their worldview or primary frustration — verbatim from research]"

---

## Context
[2-3 sentences on their day-to-day and how [product domain] fits into their work]

## Goals
- [Primary goal — what they're ultimately trying to achieve]
- [Secondary goal]

## Frustrations
- [Specific frustration — observed in research, not assumed]
- [Specific frustration]

## Current tools / workaround
[What they use today and why it's imperfect]

## What "good" looks like to them
[What they'd consider a great experience — in their words]

## What they don't care about
[Things that sound appealing to us but aren't priorities for them]
```

### 5. Journey Map
Maps the current (or ideal) experience across touchpoints.

```
# Journey Map: [Scenario Name]

**Actor**: [Persona name]
**Scenario**: [What they're trying to accomplish]
**Scope**: [Start point → end point]

---

| Stage | [Stage 1] | [Stage 2] | [Stage 3] | [Stage 4] |
|-------|----------|----------|----------|----------|
| **Actions** | [What they do] | | | |
| **Thoughts** | [What they're thinking] | | | |
| **Feelings** | [Emotion] | | | |
| **Pain points** | [Friction] | | | |
| **Opportunities** | [Where we can improve] | | | |

---

## Moments That Matter

[2-3 highest-impact moments — positive or negative — with specific product implications]

## Biggest Drop-off Points

[Where users abandon, give up, or switch to a workaround — with evidence]
```

### 6. Usability Findings Report
Summary of what users could and couldn't do in a usability test.

```
# Usability Findings: [Feature / Flow Tested]

**Sessions**: [N]
**Prototype / version tested**: [link or description]
**Date**: [date]

---

## Task Completion Rates

| Task | Completed | With difficulty | Failed | Avg time |
|------|-----------|----------------|--------|---------|
| [task] | [N/N] | [N/N] | [N/N] | [Xs] |

---

## Critical Issues (P0 — must fix before launch)

### Issue 1: [Title]
- **Observed**: [What happened — specific]
- **Frequency**: [N/N participants]
- **Quote**: "[Verbatim participant quote]"
- **Recommendation**: [Specific design change]

---

## Major Issues (P1 — fix before launch if possible)

[Same structure]

---

## Minor Issues (P2 — address in a follow-up)

[Summarized as a list]

---

## What Worked Well

[Positive findings — elements to preserve in future iterations]

---

## Recommended Changes (prioritized)

| Priority | Change | Rationale |
|---------|--------|-----------|
| P0 | [specific change] | [evidence] |
```

---

## Output Guidelines

- **Evidence over assertion** — every finding must have at least 2 supporting data points or be flagged as a single observation
- **Insights, not observations** — "Users were confused by the navigation" is an observation. "Users can't find the settings because they expect it under their avatar, not the main nav" is an insight
- **Specific quotes** — verbatim quotes are more persuasive than paraphrases; use them
- **Quantify where possible** — "7 of 8 participants" is stronger than "most participants"
- **Flag small n** — if a finding comes from fewer than 3 participants, say so and caveat accordingly

## Integration Points

- Feed synthesis into the **prd** skill — opportunities map directly to requirements
- Use **opportunity-solution-tree** framework to structure the opportunities from research
- Use **kano-model** framework to classify findings (basic needs vs. delighters)
- The `pdlc_orchestrator.py` runs UX research as stage 3 — between discovery and PRD
