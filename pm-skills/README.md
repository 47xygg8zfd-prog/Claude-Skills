# PM Skills for Claude

A complete collection of Claude skills tailored for product management workflows.

## Skills Included

| Skill | Description | Trigger Phrases |
|-------|-------------|--------------------|
| `prd` | Generate structured PRDs | "write a PRD", "spec this out", "product requirements for..." |
| `agile-stories` | Draft user stories, epics, AC | "write stories for", "break into tickets", "write AC for..." |
| `agile-ceremonies` | Facilitate retros, planning, refinement | "run the retro", "sprint planning agenda", "refinement template" |
| `data-queries` | Generate Snowflake SQL and Splunk SPL | "query for DAU", "Splunk search for errors", "write SQL to..." |
| `monte-carlo` | Forecast delivery dates with probabilities | "when will we finish", "probability of hitting Q3", "forecast..." |
| `tech-translation` | Decode engineering jargon & tradeoffs | "what does X mean", "translate this for me", "engineers said..." |
| `quicksight-dashboards` | Design and build QuickSight dashboards | "build a dashboard for", "visualize this data", "KPI board for..." |
| `pm-presentations` | PM slide deck templates (roadmap, exec, QBR) | "build me a deck", "slides for exec update", "roadmap presentation" |
| `claude-automation` | Scope and build Claude skills & agents | "automate this with Claude", "build a skill for", "agent to..." |
| `feature-prioritization` | RICE, ICE, MoSCoW, impact/effort matrices | "prioritize these features", "RICE score this", "what should we build first" |
| `customer-research-synthesis` | Themes, JTBD, and opportunities from raw research | "synthesize these interview notes", "find themes in this research", "summarize user feedback" |
| `okrs` | Draft, score, and check in on OKRs | "write OKRs for", "score my OKRs", "flag at-risk goals" |
| `release-notes` | Audience-tailored release notes and changelogs | "write release notes", "draft a changelog", "summarize what shipped" |
| `stakeholder-updates` | Status updates, escalations, DACI/RACI tables | "write a stakeholder update", "escalation memo", "write a DACI" |
| `competitive-analysis` | Teardowns, feature matrices, battlecards, win/loss | "competitive analysis for", "battlecard for", "compare us to" |
| `go-to-market` | Launch plans, rollout phases, channel strategy, enablement | "write a GTM plan", "plan the launch for", "launch readiness for..." |
| `experiment-design` | A/B test design, sample sizes, result interpretation | "design an A/B test for", "sample size for", "interpret these results..." |
| `north-star-metric` | Define and defend the single most important metric | "define our north star metric", "what should our north star be..." |
| `product-strategy` | Strategy one-pagers, where to play, how to win | "write a product strategy", "strategic one-pager for", "where should we focus" |
| `ui-designer` | Design specs, user flows, screen specs, component inventory, accessibility notes | "design this feature", "spec out the UX", "write design requirements for..." |
| `codebase-reader` | Read, map, and explain any codebase — architecture, onboarding guide, file explanations | "read the codebase", "explain this repo", "I'm new to this project", "map the architecture" |

## How to Install

Each folder contains a `SKILL.md` file. To install a skill:

1. Open Claude and go to **Settings → Skills**
2. Upload the `.skill` file for each skill you want
3. Claude will automatically use the skill when relevant context is detected

## Skill Interactions

```
PRD → Agile Stories → Sprint Planning (Agile Ceremonies)
                            ↓
              Data Queries (measuring success metrics)
              QuickSight Dashboards (visualizing metrics)
                            ↓
              Monte Carlo (forecasting delivery)
                            ↓
              PM Presentations (communicating to stakeholders)
                            ↓
              Tech Translation (engineering discussions)
              Claude Automation (building AI tools with eng)
                            ↓
              Customer Research Synthesis (validating direction)
              Competitive Analysis (market positioning)
                            ↓
              Feature Prioritization (what to build next)
              OKRs (goal setting and tracking)
                            ↓
              Release Notes (communicating what shipped)
              Stakeholder Updates (keeping everyone aligned)
```

## Customization Tips

- Add your Snowflake schema/table names to `data-queries`
- Add your QuickSight account details to `quicksight-dashboards`
- Add team-specific MCP server URLs to `claude-automation`
- Adjust story pointing scale in `agile-stories`
- Add company terminology to `tech-translation`
- Add your ICP and differentiators to `competitive-analysis`
- Add your team roster to `stakeholder-updates` for auto-suggested DACI owners
- Add company OKRs to `feature-prioritization` to weight scores toward current goals
- Add your user personas to `customer-research-synthesis` for segmented insights
- Add your versioning scheme and brand voice to `release-notes`
