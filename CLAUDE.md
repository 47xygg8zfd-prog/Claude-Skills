# Claude Context — PM Skills Workspace

This file provides Claude with persistent context about your product, team, and preferences so every skill works without re-entering the same information each session.

**How to use**: Fill in the sections below with your real details. Claude reads this file automatically at the start of every session.

---

## Your Product

**Product name**: [e.g. Pulse]  
**One-line description**: [e.g. B2B team analytics platform for engineering managers]  
**Stage**: [e.g. Series B / Growth / Enterprise]  
**Primary metric**: [e.g. Weekly Active Users (WAU)]  

**Ideal customer profile (ICP)**:  
[e.g. Engineering managers at mid-market B2B SaaS companies (100–500 engineers), using Jira + Slack + GitHub]

**Top 3 differentiators**:  
1. [e.g. Fastest time-to-value — live in 3 days, not 6 weeks]
2. [e.g. Built for frontline managers, not HR or executives]
3. [e.g. Actionable recommendations, not just dashboards]

**Known weaknesses / honest gaps**:  
[e.g. Fewer integrations than Teamlytics; no mobile app; no SCIM provisioning yet]

---

## Current Quarter Goals (OKRs)

**Quarter**: [e.g. Q3 2026]

**Objective 1**: [e.g. Make Pulse a habit managers return to weekly]  
- KR1: [e.g. WAU 32% → 42%]
- KR2: [e.g. Manager login frequency 1.8x → 3.5x/week]

**Objective 2**: [e.g. Turn new users into confident Pulse users in 30 days]  
- KR1: [e.g. Onboarding completion 38% → 65%]
- KR2: [e.g. Time-to-first-insight 8 days → 3 days]

**Objective 3**: [e.g. Keep the customers we've earned]  
- KR1: [e.g. 90-day retention 71% → 78%]

---

## Team

**PM**: [Your name]  
**Eng lead**: [Name]  
**Design lead**: [Name]  
**Data / analytics**: [Name]  
**CS lead**: [Name]  
**Sprint length**: [e.g. 2 weeks]  
**Team velocity**: [e.g. ~11 story points/sprint]  

---

## Key Competitors

| Competitor | Threat | Their Pitch | Our Counter |
|------------|--------|-------------|-------------|
| [e.g. Teamlytics] | High | [e.g. All-in-one people analytics] | [e.g. Faster, built for managers] |
| [e.g. DataTeam] | Medium | [e.g. GitHub-native insights] | [e.g. Broader data sources, better UX] |

---

## Data & Tools

**Analytics database**: [e.g. Snowflake]  
**Key tables**: [e.g. `events`, `users`, `accounts`, `digest_sends`]  
**Log platform**: [e.g. Splunk]  
**Dashboard tool**: [e.g. QuickSight]  
**Project tracker**: [e.g. Jira — project key: PULSE]  
**Docs**: [e.g. Confluence — space: PROD]  
**Comms**: [e.g. Slack — main channel: #product]  

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

**Status update cadence**: [e.g. Weekly, Mondays]  
**Exec update audience**: [e.g. VP Product, CFO, CEO]  
**Stakeholder Slack channels**: [e.g. #product-updates, #exec-updates]  
**Release notes go to**: [e.g. Intercom + internal Confluence page]  

---

## Terminology

Add any company-specific terms, acronyms, or jargon Claude should know:

| Term | Meaning |
|------|---------|
| [e.g. "the digest"] | [e.g. The weekly email summary feature] |
| [e.g. "ICP account"] | [e.g. An account matching our ideal customer profile] |
| [e.g. "TTV"] | [e.g. Time-to-value — how long until a new user sees their first insight] |

---

## Skill Defaults

Override default behavior for specific skills:

- **monte-carlo**: Default confidence target = 80%
- **agile-stories**: Default pointing scale = Fibonacci (see table above)
- **release-notes**: Default primary audience = end users first, then internal
- **okrs**: Company OKRs cascade (add above) — check team KRs for alignment
- **data-queries**: Default database = Snowflake; default schema = `pulse_analytics`
