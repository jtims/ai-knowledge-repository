---
id: RMK-C003
platform: reMarkable
domain: data
severity: design-invalidating
status: active
provenance:
  - type: session-verified
    ref: "source read 2026-09-17 of the rr client (hiteshjoshi/remarkable_rust at 2009321, src/sync_v3.rs). upload_bundle loads the root index, appends one entry, re-serializes every entry, uploads the result as a new blob and swaps the pointer with PUT /sync/v3/root carrying the prior generation (HTTP 412 on a race). In that revision parse_index skipped any line with fewer than five fields and discarded the per-entry type field, so the rewritten root would omit any document whose line it could not read. Behaviour established by reading the code, not by reproducing a loss."
    date: 2026-09-17
verified: 2026-09-17
related: ["[[RMK-C001_official-import-is-pdf-and-epub-only]]", "[[RMK-C002_developer-mode-factory-resets-and-breaks-secure-boot]]"]
---

**Constraint:** A client that adds a document through reMarkable's sync v3 endpoints does so by rebuilding and replacing the account-wide root index, so whatever that client fails to parse and re-emit is removed from the entire cloud library, and paired devices act on the index they are given.

**Design consequence:** A write through sync v3 is never scoped to the one document being added; its blast radius is the whole account. The protocol is the vendor's internal device protocol, it is not publicly documented, and the vendor can change the index format without notice, which is exactly the event that turns a tolerant parser into a data-loss path. Any integration on this path must therefore be treated as irreversible-class work: the client has to fail closed on any index line it cannot fully read, re-emit lines it did not create byte-for-byte rather than reformatting them, and record the previous root hash before the swap. A client that skips unknown lines, defaults unparseable numbers, or rewrites fields it does not understand is unsafe regardless of how well it works today. This was found in a working, released client, which is the reason it is recorded.

**Sanctioned workarounds:** Use a client with a fail-closed parser and verbatim re-emission (the hardened build at jtims/remarkable-agent-push carries that patch). Keep the previous root hash from every push: blobs are content-addressed and are not overwritten, so the prior root remains addressable. Keep the tablet fully synced so the device holds a second copy. Where the content allows it, use the official import paths in RMK-C001 instead, which do not touch the root index from third-party code.
