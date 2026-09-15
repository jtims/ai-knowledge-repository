---
id: CLD-C019
platform: Claude Code
domain: governance
severity: design-invalidating
status: active
provenance:
  - type: session-verified
    ref: "interactive resolution 2026-08-23 (D-E probe, session 6): a general-purpose subagent pinned haiku edited two ask-matched scratchpad decoys, decoy.pem against Edit(//**/*.pem) and .gitconfig against Edit(//**/.gitconfig); both writes LANDED and both cost 6678ms and 6552ms against 316ms for a non-ask Edit by the same agent on an adjacent file in the same directory, a 21x differential proving the rule was evaluated rather than skipped; the owner confirmed the same turn that permission prompts appeared and were approved, so the ask reached a human through the PARENT session UI"
    date: 2026-08-23
  - type: session-verified
    ref: "fail-closed with no answerer 2026-08-23: a nested headless claude -p run with --permission-mode acceptEdits edited two adjacent files under one invocation; headless-free.txt with no matching ask rule LANDED, while headless.pem matching Edit(//**/*.pem) was refused with the message Claude requested permissions to write to PATH but you haven't granted it yet, and the file was byte-unchanged"
    date: 2026-08-23
  - type: session-verified
    ref: "rival explanation refuted 2026-08-23: headless-notask.key, a credential-shaped extension carrying NO ask rule, LANDED under the identical acceptEdits invocation, so the refusal of headless.pem is attributable to the ask rule and not to a generic credential-path heuristic; a prior leg using --permission-mode default was DISCARDED as uninterpretable because its no-ask control was also blocked"
    date: 2026-08-23
verified: 2026-08-23
related: ["[[CLD-C018_pretooluse-hooks-never-run-for-subagent-calls]]", "[[CLD-C002_subagents-never-receive-workflow-tool]]", "[[CLD-C013_file-permission-rules-only-edit-and-read]]", "[[CLD-C011_auto-mode-classifier-does-not-gate-machine-state]]"]
---

**Constraint:** A `permissions.ask` rule is satisfiable only where an answerer exists. In an interactive session the prompt reaches the OWNER through the parent session UI, and this holds for Agent-tool subagent calls as well, even though [[CLD-C002_subagents-never-receive-workflow-tool]] removes `AskUserQuestion` from every subagent. Where no answerer exists, meaning headless `claude -p`, CI, or scheduled automation, the ask FAILS CLOSED: the tool call is refused and the write does not land. `--permission-mode acceptEdits` does NOT satisfy an ask rule; it auto-accepts only edits that no ask rule matches.

**Design consequence:** The subagent's inability to address a human is NOT the same as the permission layer's inability to reach one. Ask rules therefore GATE subagent writes in interactive use rather than hard-blocking them, which CONFIRMS workaround (1) of [[CLD-C018_pretooluse-hooks-never-run-for-subagent-calls]] instead of inverting it, and makes the permission layer a usable substitute for the PreToolUse hooks that C018 proved absent inside subagents. The cost is a prompt per matched call, borne by the owner, at roughly 6 to 24 seconds of latency per decision observed here. The inverse case is the trap: the SAME rule set that gates correctly in an interactive session hard-blocks in headless or scheduled execution, so any automation that crosses an ask-matched path fails closed and silently produces nothing. A rule set validated interactively therefore proves nothing about the same rules under `claude -p`, cron, or CI, and a permission scheme intended to govern both must be tested in both.

**Sanctioned workarounds:** (1) Prefer ask rules over PreToolUse hooks for protected-path Change Control on paths reached by subagents, since only the permission layer survives the C018 dispatch gap. (2) Do NOT place an ask rule on a path that unattended automation must write; either carve that path out or grant it explicitly in the automation's own invocation. (3) Never rely on `acceptEdits` or a permissive session mode to clear an ask rule; ask outranks both. (4) Split protected paths by whether a legitimate agent must write there. Governance and config paths, where no agent has a write need, take ask rules and SHOULD hard-block. Content paths that agents legitimately produce into are better left to the hook layer plus a two-turn relay, since an ask there taxes the owner with a prompt per file. This split was applied to `settings.json` on 2026-08-23, adding 7 `Edit()` rules over `.claude/hooks/`, `.claude/settings.json`, `.claude/settings.local.json`, `.claude/CLAUDE.md`, `.claude/context/` and `.env`, and deliberately excluding the synced knowledge folders. (5) UNKNOWN and untested: what happens when the auto-mode classifier DECLINES a subagent's ask rather than surfacing it. It could not be probed safely, because any decoy harmless enough to write is harmless enough to be approved.
