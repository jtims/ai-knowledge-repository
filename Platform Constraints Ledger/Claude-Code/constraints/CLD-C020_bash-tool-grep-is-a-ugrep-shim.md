---
id: CLD-C020
platform: Claude Code
domain: governance
severity: design-invalidating
status: active
provenance:
  - type: session-verified
    ref: "shim identified 2026-08-23 (session 9): `type grep` inside the Bash tool returns a shell FUNCTION sourced from ~/.claude/shell-snapshots/snapshot-zsh-<id>.sh, not /usr/bin/grep; the function body re-executes the Claude Code binary with ARGV0=ugrep and injects the flags -G --ignore-files --hidden -I --exclude-dir=.git/.svn/.hg/.bzr/.jj/.sl ahead of the caller's own flags; `grep --version` reports ugrep 7.8.4 while /usr/bin/grep reports BSD grep 2.6.0-FreeBSD"
    date: 2026-08-23
  - type: session-verified
    ref: "selective -E match failure, minimal repro 2026-08-23: pattern (^|[^A-Za-z0-9_])\\.env with -E against subject /app/.env returns NO MATCH through the shim and MATCH through /usr/bin/grep; the same disagreement reproduces on subjects .env and 'cat .env'; adding -i MASKS the failure and both agree; every isolated construct tested separately (plain alternation, group plus alternation, caret inside a group, dollar inside a group, both anchors in groups, negated class, escaped dot, quantified class) agrees between the two binaries, so the failure is selective rather than a general ERE difference"
    date: 2026-08-23
  - type: session-verified
    ref: "recursive under-report 2026-08-23: a recursive `grep -rl` over an owner notes folder returned 7 files through the shim and 10 through /usr/bin/grep, a 30 percent under-report, silently omitting two notes among others; the searched path is git-excluded, confirmed by git check-ignore -v"
    date: 2026-08-23
  - type: session-verified
    ref: "hooks are NOT affected 2026-08-23: `bash -c 'type grep'`, `sh -c 'type grep'` and `env -i /bin/bash -c 'type grep'` all resolve to /usr/bin/grep; pre-write-gate.sh and bash-write-tripwire.sh are both #!/bin/bash, invoke `grep -qiE` bare, and neither sources the shell snapshot; the .env guard was exercised end to end against pre-write-gate.sh and returned permissionDecision ask for /tmp/.env and /tmp/.env.local while staying silent for notes.txt and src/process.env.ts"
    date: 2026-08-23
verified: 2026-08-23
related: ["[[CLD-C001_description-hazard-chars-break-frontmatter-parsing]]"]
---

**Constraint:** Inside the Claude Code Bash tool, `grep` is **not** the system binary. The shell snapshot sourced into the tool's shell defines a `grep` shell function that re-executes the Claude Code binary as `ugrep` with `-G --ignore-files --hidden -I --exclude-dir=...` injected ahead of the caller's flags. Two behaviours diverge from `/usr/bin/grep`, both **silently**: certain `-E` patterns fail to match where the system binary matches (minimal repro `(^|[^A-Za-z0-9_])\.env` on `/app/.env`, with `-i` masking the failure), and recursive sweeps under-report because `--ignore-files` applies ignore rules (measured 7 files versus 10 on the same sweep).

**Design consequence:** Any detector, audit sweep, acceptance criterion, or drift check built on a bare `grep` call inside the Bash tool can under-report without any error, and because the regex failure is **selective rather than total**, a passing spot-check does not generalise to the pattern actually shipped. The asymmetry inverts the normal trust order: a conclusion reached in-tool is LESS reliable than the identical expression running in production, because hooks resolve `grep` to `/usr/bin/grep`. It follows that **pasting a hook's regex into the Bash tool is not a test of that hook** and can produce a false report that a working control is broken, which is exactly what happened on 2026-08-23 when the live `.env` write-gate pattern was briefly measured as failing on the two most realistic inputs. The recursive half is the more dangerous of the two for governance work, because a radius sweep that silently omits 30 percent of matches understates a remediation's blast radius while looking complete.

**Sanctioned workarounds:** (1) Call `/usr/bin/grep` by absolute path for anything load-bearing: gate patterns, radius sweeps, acceptance checks, register tallies. (2) Never validate a hook pattern through the Bash-tool `grep`; exercise the hook itself with a crafted `tool_input` payload and assert on its emitted decision, with a negative control that must stay silent. (3) For recursive audit sweeps prefer `/usr/bin/grep -r` or `find -print0 | xargs -0`, and state every exclusion out loud, since an exclusion is an assertion about what cannot matter. (4) Do not extract fields from a markdown table with a regex; use a real column parser such as `awk -F'|'` with the header row read first, after a regex field-extraction produced a fabricated 0-closed tally on a register whose rows plainly read CLOSED. (5) Validate any ad-hoc detector against a known-good AND a known-bad fixture in the same run, and print both, so a uniformly-silent instrument is distinguishable from a clean result. (6) Mechanism **UNKNOWN**: the shim injects `-G` ahead of the caller's `-E` and whether that flag collision is the cause is not established; the official documentation does not describe this shim at all, so any deeper inference about which patterns are affected must be treated as UNKNOWN and settled by differential measurement against `/usr/bin/grep` rather than by reasoning.
