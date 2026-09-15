# Python - Hard Constraints MOC

**Platform hub** · prefix `PY` · 2 active · schema: [[_SCHEMA-Constraints]] · Grows via the same-turn capture protocol.

Scope: CPython interpreter and stdlib behaviour that invalidates a design if unknown. Both current entries share a shape worth naming: the tool reports success while producing a wrong result, so neither is caught by "it ran without error".

| ID | Constraint | Domain | Severity | Verified |
|---|---|---|---|---|
| [[PY-C001_fstring-ast-offsets-are-expression-relative\|PY-C001]] | Below 3.12, AST nodes inside an f-string carry expression-relative positions, and col_offset is a byte offset | governance | design-invalidating | 2026-08-26 |
| [[PY-C002_set-plus-stable-sort-is-nondeterministic\|PY-C002]] | set iteration is hash-randomised and sorted() is stable, so tied keys order arbitrarily per run | governance | design-invalidating | 2026-08-26 |

**Outbound cross-platform edges:** exclusion patterns and repository hygiene for generated Python artifacts, see [[GIT-C001_macos-ignorecase-makes-gitignore-case-insensitive|GIT-C001]].
