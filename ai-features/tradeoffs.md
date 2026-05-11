# AI Feature Tradeoffs

How to reason about and communicate the core tradeoffs in AI feature decisions.

---

## The Core Triangle

Every AI feature involves three competing variables. You can optimize for two, not all three:

```
        Quality
          △
         / \
        /   \
       /     \
   Speed ———— Cost
```

- **High quality + low cost** = slow (use a large model with aggressive caching)
- **High quality + fast** = expensive (use a large model, pay full price)
- **Fast + cheap** = lower quality (use a smaller model or shorter prompts)

Be explicit with your team about which two you're optimizing for, and why.

---

## Model Selection Tradeoffs

| Model Tier | Examples | Best For | Tradeoff |
|------------|----------|----------|----------|
| Frontier / large | Claude Opus, GPT-4o | Complex reasoning, nuanced writing, high-stakes tasks | Highest quality, highest cost (~10–20× smaller models), higher latency |
| Mid-tier | Claude Sonnet | Most production tasks — good balance | Strong quality, moderate cost, ~1–3s latency |
| Small / fast | Claude Haiku | High-volume, latency-sensitive, simple tasks | Fastest + cheapest, quality drops on complex tasks |

**Default recommendation**: Start with a mid-tier model. Move to a smaller model if latency or cost is the bottleneck and quality holds. Move to a frontier model only if quality is genuinely insufficient.

---

## Latency Tradeoffs

Users tolerate different latency depending on context:

| Context | Acceptable Latency | Notes |
|---------|-------------------|-------|
| Inline suggestion (autocomplete) | <500ms | Anything slower feels broken |
| On-demand generation (button click) | 1–3s | Users expect some wait |
| Background task (async) | 5–30s | Acceptable if user is notified |
| Batch job (overnight) | Minutes–hours | Fine if results are ready when needed |

**Streaming** (progressive output rendering) dramatically improves perceived latency for on-demand generation. Implement streaming before optimizing for actual latency — it's cheaper and often sufficient.

---

## Cost Tradeoffs

Token costs compound at scale. Before launching:

**Estimate your monthly cost:**
```
monthly_cost = daily_requests × avg_input_tokens × input_price_per_token
             + daily_requests × avg_output_tokens × output_price_per_token
```

**Cost reduction levers (in order of impact):**

1. **Prompt caching** — Cache static parts of your system prompt. Most providers offer 50–90% discount on cached tokens. For prompts with a large static context (e.g., product docs, user profile), this is the single highest-ROI optimization.
2. **Smaller model** — Switching from frontier to mid-tier can cut costs 10×. Evaluate quality first.
3. **Shorter prompts** — Every token costs money. Remove verbose instructions, redundant context, unnecessary examples.
4. **Output length control** — Use `max_tokens` to cap output length. Many tasks don't need 2,000 tokens.
5. **Batching** — For non-real-time tasks, batch requests through Batch API (typically 50% discount).

---

## Quality vs. Speed vs. Cost: Decision Framework

| Scenario | Recommendation |
|----------|---------------|
| User-facing, real-time, high-stakes (e.g., customer-visible content) | Prioritize quality. Use mid-tier or frontier. Add human review gate. |
| User-facing, real-time, low-stakes (e.g., internal draft suggestions) | Balance quality and speed. Use mid-tier. Implement streaming. |
| High-volume, background, moderate quality needed (e.g., batch classification) | Prioritize cost. Use small model + Batch API. Eval rigorously. |
| Low-volume, high-stakes, async (e.g., quarterly reports, exec summaries) | Use frontier model. Cost is low at low volume; quality matters. |

---

## Communicating Tradeoffs to Stakeholders

When stakeholders ask "why isn't the AI better?", use this framing:

**The quality dial**:
> "AI quality exists on a spectrum. Right now we're at [X] quality. To move to [Y] quality costs us [Z] more per month / [N] more milliseconds per request. Here's what that gets us: [specific improvement]. Is that worth it?"

**The cost curve**:
> "At our current usage of [N] requests/day, this feature costs $[X]/month. If usage grows to [Y] requests/day (our 12-month projection), cost scales to $[Z]/month. Here are three ways we could reduce that: [options]."

**The accuracy bar**:
> "We've set a quality bar of 85% pass rate on our eval set. We're currently at [X]%. Each 5-point improvement requires roughly [effort estimate]. The business impact of hitting 95% vs. 85% is [impact]."
