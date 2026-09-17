---
id: RMK-C002
platform: reMarkable
domain: access
severity: design-invalidating
status: active
provenance:
  - type: official-doc
    ref: "developer.remarkable.com/documentation/developer-mode. Enabling developer mode also performs a factory reset, so data on the device at that time is lost. It breaks the chain of trust enabled by secure boot while keeping disk encryption. A boot warning is shown that cannot be removed or modified. SSH is root at 10.11.99.1 over USB, and Wi-Fi SSH is off until rm-ssh-over-wlan on is run. The vendor will not support software subject to such modifications. Fetched 2026-09-17."
    date: 2026-09-17
verified: 2026-09-17
related: ["[[RMK-C003_sync-v3-write-replaces-the-account-wide-root-index]]"]
---

**Constraint:** On a reMarkable Paper Pro, SSH and filesystem access require developer mode, and enabling developer mode factory-resets the device, breaks the secure-boot chain of trust, adds a boot warning that cannot be removed, and ends vendor support for the modified software.

**Design consequence:** Every integration that reaches the tablet over SSH (on-device tooling, SSH-mode MCP servers, direct reads of the notebook store) carries those four costs as an entry fee, and the first of them is irreversible for any data not already synced. An SSH-based design therefore cannot be trialled casually on a device that holds real work, and it cannot be the default recommendation for a user who wants the device left in its supported state. The vendor documents that developer mode applies to the Paper Pro generation only; earlier devices are outside this node.

**Sanctioned workarounds:** Prefer the cloud path or the USB web interface, neither of which needs developer mode. If SSH is genuinely required, confirm a complete cloud sync first, and treat the enablement as an owner decision with the factory reset stated up front. Developer mode can be disabled again through the vendor's recovery application.
