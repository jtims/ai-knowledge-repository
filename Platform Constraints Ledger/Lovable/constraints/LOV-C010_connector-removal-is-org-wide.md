---
id: LOV-C010
platform: lovable
domain: governance
severity: design-invalidating
status: active
provenance:
  - {type: owner-confirmed, ref: "org-owner constraint (memory: feedback_org_owner_no_chat_removal); project layer §3 runbook", date: 2026-07-07}
verified: 2026-07-07
related: ["[[LOV-C013_sso-changes-silently-stale-mcp-tokens]]"]
---

**Constraint:** removing the Lovable connector from a chat/app as the org owner removes it ORG-WIDE, breaking Lovable for the whole team.

**Design consequence:** "remove and re-add" is never a valid re-auth step for org-owned connectors; runbooks that include removal are destructive.

**Sanctioned workarounds:** re-auth ONLY via Customize → Connectors → disconnect, then reconnect (fresh OAuth); never `claude mcp remove`, never connector deletion.
