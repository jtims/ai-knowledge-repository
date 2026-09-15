# Atlassian - Hard Constraints MOC

**Platform hub** · prefix `JIRA` · 1 active · schema: [[_SCHEMA-Constraints]] · Grows via the same-turn capture protocol.

Scope: Atlassian platform behaviour (Jira, Confluence, and the claude.ai Atlassian connector's tool surface) that invalidates a design if unknown. The `JIRA` prefix was reserved in the schema registry for Atlassian as a whole; it covers Confluence-side constraints too until the owner splits them. The seed entry shares the shape named on the Python hub: the tool reports success while producing a wrong result, so it is not caught by "it ran without error".

| ID | Constraint | Domain | Severity | Verified |
|---|---|---|---|---|
| [[JIRA-C001_jira-tools-silently-return-confluence-results\|JIRA-C001]] | Connector Jira tools silently return Confluence objects: getVisibleJiraProjects yields spaces; literal-email JQL falls back to Confluence keyword search | data | design-invalidating | 2026-08-28 |
