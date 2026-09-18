---
id: GIT-C004
platform: Git
domain: access
severity: costly
status: active
provenance:
  - type: session-verified
    ref: "live proof 2026-09-18, owner session 6. git push origin main from ~/Projects/ai-knowledge-repository to a PRIVATE organization repository whose only member and only collaborator is jtims (gh api: private true; members jtims; collaborators jtims admin), over HTTPS through the gh credential helper (account jtims). Five local commits, all authored under the owner's personal address (the global user.email on this Mac), HEAD f512ca3. Refused with: remote: error: GH007: Your push would publish a private email address. Then: ! [remote rejected] main -> main (push declined due to email privacy restrictions). git ls-remote afterwards: main still dcfb693, nothing published. The same repository had accepted two pushes on 2026-09-15 whose commits carried the same author address (origin/main reflog: a43f35e at 12:18, dcfb693 at 13:53 CDT) while that address sat on a second account of the owner's; the owner moved it to jtims on 2026-09-18 (GIT-C003, third read). The attribution walkthrough written for that move had named this setting and concluded that nothing in the project's plan would trip it, looking only at the repository that already commits under the noreply address."
    date: 2026-09-18
  - type: official-doc
    ref: "docs.github.com/en/account-and-profile/how-tos/email-preferences/blocking-command-line-pushes-that-expose-your-personal-email-address, fetched 2026-09-18 through a summarizing fetch. Quoted from it. Each time you push to GitHub, we'll check the most recent commit. If the author email on that commit is a private email on your GitHub account, we will block the push and warn you about exposing your private email. The page as fetched says nothing about private repositories; the live proof above shows they are not exempt."
    date: 2026-09-18
verified: 2026-09-18
related:
  - "[[GIT-C003_github-links-commits-to-the-account-holding-the-author-email]]"
---

**Constraint:** When the pushing GitHub account has "Block command line pushes that expose my email" turned on, GitHub refuses a push (GH007) whose most recent commit is authored under one of that account's private email addresses, also into a private repository that only the account itself can read, so moving an address onto the account (the GIT-C003 fix) can stop pushes that the same repository accepted days earlier.

**Design consequence:** A commit-then-push step cannot assume that a repository which accepted earlier pushes will accept the next one: the check follows the account that holds the author address at push time, not the repository's visibility or its history. Every repository that commits under a machine's global `user.email` inherits the refusal the moment that address becomes a private address of the pushing account, and the failure appears only at the push, after the commits exist. A pre-push review of audience, workflow files and changed paths does not catch it (this one did not); the HEAD commit's author address has to be compared with the pushing account's email settings. By the documented wording only the most recent commit is checked, so older commits under the private address still travel beneath a noreply HEAD: the setting does not guarantee that the address stays unpublished (INFERRED from the doc's wording, not tested here).

**Sanctioned workarounds:** Commit under the account's GitHub noreply address, set repo-locally (`git config --local user.email <id>+<login>@users.noreply.github.com`) before the first commit in any repository that pushes to GitHub, or globally where every repository on the machine pushes under that one account. For commits already made under the private address, choose by exposure. If they may ever be readable by anyone else, rewrite their author before the push (their hashes move, so every record that cites them must be corrected). If the repository is private and its only reader is the owner, nothing is exposed: the owner may turn the setting off for that push (an account action only the owner can take), or the commits may travel beneath the next genuine commit made under the noreply address, a choice the owner makes knowingly. Never add a commit whose only purpose is to put a noreply address at HEAD.
