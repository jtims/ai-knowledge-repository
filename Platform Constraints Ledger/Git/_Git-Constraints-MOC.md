# Git - Hard Constraints MOC

**Platform hub** · prefix `GIT` · 2 active · schema: [[_SCHEMA-Constraints]] · Grows via the same-turn capture protocol.

Scope: git client behaviour, including host-filesystem-dependent behaviour and client configuration that changes which credential a hosted remote receives, that invalidates or forces a design if unknown. Relevant to every project in this estate, and specifically to any scheme that relies on `.gitignore` to keep named-individual data out of a shared repository.

| ID | Constraint | Domain | Severity | Verified |
|---|---|---|---|---|
| [[GIT-C001_macos-ignorecase-makes-gitignore-case-insensitive\|GIT-C001]] | On macOS core.ignorecase is true, so .gitignore matching is case-insensitive and a data glob can silently exclude source | governance | design-invalidating | 2026-08-26 |
| [[GIT-C002_https-rewrite-plus-missing-workflow-scope-blocks-workflow-pushes\|GIT-C002]] | A global insteadOf rule silently sends SSH remotes over HTTPS, and an OAuth token without workflow scope cannot push .github/workflows files | credentials | costly | 2026-09-17 |

**Outbound cross-platform edges:** reproducibility of the generated artifacts these patterns exclude, see [[PY-C002_set-plus-stable-sort-is-nondeterministic|PY-C002]].
