---
id: CLD-CAP003
platform: Claude Code
domain: data
leverage: unlocks
status: active
provenance:
  - type: official-doc
    ref: "code.claude.com/docs/en/memory — autoMemoryDirectory setting; auto memory keyed from the git repository"
    date: 2026-08-21
  - type: session-verified
    ref: "live 2026-08-21 — nested claude -p launched from a home-repo SUBDIR carrying a .claude/settings.json autoMemoryDirectory redirect loaded a unique marker from the redirected store, NOT the home store"
    date: 2026-08-21
verified: 2026-08-21
related: ["[[CLD-C016_auto-memory-keys-one-store-per-repo-root]]"]
---

**Capability:** Setting `autoMemoryDirectory` in a directory's `.claude/settings.json` redirects that scope's auto-memory store to an arbitrary path — and the redirect fires even when the directory is a SUBDIR of a git repo, so a project nested inside a larger repo or vault can carry its own isolated memory store WITHOUT being its own git repo.

**What it unlocks:** Per-project memory isolation without git-init or repo-conversion — the mechanism basis for a tiered project≫vault≫global memory architecture. Auto-memory otherwise keys ONE store per git-repo-root (all subdirs of one repo share it); without this redirect you would wrongly rule OUT per-project stores inside a shared vault and accept a single always-loaded index that bloats across unrelated projects (the observed 23.6KB→cap failure).

**Caveats & linked constraints:** Auto-memory is still one store per scope — it does NOT cascade multiple MEMORY.md tiers. The redirect resolves from the LAUNCH cwd: mounting a project from a home session (`/project-mount` / `--add-dir`) does NOT auto-load the redirected store — it is native only when Claude Code is launched from within the project dir (otherwise the tier must be loaded explicitly, e.g. via a RESUME brief). MEMORY.md loads only the first 200 lines / 25KB. Governing constraint — [[CLD-C016_auto-memory-keys-one-store-per-repo-root]] (auto-memory keys one store per git-repo-root; the root cause of cross-project index bloat) — captured 2026-08-21.
