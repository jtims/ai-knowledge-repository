---
id: CLD-C032
platform: Claude Code
domain: access
severity: design-invalidating
status: active
provenance:
  - type: official-doc
    ref: "claude.ai artifact runtime contract 0.2.52, platform-served type definitions (sample.d.ts): modelTier is the union quick, default, complex; SampleResult.modelTierApplied reports the tier that answered, which may be a substitute the viewer's plan allowed; there is no model ID, no effort option and no system role; Claude sees only the input passed. Read 2026-09-22 through the artifact-capabilities skill in an owner project."
    date: 2026-09-22
verified: 2026-09-22
related: ["[[CLD-C031_artifact-page-network-is-blocked]]", "[[CLD-CAP008_artifact-sample-capability-asks-claude-on-the-viewers-plan]]"]
---

**Constraint:** Surface: the claude.ai artifact runtime. The in-page Claude call (the sample capability) selects a model by tier only, quick, default or complex; it has no model ID, no effort setting, no system prompt, no browsing and no memory between calls, and the platform may substitute a cheaper tier when the viewer's plan lacks the one requested, reported after the fact in modelTierApplied.

**Design consequence:** A requirement of the form "run this step on a named model at a set effort" cannot be honored inside an artifact under any page design. The most a page can guarantee is a request for the complex tier and a display of the tier that actually answered. Named-model or effort-controlled work belongs in Claude Code (a subagent pinned by model and effort), in a direct API call from a host that holds a key, or on a Claude surface with a model picker such as the Chrome side panel or Cowork.

**Sanctioned workarounds:** Request modelTier complex and show modelTierApplied beside the result; put the instruction, the page's data and the output format in the input itself, under 64 KiB; move named-model work out of the page and hand its output back through the artifact database.
