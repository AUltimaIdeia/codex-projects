import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";

loadDotEnv();

const DEFAULT_API_VERSION = process.env.META_API_VERSION || "v25.0";
const DEFAULT_REDIRECT_URI =
  process.env.META_REDIRECT_URI || "http://127.0.0.1:8787/callback";

function loadDotEnv() {
  const envPath = resolve(process.cwd(), ".env");
  if (!existsSync(envPath)) {
    return;
  }

  const lines = readFileSync(envPath, "utf8").split(/\r?\n/u);
  for (const rawLine of lines) {
    const line = rawLine.trim();
    if (!line || line.startsWith("#")) {
      continue;
    }

    const separatorIndex = line.indexOf("=");
    if (separatorIndex === -1) {
      continue;
    }

    const key = line.slice(0, separatorIndex).trim();
    const value = line.slice(separatorIndex + 1).trim().replace(/^['"]|['"]$/g, "");
    if (!key || process.env[key] !== undefined) {
      continue;
    }
    process.env[key] = value;
  }
}

function requiredEnv(name) {
  const value = process.env[name];
  if (!value) {
    throw new Error(`Missing required environment variable: ${name}`);
  }
  return value;
}

export function getMetaConfig() {
  const accessToken = requiredEnv("META_ACCESS_TOKEN");
  const appId = process.env.META_APP_ID || "";
  const appSecret = process.env.META_APP_SECRET || "";
  const apiVersion = process.env.META_API_VERSION || DEFAULT_API_VERSION;
  const redirectUri = process.env.META_REDIRECT_URI || DEFAULT_REDIRECT_URI;
  const allowedAccountIds = new Set(
    (process.env.META_AD_ACCOUNT_IDS || "")
      .split(",")
      .map((value) => value.trim())
      .filter(Boolean)
      .map(stripActPrefix),
  );

  return {
    accessToken,
    appId,
    appSecret,
    apiVersion,
    redirectUri,
    allowedAccountIds,
  };
}

export function stripActPrefix(accountId) {
  return String(accountId).replace(/^act_/, "");
}

export function normalizeAccountId(accountId) {
  const bare = stripActPrefix(accountId);
  if (!bare) {
    throw new Error("account_id is required");
  }
  return `act_${bare}`;
}

function buildGraphUrl(path, params = {}, config = getMetaConfig()) {
  const cleanPath = path.startsWith("/") ? path.slice(1) : path;
  const url = new URL(`https://graph.facebook.com/${config.apiVersion}/${cleanPath}`);

  for (const [key, value] of Object.entries(params)) {
    if (value === undefined || value === null || value === "") {
      continue;
    }
    if (Array.isArray(value)) {
      url.searchParams.set(key, value.join(","));
      continue;
    }
    if (typeof value === "object") {
      url.searchParams.set(key, JSON.stringify(value));
      continue;
    }
    url.searchParams.set(key, String(value));
  }

  url.searchParams.set("access_token", config.accessToken);
  return url;
}

async function graphGet(path, params = {}, config = getMetaConfig()) {
  const url = buildGraphUrl(path, params, config);
  const response = await fetch(url, {
    method: "GET",
    headers: {
      Accept: "application/json",
    },
  });

  const payload = await response.json().catch(() => ({}));
  if (!response.ok || payload.error) {
    const message =
      payload?.error?.message ||
      `Meta API request failed with status ${response.status}`;
    throw new Error(message);
  }

  return payload;
}

function applyAccountAllowlist(accounts, config) {
  if (config.allowedAccountIds.size === 0) {
    return accounts;
  }

  return accounts.filter((account) =>
    config.allowedAccountIds.has(stripActPrefix(account.account_id || account.id)),
  );
}

function numberOrNull(value) {
  if (value === undefined || value === null || value === "") {
    return null;
  }
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

function parseActionCollection(items) {
  const result = {};
  for (const item of items || []) {
    if (!item?.action_type) {
      continue;
    }
    result[item.action_type] = numberOrNull(item.value) || 0;
  }
  return result;
}

function toMetricSnapshot(row) {
  const actions = parseActionCollection(row.actions);
  const actionValues = parseActionCollection(row.action_values);
  const purchaseRoas = Array.isArray(row.purchase_roas)
    ? row.purchase_roas.map((item) => ({
        action_type: item.action_type,
        value: numberOrNull(item.value),
      }))
    : [];

  return {
    campaign_id: row.campaign_id,
    campaign_name: row.campaign_name,
    clicks: numberOrNull(row.clicks),
    cpc: numberOrNull(row.cpc),
    cpm: numberOrNull(row.cpm),
    ctr: numberOrNull(row.ctr),
    frequency: numberOrNull(row.frequency),
    impressions: numberOrNull(row.impressions),
    reach: numberOrNull(row.reach),
    spend: numberOrNull(row.spend),
    actions,
    action_values: actionValues,
    purchase_roas: purchaseRoas,
  };
}

function buildDiagnosticNotes(snapshot) {
  const notes = [];

  if ((snapshot.impressions || 0) === 0) {
    notes.push("No delivery in the selected window.");
  }
  if ((snapshot.spend || 0) > 0 && (snapshot.clicks || 0) === 0) {
    notes.push("Spend occurred without any recorded clicks.");
  }
  if (snapshot.ctr !== null && snapshot.ctr < 0.7) {
    notes.push("CTR is low enough to merit creative, audience, or offer review.");
  }
  if (snapshot.frequency !== null && snapshot.frequency > 3) {
    notes.push("Frequency is elevated; watch for audience fatigue.");
  }

  const roasValue =
    snapshot.purchase_roas.find((item) => item.value !== null)?.value ?? null;
  if (roasValue !== null && roasValue < 1) {
    notes.push("Purchase ROAS is below 1.0 in the selected window.");
  }

  const purchaseValue =
    snapshot.action_values["omni_purchase"] ||
    snapshot.action_values["offsite_conversion.fb_pixel_purchase"] ||
    snapshot.action_values["purchase"];

  if ((snapshot.spend || 0) > 0 && !purchaseValue) {
    notes.push("Spend is present but no purchase value was returned.");
  }

  if (notes.length === 0) {
    notes.push("No obvious diagnostic flags were detected from the selected metrics.");
  }

  return notes;
}

function dateParams({ datePreset, since, until }) {
  if (datePreset) {
    return { date_preset: datePreset };
  }
  if (since && until) {
    return { time_range: { since, until } };
  }
  return { date_preset: "last_30d" };
}

export async function validateConnection(config = getMetaConfig()) {
  const me = await graphGet("/me", { fields: "id,name" }, config);
  const adAccountsResponse = await graphGet(
    "/me/adaccounts",
    {
      fields:
        "id,name,account_id,account_status,currency,timezone_name,business_name",
      limit: 100,
    },
    config,
  );

  const adAccounts = applyAccountAllowlist(adAccountsResponse.data || [], config);

  return {
    api_version: config.apiVersion,
    redirect_uri: config.redirectUri,
    user: me,
    ad_accounts: adAccounts,
  };
}

export async function listAdAccounts(config = getMetaConfig()) {
  const payload = await validateConnection(config);
  return payload.ad_accounts;
}

export async function listCampaigns(
  { accountId, limit = 50, effectiveStatus = [] },
  config = getMetaConfig(),
) {
  const account = normalizeAccountId(accountId);
  const params = {
    fields:
      "id,name,status,effective_status,objective,buying_type,created_time,updated_time,daily_budget,lifetime_budget,start_time,stop_time",
    limit,
  };

  if (effectiveStatus.length > 0) {
    params.effective_status = effectiveStatus;
  }

  const payload = await graphGet(`/${account}/campaigns`, params, config);
  return payload.data || [];
}

export async function getInsights(
  {
    accountId,
    level = "campaign",
    limit = 50,
    datePreset,
    since,
    until,
    fields,
    filtering,
  },
  config = getMetaConfig(),
) {
  const account = normalizeAccountId(accountId);
  const defaultFields = [
    "account_id",
    "account_name",
    "campaign_id",
    "campaign_name",
    "adset_id",
    "adset_name",
    "ad_id",
    "ad_name",
    "impressions",
    "reach",
    "clicks",
    "spend",
    "cpc",
    "cpm",
    "ctr",
    "frequency",
    "actions",
    "action_values",
    "purchase_roas",
  ];

  const params = {
    level,
    fields: fields?.length ? fields : defaultFields,
    limit,
    filtering,
    ...dateParams({ datePreset, since, until }),
  };

  const payload = await graphGet(`/${account}/insights`, params, config);
  return payload.data || [];
}

export async function campaignDiagnostics(
  { accountId, limit = 25, datePreset, since, until },
  config = getMetaConfig(),
) {
  const campaigns = await listCampaigns({ accountId, limit: 200 }, config);
  const insights = await getInsights(
    {
      accountId,
      level: "campaign",
      limit,
      datePreset,
      since,
      until,
      fields: [
        "campaign_id",
        "campaign_name",
        "impressions",
        "reach",
        "clicks",
        "spend",
        "cpc",
        "cpm",
        "ctr",
        "frequency",
        "actions",
        "action_values",
        "purchase_roas",
      ],
    },
    config,
  );

  const campaignMap = new Map(
    campaigns.map((campaign) => [campaign.id, campaign]),
  );

  return insights.map((row) => {
    const snapshot = toMetricSnapshot(row);
    const campaign = campaignMap.get(snapshot.campaign_id) || {};

    return {
      ...snapshot,
      status: campaign.status || null,
      effective_status: campaign.effective_status || null,
      objective: campaign.objective || null,
      notes: buildDiagnosticNotes(snapshot),
    };
  });
}

export function createAuthUrl({
  appId,
  redirectUri = DEFAULT_REDIRECT_URI,
  scope = ["ads_read", "business_management"],
  state = "meta-ads-diagnostics",
}) {
  if (!appId) {
    throw new Error("appId is required to build the auth URL.");
  }
  const url = new URL("https://www.facebook.com/dialog/oauth");
  url.searchParams.set("client_id", appId);
  url.searchParams.set("redirect_uri", redirectUri);
  url.searchParams.set("scope", scope.join(","));
  url.searchParams.set("response_type", "code");
  url.searchParams.set("state", state);
  return url.toString();
}

export async function exchangeCodeForToken({
  appId,
  appSecret,
  redirectUri = DEFAULT_REDIRECT_URI,
  code,
  apiVersion = DEFAULT_API_VERSION,
}) {
  if (!appId || !appSecret || !code) {
    throw new Error("appId, appSecret, and code are required.");
  }

  const url = new URL(`https://graph.facebook.com/${apiVersion}/oauth/access_token`);
  url.searchParams.set("client_id", appId);
  url.searchParams.set("client_secret", appSecret);
  url.searchParams.set("redirect_uri", redirectUri);
  url.searchParams.set("code", code);

  const response = await fetch(url);
  const payload = await response.json();
  if (!response.ok || payload.error) {
    throw new Error(payload?.error?.message || "Failed to exchange code for token.");
  }
  return payload;
}

export async function exchangeForLongLivedToken({
  appId,
  appSecret,
  token,
  apiVersion = DEFAULT_API_VERSION,
}) {
  if (!appId || !appSecret || !token) {
    throw new Error("appId, appSecret, and token are required.");
  }

  const url = new URL(`https://graph.facebook.com/${apiVersion}/oauth/access_token`);
  url.searchParams.set("grant_type", "fb_exchange_token");
  url.searchParams.set("client_id", appId);
  url.searchParams.set("client_secret", appSecret);
  url.searchParams.set("fb_exchange_token", token);

  const response = await fetch(url);
  const payload = await response.json();
  if (!response.ok || payload.error) {
    throw new Error(
      payload?.error?.message || "Failed to exchange for a long-lived token.",
    );
  }
  return payload;
}
