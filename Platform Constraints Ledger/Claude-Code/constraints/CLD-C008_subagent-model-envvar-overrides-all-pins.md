---
id: CLD-C008
platform: Claude Code
domain: cost
severity: design-invalidating
status: active
provenance:
  - type: official-doc
    ref: code.claude.com/docs/en/sub-agents#choose-a-model
    date: 2026-08-06
  - type: official-doc
    ref: code.claude.com/docs/en/model-config#environment-variables
    date: 2026-08-06
verified: 2026-08-06
related: []
---

**Constraint:** The `CLAUDE_CODE_SUBAGENT_MODEL` environment variable has the HIGHEST precedence in subagent model resolution — above the per-invocation `model` parameter and above the definition frontmatter.

**Design consequence:** Setting this variable silently flattens an entire model-tier matrix, including any final-audit tier pinned to the most capable model. Every per-call pin in every workflow becomes inert with no error surfaced. Separately, an enterprise `availableModels` allowlist causes silent fallback: before CC v2.1.222 any blocked pin falls back to the inherited model, and from v2.1.222 only a blocked family alias substitutes to the newest permitted family version while full model IDs still fall back.

**Sanctioned workarounds:** Never set `CLAUDE_CODE_SUBAGENT_MODEL`. Run a routing preflight that asserts each tier resolved to its pinned model before any real spend, and abort the run on failure — this is the only defence against the allowlist silent-fallback path.
