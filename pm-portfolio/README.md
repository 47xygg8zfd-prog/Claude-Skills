# PM Portfolio — Pulse

A product thinking portfolio built around **Pulse**, a Series B B2B team analytics platform for engineering managers. Every artifact here reflects a real decision, trade-off, or framework — not a textbook exercise.

**Product**: Pulse — gives engineering managers insight into team health, delivery velocity, and sprint predictability without spreadsheets.  
**Stage**: Series B  
**Primary metric**: Digest-active WAU (managers who open and act on the weekly digest)  
**Target customer**: EMs at 200–2000 person SaaS companies, owning 8–30 engineers on Jira + GitHub + Slack

---

## What's Here

### 1. [Case Study: Weekly Digest Feature](./case-studies/pulse-digest-feature/)

End-to-end product work on Pulse's core engagement surface. Shows how I frame problems, write requirements, design experiments, and close the loop.

| Artifact | What it shows |
|----------|--------------|
| [Problem Statement](./case-studies/pulse-digest-feature/01-problem-statement.md) | Problem framing, personas, option trade-offs |
| [PRD](./case-studies/pulse-digest-feature/02-prd.md) | Requirements with research justification, success metrics |
| [Experiment Design](./case-studies/pulse-digest-feature/03-experiment-design.md) | A/B test design, sample size math, decision criteria |
| [Retrospective](./case-studies/pulse-digest-feature/04-retrospective.md) | What we got wrong, what we'd change, v2 recommendations |

**Outcome**: +11pp digest-active WAU, 73% open rate (target: 75%), shipped to 100% of accounts.

---

### 2. [Product Teardowns](./product-teardowns/)

Competitive analysis of Pulse's three main competitors. Shows market awareness, UX intuition, and strategic thinking — including honest assessments of where competitors win.

| Teardown | Threat level | Key finding |
|----------|-------------|-------------|
| [LinearB](./product-teardowns/linearb.md) | High | Best-in-class git analytics; weak on actionability |
| [Swarmia](./product-teardowns/swarmia.md) | Medium | Strong flow metrics; requires a data analyst to interpret |
| [Allstacks](./product-teardowns/allstacks.md) | Low | Serves execs, not managers — different buyer entirely |
| [Competitive Matrix](./product-teardowns/competitive-matrix.md) | — | 15-feature comparison across all four products |

---

### 3. [Metrics Framework](./metrics-frameworks/)

How I define, structure, and prioritize metrics for a SaaS product. The core principle: every input metric needs a documented hypothesis linking it to the north star. Dashboards without a hierarchy are just noise.

| Document | What it covers |
|----------|---------------|
| [North Star Metric](./metrics-frameworks/north-star-metric.md) | Why digest-active WAU, how it's defined, guardrails |
| [Metric Tree](./metrics-frameworks/metric-tree.md) | Full 4-layer hierarchy: acquisition → activation → engagement → retention |
| [SaaS Retention Framework](./metrics-frameworks/saas-retention-framework.md) | Cohort analysis, failure modes, Snowflake SQL |

**Current focus**: TTV is the gating constraint (8 days → 3 days target). Fixing activation unlocks everything downstream.

---

### 4. [PM Operating System](./pm-operating-system/)

Templates and frameworks that show how I structure product work. These aren't aspirational — they're what I actually use.

| Template | What it covers |
|----------|---------------|
| [PRD Template](./pm-operating-system/prd-template.md) | Requirements with research justification, decision log |
| [Prioritization Framework](./pm-operating-system/prioritization-framework.md) | RICE scoring with worked example and when *not* to use it |
| [Weekly Review Template](./pm-operating-system/weekly-review-template.md) | 20-minute weekly snapshot: metrics, decisions, risks, next week |
| [DACI Template](./pm-operating-system/daci-template.md) | Decision ownership framework with filled-in Pulse example |

---

## How to Read This Portfolio

**If you want to see how I define problems**: Start with the [Problem Statement](./case-studies/pulse-digest-feature/01-problem-statement.md) — specifically the three personas and the option trade-off table.

**If you want to see how I think about metrics**: Start with the [North Star Metric](./metrics-frameworks/north-star-metric.md) and the "Where to Focus" section of the [Metric Tree](./metrics-frameworks/metric-tree.md).

**If you want to see how I run experiments**: The [Experiment Design](./case-studies/pulse-digest-feature/03-experiment-design.md) shows full A/B test methodology including the sample size calculation.

**If you want to see my working style**: The [PM Operating System](./pm-operating-system/) shows the templates and frameworks I use daily — and the opinionated commentary around each one.

---

## Built With

These artifacts were generated using the [Claude Skills and Agents](../) toolkit — a collection of PM-focused AI workflows for drafting PRDs, designing experiments, synthesizing research, and more. The portfolio demonstrates both the output quality and how AI-native PMs can move faster without sacrificing rigor.
