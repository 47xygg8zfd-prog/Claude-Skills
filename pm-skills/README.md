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
```

## Customization Tips

- Add your Snowflake schema/table names to `data-queries`
- Add your QuickSight account details to `quicksight-dashboards`
- Add team-specific MCP server URLs to `claude-automation`
- Adjust story pointing scale in `agile-stories`
- Add company terminology to `tech-translation`
