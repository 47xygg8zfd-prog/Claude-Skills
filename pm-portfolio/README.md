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

Nine product teardowns using a consistent framework: what the product really optimizes for, key metrics and what they reveal, JTBD, growth loop, retention mechanics, monetization alignment, strategic feature bets, weaknesses, and what I'd build next. Includes honest assessments of where competitors win.

| Teardown | Category | Key finding |
|----------|----------|-------------|
| [LinearB](./product-teardowns/linearb.md) | Direct competitor | Best-in-class git analytics; weak on actionability |
| [Swarmia](./product-teardowns/swarmia.md) | Direct competitor | Strong flow metrics; requires a data analyst to interpret |
| [Allstacks](./product-teardowns/allstacks.md) | Adjacent competitor | Serves execs, not managers — different buyer entirely |
| [Spotify](./product-teardowns/spotify.md) | Consumer benchmark | Habit formation and personalization at scale |
| [Linear](./product-teardowns/linear.md) | Adjacent tool | Opinionated UX as a growth strategy |
| [OpenAI](./product-teardowns/openai.md) | Platform | Developer ecosystem and API-first distribution |
| [Gemini](./product-teardowns/gemini.md) | Platform | Distribution leverage via Google integration |
| [Cursor](./product-teardowns/cursor.md) | Adjacent tool | Workflow integration as the moat |
| [Lovable](./product-teardowns/lovable.md) | Emerging tool | No-code AI product creation and viral loops |
| [Competitive Matrix](./product-teardowns/competitive-matrix.md) | — | 19-feature comparison across all products |

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

### 4. [Product Roadmap](./roadmap/)

A GitHub-style public roadmap for Pulse using the same labeling system as github/roadmap: release phases (exploring → in design → preview → beta → GA), quarter targets, product area, and plan tier. Includes a "What We're Not Building" table and a forward-looking statement disclaimer.

| Artifact | What it shows |
|----------|--------------|
| [Pulse Roadmap](./roadmap/pulse-roadmap.md) | Full roadmap across all phases with feature specs, success gates, and rollout plans |

---

### 5. [PM Operating System](./pm-operating-system/)

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

**If you want to see market awareness**: The [Product Teardowns](./product-teardowns/) show how I analyze competitors — including honest assessments of where they win and what I'd build if I were their PM.

**If you want to see how I communicate roadmap**: The [Product Roadmap](./roadmap/pulse-roadmap.md) shows a GitHub-style release-phase roadmap with specs, success gates, and explicit "not building" rationale.

**If you want to see my working style**: The [PM Operating System](./pm-operating-system/) shows the templates and frameworks I use daily — and the opinionated commentary around each one.

---

## Built With

These artifacts were generated using the [Claude Skills and Agents](../) toolkit — a collection of PM-focused AI workflows for drafting PRDs, designing experiments, synthesizing research, and more. The portfolio demonstrates both the output quality and how AI-native PMs can move faster without sacrificing rigor.
