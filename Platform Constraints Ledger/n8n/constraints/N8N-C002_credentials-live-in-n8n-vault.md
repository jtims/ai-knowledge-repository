---
id: N8N-C002
platform: n8n
domain: credentials
severity: friction
status: active
provenance:
  - {type: official-doc, ref: "docs.n8n.io — credentials are stored encrypted in n8n and attached to nodes; sharing is per-credential", date: 2026-08-06}
verified: 2026-08-06
related: ["[[LOV-C002_no-service-keys-no-external-db-access]]"]
---

**Constraint:** third-party credentials for n8n automations live in n8n's encrypted credential vault, attached per-node with per-credential sharing — not in app secrets, not in workflow JSON (exports strip them).

**Design consequence:** workflow designs must name which vault credential each node uses and who provisions it; importing a workflow JSON never carries its credentials.

**Sanctioned workarounds:** provision credentials in the vault ahead of workflow import; least-privilege per credential (scoped PATs, table-scoped DB identities — see LOV-C002 for Lovable Cloud targets).
