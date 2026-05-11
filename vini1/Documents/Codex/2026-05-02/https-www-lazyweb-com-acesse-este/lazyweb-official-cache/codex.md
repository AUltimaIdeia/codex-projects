# Lazyweb Codex Setup

Lazyweb ships as a Codex plugin marketplace at `https://github.com/aboul3ata/lazyweb-skill`. The plugin bundles Lazyweb design skills and an MCP configuration that connects to `https://www.lazyweb.com/mcp`.

## Install

```bash
mkdir -p ~/.lazyweb
TOKEN=$(curl -sS -X POST https://www.lazyweb.com/api/mcp/install-token \
  -H "content-type: application/json" \
  -d '{}' | node -e "let s='';process.stdin.on('data',d=>s+=d);process.stdin.on('end',()=>console.log(JSON.parse(s).token))")
printf '%s\n' "$TOKEN" > ~/.lazyweb/lazyweb_mcp_token
codex plugin marketplace add https://github.com/aboul3ata/lazyweb-skill
```

The plugin reads the token in this order:

1. `LAZYWEB_MCP_TOKEN`
2. `~/.lazyweb/lazyweb_mcp_token`
3. `~/.codex/lazyweb_mcp_token`

Lazyweb is free. The bearer token only authorizes no-billing UI reference tools; it does not grant purchases, paid spend, private user data, or destructive actions. It is okay in ignored local config, but do not commit it to public git.

## Verify

After installing, restart Codex if it was already running. Ask Codex to list MCP tools and confirm these tools exist:

- `lazyweb_health`
- `lazyweb_search`
- `lazyweb_find_similar`
- `lazyweb_compare_image`

Then run:

```json
{"tool":"lazyweb_health","arguments":{}}
```

And:

```json
{"tool":"lazyweb_search","arguments":{"query":"pricing page","limit":3}}
```

## Use Lazyweb

- "Show me pricing page references before we redesign ours."
- "Research onboarding patterns for a B2B SaaS product."
- "Improve this dashboard using real app references."
- "Compare this flow against how strong apps handle the same job."
