---
id: LOV-CAP002
platform: lovable
domain: deployment
leverage: unlocks
status: active
provenance:
  - type: session-verified
    ref: "gateway-refresh scheduled run 2026-08-25 — profiled live field domains across all 100 projects on page 1 of list_projects(<org-workspace-id>), then confirmed per-project on 9 get_project calls"
    date: 2026-08-25
verified: 2026-08-25
related: ["[[LOV-C005_publish-is-manual]]"]
---

**Capability:** A Lovable project object carries `publish_visibility` — a field DISTINCT from `visibility` — which is the actual public-vs-private **publish posture** of the deployed app, so the MCP surface CAN tell an externally-exposed app from an internal one. Measured domains across 100 org-workspace projects: `publish_visibility` ∈ {null (44), 'private' (54), 'public' (2)}; `visibility` ∈ {'draft' (81), 'private' (15), 'workspace_view' (4)}. `visibility` is the editor/sharing state and **never** takes the value 'public'; `publish_visibility` is null or key-absent on a project that has never been published. Both fields are returned by `list_projects` and `get_project`, and the `publish_status` filter enum on `list_projects` (`any | published | internal | external | not_published`) is keyed off this field, not off `visibility`.

**What it unlocks:** Any design that must know whether a Lovable app is externally exposed — gateway posture tagging (`app_env` on the AI gateway allowlist), Datadog `env` dimensions, Portkey metadata, external-exposure audits, security-review triage. Without this fact, a reasonable engineer reads `visibility` as the publish posture, writes a rule keyed on `visibility = 'public'`, and concludes the MCP surface cannot distinguish internal from external — the rule never fires, so every published app is silently stamped internal and no error is ever raised.

**Caveats & linked constraints:** Publish posture is a **manual owner act** — see [[LOV-C005_publish-is-manual]]: `publish_visibility` reflects the last human Publish, not the state of merged code, so a project can read 'private'/null while newer code sits unpublished. Treat null and key-absent as the same "never published" case (the key is omitted entirely on unpublished projects rather than serialized as null). `is_published` must still gate the classification first: a project can carry `publish_visibility: 'public'` while `is_published: false` (1 of 100 observed), and `is_published` is the authority in that conflict. Field names are vendor-owned and unversioned on this surface — re-verify the domains before relying on them in a new design.
