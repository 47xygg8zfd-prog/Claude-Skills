# Claude Context — PM Skills Workspace

This file provides Claude with persistent context about your product, team, and preferences so every skill works without re-entering the same information each session.

**How to use**: Fill in the sections below with your real details. Claude reads this file automatically at the start of every session.

---

## Your Product

**Product name**: Pulse  
**One-line description**: B2B team analytics platform that gives engineering managers insight into team health, delivery velocity, and sprint predictability — without the spreadsheets.  
**Stage**: Series B  
**Primary metric**: WAU of managers who open and act on the weekly digest (digest-active WAU)  

**Ideal customer profile (ICP)**:  
Engineering managers at mid-market B2B SaaS companies (200–2000 employees) who own a team of 8–30 engineers, use Jira + GitHub + Slack as their primary toolchain, and are accountable for delivery predictability and team health. Not HR. Not executives. The manager in the stand-up.

**Top 3 differentiators**:  
1. Manager-first — built for the person running the team, not for HR dashboards or exec roll-ups
2. Actionable recommendations, not just metrics — Pulse tells you what to do, not just what happened
3. Live in 3 days, not 3 months — no professional services, no lengthy implementation, just connect your tools and go

**Known weaknesses / honest gaps**:  
No mobile app; fewer Jira configuration variants supported than Linearb (custom workflows are a gap); no org-level rollup — Pulse is team-scoped only, so multi-team directors need to context-switch between views

---

## Current Quarter Goals (OKRs)

**Quarter**: Q2 2026

**Objective 1**: Make Pulse the habit engineering managers return to every week  
- KR1: Digest-active WAU 38% → 52%
- KR2: Weekly digest open rate 61% → 75%

**Objective 2**: Nail onboarding — get managers to their first insight fast  
- KR1: Time-to-first-insight 8 days → 3 days
- KR2: 30-day retention 64% → 78%

---

## Team

**PM**: Jordan  
**Eng lead**: Sam  
**Design lead**: Priya  
**Data / analytics**: Alex  
**CS lead**: Morgan  
**Sprint length**: 2 weeks  
**Team velocity**: ~18 story points/sprint  

---

## Key Competitors

| Competitor | Threat | Their Pitch | Our Counter |
|------------|--------|-------------|-------------|
| Linearb | High | Git analytics for engineering teams — merge times, cycle time, PR review lag | We're manager-first; they're metrics-first. Pulse tells you what to do with the data, Linearb just shows it. |
| Swarmia | Medium | Flow metrics and team health for engineering orgs | Better recommendations and faster setup; Swarmia still requires a data analyst to interpret the output. |
| Allstacks | Low | Executive-level engineering reporting and roadmap forecasting | We serve managers, not execs. Allstacks is a top-down tool; Pulse is bottom-up and actionable. |

---

## Data & Tools

**Analytics database**: Snowflake  
**Key tables**: `events`, `users`, `accounts`, `digest_sends`, `sprint_data`  
**Log platform**: CloudWatch  
**Dashboard tool**: QuickSight  
**Project tracker**: Jira — project key: PULSE  
**Docs**: Confluence — space: PROD  
**Comms**: Slack — main channel: #product  

---

## Story Pointing Scale

| Points | Meaning |
|--------|---------|
| 1 | Trivial — a config change or copy fix |
| 2 | Small — well-understood, few edge cases |
| 3 | Medium — some complexity or unknowns |
| 5 | Large — significant work or multiple components |
| 8 | Very large — consider breaking down |
| 13+ | Epic — must be broken down before sprint |

---

## Communication Preferences

**Status update cadence**: Weekly, Mondays  
**Exec update audience**: VP Product, CFO, CEO  
**Stakeholder Slack channels**: #product-updates, #exec-updates  
**Release notes go to**: Intercom (customer-facing) + internal Confluence page (PROD space)  

---

## Terminology

| Term | Meaning |
|------|---------|
| "the digest" | The weekly email summary sent to managers every Monday morning — our primary engagement surface and core product loop |
| "ICP account" | An account where the manager owns a team of 8–30 engineers on Jira + GitHub + Slack |
| "TTV" | Time-to-value — how long from sign-up until a manager sees their first meaningful insight in Pulse |
| "manager health score" | Composite metric combining digest open rate, insight click-through, and recommendation action rate for a given manager |
| "digest-active WAU" | Weekly active users who opened and interacted with that week's digest — our primary north star metric |
| "sprint predictability" | The ratio of committed story points delivered vs. planned across the last 4 sprints — a key metric Pulse surfaces |

---

## Skill Defaults

Override default behavior for specific skills:

- **monte-carlo**: Default confidence target = 85%
- **agile-stories**: Default pointing scale = Fibonacci (see table above)
- **release-notes**: Default primary audience = end users first, then internal
- **okrs**: Company OKRs cascade (add above) — check team KRs for alignment
- **data-queries**: Default database = Snowflake; default schema = `pulse_analytics`
