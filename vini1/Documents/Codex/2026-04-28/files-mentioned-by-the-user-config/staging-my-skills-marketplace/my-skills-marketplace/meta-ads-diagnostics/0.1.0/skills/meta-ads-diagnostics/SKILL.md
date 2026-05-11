---
name: meta-ads-diagnostics
description: Use the local Meta Ads Diagnostics plugin to validate Meta Ads connectivity, inspect accessible ad accounts, pull campaign insights, and generate read-only diagnostic summaries. Prefer this skill whenever the user wants Meta Ads reports, campaign triage, or account-level diagnostics without making account changes.
---

# Meta Ads Diagnostics

Use this skill when the task is about Meta Ads reporting, account inspection, campaign diagnostics, or performance triage.

## Purpose

This skill routes Meta Ads analysis through the local MCP tools exposed by the `meta-ads-diagnostics` plugin.

It is intentionally read-only.

Do not attempt to:

- create campaigns
- edit budgets
- pause entities
- publish creatives

If the user asks for writes, explain that this plugin version does not expose mutation tools yet.

## Operating Sequence

1. Start with `meta_validate_connection`.
2. If the connection is valid, call `meta_list_ad_accounts`.
3. Ask for or infer the relevant ad account only when it matters.
4. Use `meta_list_campaigns` to narrow the surface before deeper analysis.
5. Use `meta_get_insights` for raw reporting.
6. Use `meta_campaign_diagnostics` when the user wants interpretation or triage.

## When To Use Which Tool

### `meta_validate_connection`

Use first whenever the token or setup may be unverified.

### `meta_list_ad_accounts`

Use to discover which ad accounts the token can read.

### `meta_list_campaigns`

Use when the user needs entity context before insights.

### `meta_get_insights`

Use for raw metrics by date range or preset.

### `meta_campaign_diagnostics`

Use when the user wants a sharper answer than raw numbers, such as:

- "what looks broken?"
- "which campaigns need attention?"
- "where is spend happening without signal?"

## Default Behaviors

- Prefer the last 30 days if the user does not specify a period.
- Prefer campaign-level analysis first. Go to ad set or ad level only if the question needs that granularity.
- Treat heuristic conclusions as guidance, not fact.
- Surface exact account IDs and campaign IDs in outputs when they matter for follow-up actions.

## Boundaries

This skill is analysis-oriented. It should not invent business explanations that the API data does not support.

If a conclusion is inferred from metrics, say that it is an inference.
