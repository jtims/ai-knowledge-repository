---
id: CLD-C013
platform: Claude Code
domain: governance
severity: design-invalidating
status: active
provenance:
  - type: official-doc
    ref: "code.claude.com/docs/en/permissions.md (fetched 2026-08-19): Claude Code checks file permissions against Edit(path) and Read(path) rules only; a path rule for Write, NotebookEdit, Glob, or legacy MultiEdit is accepted but never consulted (startup warning), except a Glob rule via --allowedTools. Edit rules apply to all built-in file-editing tools; a Read deny rule blocks Edit and Write on the same path but not NotebookEdit. Requires CC v2.1.210+."
    date: 2026-08-19
  - type: session-verified
    ref: "own read 2026-08-19 of ~/.claude/settings.json — all 11 Layer-1 file permission ask-rules are Edit(...) form (zero Write()/MultiEdit()); consistent with only Edit()/Read() path rules being consulted"
    date: 2026-08-19
verified: 2026-08-19
related: ["[[CLD-C009_plugin-subagents-ignore-permission-hooks-mcp]]", "[[CLD-C011_auto-mode-classifier-does-not-gate-machine-state]]"]
---

**Constraint:** Claude Code consults file-path permission rules for `Edit(path)` and `Read(path)` **only** (v2.1.210+). A path rule written for `Write`, `NotebookEdit`, `Glob`, or the legacy `MultiEdit` is accepted but NEVER consulted (it warns at startup) — the sole exception being a `Glob` path rule passed via `--allowedTools`. A tool-name rule with NO path (e.g. a bare `Write` deny) DOES match, at the tool level, everywhere. `Edit` rules already apply to all built-in file-editing tools; a `Read` deny rule also blocks `Edit` and `Write` on the same path (but not `NotebookEdit`).

**Design consequence:** Any least-privilege or Change-Control scheme that scopes file access with `Write(path)`, `MultiEdit(path)`, `NotebookEdit(path)`, or `Glob(path)` rules silently NO-OPS — the rule loads, the startup warning is easy to miss, and the path is left ungoverned. A governance design validated by "the rule is present in settings.json" is not validated at all; only `Edit(path)`/`Read(path)` path rules (or a bare tool-name rule) actually gate. This is why the hook layer (`pre-write-gate.sh` on `Edit|Write|NotebookEdit`, `bash-write-tripwire.sh` on `Bash`) is the real enforcement here, not permission path-rules alone.

**Sanctioned workarounds:** (1) Use `Edit(path)` to gate all file edits (it covers Write/MultiEdit/NotebookEdit) and `Read(path)` in place of `Glob(path)`. (2) To forbid a path to every tool, pair a `Read(path)` deny (blocks Edit+Write) with an explicit `Edit(path)` deny (for NotebookEdit). (3) For path-scoped control of a tool whose path-rules are ignored, enforce with a PreToolUse hook matched on that tool, not a permission rule. (4) After adding permission rules, read the startup warning — an "is not matched by file permission checks" line means the rule is inert.
