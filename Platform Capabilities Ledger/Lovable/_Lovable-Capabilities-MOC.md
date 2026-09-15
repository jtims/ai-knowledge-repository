# Lovable — Capabilities MOC

**Platform hub** · prefix `LOV-CAP` · 2 active · schema: [[_SCHEMA-Capabilities]] · Covers Lovable + Lovable Cloud (managed Supabase backends). Grows via the Change-Control-gated capture protocol.

| ID | Capability | Domain | Leverage | Verified |
|---|---|---|---|---|
| [[LOV-CAP001_external-integration-via-app-surface\|LOV-CAP001]] | External systems integrate via an edge-fn ingest route / app-user + RLS over PostgREST — never direct DB creds | access | unlocks | 2026-08-10 |
| [[LOV-CAP002_publish-visibility-is-the-publish-posture-field\|LOV-CAP002]] | `publish_visibility` (NOT `visibility`) is the public-vs-private publish posture — `visibility` never carries 'public' | deployment | unlocks | 2026-08-25 |

**Cross-ledger:** capability nodes here link back to their governing [[_Lovable-Constraints-MOC|Lovable constraints]] via `related` (e.g. the sanctioned external-DB access path bounded by `LOV-C002`).
