# Example Output: Feature Prioritization Skill

**Prompt used:** "Prioritize these 6 features for next quarter using RICE: weekly digest, mobile app, SSO, custom dashboards, API access, in-app onboarding"

---

## RICE Prioritization — Pulse Q3 2026

**Assumptions**:
- Reach = estimated users impacted per quarter (out of 4,200 active seats)
- Impact scale: 3 = massive, 2 = significant, 1 = moderate, 0.5 = low, 0.25 = minimal
- Confidence: 100% = strong data, 80% = reasonable signal, 50% = mostly a guess
- Effort = person-months (team of 6 engineers)

---

### RICE Scores

| Feature | Reach | Impact | Confidence | Effort | RICE Score | Priority |
|---------|-------|--------|------------|--------|------------|----------|
| In-app onboarding | 1,800 | 2 | 80% | 1.0 | **2,880** | #1 |
| Weekly digest | 2,100 | 1 | 100% | 2.0 | **1,050** | #2 |
| SSO | 600 | 3 | 100% | 1.5 | **1,200** | #3 |
| Custom dashboards | 900 | 2 | 80% | 4.0 | **360** | #4 |
| API access | 300 | 3 | 50% | 3.0 | **150** | #5 |
| Mobile app | 1,200 | 1 | 50% | 8.0 | **75** | #6 |

---

### Recommendation

**Build in Q3**: In-app onboarding, SSO, Weekly digest

**In-app onboarding** scores highest because it affects every new user (1,800 seats onboarded per quarter) and our data shows that users who complete onboarding have 2.4x higher 90-day retention. This is the clearest ROI on the board.

**SSO** scores well despite lower reach because it's a hard blocker for 4 enterprise prospects currently in late-stage sales. Closing even two of those deals more than pays for the 1.5 person-months.

**Weekly digest** is a solid #2 and pairs naturally with onboarding — users who get the digest in their first 30 days form the habit faster. Recommend sequencing digest after onboarding in the quarter.

---

### Defer to Q4

**Custom dashboards** — high demand from power users but 4 person-months is heavy. Revisit once onboarding improvement data is in; the right dashboard structure may depend on what we learn.

**API access** — strong strategic value but confidence is low (50%). We need 2-3 customer conversations to validate the use cases before committing eng time.

**Mobile app** — lowest RICE by a wide margin. Usage data shows 94% of Pulse sessions are on desktop. Revisit if mobile session share crosses 15%.

---

### Flags

- API access estimate is rough — schedule a spike before Q4 planning
- SSO effort may increase if prospects require SAML 2.0 + SCIM provisioning (currently estimated for SAML only)
