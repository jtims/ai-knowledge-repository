---
id: CLD-CAP004
platform: Claude Code
domain: governance
leverage: unlocks
status: active
provenance:
  - type: session-verified
    ref: "headless leg 2026-08-23 (session 7): a temporary agent carrying frontmatter hooks PreToolUse [{matcher: Write, hooks: [{type: command, command: <script>}]}] and tools Write only - the hook DENIED via exit 2 on a uniquely-named path while an adjacent control write LANDED in the SAME invocation; delegation confirmed structurally by exactly one subagent transcript; the hook's own log recorded both the DENY and the ALLOW"
    date: 2026-08-23
verified: 2026-08-23
related: ["[[CLD-C018_pretooluse-hooks-never-run-for-subagent-calls]]", "[[CLD-C019_ask-rules-fail-closed-without-an-answerer]]", "[[CLD-C009_plugin-subagents-ignore-permission-hooks-mcp]]"]
---

**Capability:** A `PreToolUse` hook declared in a **subagent's own frontmatter** DOES fire for that subagent, and can block it (exit 2 denies). This is a **different mechanism** from a `settings.json` hook and is not in tension with [[CLD-C018_pretooluse-hooks-never-run-for-subagent-calls]], which concerns user-scope settings hooks.

**What it unlocks:** A real mechanical bound on subagent behaviour where the settings-scope hook layer provides none. Without this, CLD-C018 leaves only two levers - `Edit(path)` permission rules (which [[CLD-C019_ask-rules-fail-closed-without-an-answerer]] shows fail closed with no answerer, so they are unusable headless) and `tools`/`disallowedTools` stripping (coarse: it removes a capability rather than bounding it). Per-agent frontmatter hooks are finer-grained than both and are the **sanctioned route for the swarm `out_dir` problem** - confining a worker's writes to its run directory. It changed the F49 remediation route at D85. If this capability were unknown, a designer reading CLD-C018 alone would wrongly rule OUT hook-based subagent enforcement entirely and fall back to tool-stripping or to an ungated design.

**Caveats & linked constraints:** **The INTERACTIVE leg is UNVERIFIED.** Only the headless leg was probed, because a newly written agent definition is not synchronously registered, so the in-session Agent-tool path may route differently - do not treat this node as covering interactive use until that leg runs. Frontmatter hooks are also **not** the same as plugin-level `hooks/hooks.json`, and [[CLD-C009_plugin-subagents-ignore-permission-hooks-mcp]] records that plugin-packaged subagents ignore permission hooks and MCP config, with `tools`/`disallowedTools` the only frontmatter lever that survives packaging - so a frontmatter hook's survival through plugin packaging is **UNKNOWN**. Shell-mediated writes remain a gap: per CLD-C018 workaround (3), a write-shape regex like `bash-write-tripwire.sh` has no permission-pattern equivalent, so a subagent with `Bash` can still write around a path-matcher hook. Governing constraint - [[CLD-C018_pretooluse-hooks-never-run-for-subagent-calls]], whose own evidence now rests on ONE leg (the timing discriminator) and whose open question (7) records that the official sub-agents doc states the opposite; re-probe before leaning on either node.
