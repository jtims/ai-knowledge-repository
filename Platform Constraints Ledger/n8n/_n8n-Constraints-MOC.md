# n8n — Hard Constraints MOC

**Platform hub** · prefix `N8N` · 2 active · schema: [[_SCHEMA-Constraints]] · Grows via the same-turn capture protocol.

| ID | Constraint | Domain | Severity | Verified |
|---|---|---|---|---|
| [[N8N-C001_webhooks-unauthenticated-by-default\|N8N-C001]] | Webhooks accept unauthenticated calls unless auth configured | access | design-invalidating | 2026-08-06 |
| [[N8N-C002_credentials-live-in-n8n-vault\|N8N-C002]] | Credentials live in the n8n vault; workflow JSON never carries them | credentials | friction | 2026-08-06 |

**Outbound cross-platform edges:** writing to a Lovable Cloud database from n8n → [[LOV-C002_no-service-keys-no-external-db-access|LOV-C002]] (no direct DB credentials exist; ride app-surface auth or edge ingest).
