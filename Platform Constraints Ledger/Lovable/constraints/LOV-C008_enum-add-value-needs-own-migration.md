---
id: LOV-C008
platform: lovable
domain: data
severity: friction
status: active
provenance:
  - {type: session-verified, ref: "Postgres 55P04 hit live; enum ADD VALUE cannot run in a transaction with dependent statements (memory: reference_lovable_supabase_migration_constraints)", date: 2026-07-15}
verified: 2026-07-15
related: ["[[LOV-C007_storage-schema-sql-blocked-in-migrations]]"]
---

**Constraint:** `ALTER TYPE ... ADD VALUE` must ship as its OWN migration — combining it with statements that use the new value throws 55P04.

**Design consequence:** enum evolution is always a two-migration sequence; single-send schema batches that bundle it will fail.

**Sanctioned workarounds:** migration 1 = ADD VALUE alone; migration 2 = everything that references it.
