---
id: GIT-C002
platform: Git
domain: credentials
severity: costly
status: active
provenance:
  - type: session-verified
    ref: "live proof 2026-09-17, remarkable-agent-push repo. With origin set to git@github.com:jtims/remarkable-agent-push.git the push went to https://github.com/... and was rejected with: refusing to allow an OAuth App to create or update workflow .github/workflows/ci.yml without workflow scope. git config --global --get-regexp url showed url.https://github.com/.insteadof git@github.com: and gh auth status showed token scopes without workflow. Setting origin to the ssh://git@github.com/ form was not rewritten and reached SSH, where it failed separately because ~/.ssh/known_hosts did not exist."
    date: 2026-09-17
verified: 2026-09-17
related: []
---

**Constraint:** GitHub rejects any HTTPS push that creates or updates a file under `.github/workflows/` when the OAuth token lacks the `workflow` scope, and a global `url.https://github.com/.insteadOf git@github.com:` rule silently rewrites scp-style SSH remotes to HTTPS, so pointing the remote at SSH does not change which credential is used.

**Design consequence:** A plan in which an agent commits CI workflow files and pushes them cannot assume that `repo` scope is enough, and cannot assume that an SSH remote URL means SSH is in use. The rewrite gives no output: `git remote -v` shows the SSH URL while the transfer runs over HTTPS with the `gh` credential helper, and the only evidence is the `https://` URL in the rejection message. The `ssh://git@github.com/owner/repo.git` URL form is not matched by that rule because the rule's prefix is the scp-style `git@github.com:`. Reaching SSH then requires a trusted host key, which a freshly migrated machine may not have.

**Sanctioned workarounds:** The owner adds the scope with `gh auth refresh -h github.com -s workflow`, accepting that the token can then modify workflows in every writable repository. Or use the `ssh://` URL form for the one repository, after the owner has populated `known_hosts` from `gh api meta` rather than accepting a first-connection prompt. Both are credential or trust-store changes and belong to the owner, not the agent. Check `git config --global --get-regexp '^url\.'` before relying on any remote URL's scheme.
