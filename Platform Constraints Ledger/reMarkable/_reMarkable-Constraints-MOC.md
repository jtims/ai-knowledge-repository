# reMarkable - Hard Constraints MOC

**Platform hub** · prefix `RMK` · 3 active · schema: [[_SCHEMA-Constraints]] · Grows via the same-turn capture protocol.

Scope: the reMarkable paper tablets (Paper Pro generation unless a node says otherwise), reMarkable OS, the reMarkable cloud and its sync protocol, and third-party clients that write to that cloud. Seeded 2026-09-17 from an owner project, which audited the `rr` push client before enabling it.

| ID | Constraint | Domain | Severity | Verified |
|---|---|---|---|---|
| [[RMK-C001_official-import-is-pdf-and-epub-only\|RMK-C001]] | Official import is PDF and EPUB only; markdown, HTML, DOCX and text have no official path to the device | data | design-invalidating | 2026-09-17 |
| [[RMK-C002_developer-mode-factory-resets-and-breaks-secure-boot\|RMK-C002]] | SSH needs developer mode, which factory-resets the device, breaks the secure-boot chain and ends vendor support | access | design-invalidating | 2026-09-17 |
| [[RMK-C003_sync-v3-write-replaces-the-account-wide-root-index\|RMK-C003]] | A sync v3 write replaces the account-wide root index, so a client that cannot re-emit a line removes that document from the whole library | data | design-invalidating | 2026-09-17 |

**Declined at the admission bar (2026-09-17):** "the document API (`/doc/v2/files`) requires a Connect subscription". The only evidence is a comment in third-party client source, which is none of the three provenance types this ledger accepts. It re-enters if an official statement or a live 401 on a free-tier account is observed.

**Pending live proof:** the counterpart capability (native notebooks can be delivered through cloud sync without developer mode) is not yet recorded in the Capabilities Ledger because no push has been observed on a device.

**Outbound cross-platform edges:** pushing the hardened client's CI workflows surfaced [[GIT-C002_https-rewrite-plus-missing-workflow-scope-blocks-workflow-pushes|GIT-C002]].
