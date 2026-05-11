# Integration: Confluence

Connect Claude to Confluence so skills can create and update pages directly — PRDs, release notes, retros, and OKR docs land in your wiki automatically.

## What This Unlocks

| Skill | With Confluence Integration |
|-------|----------------------------|
| `prd` | Creates a formatted PRD page in your product space |
| `release-notes` | Publishes release notes to your changelog space |
| `agile-ceremonies` | Creates retro and sprint planning pages |
| `okrs` | Creates OKR pages and adds check-in sections |
| `stakeholder-updates` | Posts status updates to your team space |
| `customer-research-synthesis` | Saves research synthesis to your research space |
| `claude-automation` | Reads Jira ticket → creates PRD draft in Confluence (full automation) |

## Setup

### 1. Get your Confluence credentials

You need:
- **Confluence base URL**: `https://your-org.atlassian.net/wiki`
- **Email**: your Atlassian account email
- **API token**: same token as Jira (generate at https://id.atlassian.com/manage-profile/security/api-tokens)

### 2. Add to Claude settings

```json
{
  "mcpServers": {
    "confluence": {
      "command": "npx",
      "args": ["-y", "@anthropic-labs/mcp-server-confluence"],
      "env": {
        "CONFLUENCE_BASE_URL": "https://your-org.atlassian.net/wiki",
        "CONFLUENCE_EMAIL": "you@yourcompany.com",
        "CONFLUENCE_API_TOKEN": "your-api-token"
      }
    }
  }
}
```

### 3. Restart Claude

## Example Prompts (with integration active)

**Create a PRD page:**
```
Write a PRD for [feature] and create a Confluence page in the PROD space
under "PRDs > Q3 2026". Set the label to "draft".
```

**Publish release notes:**
```
Write release notes for v2.4 and publish them to Confluence in the
"Release Notes" space. Audience: internal team.
What shipped: [bullet list]
```

**Create a retro page:**
```
Run a retro for Sprint 24 and save the output as a new Confluence page
in the TEAM space under "Retrospectives".
```

**Read a page for context:**
```
Read the "Q3 2026 OKRs" page in Confluence and use it as context
for this week's stakeholder update.
```

## Permissions Required

The API token needs:
- `read:confluence-content.all` — read pages and spaces
- `write:confluence-content` — create and update pages

## Customization

Add your Confluence space keys to `CLAUDE.md`:
```
Docs: Confluence
- Product space: PROD
- Team space: TEAM
- Release notes space: RELEASES
```
