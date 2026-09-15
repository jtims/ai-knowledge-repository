---
id: CLD-C017
platform: Claude Code
domain: governance
severity: design-invalidating
status: active
provenance:
  - type: session-verified
    ref: 'live probes 2026-08-22 (an owner session, RB sequence) - fresh headless session, bare rb-worker spawn = registry miss with available-agents list showing only reasoning-bundle:rb-worker/rb-judge/rb-auditor; namespaced spawn SUCCEEDED same probe; graph-of-thought Phase-0 preflight ABORTED on bare agentTypes both in-session and in a fresh process until qualified (fix commit ee46f7f, the private origin/reasoning-bundle)'
    date: 2026-08-22
  - type: session-verified
    ref: 'live proof 2026-08-22 (same session, owner-approved addendum) - installPath resolved to ~/.claude/plugins/cache/reasoning-bundle/reasoning-bundle/0.2.0 pinned at gitCommitSha d891946 while the source directory carried fix ee46f7f; claude plugin update no-oped ("already at the latest version") until the manifest version bumped to 0.2.1 (548aeff), after which the new cache carried all fixes'
    date: 2026-08-22
verified: 2026-08-22
related: ["[[CLD-C009_plugin-subagents-ignore-permission-hooks-mcp]]", "[[CLD-C001_description-hazard-chars-break-frontmatter-parsing]]"]
---

**Constraint:** An agent bundled inside an installed plugin registers in the harness agent registry ONLY under its namespace-qualified id `<plugin-name>:<agent-name>`; the bare agent name does not resolve for Agent-tool `subagent_type` or Workflow `agentType` references (registry miss), even though the definition file's own `name:` field is the bare name.

**Design consequence:** Any workflow, script, hook, or harness config that hardcodes a bare agentType silently breaks the moment its roster ships inside a plugin — live-proven by the reasoning-bundle `graph-of-thought` workflow, whose Phase-0 preflight aborted on all three tiers (in the installing session AND in a fresh process) until every reference was qualified. The complementary fact in [[CLD-C009_plugin-subagents-ignore-permission-hooks-mcp]] (a plugin agent's declared `name` may not contain `:`) means qualified ids can never collide with declared names. Three compounding traps: registration is session-start-snapshotted, so a plugin installed mid-session never registers in the installing session; definition-scanning gates that only read `~/.claude/agents` / `./.claude/agents` (pre-agent-pin-gate class) treat plugin agents as pin-less unless taught to resolve installed-plugin paths; and a directory-source install is a SNAPSHOT copied into a version-keyed cache (`~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/`) — edits to the source directory never propagate to sessions, and `claude plugin update` no-ops while the manifest `version` string is unchanged, so a dev loop that edits, relaunches, and re-tests is silently testing the stale snapshot.

**Sanctioned workarounds:** Qualify every spawn reference with the plugin name from `plugin.json` `name` (stable across installs); a plugin's own workflows self-reference their bundled roster namespace-qualified. Verify registration against the harness registry (a spawn probe, or the failure message's available-agents list), never against the definition file, per [[CLD-C001_description-hazard-chars-break-frontmatter-parsing]]. Treat any mid-session plugin install as next-session-effective. Definition-scanning hooks must resolve installed plugins (via `~/.claude/plugins/installed_plugins.json` installPath) before assuming a namespaced type is unpinned. To propagate source edits to the install: bump the manifest `version` (patch release), then `claude plugin update <plugin>@<marketplace>` and verify the new cache dir carries the change (grep the cached file + check `gitCommitSha`) — never trust a fresh session alone to pick up source-directory edits.
