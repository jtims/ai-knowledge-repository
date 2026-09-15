---
id: CLD-C003
platform: Claude Code
domain: access
severity: design-invalidating
status: active
provenance:
  - type: official-doc
    ref: code.claude.com/docs/en/workflows#approve-the-plan-before-it-runs
    date: 2026-08-06
verified: 2026-08-06
related: []
---

**Constraint:** Subagents spawned by a dynamic workflow ALWAYS run in `acceptEdits` mode and inherit the session tool allowlist, regardless of the session permission mode. File edits are auto-approved.

**Design consequence:** Permission mode cannot be used to contain a workflow run. A session in default or plan mode still spawns workflow agents that write files without prompting, so any containment design resting on session permission mode is void for workflow vectors. Hook-based controls remain effective because settings-file hooks DO fire inside subagents.

**Sanctioned workarounds:** Contain workflow writes with PreToolUse hooks (which fire inside subagents) rather than permission modes; scope agent `tools`/`disallowedTools`; keep write paths inside a designated out_dir; pre-add required commands to the allowlist so long runs do not stall.
