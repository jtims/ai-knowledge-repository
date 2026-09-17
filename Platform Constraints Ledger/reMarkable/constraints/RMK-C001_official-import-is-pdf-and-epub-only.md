---
id: RMK-C001
platform: reMarkable
domain: data
severity: design-invalidating
status: active
provenance:
  - type: official-doc
    ref: "support.remarkable.com/s/article/About-reMarkable-Paper-Pro, Software section. Supported file formats (importing) PDF, EPUB. Supported file formats (exporting) PDF, SVG, PNG. Same two lists on the Paper Pro Move article. Read in a rendered browser 2026-09-17 because the page is a JavaScript shell to plain fetchers."
    date: 2026-09-17
verified: 2026-09-17
related: ["[[RMK-C003_sync-v3-write-replaces-the-account-wide-root-index]]"]
---

**Constraint:** The only file formats a reMarkable Paper Pro or Paper Pro Move officially imports are PDF and EPUB, and the only formats it exports are PDF, SVG and PNG; markdown, HTML, DOCX and plain text have no official import path to the device.

**Design consequence:** Any design that sends agent-authored or vault-authored text to the tablet has to choose between two shapes, and the choice is forced at the start. Convert to PDF or EPUB and accept a fixed-layout or reflowed reading document that is annotated on top, not edited as typed text. Or produce the device's own native notebook format and deliver it through the cloud sync protocol, which is undocumented and carries the root-index risk recorded in RMK-C003. There is no third option on an unmodified device. The vendor's Convert to Notebook features (Word files, web articles, cloud-drive files) are additional official paths but are gated behind a Connect subscription and do not accept markdown.

**Sanctioned workarounds:** Render to PDF or EPUB and import through the official apps or Read on reMarkable. Use a native-notebook client only when it parses the root index fail-closed (see RMK-C003). With Connect active, route Word or web content through Convert to Notebook.
