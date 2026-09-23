# Platform Constraints Ledger — Schema & Operating Contract

**Version: 1.11 | 2026-09-23** · Owner-approved architecture (2026-08-06). This ledger is the **SSOT for hard platform constraints** — facts that invalidate a design if unknown. It is graph-ready by construction: atomic notes = nodes, typed frontmatter = properties, wikilinks = edges, MOCs = hubs.

## Admission bar (owner-ruled)

**Hard constraints only.** A fact is admitted when it would invalidate or force a design decision if unknown: access boundaries, credential/API non-exposure, irreversibilities, enforcement gaps, deployment-channel behavior, hard cost triggers, tier limits. Every entry requires **provenance** — an official doc reference and/or an owner confirmation with date. Preferences, how-tos, and soft conventions stay in skills/memory, NOT here.

## Entry format (one file = one constraint = one graph node)

- **Location:** `<Platform>/constraints/<ID>_<kebab-slug>.md`
- **Naming exception to the date convention (deliberate):** node filenames carry NO date — wikilink stability is the point; the `verified:` date lives in frontmatter. MOC and schema files are likewise undated for stable linking.
- **Frontmatter:** `id`, `platform`, `domain` (access | credentials | deployment | data | governance | cost), `severity` (design-invalidating | costly | friction), `status` (active | superseded | retired — **never delete**; supersession is a `related` edge + status flip), `provenance` (list of {type: official-doc | owner-confirmed | session-verified, ref, date}), `verified` (last re-verification date), `related` (wikilinks).
- **Body:** `**Constraint:**` one-sentence hard fact · `**Design consequence:**` what it invalidates/forces · `**Sanctioned workarounds:**` allowed patterns.

## Governance controls (co-located, v1.1)

`_tooling/` holds the controls that enforce this contract, deliberately **inside** the ledger rather than in one operator's machine-local config — a contract citing a tool nobody else can reach is not enforceable, and this ledger syncs to SharePoint as an org SSOT.

| Control | Location | Role |
|---|---|---|
| `validate-ledger.py` | `_tooling/` (**canonical**; `~/.claude/hooks/validate-ledger.py` is a symlink to it) | Lints every node against this schema: E1 parse · E2 required keys · E3 controlled vocabularies · E4 id/filename · E5 provenance shape · E6 body sections · E7 MOC listing · W1–W3 advisories |
| `sync-to-git.sh` | retired 2026-09-14 | This repository became the source of truth at the 2026-09-14 setup migration (the former synced knowledge-folder copy is gone), so the one-way synced folder → git mirror script was removed. Commit changes here directly. |
| `ledger-validate-on-write.sh` | `~/.claude/hooks/` (`PostToolUse`) | Tripwire — reports the validator result immediately after any write inside the ledger. Cannot block; the required PASS is the gate |
| `platform-constraints-inject.sh` | `~/.claude/hooks/` (`UserPromptSubmit`) | Decision-time injection of a platform's nodes on keyword match |

Invoke the validator via `python3`, not the shebang, so the call does not depend on the executable bit. Full detail: `_tooling/README.md`.

## ID registry (monotonic per platform, never renumbered)

| Prefix | Platform | Status |
|---|---|---|
| LOV | Lovable (incl. Lovable Cloud / managed Supabase) | ACTIVE (C001–C024) |
| N8N | n8n | ACTIVE (C001–C002) |
| CLD | Claude Code (harness; other Claude surfaces as their constraints arrive) | ACTIVE (C001-C033; C029 superseded) |
| PY | Python (CPython interpreter and stdlib) | ACTIVE (C001-C002) |
| GIT | Git (client behaviour, including host-filesystem-dependent behaviour and credential-routing configuration, how a Git host attributes the commits it receives, and which pushes it refuses because of their author address) | ACTIVE (C001-C004) |
| JIRA | Atlassian (Jira + Confluence + the claude.ai connector tool surface) | ACTIVE (C001) |
| RMK | reMarkable (paper tablets, reMarkable OS, the reMarkable cloud and its sync protocol, third-party cloud clients) | ACTIVE (C001-C004) |
| GPT / SFDC / HUB / STR / DDG | ChatGPT · Salesforce · HubSpot · Stripe · Datadog | RESERVED |

**Adding a platform:** create `<Platform>/{_<Platform>-Constraints-MOC.md, constraints/}` from templates, register the prefix here, add one keyword line to `~/.claude/hooks/platform-constraints-inject.sh`. No schema changes.

## Cross-platform ownership rule

A constraint lives with the platform **whose behavior causes it**; other platforms' MOCs link to it. Example: "n8n cannot write directly to a Lovable Cloud DB" is `LOV-C002` (Lovable causes it), linked from the n8n MOC.

## Capture protocol (same-turn, owner-ruled)

The moment a hard constraint is surfaced (owner correction, doc verification, live proof): propose the entry **in that turn** (Change Control gated, one-line approval) → write the atomic file from `_templates/constraint-entry-template.md` → append one line to the platform MOC + the global MOC → **run the contract validator and require PASS before reporting done** — `python3 ~/.claude/hooks/validate-ledger.py` (a symlink to the canonical `_tooling/validate-ledger.py`, which travels with this ledger). A `PostToolUse` tripwire (`~/.claude/hooks/ledger-validate-on-write.sh`) also reports the result automatically after any write inside the ledger; it cannot block, so the required PASS above remains the gate. Finally, **commit** the change in this repository, which has been the source of truth since the 2026-09-14 migration. Enforced by the standing rule in `~/.claude/context/change-control.md` (Platform Constraints Protocol) and the `platform-constraints` skill.

## Decision-time access

1. **Deterministic hook** (`UserPromptSubmit` → `platform-constraints-inject.sh`): keyword match on the user prompt → concatenates `<Platform>/constraints/*.md` into context. No rollup file exists to drift — injection reads the nodes directly.
2. **Skill** `platform-constraints`: auto-loads on platform/design triggers, covers model-introduced platforms the hook can't see, and carries the **citation rule** — any design/spec proposal touching a listed platform must name the constraint IDs consulted.

## Knowledge-graph evolution (owner-planned)

Near-term refinement adds typed edges (`supersedes`, `conflicts-with`, `depends-on`) and query views (Dataview / Smart Connections — `.smart-env` already indexes this vault). The atomic-node substrate is designed not to move.

**Changelog**
- v1.11 (2026-09-23): ID registry: the Claude Code range reads C001-C033 (C029 superseded). CLD-C033 (a published artifact page is a cross-origin frame that the browser pane's DOM tools cannot reach) is the third claude.ai artifact-runtime node, admitted under the same other-surfaces provision of the CLD row; provenance is session-verified: owner sessions 4 and 6 (2026-09-22) and a live probe 2026-09-23 in the Claude Code desktop app's built-in browser pane. No inject-hook keyword added, for the reason given at v1.10. No schema changes.
- v1.10 (2026-09-22): ID registry: the Claude Code range reads C001–C032 (C029 superseded). CLD-C031 (artifact page code has no outbound network) and CLD-C032 (the artifact's in-page Claude call selects a tier, not a model) are the first claude.ai artifact-runtime nodes, admitted under the existing other-surfaces provision of the CLD row rather than as a new platform; provenance is the runtime contract 0.2.52 type definitions (official-doc) read 2026-09-22 in an owner project. No inject-hook keyword added: a generic artifact keyword would inject the whole CLD set on most prompts. No schema changes.
- v1.9 (2026-09-18): ID registry: the Git range reads C001-C004, and the Git scope line gains push refusal by author address. GIT-C004 (GitHub refuses a push whose latest commit carries a private address of the pushing account, also into a private repository) is live proof from an owner project plus the official doc. No contract change.
- v1.8 (2026-09-18): ID registry: the Git range reads C001-C003, and the Git scope line gains host attribution. GIT-C003 (GitHub links a commit to the account that holds its author address) is official-doc plus two live reads from an owner project. It sits under `GIT` rather than a new GitHub prefix by owner ruling, following the v1.6 precedent of widening the Git scope line for GIT-C002. No contract change.
- v1.7 (2026-09-17): ID registry: the reMarkable range reads C001-C004. RMK-C004 (the document API answers 401 to a browser-paired device token even with Connect active) was declined at v1.6 for lack of admissible provenance and is admitted here on live proof from the same session, in a different form than the third-party source comment had implied. GIT-C002 re-verified: the `ssh://` workaround succeeded once `known_hosts` was populated from `gh api meta`. No contract change.
- v1.6 (2026-09-17): **reMarkable added as a platform (prefix `RMK`), seeded with RMK-C001 to RMK-C003; the Git range reads C001-C002.** Both arrive from one session in an owner project, which audited the `rr` push-to-tablet client before enabling it. RMK-C001 (official import is PDF and EPUB only) and RMK-C002 (developer mode factory-resets the device and breaks secure boot) are official-doc. RMK-C003 (a sync v3 write replaces the account-wide root index) is session-verified by source read, not by reproducing a loss, and the node says so. A fourth candidate, that the document API requires a Connect subscription, was DECLINED: its only evidence is a comment in third-party source, which is none of the three provenance types. GIT-C002 is live proof from the same session: a global `insteadOf` rule sent an SSH remote over HTTPS, where an OAuth token without `workflow` scope was refused. The Git scope line gains credential-routing configuration to cover it. No contract change.
- v1.5 (2026-09-15): ID registry: the Claude Code range reads C001–C030. CLD-C030 was added in the F33 remediation session and supersedes CLD-C029, the ledger's first use of `status: superseded`, done as this contract specifies: a status flip plus a `related` edge, with the superseded node kept in place and still listed in its MOC (E7). No contract change.
- v1.4 (2026-09-15): ID registry corrected: the Claude Code range reads C001–C029. CLD-C029 was added 2026-09-15 in an owner session, and this line was left at C028 (drift noted in the global MOC v1.24). No contract change.
- v1.3 (2026-08-28): **Atlassian activated (prefix `JIRA`, previously reserved), seeded with JIRA-C001** - the claude.ai Atlassian connector's Jira tools can silently answer with Confluence objects (`getVisibleJiraProjects` returns spaces; literal-email JQL falls back to a Confluence keyword search). Session-verified live 2026-08-28 (source-expansion swarm run wf_b335fa0d-ee8). The prefix covers Atlassian as a whole (Jira + Confluence + connector tool surface) until the owner splits it. Same silent-wrong-result family as PY-C001/PY-C002/GIT-C001.
- v1.2 (2026-08-26): **Two platforms added: Python (prefix `PY`) and Git (prefix `GIT`).** Both were seeded from defects found in one session while productionizing the Claude analytics monthly process, and both are of a shape the ledger did not yet cover: the tool reports success while producing a wrong result. `PY-C001` (pre-3.12 AST nodes inside an f-string carry expression-relative positions, and `col_offset` is a byte offset) silently corrupted a source file mid-rewrite. `PY-C002` (`set` iteration is hash-randomised while `sorted()` is stable, so ties order arbitrarily) removed regenerate-and-diff as a verification technique without any error. `GIT-C001` (macOS sets `core.ignorecase=true`, so `.gitignore` matching is case-insensitive) let an unanchored data-exclusion glob silently drop an intended source file, and a commit shipped 11 of 12 files looking successful. Recorded as separate platforms rather than one toolchain folder because the schema's ownership rule is per-platform-behaviour and the injection hook routes on per-platform keywords; a Bash candidate from the same session was **declined** as well-documented and low-consequence, to hold the admission bar.
- v1.1 (2026-08-06): **Git mirror added** — the former private mirror repository (private), scoped to the whole `AI Knowledge Repository/` parent so the planned consolidation needs no later rename. One-way synced folder → git via `_tooling/sync-to-git.sh`; the synced folder remains SSOT. Rationale: the former synced copy gave this ledger offsite replication but no commit history, while the vault has the inverse gap (local git, no remote) — neither surface had both. **Contract validator added** — `~/.claude/hooks/validate-ledger.py` lints every node against this schema (required keys, controlled vocabularies, id/filename agreement, provenance shape, required body sections, MOC listing, wikilink resolution) and is now a required step in the capture protocol. Written because a newly authored node (`CLD-C006`) shipped with an unquoted `': '` in a provenance `ref` — a YAML syntax error — and nothing checked it; a node that fails to parse still reaches the model verbatim through the injection hook, looking authoritative. Claude Code added as a platform (prefix `CLD`, 8 nodes seeded) — the harness itself is a constraint surface: definition-loading, the seven agent-spawn vectors, permission/hook behaviour, model-resolution precedence. `CLD-C001` is the ledger's first **session-verified** (live-proof) admission rather than doc-sourced.
- v1.0 (2026-08-06): initial. Seeded Lovable (13) + n8n (2).
