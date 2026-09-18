# Git - Hard Constraints MOC

**Platform hub** · prefix `GIT` · 4 active · schema: [[_SCHEMA-Constraints]] · Grows via the same-turn capture protocol.

Scope: git client behaviour, including host-filesystem-dependent behaviour client configuration that changes which credential a hosted remote receives, how a Git host attributes the commits it receives, and which pushes it refuses because of their author address, that invalidates or forces a design if unknown. Relevant to every project in this estate, and specifically to any scheme that relies on `.gitignore` to keep named-individual data out of a shared repository.

| ID | Constraint | Domain | Severity | Verified |
|---|---|---|---|---|
| [[GIT-C001_macos-ignorecase-makes-gitignore-case-insensitive\|GIT-C001]] | On macOS core.ignorecase is true, so .gitignore matching is case-insensitive and a data glob can silently exclude source | governance | design-invalidating | 2026-08-26 |
| [[GIT-C002_https-rewrite-plus-missing-workflow-scope-blocks-workflow-pushes\|GIT-C002]] | A global insteadOf rule silently sends SSH remotes over HTTPS, and an OAuth token without workflow scope cannot push .github/workflows files | credentials | costly | 2026-09-17 |
| [[GIT-C003_github-links-commits-to-the-account-holding-the-author-email\|GIT-C003]] | GitHub links a commit to the account that holds its author email address, not to the pusher or the repository owner, so a repository can go public under another account's name | governance | costly | 2026-09-18 |
| [[GIT-C004_github-refuses-pushes-authored-under-a-private-email\|GIT-C004]] | With email push protection on, GitHub refuses a push whose latest commit carries a private address of the pushing account, even into a private repository | access | costly | 2026-09-18 |

**Outbound cross-platform edges:** reproducibility of the generated artifacts these patterns exclude, see [[PY-C002_set-plus-stable-sort-is-nondeterministic|PY-C002]].
