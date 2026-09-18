# reMarkable - Capabilities MOC

**Platform hub** · prefix `RMK-CAP` · 2 active · schema: [[_SCHEMA-Capabilities]] · Grows via the Change-Control-gated capture protocol.

| ID | Capability | Domain | Leverage | Verified |
|---|---|---|---|---|
| [[RMK-CAP001_native-notebooks-deliverable-through-cloud-sync\|RMK-CAP001]] | Agent-authored markdown can land on an unmodified Paper Pro as a native, pen-editable notebook through cloud sync v3: no developer mode, no document API, no PDF or EPUB conversion | data | unlocks | 2026-09-17 |
| [[RMK-CAP002_stored-shapes-readable-from-any-root-with-downloads-only\|RMK-CAP002]] | How any document or folder is stored (root line, own index, metadata and content JSON) can be read from the current root or an older root by hash, downloads only, so vendor-written shapes are learned without a write | data | accelerates | 2026-09-18 |

**Cross-ledger:** capability nodes here link back to their governing [[_reMarkable-Constraints-MOC|reMarkable constraints]] via `related`. RMK-CAP001 is only safe under the conditions in [[RMK-C003_sync-v3-write-replaces-the-account-wide-root-index|RMK-C003]]. RMK-CAP002 only reads; any write designed from what it shows is bound by RMK-C003 as well.
