# Skill: Pricing & Packaging

## Trigger Phrases
- "pricing tiers"
- "what should be in the free tier"
- "feature gating"
- "packaging design"
- "willingness to pay"
- "price this feature"
- "should this be an add-on"
- "compare our pricing to"
- "monetization strategy"

## Description
Design pricing tiers, feature gating, and packaging. Use when the user needs to define pricing tiers, decide which features go in which tier, model willingness-to-pay, compare to competitor pricing, or structure a packaging change.

## Behavior

### The Core Pricing Questions (answer before any output)

Every pricing engagement starts here:
1. **Who pays?** — the buyer persona, not the user persona; they are often different
2. **What do they pay for?** — the value they receive, not the cost to deliver it
3. **What's the value metric?** — the unit that scales with customer value (seats, usage, outcomes)
4. **What's the land-and-expand motion?** — how does a customer at Tier 1 naturally grow into Tier 2?

---

### Value Metric Framework

Choose the value metric before designing tiers. The wrong metric caps growth.

| Model | Best when | Avoid when |
|-------|-----------|------------|
| Per seat | Value scales with number of users | Power users dominate; most seats go unused |
| Per usage | Value is consumption-based (API calls, reports run) | Usage is unpredictable; customers fear surprise bills |
| Per outcome | Value is directly measurable (revenue generated, costs saved) | Outcomes are hard to attribute to your product |
| Flat fee | Simple sale, predictable buyer budget, early-stage | You're leaving money on the table as customers grow |

**Common mistake**: Pricing on your cost of delivery instead of customer value. Your infrastructure cost is irrelevant to what a customer will pay.

---

### Mode 1: Tier Design

Produce a table. Each tier must have a clear upgrade trigger — the moment a customer feels the constraint of their current tier.

| Tier | Target Customer | Price | Key Features Included | Key Features Excluded | Upgrade Trigger |
|------|----------------|-------|-----------------------|-----------------------|----------------|
| [Free / Starter] | [ICP at smallest scale] | $0 / $X/mo | [List] | [List] | [e.g., "hits 3-user limit"] |
| [Growth / Pro] | [ICP at mid scale] | $X/mo | [List] | [List] | [e.g., "needs SSO or advanced reporting"] |
| [Enterprise] | [ICP at full scale] | Custom | [List] | — | Contract renewal / expansion |

After the table: explain the packaging logic — why each feature is where it is, not just what tier it's in.

---

### Mode 2: Feature Gating Matrix

For each feature, apply the gating test:

> Does this feature make customers successful **at their current tier**, or does it make them successful **at the next tier**?

- If it makes them successful at their current tier: it belongs in that tier
- If it unlocks a new level of value: it's a gate to the next tier

| Feature | Current Tier | Gating Rationale | Upgrade Driver? |
|---------|-------------|-------------------|----------------|
| [Feature] | [Tier] | [Why it lives here] | Yes / No |

Flag features that are gated too aggressively (frustrating current customers) or too generously (removing upgrade incentive).

---

### Mode 3: Competitive Pricing Analysis

| Competitor | Tier Structure | Entry Price | Value Metric | Where They're Cheaper | Where You're Cheaper | Positioning Implication |
|------------|---------------|-------------|-------------|----------------------|---------------------|------------------------|
| [Name] | [Free/Pro/Enterprise] | $X/mo | [Seats/Usage] | [Features, segments] | [Features, segments] | [What this means for positioning] |

Conclude with: where you are overpriced relative to perceived value, where you are underpriced, and what the data suggests about repositioning.

---

### Packaging Rules

- The free tier must create genuine value, or it creates churn. A free tier that frustrates users is worse than no free tier.
- The upgrade path must be felt before it's offered. Customers upgrade when they hit a limit, not when they read a pricing page.
- Packaging changes are effectively irreversible. Customers anchor to current price and perceive any increase as a loss. Model this explicitly before recommending changes.
- Always model cannibalization risk: if you add a new lower tier, what percentage of current paying customers will downgrade?
- Add-ons work for features with uneven demand. If >60% of customers want it, it belongs in the base tier.

## Output Style
- State the value metric choice and rationale before any tier design
- Quantify cannibalization risk when modeling packaging changes
- Be direct about where pricing signals a positioning problem, not just a revenue opportunity

## Customization Tips
- Add your current tier names and prices to CLAUDE.md so Claude can use them as baseline
- Add your top competitors to the Key Competitors table in CLAUDE.md for automatic inclusion in competitive analysis
- Specify your land-and-expand motion so Claude can check tier design against it
