# Skill: Release Notes

## Trigger Phrases
- "write release notes"
- "draft a changelog"
- "summarize what shipped"
- "release notes for version"
- "what's new in this release"
- "write release comms"
- "internal release summary"

## Description
Draft release notes and changelogs tailored to different audiences — end users, internal teams, sales/CS, and executives. Transforms engineering tickets, PR descriptions, or rough bullet points into polished, audience-appropriate release communication.

## Behavior

When triggered, ask the user for:
1. Raw input (ticket titles, PR descriptions, bullet points of what shipped)
2. Target audience(s): end users / internal / sales & CS / exec
3. Release version or date (optional)
4. Any features to highlight vs. bury (e.g. bug fixes only, no new features)

Then produce the selected format(s):

### End-User Format
Friendly, benefit-led language. No jargon. Focus on what they can now do, not what changed technically.

**What's New — [Version / Date]**

**[Feature Name]**
[One sentence: what it does and why it matters to the user.]

**Improvements**
- [Bug fix or enhancement in plain language]
- ...

---

### Internal / Engineering Format
Factual, complete. Include version numbers, migration notes, deprecations, and known issues.

**Release [Version] — [Date]**
- **New**: ...
- **Changed**: ...
- **Fixed**: ...
- **Deprecated**: ...
- **Known Issues**: ...

---

### Sales & CS Format
Focused on customer value, competitive differentiation, and talking points. Flags anything that affects pricing, limits, or common support tickets.

**[Version] — What to Know**
- **Top Highlights** (use in demos): ...
- **Customer Impact**: ...
- **Common Questions to Expect**: ...

---

### Exec Format
3-5 bullet summary. Business outcomes, not features. Flag any risk items.

**[Version] Summary**
- ...

## Output Style
- Match tone to audience (casual for users, precise for engineering, persuasive for sales)
- Lead with highest-impact changes
- Never use internal ticket IDs or PR numbers in user-facing output
- Flag anything that requires a migration step or breaks existing behavior

## Customization Tips
- Add your product name and brand voice guidelines
- Add your versioning scheme (semver, date-based, etc.)
- Add a template header/footer if release notes go into a specific tool (Notion, Confluence, Intercom)
