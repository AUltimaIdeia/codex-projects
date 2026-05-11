# How To Use Lazyweb

Use Lazyweb when an AI agent needs grounded UI and product-design context from real apps.

## Good Requests

- "Find pricing page references for a B2B SaaS landing page."
- "Research onboarding flows for developer tools."
- "Improve this design with real app references."
- "Compare our checkout flow against strong consumer apps."
- "Show me examples of settings pages that handle billing and team management well."

## Agent Workflow

1. Call `lazyweb_health` to confirm MCP is connected.
2. Call `lazyweb_search` with a concrete UI need, such as `pricing page`, `mobile onboarding`, or `team settings billing`.
3. Use multiple searches from different angles when the design space is broad.
4. Cite the strongest patterns and explain how they should affect the user's UI.
5. When improving an existing design, compare the current screen against Lazyweb references before recommending changes.

## What Lazyweb Is Best For

- Landing pages and pricing pages.
- Onboarding and activation flows.
- Dashboards, settings, billing, checkout, and upgrade paths.
- Mobile and web app UI references.
- Competitive design comparisons.
- Design critique grounded in real product screenshots.

## What Lazyweb Is Not For

- Backend-only implementation work.
- Database migrations.
- Legal, medical, financial, or non-design research.
- Generic code cleanup with no UI or product-design component.
