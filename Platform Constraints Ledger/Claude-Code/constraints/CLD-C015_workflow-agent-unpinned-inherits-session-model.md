---
id: CLD-C015
platform: Claude Code
domain: cost
severity: design-invalidating
status: active
provenance:
  - type: official-doc
    ref: "Workflow tool contract — opts.model: when omitted the agent inherits the main-loop (resolved session) model"
    date: 2026-08-21
  - type: session-verified
    ref: "live 2026-08-21 — a Workflow with unpinned agent() calls was BLOCKED by workflow-model-pin-gate.py; the identical script passed once every agent() carried model + effort pins"
    date: 2026-08-21
verified: 2026-08-21
related: ["[[CLD-C008_subagent-model-envvar-overrides-all-pins]]", "[[CLD-C005_forks-always-inherit-driver-model]]"]
---

**Constraint:** A Workflow `agent()` call with no explicit `model` pin inherits the main-loop (resolved session) model rather than a tier-appropriate one — so in a premium-model (e.g. Fable) session every unpinned helper/worker runs at the premium tier.

**Design consequence:** A model-tier matrix (helpers=haiku · workers=sonnet · judges=opus · final-audit=fable) built on the assumption that agents default to a cheap tier is silently defeated — unpinned agents burn the premium/Fable budget with no error surfaced. Same silent-inheritance family as CLD-C008 (the subagent-model env var) and CLD-C005 (forks inherit the driver model): model resolution has multiple defaults-to-expensive paths.

**Sanctioned workarounds:** Pin `model` + `effort` on EVERY `agent()` per the tier matrix (helpers=haiku/low · workers=sonnet/medium · judges=opus/high · final-audit=claude-fable-5/xhigh; prefer a typed `schema` too). The `workflow-model-pin-gate.py` PreToolUse hook enforces it — it BLOCKS any `agent()` missing a `model` pin (and flags missing `effort`/`schema`) before the run starts; inheriting the session tier deliberately still requires writing that tier out as an explicit literal.
