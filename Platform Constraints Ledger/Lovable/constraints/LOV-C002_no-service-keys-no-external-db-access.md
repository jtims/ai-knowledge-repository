---
id: LOV-C002
platform: lovable
domain: credentials
severity: design-invalidating
status: active
provenance:
  - {type: official-doc, ref: "docs.lovable.dev/features/cloud (no credential exposure documented; external access not offered)", date: 2026-08-06}
  - {type: owner-confirmed, ref: "owner session — owner caught the broken n8n write path", date: 2026-08-06}
verified: 2026-08-06
related: ["[[LOV-C001_no-supabase-dashboard]]", "[[N8N-C002_credentials-live-in-n8n-vault]]"]
---

**Constraint:** Lovable Cloud never exposes the service-role key, database connection string, or any credential an external tool could use — external tools (n8n Supabase node, psql, Supabase MCP) CANNOT connect to the database directly.

**Design consequence:** any integration design assuming direct DB credentials is invalid before it starts.

**Sanctioned workarounds:** a dedicated migration-seeded app user + RLS scoped to the target table, accessed via the app's public auth + PostgREST surface; or an HMAC-secured ingest route on an existing edge function.
