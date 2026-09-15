---
id: LOV-C018
platform: lovable
domain: governance
severity: design-invalidating
status: active
provenance:
  - {type: session-verified, ref: "live JSONSchema for initiate_project fetched from tools/list on both the claude-mcp registered route and the claude.ai connector route - properties contains exactly one key, prompt (string, described as 100 to 100,000 characters), and required is [prompt]. No workspace_id, no template_project_id, no design_systems, no wait, no timeout_seconds. Contrast create_project on the same surface, which carries all of those", date: 2026-08-24}
  - {type: session-verified, ref: "initiate_project is absent from the official docs Available tools tables at docs.lovable.dev/integrations/lovable-mcp-server and absent from the vendor machine-readable reference at mcp.lovable.dev/skill.md, while being live on the server - so a reader of either document would not know it exists, yet a model reading tools/list will see it and may select it", date: 2026-08-24}
verified: 2026-08-24
related: ["[[LOV-C016_workspace-default-template-not-applied-on-mcp-path]]", "[[LOV-C012_credit-consuming-operations]]"]
---

**Constraint:** `initiate_project` accepts exactly one property, `prompt`. It has **no `workspace_id`** and **no `template_project_id`**, so it can neither be scoped to a chosen workspace nor seed a template. It is nonetheless a live, credit-consuming project-creation tool, and it is documented in **neither** the official docs nor the vendor machine-readable reference.

**Design consequence:** `initiate_project` cannot satisfy any governed-creation requirement, and it defeats two separate controls at once. It bypasses template seeding, so the project arrives on the bare default stack per [[LOV-C017_bare-mcp-create-returns-different-framework]]. It also bypasses workspace scoping, so the server chooses the workspace, which on a multi-workspace account can silently place an org project in a personal or event workspace. The hazard is specifically that the tool is **invisible to documentation review but visible to tool selection**: a governance document derived from the docs will not think to prohibit it, while a model enumerating `tools/list` may reach for it as the natural "start a new project" verb given its description. Prohibitions written from documentation are therefore incomplete by construction.

**Sanctioned workarounds:** prohibit `initiate_project` explicitly by name in any governing skill or instruction set, rather than relying on a general "use `create_project`" preference. Always use `create_project` with `workspace_id` **and** `template_project_id` passed explicitly. When auditing a governance artifact for completeness, diff it against live `tools/list` rather than against the vendor documentation, since the two disagree in both directions (see the do-not-call list of seven documented-but-unregistered tools recorded in an owner audit record (2026-08-24)).
