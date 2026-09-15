---
id: CLD-C029
platform: Claude Code
domain: governance
severity: design-invalidating
status: active
provenance:
  - type: session-verified
    ref: "owner session d1ea2b00, desktop app with CLI 2.1.270 in permission mode auto: bash-write-tripwire.sh returned permissionDecision ask on two read-only heredoc python3 commands at 14:16:01Z and 14:16:21Z (hook_success records in the transcript); both commands executed (session-changelog.log at 14:16:13Z and 14:16:30Z); no batch-approve token was active (0 BATCH-SUPPRESS lines)"
    date: 2026-09-15
  - type: owner-confirmed
    ref: "owner, same session: only one prompt appeared all session before the probes, so neither ask reached a human"
    date: 2026-09-15
  - type: session-verified
    ref: "controls in the same session, each call sent alone: a Write to a scratch .env (Edit ask rule plus pre-write-gate), git push --force (pre-push-gate only, since Bash(git push:*) is allowed), brew install (ask rule plus machine-state-gate) and a Write to a scratch .claude/skills/ path (pre-write-gate only) all prompted the owner; the auto-mode classifier separately denied a read-only heredoc python3 command although Bash(python3:*) is allowed, so heredoc commands reach the classifier instead of matching allow rules"
    date: 2026-09-15
  - type: official-doc
    ref: "code.claude.com/docs/en/permission-modes (fetched 2026-09-15): prompts forced by an ask rule or by a hook are still shown in auto mode, which the two silent asks contradict; code.claude.com/docs/en/hooks: the Bash if filter is best-effort and runs the hook when it cannot parse a command"
    date: 2026-09-15
verified: 2026-09-15
related: ["[[CLD-C011_auto-mode-classifier-does-not-gate-machine-state]]", "[[CLD-C013_file-permission-rules-only-edit-and-read]]", "[[CLD-C018_pretooluse-hooks-never-run-for-subagent-calls]]", "[[CLD-C019_ask-rules-fail-closed-without-an-answerer]]"]
---

**Constraint:** In permission mode `auto`, a PreToolUse hook's `ask` on a Bash command the harness cannot parse (observed: a heredoc, `python3 - <<'EOF'`) does not reliably reach the user. Two such asks resolved with no prompt and the commands ran, while all four probes sent one call at a time (two single-line commands and two file-tool writes) prompted as documented. The mechanism is inferred from two events and one classifier denial: an unparseable command is decided by the auto-mode classifier, which can approve it over the hook's `ask`.

**Design consequence:** In auto mode, a Bash-side hook such as `bash-write-tripwire.sh` is not a human checkpoint for heredoc or otherwise unparseable commands, so a shell-mediated write to a protected path can land with no prompt when the classifier judges it benign. The same may apply to `machine-state-gate.sh` on interpreter-wrapped commands (untested). This qualifies [[CLD-C011_auto-mode-classifier-does-not-gate-machine-state|CLD-C011]], which calls PreToolUse hooks reliable gates in auto mode: that holds for commands the harness can parse and for file-tool writes, not for unparseable shell.

**Sanctioned workarounds:** (1) make protected writes through Edit or Write, whose hook `ask` prompted in both probes, and back governance paths with `Edit(path)` ask rules ([[CLD-C013_file-permission-rules-only-edit-and-read|CLD-C013]]), which the docs guarantee to prompt in auto mode; (2) keep `permissions.ask` rules for must-prompt command families, remembering they match the command as written; (3) treat the tripwire as detection rather than prevention and audit `~/.claude/session-changelog.log`, which records every executed Bash call either way; (4) re-verify after harness upgrades, since the parse boundary and the classifier are version-dependent. Still UNKNOWN: the exact parse boundary, and whether a hook `deny` on an unparseable command holds.
