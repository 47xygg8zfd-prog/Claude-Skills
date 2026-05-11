---
name: tech-translation
description: >
  Decode technical engineering conversations, architecture discussions, and jargon into clear
  PM-friendly language. Explain technical tradeoffs, system design decisions, and engineering
  concepts so PMs can participate meaningfully in technical discussions and make informed decisions.
  Use this skill whenever the user wants to understand a technical concept, decode what engineers
  said in a meeting, evaluate a technical tradeoff, or explain an engineering decision to stakeholders.
  Also trigger for phrases like "what does X mean", "engineers said Y, what does that mean for us",
  "explain this architecture", "help me understand the tradeoff", "translate this for me", or
  "what questions should I ask engineering about X".
---

# Tech Translation Skill

Bridge the gap between engineering and product. Understand technical concepts, decode jargon, and
participate meaningfully in technical discussions.

---

## Core Principle

You don't need to understand how to *build* it. You need to understand:
1. **What it does** (user/business impact)
2. **What it costs** (time, complexity, risk)
3. **What the tradeoffs are** (why they chose this approach)
4. **What could go wrong** (risks you need to plan around)

---

## Common Engineering Concepts Decoded

### Architecture & Infrastructure

| Engineers Say | PM Translation |
|--------------|----------------|
| Microservices | App is split into small independent services — more flexible but more complex to manage |
| Monolith | Everything is one big app — simpler to build, harder to scale |
| API / REST / GraphQL | How two systems talk to each other. REST = standard; GraphQL = more flexible queries |
| Event-driven / Message queue | Systems communicate asynchronously — decoupled, more resilient but harder to trace |
| Cache / Redis | Store frequently-used data in fast memory so we don't hit the database every time |
| CDN | Serve static content (images, JS) from servers close to the user — speeds up load times |
| Load balancer | Distributes traffic across multiple servers — handles scale, adds resilience |
| Database sharding | Splitting a database into smaller pieces — needed for scale, adds complexity |

### Performance & Reliability

| Engineers Say | PM Translation |
|--------------|----------------|
| Latency | Time between user action and system response |
| Throughput | How many operations per second the system can handle |
| P95 / P99 latency | 95% / 99% of requests are faster than X ms — the "worst case" experience |
| Uptime / SLA | % of time the service is available. 99.9% = ~9 hrs downtime/year |
| Race condition | Two things happen at the same time and conflict — causes intermittent, hard-to-reproduce bugs |
| Memory leak | App slowly uses more memory over time until it crashes — needs a fix, not a restart |
| Technical debt | Shortcuts taken earlier that slow us down now — needs to be paid back eventually |

### Development Practices

| Engineers Say | PM Translation |
|--------------|----------------|
| Refactor | Rewrite code to be cleaner/faster without changing behavior — invisible to users |
| Feature flag | On/off switch for a feature in production — enables gradual rollouts and A/B tests |
| Canary deployment | Roll out to a small % of users first to catch issues before full release |
| A/B test / experiment | Split traffic to test two variants — you'll need to define the metric |
| CI/CD | Automated testing + deployment pipeline — changes ship faster and more safely |
| Test coverage | % of code covered by automated tests — higher = safer to change |
| Regression | A bug that re-appears after being fixed — often caught by automated tests |
| Integration test / E2E | Tests that verify the full user flow works end-to-end |

### Data & Storage

| Engineers Say | PM Translation |
|--------------|----------------|
| Schema | The structure/shape of the data (what columns/fields exist) |
| Migration | Changing the database structure — can be slow/risky on large tables |
| Backfill | Re-processing historical data with new logic — time-consuming, one-time job |
| ETL / pipeline | Extract, Transform, Load — moving data from one system to another |
| Data lake | Dumping ground for raw data — cheap storage, queried later |
| Data warehouse | Cleaned, structured data optimized for analysis (e.g., Snowflake) |
| Eventual consistency | Data will be correct *eventually* — brief windows where it might look stale |

---

## Tradeoff Frameworks

When engineers present options, use this mental model:

### The 3-Way Tradeoff
You usually can't have all three:
```
      FAST
       ▲
      /|\
     / | \
    /  |  \
CHEAP─────GOOD
```
Pick two. Ask engineers which two they're optimizing for.

### Build vs. Buy vs. Borrow
| Option | When to Choose |
|--------|---------------|
| Build | Core differentiator, no good external option, long-term need |
| Buy | Commodity capability, fast time-to-value, not a differentiator |
| Borrow (open source) | Good community support, acceptable license, you have eng capacity to maintain |

### Tradeoff Questions to Ask
- "What's the cost of doing this the right way vs. the fast way?"
- "If we take this shortcut now, when does the debt come due?"
- "What's the blast radius if this fails in production?"
- "Is this reversible? Can we roll back if something goes wrong?"
- "What monitoring will we have — how will we know if this breaks?"

---

## Questions to Ask in Technical Meetings

### When Engineers Propose a Solution
1. "What problem is this solving?" (Make sure you agree on the problem)
2. "What alternatives did you consider and why did you rule them out?"
3. "What are the failure modes — what could go wrong?"
4. "How will we know if this is working?" (Metrics, monitoring)
5. "Is this reversible?"
6. "What's the estimated effort and what are the main unknowns?"

### When You Hear "That's Not Technically Possible"
Gentle follow-ups:
- "Can you help me understand the constraint? Is it time, complexity, or something else?"
- "Is there a simpler version that achieves 80% of the goal?"
- "What would it take to make it possible in a future sprint?"

### When Estimates Feel Off
- "Can you walk me through what's driving the estimate?"
- "What are the biggest unknowns that could make this take longer?"
- "Is there a way to de-risk the biggest unknown first?"

---

## Meeting Debrief Mode

If the user says "we just had a technical meeting, help me understand what was decided":

1. Ask them to paste their notes or describe what was discussed
2. Extract: What was the decision? What were the options? What were the tradeoffs?
3. Translate into PM-relevant implications: timeline impact, user impact, risk
4. Surface follow-up questions the PM should ask
5. Suggest how to communicate the decision to stakeholders

---

## Explaining Technical Concepts to Stakeholders

Use this structure:
```
1. What we're doing: [1 sentence, plain language]
2. Why it matters: [user or business benefit]
3. What it means for the timeline: [any impact on delivery]
4. The risk: [what could go wrong, how we're mitigating]
```

**Example:**
> We're migrating our user authentication system to a new provider. This means users will have a more secure login experience and we'll support SSO for enterprise customers. The migration will take 3 sprints and requires a maintenance window of ~2 hours. We're mitigating risk by migrating 5% of users first and monitoring for issues before the full rollout.

---

## Integration Points
- Use **prd** skill to document technical decisions and their product implications
- Use **agile-stories** skill to write technical stories after understanding engineering approach
- Use **pptx** skill to explain technical architecture to non-technical stakeholders
