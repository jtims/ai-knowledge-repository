---
id: LOV-C015
platform: lovable
domain: data
severity: design-invalidating
status: active
provenance:
  - {type: session-verified, ref: "grant lockdown (REVOKE anon/authenticated EXECUTE on the 6 public SECURITY DEFINER RPCs) applied + verified live on golden template ba5b59dd; after remixing it to event master 9a3ded0e the fresh backend showed all 6 functions back to Supabase-default anon+authenticated EXECUTE (has_function_privilege), and the backup repo carried no supabase/migrations dir — the lockdown did not survive; re-applied + verified live on 9a3ded0e", date: 2026-08-10}
  - {type: official-doc, ref: "Supabase docs — new functions default-grant EXECUTE to public/anon/authenticated/postgres/service_role; revoke the named roles, not just PUBLIC", date: 2026-08-10}
verified: 2026-08-10
related: ["[[LOV-C014_remix-regenerates-generated-files]]", "[[LOV-C009_live-schema-diverges-from-git]]"]
---

**Constraint:** database privilege hardening does NOT survive a Lovable remix — a remixed project provisions a fresh backend whose public `SECURITY DEFINER` functions are recreated with Supabase's default EXECUTE grants (to `anon` + `authenticated`), so any REVOKE-based least-privilege lockdown applied to the source template is silently reset on every clone.

**Design consequence:** a grant/RLS hardening applied once to a "golden" template does NOT propagate to its remixes — each clone silently ships with the permissive defaults (e.g. `anon`/`authenticated` can EXECUTE `SECURITY DEFINER` RPCs → Supabase linter 0028/0029 re-fires). A REVOKE migration added to the repo does not reliably carry either: a remix's backup repo may lack the `supabase/migrations` dir, and migrations do not reliably re-run on a clone (see [[LOV-C009_live-schema-diverges-from-git]]). "Clone security == template security" is false — a security fix verified on the template is unverified on every clone.

**Sanctioned workarounds:** treat privilege hardening as a PER-CLONE pre-provision step, never a one-time template edit — after each remix, SELECT-verify grants (`has_function_privilege`) and re-apply the REVOKE/GRANT block via `query_database` (or a Lovable migration send). `service_role` keeps its explicit grant across `REVOKE ... FROM PUBLIC, anon, authenticated`, so edge functions (which call RPCs via the service role) are unaffected — revoke the named API roles, not just PUBLIC. Keep the verify + re-apply SQL in the clone runbook.
