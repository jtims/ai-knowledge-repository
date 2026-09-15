---
id: LOV-C006
platform: lovable
domain: governance
severity: design-invalidating
status: active
provenance:
  - {type: owner-confirmed, ref: "governance program finding (memory: feedback_lovable_knowledge_not_enforced)", date: 2026-07-09}
verified: 2026-07-09
related: []
---

**Constraint:** Lovable Workspace/Project Knowledge and workspace skills are advisory only — the agent applies them inconsistently and nothing enforces them.

**Design consequence:** governance built on Knowledge/skills is theater; security-critical instructions in a send may be ignored unless restated inline.

**Sanctioned workarounds:** enforcement ranking — CI on the synced repo + gateway allowlist > build-time failure > default template > knowledge/skills; restate security-critical rules inline in any send that touches them.
