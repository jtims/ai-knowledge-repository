---
id: LOV-C014
platform: lovable
domain: deployment
severity: design-invalidating
status: active
provenance:
  - {type: session-verified, ref: "remixed clone ae6d409b blanked on every route — Lovable regenerated src/integrations/supabase/client.ts as its stock env-based client, dropping the isSupabaseConfigured export that App.tsx/main.tsx import (esbuild entry dep-scan failed, React never mounted); fresh remix ba5b59dd rendered clean only after the guard moved to app-owned src/lib/supabase-config.ts. Fix shipped as ext-hackathon-template v1.1.1 (75c7256)", date: 2026-08-10}
verified: 2026-08-10
related: ["[[LOV-C009_live-schema-diverges-from-git]]"]
---

**Constraint:** on every remix / Cloud-enable, Lovable regenerates its managed generated files — `src/integrations/supabase/client.ts`, `.env`, `supabase/config.toml`, and `src/integrations/supabase/types.ts` — to repoint the new project at its own backend, and any custom export added to, or hand-edit of, these files is silently dropped or rewritten in the process.

**Design consequence:** app code that imports an app-owned symbol from — or depends on a hand-edit to — a generated file builds on the source project but breaks on every remix. Observed: a dropped `isSupabaseConfigured` export → esbuild entry dep-scan failure → blank app on ALL routes (not just the affected page). Regenerated `types.ts` can also change RPC-param nullability and surface new typecheck errors on clones that the source did not show.

**Sanctioned workarounds:** keep app-owned logic in NON-generated files (e.g. `src/lib/supabase-config.ts` deriving flags from `import.meta.env.VITE_SUPABASE_*`, which Lovable injects per clone); never add exports to, or hand-edit, `client.ts` / `types.ts` / `config.toml` / `.env`; run the post-remix ownership gate after every remix (confirm generated config points at the clone's OWN ref, not the source's).
