---
id: LOV-C019
platform: lovable
domain: governance
severity: costly
status: active
provenance:
  - {type: session-verified, ref: "list_template_projects on the org workspace returned 7 entries with total 7; list_design_systems on the same workspace returned 2, namely the org design system <design-system-id> and Cozy Code Library <library-id>, both carrying description 'Library project'. Both ids also appear in the list_template_projects payload. The dashboard Settings > Templates page rendered 5 entries and excluded both", date: 2026-08-24}
verified: 2026-08-24
related: ["[[LOV-C016_workspace-default-template-not-applied-on-mcp-path]]", "[[LOV-C017_bare-mcp-create-returns-different-framework]]"]
---

**Constraint:** `list_template_projects` returns **design-system library projects alongside real project templates**, while the dashboard Templates page excludes them. The two surfaces disagree on the size and membership of the template set (7 via API versus 5 in the UI on the measured workspace). Library entries are distinguishable only by cross-referencing `list_design_systems`, or heuristically by their `description` reading "Library project".

**Design consequence:** any template resolution that selects by position, by count, or by fuzzy name match over the raw `list_template_projects` payload can select a design-system library and pass its id as `template_project_id`. Because templates copy the entire codebase at creation, the result is a new project seeded from a component library rather than an application scaffold, which is a wasted credit spend plus a project that must be discarded per [[LOV-C017_bare-mcp-create-returns-different-framework]]. The divergence also breaks reconciliation work: an audit comparing "templates in the workspace" between the API and the dashboard will report a spurious two-item discrepancy and may conclude the registry is corrupt. Design systems and templates are genuinely different mechanisms - templates copy at creation and never update, design systems bind by reference and update on future generations - so conflating them in a listing is a real API defect, not a naming quirk.

**Sanctioned workarounds:** always call `list_design_systems(workspace_id)` alongside `list_template_projects(workspace_id)` and **exclude every template entry whose id also appears in the design-systems result** before matching. Prefer resolving the template by an explicit, governed id over any name or position match. Do not rely on the `description` field reading "Library project" as the discriminator, since it is author-supplied free text rather than a typed flag. When reconciling API output against the dashboard, apply the exclusion first, then compare counts.
