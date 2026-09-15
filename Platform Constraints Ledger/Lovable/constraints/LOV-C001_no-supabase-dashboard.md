---
id: LOV-C001
platform: lovable
domain: access
severity: design-invalidating
status: active
provenance:
  - {type: owner-confirmed, ref: "Hub RBAC design session", date: 2026-07-23}
  - {type: official-doc, ref: "docs.lovable.dev/integrations/supabase + features/cloud", date: 2026-08-06}
verified: 2026-08-06
related: ["[[LOV-C002_no-service-keys-no-external-db-access]]", "[[LOV-C003_no-eject-for-shipped-apps]]"]
---

**Constraint:** Lovable Cloud projects expose NO Supabase dashboard — only the Cloud tab surfaces (Database tables/records/policies/backups, SQL editor, Users, Storage, Secrets, Edge functions, Logs). "Full access to the Supabase dashboard" is documented as a benefit exclusive to connecting your OWN Supabase project.

**Design consequence:** any dashboard-only action (Auth provider config, signup toggles, UI-based secret edits, project settings) is impossible for these backends.

**Sanctioned workarounds:** Lovable migrations (agent sends), edge functions, RLS/SQL, app code; gate auth/signup at the app/data layer; inspect via Lovable MCP `query_database`/`read_file`.
