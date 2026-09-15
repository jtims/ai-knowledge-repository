# Platform Constraints Ledger — `_tooling/`

**Version: 1.1 | 2026-08-06** · Governance controls that travel WITH the ledger.

This folder exists because `_SCHEMA-Constraints.md` makes a validator PASS a required step in the capture protocol. A contract that cites a tool living only in one operator's machine-local `~/.claude/hooks/` is not enforceable by anyone else, and the ledger is the SSOT for every machine that uses it. The control has to be co-located with the thing it governs.

## `validate-ledger.py` — the contract validator

**This file is the canonical copy.** `~/.claude/hooks/validate-ledger.py` is a **symlink** to it, so there is exactly one source of truth by construction and the two cannot drift. Writes through the symlink realpath-resolve into this repository and therefore trip the Change Control gate — intended, not incidental.

```bash
# from anywhere (default root is this ledger)
python3 ~/.claude/hooks/validate-ledger.py

# or explicitly, e.g. from another machine or surface
python3 "<ledger>/_tooling/validate-ledger.py" "<ledger>"
```

Invoke via `python3` rather than relying on the shebang, so the call does not depend on the executable bit.

**Exit 0 = PASS** (warnings allowed) · **exit 1 = FAIL** (any error).

### What it enforces

| Code | Level | Check |
|---|---|---|
| `E1` | ERROR | frontmatter missing, or not strict-YAML parseable |
| `E2` | ERROR | required key missing (`id`, `platform`, `domain`, `severity`, `status`, `provenance`, `verified`, `related`) |
| `E3` | ERROR | controlled-vocabulary violation — `domain`, `severity`, `status`, or a provenance `type` |
| `E4` | ERROR | `id` does not match the filename prefix |
| `E5` | ERROR | `provenance` absent/empty, or an entry missing `type`/`ref`/`date` |
| `E6` | ERROR | a required body section missing (`**Constraint:**` / `**Design consequence:**` / `**Sanctioned workarounds:**`) |
| `E7` | ERROR | node not listed in its platform MOC — the hub is the entry point, so an unlisted node is invisible |
| `W1` | WARN | `verified` is not an ISO date |
| `W2` | WARN | a `related` wikilink target does not resolve to a node in the ledger |
| `W3` | WARN | **diagnostic only** — after a real parse failure, names the line likely responsible |

### Why W3 is diagnostic rather than detective

An earlier draft scanned every frontmatter line for unquoted `': '` unconditionally and produced **18 false positives** against the live ledger, because valid YAML *flow mappings* — `- {type: official-doc, ref: "...", date: ...}` — read as violations under naive line-splitting. A warning class that cries wolf trains the reader to ignore it, which is worse than no warning at all. W3 now runs only when `E1` has already fired, purely to point at the offending line.

### Why this validator exists at all

On 2026-08-06 a newly authored node, `CLD-C006`, shipped with an unquoted `': '` inside a provenance `ref` — a YAML syntax error. Nothing caught it; the owner did, by eye. The ledger had no validator while three other surfaces did.

That failure mode is worse here than in ordinary content, because the decision-time injection hook (`platform-constraints-inject.sh`) **concatenates raw node text** into model context. A node that fails every parser still reaches the model verbatim, looking authoritative. Silent syntax breakage in an SSOT is therefore not cosmetic — it is a correctness problem for every design decision downstream.

## Governance flow

1. **Author or edit** any node, MOC, or schema file per `_SCHEMA-Constraints.md`.
2. **Automatic feedback:** the `PostToolUse` hook `~/.claude/hooks/ledger-validate-on-write.sh` fires on any write inside this ledger and reports the validator result immediately in-session. It cannot block — the write has already happened — so it is a tripwire, not a gate.
3. **Required before "done":** run the validator and require PASS. This is the capture protocol's final step (`_SCHEMA-Constraints.md`).
4. **Commit to git** directly. Not automatic on write: per-edit commits would make history unreadable.
5. **Never delete** a node — supersede it: flip `status` and add a `related` edge.

**MOC edits are validated too**, not just node writes: removing or renaming a MOC row orphans a node, which surfaces as `E7`.

**Changelog** — v1.1 (2026-08-06): a git mirror script was added (retired 2026-09-14). v1.0 (2026-08-06): initial. Canonical validator relocated here from `~/.claude/hooks/` (now a symlink) so the control travels with the ledger; `_tooling/` established; PostToolUse tripwire documented.
