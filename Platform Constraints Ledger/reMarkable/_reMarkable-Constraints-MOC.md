# reMarkable - Hard Constraints MOC

**Platform hub** · prefix `RMK` · 4 active · schema: [[_SCHEMA-Constraints]] · Grows via the same-turn capture protocol.

Scope: the reMarkable paper tablets (Paper Pro generation unless a node says otherwise), reMarkable OS, the reMarkable cloud and its sync protocol, and third-party clients that write to that cloud. Seeded 2026-09-17 from an owner project, which audited the `rr` push client before enabling it.

| ID | Constraint | Domain | Severity | Verified |
|---|---|---|---|---|
| [[RMK-C001_official-import-is-pdf-and-epub-only\|RMK-C001]] | Official import is PDF and EPUB only; markdown, HTML, DOCX and text have no official path to the device | data | design-invalidating | 2026-09-17 |
| [[RMK-C002_developer-mode-factory-resets-and-breaks-secure-boot\|RMK-C002]] | SSH needs developer mode, which factory-resets the device, breaks the secure-boot chain and ends vendor support | access | design-invalidating | 2026-09-17 |
| [[RMK-C003_sync-v3-write-replaces-the-account-wide-root-index\|RMK-C003]] | A sync v3 write replaces the account-wide root index, so a client that cannot re-emit a line removes that document from the whole library | data | design-invalidating | 2026-09-17 |
| [[RMK-C004_document-api-returns-401-to-a-browser-paired-device-token\|RMK-C004]] | The document API answers 401 to a browser-paired device token even with Connect active, so such a client cannot create folders or delete what it pushed through that API (folder creation on sync v3: RMK-CAP003) | access | design-invalidating | 2026-09-17 |

**History of RMK-C004:** first declined on 2026-09-17 in the form "the document API requires a Connect subscription", because its only evidence was a comment in third-party source. Admitted later the same day on live proof, and in a different form than the comment implied: the refusal happens with Connect active.

**Counterpart capability:** [[RMK-CAP001_native-notebooks-deliverable-through-cloud-sync|RMK-CAP001]] in the Capabilities Ledger, recorded once a live push was observed on a device.

**Outbound cross-platform edges:** pushing the hardened client's CI workflows surfaced [[GIT-C002_https-rewrite-plus-missing-workflow-scope-blocks-workflow-pushes|GIT-C002]].
