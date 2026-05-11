# Skill: Competitive Analysis

## Trigger Phrases
- "competitive analysis for"
- "compare us to"
- "competitor teardown"
- "win/loss analysis"
- "how do we stack up against"
- "positioning vs"
- "battlecard for"
- "what are competitors doing"
- "analyze the competitive landscape"

## Description
Produce structured competitor teardowns, win/loss summaries, positioning matrices, and sales battlecards. Works from user-supplied research, product descriptions, or feature lists — does not browse the web.

## Behavior

When triggered, ask the user for:
1. Your product and its core value proposition
2. Competitor(s) to analyze
3. Available input (feature lists, pricing pages, sales call notes, win/loss data, customer quotes)
4. Output type needed (see modes below)

### Mode 1: Competitor Teardown
For each competitor, produce:

**[Competitor Name]**
- **Positioning**: How they describe themselves
- **Target customer**: Who they go after
- **Key strengths**: Top 3 (evidence-based)
- **Key weaknesses**: Top 3 (evidence-based)
- **Pricing model**: Structure and known tiers
- **Recent moves**: Product launches, funding, partnerships, hiring signals
- **Threat level**: Low / Medium / High + rationale

---

### Mode 2: Feature Comparison Matrix
| Feature / Capability | Your Product | Competitor A | Competitor B | Competitor C |
|----------------------|-------------|--------------|--------------|--------------|
| [Feature]            | ✅ / ❌ / 🔶 | ...          | ...          | ...          |

Legend: ✅ Strong  🔶 Partial  ❌ Missing

Follow with:
- **Where you win**: Features with clear advantage
- **Where you lose**: Gaps to prioritize
- **Table stakes**: Features all players have (deprioritize investment here)

---

### Mode 3: Win/Loss Analysis
Ask the user for win/loss data (deal notes, CRM reasons, customer quotes).

Produce:
| Reason | Win % | Loss % | Pattern |
|--------|-------|--------|---------|
| ...    | ...   | ...    | ...     |

Follow with:
- **Top win themes**: What's driving wins
- **Top loss themes**: What's driving losses
- **Recommended actions**: Product, pricing, or sales enablement responses

---

### Mode 4: Positioning Matrix
Plot competitors on two axes chosen by the user (e.g. Enterprise vs. SMB, All-in-one vs. Point solution).

Describe the matrix in text, then provide a summary of where whitespace exists and where it's crowded.

---

### Mode 5: Sales Battlecard
One-page format for sales/CS use:

**[Competitor] Battlecard**

- **When you'll face them**: [Deal types, segments]
- **Their pitch**: What they lead with
- **Our counter**: How to reframe
- **Landmines to plant**: Questions that expose their weaknesses
- **Proof points**: Customer quotes or data that support our position
- **When we lose**: Honest situations where they're a better fit (builds credibility)

## Output Style
- Evidence-based: attribute claims to sources when provided
- Flag low-confidence claims (inferred vs. confirmed)
- Battlecards: punchy and scannable — sales reps read these in 30 seconds before a call
- Teardowns: thorough and structured for PM/strategy audiences

## Customization Tips
- Add your ICP (ideal customer profile) so comparisons stay relevant to your segment
- Add your key differentiators so Claude can consistently reinforce positioning
- Add known competitors by name so trigger detection is faster
- Add win/loss data as context for battlecard generation
