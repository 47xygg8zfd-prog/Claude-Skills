# Skill: Stakeholder Updates

## Trigger Phrases
- "write a stakeholder update"
- "draft a status update"
- "weekly update for"
- "escalation memo"
- "write a DACI"
- "project status email"
- "exec update on"
- "communicate the delay"
- "write a RACI"

## Description
Draft stakeholder-ready communications: weekly status updates, escalation memos, delay notifications, DACI/RACI tables, and cross-functional alignment docs. Matches tone and format to audience and urgency.

## Behavior

### Mode 1: Weekly / Regular Status Update
Ask the user for:
1. Project or initiative name
2. Status (On Track / At Risk / Blocked)
3. Key updates since last week
4. Upcoming milestones
5. Blockers or asks

Produce:

**[Project Name] — Status Update [Date]**

**Status**: 🟢 On Track / 🟡 At Risk / 🔴 Blocked

**Summary**
[2-3 sentence narrative of where things stand.]

**This Week**
- ...

**Next Week**
- ...

**Blockers / Asks**
- [Blocker]: [Owner needed / Decision required by date]

---

### Mode 2: Escalation Memo
Ask the user for:
1. The issue requiring escalation
2. Impact if unresolved (timeline, cost, customer)
3. Decision or action needed
4. Deadline for decision

Produce a concise escalation memo:
- **Situation**: What happened
- **Impact**: Business consequence
- **Options**: 2-3 paths forward with tradeoffs
- **Recommendation**: Preferred path
- **Decision needed by**: [Date]

---

### Mode 3: Delay / Risk Notification
Tone: transparent, accountable, solution-oriented. Never defensive.

Structure:
- What was expected vs. what is happening
- Root cause (brief, factual)
- Revised timeline
- What's being done to recover
- Ask (if any)

---

### Mode 4: DACI Table
| Milestone / Decision | Driver | Approver | Contributor | Informed |
|----------------------|--------|----------|-------------|----------|
| ...                  | ...    | ...      | ...         | ...      |

**DACI definitions**:
- **Driver**: Owns the work and drives to completion
- **Approver**: Final decision authority
- **Contributor**: Input and expertise, no veto
- **Informed**: Kept in the loop, no action required

---

### Mode 5: RACI Table
| Task | Responsible | Accountable | Consulted | Informed |
|------|-------------|-------------|-----------|----------|
| ...  | ...         | ...         | ...       | ...      |

## Output Style
- Lead with status and the most important thing — assume readers skim
- Escalations: crisp and action-oriented, never political
- Delay notices: factual and forward-looking, never apologetic padding
- Copy should be ready to paste into email or Slack with minimal editing

## Customization Tips
- Add your team roster so Claude can suggest DACI/RACI owners
- Add your organization's status color conventions (some use R/Y/G, others use emojis or text)
- Add recurring stakeholder names and their communication preferences
