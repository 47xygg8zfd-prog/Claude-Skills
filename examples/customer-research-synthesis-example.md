# Example Output: Customer Research Synthesis Skill

**Prompt used:** "Synthesize these 8 customer interview notes about why managers aren't logging into Pulse regularly"

---

## Research Synthesis — Manager Engagement Drop-off
**Research goal**: Understand why managers log into Pulse fewer than 2x/week  
**Participants**: 8 managers (5 mid-market, 3 enterprise) | May 2026  
**Method**: 30-minute structured interviews

---

## Key Themes

### Theme 1: No pull — data is available but not surfaced
**Frequency**: 7/8 participants  
**Representative quotes**:
> "I know the data is there. I just don't think to go look at it unless something feels off."  
> "It's not that I don't care — I have 47 other tabs open and Pulse isn't one of them by default."

**Underlying need**: Managers want to be informed passively, not actively. The cost of "going to check" is higher than it appears.

---

### Theme 2: Dashboard overload — too much data, unclear what matters
**Frequency**: 6/8 participants  
**Representative quotes**:
> "I open it and I don't know where to look first. It's like a cockpit."  
> "I spend 10 minutes and leave less sure about my team than when I started."

**Underlying need**: Managers want a curated point of view, not a data warehouse. They need Pulse to tell them what to pay attention to, not just show everything.

---

### Theme 3: No trigger for action — insights don't connect to next steps
**Frequency**: 5/8 participants  
**Representative quotes**:
> "It shows me response time went up. OK. What do I do with that?"  
> "I'd use it more if it told me what to actually do, not just what happened."

**Underlying need**: Data without recommended action creates cognitive load and learned helplessness. Managers want guidance, not just measurement.

---

### Theme 4: Trust gap — uncertainty about data freshness and accuracy
**Frequency**: 3/8 participants  
**Representative quotes**:
> "I've caught it showing stale data before. Now I double-check everything in Jira anyway."  
> "I'm not sure if this is real-time or from yesterday."

**Underlying need**: Low confidence in data quality makes the tool feel risky to act on. Even infrequent errors erode habitual use.

---

## Jobs To Be Done

**Primary JTBD**:
> When I'm starting my week, I want to quickly understand if anything in my team needs my attention, so I can focus my energy on the right problems without spending time digging through dashboards.

**Secondary JTBD**:
> When I see a metric that looks concerning, I want a clear recommended next step, so I can take action with confidence rather than guessing.

---

## Opportunity Statements

1. How might we help managers stay informed about their team without requiring them to actively seek out information?
2. How might we reduce the cognitive load of the Pulse dashboard so managers immediately know what's most important?
3. How might we connect data insights to concrete recommended actions so managers feel empowered to act, not just observe?

---

## Sentiment Summary

| Sentiment | % of Responses | Top Topics |
|-----------|---------------|------------|
| Positive | 35% | Data depth, team visibility, setup experience |
| Neutral | 28% | Feature awareness, navigation |
| Negative | 37% | Dashboard complexity, lack of push, no action guidance |

---

## Recommended Next Steps

**Strong enough signal to act on now**:
- Build passive delivery (weekly digest) — 7/8 participants directly described this need without being prompted
- Add a "what to do" recommendation layer to key metrics — 5/8 unprompted

**Validate further before building**:
- Data trust issues (Theme 4) — only 3/8 mentioned; run a separate session focused on data accuracy perception with power users before investing in a trust-building feature
- Dashboard simplification — strong signal but solution space is large; run a card sort or design sprint before committing to a redesign

**Segments to watch**:
- Enterprise managers (3/5 mentioned data trust) — may need a separate reliability/audit feature track
- New managers (<6 months in role) — not represented in this sample; schedule dedicated sessions
