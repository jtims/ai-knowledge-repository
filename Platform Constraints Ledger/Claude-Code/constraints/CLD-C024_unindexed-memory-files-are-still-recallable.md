---
id: CLD-C024
platform: Claude Code
domain: data
severity: design-invalidating
status: active
provenance:
  - type: session-verified
    ref: "live 2026-09-01 - read from the shipped 2.1.235 Mach-O at byte offset ~281,497,836. Module exports {formatMemoryManifest, isRecallVisiblePath, loadedIndexExclusions, recallVisibleTeamMounts, scanMemoryFiles, scanMemoryHeaders}; loadedIndexExclusions() seeds a Set containing MEMORY.md plus each mount's own promptIndex; scanMemoryHeaders filters c.endsWith('.md') and otherwise falls back to path.basename(c) !== 'MEMORY.md'; relevance key is frontmatter.description ?? firstHeading(body) truncated at 120 chars; manifest line format is - [name](path): description"
    date: 2026-09-01
  - type: official-doc
    ref: "code.claude.com/docs/en/memory - 'Claude Code doesn't load topic files such as user_role.md or feedback_testing.md at startup. Claude reads them on demand using its standard file tools when it needs the information', plus the 'Recalled 2 memories' interface note"
    date: 2026-09-01
verified: 2026-09-01
related: ["[[CLD-C027_on-demand-memory-recall-is-remotely-feature-gated]]", "[[CLD-C016_auto-memory-keys-one-store-per-repo-root]]", "[[CLD-CAP003_automemorydirectory-redirects-store-from-subdir]]"]
---

**QUALIFIED 2026-09-02, and the qualifier is load-bearing: this node describes a MECHANISM that is REMOTELY GATED OFF on this machine.** See [[CLD-C027_on-demand-memory-recall-is-remotely-feature-gated]]. The prefetch entry point returns before doing any work unless `tengu_moth_copse` is true or `CLAUDE_MEMORY_STORES` is set; both were measured false and unset on 2026-09-02, with no local override available. Everything below remains correct about what the code does and how relevance is computed, and remains the right basis for reasoning about store hygiene and about what happens if the gate turns on. It is NOT a basis for treating an unindexed file as automatically reachable today. Read the two nodes together.

**Constraint:** A topic file in an auto-memory store with **no `MEMORY.md` index line is still reachable**. Alongside the always-on load of `MEMORY.md` (first 200 lines / 25,000 B), the harness runs a second, on-demand path that enumerates the store **directory**, filters to `*.md`, and **excludes `MEMORY.md` itself by basename**, ranking each remaining file on its own `description:` frontmatter (falling back to the file's first heading, truncated at 120 characters).

**Design consequence:** An index line buys **unconditional presence**, not **reachability**, and it costs bytes against the 25,000 B load cap in every single session. Two design conclusions that look obvious are therefore invalid. First, "unindexed memory is inert" is false: a stale, superseded or policy-contradicting memory file can be surfaced into a live turn with nothing in the index pointing at it, which makes de-indexing a **worse** disposal than deleting. Second, "moving pointers out of `MEMORY.md` orphans their files" is also false, so an index-budget remediation that relocates a registry does not cost those files their recall. Relevance is computed from each file's own frontmatter, so store hygiene governs recall quality directly and the index does not govern it at all. Recall is bounded rather than guaranteed: a blocking deadline exists, so presence in the store is necessary but not sufficient.

**Sanctioned workarounds:** Read the gate ([[CLD-C027_on-demand-memory-recall-is-remotely-feature-gated]]) before treating anything below as an available retrieval path. Delete, never merely de-index, any memory that contradicts current policy. Treat `description:` as the retrieval surface and write it to be matched, not as decoration. Reserve index lines for facts that must be present unconditionally, and budget them against the byte cap. Do not infer from a missing index line that a file is unread, and do not rely on the on-demand path alone for a fact that must never be missed, because it can time out.
