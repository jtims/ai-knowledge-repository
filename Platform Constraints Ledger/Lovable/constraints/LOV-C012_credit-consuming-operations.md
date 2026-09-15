---
id: LOV-C012
platform: lovable
domain: cost
severity: costly
status: active
provenance:
  - {type: owner-confirmed, ref: "credit discipline, Lovable MCP project layer §5", date: 2026-06-30}
verified: 2026-06-30
related: []
---

**Constraint:** `create_project` and non-`plan_mode` `send_message` consume workspace credits; reads, `plan_mode` sends, and `get_diff` are free. A 500 on a send does NOT mean the send failed.

**Design consequence:** unserialized or retried sends burn credits and can double-apply edits.

**Sanctioned workarounds:** draft/refine prompts outside Lovable, send once, never resend on 500 — verify the RESULT; serialize credit ops (≤1 in flight); `plan_mode` for investigation.
