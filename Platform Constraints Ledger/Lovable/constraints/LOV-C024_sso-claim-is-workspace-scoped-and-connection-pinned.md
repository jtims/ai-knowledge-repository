---
id: LOV-C024
platform: lovable
domain: credentials
severity: costly
status: active
provenance:
  - {type: session-verified, ref: "differential probe run 2026-09-01 on the claude.ai connector route during a gateway-refresh run. On ONE token in ONE session: get_me OK (5 workspaces); list_projects on the Hackathon workspace <second-workspace-id> returned 10 projects with full is_published + publish_visibility payloads; get_workspace and list_projects on the org workspace <org-workspace-id> blocked; get_project blocked on all 10 gateway_allowlist project ids, each naming the org workspace. Owner stated the browser SSO re-auth and connector disconnect-and-reconnect had already been completed before these calls", date: 2026-09-01}
  - {type: session-verified, ref: "consistent with the LOV-C013 provenance of 2026-08-10 — the block did NOT reproduce in a FRESH Claude Code session, a new session re-establishing a token that carried the current SSO claim", date: 2026-08-10}
verified: 2026-09-01
related: ["[[LOV-C013_sso-changes-silently-stale-mcp-tokens]]", "[[LOV-C010_connector-removal-is-org-wide]]"]
---

**Constraint:** The Lovable SSO claim is **workspace-scoped and pinned to the MCP connection**: one token simultaneously reads non-SSO workspaces in full while every call touching the SSO-gated workspace is blocked, and a browser re-auth completed *after* the connection was established never reaches the running session — the connection holds the token it was minted with for its whole life.

**Design consequence:** two false conclusions follow from the block if this is unknown, and both were drawn live before this node existed. First, a blocked the org call is **not** evidence of a dead token, a dead connector, or a dead route — the credential and transport can be provably healthy on the same token in the same turn, so "the connection is stale, retries cannot succeed" is wrong and misdirects the fix. Second, and more costly: **the standard remedy stops working once the session is already running.** Re-auth plus disconnect-and-reconnect is necessary but produces zero observable change in-session, so an operator who has correctly performed it sees identical failures and reasonably concludes the remedy failed or the platform is broken. `get_project` is blocked identically to `list_projects`, so there is no project-scoped escape hatch. Every retry inside the pinned session returns the same error regardless of what has been fixed elsewhere.

**Sanctioned workarounds:** Diagnose with a **differential probe**, never a single call: read a non-SSO workspace (e.g. Hackathon `<second-workspace-id>`) *and* the org workspace in the same turn. Both fail → the token is genuinely bad, so re-auth per [[LOV-C013_sso-changes-silently-stale-mcp-tokens]] (disconnect + reconnect, never remove, per [[LOV-C010_connector-removal-is-org-wide]]). Non-SSO OK + org blocked → the token is healthy and merely lacks the claim, so the fix is to **establish a new connection — restart the session or reconnect the server in-client — not another re-auth**. Never treat `get_me` as a probe in either direction (it succeeds on a claim-less token). Cap in-session retries at one after any remediation: a second identical failure is the pinned token, not new information, and further retries cannot distinguish anything. Read-only work that does not touch the gated workspace (for example a Supabase-side state read) remains fully available while the block stands, and should proceed rather than being abandoned with it.
