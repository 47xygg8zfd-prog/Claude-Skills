# Skill: North Star Metric

## Trigger Phrases
- "define our north star metric"
- "what should our north star be"
- "help me pick the right metric"
- "our primary metric for"
- "what's the one metric that"
- "north star for"
- "define success for our product"

## Description
Define, evaluate, and defend a North Star Metric (NSM) — the single metric that best captures the value your product delivers to customers and predicts long-term business health. Covers metric selection criteria, input metric trees, common pitfalls, and how to communicate the NSM to the team.

## Behavior

When triggered, ask for:
1. What the product does (one sentence)
2. Who the primary user is
3. What value the product delivers to that user
4. Current metrics the team tracks (if any)

Then produce:

### 1. North Star Metric Recommendation

State the recommended NSM and explain why it meets the criteria:

**A good North Star Metric:**
- Measures value delivered to the user (not just revenue or activity)
- Leads revenue (companies with high NSM eventually have high revenue, not the reverse)
- Is sensitive enough to move week-over-week
- Is understandable by the full team — eng, design, CS, and sales
- Can be decomposed into input metrics the team can influence

**NSM**: [Metric name]  
**Definition**: [Precise calculation]  
**Why this**: [2-3 sentence rationale tying it to user value and business health]  
**Leading indicator for**: [Which business metric it predicts]

---

### 2. Why Common Alternatives Fall Short

For each obvious alternative metric, explain why it's worse:

| Alternative | Problem |
|------------|---------|
| Revenue / MRR | Lags user value; can grow while product quality declines |
| DAU / MAU | Measures presence, not value; inflated by low-quality engagement |
| [Other suggested metric] | [Specific issue] |

---

### 3. Input Metric Tree

Decompose the NSM into 4-6 input metrics the team can directly influence:

```
North Star Metric
├── Input 1: [Metric] — influenced by [team/initiative]
├── Input 2: [Metric] — influenced by [team/initiative]
├── Input 3: [Metric] — influenced by [team/initiative]
└── Input 4: [Metric] — influenced by [team/initiative]
```

Each input metric should:
- Be measurable independently
- Have a clear owner
- Move the NSM when it improves

---

### 4. Counter-Metrics (Guardrails)

Identify 2-3 metrics that must not decline when optimizing for the NSM:

| Counter-metric | Why it matters | Acceptable threshold |
|---------------|---------------|---------------------|
| [Metric] | [Risk if ignored] | [Floor or ceiling] |

---

### 5. How to Roll It Out

A NSM only works if the team believes in it and uses it. Recommended rollout:

1. **Validate with data**: Show the historical correlation between the proposed NSM and retention/revenue before announcing it
2. **Pressure-test with the team**: Have engineering, design, and CS challenge the metric — if they can find easy ways to inflate it without creating real value, it's the wrong metric
3. **Dashboard it prominently**: The NSM should be the first number anyone sees in weekly reviews
4. **Tie quarterly OKRs to it**: At least one KR per quarter should directly connect to moving the NSM

---

### 6. Common NSM Anti-Patterns

Flag if the proposed metric falls into one of these traps:

| Anti-pattern | Example | Problem |
|-------------|---------|---------|
| Vanity metric | Total signups | Doesn't measure retained value |
| Gameable metric | Logins | Easy to inflate without value |
| Lagging indicator | NPS | Moves too slowly to guide decisions |
| Activity proxy | Messages sent | Measures effort, not outcomes |
| Revenue metric | MRR | Lags user value; can mask churn |

## Output Style
- Be direct about tradeoffs — every NSM has weaknesses; name them
- Show the input metric tree visually, not just as a list
- Push back if the suggested metric is a vanity metric or revenue metric disguised as a NSM

## Customization Tips
- Add your current top metrics to CLAUDE.md so Claude can evaluate them against NSM criteria
- Add your product stage — early-stage products often need a different NSM than growth-stage products (acquisition vs. retention focus)
- Add your business model so Claude can assess whether the NSM leads the right revenue driver
