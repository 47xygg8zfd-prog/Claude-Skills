# PM & Engineering Agents

Working Python agents built with the Anthropic SDK that simulate a full product and engineering org. Each agent runs from the command line and streams output in real time. Run them individually or chain them with the orchestrators.

---

## Orchestrators

Run these for end-to-end workflows — they call each specialist in sequence, passing output forward.

| Agent | What It Does |
|-------|-------------|
| [pdlc-orchestrator](pdlc_orchestrator.py) | **Full PDLC/SDLC** — runs all 22 stages from strategy through continuous discovery (OST, devil's advocate, MVP scoping), analytics validation, agile story generation, quality-gated build stages, and retro with next-discovery feedback loop |
| [pm-agent](pm_agent.py) | **PM workflow** — discovery → PRD → stories → experiment → stakeholder update |
| [eng-team](eng_team.py) | **Engineering team** — tech lead → backend → frontend → QA |

### PDLC Orchestrator Stages

```
Strategy (CPO)
    └── Discovery (PM)  ←────────────────────────────────────────────────────────────┐
            └── UX Research                                                           │
                    └── Opportunity Solution Tree (OST)                               │
                            └── PRD (PM)                                              │
                                    └── Devil's Advocate Review                       │
                                            └── MVP Scope (v1 / v2 / v3)  ◄── gate  │
                                                    └── Experiment Design             │
                                                            └── Assumption Test       │
                                                                    └── Data Science  │
                                                                            └── Analytics
                                                                                    └── Design Spec
                                                                                            └── Architecture
                                                                                                    └── Spec
                                                                                                            └── Tech Lead
                                                                                                                    └── Agile Stories (epics + sprint backlog)
                                                                                                                            ├── Backend
                                                                                                                            ├── Frontend
                                                                                                                            └── QA
                                                                                                                                    └── Marketing
                                                                                                                                            └── Exec Update
                                                                                                                                                    └── Retro → Next Discovery Questions ──┘
```

**Quality gates** (auto-retry up to 2×): `ux-research`, `opportunity-solution-tree`, `prd`, `mvp-scope`, `experiment`, `analytics`, `spec`, `agile-stories`

**Post-run**: cross-stage continuity check + assumption register printed after every full run

```bash
# Run full PDLC for a feature
python pdlc_orchestrator.py --goal "add a weekly digest email for engineering managers" --output-dir ./digest/

# Run select stages only
python pdlc_orchestrator.py --goal "..." --stages prd,architecture,qa

# Start from a specific stage (uses prior stage outputs if --output-dir was used)
python pdlc_orchestrator.py --goal "..." --from-stage design

# Revise a stage and re-run all downstream stages
python pdlc_orchestrator.py --goal "..." --output-dir ./digest/ --revise-stage prd --revise-note "strengthen must-have rationale"

# Generate a backlog from a PRD (standalone, no full pipeline needed)
python agile_stories.py --file prd.md --mode all --mvp 1 --velocity 22 --output backlog.md
python agile_stories.py --brief "runbook capture for on-call tool" --mode stories
python agile_stories.py --file mvp-scope.md --mode sprint-plan --velocity 18

# Enable confidence scoring for each stage (warns if score < 3/5)
python pdlc_orchestrator.py --goal "..." --score

# Skip quality gates (faster, no auto-retry)
python pdlc_orchestrator.py --goal "..." --no-gate

# Continuous discovery mode — append discovery to running log, inject prior findings as context
python pdlc_orchestrator.py --goal "..." --output-dir ./digest/ --stages discovery --snapshot
```

---

## PM Agents

| Agent | What It Does | Key Modes |
|-------|-------------|-----------|
| [prd-drafter](prd_drafter.py) | PRD from brief or ticket | — |
| [agile-stories](agile_stories.py) | Epics, sprint-ready stories, AC, and sprint plans from a PRD or MVP scope | epics / stories / sprint-plan / all |
| [okr-drafter](okr_drafter.py) | OKRs from strategic context | — |
| [feature-prioritizer](feature_prioritizer.py) | RICE-scored backlog | rice / ice / moscow |
| [experiment-designer](experiment_designer.py) | Full A/B experiment design | — |
| [release-notes-writer](release_notes_writer.py) | Audience-tailored release notes | user / engineering / exec / all |
| [stakeholder-updater](stakeholder_updater.py) | Stakeholder updates | exec / team / customer / board / all |
| [research-synthesis](research_synthesis.py) | Themes and opportunities from interviews | — |
| [sprint-reporter](sprint_reporter.py) | Sprint status updates | team / exec / stakeholder |
| [competitive-intel](competitive_intel.py) | Competitive briefing from updates | — |

---

## Design Agents

| Agent | What It Does | Key Modes |
|-------|-------------|-----------|
| [ui-designer](ui_designer.py) | Design spec, user flows, component inventory | — |
| [codebase-reader](codebase_reader.py) | Walks a local directory and produces architecture maps, onboarding guides, or file explanations | full / architecture / onboarding / file |
| [product-marketer](product_marketer.py) | Positioning, feature announcements, launch emails, blog posts, battlecards, social copy | positioning / announcement / email / blog / battlecard / social / all |
| [ux-researcher](ux_researcher.py) | Research plans, discussion guides, synthesis reports, personas, journey maps, usability findings | plan / guide / synthesis / persona / journey / usability / all |
| [data-scientist](data_scientist.py) | Measurement plans, analysis plans, experiment results interpretation, ML scoping, data storytelling | measurement / analysis / experiment-results / ml-scoping / storytelling / all |
| [spec-driven-dev](spec_driven_dev.py) | OpenAPI specs, JSON schemas, interface contracts, Given/When/Then acceptance specs, mock payloads, test matrices | openapi / schema / contract / acceptance / mock / test-matrix / all |
| [analytics-expert](analytics_expert.py) | Validate metrics are measurable, produce instrumentation plans, write SQL queries, audit event schemas, build metric dictionaries | instrumentation / sql / audit / dictionary / all |

---

## Engineering Agents

| Agent | What It Does | Key Modes |
|-------|-------------|-----------|
| [eng-tech-lead](eng_tech_lead.py) | Architecture guidance, implementation review, PR checklist | — |
| [eng-backend](eng_backend.py) | API design, data models, business logic plan, test cases | — |
| [eng-frontend](eng_frontend.py) | Component tree, state management, API integration, a11y | — |
| [eng-qa](eng_qa.py) | Test plan, AC validation, regression checklist | — |
| [architecture-designer](architecture_designer.py) | Full system architecture with trade-offs | — |
| [technical-architect](technical_architect.py) | System design, ADR, integration, scalability, migration | design / adr / integration / scalability / migration |

---

## Leadership Agents

| Agent | What It Does | Key Modes |
|-------|-------------|-----------|
| [cpo-agent](cpo_agent.py) | Product vision, portfolio strategy, board updates | vision / portfolio / market / board / investment |
| [director-pm-agent](director_pm_agent.py) | Prioritization, coaching, escalation, OKR alignment | portfolio / prioritization / coaching / escalation / alignment |
| [eng-director-agent](eng_director_agent.py) | Delivery risk, team health, debt strategy, hiring | delivery / team / debt / hiring / dependencies |
| [cto-agent](cto_agent.py) | Tech vision, architecture governance, build/buy | vision / architecture / build-buy / culture / investment |

---

## Strategy & Advisory Agents

| Agent | What It Does | Key Modes |
|-------|-------------|-----------|
| [mckinsey-consultant](mckinsey_consultant.py) | Issue trees, structured diagnosis, recommendation decks | diagnosis / issue-tree / recommendation / slide / synthesis |

---

## Setup

```bash
pip install anthropic
export ANTHROPIC_API_KEY=your-key-here
```

---

## Design Principles

All agents share the same conventions:

1. **Prompt caching** — System prompts use `cache_control: ephemeral` to reduce cost on repeated runs
2. **Streaming output** — Results stream to stdout so you see progress in real time
3. **File I/O** — All agents accept `--file` for input and `--output` to save results as markdown
4. **Chaining** — Orchestrators pass each stage's output to the next as context
5. **Single-file** — Each agent is one Python file with no framework dependencies beyond the Anthropic SDK

---

## Usage Examples

```bash
# Full lifecycle — strategy through exec update, save all outputs
python pdlc_orchestrator.py \
  --goal "build a weekly digest email for engineering managers" \
  --output-dir ./digest-feature/

# PM workflow only
python pm_agent.py --goal "add team health scores to the manager dashboard" --output-dir ./health/

# Engineering team only (give them a PRD)
python eng_team.py --prd ./digest-feature/03_prd.md --output-dir ./digest-eng/

# Single specialist
python eng_backend.py --ticket "build the digest generation service"
python cpo_agent.py --context "evaluating enterprise expansion" --mode board
python mckinsey_consultant.py --problem "NRR dropped from 115% to 98%" --mode diagnosis
python technical_architect.py --problem "design notification system for 1M users" --mode scalability

# Leadership layer
python cpo_agent.py --file strategy.md --mode portfolio
python eng_director_agent.py --situation "three teams blocked on shared infra" --mode dependencies
python cto_agent.py --context "evaluating whether to build our own ML pipeline" --mode build-buy
python director_pm_agent.py --situation "two PMs competing for same eng capacity" --mode prioritization
```
