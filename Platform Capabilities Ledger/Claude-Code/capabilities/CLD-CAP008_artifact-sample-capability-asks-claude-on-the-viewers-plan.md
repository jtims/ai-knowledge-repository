---
id: CLD-CAP008
platform: Claude Code
domain: data
leverage: unlocks
status: active
provenance:
  - type: official-doc
    ref: "claude.ai artifact runtime contract 0.2.52, platform-served type definitions (sample.d.ts) and the artifact-capabilities skill text for the sample capability: claude.use('sample'), sample(input, options) resolving text, truncated and modelTierApplied, sample.json for a parsed JSON value, options onText, signal, tools, images, modelTier and cache; consent per call on first use; 64 KiB input cap; one rejected error shape with stable codes. Read 2026-09-22 in an owner project while designing the Cover Letter Desk agentic layer. Not yet exercised live in this estate."
    date: 2026-09-22
verified: 2026-09-22
related: ["[[CLD-C031_artifact-page-network-is-blocked]]", "[[CLD-C032_artifact-sample-call-exposes-model-tier-only]]"]
---

**Capability:** Surface: the claude.ai artifact runtime. A published page that declares the sample capability can ask Claude from inside the page on the viewer's own plan: streamed text through onText, or a parsed JSON value through sample.json, with page functions offered as tools for a few rounds, images from the viewer's file pick, a five-minute answer cache, per-call consent on first use, a 64 KiB input cap and a single error shape to branch on.

**What it unlocks:** Agentic features inside a private artifact with no backend and no API key: analyze pasted text against data the page holds, return structured JSON the page renders as accept-or-reject controls, generate a draft straight into the page's editor, and read or change page state through tools. The viewer pays from their own plan, so a personal tool costs nothing to host, and nothing secret ever sits in the page.

**Caveats & linked constraints:** Model selection is by tier and may be substituted ([[CLD-C032_artifact-sample-call-exposes-model-tier-only|CLD-C032]]); the page has no network, so inputs arrive by paste, file pick, the artifact database or a connector ([[CLD-C031_artifact-page-network-is-blocked|CLD-C031]]); consent is per call and a decline ends the feature for the view; never retry from a loop; calls with tools are never cached; text inside page data can steer which tools Claude calls, so anything destructive needs a confirm step.
