# Lovable — Hard Constraints MOC

**Platform hub** · prefix `LOV` · 24 active · schema: [[_SCHEMA-Constraints]] · Covers Lovable + Lovable Cloud (managed Supabase backends).

| ID | Constraint | Domain | Severity | Verified |
|---|---|---|---|---|
| [[LOV-C001_no-supabase-dashboard\|LOV-C001]] | No Supabase dashboard — Cloud tab surfaces only | access | design-invalidating | 2026-08-06 |
| [[LOV-C002_no-service-keys-no-external-db-access\|LOV-C002]] | No service keys/connection strings — external tools can't reach the DB | credentials | design-invalidating | 2026-08-06 |
| [[LOV-C003_no-eject-for-shipped-apps\|LOV-C003]] | No Cloud→own-Supabase migration for shipped apps | governance | costly | 2026-08-06 |
| [[LOV-C004_edge-fns-dont-redeploy-on-git-push\|LOV-C004]] | Edge fns do NOT redeploy on GitHub push — Lovable send activates | deployment | design-invalidating | 2026-08-05 |
| [[LOV-C005_publish-is-manual\|LOV-C005]] | Publish is a manual owner step — merge ≠ live client | deployment | costly | 2026-08-05 |
| [[LOV-C006_knowledge-and-skills-dont-enforce\|LOV-C006]] | Knowledge/skills are advisory — never build governance on them | governance | design-invalidating | 2026-07-09 |
| [[LOV-C007_storage-schema-sql-blocked-in-migrations\|LOV-C007]] | Storage-schema SQL blocked in migrations — storage API only | data | costly | 2026-07-15 |
| [[LOV-C008_enum-add-value-needs-own-migration\|LOV-C008]] | Enum ADD VALUE must be its own migration (55P04) | data | friction | 2026-07-15 |
| [[LOV-C009_live-schema-diverges-from-git\|LOV-C009]] | Live schema diverges from git — SELECT-verify first | data | costly | 2026-08-10 |
| [[LOV-C010_connector-removal-is-org-wide\|LOV-C010]] | Connector removal is ORG-WIDE — reconnect, never remove | governance | design-invalidating | 2026-07-07 |
| [[LOV-C011_github-connection-invisible-to-exports-and-api\|LOV-C011]] | GitHub connection invisible to exports/MCP/API | access | costly | 2026-08-06 |
| [[LOV-C012_credit-consuming-operations\|LOV-C012]] | create_project + non-plan sends consume credits; never resend on 500 | cost | costly | 2026-06-30 |
| [[LOV-C013_sso-changes-silently-stale-mcp-tokens\|LOV-C013]] | SSO changes silently stale MCP tokens — workspace-scoped preflight | credentials | costly | 2026-08-10 |
| [[LOV-C014_remix-regenerates-generated-files\|LOV-C014]] | Remix regenerates client.ts/.env/config.toml/types.ts — custom exports dropped, build breaks | deployment | design-invalidating | 2026-08-10 |
| [[LOV-C015_grant-hardening-resets-on-remix\|LOV-C015]] | DB privilege hardening (function grants/RLS) resets to Supabase defaults on remix — re-apply per clone | data | design-invalidating | 2026-08-10 |
| [[LOV-C016_workspace-default-template-not-applied-on-mcp-path\|LOV-C016]] | Workspace DEFAULT template is not applied on the MCP `create_project` path, and no MCP field reveals whether one is set | governance | design-invalidating | 2026-08-24 |
| [[LOV-C017_bare-mcp-create-returns-different-framework\|LOV-C017]] | Bare `create_project` returns the current default scaffold (TanStack Start) — a DIFFERENT framework, so retrofitting is a migration | deployment | design-invalidating | 2026-08-24 |
| [[LOV-C018_initiate-project-cannot-scope-or-template\|LOV-C018]] | `initiate_project` takes only `prompt` — no workspace scope, no template; live but in NO vendor doc | governance | design-invalidating | 2026-08-24 |
| [[LOV-C019_template-list-conflates-design-systems\|LOV-C019]] | `list_template_projects` returns design-system libraries too (7 via API vs 5 in UI) — exclude the `list_design_systems` overlap | governance | costly | 2026-08-24 |
| [[LOV-C020_paused-queue-holds-mcp-sends\|LOV-C020]] | Paused message queue durably holds MCP sends — send "error" ≠ failed; executes on unpause; no MCP unpause/cancel | cost | costly | 2026-08-25 |
| [[LOV-C021_list-projects-page-exceeds-mcp-result-cap\|LOV-C021]] | `list_projects` page payload (520-633KB at limit 100 on a 791-project workspace) exceeds the MCP result cap on every call — spills to file, never returns inline | access | costly | 2026-08-25 |
| [[LOV-C022_transfer-breaks-sync-and-reconnect-creates-new-repo\|LOV-C022]] | TRANSFER breaks sync, rename does not (on GitHub); disconnect-and-reconnect is the DESTRUCTIVE repair, always creating a new repo that can never be re-linked | deployment | design-invalidating | 2026-08-28 |
| [[LOV-C023_vendor-workbook-not-authoritative-for-plan-tier\|LOV-C023]] | Vendor spend workbook is NOT authoritative for plan tier; Lovable is ENTERPRISE not Business, and the skill contradicted MEMORY.md for 26 days undetected | governance | design-invalidating | 2026-08-28 |
| [[LOV-C024_sso-claim-is-workspace-scoped-and-connection-pinned\|LOV-C024]] | SSO claim is workspace-scoped AND connection-pinned — one token reads non-SSO workspaces fine while the org workspace is blocked; an in-session re-auth never lands, so the fix is a NEW connection, not another re-auth | credentials | costly | 2026-09-01 |

**Inbound cross-platform edges:** [[N8N-C002_credentials-live-in-n8n-vault|N8N-C002]] → LOV-C002 (n8n writers to Lovable Cloud DBs must ride app-surface auth).
