# AI Knowledge Repository

Platform knowledge ledgers: hard **constraints** (design-invalidating platform facts, injected at decision time) and decision-enabling **capabilities** (pull-only), for Claude Code, Lovable, n8n, Atlassian, Git and Python.

> **Source of truth since 2026-09-14.** This repository began as a one-way mirror of a synced knowledge-folder copy. At the setup migration that copy went away, so this local repository is now authoritative and the mirror script (`sync-to-git.sh`) was retired. Commit changes here directly. Org-specific names and identifiers were generalized at the same time (ruling N1); the unscrubbed original is kept in the migration archive.

## Layout

- `Platform Constraints Ledger/`: `_SCHEMA-Constraints.md` (contract and ID registry), `_MOC-Platform-Constraints.md` (global hub), `<Platform>/_<Platform>-Constraints-MOC.md`, atomic nodes in `<Platform>/constraints/<ID>_<slug>.md`
- `Platform Capabilities Ledger/`: the same shape with `-CAP` IDs and `_SCHEMA-Capabilities.md`
- `Platform Constraints Ledger/_tooling/validate-ledger.py`: the contract validator for BOTH ledgers; `~/.claude/hooks/validate-ledger.py` is a symlink to it

## How it is used

- `~/.claude/hooks/platform-constraints-inject.sh` injects a platform's constraint nodes when a prompt names that platform.
- `~/.claude/hooks/ledger-validate-on-write.sh` reports the validator result after any write inside either ledger.
- The `platform-constraints` skill and the Platform Constraints / Capabilities protocols in `~/.claude/context/change-control.md` govern consult-before-design, cite-the-IDs and same-turn capture.

## Validate

```bash
python3 "Platform Constraints Ledger/_tooling/validate-ledger.py"
```

Require PASS before reporting any ledger change done.
