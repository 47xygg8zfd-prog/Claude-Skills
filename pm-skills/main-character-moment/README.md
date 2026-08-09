# Main Character Moment

A skill that goes back through your Slack, finds the work you actually did, and writes it up properly — so the evidence still exists when review season arrives and your brain surrenders nothing.

You did the thing. You unblocked the stuck project, you answered the question nobody else could, you quietly shipped the feature that was rotting in the backlog. Then you forgot all about it.

This finds the receipts.

> Adapted from [`iamsamraph/skills`](https://github.com/iamsamraph/skills/tree/main/main-character-moment) by Samantha Raphael, used and modified with credit.

## What it does

Once a run, it reads back through your Slack — your messages, the threads you were central to, praise from other people, huddle notes you're tagged in, canvases you made — and pulls out concrete wins. Each one gets written up in STAR format (Situation, Task, Action, Result) with a link back to the evidence, and appended to a running canvas called **Main Character Moments**.

It never overwrites what's already there. Every run adds to the pile.

If you have a calendar or documents connected, it reads those too. If you don't, it carries on without them.

## The one rule that matters

**It will not fabricate a result.**

If the evidence for something is thin, it says so and flags it as worth revisiting, rather than inventing a number to fill the page. An AI that inflates your wins gives you a log you can't take into a real conversation, which is worse than having no log at all.

## How to use it

**In Claude Code** — drop `SKILL.md` into `.claude/skills/main-character-moment/SKILL.md` in your project or home directory. Needs Slack connected.

**In Claude** — Settings → Skills, same as the other skills in this repo.

**In Slack** — paste the contents in as a Slackbot skill.

**Anywhere else** — it's plain text instructions. Paste it into whichever AI assistant you use, as long as it can read your Slack.

## Cadence

Fortnightly is the sweet spot — recent enough that the context is still warm, spaced enough that there's something worth logging. Monthly works if your pace is slower. Daily is noise with extra steps.

## Make it yours

This is deliberately generic. It assumes no particular team, tool stack, or job title, and the tags it uses (Impact, Collaboration, Leadership, Initiative, Growth) are a starting point, not gospel.

Change the tags to match how your company actually talks about performance. Change the lookback window. Change the output format. Point it at whatever else you live in.

## A note on privacy

It only reads what you already have access to. This is your record of your work — it isn't for going through other people's material to pad the list out.

---

© 2026 Samantha Raphael. Free to use and adapt, credit appreciated.
