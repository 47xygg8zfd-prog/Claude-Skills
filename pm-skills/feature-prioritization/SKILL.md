# Skill: Feature Prioritization

## Trigger Phrases
- "prioritize these features"
- "RICE score this"
- "rank these by impact"
- "help me prioritize my backlog"
- "impact effort matrix"
- "MoSCoW this"
- "what should we build first"

## Description
Score, rank, and justify feature prioritization using RICE, ICE, MoSCoW, or impact/effort frameworks. Outputs a ranked table with scores and a short rationale for each decision.

## Behavior

When triggered, ask the user for:
1. A list of features or initiatives (can be rough bullet points)
2. Preferred framework (default to RICE if not specified)
3. Any hard constraints (deadlines, dependencies, team size)

Then produce:

### RICE Output Format
| Feature | Reach | Impact | Confidence | Effort | RICE Score | Recommendation |
|---------|-------|--------|------------|--------|------------|----------------|
| ...     | ...   | ...    | ...        | ...    | ...        | ...            |

**RICE Score** = (Reach × Impact × Confidence) / Effort

- **Reach**: Users affected per quarter (numeric estimate)
- **Impact**: 0.25 / 0.5 / 1 / 2 / 3 scale
- **Confidence**: % certainty in estimates (100% / 80% / 50%)
- **Effort**: Person-months

### MoSCoW Output Format
Categorize each feature as Must Have / Should Have / Could Have / Won't Have this cycle, with a one-line justification per item.

### Impact/Effort Matrix Output Format
Place features into four quadrants:
- **Quick Wins** (high impact, low effort) — do first
- **Big Bets** (high impact, high effort) — plan carefully
- **Fill-ins** (low impact, low effort) — do if capacity allows
- **Money Pits** (low impact, high effort) — deprioritize or cut

## Output Style
- Lead with the ranked table
- Follow with a 3-5 sentence rationale explaining the top picks
- Flag any features with high uncertainty that need more data before scoring
- Keep tone direct and decision-ready — this output goes into planning meetings

## Customization Tips
- Add your team's default sprint velocity to calibrate Effort scores
- Add OKRs to weight Impact scores toward current goals
- Add "strategic alignment" as a custom RICE multiplier for executive prioritization
