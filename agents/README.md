# PM Agents

Working Python agents built with the Anthropic SDK that automate common PM workflows. Each agent runs from the command line and produces a ready-to-use output.

## Agents

| Agent | What It Does | Run Time |
|-------|-------------|----------|
| [research-synthesis](research_synthesis.py) | Ingests interview transcripts, outputs structured themes and opportunities | ~30s |
| [sprint-reporter](sprint_reporter.py) | Takes ticket data, writes a stakeholder-ready status update | ~15s |
| [prd-drafter](prd_drafter.py) | Takes a brief or ticket description, produces a full PRD draft | ~45s |
| [competitive-intel](competitive_intel.py) | Takes competitor info and recent updates, produces a briefing | ~30s |
| [architecture-designer](architecture_designer.py) | Takes a PRD or brief, produces a system architecture doc with components, APIs, and trade-offs | ~45s |
| [ui-designer](ui_designer.py) | Takes a PRD or brief, produces design specs with user flows, screen specs, and component inventory | ~45s |
| [okr-drafter](okr_drafter.py) | Takes strategic context, drafts OKRs with scoring guidance and alignment check | ~30s |
| [release-notes-writer](release_notes_writer.py) | Takes tickets or git log, writes audience-tailored release notes (user / eng / exec) | ~30s |
| [experiment-designer](experiment_designer.py) | Takes a hypothesis, produces a full A/B experiment design with sample size and analysis plan | ~30s |
| [feature-prioritizer](feature_prioritizer.py) | Takes a feature list, produces a RICE-scored backlog with trade-off analysis | ~45s |
| [stakeholder-updater](stakeholder_updater.py) | Takes project status, writes updates for exec / team / customer / board | ~30s |

## Setup

```bash
pip install anthropic
export ANTHROPIC_API_KEY=your-key-here
```

## Design Principles

All agents in this folder follow the same conventions:

1. **Prompt caching** — Static system prompts are cached to reduce cost and latency on repeated runs
2. **Streaming output** — Results stream to stdout so you see progress in real time
3. **File I/O** — Agents accept input from files or stdin and write output to a markdown file
4. **Claude Sonnet** — Default model balances quality and cost for production PM workflows; swap to Opus for higher-stakes outputs
5. **No magic** — Each agent is a single file, under 150 lines, with no framework dependencies beyond the Anthropic SDK

## Usage Pattern

```bash
# Pass input inline
python research_synthesis.py --input "paste transcript here"

# Pass a file
python research_synthesis.py --file transcripts/may-interviews.txt

# Save output to file (all agents support this)
python research_synthesis.py --file transcripts/ --output synthesis.md
```
