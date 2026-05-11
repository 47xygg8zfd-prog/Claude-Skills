---
name: product-marketer
description: >
  Produce launch messaging, positioning frameworks, feature announcements,
  sales enablement copy, and go-to-market narrative for product features or
  releases. Use this skill when the user asks for launch copy, positioning,
  a press release, a product blog post, a feature page, a sales battlecard,
  or any marketing output tied to a product or feature. Also trigger when the
  user says things like "write the announcement for", "position this feature",
  "help me explain this to customers", "write the launch email", or "what's
  the messaging for this". Works from a PRD, feature brief, or rough description.
---

# Product Marketer Skill

Produce sharp, differentiated launch messaging and marketing assets for product features and releases.

## When to Use
- A feature is approaching launch and needs announcement copy
- The team is debating how to position a feature against competitors
- A PM or designer needs customer-facing language for a new screen or flow
- Sales needs a battlecard or talk track for a new capability
- Leadership needs a press release or launch blog post

---

## Positioning First

Before writing any copy, establish the positioning. Every other asset flows from this.

### Positioning Framework

**Feature name**: [What we call it — clear, not clever unless brand supports it]

**Target customer**: [Specific person — role, company type, context — not "all users"]

**Job to be done**: When [situation], I want to [motivation], so I can [outcome].

**Category**: [What kind of thing is this? Don't invent a new category unless you have to.]

**Differentiated value**: [The one thing this does better than any alternative — specific, not generic]

**Proof point**: [The fact, stat, or customer quote that makes the claim credible]

**Against alternatives**: [What customers do today without this feature — and why that's worse]

---

## Output Formats

### 1. Messaging Hierarchy
The structured source of truth for all copy. Produce in this order:

```
Headline (≤8 words): [The single most important thing — lead with value, not feature name]
Subheadline (≤20 words): [Expand on the headline — who it's for and what they get]
Body (2-3 sentences): [More detail — how it works, what's new, why now]
CTA: [What the user should do next]

Supporting proof points (3):
• [Specific benefit — quantified where possible]
• [Specific benefit]
• [Specific benefit]
```

### 2. Feature Announcement (in-app or email)
**Length**: 100-200 words. **Tone**: Match existing brand voice — if not specified, warm and direct.

Structure:
- Hook (1 sentence): What's new and why the user should care
- What it does (2-3 sentences): Plain language, user benefit first
- How to get started (1 sentence): Clear action
- CTA button: [Label — e.g., "Try it now", "See it in action"]

### 3. Launch Email
**Subject line**: [Lead with benefit or intrigue — avoid "Introducing" as the first word]
**Preview text**: [Complements subject, adds detail]
**Body**: Hook → problem → solution → proof → CTA
**Length**: 150-250 words. One CTA only.

### 4. Product Blog Post
Structure:
1. **Hook** (1-2 paragraphs): A story, a stat, or the problem — not "Today we're excited to announce"
2. **The problem** (1 paragraph): What pain users have today
3. **The solution** (2-3 paragraphs): What we built, how it works, what makes it different
4. **Proof** (1 paragraph): Customer quote, data, or demo description
5. **How to get started** (1 paragraph): Clear, specific steps
6. **Closing** (1 sentence): Forward-looking, not self-congratulatory

Length: 400-700 words. Avoid feature-dump structure.

### 5. Sales Battlecard
```
Feature: [Name]
One-sentence pitch: [What to say in 10 seconds]

When to use this:
• [Sales scenario where this feature matters]
• [Scenario]

How to demo it:
1. [Step — what to show first]
2. [Step]
3. [Step]

Competitive comparison:
| We do... | [Competitor] does... | Our advantage |
|---------|---------------------|--------------|

Objections:
• "[Objection]" → [Response — specific, not defensive]
• "[Objection]" → [Response]

Proof points:
• [Stat or customer quote]
```

### 6. Social Copy (LinkedIn / X)
**LinkedIn**: 3-5 sentences + 3 hashtags. Lead with the insight or customer problem, not the product.
**X/Twitter**: ≤280 characters. Hook + value + CTA. No hashtag spam.

---

## Output Guidelines

- **Lead with customer benefit, not feature description.** "Managers get their week in 90 seconds" beats "We built a weekly digest."
- **Be specific.** "3x faster" beats "faster." "Engineering managers at 150-person companies" beats "teams."
- **One message per asset.** Don't try to communicate three things at once.
- **Write for skimmers.** Headers, bullets, bold on the key phrase — don't bury the value in paragraph 3.
- **Avoid launch clichés**: "excited to announce", "game-changer", "revolutionary", "best-in-class", "seamless", "robust".
- **Match the proof to the claim.** If you claim speed, show a number. If you claim ease, show steps. If you claim delight, show a quote.

## Quick Mode

If the user provides minimal context, produce:
1. A one-sentence positioning statement
2. Three headline options (different angles: benefit / pain / intrigue)
3. A 100-word feature announcement
Then ask what else is needed.

## Integration Points

- Start with the **prd** skill output to ensure messaging reflects actual scope
- Use **competitive-analysis** skill to sharpen the differentiation claim
- Hand off to **stakeholder-updates** skill to turn the launch narrative into an exec update
- Use **go-to-market** skill for the full launch plan (channels, timing, enablement)
- The `pdlc_orchestrator.py` includes a marketing stage that runs after QA — feed this skill's output to that stage
