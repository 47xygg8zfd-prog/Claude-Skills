# Wardley Mapping

## What It Is

A Wardley Map is a visual tool for understanding the competitive landscape and making strategic decisions about where to invest. Developed by Simon Wardley, it plots the components of a value chain on two axes:

- **X-axis (Evolution)**: How mature/commoditized is this component? From left (genesis / novel) to right (commodity / utility)
- **Y-axis (Value Chain)**: How visible is this to the customer? From top (user-facing) to bottom (foundational infrastructure)

```
Visible to user
      ↑
      │  [User Need]
      │      │
      │  [Feature A]──[Component B]──[Commodity C]
      │                    │
      │              [Component D]
      │
      ↓
Invisible to user
      
      Genesis ──── Custom ──── Product ──── Commodity
                        (Evolution →)
```

The map reveals:
- **Where you're competing on commodity** (waste — buy/outsource this)
- **Where you're competing on differentiation** (invest here)
- **Where the market is moving** (components evolve left to right — today's differentiator becomes tomorrow's commodity)
- **Where competitors are exposed** (if they're building custom what you can buy as commodity, they're slower and more expensive)

---

## When to Use It

- Annual strategy setting — to identify where your competitive advantage actually lives
- Build vs. buy decisions — is this component in genesis (build) or commodity (buy)?
- Identifying inertia — the things your company is building custom because "that's how we've always done it"
- Responding to competitive moves — where on the evolution curve is your competitor's new feature?
- Identifying where AI will disrupt your category (AI shifts many "custom" components toward commodity)

---

## The Evolution Stages

| Stage | Characteristics | Strategic Implication |
|-------|----------------|----------------------|
| **Genesis** | Novel, uncertain, high variance, created by pioneers | Experiment; expect failure; first-mover advantage possible |
| **Custom** | Understood but still hand-crafted; significant expertise required | Build if it's your differentiator; buy if it isn't |
| **Product** | Available as packaged products; reproducible; feature competition | Evaluate build vs. buy carefully; commodity approaching |
| **Commodity / Utility** | Standardized, highly reliable, available as a service | Buy/subscribe; building custom is waste |

---

## How to Build a Wardley Map

### Step 1: Identify the user need
Start at the top of the map — what does the user need? This is the anchor. Every component on the map exists to serve this need.

### Step 2: Map the value chain
Work downward: what components are required to deliver the user need? For each component, what does it depend on? Keep decomposing until you reach commodity infrastructure.

### Step 3: Place components on the evolution axis
For each component, ask:
- Is this something only a few organizations in the world can do? (Genesis)
- Does it require significant expertise to build and maintain? (Custom)
- Can you buy it as a packaged product from vendors? (Product)
- Can you subscribe to it as a utility? (Commodity)

### Step 4: Draw dependencies
Connect components with lines showing dependencies. Flow generally goes left to right (more custom → more commodity) as you move down the value chain.

### Step 5: Identify strategic implications
- **Red flags**: Components in the commodity zone that you're building custom (you're wasting engineering time)
- **Opportunities**: Components moving rightward (toward commodity) that your competitors are still building custom — you can buy cheap what they're building expensive
- **Moats**: Components in the custom/genesis zone that are unique to you and hard to replicate

---

## Worked Example: Pulse

**User Need**: Engineering managers understand and improve their team's performance

```
[Manager understands team performance]
              │
    ┌─────────┴──────────┐
    │                    │
[Team insights]    [Benchmarks]
    │                    │
[Data model]      [Industry data]         ← Custom → moving to Product
    │                    │
[Integrations]    [ML models]             ← Custom (integrations) / Product (ML)
    │                    │
[APIs]           [Cloud compute]          ← Commodity
    │                    │
[OAuth]          [Data storage]           ← Commodity
```

**Strategic reads from this map:**

| Component | Current Stage | Implication |
|-----------|--------------|-------------|
| Team insight algorithms | Custom | This is Pulse's moat — keep building |
| Jira/GitHub integrations | Moving to Product (integration platforms emerging) | Consider buying via Merge.dev or similar; don't build custom for each |
| ML models (recommendation) | Product (OpenAI, Anthropic APIs available) | Buy via API; don't build custom models |
| Cloud compute | Commodity | AWS/GCP; never build custom infrastructure |
| Data storage | Commodity | Snowflake/BigQuery; standard choice |
| OAuth / SSO | Commodity | Auth0 or Clerk; building custom is waste |

**The insight**: Pulse's engineers should be spending the vast majority of their time on the top two rows (insights, data model, product UX) — that's where differentiation lives. Every hour spent on OAuth, cloud infrastructure, or generic ML is an hour not spent on competitive advantage.

**Competitive threat read**: If Teamlytics builds custom ML models for team analytics, and Pulse buys the same capability via API for 1/10th the cost, Pulse can move faster and cheaper. Watch for Teamlytics job postings for ML engineers — it signals misplaced investment.

---

## The Movement Rule

Components always evolve from left to right — genesis → custom → product → commodity. They never evolve backwards.

**Implication**: Where your differentiator is today is not where it will be in 5 years. The custom analytics algorithms that make Pulse special today will be available as a commodity API in 3-5 years. The strategic question is: what are you doing now to build the *next* differentiator before this one commoditizes?

---

## Wardley Mapping and AI

AI is accelerating evolution across many software categories. Components that were "custom" two years ago (NLP, image recognition, text generation) are now "commodity" via APIs. This has strategic implications:

- **If your moat was custom ML**: that moat is shrinking faster than you think
- **If your competitor had a custom ML advantage**: their advantage may now be replicable cheaply via API
- **The new moat**: proprietary data, customer trust, and distribution — things AI can't commoditize

---

## Common Mistakes

**Making it too detailed.**  
A Wardley Map with 50 components is unreadable. Start with 10-15 components. Add detail only where strategic decisions depend on it.

**Treating evolution stages as fixed.**  
Components move. Reassess annually, or when a major platform player enters the space (which accelerates commoditization).

**Using it to justify current investments.**  
The map should challenge what you're building, not justify it. If every component maps to "custom" and "we should build it," the map is being used to confirm bias.

**Building maps alone.**  
The map is most valuable when challenged by people who disagree with your placement of components. An unchallenged map is just your assumptions drawn as a diagram.

---

## Connections

- **[Playing to Win](playing-to-win.md)**: Wardley Maps inform the "Capabilities" and "How to Win" choices — you can only sustain differentiation on components in the custom/genesis zone
- **[Second-Order Thinking](second-order-thinking.md)**: the evolution movement is a second-order dynamic — your competitor's move commoditizes your moat before you see the threat directly
- The `ai-features/tradeoffs.md` section on build vs. buy is the practical expression of Wardley's evolution axis applied to AI components
- **[Kano Model](kano-model.md)**: Kano's decay curve (delighters become basic needs) mirrors Wardley's evolution — delighters live on the left side of the map; basic needs have moved to the right
