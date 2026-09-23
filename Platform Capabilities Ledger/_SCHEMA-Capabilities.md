# Platform Capabilities Ledger — Schema & Operating Contract

**Version: 1.5 | 2026-09-23** · Owner-approved architecture (2026-08-10). Deliberate counterpart to the Platform Constraints Ledger ([[_SCHEMA-Constraints]]). This ledger is the **SSOT for decision-enabling platform capabilities** — non-obvious affordances that, if unknown, would cause you to wrongly rule a *possible* design OUT. Graph-ready by construction: atomic notes = nodes, typed frontmatter = properties, wikilinks = edges, MOCs = hubs. Same discipline as the Constraints Ledger, inverse polarity.

## Admission bar (owner-ruled — the inverse razor)

**Decision-enabling capabilities only.** A constraint is admitted when *not* knowing it would make you build something impossible (a false-positive design); a capability is admitted when *not* knowing it would make you fail to build something that was actually possible (a false-negative design). A fact qualifies only if it is **non-obvious** AND **changes a design decision**: an unlock, a sanctioned integration path, a tier/plan affordance that gates a pattern, a documented capacity a design can rely on.

Every entry requires **provenance** — an official-doc reference and/or an owner confirmation with date. Capabilities drift as vendors ship; an unverified capability is a design that breaks at build.

**Out of scope (kept out on purpose):** exhaustive feature lists, how-tos, tutorials, soft conventions — those live in vendor docs, skills, and the archived org tech-stack skill (the "what exists / what plan are we on" SSOT). This ledger answers **"what can I safely rely on that I might not realize is possible."** If a fact wouldn't change a design decision, it does not belong here.

## Entry format (one file = one capability = one graph node)

- **Location:** `<Platform>/capabilities/<ID>_<kebab-slug>.md`
- **ID infix `-CAP`** (e.g. `LOV-CAP001`) — deliberately distinct from the Constraints Ledger's `-C`, so `LOV-CAP001` and `LOV-C001` never collide in prose, wikilinks, or the git commit-message ID scan. Monotonic per platform, never renumbered.
- **Naming exception to the date convention (deliberate):** node filenames carry NO date — wikilink stability is the point; the `verified:` date lives in frontmatter. MOC files are likewise undated.
- **Both ledgers' schema files carry a distinct suffix** — `_SCHEMA-Constraints.md` and `_SCHEMA-Capabilities.md` — so neither collides under Obsidian's vault-wide basename resolution (a single shared `_SCHEMA.md` basename would silently ambiguate bare `[[_SCHEMA]]` links across the vault). The Constraints Ledger's schema was renamed from `_SCHEMA.md` → `_SCHEMA-Constraints.md` for this symmetry (Option R, owner-ruled 2026-08-10), and all its `[[_SCHEMA]]` wikilinks + live pointers were repointed in the same change. Every other twin file (`_MOC-Platform-Capabilities.md`, `capability-entry-template.md`, `_<Platform>-Capabilities-MOC.md`) already differs by basename.
- **Frontmatter:** `id`, `platform`, `domain` (access | credentials | deployment | data | governance | cost), `leverage` (unlocks | accelerates | convenience), `status` (active | superseded | retired — **never delete**; supersession is a `related` edge + status flip), `provenance` (list of {type: official-doc | owner-confirmed | session-verified, ref, date}), `verified` (last re-verification date), `related` (wikilinks — **including the constraint node(s) that bound this capability**).
- **Body:** `**Capability:**` one-sentence enabling fact · `**What it unlocks:**` the design(s) it makes possible or materially cheaper · `**Caveats & linked constraints:**` the boundaries + the `[[<ID>-C0nn]]` constraint node(s) governing its safe use ("none" is valid).

## Leverage vocabulary (the capability analogue of `severity`)

| `leverage` | Means | Admit when |
|---|---|---|
| `unlocks` | Makes possible a design a reasonable engineer would assume impossible | Highest signal — the core of the inverse razor |
| `accelerates` | A materially cheaper/faster sanctioned path than the obvious one | The saving changes the build decision |
| `convenience` | Genuinely useful but not decision-changing | Sparingly — most convenience facts belong in docs, not here |

## Access — PULL, not push (owner-ruled)

Unlike the Constraints Ledger, capabilities are **not injected** at prompt time. A constraint must not be *forgotten* (forgetting one ships a broken design), which earns reflexive `UserPromptSubmit` injection; a capability is *reached for* while designing, and auto-injecting a growing catalogue on every platform mention would inflate every prompt for little gain. Entry points:
1. The global hub [[_MOC-Platform-Capabilities]] and each `<Platform>/_<Platform>-Capabilities-MOC.md`.
2. The `platform-constraints` skill carries a one-line cross-pointer to this ledger (pull-only; no new hook).

**No keyword line is added to `platform-constraints-inject.sh`** — that is by design, not omission.

## Governance controls (shared with the Constraints Ledger)

The two ledgers share one contract validator and one git mirror; a capability node is held to the same lint (required keys, controlled vocab, id/filename agreement, provenance shape, required body sections, MOC listing, wikilink resolution) as a constraint node.

**Tooling status (Phase 2 — PENDING as of v1.0):** the canonical `validate-ledger.py` (in the Constraints Ledger's `_tooling/`) is being generalized to lint both ledger kinds; `sync-to-git.sh` is being extended to validate *every* ledger under the `AI Knowledge Repository/` parent before mirroring; the `PostToolUse` tripwire is being broadened to fire on writes in either ledger. **Until that lands, capability nodes are validated manually against this schema before "done."** The validator-location choice (in-place vs. promoted to a shared parent `_tooling/`) is **open — logged in `_AIKR-Worklog-Roadmap.md` §3 as a revisit item.**

## ID registry (monotonic per platform, never renumbered)

| Prefix | Platform | Status |
|---|---|---|
| LOV-CAP | Lovable (incl. Lovable Cloud / managed Supabase) | ACTIVE (seeding) |
| N8N-CAP | n8n | ACTIVE (seeding) |
| CLD-CAP | Claude Code | ACTIVE (CAP001-CAP009) |
| RMK-CAP | reMarkable | ACTIVE (CAP001-CAP003) |
| GPT / JIRA / SFDC / HUB / STR / DDG (·-CAP) | ChatGPT · Atlassian · Salesforce · HubSpot · Stripe · Datadog | RESERVED |

**Adding a platform:** create `<Platform>/{_<Platform>-Capabilities-MOC.md, capabilities/}`, register the prefix here. No inject-hook line (pull-only). No schema changes.

## Cross-ledger rule (capabilities ↔ constraints)

A capability node **links to the constraint node(s) that bound it** via `related`, and a constraint's `Sanctioned workarounds:` is often the capability's `What it unlocks`. The two ledgers are one graph: a capability and its governing constraint are adjacent nodes. Example: `LOV-CAP001` (edge functions can make arbitrary outbound HTTPS calls) `related: [[LOV-C002_no-service-keys-no-external-db-access]]` — the capability is the sanctioned way around the constraint.

## Capture protocol (Change Control gated, provenance required)

When a decision-enabling capability is verified (official doc, owner confirmation, or live session proof): propose the entry in that turn (one-line approval) → write the atomic file from `_templates/capability-entry-template.md` → append one line to the platform MOC + the global MOC → validate (manually until Phase-2 tooling lands, then via the shared validator) and require PASS before "done" → mirror to git (`sync-to-git.sh`, once extended). Supersede, never delete. Capture cadence is less reflexive than constraints (a capability is rarely discovered by getting burned) but the bar and the discipline are identical.

## Knowledge-graph evolution (owner-planned)

Typed edges (`supersedes`, `conflicts-with`, `depends-on`, and cross-ledger `enables` / `bounded-by`) + query views (Dataview / Smart Connections). The atomic-node substrate is designed not to move.

**Changelog**
- v1.5 (2026-09-23): ID registry: the Claude Code range reads CAP001-CAP009. CLD-CAP009 (Claude Code's built-in browser pane, when signed in to claude.ai, can drive an artifact's in-page Claude call on the owner's account by coordinates and screenshots) is session-verified from two proof runs in an owner project on 2026-09-22 and a live probe on 2026-09-23 that made no call, linked to CLD-C033, CLD-C032, CLD-C031 and CLD-CAP008. No schema changes.
- v1.4 (2026-09-22): ID registry: the Claude Code range reads CAP001-CAP008. CLD-CAP008 (a published artifact page can ask Claude on the viewer's plan through the sample capability) is official-doc from the runtime contract 0.2.52 type definitions read 2026-09-22 in an owner project, linked to CLD-C031 and CLD-C032; not yet exercised live. No schema changes.
- v1.3 (2026-09-18): ID registry: the reMarkable range reads CAP001-CAP003. RMK-CAP003 (a folder can be created through sync v3 in the vendor's own shape, without the document API) is session-verified from an owner project. No contract change.
- v1.2 (2026-09-18): ID registry: the reMarkable range reads CAP001-CAP002. RMK-CAP002 (stored shapes are readable from any root with downloads only) is session-verified from an owner project. No contract change.
- v1.1 (2026-09-17): ID registry: reMarkable added (prefix `RMK-CAP`), seeded with RMK-CAP001, mirroring the `RMK` platform added to the Constraints Ledger the same day. No contract change.
- v1.0 (2026-08-10): initial. Sibling ledger established under `AI Knowledge Repository/`. Inverse-razor admission bar; `-CAP` ID infix; `leverage` axis; pull-only access (no inject hook); shared validator/mirror with the Constraints Ledger (generalization tracked as Phase 2). Both ledger schemas suffixed (`_SCHEMA-Constraints.md` / `_SCHEMA-Capabilities.md`) for vault-wide basename symmetry (Option R — the Constraints schema was renamed from `_SCHEMA.md` and its links/pointers repointed the same day). Ratified 2026-08-10 via 4-question structured adjudication (structure=sibling · admission=decision-enabling · access=pull-only · tooling=generalize-existing).
