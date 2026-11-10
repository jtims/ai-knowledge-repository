# Platform Capabilities Ledger — `_tooling/`

**Version: 1.1 | 2026-11-10** · Governance controls for this ledger. By ruling (tooling = generalize-existing), the Capabilities Ledger **shares** the Constraints Ledger's controls rather than forking them — one validator, no drift.

## Shared controls (canonical live in the Constraints Ledger's `_tooling/`)

| Control | Canonical location | Role for this ledger |
|---|---|---|
| `validate-ledger.py` | `../../Platform Constraints Ledger/_tooling/validate-ledger.py` | Lints capability nodes against [[_SCHEMA-Capabilities]]. Since v2.0 one validator covers both ledgers and auto-detects the capabilities profile (nodes in `*/capabilities/*.md`, MOC `_*-Capabilities-MOC.md`). From the repository root: `python3 "Platform Constraints Ledger/_tooling/validate-ledger.py" .` |
| `sync-to-git.sh` | retired 2026-09-14 | The mirror script was removed at the 2026-09-14 setup migration; this repository is now the source of truth. |
| `ledger-validate-on-write.sh` | the owner's `~/.claude/hooks/` (PostToolUse tripwire; not shipped here) | Reports the validator result after a write to a ledger file. It cannot block: the write already happened. |
| `platform-constraints-inject.sh` | the owner's `~/.claude/hooks/` (UserPromptSubmit; not shipped here) | **N/A by ruling** — capabilities are pull-only; no keyword line is added. |

## Why shared, not forked

The Constraints Ledger's ethos is single-source-by-construction (the validator is canonical in one place). Forking a second validator for capabilities would reintroduce exactly the drift that design avoids. Whether to keep the canonical copy in the Constraints `_tooling/` or promote it to a shared parent `_tooling/` now that it governs two ledgers is an open design question in the owner's working notes.

## Governance flow (identical to the Constraints Ledger)

1. **Author or edit** any node / MOC / schema file per [[_SCHEMA-Capabilities]].
2. **Validate:** run the validator and require PASS before "done."
3. **Commit to git** directly in this repository.
4. **Never delete** a node — supersede it (`status` flip + `related` edge).

**Changelog** — v1.1 (2026-11-10): the validator row describes the shipped v2.0 behaviour (both ledgers); the Phase 2 pending notes, the retired git-mirror step and a pointer to an unpublished working note are removed; the hook rows say they are not shipped. v1.0 (2026-08-10): initial.
