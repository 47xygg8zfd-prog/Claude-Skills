# Skill: Product Strategy

## Trigger Phrases
- "write a product strategy"
- "product strategy for"
- "strategic one-pager for"
- "where should we focus"
- "what's our product bet"
- "define our product direction"
- "strategy doc for"
- "positioning for our product"

## Description
Write a product strategy one-pager or positioning brief that articulates where to play, how to win, and what to stop doing. Suitable for quarterly strategy reviews, new product bets, or executive alignment. Output is a decision-forcing document, not a roadmap.

## Behavior

When triggered, ask for:
1. Product name and one-line description
2. Current stage (pre-PMF / PMF / scaling / mature)
3. Top 2-3 growth or retention challenges right now
4. Key competitors and how you're positioned against them
5. Time horizon for the strategy (1 quarter / 1 year / 3 years)

Then produce:

---

### Product Strategy: [Product Name]
**Period**: [Quarter or year]  
**Author**: [Name]  
**Status**: Draft / Reviewed / Approved  

---

#### The Situation
[2-3 sentences. What's true about the market and our position right now that makes this strategy necessary? Be specific — cite a metric, a competitor move, or a customer signal.]

---

#### Where We Play

**Target customer**: [Specific ICP — not "SMBs" but "engineering managers at 100-500 person SaaS companies using Jira"]

**Use case focus**: [The specific job-to-be-done we're winning on — not everything the product does, but the use case where we're the best choice]

**Where we're NOT playing**: [Explicit out-of-scope segments, use cases, or markets — and why]

---

#### How We Win

Our durable advantage in the target use case:

1. **[Advantage 1]**: [Why it's hard to replicate and how it compounds]
2. **[Advantage 2]**: [Why it's hard to replicate and how it compounds]

**Why we win vs. [Competitor A]**: [One sentence]  
**Why we win vs. [Competitor B]**: [One sentence]  
**Where we lose honestly**: [Situations where a competitor is genuinely better — builds credibility]

---

#### The Bets

The 2-3 strategic bets we're making this period:

**Bet 1: [Name]**  
*Hypothesis*: If we [investment], then [outcome] because [reason].  
*Evidence*: [What signal supports this bet]  
*Risk*: [What would make this wrong]  
*Investment*: [Rough eng + PM capacity]  

**Bet 2: [Name]**  
[Same structure]

**Bet 3: [Name]** *(optional)*  
[Same structure]

---

#### What We're Stopping

[List 2-3 things we're explicitly deprioritizing or stopping. A strategy without cuts isn't a strategy.]

| What | Why We're Stopping |
|------|--------------------|
| [Feature / initiative] | [Honest reason — not enough impact, wrong segment, too expensive] |
| [Feature / initiative] | |

---

#### How We'll Know It's Working

| Signal | Timeframe | Threshold |
|--------|-----------|-----------|
| [Leading indicator] | 4 weeks | [Target] |
| [North star metric] | 12 weeks | [Target] |
| [Business metric] | 6 months | [Target] |

---

#### Open Questions

[2-4 questions that, if answered differently, would change the strategy. These should be genuine uncertainties, not rhetorical.]

1. [Question]
2. [Question]

---

## Output Style
- One page maximum — if it doesn't fit on one page, the strategy isn't clear yet
- The "Where We're NOT Playing" and "What We're Stopping" sections are mandatory — a strategy that tries to do everything is not a strategy
- Every bet should have an explicit risk — strategies with no acknowledged risks aren't honest
- Write for a smart executive who has 5 minutes, not a team that will read every word

## Customization Tips
- Add your company's strategic framework to CLAUDE.md if you use one (e.g. "Playing to Win," "Good Strategy Bad Strategy")
- Add your ICP and current positioning so Claude can populate the competitive framing automatically
- Add your current OKRs so the "How We'll Know It's Working" section ties to existing targets
