---
id: CLD-C005
platform: Claude Code
domain: cost
severity: design-invalidating
status: active
provenance:
  - type: official-doc
    ref: code.claude.com/docs/en/sub-agents#fork-the-current-conversation
    date: 2026-08-06
verified: 2026-08-06
related: []
---

**Constraint:** A forked subagent (`subagent_type: fork`, or `/subtask`) ALWAYS inherits the driving session model and cannot be model-pinned; it also skips both subagent tool filters and receives the parent conversation full tool pool.

**Design consequence:** Forks are unpinnable by construction, so a tier-pinning scheme cannot cover them mechanically. In a top-tier session every fork is a top-tier agent with unrestricted tools — the exact inheritance cost that model tiering exists to prevent. A user-initiated `/subtask` does not route through the Agent tool, so hook gates cannot see it.

**Sanctioned workarounds:** Prefer a pinned named agent and pass the needed context in the prompt. Where a fork is genuinely required, record the deliberate choice (this environment requires a `PIN-OVERRIDE:` marker in the prompt). Note the one upside: a fork shares the parent prompt cache, so it is cheaper per token than a fresh subagent for equivalent context.
