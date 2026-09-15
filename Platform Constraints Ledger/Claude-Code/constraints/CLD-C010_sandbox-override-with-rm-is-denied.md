---
id: CLD-C010
platform: Claude Code
domain: governance
severity: friction
status: active
provenance:
  - type: session-verified
    ref: "2026-08-10 live proof — a Bash call with dangerouslyDisableSandbox:true containing rm -rf was DENIED by the permission guard; three sandbox-override calls without rm in the same session were approved"
    date: 2026-08-10
  - type: owner-confirmed
    ref: "owner reports seeing the same denial roughly 5 times on 2026-08-10"
    date: 2026-08-10
verified: 2026-08-10
related: []
---

**Constraint:** A single `Bash` tool call that sets `dangerouslyDisableSandbox: true` AND contains a destructive command (verified with `rm -rf`) is refused by the permission guard — the whole command is denied, not just the destructive part; the sandbox override carries no implicit authorization for destructive operations.

**Design consequence:** You cannot bundle a sandbox-disabled write batch (e.g. writing outside the workspace to a synced knowledge folder) with `rm -rf` cleanup in one command — the entire call is denied and the batched work is lost. Any script or agent step that relies on one-shot sandbox-disabled destructive ops fails, silently in an unattended flow. Destructive steps must be sequenced apart from the sandbox-override batch.

**Sanctioned workarounds:** Run destructive ops in their own `Bash` call WITHOUT `dangerouslyDisableSandbox` (let the standard permission prompt gate them); or avoid `rm -rf` — use a targeted `rm <specific path>`, or leave ephemeral artifacts in the session scratchpad (auto-cleaned). Reserve the sandbox override for non-destructive writes.
