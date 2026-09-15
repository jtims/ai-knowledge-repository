---
id: LOV-C011
platform: lovable
domain: access
severity: costly
status: active
provenance:
  - {type: session-verified, ref: "get_project response carries no GitHub field; real synced repo has no .git/repository field in export tree", date: 2026-08-06}
  - {type: official-doc, ref: "docs.lovable.dev/integrations/git-integration — UI-managed connection; no API exposure documented", date: 2026-08-06}
verified: 2026-08-06
related: []
---

**Constraint:** a Lovable project's connected GitHub repo is not exposed via MCP/API, and code exports carry no repo identity (no `.git`, no `repository` field in the template `package.json`).

**Design consequence:** artifact-based GitHub-repo detection is structurally limited — a detector that scans exports for the repo slug will near-always find nothing; zero hits is expected behavior, not a bug.

**Sanctioned workarounds:** reporter-supplied repo links; a curated/auto-built org registry keyed on the Supabase project ref found in both the export and the repo's `supabase/config.toml`.
