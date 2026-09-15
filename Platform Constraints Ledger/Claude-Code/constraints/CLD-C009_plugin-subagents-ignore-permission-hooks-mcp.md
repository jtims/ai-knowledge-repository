---
id: CLD-C009
platform: Claude Code
domain: governance
severity: design-invalidating
status: active
provenance:
  - type: official-doc
    ref: code.claude.com/docs/en/sub-agents#supported-frontmatter-fields
    date: 2026-08-06
  - type: official-doc
    ref: code.claude.com/docs/en/hooks
    date: 2026-08-06
verified: 2026-08-06
related: ["[[CLD-C001_description-hazard-chars-break-frontmatter-parsing]]", "[[CLD-C003_workflow-subagents-always-acceptedits]]"]
---

**Constraint:** A subagent supplied by a **plugin** silently IGNORES three frontmatter fields — `permissionMode`, `hooks`, and `mcpServers`. `model` and `effort` are still honoured, `tools` and `disallowedTools` are still honoured, and hooks declared at the plugin level in the plugin's `hooks/hooks.json` DO apply (including inside subagents). Plugin agent names may not contain `:` (reserved for plugin-scoped identifiers); a definition whose name contains one is not loaded and the error goes only to the debug log.

**Design consequence:** Per-agent permission scoping and per-agent MCP scoping cannot be shipped inside a plugin subagent definition — they are not rejected, they simply do nothing, so a least-privilege design built on those fields is void the moment the agent ships as part of a plugin rather than as a user/project definition. Any conditional enforcement must move to the plugin's `hooks/hooks.json` or to the consumer's own settings. Model tiering, by contrast, DOES port intact, so a tier matrix survives packaging. Live in this environment: `architects:backend-architect` and `architects:frontend-architect` are both registered with the full tool pool, which is the expected result of this constraint rather than a misconfiguration.

**Sanctioned workarounds:** Express least privilege through `tools` / `disallowedTools`, which are honoured for plugin subagents. Put conditional or blocking enforcement in the plugin's `hooks/hooks.json`, not in agent frontmatter. Keep `model` and `effort` pins in frontmatter — they work. Confirm a plugin agent's EFFECTIVE tool set against the harness registry rather than reading its definition file, per [[CLD-C001_description-hazard-chars-break-frontmatter-parsing]].
