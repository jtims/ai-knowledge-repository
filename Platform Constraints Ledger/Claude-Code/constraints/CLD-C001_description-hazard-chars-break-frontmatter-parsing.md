---
id: CLD-C001
platform: Claude Code
domain: governance
severity: design-invalidating
status: active
provenance:
  - type: session-verified
    ref: live proof 2026-08-06 — owner session record
    date: 2026-08-06
  - type: session-verified
    ref: harness agent registry observed before/after the fix
    date: 2026-08-06
verified: 2026-08-06
related: []
---

**Constraint:** A subagent or skill `description` containing a space-hash sequence, or written as a double-quoted YAML scalar with backslash-escaped inner quotes, is accepted by strict YAML parsers but MIS-PARSED by the Claude Code harness — the definition either fails to register at all, or silently loses later frontmatter keys such as `tools:` and `model:`.

**Design consequence:** Agent and skill definitions cannot be validated by a YAML parse alone. A definition can pass PyYAML and still be absent from the registry, or load with the full tool pool and an inherited model instead of its declared pins — which silently defeats any tier-pinning or least-privilege scheme built on frontmatter. Two agents were observed in this state: `transcript-distiller` vanished from the registry entirely with escaped quotes, then loaded with `All tools` while a space-hash remained in a single-quoted description.

**Sanctioned workarounds:** Keep descriptions free of space-hash sequences and inner double quotes; put literal formatting syntax in the body, never the description. Single-quote every description (doubling any apostrophes). Verify against the harness registry, not a YAML parse. Enforced mechanically by `~/.claude/hooks/validate-agent-roster.py` (E2/E3) and checked by `/drift-audit` steps 3c and 3d.
