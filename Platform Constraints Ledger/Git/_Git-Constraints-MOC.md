# Git - Hard Constraints MOC

**Platform hub** · prefix `GIT` · 1 active · schema: [[_SCHEMA-Constraints]] · Grows via the same-turn capture protocol.

Scope: git client behaviour, including host-filesystem-dependent behaviour, that invalidates a design if unknown. Relevant to every project in this estate, and specifically to any scheme that relies on `.gitignore` to keep named-individual data out of a shared repository.

| ID | Constraint | Domain | Severity | Verified |
|---|---|---|---|---|
| [[GIT-C001_macos-ignorecase-makes-gitignore-case-insensitive\|GIT-C001]] | On macOS core.ignorecase is true, so .gitignore matching is case-insensitive and a data glob can silently exclude source | governance | design-invalidating | 2026-08-26 |

**Outbound cross-platform edges:** reproducibility of the generated artifacts these patterns exclude, see [[PY-C002_set-plus-stable-sort-is-nondeterministic|PY-C002]].
