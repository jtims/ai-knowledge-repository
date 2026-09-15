---
id: LOV-C007
platform: lovable
domain: data
severity: costly
status: active
provenance:
  - {type: session-verified, ref: "Lovable/Supabase migration constraints (memory: reference_lovable_supabase_migration_constraints)", date: 2026-07-15}
verified: 2026-07-15
related: ["[[LOV-C008_enum-add-value-needs-own-migration]]"]
---

**Constraint:** migrations cannot execute storage-schema SQL on Lovable-managed Supabase — storage changes via the storage API only.

**Design consequence:** bucket/storage-policy designs that assume SQL migrations will fail at apply time.

**Sanctioned workarounds:** storage API calls from edge functions / agent sends for storage objects; SQL migrations for everything else.
