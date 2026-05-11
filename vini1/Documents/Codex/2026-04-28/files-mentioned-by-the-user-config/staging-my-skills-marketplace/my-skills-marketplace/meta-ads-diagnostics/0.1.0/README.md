# Meta Ads Diagnostics

`meta-ads-diagnostics` is a read-only Codex plugin for Meta Ads reporting and diagnosis.

It exposes a local MCP server with tools for:

- validating Meta Ads connectivity
- listing accessible ad accounts
- listing campaigns for an ad account
- fetching insights for a selected period
- generating campaign-level diagnostic summaries

## Scope

This MVP is intentionally read-only.

It does not:

- create campaigns
- pause ads or ad sets
- change budgets
- mutate any Meta asset

## Plugin Surface

- `.codex-plugin/plugin.json`: plugin manifest
- `.mcp.json`: local MCP server registration
- `skills/meta-ads-diagnostics/SKILL.md`: operating guidance for Codex
- `scripts/server.mjs`: MCP server entrypoint
- `scripts/meta-api.mjs`: Meta Graph/Marketing API wrapper
- `scripts/auth.mjs`: OAuth helper for auth URL generation and token exchange
- `assets/plugin-map.md`: boundaries, architecture, and next-step guidance

## Setup

### 1. Create a Meta app

Create a Meta developer app that can request the permissions needed for ads reporting. For a read-only MVP, the main permission is typically `ads_read`. Depending on your business setup, `business_management` may also be useful for account discovery.

### 2. Configure environment variables

Create a local `.env` based on `.env.example` and fill the values:

- `META_ACCESS_TOKEN`
- `META_APP_ID`
- `META_APP_SECRET`
- `META_REDIRECT_URI`
- optional `META_AD_ACCOUNT_IDS`
- optional `META_API_VERSION`

The plugin reads directly from the process environment. It does not persist tokens by itself.

### 3. Install dependencies

From the plugin folder:

```bash
npm install
```

### 4. Optional: generate auth URL

```bash
npm run auth:url
```

This prints the Meta OAuth URL. If you provide app credentials and a redirect URI, you can then exchange the returned code:

```bash
node ./scripts/auth.mjs exchange --code "<CODE>"
```

To exchange a short-lived token for a long-lived token:

```bash
node ./scripts/auth.mjs long-lived --token "<SHORT_LIVED_TOKEN>"
```

### 5. Use the plugin tools

Recommended sequence:

1. `meta_validate_connection`
2. `meta_list_ad_accounts`
3. `meta_list_campaigns`
4. `meta_get_insights`
5. `meta_campaign_diagnostics`

## Environment Variables

| Variable | Required | Purpose |
| --- | --- | --- |
| `META_ACCESS_TOKEN` | yes | User access token with Meta Ads read permissions |
| `META_APP_ID` | no | Needed for the auth helper |
| `META_APP_SECRET` | no | Needed for code exchange and long-lived token exchange |
| `META_REDIRECT_URI` | no | OAuth callback URI, defaults to `http://127.0.0.1:8787/callback` |
| `META_API_VERSION` | no | Graph API version, defaults to `v25.0` |
| `META_AD_ACCOUNT_IDS` | no | Comma-separated allowlist for accessible ad accounts |

## Guardrails

- This plugin only performs `GET` requests against Meta APIs.
- If `META_AD_ACCOUNT_IDS` is set, the plugin hides accounts outside that allowlist.
- Diagnostic messages are heuristic and should be treated as operator guidance, not automated business truth.

## Next Expansion

If the read-only path proves stable, the next controlled layer should be:

1. pausing/resuming entities with explicit confirmation
2. budget updates with audit logs
3. campaign/ad set creation only after approval and dry-run validation
