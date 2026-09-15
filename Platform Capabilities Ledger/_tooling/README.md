# Platform Capabilities Ledger — `_tooling/`

**Version: 1.0 | 2026-08-10** · Governance controls for this ledger. By ruling (tooling = generalize-existing), the Capabilities Ledger **shares** the Constraints Ledger's controls rather than forking them — one validator, one git mirror, no drift.

## Shared controls (canonical live in the Constraints Ledger's `_tooling/`)

| Control | Canonical location | Role for this ledger |
|---|---|---|
| `validate-ledger.py` | `../../Platform Constraints Ledger/_tooling/validate-ledger.py` (`~/.claude/hooks/validate-ledger.py` symlinks it) | Lints capability nodes against [[_SCHEMA-Capabilities]] — **PENDING Phase 2 generalization** (today it is constraints-only: globs `*/constraints/*.md` and `_*-Constraints-MOC.md`). Until then, capability nodes are validated **manually** against the schema before "done." |
| `sync-to-git.sh` | retired 2026-09-14 | The mirror script was removed at the 2026-09-14 setup migration; this repository is now the source of truth. |
| `ledger-validate-on-write.sh` | `~/.claude/hooks/` (PostToolUse tripwire) | **PENDING Phase 2:** broaden to fire on writes in either ledger (today it matches only the Constraints Ledger path). |
| `platform-constraints-inject.sh` | `~/.claude/hooks/` (UserPromptSubmit) | **N/A by ruling** — capabilities are pull-only; no keyword line is added. |

## Why shared, not forked

The Constraints Ledger's ethos is single-source-by-construction (the validator is canonical in one place, symlinked elsewhere). Forking a second validator for capabilities would reintroduce exactly the drift that design avoids. The **validator-location** decision — keep the canonical in the Constraints `_tooling/` (current) vs. promote it to a shared `AI Knowledge Repository/_tooling/` now that it governs two ledgers — is logged as a revisit item in `_AIKR-Worklog-Roadmap.md` §3.

## Governance flow (once Phase 2 lands — identical to the Constraints Ledger)

1. **Author or edit** any node / MOC / schema file per [[_SCHEMA-Capabilities]].
2. **Automatic feedback:** the broadened `PostToolUse` tripwire reports the validator result after any write inside this ledger. It cannot block — the write already happened.
3. **Required before "done":** run the (generalized) validator and require PASS.
4. **Mirror to git:** `bash "../../Platform Constraints Ledger/_tooling/sync-to-git.sh"` — the change gains commit history + an offsite copy.
5. **Never delete** a node — supersede it (`status` flip + `related` edge).

**Interim (pre-Phase-2):** steps 2–3 do not yet cover capability nodes, so validate **manually** against the schema and require a clean read before "done."

**Changelog** — v1.0 (2026-08-10): initial. Declares the shared-control model; flags the Phase-2 generalization pending items and the §3 validator-location revisit.
