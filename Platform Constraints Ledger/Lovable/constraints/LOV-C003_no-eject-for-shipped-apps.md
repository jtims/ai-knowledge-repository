---
id: LOV-C003
platform: lovable
domain: governance
severity: costly
status: active
provenance:
  - {type: official-doc, ref: "docs.lovable.dev/introduction/faq — no one-click Cloud→own-Supabase migration; export + rebuild in a NEW project", date: 2026-08-06}
verified: 2026-08-06
related: ["[[LOV-C001_no-supabase-dashboard]]"]
---

**Constraint:** there is no migration path from Lovable Cloud to a user-owned Supabase for a shipped app — the documented route is export data + rebuild the schema in a NEW Lovable project.

**Design consequence:** backend opacity (LOV-C001/C002) is PERMANENT for a shipped app; the Cloud-vs-own-Supabase choice is effectively made once, at project inception.

**Sanctioned workarounds:** none for in-place ejection; choose own-Supabase at inception when dashboard/credential access is a requirement.
