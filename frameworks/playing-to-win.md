# Playing to Win

## What It Is

Playing to Win is a strategic framework developed by Roger Martin and A.G. Lafley (former P&G CEO) in their book of the same name. Its central argument: strategy is a set of integrated choices that position you to win against competitors and with customers. Strategy is not a vision, a plan, or a set of goals — it is a set of choices.

The framework organizes strategy as a **cascade of five choices**, each constrained by the others:

```
1. Winning Aspiration    ← What does winning look like?
         ↓
2. Where to Play         ← Which markets, segments, channels?
         ↓
3. How to Win            ← What's your competitive advantage?
         ↓
4. Capabilities          ← What must you be great at?
         ↓
5. Management Systems    ← What processes sustain the capabilities?
```

The choices must be mutually reinforcing. A "how to win" choice that requires capabilities you don't have and can't build is not a strategy — it's a wish.

---

## When to Use It

- Annual or quarterly strategy setting
- Entering a new market or segment
- Responding to a significant competitive move
- When the team is debating tactics without agreeing on strategy
- When the product roadmap feels disconnected from a "why we'll win" story

---

## How to Apply It (PM Context)

### Choice 1: Winning Aspiration
Not a mission statement. A specific definition of what winning looks like for your product in your market.

**Bad**: "Be the best team analytics platform."  
**Good**: "Be the tool that engineering managers at mid-market B2B SaaS companies use every week to understand and improve their teams."

Winning aspirations must be:
- Specific about who you're winning with
- Ambitious enough to require real choices
- Testable (you can know if you're winning or not)

### Choice 2: Where to Play
The most underrated choice. Where you don't play is as important as where you do.

Define:
- **Customer segment**: Exactly who (role, company size, industry, maturity)
- **Geography**: Where are you focusing first?
- **Channel**: How do you reach them (PLG, sales-led, partnership)?
- **Product category**: What job are you competing to do?
- **Price point**: Where in the value ladder?

Most importantly: **where are you explicitly NOT playing?** A where-to-play that includes everyone is not a choice.

### Choice 3: How to Win
The source of your competitive advantage in the chosen where-to-play. Must be durable (hard to copy) and relevant (customers value it).

Two generic winning positions:
- **Cost leadership**: You deliver acceptable quality at the lowest cost. Winning = being the cheapest viable option.
- **Differentiation**: You deliver superior value on one or more dimensions that matter to your target customer. Winning = being the best option for them, even at a price premium.

Most B2B SaaS companies are differentiation plays. The differentiation must be specific: "faster time-to-value" is vague. "Live in 3 days vs. competitors' 6-week implementations" is specific.

### Choice 4: Capabilities
The activities and competencies you must perform at a world-class level to win with your how-to-win. These are investments, not features — they take time to build and are hard to replicate.

### Choice 5: Management Systems
The processes, measurements, and structures that sustain your capabilities. Often ignored by product teams — but a capability without a supporting system degrades.

---

## Worked Example: Pulse

**Winning Aspiration**  
Be the analytics tool that engineering managers at mid-market B2B SaaS companies rely on to run their teams — used at least weekly, credited with meaningful improvements in team performance.

**Where to Play**
- Customer: Engineering managers (not HR, not executives) at B2B SaaS companies, 100–500 engineers
- Geography: English-speaking markets first (US, UK, Canada, Australia)
- Channel: Product-led growth — self-serve trial → convert → expand
- NOT playing: Large enterprise (>500 engineers), HR-owned purchases, non-tech industries

**How to Win**
Fastest time-to-value in the category. Managers see their first insight in under 3 days (competitors: 6–8 weeks). Built for the manager, not for HR or the executive — every design decision favors the person doing the work over the person measuring it.

**Capabilities Required**
1. Integration breadth + reliability (connects to Jira, GitHub, Slack in <1 hour)
2. Opinionated product design (surfaces what matters, doesn't overwhelm)
3. Manager-centric data model (team-level, not org-level)
4. Customer success at PLG scale (high-touch for enterprise, self-serve for mid-market)

**Management Systems**
- Weekly active user (WAU) reviewed every Monday — the north star drives every team review
- Time-to-first-insight measured per cohort — activation team accountable to this number
- Integration reliability SLA of 99.9% — eng team accountable to it in on-call rotation

---

## The Cascade Test

A good strategy passes the cascade test: every lower choice is enabled and constrained by the choice above it.

| If... | Then... |
|-------|---------|
| Winning aspiration is "weekly relied-upon tool" | Where-to-play must focus on a segment that has a recurring weekly management workflow |
| Where-to-play is mid-market engineering managers | How-to-win must be fast setup (they have no implementation budget) and manager-focused (they have no admin) |
| How-to-win is fastest TTV | Capabilities must include frictionless integration and opinionated defaults |
| Capabilities require opinionated design | Management systems must protect against roadmap scope creep toward "enterprise configurability" |

If any choice contradicts the choice above it, the strategy is incoherent.

---

## Common Mistakes

**Confusing aspiration with strategy.**  
"Be the market leader" is not a winning aspiration — it says nothing about who you're winning with or why. Make it customer-specific.

**Choosing everywhere to play.**  
A where-to-play that includes all segments, all channels, and all geographies is not a choice — it's a failure to choose. The most valuable thing about where-to-play is the explicit exclusions.

**How-to-win without a durable advantage.**  
"We win because we have better features" is not a how-to-win — features are copyable. A durable how-to-win is rooted in capabilities that take years to build: data network effects, proprietary integrations, brand trust, customer relationships.

**Building capabilities for where you want to be, not where you are.**  
Capabilities take time to build. The capabilities required for your 3-year aspiration may be different from the capabilities you need to survive this year. Stage the investment.

---

## Connections

- Use **[Eigenquestions](eigenquestions.md)** to find the most important unresolved choice in your cascade
- The `product-strategy` skill produces a one-pager that maps directly to the Playing to Win structure
- **[Wardley Mapping](wardley-mapping.md)** helps identify which capabilities are commoditizing and which are still differentiating — essential input to the "How to Win" choice
- The `thinking/principles.md` section on prioritization ("opportunity cost is the most underused concept in product") is the tactical expression of the where-to-play choice
