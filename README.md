# Claude Skills for Product Managers

A complete toolkit for product managers using Claude — 32 skills, working agents for every PM and engineering role, PDLC orchestrators, full product simulations, a PM portfolio, and strategic frameworks.

---

## What's in This Repo

| Folder | What It Contains |
|--------|-----------------|
| [`pm-skills/`](pm-skills/) | 32 Claude skills covering the full PM and product development workflow |
| [`agents/`](agents/) | 40+ working Python agents — PM, design, engineering, leadership, strategy — plus PDLC/SDLC orchestrators |
| [`pm-portfolio/`](pm-portfolio/) | PM portfolio with case studies, 9 product teardowns, metrics framework, and PM OS templates |
| [`simulation/`](simulation/) | Full PDLC simulations: on-call burnout tool (20 stages), PM upskilling (15 stages), Bridge tech-translator (8 stages + competitive analysis) |
| [`frameworks/`](frameworks/) | Strategic and product thinking frameworks: HEART, Wardley, Kano, OST, Playing to Win, and more |
| [`case-study/`](case-study/) | End-to-end PM case study showing all skills on one scenario |
| [`thinking/`](thinking/) | PM principles, hard decisions, product teardowns, and anti-patterns |
| [`examples/`](examples/) | Sample outputs for every skill |
| [`workflows/`](workflows/) | End-to-end guides for chaining skills together |
| [`prompts/`](prompts/) | Copy-paste prompt library for one-off tasks |
| [`integrations/`](integrations/) | MCP config snippets for Jira, Linear, Notion, Confluence, and Slack |
| [`templates/`](templates/) | Fillable markdown templates for PRDs, OKRs, retros, and more |
| [`metrics/`](metrics/) | KPI definitions, benchmarks, and Snowflake SQL by product area |
| [`ai-features/`](ai-features/) | Framework for scoping, evaluating, and shipping AI features |
| [`CLAUDE.md`](CLAUDE.md) | Fill-in-once context file that makes every skill smarter |

---

## Skills

| Skill | What It Does |
|-------|-------------|
| [`prd`](pm-skills/prd/) | Generate structured PRDs |
| [`agile-stories`](pm-skills/agile-stories/) | Sprint-ready epics, user stories with Given/When/Then AC, story points, sprint plans |
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
| [`go-to-market`](pm-skills/go-to-market/) | Launch plans, rollout phases, channel strategy, and enablement |
| [`experiment-design`](pm-skills/experiment-design/) | A/B test design, sample sizes, and result interpretation |
| [`north-star-metric`](pm-skills/north-star-metric/) | Define and defend the single most important metric |
| [`product-strategy`](pm-skills/product-strategy/) | Strategy one-pagers, where to play, how to win |
| [`ui-designer`](pm-skills/ui-designer/) | Design specs, user flows, screen specs, component inventory, accessibility |
| [`codebase-reader`](pm-skills/codebase-reader/) | Read, map, and explain any codebase |
| [`product-marketer`](pm-skills/product-marketer/) | Positioning, launch copy, emails, blog posts, battlecards, social |
| [`ux-researcher`](pm-skills/ux-researcher/) | Research plans, discussion guides, synthesis reports, personas, journey maps |
| [`data-scientist`](pm-skills/data-scientist/) | Measurement plans, analysis plans, experiment results, ML scoping |
| [`spec-driven-dev`](pm-skills/spec-driven-dev/) | OpenAPI specs, JSON schemas, Given/When/Then acceptance specs, mock payloads |
| [`analytics`](pm-skills/analytics/) | Define, validate, and audit product analytics instrumentation |
| [`continuous-discovery`](pm-skills/continuous-discovery/) | Opportunity solution trees, weekly interview cadence, assumption testing |
| [`roadmap`](pm-skills/roadmap/) | Quarterly roadmaps, Now/Next/Later views, scenario modeling |
| [`pricing-packaging`](pm-skills/pricing-packaging/) | Tier design, feature gating matrix, competitive pricing |
| [`interview-analysis`](pm-skills/interview-analysis/) | Theme extraction, JTBD maps, OST input, personas from raw interview notes |
| [`product-strategy`](pm-skills/product-strategy/) | Strategy one-pagers, where to play, how to win |
| [`e2e-testing`](pm-skills/e2e-testing/) | Regression test suites for Claude agents — structural smoke tests, semantic section checks, LLM-as-judge scoring |
| [`main-character-moment`](pm-skills/main-character-moment/) | Mine Slack for concrete work wins and log them in STAR format to a running canvas |

---

## Agents

See [`agents/README.md`](agents/README.md) for the full list. Highlights:

**Orchestrators**
- [`pdlc-orchestrator`](agents/pdlc_orchestrator.py) — full 24-stage PDLC from strategy through continuous discovery, with quality gates and auto-retry
- [`pm-agent`](agents/pm_agent.py) — PM workflow: discovery → PRD → stories → experiment → stakeholder update
- [`eng-team`](agents/eng_team.py) — engineering team: tech lead → backend → frontend → QA

**PM Agents** — prd-drafter, agile-stories, okr-drafter, feature-prioritizer, experiment-designer, release-notes-writer, stakeholder-updater, research-synthesis, roadmap, pricing-packager, interview-analyst, sprint-reporter, competitive-intel

**Design Agents** — ui-designer, codebase-reader, product-marketer, ux-researcher, data-scientist, spec-driven-dev, analytics-expert, e2e-tester

**Engineering Agents** — eng-tech-lead, eng-backend, eng-frontend, eng-qa, architecture-designer, technical-architect

**Leadership Agents** — cpo-agent, director-pm-agent, eng-director-agent, cto-agent

**Strategy** — mckinsey-consultant

---

## PM Portfolio

[`pm-portfolio/`](pm-portfolio/) — a complete PM portfolio built around Pulse, a Series B B2B team analytics platform.

| Section | What It Shows |
|---------|--------------|
| [Case Study: Weekly Digest](pm-portfolio/case-studies/pulse-digest-feature/) | Problem framing → PRD → A/B experiment → retrospective. Outcome: +11pp digest-active WAU |
| [Product Teardowns](pm-portfolio/product-teardowns/) | 9 teardowns (LinearB, Swarmia, Allstacks, Spotify, Linear, OpenAI, Gemini, Cursor, Lovable) + competitive matrix |
| [Metrics Framework](pm-portfolio/metrics-frameworks/) | North star metric, 4-layer metric tree, SaaS retention framework with Snowflake SQL |
| [PM Operating System](pm-portfolio/pm-operating-system/) | PRD template, RICE prioritization, weekly review, DACI decision framework |

---

## Simulations

Full PDLC simulations showing what real product work looks like end-to-end:

| Simulation | Stages | What It Covers |
|-----------|--------|---------------|
| [On-Call Burnout Tool](simulation/oncall-burnout/) | 20 | Strategy through exec update for an on-call burnout detection product (Sentinel) |
| [PM Technical Upskilling](simulation/pm-technical-upskilling/) | 15 | Full product development for a PM technical upskilling platform |
| [Bridge: Tech Translator](simulation/tech-translator/) | 8 | Discovery through MVP scoping for a PM-to-engineer translation tool — includes competitive analysis, devil's advocate review, and 3 MVP options |

---

## Quick Start

### 1. Fill in CLAUDE.md
Open [`CLAUDE.md`](CLAUDE.md) and fill in your product name, ICP, OKRs, team, and tools. Every skill reads this automatically — fill it in once and skip re-entering context every session.

### 2. Install skills
Each skill lives in `pm-skills/<skill-name>/SKILL.md`. Upload to Claude → **Settings → Skills**. Claude triggers the skill automatically when relevant context is detected.

### 3. Run an agent
```bash
pip install anthropic
export ANTHROPIC_API_KEY=your-key-here

# Full PDLC — strategy through retrospective
python agents/pdlc_orchestrator.py --goal "add a weekly digest email for engineering managers" --output-dir ./digest/

# Single specialist
python agents/prd_drafter.py --brief "add team health scores to the manager dashboard"
python agents/experiment_designer.py --hypothesis "digest email increases WAU"
python agents/e2e_tester.py --brief "regression suite for all PM agents" --mode all --output tests/
```

### 4. Connect your tools (optional)
See [`integrations/`](integrations/) for MCP config snippets for Jira, Linear, Notion, Confluence, and Slack.

---

## Repo Structure

```
Claude-Skills/
├── CLAUDE.md                        # Your persistent product + team context
├── QUICKSTART.md                    # Step-by-step onboarding
├── pm-skills/                       # 32 skill definitions
├── agents/                          # 40+ working Python agents + orchestrators
├── pm-portfolio/                    # PM portfolio: case study, teardowns, metrics, OS
│   ├── case-studies/
│   ├── product-teardowns/           # 9 teardowns + competitive matrix
│   ├── metrics-frameworks/
│   └── pm-operating-system/
├── simulation/                      # Full PDLC simulations (3 products)
│   ├── oncall-burnout/
│   ├── pm-technical-upskilling/
│   └── tech-translator/
├── frameworks/                      # Strategic frameworks
├── thinking/                        # PM principles and anti-patterns
├── case-study/                      # End-to-end PM case study
├── examples/                        # Sample outputs for every skill
├── workflows/                       # Multi-skill workflow guides
├── prompts/                         # One-off prompt library
├── integrations/                    # MCP configs for PM tools
├── templates/                       # Fillable doc templates
├── metrics/                         # KPI definitions + SQL
└── ai-features/                     # AI feature PM framework
```
