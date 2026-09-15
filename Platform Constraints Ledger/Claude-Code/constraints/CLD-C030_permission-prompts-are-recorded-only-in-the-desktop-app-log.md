---
id: CLD-C030
platform: Claude Code
domain: governance
severity: design-invalidating
status: active
provenance:
  - type: session-verified
    ref: "owner F33 remediation session 3231f15e, desktop app with CLI 2.1.270 in permission mode auto: the session transcript holds no entry for a permission prompt or its answer (between each probe's tool_use and tool_result there are only file-history-delta and attachment entries), while ~/Library/Logs/Claude/main.log records each prompt as an 'Emitted tool permission request <id> for <Tool> in session local_<id>' line and a 'LocalSessions.respondToToolPermission: requestId=<id>, decision=once|always|deny' line; 50 requests on 2026-09-15 paired by id"
    date: 2026-09-15
  - type: session-verified
    ref: "the log contradicts two findings built on recollection and transcript timing: all four Writes that F33 called unprompted (session eef75a3d, 11:58:59 to 12:05:47 local) raised a Write request answered once after 2, 5, 1 and 4 s, and both heredoc asks that CLD-C029 called silent (session d1ea2b00, 09:16:06 and 09:16:26 local) raised a Bash request answered once after 7 and 4 s, at the moments the commands ran. Control: a Write that auto mode routes to the classifier with no user rule (~/.claude/.gitignore, session eef75a3d, 12:13:23 local) raised no request, so a request line marks a real prompt"
    date: 2026-09-15
  - type: owner-confirmed
    ref: "owner, 2026-09-15: reported seeing no prompt for any of the six contested events; in a hands-off probe the Write request stayed pending 124 s (13:10:00 to 13:12:04 local) until the owner approved it in the desktop window, with nothing shown on the phone, so no automatic responder answered it"
    date: 2026-09-15
verified: 2026-09-15
related: ["[[CLD-C029_hook-ask-on-unparseable-bash-can-pass-without-prompt]]", "[[CLD-C013_file-permission-rules-only-edit-and-read]]", "[[CLD-C019_ask-rules-fail-closed-without-an-answerer]]", "[[CLD-C011_auto-mode-classifier-does-not-gate-machine-state]]"]
---

**Constraint:** The Claude Code session transcript records neither a permission prompt nor its answer; in the desktop app the only record is `~/Library/Logs/Claude/main.log` (one `Emitted tool permission request` line and one `respondToToolPermission ... decision=` line per prompt), so whether a gate prompted cannot be established from the transcript, from call timing or from recollection.

**Design consequence:** A gate check that concludes "no prompt" from the operator's memory or from transcript timing is not a check. On 2026-09-15 that method had produced two false findings, F33 (the D35 `Edit(path)` ask rules miss the Write tool) and [[CLD-C029_hook-ask-on-unparseable-bash-can-pass-without-prompt|CLD-C029]] (a hook `ask` on unparseable Bash passes silently in auto mode), both contradicted by the log: six prompts were answered "once" in 1 to 7 s, inside the 1 to 12 s range of this operator's known approvals that day, and were not remembered. The `Edit(path)` rules gated the Write tool on 7 of 7 Writes to paths no hook covered, as [[CLD-C013_file-permission-rules-only-edit-and-read|CLD-C013]] documents. Who answered the six prompts is recorded nowhere.

**Sanctioned workarounds:** (1) Verify every live gate probe against `main.log`: pair the request and response lines by request id, and read a missing request line as "no prompt". (2) Send one probe per message and have the operator wait a fixed interval before answering, so a faster answer is attributable to something else. (3) Record the request id, the decision and the delay as the probe's evidence, not the operator's recollection. (4) Scope: the log is per machine and specific to the desktop app; the equivalent record for CLI-only and headless sessions is UNKNOWN.
