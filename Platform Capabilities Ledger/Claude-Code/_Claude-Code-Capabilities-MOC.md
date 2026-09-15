# Claude Code — Capabilities MOC

**Platform hub** · prefix `CLD-CAP` · 6 active · schema: [[_SCHEMA-Capabilities]] · Grows via the Change-Control-gated capture protocol.

| ID | Capability | Domain | Leverage | Verified |
|---|---|---|---|---|
| [[CLD-CAP001_hooks-deterministic-governance\|CLD-CAP001]] | Hooks (`UserPromptSubmit`/`PostToolUse`) deterministically inject + validate; a synced folder-canonical tool symlinks into `~/.claude/hooks` | governance | unlocks | 2026-08-10 |
| [[CLD-CAP002_cross-scope-hooks-merge\|CLD-CAP002]] | `SessionStart`/etc. hooks MERGE across settings scopes (user+project+local all run); per-project hooks don't suppress global governance hooks | governance | unlocks | 2026-08-18 |
| [[CLD-CAP003_automemorydirectory-redirects-store-from-subdir\|CLD-CAP003]] | `autoMemoryDirectory` in a subdir's `.claude/settings.json` redirects its auto-memory store — per-project memory inside a shared vault, no git-init | data | unlocks | 2026-08-21 |
| [[CLD-CAP004_subagent-frontmatter-pretooluse-hook-fires\|CLD-CAP004]] | A `PreToolUse` hook in a SUBAGENT'S OWN frontmatter DOES fire for that subagent and can block it (exit 2) — a real mechanical bound where settings-scope hooks give none (CLD-C018). Headless leg VERIFIED; **interactive leg UNVERIFIED** | governance | unlocks | 2026-08-23 |
| [[CLD-CAP005_org-skill-files-on-disk-and-readable\|CLD-CAP005]] | An org-managed claude.ai skill is on DISK at `/mnt/skills/organization/<name>/` and its bundled `references/` files ARE model-readable — multi-file progressive-disclosure skills work on claude.ai, not just Claude Code. Caveat: reachable is NOT auto-loaded; a skill search returns metadata only | access | unlocks | 2026-08-24 |
| [[CLD-CAP006_project-scope-settings-consulted-in-headless-and-sdk-runs\|CLD-CAP006]] | A project-scope `autoMemoryDirectory` redirect IS consulted in NON-INTERACTIVE runs (headless, `-p`, SDK) unconditionally, because `Aje() = !isInteractive() || trustAccepted`; and `userSettings` sits LAST in the chain, so a user-scope pin can never outrank a project redirect. Precedence half VERIFIED; the `--setting-sources` loading half stays UNKNOWN | data | unlocks | 2026-09-03 |

**Cross-ledger:** capability nodes here link back to their governing [[_Claude-Code-Constraints-MOC|Claude Code constraints]] via `related`.
