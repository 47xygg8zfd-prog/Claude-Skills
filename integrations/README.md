# Tool Integrations

MCP (Model Context Protocol) configuration snippets for connecting Claude to the tools PMs use every day. Once configured, skills can read from and write to these tools directly — no copy-pasting between apps.

## Available Integrations

| Tool | What It Unlocks |
|------|----------------|
| [Jira](jira.md) | Read tickets, create stories, update status, post comments |
| [Linear](linear.md) | Read and create issues, update cycles, manage projects |
| [Notion](notion.md) | Read and write pages, create PRDs and OKR docs in-place |
| [Confluence](confluence.md) | Create and update pages, post release notes and retros |
| [Slack](slack.md) | Post status updates, send digest summaries, notify channels |

## How MCP Integrations Work

Claude uses the Model Context Protocol to connect to external tools. Each integration requires:
1. An MCP server (either self-hosted or a hosted provider)
2. API credentials for the target tool
3. A config entry in your Claude `settings.json`

The config snippets below show exactly what to add. Once connected, you can use natural language — "create a Jira story for the digest feature" — and Claude will do it directly.

## General Setup

Add MCP servers to your Claude config at `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "tool-name": {
      "command": "npx",
      "args": ["-y", "@some-mcp/server"],
      "env": {
        "API_KEY": "your-key-here"
      }
    }
  }
}
```

See each integration file for the exact config snippet and required credentials.
