# Workflow: Research to Roadmap

How to go from raw customer and market signals to a defensible quarterly roadmap.

---

## Overview

```
Customer Research Synthesis
        +
Competitive Analysis
        ↓
Feature Prioritization
        ↓
      OKRs
        ↓
PM Presentations (roadmap deck)
        ↓
Stakeholder Updates (ongoing)
```

---

## Step 1: Synthesize Customer Research

**Skill**: `customer-research-synthesis`  
**Input**: All research collected in the prior quarter — interviews, NPS, support themes, churn exit surveys  
**Output**: Ranked themes, JTBD statements, opportunity statements

**Tip**: Run this separately for different segments (e.g., SMB vs. Enterprise, new users vs. power users). The themes often differ significantly and should drive different roadmap bets.

---

## Step 2: Run Competitive Analysis

**Skill**: `competitive-analysis`  
**Input**: Any new intel — competitor release notes, G2 reviews, lost deals, sales battlecard feedback  
**Output**: Updated teardowns, gap analysis, positioning refresher

**What to look for**:
- Features competitors shipped that customers are now asking you for (table stakes signal)
- Features you have that competitors don't (reinforce in roadmap narrative)
- Segments competitors are moving into (inform your ICP focus)

**Combine with Step 1**: Cross-reference competitor gaps with customer opportunity statements. The highest-value roadmap items sit at the intersection of "customers want this" and "competitors don't do it well."

---

## Step 3: Prioritize Features

**Skill**: `feature-prioritization`  
**Input**: Long list of candidates from research (Step 1) and competitive gaps (Step 2)  
**Output**: RICE-ranked shortlist for the quarter

**Prompt to start**:
```
Prioritize this feature list for [quarter] using RICE.
Strategic context: [paste top 2-3 opportunity statements from Step 1]
Competitive context: [paste top gaps from Step 2]
OKRs we're targeting: [paste current OKRs]
Features to evaluate:
[list]
```

---

## Step 4: Set OKRs

**Skill**: `okrs`  
**Input**: Top prioritized features (Step 3), company-level goals  
**Output**: Team OKRs with measurable key results tied to the roadmap

**Sequence matters**: Set OKRs *after* prioritization, not before. OKRs should reflect what you've committed to building — not the other way around. This prevents OKRs from becoming a post-hoc rationalization of already-decided work.

**Prompt to start**:
```
Draft Q[N] OKRs for our product team.
We're focused on: [paste top 3 RICE winners from Step 3]
Company-level goals: [paste if available]
Prior quarter carry-overs: [any unfinished KRs]
```

---

## Step 5: Build the Roadmap Deck

**Skill**: `pm-presentations`  
**Input**: Prioritized features (Step 3), OKRs (Step 4), competitive context (Step 2)  
**Output**: Roadmap presentation for exec or all-hands

**Prompt to start**:
```
Build a roadmap presentation for [audience: exec / all-hands / board].
Quarter: [Q and year]
Top bets: [paste top 3-5 RICE winners]
OKRs: [paste from Step 4]
What we're NOT doing: [top deprioritized items and why]
Competitive context to include: [optional — 1-2 key points from Step 2]
```

**Slide structure to request**:
1. The problem we're solving this quarter (rooted in research)
2. Our bets (roadmap themes, not a feature list)
3. How we'll know if we won (OKRs / success metrics)
4. What we're not doing and why
5. Dependencies and risks

---

## Step 6: Communicate Progress

**Skill**: `stakeholder-updates`  
**Use throughout the quarter**: Weekly status updates keep stakeholders aligned without requiring all-hands updates.

**Prompt to start each week**:
```
Write a weekly status update for [project/initiative].
Status: [On Track / At Risk / Blocked]
This week: [bullet points]
Next week: [bullet points]
Blockers: [any, with owner and deadline]
```

---

## Tips

- **Do Steps 1 and 2 in parallel.** Customer research and competitive analysis inform each other — a competitor strength is only a threat if customers care about it.
- **Separate "now" from "next."** Prioritization (Step 3) answers Q[N]. Keep a separate "later" list that feeds Q[N+1] planning.
- **Show the cuts.** The strongest roadmap presentations include a "what we're not doing" slide. It builds trust with engineers (no scope creep) and executives (disciplined tradeoffs).
- **OKRs anchor the narrative.** Every roadmap bet should connect to an OKR. If a feature doesn't move a key result, either cut it or add the right KR.
