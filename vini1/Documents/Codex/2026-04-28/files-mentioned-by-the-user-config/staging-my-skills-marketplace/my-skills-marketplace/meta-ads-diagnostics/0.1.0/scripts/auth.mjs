import {
  createAuthUrl,
  exchangeCodeForToken,
  exchangeForLongLivedToken,
} from "./meta-api.mjs";

function parseArgs(argv) {
  const [command, ...rest] = argv;
  const flags = {};

  for (let index = 0; index < rest.length; index += 1) {
    const item = rest[index];
    if (!item.startsWith("--")) {
      continue;
    }
    const key = item.slice(2);
    const next = rest[index + 1];
    if (!next || next.startsWith("--")) {
      flags[key] = true;
      continue;
    }
    flags[key] = next;
    index += 1;
  }

  return { command, flags };
}

function getEnvOrFlag(flags, key, envName) {
  return flags[key] || process.env[envName] || "";
}

function printHelp() {
  console.log(`Usage:
  node ./scripts/auth.mjs url [--open]
  node ./scripts/auth.mjs exchange --code "<CODE>"
  node ./scripts/auth.mjs long-lived --token "<SHORT_LIVED_TOKEN>"

Environment:
  META_APP_ID
  META_APP_SECRET
  META_REDIRECT_URI
  META_API_VERSION
`);
}

async function main() {
  const { command, flags } = parseArgs(process.argv.slice(2));

  if (!command || command === "help" || command === "--help") {
    printHelp();
    return;
  }

  if (command === "url") {
    const appId = getEnvOrFlag(flags, "app-id", "META_APP_ID");
    const redirectUri =
      getEnvOrFlag(flags, "redirect-uri", "META_REDIRECT_URI") ||
      "http://127.0.0.1:8787/callback";
    const scope = String(flags.scope || "ads_read,business_management")
      .split(",")
      .map((item) => item.trim())
      .filter(Boolean);

    const url = createAuthUrl({ appId, redirectUri, scope });
    console.log(url);

    if (flags.open) {
      const { spawn } = await import("node:child_process");
      spawn("open", [url], { stdio: "ignore", detached: true }).unref();
    }
    return;
  }

  if (command === "exchange") {
    const appId = getEnvOrFlag(flags, "app-id", "META_APP_ID");
    const appSecret = getEnvOrFlag(flags, "app-secret", "META_APP_SECRET");
    const redirectUri =
      getEnvOrFlag(flags, "redirect-uri", "META_REDIRECT_URI") ||
      "http://127.0.0.1:8787/callback";
    const code = flags.code || "";

    const payload = await exchangeCodeForToken({
      appId,
      appSecret,
      redirectUri,
      code,
      apiVersion: getEnvOrFlag(flags, "api-version", "META_API_VERSION") || "v25.0",
    });

    console.log(JSON.stringify(payload, null, 2));
    return;
  }

  if (command === "long-lived") {
    const appId = getEnvOrFlag(flags, "app-id", "META_APP_ID");
    const appSecret = getEnvOrFlag(flags, "app-secret", "META_APP_SECRET");
    const token = flags.token || process.env.META_ACCESS_TOKEN || "";

    const payload = await exchangeForLongLivedToken({
      appId,
      appSecret,
      token,
      apiVersion: getEnvOrFlag(flags, "api-version", "META_API_VERSION") || "v25.0",
    });

    console.log(JSON.stringify(payload, null, 2));
    return;
  }

  throw new Error(`Unknown command: ${command}`);
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exitCode = 1;
});
