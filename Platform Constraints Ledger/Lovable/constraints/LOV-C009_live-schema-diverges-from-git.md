---
id: LOV-C009
platform: lovable
domain: data
severity: costly
status: active
provenance:
  - {type: session-verified, ref: "live schema found diverged from repo migrations during owner gateway work (memory reference_lovable_supabase_migration_constraints)", date: 2026-07-15}
  - {type: session-verified, ref: "v1.1.0 server-side email-domain allowlist (auth.users BEFORE INSERT trigger, migration 20260805174500) was ABSENT on fresh remix ba5b59dd despite shipping in the repo — auth-schema triggers defined by a repo migration do not reliably materialize on Cloud-enable", date: 2026-08-10}
verified: 2026-08-10
related: []
---

**Constraint:** the live database schema of a Lovable-managed Supabase can diverge from what the repo's migration files imply — git is not ground truth for DB state.

**Design consequence:** asserting schema/RLS/data state from repo reads alone produces false claims; migration plans built on git-only knowledge can collide with live state. In particular, a security-critical trigger a repo migration defines on `auth.users` may simply be absent on a fresh remix — never assume a migrated trigger exists on a clone.

**Sanctioned workarounds:** SELECT-verify live state (information_schema, pg_policies, target rows) via `query_database` before asserting or migrating.
