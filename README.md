# PM Skills for Claude

A complete toolkit for product managers using Claude — 15 skills, workflow guides, a prompt library, example outputs, and tool integrations.

---

## What's in This Repo

| Folder | What It Contains |
|--------|-----------------|
| [`pm-skills/`](pm-skills/) | 15 Claude skills covering the full PM workflow |
| [`examples/`](examples/) | Sample outputs for every skill, using a consistent fictional product |
| [`workflows/`](workflows/) | End-to-end guides for chaining skills together |
| [`prompts/`](prompts/) | 16 copy-paste prompts for one-off tasks |
| [`integrations/`](integrations/) | MCP config snippets for Jira, Linear, Notion, Confluence, and Slack |
| [`templates/`](templates/) | Fillable markdown templates for PRDs, OKRs, retros, and more |
| [`metrics/`](metrics/) | KPI definitions, benchmarks, and Snowflake SQL by product area |
| [`ai-features/`](ai-features/) | Framework for scoping, evaluating, and shipping AI features |
| [`case-study/`](case-study/) | End-to-end PM case study showing all skills used on one scenario |
| [`CLAUDE.md`](CLAUDE.md) | Fill-in-once context file that makes every skill smarter |

---

## Skills

| Skill | What It Does |
|-------|-------------|
| [`prd`](pm-skills/prd/) | Generate structured PRDs |
| [`agile-stories`](pm-skills/agile-stories/) | Draft user stories, epics, and acceptance criteria |
| [`agile-ceremonies`](pm-skills/agile-ceremonies/) | Facilitate retros, sprint planning, and refinement |
| [`data-queries`](pm-skills/data-queries/) | Generate Snowflake SQL and Splunk SPL |
| [`monte-carlo`](pm-skills/monte-carlo/) | Forecast delivery dates with probability ranges |
| [`tech-translation`](pm-skills/tech-translation/) | Decode engineering jargon and tradeoffs |
| [`quicksight-dashboards`](pm-skills/quicksight-dashboards/) | Design and build QuickSight dashboards |
| [`pm-presentations`](pm-skills/pm-presentations/) | Roadmap, exec update, and QBR slide decks |
| [`claude-automation`](pm-skills/claude-automation/) | Scope and build Claude skills and agents |
| [`feature-prioritization`](pm-skills/feature-prioritization/) | RICE, ICE, MoSCoW, and impact/effort matrices |
| [`customer-research-synthesis`](pm-skills/customer-research-synthesis/) | Themes, JTBD, and opportunities from raw research |
| [`okrs`](pm-skills/okrs/) | Draft, score, and check in on OKRs |
| [`release-notes`](pm-skills/release-notes/) | Audience-tailored release notes and changelogs |
| [`stakeholder-updates`](pm-skills/stakeholder-updates/) | Status updates, escalations, and DACI/RACI tables |
| [`competitive-analysis`](pm-skills/competitive-analysis/) | Teardowns, feature matrices, battlecards, and win/loss analysis |

---

## Workflows

| Workflow | When to Use |
|----------|------------|
| [Discovery to Delivery](workflows/discovery-to-delivery.md) | Taking a feature from research through to release |
| [Research to Roadmap](workflows/research-to-roadmap.md) | Quarterly planning cycle |
| [Incident & Risk Comms](workflows/incident-to-comms.md) | Responding to a launch risk or production incident |

---

## Quick Start

### 1. Fill in CLAUDE.md
Open [`CLAUDE.md`](CLAUDE.md) and fill in your product name, ICP, OKRs, team, and tools. This is read automatically at the start of every Claude session — fill it in once and every skill works without re-entering context.

### 2. Install the skills
Each skill lives in `pm-skills/<skill-name>/SKILL.md`. To install:
1. Open Claude → **Settings → Skills**
2. Upload the `SKILL.md` for each skill you want
3. Claude will trigger the skill automatically when relevant context is detected

### 3. Connect your tools (optional)
See [`integrations/`](integrations/) for MCP config snippets that connect Claude directly to Jira, Linear, Notion, Confluence, and Slack.

### 4. Use the prompt library for one-off tasks
[`prompts/README.md`](prompts/README.md) has 16 copy-paste prompts for tasks that don't need a full skill — ticket rewrites, AC generation, meeting agendas, decision logs, and more.

---

## Example Outputs

Not sure what a skill produces? The [`examples/`](examples/) folder has realistic sample outputs for all 15 skills, built around a single fictional product so they cross-reference each other. See the [examples README](examples/README.md) for the full list.

---

## Customization

The fastest way to customize skills for your context:
- **CLAUDE.md** — add your product details, team, OKRs, and terminology once
- **Individual SKILL.md files** — each skill has a "Customization Tips" section at the bottom
- **Integrations** — connect to your actual tools so skills can read and write directly

---

## Repo Structure

```
Claude-Skills/
├── CLAUDE.md                  # Your persistent product + team context
├── pm-skills/                 # 15 skill definitions
│   ├── prd/
│   ├── agile-stories/
│   └── ... (13 more)
├── examples/                  # Sample outputs for every skill
├── workflows/                 # Multi-skill workflow guides
├── prompts/                   # One-off prompt library
├── integrations/              # MCP configs for PM tools
├── templates/                 # Fillable doc templates
├── metrics/                   # KPI definitions + SQL by product area
├── ai-features/               # AI feature PM framework
└── case-study/                # End-to-end PM case study
```
