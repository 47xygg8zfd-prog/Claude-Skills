# Workflow: Incident & Risk Communication

How to handle a launch risk, production incident, or project delay — from detection to stakeholder communication.

---

## Overview

```
Something goes wrong
        ↓
Tech Translation (understand what happened)
        ↓
Data Queries (measure the impact)
        ↓
Stakeholder Updates (escalation memo + status update)
        ↓
Release Notes (post-incident summary, if customer-facing)
        ↓
Agile Ceremonies (retro to prevent recurrence)
```

---

## Step 1: Understand the Technical Situation

**Skill**: `tech-translation`  
**Use when**: Engineers are describing the incident and you need to understand severity, scope, and root cause well enough to communicate it upward.

**Prompt to start**:
```
Translate this incident description for me. I need to understand:
1. What broke and why (plain English)
2. Who is affected and how
3. How severe is this (data loss? downtime? degraded experience?)
4. What is the fix and how long will it take?
Incident description: "[paste engineer's Slack message or incident report]"
```

**What you need before escalating**: blast radius (how many customers?), severity (is data at risk?), ETA to resolution, and whether it's still ongoing.

---

## Step 2: Measure the Impact

**Skill**: `data-queries`  
**Use when**: You need to quantify how many users or accounts were affected.

**Prompt to start**:
```
Write a Snowflake query to find accounts affected by [incident].
Definition of affected: [e.g. users who saw a 0 value for collaboration_score between 2026-05-01 and 2026-05-08]
Tables: [list relevant tables]
Output: account_id, account_name, plan_tier, affected_user_count
```

**Why this matters**: Stakeholders will ask "how many customers were affected?" Have the number before the call, not after.

---

## Step 3: Escalation Memo (if needed)

**Skill**: `stakeholder-updates` → Mode 2: Escalation Memo  
**Use when**: The incident requires a decision, additional resources, or executive awareness.

**Prompt to start**:
```
Write an escalation memo for this incident.
What happened: [summary from Step 1]
Customer impact: [numbers from Step 2]
Current status: [resolved / ongoing / mitigated]
Decision needed: [e.g. approve customer credits, delay launch, pull eng from other work]
Options: [2-3 paths with tradeoffs]
Recommendation: [your preferred path]
Decision needed by: [time]
```

---

## Step 4: Delay or Risk Notification

**Skill**: `stakeholder-updates` → Mode 3: Delay/Risk Notification  
**Use when**: The incident will cause a launch delay or miss a committed milestone.

**Prompt to start**:
```
Write a delay notification for [feature/launch].
Original date: [date]
New expected date: [date or range]
Root cause: [brief, factual]
What we're doing to recover: [concrete actions]
Ask (if any): [resource, decision, or approval needed]
Tone: transparent and forward-looking.
```

---

## Step 5: Customer-Facing Communication (if needed)

**Skill**: `release-notes` → End-User Format  
**Use when**: The incident was customer-visible and needs a public post-incident summary.

**Prompt to start**:
```
Write a customer-facing post-incident summary.
What happened: [plain English, no jargon]
Who was affected: [segment, not account names]
Duration: [start to resolution time]
What we did: [actions taken]
What we've changed to prevent recurrence: [if applicable]
Tone: honest, accountable, no defensive language.
```

---

## Step 6: Retrospective

**Skill**: `agile-ceremonies` → Retro format  
**Use when**: After the dust settles, the team needs to understand what went wrong and prevent recurrence.

**Prompt to start**:
```
Run a post-incident retrospective for [incident name].
What happened: [brief summary]
Timeline: [key events and when they occurred]
Team involved: [roles, not names]
Format: Start/Stop/Continue + action items with owners and due dates.
Focus on process and systems, not blame.
```

---

## Tips

- **Don't estimate impact before querying it.** "A few hundred users" in an escalation memo that turns out to be 4,000 destroys credibility. Run the query first (Step 2), even if it takes 10 minutes.
- **Separate the update from the ask.** A status update tells people what's happening. An escalation memo asks for a decision. Don't mix them — escalations need a clear call to action.
- **Time-box the retro.** Run it within 5 business days of resolution, while context is fresh. Retros that happen 3 weeks later produce generic action items.
- **Close the loop with CS.** After any customer-visible incident, CS needs talking points before customers call in. A quick Slack message with the plain-English summary (from Step 5) is enough.
