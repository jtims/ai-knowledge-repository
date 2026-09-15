---
id: CLD-C014
platform: Claude Code
domain: governance
severity: design-invalidating
status: active
provenance:
  - type: session-verified
    ref: "live NotebookEdit tool schema read this session (2026-08-21): required params notebook_path (absolute) + new_source; optional cell_id/cell_type/edit_mode; NO file_path/path/target key. Tool description: replaces/inserts/deletes a cell in a Jupyter notebook (.ipynb)."
    date: 2026-08-21
  - type: session-verified
    ref: "execution proof 2026-08-21 vs live pre-write-gate.sh — {tool_input:{notebook_path:'<protected>.ipynb'}} returned silent (allow) while {tool_input:{file_path:'<same path>'}} returned ask; the missing jq key is the sole cause. Fixed in pre-write-gate v3.2 (F36) and re-verified 31/31."
    date: 2026-08-21
  - type: session-verified
    ref: "harness-DISPATCH reconfirm 2026-08-21 (session 3) — a REAL NotebookEdit tool call to a protected-pattern path was routed by the harness through live pre-write-gate v3.2: transcript hook attachment PreToolUse:NotebookEdit with permissionDecision ask on notebook_path. Closes the F36 fix record's deferred residual (register v2.7). Adjacent fact: an unread/nonexistent notebook target is rejected by input validation BEFORE hook dispatch (~2ms, no hook attachment) — gate probes must use real, already-Read files."
    date: 2026-08-21
verified: 2026-08-21
related: ["[[CLD-C013_file-permission-rules-only-edit-and-read]]", "[[CLD-C009_plugin-subagents-ignore-permission-hooks-mcp]]"]
---

**Constraint:** The `NotebookEdit` tool carries its target path in `tool_input` under the key **`notebook_path`** (absolute), NOT `file_path`. A PreToolUse hook matched on `Edit|Write|NotebookEdit` that extracts only `.tool_input.file_path` (with `.path`/`.target` fallbacks) resolves an EMPTY path for every NotebookEdit call — and if it early-exits on empty, it silently allows the write.

**Design consequence:** A path-based Change-Control / least-privilege gate built on `file_path` alone is fully fail-open for NotebookEdit — an entire registered tool type — including `.ipynb` writes into protected directories. This COMPOUNDS `CLD-C013`: the permission-rule layer also does not consult `NotebookEdit(path)` rules, so a NotebookEdit write to a protected path is doubly ungated (no consulted permission rule + a hook that misses the key). Practical exploitability is bounded (NotebookEdit edits existing `.ipynb` cells, requiring a prior Read), but the Change-Control guarantee is broken outright, and any verification that only feeds the gate a `file_path`-shaped payload will report a false pass.

**Sanctioned workarounds:** (1) Extract `.tool_input.notebook_path` alongside `.tool_input.file_path` in any Edit/Write PreToolUse hook — the F36 fix (`pre-write-gate.sh` v3.2). (2) Exercise a gate with the ACTUAL `tool_input` shape of EVERY tool named in its matcher; a `file_path` payload cannot test NotebookEdit. (3) Do not rely on a permission `NotebookEdit(path)` rule as a backstop (inert per CLD-C013); pair `Read(path)` + `Edit(path)` denies, or enforce with the hook.
