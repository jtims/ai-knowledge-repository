---
id: LOV-CAP001
platform: lovable
domain: access
leverage: unlocks
status: active
provenance:
  - type: owner-confirmed
    ref: "owner session 2026-08-06 — sanctioned external write path when direct DB credentials are unavailable (the LOV-C002 workaround)"
    date: 2026-08-06
  - type: official-doc
    ref: "docs.lovable.dev/features/cloud + Supabase edge functions / PostgREST (app-surface auth + RLS)"
    date: 2026-08-10
verified: 2026-08-10
related: ["[[LOV-C002_no-service-keys-no-external-db-access]]"]
---

**Capability:** A Lovable Cloud app integrates with external systems through its own surfaces — an HMAC-secured edge-function ingest route, or a migration-seeded app user with RLS reached over the public PostgREST/auth API — so external writers (n8n, scripts) CAN reach Cloud data even though no service-role key or connection string is ever exposed.

**What it unlocks:** External→Cloud integration designs (n8n webhooks writing to Cloud data, third-party ingest) that a flat "no DB credentials" reading would wrongly rule out entirely. The integration rides app-surface auth, not direct DB access.

**Caveats & linked constraints:** Bounded by [[LOV-C002_no-service-keys-no-external-db-access]] — there is NO direct DB path; everything goes through app auth + RLS + edge functions. RLS must be scoped to the target table, and the ingest route must carry its own auth (HMAC or app user) because the surface is public.
