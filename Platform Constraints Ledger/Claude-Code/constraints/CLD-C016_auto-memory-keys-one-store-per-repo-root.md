---
id: CLD-C016
platform: Claude Code
domain: data
severity: design-invalidating
status: active
provenance:
  - type: official-doc
    ref: "code.claude.com/docs/en/memory — auto memory is keyed from the git repository (one store per repo root); autoMemoryDirectory overrides the store location"
    date: 2026-08-21
  - type: session-verified
    ref: "live 2026-08-21 — git rev-parse from every vault/project path under ~ resolved to the HOME repo root; store enumeration showed one shared home store (+1 orphan); the shared always-loaded MEMORY.md had accreted 23.6KB across unrelated projects, ~94% of the 25KB load cap"
    date: 2026-08-21
verified: 2026-08-21
related: ["[[CLD-CAP003_automemorydirectory-redirects-store-from-subdir]]"]
---

**Constraint:** Claude Code auto-memory keys exactly ONE store per git-repo-root — every session launched anywhere inside a repo (subdirectories, nested vaults, unrelated projects sharing the tree) reads and writes the SAME always-loaded `MEMORY.md` index and memory store (load cap: first 200 lines / 25KB).

**Design consequence:** When the home directory itself is a git repo, ALL in-home projects and vaults silently share one global memory store — per-project memory isolation does not exist by default, the single index accretes across unrelated projects toward the load cap (observed live: 23.6KB ≈ 94% of cap), and stale cross-project content taxes every session. Any memory architecture that assumes per-project stores inside one repo is invalid without an explicit override. This is the root cause of the 2026-08-21 MEMORY.md bloat remediation.

**Sanctioned workarounds:** (1) `autoMemoryDirectory` in the project subdir's `.claude/settings.json` redirects that scope's store — [[CLD-CAP003_automemorydirectory-redirects-store-from-subdir]] is the capability leg (note its launch-cwd caveat: mount-from-home does NOT auto-load the redirected store; the RESUME brief carries the tier). (2) Keep the shared global index lean by contract: cross-cutting entries plus a thin active-project registry pointing at per-project SSOTs (two-tier model, adopted 2026-08-21). (3) Convert a vault/project into its own git repo — it gets its own store, at the cost of repo management and home-repo exclusion upkeep.
