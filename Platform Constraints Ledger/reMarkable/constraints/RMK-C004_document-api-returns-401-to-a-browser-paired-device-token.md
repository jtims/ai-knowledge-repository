---
id: RMK-C004
platform: reMarkable
domain: access
severity: design-invalidating
status: active
provenance:
  - type: session-verified
    ref: "live 2026-09-17, rr 0.3.6-jt.3. rr mkdir _rr-test, a POST to /doc/v2/files on the eu regional host, failed with the client's message for HTTP 401 (cloud_api.rs maps UNAUTHORIZED to AuthExpired, shown as token expired). One second later rr status succeeded against /sync/v3/root with the same token, which had about two hours of validity left, so the token was not expired. The root generation was unchanged by the refusal. The token's scope claim was not decoded, so the cause is inferred."
    date: 2026-09-17
  - type: owner-confirmed
    ref: "owner, 2026-09-17. The account has an active Connect subscription, so the refusal is not explained by the free tier."
    date: 2026-09-17
verified: 2026-09-17
related: ["[[RMK-C003_sync-v3-write-replaces-the-account-wide-root-index]]"]
---

**Constraint:** A client paired through reMarkable's browser device-pairing flow receives HTTP 401 from the document API (`/doc/v2/files`) even on an account with an active Connect subscription, while the same token is accepted by the sync v3 endpoints.

**Design consequence:** Anything built on the document API is unavailable to such a client: creating folders, and by the same endpoint listing with its metadata and deleting documents or folders. Observed on folder creation; deletion and listing through that endpoint were not exercised and are expected to fail the same way. An agent workflow therefore cannot assume it can make its own destination folder or clean up what it pushed, and a test plan cannot assume the client can delete its own test artifacts. Subscribing to Connect does not change this, which contradicts the natural reading of comments in the upstream client's source. A client that reports the 401 as an expired token will send the operator to re-pair for no benefit; the message, not the pairing, is what is wrong. The likely cause is that device tokens from this pairing flow carry a sync-only scope; that is inferred from the behaviour and was not confirmed by decoding the token.

**Sanctioned workarounds:** The owner creates folders and deletes documents on the tablet or in the vendor's web, desktop or phone app; the client then targets an existing folder by id. Folder creation and deletion can be implemented on sync v3 instead, since a folder is an index entry with metadata like any document, but that is a root-index write and inherits every condition in RMK-C003. Do not re-pair in response to this error.
