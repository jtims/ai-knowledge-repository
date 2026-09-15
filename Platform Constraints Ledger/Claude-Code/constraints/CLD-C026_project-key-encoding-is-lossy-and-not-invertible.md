---
id: CLD-C026
platform: Claude Code
domain: data
severity: design-invalidating
status: active
provenance:
  - type: session-verified
    ref: "live 2026-09-02 (owner session 5, CLI 2.1.235) - re.sub(r'[/_ .]','-',path) reproduced the directory name under ~/.claude/projects/ for 4 live keys: /Users/owner, /Users/owner/vault/projects, /Users/owner/Projects/reasoning-bundle, and /Users/owner/Personal/Alpha/Sites/app_v2. Negative control -Users-owner-NoSuchDir-xyzzy-42 must not resolve and did not"
    date: 2026-09-02
  - type: session-verified
    ref: "live 2026-09-02 - the false finding this node exists to prevent: an audit register row asserted an orphaned store whose keyed path no longer existed, derived by substituting / for every -. The real directory .../Sites/app_v2 exists, is its own git repo, and its store is live. B4 REFUTED, work-order item R10 WITHDRAWN"
    date: 2026-09-02
verified: 2026-09-02
related: ["[[CLD-C016_auto-memory-keys-one-store-per-repo-root]]", "[[CLD-C024_unindexed-memory-files-are-still-recallable]]"]
---

**Constraint:** The project key that names a directory under `~/.claude/projects/` is produced by mapping **each of `/`, `_`, space and `.` to a single `-`**, with a literal `-` in the path passed through unchanged. The encoding is therefore **lossy**, and its inverse is **ambiguous**: a `-` in a key carries no information about which character produced it, so a path cannot be recovered from a key by string substitution.

**Design consequence:** Any code, audit or diagnostic that recovers a filesystem path from a project key by replacing `-` with `/` is guessing, and it fails in exactly the cases that matter: a directory whose own name contains `_`, `.`, a space or a `-`. The failure is silent and inverted, because a wrong decode names a path that does not exist and so **reads as evidence of an orphaned or unreachable store**. This is not hypothetical. `app_v2` encodes to `app-v2`; the naive decode produced `.../Sites/app/v2`, which has never existed, while the real directory sat one substitution away, was its own git repository, and held a live and fully addressable auto-memory store. That decode became a recorded defect row and an entire remediation item proposing disposal of live content, both of which had to be withdrawn. Note also that the key does not identify its own scope: an auto-memory store keys to the **git repository root** per `CLD-C016` while a transcript directory keys to the **working directory**, so two directories can exist for one session and the key alone does not say which is which.

**Sanctioned workarounds:** Never invert the encoding by substitution. Resolve a key by **walking the filesystem**: split on `-`, then for each token try each joiner (`/`, space, `_`, `.`, `-`) in turn, keeping any candidate that exists or is a prefix of an existing entry, and require the final candidate to be a directory. Prune on prefix rather than on existence alone, or multi-word directory names are dropped (`.../vault` is not a path even though `.../vault projects` is). Perform the prefix test with a literal comparison rather than a glob, or a directory whose name contains glob metacharacters resolves to nothing and is reported as an orphan, reproducing the very error this node describes. Report any truncation of the candidate set rather than capping silently. Before acting on any "orphaned store" verdict, confirm by hand that no directory resolves. Reference implementation: `~/.claude/scripts/align-audit.sh` v1.3 check 12 (`resolve_project_key`).
