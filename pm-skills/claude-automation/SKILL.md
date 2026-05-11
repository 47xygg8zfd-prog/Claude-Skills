---
name: claude-automation
description: >
  Help PMs scope, design, and collaborate with engineering on Claude-powered automations, skills,
  and agents. Use this skill whenever the user wants to automate a PM workflow using AI, build a
  Claude skill, design an agent, evaluate whether a task is a good automation candidate, write a
  prompt for an internal tool, or work with engineering to ship an AI-powered feature. Also trigger
  for phrases like "automate this with Claude", "build a skill for", "create an agent to", "is this
  a good use case for AI", "help me scope an LLM feature", "write a system prompt for", "prompt
  engineering for our tool", or "work with eng on an AI automation". Produces automation scoping
  docs, prompt drafts, skill specs, and agent architecture guidance.
---

# Claude Automation Skill

Help PMs identify, scope, and collaborate on Claude-powered automations, skills, and agents.

---

## Your Role as PM in AI Automation

You don't need to write code. Your job is to:
1. **Identify** which workflows are worth automating
2. **Scope** what the automation should do (and not do)
3. **Define success** — how will you know it's working?
4. **Write or review the prompt** — the core of any Claude integration
5. **Partner with engineering** — hand off a clear spec, not just a vague idea

---

## Step 1: Is This a Good Automation Candidate?

Use this checklist before investing engineering time:

### ✅ Good Candidates
- [ ] Task is **repetitive** — done >3x per week
- [ ] Task has a **clear input and output** (not open-ended judgment)
- [ ] **Errors are recoverable** — a bad output can be reviewed/corrected before action
- [ ] **Context fits in a prompt** — input data is <50k tokens
- [ ] **Speed matters** — humans take 10+ minutes, Claude takes seconds
- [ ] **Quality bar is clear** — you can define what "good" looks like

### ⚠️ Proceed with Caution
- [ ] Task requires real-time data (needs tool use or RAG)
- [ ] Output has **legal or compliance implications** — needs human review gate
- [ ] Task requires **nuanced judgment** — Claude's output may need significant editing
- [ ] Task involves **PII** — confirm data handling policy with Legal/Security

### 🚫 Not Good Candidates (yet)
- Task requires access to systems Claude can't connect to without complex tooling
- Task needs guaranteed 100% accuracy (e.g., financial calculations, medical dosing)
- Task is extremely infrequent and low value

---

## Step 2: Automation Types (Pick One)

| Type | What It Is | PM Example |
|------|-----------|------------|
| **Skill** | Reusable instructions Claude consults when a topic comes up | PRD writing template, story format |
| **Inline Prompt** | One-off prompt in a tool or workflow | "Summarize this Slack thread" button |
| **Agent (single-step)** | Claude takes a specific action | Draft and send sprint summary email |
| **Agent (multi-step)** | Claude completes a workflow with multiple steps | Read Jira → write retro summary → post to Confluence |
| **RAG Pipeline** | Claude answers questions grounded in your docs | "Ask your Notion docs" chatbot |

---

## Step 3: Write the Scope Document

Before handing off to engineering, write a 1-page scope doc. Template:

```
AUTOMATION SCOPE: [Name]
───────────────────────────────
PROBLEM
What manual task are we automating? How often? Who does it?

TRIGGER
When does this automation run?
  □ User clicks a button
  □ Scheduled (how often?)
  □ Event-based (which event?)

INPUT
What data does Claude receive?
  - Source: [Jira / Slack / Snowflake / manual paste / etc.]
  - Format: [text, JSON, table, etc.]
  - Size: [estimated tokens / records]

OUTPUT
What should Claude produce?
  - Format: [paragraph, JSON, table, Markdown, etc.]
  - Destination: [Confluence, Jira, Slack, email, UI display]
  - Review gate: [auto-post vs. human-reviews-first]

SUCCESS CRITERIA
How will we measure if this is working?
  - Quality metric: [e.g., "PM edits <20% of output"]
  - Volume metric: [e.g., "saves 2 hrs/week"]
  - Accuracy: [e.g., ">90% of outputs are usable without edits"]

FAILURE MODE HANDLING
What happens if Claude's output is wrong?
  - Who reviews before publishing?
  - Is there a rollback / edit flow?

CONSTRAINTS
  - Data sensitivity: [PII / confidential / public]
  - Latency requirement: [<5 sec / async OK]
  - Cost tolerance: [# of API calls per day/week]

ENGINEERING ASKS
  - Estimated complexity: [S / M / L / XL]
  - Dependencies: [MCP servers, data access, UI changes]
```

---

## Step 4: Write the Prompt

The prompt is the product. A good prompt has:

### Prompt Anatomy

```
[SYSTEM — who Claude is and what it does]
You are a PM assistant for [Team Name]. You help draft [output type].
Your outputs are used by [audience] for [purpose].
Always follow [style / format constraints].

[CONTEXT — what Claude needs to know]
<team_context>
Team: [name], using [tools], working on [product area].
Sprint length: [X weeks]. Story point scale: [Fibonacci].
</team_context>

[TASK — what to produce]
Given the following [input], produce a [output format].

Requirements:
- [Specific constraint 1]
- [Specific constraint 2]
- Format output as [Markdown table / JSON / bullet list]

[INPUT — the data]
<input>
{{user_provided_data}}
</input>

[OUTPUT FORMAT — exactly what you expect]
Respond only with [format]. Do not include preamble or explanation.
```

### Prompt Writing Tips for PMs

**Be specific about format** — "a table with columns: Story, AC, Points" beats "a table"

**Give examples** — show Claude one or two examples of good output before the task

**Define the negative space** — "Do NOT include implementation details. Do NOT exceed 3 acceptance criteria per story."

**Set the persona** — "You are a senior PM at a B2B SaaS company" improves tone

**Temperature intuition**:
- Low (0.2–0.5): Structured outputs, JSON, SQL, templates
- Medium (0.7): PRDs, stories, analysis
- High (1.0+): Brainstorming, creative alternatives

---

## Step 5: Test Your Prompt

Before engineering builds around it, test manually:

### Prompt Testing Checklist
- [ ] Does it produce the right format consistently?
- [ ] Does it handle edge cases (empty input, unusual data)?
- [ ] Does it stay in scope? (doesn't add unrequested info)
- [ ] Does it fail gracefully? (asks for clarification vs. hallucinating)
- [ ] Is the output length appropriate?
- [ ] Test with 5–10 real examples before calling it done

### Red Flags in Prompt Output
| Problem | Fix |
|---------|-----|
| Makes up data | Add: "Only use information in the provided input. Do not infer." |
| Too long / verbose | Add: "Be concise. Max [N] sentences per section." |
| Wrong format | Add a concrete output example in the prompt |
| Inconsistent | Lower temperature; add format constraints |
| Misses edge cases | Add explicit handling: "If input is empty, respond with..." |

---

## Common PM Automations (Starter Prompts)

### Sprint Summary Generator
```
You are a PM assistant. Given a list of completed Jira stories, write a sprint summary
for stakeholders.

Format:
## Sprint [N] Summary — [Date]
**Sprint Goal**: [state the goal if provided, otherwise omit]
**Completed**: [X stories, Y points]

### What We Shipped
[3–5 bullets, each: feature name — one sentence on user/business impact]

### Carried Over
[bullet list, with reason if known]

### Metrics to Watch
[any KPIs or signals to look for post-launch]

Input stories:
{{jira_stories_json}}
```

### Story Drafting from Notes
```
You are a PM assistant. Convert the following meeting notes or feature idea into
well-formed agile user stories.

For each story, output:
- Title: As a [persona], I want to [action] so that [benefit]
- Acceptance Criteria (3–5 Given/When/Then scenarios)
- Story Points estimate (1/2/3/5/8)
- Out of scope (1–2 items)

Input notes:
{{raw_notes}}
```

### PRD First Draft
```
You are an experienced product manager. Based on the following problem description,
draft a PRD skeleton.

Include: Problem Statement, Goals, Success Metrics, Non-Goals, High-level Requirements
(MoSCoW), Open Questions.

Mark any section where you need more input as [NEEDS INPUT: specific question].

Problem description:
{{problem_description}}
```

### Retro Action Item Tracker
```
You are a PM assistant. Given the following retro notes, extract and format action items.

Output a Markdown table with columns: Action | Owner | Due Date | Category
Category options: Process, Technical, Communication, Team Health

If owner or due date is not mentioned, use "[UNASSIGNED]" and "[TBD]" respectively.

Retro notes:
{{retro_notes}}
```

---

## Engineering Collaboration Guide

### How to Hand Off an Automation to Eng

1. **Share the scope doc** (Step 3 above)
2. **Include your tested prompt** — don't just describe it, give them the actual text
3. **Define the API contract** — what data comes in, what comes out
4. **Agree on the review gate** — is this auto-publish or human-in-the-loop?
5. **Define rollout plan** — internal test → pilot users → full rollout

### Questions to Ask Engineering
- "What MCP servers do we need for this to access [Jira / Confluence / Slack]?"
- "Can we log inputs/outputs so I can review quality?"
- "What does the error state look like to the user?"
- "How do we update the prompt without a code deploy?"
- "What's the latency budget?"

### Red Flags from Engineering
- "We'll just have it do X automatically" — ask: what's the review gate?
- "The prompt is in the code, we'll update it when needed" — push for prompt management
- "It's just a Claude API call, it'll be done in a day" — prompt testing and edge cases take time

---

## MCP Servers (Common for PM Automations)

| Service | Use Case |
|---------|---------|
| Jira MCP | Read/write stories, update sprint |
| Confluence MCP | Post retro summaries, update docs |
| Slack MCP | Post sprint summaries, daily digests |
| Google Drive / Notion | Retrieve context documents for RAG |
| Snowflake | Query metrics for automated reports |
| GitHub | Summarize PRs, read changelogs |

---

## Integration Points
- Use **prd** skill to write the full product spec for a Claude automation feature
- Use **agile-stories** skill to break the automation into dev-ready stories for engineering
- Use **data-queries** skill to define what Snowflake data the automation needs
- Use **tech-translation** skill to understand the engineering architecture choices
