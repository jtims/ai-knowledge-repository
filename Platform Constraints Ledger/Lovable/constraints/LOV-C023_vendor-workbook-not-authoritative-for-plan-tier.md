---
id: LOV-C023
platform: lovable
domain: governance
severity: design-invalidating
status: active
provenance:
  - {type: owner-confirmed, ref: "owner correction during a docs-index build: 'Lovable tier is ENTERPRISE, not business'", date: 2026-08-28}
  - {type: session-verified, ref: "the archived org tech-stack skill (v2.2) references/category-automation-ai.md asserted **Business**, introduced by the v2.1 'Plan-tier reconciliation against an employer-era vendor entitlement register (2026-07-28)' which recorded 'Lovable Standard -> Business'. Global MEMORY.md line 44 asserted 'Lovable = ENTERPRISE tier' over the same period. Both read side by side 2026-08-28; they had disagreed for 26 days", date: 2026-08-28}
verified: 2026-08-28
related: ["[[LOV-C001_no-supabase-dashboard]]", "[[LOV-C002_no-service-keys-no-external-db-access]]"]
---

**Constraint:** The vendor spend workbook is NOT authoritative for Lovable plan tier. Lovable is **ENTERPRISE** (owner-confirmed 2026-08-28). The `Business` value carried by the archived org tech-stack skill from 2026-08-02 to 2026-08-28 came from a workbook reconciliation and was wrong. More generally: a tier derived from the spend workbook is a REPORTED claim from a single financial source, not a VERIFIED entitlement, and the workbook has now been shown to disagree with the owner on at least one platform.

**Design consequence:** Any design gated on Business-tier Lovable limits is scoped against the wrong entitlement set. The retired row's own caveat named the exact axes at risk: SSO, audit-log export, and retention. Under-scoping is the dangerous direction, because it rules OUT a capability that actually exists and pushes the design toward an unnecessary workaround, which is the inverse-razor failure the Capabilities Ledger exists to catch. The failure was silent for 26 days and structurally undetectable: the skill is loaded by most sessions, the memory index is loaded by every session, the two contradicted each other, and nothing compares them. Any other tier in that inventory sourced from the same 2026-08-02 workbook reconciliation carries the same unverified status, and the nine tier corrections that pass recorded are all from this one source.

**Sanctioned workarounds:** Treat a workbook-derived plan tier as REPORTED, never VERIFIED, and label it that way in any design that turns on it. Before a tier drives an irreversible or entitlement-gated decision, confirm it against the owner or the vendor admin console rather than the inventory row alone; the n8n row is the precedent, corrected to ENTERPRISE EDITION on 2026-08-02 from the tenant admin console after the same workbook reading gave a wrong answer. Where a tier is genuinely unrecorded, report UNKNOWN and never infer one from observed usage, which the archived org tech-stack skill's reporting rule already requires for the five name-only vendors. When correcting a tier, remember the fact lives in exactly one shared reference file while the changelog history lives in two SKILL.md variants, and that a synced skills folder edit does NOT reach claude.ai without a re-upload (CLD-C021).
