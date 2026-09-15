---
id: CLD-C025
platform: Claude Code
domain: governance
severity: design-invalidating
status: active
provenance:
  - type: official-doc
    ref: "code.claude.com/docs/en/sub-agents#enable-persistent-memory - verbatim: 'Read, Write, and Edit tools are automatically enabled so the subagent can manage its memory files.' Same page gives the three scopes and locations, and states the field has no effect when auto memory is off"
    date: 2026-09-01
verified: 2026-09-01
related: ["[[CLD-C001_description-hazard-chars-break-frontmatter-parsing]]", "[[CLD-C016_auto-memory-keys-one-store-per-repo-root]]"]
---

**Constraint:** Declaring a `memory:` field on a subagent definition **automatically enables the Read, Write and Edit tools on that agent**, irrespective of the `tools:` list the definition declares. Scopes and locations: `user` at `~/.claude/agent-memory/<name-of-agent>/`, `project` at `.claude/agent-memory/<name-of-agent>/`, `local` at `.claude/agent-memory-local/<name-of-agent>/`. The field has **no effect at all** when auto memory is disabled, via `autoMemoryEnabled` or `CLAUDE_CODE_DISABLE_AUTO_MEMORY`, and the agent then launches with neither the memory instructions nor the tool access.

**Design consequence:** Any least-privilege tiering expressed through agent frontmatter is **silently widened** by adding memory to it. A tier designed to be read-only (helper, explorer and auditor seats whose whole contract is that they cannot write) acquires filesystem write capability that the roster does not declare and that no reviewer reading the `tools:` line would expect. The widening is invisible in the definition, and because frontmatter in this harness has a known silent mis-parse class, a YAML parse of the definition cannot detect either the widening or its absence. The reverse coupling is equally load-bearing: a design that depends on subagent memory is inert the moment auto memory is turned off anywhere in the settings chain, with the agent still spawning normally.

**Sanctioned workarounds:** Declare `memory:` only on tiers where write access is already sanctioned (worker, judge and architect seats); never on a read-only tier, where the widening defeats the contract the tier exists to enforce. Verify the effective tool pool against the harness agent registry, never against a YAML parse, per `CLD-C001`. Treat a memory-dependent agent design as conditional on `autoMemoryEnabled` and assert that setting rather than assuming it.
