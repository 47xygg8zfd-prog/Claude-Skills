# Integration: Notion

Connect Claude to Notion so skills can create and update pages directly — PRDs, OKR docs, research synthesis, and more land in Notion automatically.

## What This Unlocks

| Skill | With Notion Integration |
|-------|------------------------|
| `prd` | Creates a formatted PRD page in your PRD database |
| `okrs` | Creates and updates OKR pages; adds check-in entries |
| `customer-research-synthesis` | Writes synthesis directly to your research database |
| `agile-ceremonies` | Creates retro pages in your team wiki |
| `competitive-analysis` | Updates competitor pages in your competitive intel database |
| `release-notes` | Writes release notes to your changelog database |

## Setup

### 1. Create a Notion integration

1. Go to https://www.notion.so/my-integrations
2. Click **New integration**
3. Name it "Claude PM Skills"
4. Select your workspace
5. Copy the **Internal Integration Secret** (starts with `secret_`)

### 2. Share pages with the integration

For each Notion database Claude should access:
1. Open the database in Notion
2. Click **...** → **Connections** → Add your "Claude PM Skills" integration

### 3. Add to Claude settings

```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@anthropic-labs/mcp-server-notion"],
      "env": {
        "NOTION_API_KEY": "secret_your-integration-secret"
      }
    }
  }
}
```

### 4. Restart Claude

## Example Prompts (with integration active)

**Create a PRD directly in Notion:**
```
Write a PRD for [feature] and save it to our Notion PRD database.
Set status to "Draft" and tag it with the "Engagement" initiative.
```

**Update OKR check-in:**
```
Open the Q3 2026 OKRs page in Notion and add a mid-cycle check-in entry
with today's scores: [paste scores]
```

**Save research synthesis:**
```
Synthesize these interview notes and save the output to our
User Research database in Notion. Title: "Manager Engagement — May 2026".
[paste notes]
```

**Read a PRD for context:**
```
Read the "Weekly Digest" PRD from Notion and use it to write sprint stories.
```

## Customization

Add your Notion database IDs to `CLAUDE.md` so Claude knows where to save different document types:

```
Docs: Notion
- PRD database: [paste database URL or ID]
- OKR database: [paste database URL or ID]
- Research database: [paste database URL or ID]
- Retro database: [paste database URL or ID]
```

To find a database ID: open the database in Notion, copy the URL — the ID is the 32-character string after the last `/` and before the `?`.
