---
id: LOV-C013
platform: lovable
domain: credentials
severity: costly
status: active
provenance:
  - {type: session-verified, ref: "stale-token-after-SSO signature hit 2026-07-07 (runbook created) and again 2026-08-05 mid-session", date: 2026-08-05}
  - {type: session-verified, ref: "did NOT reproduce in a fresh Claude Code session 2026-08-10 — a new session's project-scoped MCP read of project <project-id> inside the SSO-gated org workspace succeeded; a fresh session re-establishes a token carrying the current SSO claim (workspace-scoped list not re-tested this session, so the block is not proven fully cleared)", date: 2026-08-10}
  - {type: session-verified, ref: "REPRODUCED live 2026-08-24 on the claude-mcp registered route: get_me returned all 5 workspaces while list_template_projects and get_project on the org workspace both returned SSO authentication required for the org workspace - the account-OK / workspace-blocked signature exactly as recorded. The claude.ai connector route on the SAME endpoint answered every workspace-scoped call normally, confirming the two routes hold independent tokens. The stale local registration was removed (LOCAL ~/.claude.json only; the org connector was untouched, so LOV-C010 is not engaged)", date: 2026-08-24}
  - {type: official-doc, ref: "docs.lovable.dev/integrations/lovable-mcp-server troubleshooting - on a workspace with Enforce SSO plus a session duration (24h, 48h or 7d) the MCP server requires a fresh SSO sign-in ONCE THAT WINDOW ELAPSES, answering 401 with a WWW-Authenticate Bearer error=invalid_token challenge that spec-compliant clients auto-restart. This reframes the fault as RECURRING and expected, not solely a one-off pre-SSO-token artifact. The live error body also carries a reauth URL of the form https://lovable.dev/sso/reauth?workspace_id=<id>", date: 2026-08-24}
verified: 2026-08-24
related: ["[[LOV-C010_connector-removal-is-org-wide]]", "[[LOV-C016_workspace-default-template-not-applied-on-mcp-path]]"]
---

**Constraint:** SSO/identity/workspace-membership changes silently invalidate existing Lovable MCP OAuth tokens for workspace-scoped operations — account-level calls (`get_me`) keep succeeding while every workspace read is blocked; token refresh cannot add an SSO claim.

**Design consequence:** a "connected" status is not proof of a working connection; fan-outs on an unverified connection fail silently across all workers. There are **two distinct causes with an identical presentation**, and they need different fixes: (a) an SSO **session window elapsing**, which is recurring, expected, and cleared by completing the sign-in the client opens; and (b) a token minted **before** the workspace was SSO-gated, which lacks the claim entirely and is cleared only by a full re-consent, since a refresh cannot add a claim that was never granted. Do not conclude "one-off, already fixed" from a single successful re-auth. Where the same endpoint is reachable by two registrations, each holds its own token and one can be fresh while the other is dead.

**Sanctioned workarounds:** preflight **every session** with a workspace-scoped read (`list_projects` on the org workspace) — never an account call like `get_me`, which succeeds on a dead token; treat any SSO change as a re-consent event (disconnect + reconnect per [[LOV-C010_connector-removal-is-org-wide]], never a removal); abort multi-agent runs if preflight fails rather than fanning workers onto an unverified connection. **Consolidate to a single registration** so no caller can resolve to a stale route; removing a purely local `claude mcp` registration is safe and does not engage LOV-C010, whereas removing the shared connector definition does. Use the reauth URL returned in the error body.
