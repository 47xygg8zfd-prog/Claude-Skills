# Skill: Go-to-Market

## Trigger Phrases
- "write a GTM plan"
- "plan the launch for"
- "go-to-market for"
- "how do we launch this"
- "launch plan for"
- "who do we target first"
- "rollout strategy for"
- "launch readiness for"

## Description
Build a go-to-market plan for a feature or product launch. Covers target segment, positioning, launch phases, channel strategy, enablement needs, and success metrics. Works for internal launches, limited betas, and full GA releases.

## Behavior

When triggered, ask the user for:
1. What's launching (feature, product, or pricing change)
2. Target audience (existing customers, new segment, or both)
3. Launch type (internal / limited beta / phased rollout / full GA)
4. Key constraint (timeline, team capacity, or dependency)

Then produce:

### 1. Launch Summary
| Field | Detail |
|-------|--------|
| What's launching | |
| Target audience | |
| Launch date | |
| Launch type | |
| Owner | |

---

### 2. Positioning
**For**: [target customer]  
**Who**: [has this problem]  
**The feature**: [name]  
**Is a**: [category]  
**That**: [key benefit]  
**Unlike**: [current alternative]  
**We**: [key differentiator]

---

### 3. Target Segment & Rollout Phasing

| Phase | Who | % of Users | Goal | Duration |
|-------|-----|-----------|------|----------|
| Alpha | Internal / design partners | <5% | Validate core flow | 1-2 weeks |
| Beta | Opted-in power users | 10-25% | Catch edge cases, gather feedback | 2-4 weeks |
| Limited GA | Specific segment or tier | 25-50% | Validate metrics, CS readiness | 2-4 weeks |
| Full GA | All eligible users | 100% | Scale | Ongoing |

Adjust phases based on launch type — internal tools may skip to full GA; high-risk changes may need a longer beta.

---

### 4. Channel Plan

| Channel | Message | Owner | Timing |
|---------|---------|-------|--------|
| In-app announcement | | Product | GA day |
| Email to affected users | | Marketing / PM | GA day |
| Release notes | | PM | GA day |
| CS / Sales briefing | | PM | 1 week before GA |
| Help center article | | CS | Before GA |
| Internal Slack announcement | | PM | GA day |

---

### 5. Enablement Checklist

**Sales / CS** (complete before GA):
- [ ] Feature briefing sent (what it does, who it's for, common questions)
- [ ] Battlecard or talking points updated (if competitive)
- [ ] Demo environment updated
- [ ] Known issues and workarounds documented

**Support**:
- [ ] Help center article published
- [ ] Support macros / canned responses updated
- [ ] Escalation path defined for launch-day issues

**Legal / Compliance** (if applicable):
- [ ] Privacy policy updated (if new data collection)
- [ ] Terms of service updated (if new functionality)
- [ ] GDPR / data processing agreements reviewed

---

### 6. Success Metrics

| Metric | Baseline | Target | Measurement Window |
|--------|----------|--------|--------------------|
| [Primary metric] | | | 30 days post-launch |
| [Adoption metric] | | | 14 days post-launch |
| [Quality metric] | | | 7 days post-launch |

---

### 7. Rollback Criteria

Define the conditions that trigger a rollback or pause before full GA:
- [Metric] drops below [threshold]
- Error rate exceeds [threshold]
- [Number] critical support tickets received within [time window]

## Output Style
- Actionable and owner-assigned — every item has a name next to it
- Flag any missing dependencies (e.g., "CS briefing requires release notes first")
- Keep the summary tight enough to share in a Slack message

## Customization Tips
- Add your standard launch channels to CLAUDE.md so they're included automatically
- Add your CS lead and marketing lead names so owner fields auto-populate
- Add your standard rollout percentages if they differ from defaults (e.g., your org always does 5% / 20% / 100%)
