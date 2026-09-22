---
id: CLD-C031
platform: Claude Code
domain: access
severity: design-invalidating
status: active
provenance:
  - type: official-doc
    ref: "claude.ai artifact runtime contract 0.2.52, platform-served type definitions (sample.d.ts, the images option): the page cannot fetch images from URLs because its network is blocked; and the runtime's page contract, which rules out cross-origin fetches and plain download links. Read 2026-09-22 through the artifact-capabilities skill in an owner project."
    date: 2026-09-22
  - type: session-verified
    ref: "owner session 4, 2026-09-22: the Cover Letter Desk design ruled out cross-origin font fetches under the page contract and published the fonts as same-origin artifact files, which the page fetches successfully. Not yet live-proven from inside an artifact page by a failing cross-origin fetch."
    date: 2026-09-22
verified: 2026-09-22
related: ["[[CLD-C032_artifact-sample-call-exposes-model-tier-only]]", "[[CLD-CAP008_artifact-sample-capability-asks-claude-on-the-viewers-plan]]"]
---

**Constraint:** Surface: the claude.ai artifact runtime. Page code in a published artifact has no outbound network beyond the artifact's own published files and the script and font sources the page contract allows; it cannot fetch a third-party URL, a public job-board API, an image by URL, or a backend of the owner's own.

**Design consequence:** Any artifact feature that starts from a URL (paste a link and read the page), or that would call an edge function, a proxy or the Claude API with a key held elsewhere, cannot be built inside the page. Data reaches the page by paste, by the viewer's file pick, through the artifact database written from a Claude Code session with ArtifactData, or through a connector the viewer has granted under the mcp capability. Since no backend is reachable, the page also cannot select a named model or an effort level for its Claude call ([[CLD-C032_artifact-sample-call-exposes-model-tier-only|CLD-C032]]).

**Sanctioned workarounds:** Paste the text into the page; fetch in Claude Code and file the content into the artifact database for the page to read; publish static data as artifact files; use the mcp capability for a viewer-granted connector; use the sample capability for the in-page Claude call ([[CLD-CAP008_artifact-sample-capability-asks-claude-on-the-viewers-plan|CLD-CAP008]]).
