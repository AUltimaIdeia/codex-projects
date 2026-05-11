import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import {
  campaignDiagnostics,
  getInsights,
  listAdAccounts,
  listCampaigns,
  validateConnection,
} from "./meta-api.mjs";

const server = new McpServer({
  name: "meta-ads-diagnostics",
  version: "0.1.0",
});

function asToolResult(data) {
  return {
    content: [
      {
        type: "text",
        text: JSON.stringify(data, null, 2),
      },
    ],
  };
}

function asToolError(error) {
  return {
    content: [
      {
        type: "text",
        text: error instanceof Error ? error.message : String(error),
      },
    ],
    isError: true,
  };
}

async function withToolErrorBoundary(fn) {
  try {
    return asToolResult(await fn());
  } catch (error) {
    return asToolError(error);
  }
}

server.tool(
  "meta_validate_connection",
  "Validate that the configured Meta token works and list the ad accounts visible to it.",
  {},
  async () => withToolErrorBoundary(() => validateConnection()),
);

server.tool(
  "meta_list_ad_accounts",
  "List the Meta ad accounts accessible to the configured token.",
  {},
  async () => withToolErrorBoundary(() => listAdAccounts()),
);

server.tool(
  "meta_list_campaigns",
  "List campaigns for a Meta ad account without changing anything.",
  {
    accountId: z.string().describe("Meta ad account id, with or without the act_ prefix."),
    limit: z.number().int().min(1).max(200).optional(),
    effectiveStatus: z
      .array(z.string())
      .optional()
      .describe("Optional list of effective statuses to filter by."),
  },
  async ({ accountId, limit, effectiveStatus }) =>
    withToolErrorBoundary(() =>
      listCampaigns({ accountId, limit, effectiveStatus }),
    ),
);

server.tool(
  "meta_get_insights",
  "Fetch raw Meta Ads insights for an ad account in a read-only way.",
  {
    accountId: z.string().describe("Meta ad account id, with or without the act_ prefix."),
    level: z.enum(["account", "campaign", "adset", "ad"]).optional(),
    limit: z.number().int().min(1).max(500).optional(),
    datePreset: z.string().optional().describe("Example: last_30d, yesterday, this_month."),
    since: z.string().optional().describe("Start date in YYYY-MM-DD."),
    until: z.string().optional().describe("End date in YYYY-MM-DD."),
    fields: z.array(z.string()).optional(),
    filtering: z.array(z.record(z.any())).optional(),
  },
  async ({ accountId, level, limit, datePreset, since, until, fields, filtering }) =>
    withToolErrorBoundary(() =>
      getInsights({
        accountId,
        level,
        limit,
        datePreset,
        since,
        until,
        fields,
        filtering,
      }),
    ),
);

server.tool(
  "meta_campaign_diagnostics",
  "Generate a campaign-level diagnostic summary from Meta Ads insights without making account changes.",
  {
    accountId: z.string().describe("Meta ad account id, with or without the act_ prefix."),
    limit: z.number().int().min(1).max(100).optional(),
    datePreset: z.string().optional().describe("Example: last_30d, last_7d, yesterday."),
    since: z.string().optional().describe("Start date in YYYY-MM-DD."),
    until: z.string().optional().describe("End date in YYYY-MM-DD."),
  },
  async ({ accountId, limit, datePreset, since, until }) =>
    withToolErrorBoundary(() =>
      campaignDiagnostics({ accountId, limit, datePreset, since, until }),
    ),
);

const transport = new StdioServerTransport();
await server.connect(transport);
