---
id: CLD-C011
platform: Claude Code
domain: governance
severity: design-invalidating
status: active
provenance:
  - type: owner-confirmed
    ref: "owner correction 2026-08-11 — open -a Docker launched Docker Desktop with no prompt during the owner fix-batch session; ruled unacceptable (machine state requires explicit prior permission; announcing intent is not consent)"
    date: 2026-08-11
  - type: official-doc
    ref: "code.claude.com/docs/en/permission-modes#what-the-classifier-blocks-by-default + auto-mode-config — classifier blocks irreversible/destructive/outward-aimed only; ask rules 'always force a permission prompt, even in auto mode' and beat a competing allow rule"
    date: 2026-08-11
  - type: session-verified
    ref: "session 8f074569 transcript records permissionMode:auto; session-changelog.log line 8229 records the command executing unprompted; no allow/ask/deny rule matched (both settings files read — there was no ask array at all)"
    date: 2026-08-11
verified: 2026-08-11
related: ["[[CLD-C003_workflow-subagents-always-acceptedits]]", "[[CLD-C009_plugin-subagents-ignore-permission-hooks-mcp]]"]
---

**Constraint:** Permission mode `auto` routes unmatched Bash commands to a classifier whose default block list covers irreversible / destructive / outward-aimed actions ONLY — launching a local application (`open -a`), starting a local daemon or container/VM fleet, and installing software machine-wide are NOT blocked and execute with no prompt. `permissions.ask` rules (doc-guaranteed to prompt even in auto mode) and PreToolUse hooks are the only reliable gates, and both are evaluated before the classifier. An `allow` rule ALSO resolves before the classifier, so a machine-state allow entry (e.g. `Bash(brew install:*)`, found live in both settings files) is a standing silent-install hole in every mode.

**Design consequence:** Any governance design assuming "auto mode will stop machine-state actions" is invalid — the control does not exist unless explicitly built. Sessions on `defaultMode: auto` with no `ask` array had zero human signal on app launches, daemon starts, and installs (live-proven 2026-08-11: Docker Desktop launched silently mid-session). Hook/permission config is snapshotted at session start — a mitigation applied mid-session is not live until the next session, so an in-session "it prompted" check against fresh config is a false instrument.

**Sanctioned workarounds:** (1) `permissions.ask` glob rules for machine-state command families (applied 2026-08-11, settings.json v1.3 — 53 rules; `brew install`/`claude install` removed from allow in BOTH files); (2) PreToolUse Bash hook `~/.claude/hooks/machine-state-gate.sh` — compound-command + interpreter-wrapper aware, decision `ask` never silent-deny, 84-case matrix; (3) never place machine-state commands in `allow`. Residual (honest): wrapper scripts / Makefile targets / runtime-composed commands slip string matching, and MCP tools with machine side effects (e.g. iOS-simulator boot) are outside a Bash matcher entirely — companion `mcp__*` gate pending.
