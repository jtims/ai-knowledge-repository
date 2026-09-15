---
id: CLD-CAP001
platform: Claude Code
domain: governance
leverage: unlocks
status: active
provenance:
  - type: session-verified
    ref: "2026-08-10 build — UserPromptSubmit inject hook + PostToolUse validate-on-write tripwire built and functionally tested this session; validate-ledger.py kept canonical in the synced folder and symlinked into ~/.claude/hooks/ (one source, both surfaces)"
    date: 2026-08-10
verified: 2026-08-10
related: ["[[CLD-C009_plugin-subagents-ignore-permission-hooks-mcp]]"]
---

**Capability:** Claude Code hooks run deterministic code at fixed lifecycle points — `UserPromptSubmit` can inject context into the model's turn, and `PostToolUse` can validate or report on a write the moment it lands — and a tool kept canonical in the synced folder can be symlinked into `~/.claude/hooks/`, so a single source governs every surface without drift.

**What it unlocks:** Enforceable, drift-proof decision-time governance (the Platform Constraints/Capabilities ledgers' keyword injection and validate-on-write tripwire) instead of relying on advisory model memory or knowledge files that never enforce. If you assume governance can only live in fallible context, you rule out mechanisms that actually hold.

**Caveats & linked constraints:** `PostToolUse` cannot BLOCK — the write already happened, so the hook reports and the enforcing gate remains a required check before "done", not the hook itself. Plugin/subagent contexts do not honour all hook wiring — see [[CLD-C009_plugin-subagents-ignore-permission-hooks-mcp]]. Injection feeds RAW text to the model, so a malformed injected node reaches context looking authoritative — validate what you inject.
