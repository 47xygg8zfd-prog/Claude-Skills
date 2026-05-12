# Quickstart

## What this is

A collection of Claude skills, Python agents, and a multi-stage PDLC/SDLC orchestrator for PMs and engineering teams. You can install skills into Claude.ai and talk to them directly, run individual agents from the command line for specific outputs, or run the full 24-stage pipeline from strategic framing through retrospective. Fill in `CLAUDE.md` once and every skill and agent uses your product context automatically.

---

## Setup

```bash
git clone [repo]
cd Claude-Skills
pip install anthropic
export ANTHROPIC_API_KEY=your-key-here
```

---

## Your first run — pick one entry point

### Option A: Ask Claude (no code)

Install a skill from `pm-skills/` into Claude.ai under Settings → Skills. Then just talk:

- "Write a PRD for a weekly digest email"
- "Design an A/B test for onboarding progress bars"
- "Build an opportunity solution tree for retention"

### Option B: Run a single agent (5 minutes)

```bash
# Draft a PRD from a brief
python agents/prd_drafter.py --brief "weekly digest email for engineering managers"

# Design an experiment
python agents/experiment_designer.py --feature "progress bar" --metric "onboarding completion"

# Write user stories from a PRD
python agents/agile_stories.py --file prd.md --mode all --mvp 1 --velocity 22
```

### Option C: Run the full PDLC pipeline (30–60 min, 24 stages)

```bash
python agents/pdlc_orchestrator.py \
  --goal "add a weekly digest email for engineering managers" \
  --output-dir ./digest-feature/
```

---

## What the pipeline produces

Each stage writes a numbered markdown file to `--output-dir`. Stages run in sequence; each one feeds the next.

| # | Stage | Artifact |
|---|-------|----------|
| 1 | `strategy` | Strategic framing — problem, opportunity, fit to OKRs |
| 2 | `discovery` | Discovery plan — research questions, methods, hypotheses |
| 3 | `ux-research` | Research plan, discussion guide, personas, journey map |
| 4 | `opportunity-solution-tree` | OST — outcomes, opportunities, solutions, experiments |
| 5 | `prd` | Full PRD — background, goals, requirements, metrics |
| 6 | `devil-advocate` | Critique — risks, weak assumptions, open questions |
| 7 | `mvp-scope` | MVP scope with phase 1/2/3 breakdown |
| 8 | `experiment` | Experiment design — hypothesis, metrics, sample size, rollout |
| 9 | `assumption-test` | Riskiest assumptions ranked with test designs |
| 10 | `data-science` | Data science plan — model design, features, success criteria |
| 11 | `analytics` | Analytics spec — events, funnels, dashboards |
| 12 | `design` | UX design brief — flows, components, edge cases |
| 13 | `architecture` | System architecture — services, APIs, data model |
| 14 | `spec` | Engineering spec — detailed technical requirements |
| 15 | `tech-lead` | Tech lead review — estimates, risks, open decisions |
| 16 | `agile-stories` | Epics, sprint-ready stories, and sprint plan |
| 17 | `backend` | Backend implementation plan — endpoints, schema, migrations |
| 18 | `frontend` | Frontend implementation plan — components, state, API calls |
| 19 | `qa` | QA plan — test cases, edge cases, acceptance criteria |
| 20 | `marketing` | GTM brief — messaging, launch plan, positioning |
| 21 | `exec-update` | Exec update — status, risks, asks, timeline |
| 22 | `retro` | Retrospective — what worked, what didn't, actions |

See `simulation/` for example outputs from a full run.

---

## Customize for your product

Open `CLAUDE.md` and fill in your product name, OKRs, team names, database, and competitors. Every skill and agent reads this file automatically — you only enter this context once.

Key fields to fill in first:
- **Your Product** — name, description, ICP, differentiators
- **Current Quarter Goals** — OKRs so every artifact aligns to what matters now
- **Data & Tools** — database, tables, and project tracker so queries and tickets are correct
- **Team** — names and velocity so stories and sprint plans are realistic

---

## Common patterns

| Situation | Command |
|-----------|---------|
| I have a feature idea, where do I start? | `python agents/pdlc_orchestrator.py --goal "..." --stages strategy,discovery,ux-research,prd` |
| I have a PRD, I need stories | `python agents/agile_stories.py --file prd.md --mode all --mvp 1` |
| I need to scope an MVP | `python agents/pdlc_orchestrator.py --goal "..." --stages prd,devil-advocate,mvp-scope` |
| I want to revise one stage and cascade | `python agents/pdlc_orchestrator.py --output-dir ./out/ --revise-stage prd --revise-note "strengthen rationale"` |
| I have interview transcripts | `python agents/research_synthesis.py --file transcripts.md` |
| I need a prioritized feature list | `python agents/feature_prioritizer.py --features features.md --method rice` |

---

## Full agent list

### PM agents
| Agent | What it does | Command |
|-------|-------------|---------|
| `prd_drafter.py` | Draft a PRD from a brief or ticket | `python agents/prd_drafter.py --brief "..."` |
| `experiment_designer.py` | Full experiment design from a hypothesis | `python agents/experiment_designer.py --feature "..." --metric "..."` |
| `agile_stories.py` | Epics, stories, and sprint plan from a PRD | `python agents/agile_stories.py --file prd.md --mode all` |
| `okr_drafter.py` | Draft OKRs from strategic context | `python agents/okr_drafter.py --context CLAUDE.md --quarter Q3` |
| `feature_prioritizer.py` | RICE/ICE/MoSCoW prioritization | `python agents/feature_prioritizer.py --features features.md` |
| `sprint_reporter.py` | Sprint status update from ticket data | `python agents/sprint_reporter.py --input tickets.md --audience exec` |
| `stakeholder_updater.py` | Audience-tailored stakeholder updates | `python agents/stakeholder_updater.py --file status.md --audience all` |
| `release_notes_writer.py` | Release notes from tickets or git log | `python agents/release_notes_writer.py --input tickets.md --audience all` |

### Design & Research agents
| Agent | What it does | Command |
|-------|-------------|---------|
| `ux_researcher.py` | Research plans, guides, personas, journey maps | `python agents/ux_researcher.py --brief "..." --mode all` |
| `research_synthesis.py` | Synthesize customer research transcripts | `python agents/research_synthesis.py --file transcripts.md` |
| `ui_designer.py` | UI design brief and component spec | `python agents/ui_designer.py --brief "..."` |
| `competitive_intel.py` | Competitive intelligence briefing | `python agents/competitive_intel.py --text "raw intel"` |

### Engineering agents
| Agent | What it does | Command |
|-------|-------------|---------|
| `technical_architect.py` | System architecture and API design | `python agents/technical_architect.py --brief "..."` |
| `spec_driven_dev.py` | Engineering spec from PRD | `python agents/spec_driven_dev.py --file prd.md` |
| `eng_backend.py` | Backend implementation plan | `python agents/eng_backend.py --file spec.md` |
| `eng_frontend.py` | Frontend implementation plan | `python agents/eng_frontend.py --file spec.md` |
| `eng_qa.py` | QA plan and test cases | `python agents/eng_qa.py --file spec.md` |
| `codebase_reader.py` | Read and summarize a codebase | `python agents/codebase_reader.py --path ./src/` |
| `analytics_expert.py` | Analytics spec and event taxonomy | `python agents/analytics_expert.py --brief "..."` |
| `data_scientist.py` | Data science plan and model design | `python agents/data_scientist.py --brief "..."` |

### Leadership agents
| Agent | What it does | Command |
|-------|-------------|---------|
| `pdlc_orchestrator.py` | Full 24-stage PDLC/SDLC pipeline | `python agents/pdlc_orchestrator.py --goal "..."` |
| `cpo_agent.py` | CPO-level product strategy review | `python agents/cpo_agent.py --file prd.md` |
| `cto_agent.py` | CTO-level architecture and risk review | `python agents/cto_agent.py --file spec.md` |
| `mckinsey_consultant.py` | Strategic framing and exec narrative | `python agents/mckinsey_consultant.py --brief "..."` |
| `product_marketer.py` | GTM brief and positioning | `python agents/product_marketer.py --file prd.md` |
