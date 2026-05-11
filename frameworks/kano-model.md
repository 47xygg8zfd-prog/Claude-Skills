# Kano Model

## What It Is

The Kano Model, developed by Professor Noriaki Kano in 1984, classifies product features by the relationship between their presence and customer satisfaction. The central insight: not all features create satisfaction in the same way. Some features, if absent, cause deep dissatisfaction — but their presence barely registers. Others delight customers when present but aren't missed when absent.

### The Five Categories

**1. Basic Needs (Must-Be Quality)**  
Features users expect as a given. Their absence causes serious dissatisfaction. Their presence produces no satisfaction — users don't notice them when they're there.

*Example*: Your analytics tool correctly calculates averages. Users don't think "great math!" They think nothing. But if the math is wrong, they notice immediately and lose trust.

**2. Performance Needs (One-Dimensional Quality)**  
Features where more is better and less is worse, linearly. Satisfaction scales with how well these are executed.

*Example*: Dashboard load time. Faster → more satisfied. Slower → less satisfied. Direct linear relationship.

**3. Delighters (Attractive Quality)**  
Features users didn't expect and don't ask for. Their absence causes no dissatisfaction (users don't know to miss them). Their presence creates disproportionate delight.

*Example*: Discover Weekly on Spotify. Nobody asked for an algorithm to make them a personalized playlist every Monday. When it appeared, it was delightful. Its absence wouldn't have been complained about.

**4. Indifferent**  
Features that produce no reaction either way — users don't care if they're there or not. These are waste.

**5. Reverse**  
Features that decrease satisfaction when present. Usually complexity-creating features that some users want but others find confusing or intrusive.

---

## The Kano Insight for PMs

**Basic needs don't win customers — they just don't lose them.**  
Investing heavily in perfecting basic needs is a trap. You're investing in not losing customers rather than in gaining or keeping them. Meet the bar, then move on.

**Performance needs are the battleground.**  
Most features a product team debates are performance needs. These are where execution quality separates winners from losers.

**Delighters become performance needs, then basic needs over time.**  
This is the most important dynamic in the model. Yesterday's delighter becomes today's expectation. Discover Weekly was a delighter in 2015. By 2020 it was a performance need. By 2025 its absence would be a disappointment. The decay timeline varies but is inevitable.

**Implication**: You must keep finding new delighters. The features that delighted your users 3 years ago are now basic needs — they create no satisfaction, only dissatisfaction if broken.

---

## How to Apply It

### Method 1: Kano Survey
For each feature, ask two questions:
1. **Functional**: How do you feel if this feature IS present? (delighted / expect it / neutral / tolerate it / dislike it)
2. **Dysfunctional**: How do you feel if this feature is NOT present? (delighted / expect it / neutral / tolerate it / dislike it)

Cross-tabulate responses to classify each feature.

### Method 2: Qualitative Classification
For smaller teams or faster cycles, classify features through structured discussion:

**Ask for each candidate feature:**
- "If we didn't have this, would customers cancel or complain loudly?" → Basic need
- "Does more/better of this always make customers happier?" → Performance need
- "Did we discover this from research, or did customers ask for it?" (asked for = usually performance, discovered = sometimes delighter)
- "Would customers be surprised and pleased by this?" → Delighter candidate

### Method 3: Retrospective Classification
Apply Kano to your existing feature set to find waste:
- Which features are customers indifferent to? (candidates for removal or deprioritization)
- Which former delighters are now basic needs? (where are you over-investing in polish?)
- Which performance needs are below par? (where is investment most urgent?)

---

## Worked Example: Pulse Features

| Feature | Category | Implication |
|---------|----------|-------------|
| Correct metric calculations | Basic Need | Fix bugs immediately; no investment in "better" math |
| Dashboard load time | Performance | Continuous investment; every 100ms matters |
| Jira integration | Basic Need (for ICP) | Must work reliably; not a differentiator |
| Weekly digest | Delighter → Performance | Was a surprise in beta; becoming expected as category matures |
| "Suggested action" in digest | Delighter | Customers didn't ask for it; creates disproportionate delight |
| Custom color themes | Indifferent | Low usage data confirms; deprioritize |
| Manager-level (not org-level) view | Performance | ICP cares deeply; more granularity = more satisfaction |
| Collaboration score algorithm | Reverse (for some) | Power users love it; some managers feel surveilled — segment carefully |

**How this changes roadmap decisions:**
- Don't invest engineering time making Jira integration "better" — make it reliable. It's a basic need.
- The "suggested action" in the digest is a delighter — protect it from scope cuts. It's creating satisfaction that data shows but users don't articulate in feature requests.
- Custom themes should be removed from the backlog. Indifferent features are noise.

---

## The Decay Curve

Track feature classification over time. A feature that was a delighter 18 months ago may now be a basic need. Re-survey annually (or when a significant competitor ships a similar feature).

```
Time →
Delighter → Performance Need → Basic Need

When a competitor ships your delighter,
the decay accelerates for your product too.
```

**Practical implication**: when a competitor ships a feature you don't have, check which Kano category it belongs to:
- If it's a delighter for them: you don't need to react immediately — users don't expect it from you yet
- If it was your delighter and is now a basic need: your moat just got smaller; respond faster

---

## Common Mistakes

**Building to the average.**  
Kano classifications vary by customer segment. A feature that's a delighter for power users may be indifferent to casual users. Segment your surveys and your classifications.

**Treating basic needs as low priority.**  
Basic needs don't create satisfaction — but they create serious dissatisfaction when broken. "The calculation is wrong" is a trust-destroying failure mode. Maintain basic needs with zero tolerance for regression.

**Confusing "customers asked for it" with "it's important."**  
Customers ask for performance needs. They rarely ask for delighters (they don't know to want them). The most valuable features you can build are the ones customers didn't know they needed — but you can only find those through deep research, not through request tracking.

**Not revisiting classifications.**  
A Kano map from 18 months ago is stale. The decay curve is real. Yesterday's delighters are today's basic needs.

---

## Connections

- Use Kano with **[Opportunity Solution Tree](opportunity-solution-tree.md)**: Kano classifies which opportunities to prioritize — delighters go at the top of the discovery backlog, indifferent opportunities get dropped
- Use with **[Feature Prioritization](../pm-skills/feature-prioritization/SKILL.md)**: add a Kano column to RICE scoring — basic needs get a "reliability floor" investment regardless of RICE score
- **[Second-Order Thinking](second-order-thinking.md)**: the decay curve is a second-order effect of competitive dynamics — Kano makes it visible
