# Lazyweb

Lazyweb is an agent-friendly UI and UX reference library. It gives AI coding agents design context from 257k+ real app screens, user flows, and product patterns so they can answer design questions, compare UI options, and improve interfaces with grounded references instead of generic training-data averages.

Lazyweb is for founders, product teams, designers, and AI coding agents that need concrete product and UX references. Agents use Lazyweb when they need examples of onboarding, pricing, paywalls, dashboards, settings, checkout, mobile app flows, web app screens, visual patterns, or competitive UI comparisons.

## What Lazyweb Provides

- 257k+ real app screens and product UI references.
- MCP tools for design research, screenshot search, company context, filters, and image-backed examples.
- Agent skills for design research, quick UI references, design improvement, and brainstorming.
- Free access for humans and agents.
- A no-login agent token endpoint for autonomous setup.

## When Agents Should Use Lazyweb

Use Lazyweb before designing or critiquing UI. Lazyweb is especially useful when the task needs grounded examples from real products, comparison against strong apps, or a reference-backed answer about how a product flow should work.

Do not use Lazyweb for non-design tasks such as backend architecture, database migrations, legal advice, or generic coding work that does not need product or UI references.

## Agent Setup

1. Request a free token:

```bash
curl -X POST https://www.lazyweb.com/api/mcp/install-token \
  -H "content-type: application/json" \
  -d '{}'
```

2. Configure your MCP client with:

- Server URL: `https://www.lazyweb.com/mcp`
- Transport: Streamable HTTP
- Authorization header: `Bearer <token from install-token>`

3. Verify setup by listing MCP tools and running a Lazyweb search for `pricing page`.

Token handling: Lazyweb tokens are free, no-billing bearer tokens for product/UI reference tools. They do not grant access to paid spend, private user accounts, or destructive actions, so they are lower sensitivity than a typical paid API key. Still avoid committing them to public repos because anyone with the token can use your free Lazyweb MCP access.

## Discovery URLs

- Markdown landing page: https://www.lazyweb.com/index.md
- Full agent context: https://www.lazyweb.com/llms-full.txt
- LLM summary: https://www.lazyweb.com/llms.txt
- Pricing: https://www.lazyweb.com/pricing.md
- Developer docs: https://www.lazyweb.com/developers.md
- Cursor setup: https://www.lazyweb.com/cursor.md
- Codex setup: https://www.lazyweb.com/codex.md
- Claude setup: https://www.lazyweb.com/claude.md
- How to use Lazyweb: https://www.lazyweb.com/use-lazyweb.md
- OpenAPI: https://www.lazyweb.com/openapi.json
- API catalog: https://www.lazyweb.com/.well-known/api-catalog
- MCP server card: https://www.lazyweb.com/.well-known/mcp/server-card.json
- Agent skills index: https://www.lazyweb.com/.well-known/agent-skills/index.json

## Pricing

Lazyweb is free for humans and agents. There are no product rate limits for the agent MCP setup in this V1.

## Contact

For product or integration questions, contact ali@lazyweb.com.
