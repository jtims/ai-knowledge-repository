---
id: LOV-C021
platform: lovable
domain: access
severity: costly
status: active
provenance:
  - {type: session-verified, ref: "an evaluation session 2026-08-25 — three consecutive `list_projects` calls at `limit: 100` against workspace `<org-workspace-id>` (`get_workspace` reported `num_projects: 791`) returned 632,858 / 521,988 / 525,954 characters. All three exceeded the MCP client's result-token cap, were refused as inline results, and were force-persisted to a file the caller then had to read and query with `jq`. 3 of 3 calls, no successful inline return at that page size", date: 2026-08-25}
verified: 2026-08-25
related: ["[[LOV-C011_github-connection-invisible-to-exports-and-api]]", "[[LOV-C019_template-list-conflates-design-systems]]"]
---

**Constraint:** on a large workspace, a single `list_projects` page is too big to return inline. Each project record carries `description`, `generated_description`, `latest_screenshot_url`, `editor_url` and `preview_url`, so at `limit: 100` the payload runs **520–633 synced folder per page** and exceeds the MCP result-token cap on **every** call. The result is not truncated and not an error: it is refused as an inline result and spilled to a file, which the caller must then read and query out of band. At 791 projects a full enumeration is 8 pages, so the spill is the normal case rather than an edge case.

**Design consequence:** any fleet-wide enumeration of a large Lovable workspace **cannot be consumed inline**, and a caller that assumes inline results fails deterministically rather than intermittently — this is a function of workspace size and page size, not of load or rate limiting. Three specific traps. First, the cheap-read assumption breaks: `list_projects` is free and idempotent under the safety floor, so it reads as a safe cheap call, but it is expensive in *context* and costs a wasted round trip on every attempt. Second, pagination is what triggers it, so the naive "one big page" optimisation is exactly backwards here. Third, and worst for automation, a workflow or subagent fan-out that expects a parsable inline array gets a file path instead and will either error or silently proceed on nothing. Fleet-audit, sunset-sizing and governance-sweep designs that enumerate the workspace must be architected for file-plus-query from the start, because retrofitting the consumption pattern is a rewrite of the consumer.

**Sanctioned workarounds:** reduce page size (`limit` well below 100) when the result must be reasoned over inline; otherwise plan for file-based consumption from the first call and query the spill with `jq` rather than reading it whole. Where only aggregates are needed, prefer them: `get_workspace` alone returns `num_projects`, which answers fleet-size questions with one small call and no enumeration. When per-project attributes are genuinely required (`tech_stack`, `is_published`, `created_at`, `last_edited_at`, `user_id`), enumerate to file and aggregate there, and state the measured denominator rather than implying the whole workspace was read. Note that the per-project GitHub repo is still not obtainable at any page size, per [[LOV-C011_github-connection-invisible-to-exports-and-api]], so a repo-backed-versus-repo-less ratio derived this way is INFERRED and must be labelled as such.
