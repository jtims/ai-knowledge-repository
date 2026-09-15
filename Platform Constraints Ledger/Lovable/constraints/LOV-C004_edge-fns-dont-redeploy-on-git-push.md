---
id: LOV-C004
platform: lovable
domain: deployment
severity: design-invalidating
status: active
provenance:
  - {type: session-verified, ref: "owner intake 2026-08-05 — fn_marker NULL post-publish (proven negative), then present after one Lovable redeploy send (all 22 fns, zero diffs)", date: 2026-08-05}
verified: 2026-08-05
related: ["[[LOV-C005_publish-is-manual]]"]
---

**Constraint:** GitHub push/merge into a Lovable-synced repo updates the code but does NOT redeploy Supabase edge functions — the merged fn code sits inactive until deployed.

**Design consequence:** shipping server-side changes via the GitHub channel alone silently leaves old fn behavior live; runtime verification against unredeployed fns tests the wrong code.

**Sanctioned workarounds:** one Lovable send per merged batch-set: "Redeploy ALL Supabase edge functions — code must NOT be changed"; prove activation with a version marker (e.g. `analysis.fn_marker`).
