> ## Documentation Index
> Fetch the complete documentation index at: https://docs.kapso.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Build with AI

> Give your AI agent the tools and context it needs to work with Kapso.

If you're building with Codex, Cursor, Claude, or another AI agent, start here.

This page gives your agent the fastest path into Kapso:

* the CLI for live project operations
* `llms.txt` for documentation context
* Kapso skills for code editing
* docs MCP for interactive browsing
* direct links to the most common starting points

## Prerequisite

A human still needs to create a Kapso project first. After that, your agent can either use the CLI setup flow or work directly with a project API key for APIs, SDKs, and docs integrations.

## Kapso CLI

For live project operations, start with the CLI.

```bash  theme={null}
curl -fsSL https://kapso.ai/install.sh | bash

kapso setup
kapso whatsapp numbers list
kapso whatsapp messages send --phone-number "<your-number>" --to 15551234567 --text "Hello"
```

Use the CLI when the agent needs to inspect project state, create setup links, manage webhooks, send messages, or work against a real Kapso project from a terminal session.

## Agent skills

If the agent is working inside a codebase, install Kapso skills:

```bash  theme={null}
npx skills add gokapso/agent-skills
```

Use skills when you want the agent to follow Kapso-specific workflows, scripts, and integration patterns while editing code.

## Docs

Use the docs when the agent needs current product and API context rather than live project access.

### llms.txt

Give your agent the Kapso docs in one file:

```text  theme={null}
https://docs.kapso.ai/llms.txt
```

This is the fastest way to give an agent current documentation context.

### MCP

If your agent supports MCP, connect the docs MCP server for interactive documentation browsing:

<CodeGroup>
  ```bash Codex theme={null}
  codex mcp add kapso-docs http https://docs.kapso.ai/mcp
  ```

  ```bash Claude Code theme={null}
  claude mcp add --transport http kapso-docs https://docs.kapso.ai/mcp
  ```

  ```json Cursor theme={null}
  {
    "mcpServers": {
      "kapso-docs": {
        "url": "https://docs.kapso.ai/mcp"
      }
    }
  }
  ```
</CodeGroup>

Use the same `https://docs.kapso.ai/mcp` endpoint in any MCP client that supports streamable HTTP.

## More pages

<CardGroup cols={2}>
  <Card title="Send messages" icon="message" href="/docs/whatsapp/send-messages/text">
    Start sending text, media, templates, and interactive messages.
  </Card>

  <Card title="Receive messages" icon="webhook" href="/docs/whatsapp/receive-messages">
    Receive WhatsApp events through Kapso webhooks or forwarded Meta payloads.
  </Card>

  <Card title="For your team" icon="users" href="/docs/platform/for-your-team">
    Use Kapso for support, operations, broadcasts, and inbox workflows.
  </Card>

  <Card title="Onboard customers" icon="building" href="/docs/platform/customer-guide">
    Let your customers connect their own WhatsApp accounts to your product.
  </Card>
</CardGroup>


Built with [Mintlify](https://mintlify.com).