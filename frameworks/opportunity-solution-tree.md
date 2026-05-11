# Opportunity Solution Tree

## What It Is

The Opportunity Solution Tree (OST) is a visual framework developed by Teresa Torres for connecting a desired outcome to the opportunities that could deliver it, the solutions that could address those opportunities, and the experiments that validate those solutions.

The tree structure makes the relationships explicit:

```
          Outcome
         /   |   \
        O1   O2   O3        ← Opportunities (customer needs, pain points, desires)
       / \       / \
      S1  S2   S3  S4       ← Solutions (features, design changes, experiments)
      |    |    |
     E1   E2   E3           ← Experiments (assumption tests, prototypes, A/B tests)
```

The core insight: most product teams jump from outcomes directly to solutions, skipping the opportunity layer. This produces solutions that address the wrong problem, or multiple solutions competing for the same problem without knowing it. The OST forces you to be explicit about what opportunity each solution is addressing.

Popularized in Teresa Torres's book *Continuous Discovery Habits*.

---

## When to Use It

- At the start of a discovery cycle, to structure your opportunity space before generating solutions
- When the team has a backlog full of solutions but no shared understanding of why
- When multiple stakeholders are pushing different solutions that seem unrelated
- When A/B tests keep showing neutral results — often a sign you're in the wrong opportunity
- Any time you hear "we should build X" without a preceding "because customers struggle with Y"

---

## How to Build One

### Step 1: Define the outcome
Start with a single, measurable outcome tied to a business or product goal. Not "improve the product" — that's too vague. Not a list of outcomes — one tree, one outcome.

The outcome should be a metric that matters: "Increase WAU from 32% to 42%" or "Reduce time-to-first-insight from 8 days to 3 days."

### Step 2: Discover opportunities
Opportunities are customer needs, pain points, desires, and context gaps that, if addressed, would move the outcome. They come from research — interviews, session recordings, support tickets, NPS verbatims.

**Not a solution.** "Customers want a mobile app" is a solution. "Customers can't check team status when away from their desk" is an opportunity.

For each opportunity, ask:
- How many customers experience this? (reach)
- How often does it occur? (frequency)
- How much pain does it cause? (intensity)
- How much would addressing it move the outcome? (impact)

### Step 3: Map sub-opportunities
Most large opportunities have sub-opportunities nested within them. "Managers struggle to stay informed without logging in" has sub-opportunities: informed on what? How often? In what format?

Keep decomposing until opportunities are specific enough to generate solution ideas naturally.

### Step 4: Generate solutions
For each opportunity leaf node, generate multiple solutions. Not one solution per opportunity — multiple. You don't know which solution is best until you've identified the options.

**Rule**: Every solution must be attached to a specific opportunity. If you can't name which opportunity a solution addresses, it shouldn't be in the tree.

### Step 5: Identify assumptions and design experiments
Every solution rests on assumptions. Surface the riskiest ones:
- **Desirability**: Do customers want this?
- **Viability**: Will this move the outcome?
- **Feasibility**: Can we build it?
- **Usability**: Can customers use it?

Design the smallest experiment that would test the riskiest assumption before committing to build.

---

## Worked Example: Pulse

**Outcome**: Increase manager WAU from 32% to 42%

```
Increase Manager WAU (32% → 42%)
├── O1: Managers don't have a reason to open Pulse without a specific trigger
│   ├── O1a: No passive notification when something important changes
│   │   ├── S1: Weekly email digest (top changes + recommended action)
│   │   │   └── E1: Prototype digest with 20 managers — would they open it?
│   │   └── S2: Slack bot that posts weekly summary to team channel
│   │       └── E2: Survey — do managers want team-visible summaries?
│   └── O1b: No habit cue built into existing workflows
│       └── S3: Monday morning calendar event with digest link
│           └── E3: Test with 10 managers — does calendar event increase logins?
│
├── O2: Dashboard is overwhelming — managers don't know what to look at
│   ├── O2a: Too many metrics with no hierarchy
│   │   └── S4: "Manager view" — 3 curated metrics per team, not the full dashboard
│   │       └── E4: A/B test: default manager view vs. full dashboard — WAU delta
│   └── O2b: No guidance on what's normal vs. concerning
│       └── S5: Trend indicators with benchmark comparison
│           └── E5: Wizard of Oz test — manually add trend callouts, measure click rate
│
└── O3: Managers who log in don't find new value after the first week
    ├── S6: Weekly "what changed" summary on the homepage
    └── S7: AI-generated insight of the week
        └── E6: Fake door test — show "insight of the week" placeholder, measure click rate
```

**How this changes the work:**
- The team can now see that S1 (digest) and S3 (calendar event) address the same root opportunity (O1b). They should pick one, not build both.
- E1 should run before any engineering starts on S1. If managers say they wouldn't open the digest, the engineering investment is wrong.
- O3 hadn't been articulated before building this tree. It surfaces a retention problem distinct from the habit-formation problem.

---

## Common Mistakes

**Putting solutions in the opportunity layer.**  
"Customers want a mobile app" is a solution dressed up as an opportunity. Push it: what need does the mobile app address? That's the opportunity.

**One solution per opportunity.**  
If you have exactly one solution per opportunity, you haven't generated enough options. Good solution generation requires at least 3 options per opportunity before evaluating.

**Building the tree in a meeting.**  
OSTs are built from research, not from brainstorming. The opportunity layer must come from customer evidence — interviews, support tickets, behavioral data. A tree built from stakeholder opinions is a backlog, not a discovery artifact.

**Treating the tree as permanent.**  
The tree should update as you learn. New research adds new opportunities. Failed experiments close branches. A tree that hasn't changed in 3 months is probably not being maintained.

**Skipping the experiment layer.**  
The value of the OST is not just in organizing the work — it's in forcing you to identify what you're assuming before you build. Every solution has assumptions. Surface them.

---

## Connections

- **[Eigenquestions](eigenquestions.md)**: the OST helps find the eigenquestion by showing which opportunity has the most branches underneath it — the highest-density node is often the load-bearing question
- **[Kano Model](kano-model.md)**: use Kano to classify opportunities in the tree — basic needs (must-haves), performance opportunities, and delight opportunities get different investment levels
- The `experiment-design` skill is the right tool for designing the experiments at the bottom of the OST
- The `customer-research-synthesis` skill surfaces the opportunities from raw research that feed the top of the tree
