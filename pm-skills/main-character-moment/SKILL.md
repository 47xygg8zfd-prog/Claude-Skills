---
name: main-character-moment
description: Finds concrete work wins in the user's recent Slack activity (their messages and threads, praise from others, huddle notes they're tagged in, canvases they've made), writes each one up in STAR format, and appends them to a running Slack canvas so the evidence still exists at review time. Pulls optional calendar and document context when connected. Use whenever the user mentions a wins log, brag doc, highlight reel, main character moment, tracking accomplishments, prepping for a performance review or self-assessment, building a promotion case, or updating a resume. Also use for retrospective asks like "what did I actually ship this quarter", even if they never name this skill.
---

# Skill: Main Character Moment

## Trigger Phrases
- "wins log"
- "brag doc"
- "what did I actually ship this quarter"
- "prep for my performance review"
- "build my promotion case"
- "track my accomplishments"
- "main character moment"
- "highlight reel for my self-assessment"

You did the thing. You unblocked the stuck project, you answered the question nobody else could, you quietly shipped the feature that was rotting in the backlog. Then you forgot all about it, and now it's review season and the only thing your brain will surrender is a vague memory of last Tuesday.

This skill goes back through Slack and finds the receipts.

It works in any role and any organisation. Nothing here assumes a particular team, tool stack, or job title.

## What it reads

**Slack. Always.** Everything runs through the Slack MCP, and Slack alone is enough for a full run. Look for the fingerprints the user left behind:

- Their own messages and the threads they were central to
- Mentions, reactions and outright praise. Someone else saying "this saved us" is the strongest evidence there is
- **Huddle notes the user is tagged in.** Gold. Huddles are where the actual decisions happen and the notes record who committed to what. Read them for what got decided and which bits landed on the user
- Canvases and files they created and shared

**Calendar. If it's connected.** Events with notes or a description attached get read for what was discussed, decided, or delivered.

**Documents. If they're connected.** Docs the user created and shared, read for what they've been building.

Calendar and docs are both optional garnish. If either isn't connected, or a lookup throws an error, skip it, note it in the footer, and carry on. A missing connector never blocks the run.

Only read what the user already has access to. This is their record of their work. No rifling through other people's material to pad the list out.

## Steps

### Phase 1 — Scope

This file is the skill **definition**. Instructions only. Never write logged wins into it.

Output lives in a separate running Slack canvas titled **Main Character Moments**. On the first run it won't exist yet, so create it with the Slack MCP's canvas creation tool (`slack_create_canvas`) and hang on to its file_id or link so every future run appends to the same place instead of scattering wins across a dozen orphan canvases.

Set the lookback window:

- Default to everything since the last dated section in the log canvas
- If the log is brand new, default to the last 2 weeks
- Only ask the user if they want a different window, or want to narrow to a specific project. Otherwise just go. Nobody needs a clarifying question about a thing they didn't ask for

### Phase 2 — Gather

Bulk searches, capped. Enough signal to write honestly, not a forensic audit of the user's entire Slack history.

- **Slack search.** Cap at around six searches covering distinct angles: shipped work, praise and reactions, problem-solving, leadership and initiative, cross-team help. Include a pass specifically for huddle notes the user is tagged in, since those tend to carry decisions that never made it into a channel
- **Calendar.** One pass over the window. Pull the text from events that have notes or a description. Events with nothing attached get skipped. Don't go fetching extra context for an empty meeting invite
- **Documents and canvases.** Find what the user created and shared in the window. Read the top few most relevant, around five. Not everything they've ever touched
- If a source isn't available, skip it and say so in the footer

### Phase 3 — Synthesize

Pick out **1 to 5 concrete wins**. Moments with real evidence behind them, not a shapeless fog of activity.

"Was across the migration" is not a win. "Traced the migration failure to an expired service token and had it moving again inside an hour" is a win. If it wouldn't survive being read aloud to a skeptical manager, it isn't one.

Write each in STAR format:

- **Situation.** The context or the problem
- **Task.** What needed to happen, and why it landed on the user
- **Action.** What the user specifically did. Not the team. "We" is worthless six months from now
- **Result.** The measurable or observable outcome

Tag each entry loosely with one or more of: Impact, Collaboration, Leadership, Initiative, Growth.

Link the source. Thread, huddle note, meeting, or doc. Future them will not remember, and a claim with a link attached is worth ten without.

Be honest about thin evidence. Either sharpen it by pulling one more piece of context, or flag it as "worth revisiting". Never inflate something to fill the page.

### Phase 4 — Output

Append a new dated section to the **Main Character Moments** canvas. Newest on top, directly under the title. Never overwrite what's already there. Never write output into this skill definition. Every run adds to the pile.

## Output format

```
## New Wins Logged — [Month Day, Year]

Sources checked: [Slack / huddle notes / calendar / shared documents — note anything skipped and why]

### [Short punchy title for the win] — [Tag(s)]
- Situation: [context/problem]
- Task: [what needed to happen, and why the user]
- Action: [what the user specifically did]
- Result: [measurable/observable outcome]
- Source: [link to thread, huddle note, meeting, or doc]

[repeat per win]

---
[Older entries remain below, oldest at the bottom]
```

If nothing solid surfaces, say so. Don't manufacture a moment:

> Nothing concrete surfaced this period. Worth checking in on what's been happening, or widening the lookback window.

## Key principles

- **Personal record, not a performance review.** The evidence has to be specific enough to be useful later, but the tone stays light. Nobody wants their own wins log reading like an HR form
- **Never fabricate a result.** If the outcome isn't measurable or observable from the evidence, say that plainly instead of inventing a number. A log the user can't trust is worse than no log at all
- **Append-only.** New section on top every run. Never delete or rewrite what came before
- **Their work, not the team's.** The Action line is about this person. Collective language is the fastest way to make a win useless

## Suggested cadence

Fortnightly is the sweet spot. Recent enough that the context is still warm, spaced enough that there's actually something to log. Monthly works if the pace is slower. Daily is just noise with extra steps.

---

Adapted from [`main-character-moment`](https://github.com/iamsamraph/skills/tree/main/main-character-moment) by Samantha Raphael. © 2026 Samantha Raphael. Free to use and adapt, credit appreciated.
