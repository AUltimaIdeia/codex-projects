# Meta Ads Diagnostics Plugin Map

## Architecture Decision

Recommendation: single-purpose plugin with a local MCP server and one operating skill.

## Why

- Meta Ads access is an integration problem, not just an instruction problem.
- Read-only first reduces risk and removes the chance of accidental spend changes.
- A local MCP server gives Codex explicit tools instead of relying on fragile prompt-only API choreography.

## Responsibilities

This plugin owns:

- Meta Ads read-only connectivity
- account, campaign, and insights retrieval
- heuristic campaign diagnostics
- OAuth helper commands for setup

This plugin does not own:

- campaign creation
- bid or budget management
- creative uploads
- automated optimization loops

## Tool Surface

- `meta_validate_connection`
- `meta_list_ad_accounts`
- `meta_list_campaigns`
- `meta_get_insights`
- `meta_campaign_diagnostics`

## Governance

- only `GET` endpoints are used
- write actions are explicitly out of scope in `0.1.0`
- the token is read from env, not embedded in files

## Upgrade Path

If this plugin graduates beyond MVP:

1. add explicit dry-run planning for write actions
2. add audit logging for every mutation
3. split read-only diagnostics from write-capable execution surfaces
