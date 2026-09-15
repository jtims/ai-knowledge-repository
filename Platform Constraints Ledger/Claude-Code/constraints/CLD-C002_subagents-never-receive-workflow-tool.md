---
id: CLD-C002
platform: Claude Code
domain: governance
severity: design-invalidating
status: active
provenance:
  - type: official-doc
    ref: code.claude.com/docs/en/sub-agents#available-tools
    date: 2026-08-06
verified: 2026-08-06
related: []
---

**Constraint:** Every subagent has the `Workflow` tool removed, along with `AskUserQuestion`, `EnterPlanMode`, `ScheduleWakeup`, `TaskOutput`, `WaitForMcpServers`, `EndConversation`, and `ExitPlanMode` (the last unless `permissionMode: plan`).

**Design consequence:** A subagent can never launch a dynamic workflow, so any design where a delegated agent "kicks off a workflow" is impossible. Nested fan-out must be Agent-tool based and is bounded by the spawn-depth limit. Also: a background subagent keeps every MCP tool but only a reduced built-in set, and the removal is reported as NO error — the same definition resolves to different tools in foreground versus background.

**Sanctioned workarounds:** Orchestrate workflows only from the main session. For nested fan-out, give the parent subagent the `Agent` tool and stay within the depth limit. Set `background: false` when a subagent needs a built-in outside the background set.
