---
id: CLD-C006
platform: Claude Code
domain: cost
severity: costly
status: active
provenance:
  - type: official-doc
    ref: code.claude.com/docs/en/sub-agents#what-loads-at-startup
    date: 2026-08-06
  - type: session-verified
    ref: 'measured locally: 486 lines / 32,564 bytes / ~8.1k tokens'
    date: 2026-08-06
verified: 2026-08-06
related: []
---

**Constraint:** Every built-in and custom subagent loads the entire CLAUDE.md hierarchy plus a git-status snapshot at startup. Only the built-in `Explore` and `Plan` agents skip them, and there is NO frontmatter field or per-agent setting to change which agents skip them.

**Design consequence:** The always-on instruction layer is a fixed per-agent tax that scales linearly with fan-out width. Measured at ~8.1k tokens per agent in this environment, a 30-agent fan-out carries roughly 244k tokens of preamble before any work is done. Fan-out width cannot be planned on model tier alone; the CLAUDE.md size is a multiplier on every vector except Explore and Plan.

**Sanctioned workarounds:** Keep CLAUDE.md lean (official guidance: aim under 200 lines) and move procedural detail into load-on-demand skills. Use `Explore`/`Plan` for recon so the tax is skipped. Prefer fewer, better-scoped agents over wide shallow fan-outs.
