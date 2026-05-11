"use strict";

(function registerLazywebWebMcp() {
  var PRODUCT_NAME = "Lazyweb";

  function hasWebMcp() {
    return Boolean(
      window.navigator &&
        window.navigator.modelContext &&
        typeof window.navigator.modelContext.provideContext === "function"
    );
  }

  function absoluteUrl(path) {
    return new URL(path, window.location.origin).toString();
  }

  function textResult(text, data) {
    var result = {
      content: [
        {
          type: "text",
          text: String(text || "")
        }
      ]
    };
    if (data !== undefined) result.structuredContent = data;
    return result;
  }

  async function fetchText(path, options) {
    var response = await fetch(path, options || {});
    var text = await response.text();
    if (!response.ok) {
      throw new Error("Lazyweb request failed for " + path + ": " + response.status + " " + text.slice(0, 240));
    }
    return {
      url: absoluteUrl(path),
      status: response.status,
      contentType: response.headers.get("content-type") || "",
      text: text
    };
  }

  async function fetchJson(path, options) {
    var payload = await fetchText(path, options);
    try {
      payload.json = JSON.parse(payload.text);
    } catch (err) {
      throw new Error("Lazyweb request did not return JSON for " + path + ": " + err.message);
    }
    return payload;
  }

  function resourcePath(resource) {
    var key = String(resource || "index").toLowerCase();
    var resources = {
      index: "/index.md",
      landing: "/index.md",
      llms: "/llms.txt",
      full: "/llms-full.txt",
      developers: "/developers.md",
      cursor: "/cursor.md",
      codex: "/codex.md",
      claude: "/claude.md",
      use: "/use-lazyweb.md",
      usage: "/use-lazyweb.md",
      pricing: "/pricing.md"
    };
    return resources[key] || resources.index;
  }

  var tools = [
    {
      name: "lazyweb_get_agent_context",
      description:
        "Fetch Lazyweb's agent-readable product context, setup docs, pricing, usage examples, or developer documentation as Markdown/plain text.",
      inputSchema: {
        type: "object",
        properties: {
          resource: {
            type: "string",
            enum: ["index", "landing", "llms", "full", "developers", "cursor", "codex", "claude", "use", "usage", "pricing"],
            description: "The Lazyweb agent resource to fetch."
          }
        },
        required: [],
        additionalProperties: false
      },
      execute: async function executeLazywebGetAgentContext(input) {
        var path = resourcePath(input && input.resource);
        var payload = await fetchText(path, {
          headers: {
            accept: path.endsWith(".md") ? "text/markdown" : "text/plain"
          }
        });
        return textResult(payload.text, {
          product: PRODUCT_NAME,
          resource: input && input.resource ? input.resource : "index",
          url: payload.url,
          contentType: payload.contentType
        });
      }
    },
    {
      name: "lazyweb_create_mcp_install_token",
      description:
        "Create a free Lazyweb MCP bearer token and return client-specific setup details for Cursor, Codex, Claude Code, Claude Desktop, and generic MCP clients.",
      inputSchema: {
        type: "object",
        properties: {},
        required: [],
        additionalProperties: false
      },
      execute: async function executeLazywebCreateMcpInstallToken() {
        var payload = await fetchJson("/api/mcp/install-token", {
          method: "POST",
          headers: {
            "content-type": "application/json",
            accept: "application/json"
          },
          body: "{}"
        });
        return textResult(JSON.stringify(payload.json, null, 2), {
          product: PRODUCT_NAME,
          tokenEndpoint: payload.url,
          install: payload.json
        });
      }
    },
    {
      name: "lazyweb_get_mcp_server_card",
      description:
        "Fetch Lazyweb's MCP Server Card, including serverInfo, Streamable HTTP transport endpoint, authentication, and tool capabilities.",
      inputSchema: {
        type: "object",
        properties: {},
        required: [],
        additionalProperties: false
      },
      execute: async function executeLazywebGetMcpServerCard() {
        var payload = await fetchJson("/.well-known/mcp/server-card.json", {
          headers: { accept: "application/json" }
        });
        return textResult(JSON.stringify(payload.json, null, 2), {
          product: PRODUCT_NAME,
          url: payload.url,
          serverCard: payload.json
        });
      }
    },
    {
      name: "lazyweb_get_agent_skill",
      description:
        "Fetch Lazyweb's Agent Skills Discovery index and the referenced SKILL.md instructions for installing and using Lazyweb MCP.",
      inputSchema: {
        type: "object",
        properties: {},
        required: [],
        additionalProperties: false
      },
      execute: async function executeLazywebGetAgentSkill() {
        var indexPayload = await fetchJson("/.well-known/agent-skills/index.json", {
          headers: { accept: "application/json" }
        });
        var skills = Array.isArray(indexPayload.json.skills) ? indexPayload.json.skills : [];
        var lazywebSkill = skills.find(function findLazywebSkill(skill) {
          return skill && skill.name === "lazyweb" && skill.url;
        });
        if (!lazywebSkill) {
          throw new Error("Lazyweb skill is missing from the agent skills index.");
        }
        var skillUrl = new URL(lazywebSkill.url, window.location.origin);
        var skillPayload = await fetchText(skillUrl.pathname + skillUrl.search, {
          headers: { accept: "text/markdown" }
        });
        return textResult(skillPayload.text, {
          product: PRODUCT_NAME,
          indexUrl: indexPayload.url,
          skillUrl: skillPayload.url,
          digest: lazywebSkill.digest,
          index: indexPayload.json
        });
      }
    },
    {
      name: "lazyweb_verify_mcp_tools",
      description:
        "Verify a Lazyweb MCP bearer token by initializing the Streamable HTTP MCP endpoint and listing the tools available to the agent.",
      inputSchema: {
        type: "object",
        properties: {
          token: {
            type: "string",
            minLength: 1,
            description: "Bearer token returned by lazyweb_create_mcp_install_token."
          },
          mcpUrl: {
            type: "string",
            description: "Optional MCP endpoint. Defaults to the current site's /mcp endpoint."
          }
        },
        required: ["token"],
        additionalProperties: false
      },
      execute: async function executeLazywebVerifyMcpTools(input) {
        var token = input && input.token;
        if (!token) throw new Error("token is required.");
        var mcpUrl = input && input.mcpUrl ? input.mcpUrl : absoluteUrl("/mcp");
        var initResponse = await fetch(mcpUrl, {
          method: "POST",
          headers: {
            "content-type": "application/json",
            accept: "application/json, text/event-stream",
            authorization: "Bearer " + token,
            "mcp-protocol-version": "2025-06-18"
          },
          body: JSON.stringify({
            jsonrpc: "2.0",
            id: 1,
            method: "initialize",
            params: {
              protocolVersion: "2025-06-18",
              capabilities: {},
              clientInfo: {
                name: "lazyweb-webmcp",
                version: "1.0.0"
              }
            }
          })
        });
        var initText = await initResponse.text();
        if (!initResponse.ok) {
          throw new Error("Lazyweb MCP initialize failed: " + initResponse.status + " " + initText.slice(0, 240));
        }
        var sessionId = initResponse.headers.get("mcp-session-id") || "";
        var headers = {
          "content-type": "application/json",
          accept: "application/json, text/event-stream",
          authorization: "Bearer " + token,
          "mcp-protocol-version": "2025-06-18"
        };
        if (sessionId) headers["mcp-session-id"] = sessionId;
        var initializedResponse = await fetch(mcpUrl, {
          method: "POST",
          headers: headers,
          body: JSON.stringify({
            jsonrpc: "2.0",
            method: "notifications/initialized",
            params: {}
          })
        });
        if (!initializedResponse.ok) {
          var initializedText = await initializedResponse.text();
          throw new Error("Lazyweb MCP initialized notification failed: " + initializedResponse.status + " " + initializedText.slice(0, 240));
        }
        var toolsResponse = await fetch(mcpUrl, {
          method: "POST",
          headers: headers,
          body: JSON.stringify({
            jsonrpc: "2.0",
            id: 2,
            method: "tools/list",
            params: {}
          })
        });
        var toolsText = await toolsResponse.text();
        if (!toolsResponse.ok) {
          throw new Error("Lazyweb MCP tools/list failed: " + toolsResponse.status + " " + toolsText.slice(0, 240));
        }
        return textResult(toolsText, {
          product: PRODUCT_NAME,
          mcpUrl: mcpUrl,
          initialized: true,
          sessionId: sessionId || null
        });
      }
    },
    {
      name: "lazyweb_open_mcp_install_page",
      description:
        "Return the Lazyweb MCP install page URL, and optionally open it for a human who wants to inspect or copy setup details.",
      inputSchema: {
        type: "object",
        properties: {
          open: {
            type: "boolean",
            description: "When true, open the install page in a new tab. Defaults to false."
          }
        },
        required: [],
        additionalProperties: false
      },
      execute: async function executeLazywebOpenMcpInstallPage(input) {
        var url = absoluteUrl("/mcp-install");
        if (input && input.open === true) {
          window.open(url, "_blank", "noopener");
        }
        return textResult(url, {
          product: PRODUCT_NAME,
          url: url,
          opened: Boolean(input && input.open === true)
        });
      }
    }
  ];

  function provideContext() {
    if (!hasWebMcp()) return;
    var maybePromise = window.navigator.modelContext.provideContext({ tools: tools });
    if (maybePromise && typeof maybePromise.catch === "function") {
      maybePromise.catch(function handleWebMcpError(err) {
        console.warn("Lazyweb WebMCP registration failed", err);
      });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", provideContext, { once: true });
  } else {
    provideContext();
  }
})();