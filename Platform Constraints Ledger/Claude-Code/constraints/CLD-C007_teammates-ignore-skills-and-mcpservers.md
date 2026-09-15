---
id: CLD-C007
platform: Claude Code
domain: governance
severity: design-invalidating
status: active
provenance:
  - type: official-doc
    ref: code.claude.com/docs/en/agent-teams
    date: 2026-08-06
verified: 2026-08-06
related: []
---

**Constraint:** Agent-team teammates do NOT inherit the lead `/model` selection, they DO inherit the lead effort level, and a subagent definition `skills` and `mcpServers` frontmatter is IGNORED when that definition runs as a teammate.

**Design consequence:** A tier-pinned agent definition does not carry its full configuration into a team. Model must be named explicitly in the spawn prompt or via the default-teammate-model setting, and any design relying on preloaded skills or scoped MCP servers silently loses them. Teammates also start with the lead permission mode and cannot be given per-teammate modes at spawn; teams break `/resume` for in-process teammates.

**Sanctioned workarounds:** Name the model explicitly per teammate; restate needed skill content in the spawn prompt; partition files so no two teammates edit the same one. Enable teams per-run at launch only, never in settings env, because the feature is experimental and resume-breaking.
