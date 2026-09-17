---
id: RMK-CAP001
platform: reMarkable
domain: data
leverage: unlocks
status: active
provenance:
  - type: session-verified
    ref: "live push 2026-09-17 with rr 0.3.6-jt.3 (jtims/remarkable-agent-push) to a real 54-entry library on index schema v3. A one-page markdown file became document 50790e32-3aa7-4850-a05a-72815ac154ce inside a folder, root generation 1789660070533788 to 1789660297193586. Verified three ways. The root index differed from the pre-push root by exactly one added line. The id listing went 54 to 55 with none missing. The vendor web app at app.remarkable.com, read through the owner's signed-in browser, showed the same 12 top-level items and rendered the notebook with title, bullets, nested bullet and a bordered table."
    date: 2026-09-17
  - type: owner-confirmed
    ref: "owner, 2026-09-17, after turning the tablet's Wi-Fi back on. The notebook synced to the reMarkable Paper Pro and accepts pen input. The owner also confirmed the table is unevenly spaced on the tablet, matching the web render. The tablet's firmware version was not read from the device."
    date: 2026-09-17
verified: 2026-09-17
related: ["[[RMK-C001_official-import-is-pdf-and-epub-only]]", "[[RMK-C002_developer-mode-factory-resets-and-breaks-secure-boot]]", "[[RMK-C003_sync-v3-write-replaces-the-account-wide-root-index]]", "[[RMK-C004_document-api-returns-401-to-a-browser-paired-device-token]]"]
---

**Capability:** A client paired as a device can deliver agent-authored markdown to an unmodified reMarkable Paper Pro as a native, pen-editable notebook by building the v6 notebook files locally and writing them through the cloud sync v3 endpoints, with no developer mode, no use of the document API, and no conversion to PDF or EPUB.

**What it unlocks:** RMK-C001 reads as though text can only reach the tablet as a PDF or EPUB, which is a reading document annotated on top. This is the other shape: real typed text the owner can write on and edit, arriving from a terminal command an agent can run. It makes "send this to my tablet" a practical step in an agent workflow (meeting briefs, research summaries, vault deliverables) without touching the device's supported state (RMK-C002) and without the endpoints that refuse this kind of token (RMK-C004). Folder placement works by passing an existing folder's id. The same session showed that a superseded root index remains retrievable for at least an hour after it is replaced, which is what makes a rollback of the root pointer feasible.

**Caveats & linked constraints:** Safe only with a client that meets RMK-C003: fail-closed index parsing, byte-for-byte re-emission of lines it did not create, a recorded previous root, and ideally a dry run immediately before the write, since the library changes underneath the client (it did, twice, during the verifying session). The protocol is undocumented and the vendor can change it. Rendering is limited: headings share one style, inline emphasis is dropped, numbered lists become bullets, code blocks and images are skipped, non-Latin text and emoji do not render, and rasterized tables are placed with uneven spacing. YAML frontmatter must be stripped first, because `---` is a page break. The client cannot create folders or delete what it pushed (RMK-C004); the owner does that on the tablet or in the vendor app. Performing a rollback against the server has not been exercised; only its read side has.
