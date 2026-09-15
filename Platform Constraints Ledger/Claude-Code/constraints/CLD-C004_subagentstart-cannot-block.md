---
id: CLD-C004
platform: Claude Code
domain: governance
severity: design-invalidating
status: active
provenance:
  - type: official-doc
    ref: code.claude.com/docs/en/hooks
    date: 2026-08-06
verified: 2026-08-06
related: []
---

**Constraint:** The `SubagentStart` hook event CANNOT block or deny a subagent from spawning — on any non-zero exit it only shows stderr to the user. It supports `additionalContext` injection and nothing else.

**Design consequence:** Pre-spawn enforcement cannot be built on `SubagentStart`. Any gate that must prevent a subagent from starting has to hook `PreToolUse` matched on the `Agent` tool, whose exit 2 stops the call before permission rules are evaluated. Blocking events are PreToolUse, PermissionRequest, UserPromptSubmit, Stop, SubagentStop, TeammateIdle, TaskCreated, TaskCompleted, PreCompact, and WorktreeCreate.

**Sanctioned workarounds:** Gate with `PreToolUse` on `Agent` (verified to fire in this environment 2026-08-06). Use `SubagentStart` for observability and context injection only; use `SubagentStop` for post-hoc validation, which can block.
