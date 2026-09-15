---
id: CLD-CAP002
platform: Claude Code
domain: governance
leverage: unlocks
status: active
provenance:
  - type: official-doc
    ref: "code.claude.com/docs/en/hooks-guide.md (l.512 'every hook's command runs to completion before Claude Code merges the results'; l.589 SessionStart/UserPromptSubmit plain stdout → context) + settings.md (precedence Managed>CLI>Local>Project>User; project/local settings resolve to git-repo root, load by cwd)"
    date: 2026-08-18
  - type: session-verified
    ref: "A2 probe (scratchpad/a2-probe.sh): throwaway git repo with a project-scope AND a local-scope SessionStart hook; headless `claude -p` fired BOTH sentinels simultaneously — cross-scope merge, no override, no hook-trust block"
    date: 2026-08-18
verified: 2026-08-18
related: ["[[CLD-CAP001_hooks-deterministic-governance]]", "[[CLD-C009_plugin-subagents-ignore-permission-hooks-mcp]]"]
---

**Capability:** When a Claude Code lifecycle event (e.g. `SessionStart`) has hooks defined in more than one settings scope — user (`~/.claude/settings.json`), project (`.claude/settings.json`), local (`.claude/settings.local.json`) — **every scope's hooks run (they merge, in parallel); the higher-precedence scope does NOT replace the lower one**; and for `SessionStart`/`UserPromptSubmit` a hook's plain stdout is injected into the model's context (structured JSON not required).

**What it unlocks:** Per-project / per-clone `SessionStart` hooks that coexist with global governance hooks — a project- or local-scoped hook can be added WITHOUT silently suppressing the user-global `opus-driver-protocol.sh` (or any other global SessionStart hook). This makes decentralized per-project session automation (e.g. a per-clone git-freshness guard) safe; without this fact you would wrongly rule OUT project-scoped SessionStart hooks for fear of clobbering global governance, and force everything into a single global hook. Project/local settings resolve to the **git-repo root** and load only for sessions whose cwd is inside that repo (exceptions: outside a git repo, repo-root-is-home, Agent SDK), so such hooks cost nothing on unrelated sessions.

**Caveats & linked constraints:** The docs explicitly guarantee merge only for multiple hooks within the **same** event ("every hook's command runs to completion") and for permission-rule merging across scopes; they are **silent on cross-scope hook-array merge specifically** — so this capability rests on **execution proof** (2026-08-18 A2 probe: a project-scope AND a local-scope SessionStart hook both fired) and must be **re-verified on Claude Code major upgrades**. Plugin / subagent / Agent-SDK contexts may resolve settings or honour hooks differently — see [[CLD-C009_plugin-subagents-ignore-permission-hooks-mcp]]. Injected stdout reaches the model as authoritative-looking raw text — validate what a hook emits (cf. [[CLD-CAP001_hooks-deterministic-governance]]).
