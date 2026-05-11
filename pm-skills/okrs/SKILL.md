# Skill: OKRs

## Trigger Phrases
- "write OKRs for"
- "help me set objectives"
- "draft key results for"
- "score my OKRs"
- "check in on OKRs"
- "are we on track for"
- "flag at-risk goals"
- "quarterly goals for"

## Description
Write, score, and check in on Objectives and Key Results. Covers drafting OKRs from strategy inputs, mid-cycle scoring, identifying at-risk KRs, and producing check-in summaries for stakeholders.

## Behavior

### Mode 1: Draft OKRs
Ask the user for:
1. Team or individual name
2. Time period (quarter/year)
3. Strategic priorities or themes (rough bullets are fine)
4. Any carry-over goals from prior cycle

Produce:

**Objective**: [Inspirational, qualitative goal — one sentence, present-tense, outcome-oriented]

| Key Result | Target | Measurement Method | Owner |
|------------|--------|--------------------|-------|
| KR1: ...   | ...    | ...                | ...   |
| KR2: ...   | ...    | ...                | ...   |
| KR3: ...   | ...    | ...                | ...   |

Rules enforced:
- Objectives are qualitative and motivating (not a task)
- Key Results are measurable, time-bound, and binary or numeric
- 2-5 KRs per Objective
- No "do X" KRs — only "achieve Y outcome"

### Mode 2: Score / Check-in
Ask the user for:
1. OKRs (paste existing ones)
2. Current progress data per KR

Produce:

| Key Result | Target | Current | Score (0–1.0) | Status | Risk |
|------------|--------|---------|---------------|--------|------|
| ...        | ...    | ...     | ...           | ...    | ...  |

**Score guidance**: 0.7 is success; 1.0 means target was too easy; <0.4 is at-risk.

Follow with:
- **At-Risk KRs**: What's blocking them and recommended interventions
- **On-Track KRs**: Brief confirmation
- **Check-in narrative**: 3-5 sentence summary suitable for a team or exec update

### Mode 3: Retrospective
At end of cycle, produce a structured OKR retrospective:
- Final scores per KR
- What drove results (or didn't)
- Carry-forward recommendations for next cycle

## Output Style
- Direct and data-driven
- Flag KRs that are activity-based (not outcome-based) and suggest rewrites
- Check-in narratives should be copy-pasteable into Slack or email

## Customization Tips
- Add company-level OKRs so Claude can check team OKRs for alignment
- Add your scoring rubric if it differs from the standard 0–1.0 scale
- Add team members so Claude can suggest KR owners automatically
