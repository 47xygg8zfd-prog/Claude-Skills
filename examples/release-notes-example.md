# Example Output: Release Notes Skill

**Prompt used:** "Write release notes for Pulse v2.4 — we shipped the weekly digest, SSO via SAML 2.0, and fixed a bug where collaboration scores showed as 0 for teams under 5 people"

---

## End-User Version

**What's New in Pulse — May 2026**

---

**Weekly Team Digest**  
Your most important team insights, delivered to your inbox every Monday morning. No login required — Pulse will highlight what changed, flag anything that needs your attention, and suggest one action to take. Enable it in Settings → Notifications.

**Single Sign-On (SSO)**  
Pulse now supports SAML 2.0 SSO. Admins can connect Pulse to Okta, Azure AD, or any SAML-compatible identity provider in Settings → Security. Once enabled, your team signs in with their existing company credentials.

**Bug Fixes**  
- Fixed an issue where collaboration scores displayed as 0 for teams with fewer than 5 members. Scores now calculate correctly for all team sizes.

---

## Internal / Engineering Version

**Release v2.4.0 — 2026-05-11**

**New**
- `feature/weekly-digest`: Weekly email digest for managers. Aggregation job runs Sunday 23:00 UTC. Delivery via SendGrid. Opt-in per org via admin settings. See [RFC-041] for architecture.
- `feature/sso-saml2`: SAML 2.0 SSO support. Supports SP-initiated flow. IdP metadata URL config in admin panel. SCIM provisioning NOT included in this release (see backlog item #1847).

**Fixed**
- `fix/collab-score-small-teams`: Collaboration score returned `0` for teams with `member_count < 5` due to division-by-zero in `score_normalizer.rb:L88`. Fixed normalization floor. Affected ~340 teams.

**Migration Notes**
- Run `rake db:migrate` — adds `digest_snapshots` table and `org_settings.digest_enabled` column.
- SSO feature flag (`sso_saml_enabled`) is OFF by default. Enable per org via admin or Flipper console.

**Known Issues**
- Digest delivery time respects user timezone but falls back to UTC (not org timezone) if user timezone is unset. Fix targeted for v2.4.1.

---

## Sales & CS Version

**Pulse v2.4 — What to Know**

**Top Highlights (use in demos)**
- **Weekly Digest**: Huge habit-formation story. Managers get a Monday morning email with their team's highlights and one recommended action. No login needed. This directly addresses the #1 objection in churned accounts ("we forgot to use it").
- **SSO via SAML 2.0**: Unlocks the 4 enterprise deals currently blocked on SSO. Works with Okta, Azure AD, and any SAML provider. Okta setup guide available in the Help Center.

**Customer Impact**
- ~340 teams that had collaboration scores stuck at 0 will now see correct data — proactively reach out to accounts affected; this may prompt re-engagement.

**Common Questions to Expect**
- *"Does the digest include all my teams or just one?"* — All teams the manager owns in Pulse, one section per team.
- *"Does SSO support SCIM / auto-provisioning?"* — Not in this release. On the roadmap for Q4.
- *"Can I customize the digest day/time?"* — Weekly on Mondays at 9am local time only. Customization is planned for v2.5.

---

## Exec Version

**Pulse v2.4 Summary**

- Launched weekly email digest — our primary initiative to improve manager habit formation and reduce the "low engagement" churn signal. Early open rate target: 45%.
- Shipped SAML 2.0 SSO, unblocking 4 enterprise deals currently in late-stage sales.
- Fixed a data accuracy bug affecting ~340 small teams; proactive CS outreach underway.
- No incidents at launch. Digest delivery infrastructure load-tested to 50k sends/hour.
