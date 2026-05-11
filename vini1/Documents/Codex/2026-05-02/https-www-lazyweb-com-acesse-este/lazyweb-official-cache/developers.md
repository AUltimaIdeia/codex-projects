# Lazyweb Developer Docs

Lazyweb exposes an MCP-first interface for AI agents that need design context, UI references, screenshot search, and product pattern examples.

## Quickstart

```bash
TOKEN=$(curl -sS -X POST https://www.lazyweb.com/api/mcp/install-token \
  -H "content-type: application/json" \
  -d '{}' | node -e "let s='';process.stdin.on('data',d=>s+=d);process.stdin.on('end',()=>console.log(JSON.parse(s).token))")
```

Configure your MCP client:

- URL: `https://www.lazyweb.com/mcp`
- Transport: Streamable HTTP
- Header: `Authorization: Bearer $TOKEN`

## Main Resources

- `POST /api/mcp/install-token`: create a free Lazyweb agent token.
- `POST /mcp`: Streamable HTTP MCP endpoint.
- `GET /.well-known/mcp/server-card.json`: MCP server metadata.
- `GET /.well-known/agent-skills/index.json`: agent skill discovery index.
- `GET /openapi.json`: public OpenAPI description.
- `GET /index.md`: Markdown landing page for agents.
- `GET /cursor.md`: Cursor-specific setup instructions for MCP tools and optional `/lazyweb` skills.
- `GET /codex.md`: Codex plugin setup instructions.
- `GET /claude.md`: Claude Code plugin setup and Claude Desktop MCP-only guidance.
- `GET /use-lazyweb.md`: example prompts and when to use Lazyweb.

## Authentication

Agents do not need a browser session. Call `POST /api/mcp/install-token` and use the returned `token` as a bearer token for `https://www.lazyweb.com/mcp`.

Lazyweb MCP tokens are free setup tokens. They do not unlock billing, purchases, private account data, or destructive actions. Treat them as low-risk bearer credentials: it is acceptable for a local agent to place one in a local Cursor or MCP config, but do not publish or commit the token to shared repositories.

## Cursor Setup

In Cursor, MCP tools and `/lazyweb` skills are separate. Connecting `https://www.lazyweb.com/mcp` exposes Lazyweb MCP tools to Agent chat, but it does not add a slash command. Cursor slash skills require a local file at `.cursor/skills/lazyweb/SKILL.md` for a project or `~/.cursor/skills/lazyweb/SKILL.md` globally.

Fetch the complete Cursor setup guide at `https://www.lazyweb.com/cursor.md`.

## Codex And Claude Code Plugins

Codex and Claude Code should use the plugin source `https://github.com/aboul3ata/lazyweb-skill`.
The plugin reads tokens from `LAZYWEB_MCP_TOKEN`, then `~/.lazyweb/lazyweb_mcp_token`, then the legacy `~/.codex/lazyweb_mcp_token`.

Fetch the complete Codex setup guide at `https://www.lazyweb.com/codex.md`.
Fetch the complete Claude setup guide at `https://www.lazyweb.com/claude.md`.

## Pricing And Limits

Lazyweb is free for humans and agents. This V1 does not apply product rate limits to the MCP setup path.

## Error Recovery

If MCP returns `unauthorized`, request a fresh token from `/api/mcp/install-token` and retry with `Authorization: Bearer <token>`. If setup still fails, verify the MCP URL is `https://www.lazyweb.com/mcp` and contact ali@lazyweb.com.
