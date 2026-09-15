---
id: LOV-C005
platform: lovable
domain: deployment
severity: costly
status: active
provenance:
  - {type: session-verified, ref: "owner intake 2026-08-05 — first runtime attempt hit the stale bundle; live only after owner clicked Publish", date: 2026-08-05}
verified: 2026-08-05
related: ["[[LOV-C004_edge-fns-dont-redeploy-on-git-push]]"]
---

**Constraint:** Lovable ingesting merged GitHub commits does not make the client live — Publish is a manual owner step; the published bundle stays stale until then.

**Design consequence:** no fully-automated ship path for client changes; runtime verification before publish tests the old bundle.

**Sanctioned workarounds:** fold "owner publishes" into every ship sequence as an explicit gate; verify against the published URL only after the publish is confirmed.
