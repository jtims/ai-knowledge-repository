---
id: LOV-C017
platform: lovable
domain: deployment
severity: design-invalidating
status: active
provenance:
  - {type: session-verified, ref: "package.json read from control project <control-project-id> created by create_project with no template_project_id on the org workspace - name tanstack_start_ts with dependencies @tanstack/react-start 1.168.32, @tanstack/react-router 1.170.18, nitro 3.0.260603-beta, vite 8.1.5, tailwindcss ^4.2.1, react ^19.2.0, and devDependency @lovable.dev/vite-tanstack-config. File tree carried src/router.tsx, src/routeTree.gen.ts, src/routes/__root.tsx, src/routes/index.tsx, src/server.ts, src/start.ts, bunfig.toml. the org template by contrast reports tech_stack new_style_vite_react_shadcn_ts_testing_2026-01-08 via get_project", date: 2026-08-24}
  - {type: official-doc, ref: "docs.lovable.dev carries a dedicated /features/upgrade-to-tanstack-start page, corroborating that TanStack Start is the current default target rather than an anomaly of one project", date: 2026-08-24}
verified: 2026-08-24
related: ["[[LOV-C016_workspace-default-template-not-applied-on-mcp-path]]", "[[LOV-C014_remix-regenerates-generated-files]]"]
---

**Constraint:** `create_project` without `template_project_id` returns Lovable's **current default scaffold, which is TanStack Start** (`@tanstack/react-start` + `@tanstack/react-router` + `nitro`, Tailwind v4, React 19, file-based routing under `src/routes/`). Where an organization's template is a Vite + React Router application, the bare result is a **different framework**, not an ungoverned copy of the template.

**Design consequence:** the cost of missing the template seed is a framework migration, not a file copy. Nothing that assumes the template's shape transfers: a Module Federation dual-mode contract keyed on a `src/StandaloneApp.tsx` entry, observability wiring initialised in `src/main.tsx` before `createRoot`, `src/authz/*` platform-auth modules, and any `.env.mf-*` build modes all have no counterpart in a TanStack Start tree with `src/server.ts` and `src/start.ts` entrypoints. "Add the governance files afterwards" is therefore not a viable remediation, and any runbook offering it is wrong. Note also that the default stack is a moving target set by the vendor: a template pinned to an older stack diverges further from the bare default over time, so the gap widens silently.

**Sanctioned workarounds:** never remediate a mis-seeded project in place - **create a new project with `template_project_id` set** and abandon the stray one (deletion is a dashboard action; no delete tool exists on the MCP surface). Detect the condition cheaply by reading `package.json` and checking the `name` field and the presence of `@tanstack/react-start` before doing any work. When comparing a project against the template, compare `tech_stack` from `get_project` first, since a stack mismatch invalidates every file-level comparison that follows.
