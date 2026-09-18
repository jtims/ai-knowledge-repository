---
id: RMK-CAP003
platform: reMarkable
domain: data
leverage: unlocks
status: active
provenance:
  - type: session-verified
    ref: "live 2026-09-18 with rr 0.3.6-jt.6 (jtims/remarkable-agent-push, release v0.3.6-jt.6 at 430f670), owner session 7, rulings D127 to D131. rr mkdir with --dry-run showed the root index going from 62 to 63 lines, 0 removed, 1 added ending :80000000:<id>:1:214, order preserved. The write created one folder at the top level; the root generation moved once and the previous root equalled the dry run's. Complete listings before and after: 0 ids lost, 0 other rows changed, 1 new. rr inspect read the stored folder as one .metadata blob of 214 bytes, 8 fields in alphabetical order, a 4-space indent, parent empty, type CollectionType, an item index of schema 3 with one line, and a root line ending :1:214. The owner saw it on the tablet at the top level and opened it as an empty folder, then trashed it on the tablet; rr inspect afterwards showed that the tablet changed exactly parent (to trash) and lastModified and kept the 8 fields and the single blob."
    date: 2026-09-18
  - type: session-verified
    ref: "source 2026-09-18 at 430f670. src/sync_v3/folder.rs builds the folder, and the write goes through the push's own helpers upload_doc and plan_doc, whose bodies are upload_bundle's and plan_bundle's moved verbatim (0 lines removed from src/sync_v3.rs), so plan_root's one-added-line invariant and byte-for-byte re-emission apply. 12 new tests ok by name in both test jobs of CI runs 35394388146 and 35395070373, 138 passed each."
    date: 2026-09-18
verified: 2026-09-18
related: ["[[RMK-C003_sync-v3-write-replaces-the-account-wide-root-index]]", "[[RMK-C004_document-api-returns-401-to-a-browser-paired-device-token]]", "[[RMK-CAP002_stored-shapes-readable-from-any-root-with-downloads-only]]", "[[RMK-CAP001_native-notebooks-deliverable-through-cloud-sync]]"]
---

**Capability:** A client paired through the browser device flow can create a folder in the reMarkable cloud through the sync v3 endpoints, with no document API, by writing one `.metadata` blob in the shape the vendor's own software writes (8 fields: `createdTime`, `lastModified`, `new`, `parent`, `pinned`, `source`, `type` set to `CollectionType`, `visibleName`; alphabetical keys, a 4-space indent, one trailing newline) and adding one line to the root index; the tablet shows it, opens it and edits it like a folder made on the device.

**What it unlocks:** RMK-C004 says an agent workflow cannot assume it can make its own destination folder, because folder creation on the document API answers 401 to this pairing. That holds for the document API only. On sync v3 a client can create the folder a push is aimed at, so "put this in a new folder" no longer needs a manual step on the tablet, and a test plan can create its own disposable folder. The shape was learned by reading, not guessed (RMK-CAP002), and the write reuses the push's proven path. In this estate it moved `rr mkdir` off the rr skill's never-run list onto a procedure the owner requests (an owner project rulings D133 and D134).

**Caveats & linked constraints:** It is a root-index write and carries every condition of [[RMK-C003_sync-v3-write-replaces-the-account-wide-root-index|RMK-C003]]: fail-closed parsing, verbatim re-emission, a one-added-line planner, a dry run immediately before, a recorded previous root. Proven once, on one top-level folder; a nested folder uses the same code with the parent's id in `parent` but has not been written live. Names and the parent are checked against a listing read before the write, so a change made on another device in between is not re-checked. Deleting is not covered: `rr rm` still uses the document API ([[RMK-C004_document-api-returns-401-to-a-browser-paired-device-token|RMK-C004]]), and its rebuild as a trash move is planned. The shape is undocumented and the vendor can change it.
