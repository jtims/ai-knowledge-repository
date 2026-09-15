---
id: LOV-C020
platform: lovable
domain: cost
severity: costly
status: active
provenance:
  - {type: session-verified, ref: "a production redeploy 2026-08-25 — send_message (wait=true) returned status 'error' with 'queue is paused (reason: user)' while the message was durably enqueued at position 1; get_message confirmed status 'queued' with the verbatim text; on owner unpause the message executed and consumed 0.6 credits; the MCP tool surface exposes no unpause, cancel, or queue-delete operation", date: 2026-08-25}
verified: 2026-08-25
related: ["[[LOV-C012_credit-consuming-operations]]"]
---

**Constraint:** A Lovable project's message queue can be paused editor-side (`queue_pause_reason: user`). While paused, MCP `send_message` returns status **"error"** — yet the message IS durably enqueued and WILL execute (and consume credits) whenever the queue is unpaused. No MCP operation can unpause the queue or cancel/delete a queued message; both are editor-only actions.

**Design consequence:** "error" from `send_message` does not mean the send failed — treating it as failure and resending double-queues and double-spends (the [[LOV-C012_credit-consuming-operations]] trap by another door). A queued message is a pending state change that fires later without further confirmation, so an automated flow can both stall silently behind a paused queue and execute long after the caller gave up.

**Sanctioned workarounds:** after ANY send error, `get_message` on the returned `message_id` BEFORE deciding anything — status `queued` means the send exists and counts as THE one send under [[LOV-C012_credit-consuming-operations]]; surface a paused queue to the owner same turn (unpause, or editor-side delete of the queued message, are the only moves); never issue another send while one is queued.
