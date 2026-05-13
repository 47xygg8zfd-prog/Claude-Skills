# Problem Statement & Decision

## The Problem

**Pain**: Engineering managers return to Pulse only when something is already on fire. By that point, sprint slippage or team health deterioration is a lagging signal — the damage is done.

**User**: Engineering managers at mid-market SaaS (200–2000 employees) who are accountable for delivery predictability but spend most of their cognitive load in Jira, GitHub, and Slack — not analytics tools.

**Evidence**: Exit interviews with 12 churned accounts (Q4 2025) showed 9 of 12 said Pulse was "useful when I remember to use it." Session data confirmed: 71% of weekly sessions were initiated by a direct link from an alert — not by managers opening Pulse on their own. Median sessions per active user per week: 1.3. For managers who opened the digest: 3.1.

---

## User Personas

### Persona 1 — Maya, the New EM (Promoted 8 months ago)
Runs a 9-person team. Came up through engineering; still context-switches into IC work two days a week. Checks Pulse reactively after sprint reviews when her director asks about velocity. Does not have a weekly review ritual yet. Needs Pulse to teach her what to look for, not just show the data.

### Persona 2 — Carlos, the Experienced EM (5 years managing)
Runs a 22-person distributed team across two time zones. Has a weekly Friday sync with his skip-level. Wants a concise brief he can skim in under 3 minutes that gives him a defensible narrative on team health. Already has a review ritual — he needs Pulse to slot into it, not replace it.

### Persona 3 — Dana, the Director (Manages 3 EMs)
Technically outside our ICP for the digest itself, but shapes whether Pulse gets renewed. Cares about whether her EMs are using the tool. A digest that drives EM engagement directly improves Dana's perception of value and reduces churn risk at renewal.

---

## Core Research Insight

Managers don't lack data. Pulse already surfaces sprint predictability, PR cycle time, and team health scores in-app. The gap is behavioral: **managers lack a scheduled forcing function to review that data weekly.** The digest is not a feature — it is a habit trigger.

---

## Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| A — In-app notification center | Badge + inbox inside Pulse for weekly summary | No new channel; full data richness | Requires manager to open Pulse first; solves nothing for the re-engagement problem |
| B — Weekly email digest | Monday-morning email with curated signals + one recommendation | Meets managers where they are; easy to forward to skip-level; measurable open/click rate | Email fatigue risk; limited real estate for nuance |
| C — Slack integration | Push weekly summary to manager's DMs or team channel | Meets managers where they live; async-native | Slack noise is already high; harder to design recommendation-first; depends on Slack workspace permissions per account |

---

## Final Recommendation: Option B — Weekly Email Digest

**Rationale**: Email is the only channel where we control delivery timing, rendering, and measurement without depending on a third-party permission model (Slack) or requiring the manager to already be in the product (in-app). More importantly, email is the medium Carlos and Maya already use for their skip-level summaries — we are not asking them to adopt a new behavior, we are inserting into one they already have.

Slack integration was deprioritized to Q3 as a complementary surface, not a replacement. The in-app notification center remains on the backlog as a v2 enhancement once the habit is established.
