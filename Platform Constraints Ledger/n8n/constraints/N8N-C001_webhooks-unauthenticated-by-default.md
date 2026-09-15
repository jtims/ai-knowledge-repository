---
id: N8N-C001
platform: n8n
domain: access
severity: design-invalidating
status: active
provenance:
  - {type: official-doc, ref: "docs.n8n.io — Webhook node authentication options (none by default; header/basic/JWT must be configured)", date: 2026-08-06}
verified: 2026-08-06
related: []
---

**Constraint:** n8n Webhook nodes accept unauthenticated calls unless authentication is explicitly configured on the node.

**Design consequence:** every production webhook exposed without configured auth is an open, unauthenticated entry point into the workflow (and whatever credentials it wields downstream). This is the risk class the owner intake's `sec_webhook_auth` check exists to catch.

**Sanctioned workarounds:** configure node auth (header token / basic / JWT) or HMAC-verify in the first node; never ship a bare production webhook.
