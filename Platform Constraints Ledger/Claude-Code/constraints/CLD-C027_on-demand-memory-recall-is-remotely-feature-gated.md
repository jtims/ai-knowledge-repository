---
id: CLD-C027
platform: Claude Code
domain: data
severity: design-invalidating
status: active
provenance:
  - type: session-verified
    ref: "live 2026-09-02 - read from the shipped 2.1.235 Mach-O. startRelevantMemoryPrefetch (w3a) at offset 286,099,439 opens with an early return: if(!n||t.agentId||!my()||!ICe()||Pyv.has(r))return. ICe() at 277,088,217 is function ICe(){if(et(TENGU_MOTH_COPSE,false))return true;return mqo()} with mqo(){return !!process.env.CLAUDE_MEMORY_STORES?.trim()}. The only builder of a relevant_memories attachment is Iyv, whose sole caller sits inside w3a: regex over the full binary returns exactly two occurrences of the eFf( call token, its own definition at 286,069,841 and one call at 286,098,426"
    date: 2026-09-02
  - type: session-verified
    ref: "live 2026-09-02 - measured config. cachedGrowthBookFeatures.tengu_moth_copse is false and tengu_mill_orange is false in ~/.claude.json, 584 cached features, cachedGrowthBookFeaturesAt 1788370149072 = 2026-09-02T12:29:09. CLAUDE_MEMORY_STORES is unset in the process environment and absent from all six of .zshrc, .zshenv, .zprofile, global settings.json, settings.local.json and the project settings.json"
    date: 2026-09-02
  - type: session-verified
    ref: "live 2026-09-02 - no local override exists. readConfigOverrides(), setConfigOverride() and clearConfigOverrides() at offset 277,069,433 are empty-return no-ops, and getEnvironmentOverrides() at 277,069,081 carries an unconditional return statement placed BEFORE the line that would read the override env var, so that body is dead code. Regex over the full binary returns zero hits each for CLAUDE_CODE_FEATURE_FLAG, featureFlagOverrides, flagOverrides and FORCE_FEATURE"
    date: 2026-09-02
verified: 2026-09-02
related: ["[[CLD-C024_unindexed-memory-files-are-still-recallable]]", "[[CLD-C016_auto-memory-keys-one-store-per-repo-root]]", "[[CLD-CAP003_automemorydirectory-redirects-store-from-subdir]]"]
---

**Constraint:** Claude Code's on-demand memory recall, the second path that surfaces topic files without an index line, is **remotely feature-gated and does not run unless the gate is on**. The prefetch entry point returns before doing any work unless `ICe()` is true, and `ICe()` is satisfied only by the server-evaluated flag `tengu_moth_copse` or by a non-empty `CLAUDE_MEMORY_STORES` environment variable. The flag is resolved remotely and mirrored into `~/.claude.json`; the local override mechanisms are present as symbols but inert, so an operator cannot turn the path on. On this machine as of 2026-09-02 the flag is false, the env var is unset, and the path therefore never starts. A second flag, `tengu_mill_orange`, separately gates both the blocking consume of the result and the BM25 index variant of the search.

**Design consequence:** A memory-configuration design cannot treat on-demand recall as available. Where the gate is off, the **only** automatic surfacing channel is the always-on load of `MEMORY.md`, capped at 200 lines or 25,000 bytes, and every topic file without an index line is reached only when the model chooses to open it with an ordinary file tool. Three specific conclusions invert. First, de-indexing is not merely a downgrade from unconditional presence to conditional recall, it removes the automatic channel entirely. Second, an index-budget remediation that relocates pointers out of `MEMORY.md` costs those pointers their automatic surfacing, not merely their always-on presence, so the trade must be priced against a stub that a reader has to follow rather than against a retrieval path. Third, any experiment that measures recall latency, relevance or deadline behaviour has no referent while the gate is off: its negative result reads as NOT ENABLED and must never be scored as a failure of the mechanism. The gate is also entrypoint-sensitive in principle, because the entrypoint is one of the targeting attributes on the remote evaluation, so a value observed under one surface does not establish the value under another.

**Sanctioned workarounds:** Read the gate before relying on the path or designing an experiment about it: check `cachedGrowthBookFeatures.tengu_moth_copse` and `tengu_mill_orange` in `~/.claude.json` together with `CLAUDE_MEMORY_STORES`, and record both values and the `cachedGrowthBookFeaturesAt` timestamp beside any claim, because the cache refreshes on an interval. Treat an index line as the only reliable automatic channel for a fact that must not be missed, and budget index bytes on that basis. Do not attempt a local override; none of the override entry points is implemented. Re-verify after every upgrade, since the gate is a rollout flag rather than a fixed behaviour and its default may change without a changelog entry.
