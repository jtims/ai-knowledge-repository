---
id: CLD-C012
platform: Claude Code
domain: cost
severity: design-invalidating
status: active
provenance:
  - type: session-verified
    ref: "run wf_2559383a-a9c journal, 2026-08-18 — pause retrofit (TaskStop mid-Verify) + one StructuredOutput retry-cap agent death forced the Verify+Synthesize tail to execute 3x; segment-2 5.74M tok / 45.4 min, segment-3 5.37M tok / 69.9 min (~4-4.5M of it re-execution); two further schema deaths in the re-run cost two claims their verdicts, one item's only adjudication surviving solely in a vault capture"
    date: 2026-08-18
  - type: official-doc
    ref: "Claude Code Workflow tool contract — 'the longest unchanged prefix of agent() calls returns cached results instantly; the first edited/new call and everything after it runs live'; resume requires TaskStop first; Date.now/Math.random banned in scripts to keep replay deterministic"
    date: 2026-08-18
verified: 2026-08-18
related: ["[[CLD-C002_subagents-never-receive-workflow-tool]]", "[[CLD-C003_workflow-subagents-always-acceptedits]]", "[[CLD-C008_subagent-model-envvar-overrides-all-pins]]"]
---

**Constraint:** A Workflow run resumed via `resumeFromRunId` replays as a positional longest-unchanged-PREFIX of `agent()` calls — a call that was killed mid-flight, errored (e.g. StructuredOutput retry cap), or whose prompt/opts changed stores no reusable result, and EVERY call positioned after the first such hole re-executes live. There is no per-call memoization, no mid-run pause primitive (pausing = TaskStop → script edit → resume), and no skip-forward.

**Design consequence:** Any orchestration design assuming a running workflow can be paused cheaply, resumed selectively, or gated retroactively is invalid. A human gate retrofitted onto a running script costs the whole tail: live-proven 2026-08-18 (run `wf_2559383a-a9c`) — one retrofit pause plus one schema-cap agent death made the Verify+Synthesize tail execute three times (~4–4.5M re-executed subagent tokens), and fresh schema deaths in the re-run erased two claims' verdicts, one item's only adjudication surviving solely in a vault capture. Stages whose prompts embed upstream outputs (a synthesizer embedding a claims table) amplify this: any upstream delta invalidates them and everything after them. An errored agent is a PERMANENT hole — every future resume of that run re-runs its tail.

**Sanctioned workarounds:** (1) build every human gate INTO the script before launch as an arg-controlled early return (e.g. `pause_before_audit`) — never retrofit onto a running run; (2) place fragile schema-heavy calls as late as possible, and give repair/synthesize stages distinct schemas so journal forensics can distinguish them; (3) before ANY resume, read `journal.jsonl`, locate the first hole, and price the tail re-run before spending it; (4) persist stage outputs to disk at stage boundaries so a tail re-run can never destroy the only copy of a result.
