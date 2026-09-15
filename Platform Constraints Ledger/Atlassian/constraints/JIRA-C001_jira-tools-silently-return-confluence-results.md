---
id: JIRA-C001
platform: Atlassian
domain: data
severity: design-invalidating
status: active
provenance:
  - type: session-verified
    ref: "live sweep 2026-08-28, source-expansion swarm wf_b335fa0d-ee8 Jira worker on <org-site>.atlassian.net (cloudId <cloud-id>): getVisibleJiraProjects returned 50 Confluence space objects; literal-email JQL returned 15 Confluence pages as if they were issues; currentUser()/project-scoped JQL returned correct issues, cross-checked by getJiraIssue"
    date: 2026-08-28
verified: 2026-08-28
related: []
---

**Constraint:** The Atlassian connector's Jira tools can silently answer with Confluence objects instead of Jira data: `getVisibleJiraProjects` returns Confluence spaces (zero Jira project fields), and a JQL query using a literal email string (e.g. `assignee = "user@org.com"`) neither errors nor returns empty; it falls back to a Confluence keyword search and returns plausible-looking pages as results.

**Design consequence:** "It returned results" is not evidence a Jira query ran. Any automation trusting these calls without shape verification ingests wrong-platform data that looks valid. Project enumeration via `getVisibleJiraProjects` and identity filters via literal email strings are both design-invalid on this connector.

**Sanctioned workarounds:** Filter identity with `currentUser()` or a resolved accountId (`lookupJiraAccountId`), never a literal email. Enumerate projects via project-scoped JQL (`project = <KEY>`). Assert returned nodes carry Jira issue shape (`key`, `issuetype`, `status`) before use; treat Confluence-shaped fields (`spaceOwnerId`, `homepageId`) as a misroute signal and fail loudly.
