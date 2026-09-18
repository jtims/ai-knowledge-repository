---
id: GIT-C003
platform: Git
domain: governance
severity: costly
status: active
provenance:
  - type: official-doc
    ref: "docs.github.com/en/pull-requests/committing-changes-to-your-project/troubleshooting-commits/why-are-my-commits-linked-to-the-wrong-user, fetched 2026-09-18 through a summarizing fetch. Quoted from it. GitHub links a commit to a user by matching the email address in the commit header to an email address on a GitHub account. And. Old commits might not be linked after you update your email settings. The page does not say whether one address can sit on two accounts."
    date: 2026-09-18
  - type: session-verified
    ref: "live proof 2026-09-18, owner session 4, minutes after jtims/remarkable-agent-push was made public. gh api repos/jtims/remarkable-agent-push/commits, login per author address, showed the 17 commits authored under the owner's personal address linked to a second GitHub account of the owner's, not to jtims, which owns the repository and pushed every one of them. The commits authored under the jtims noreply address were linked to jtims. The pre-publication review (15 read-only agents, a pattern scan with a planted control, one audit pass) examined content only and never looked at this linkage."
    date: 2026-09-18
  - type: session-verified
    ref: "second read 2026-09-18, owner session 5. The same API call returned jtims for the same 17 commits. Nothing had been pushed in between (main still 7234cce, one remote head, the same tags), so the link is computed from the account that holds the address now and applies to commits already on GitHub. What changed on the account side was not observed by the session."
    date: 2026-09-18
  - type: session-verified
    ref: "third read 2026-09-18, owner session 5, after the owner said in chat that the address had been moved from the second account to jtims. Per commit, all 17 read verified true with reason valid, where session 4 had read verified false with reason unknown_key, and the fix commit a477994 carries verified_at 2026-09-18T17:55:31Z. Nothing was pushed between the reads. The signature result therefore moved together with the account link, with no change to any commit, key or tag."
    date: 2026-09-18
verified: 2026-09-18
related: []
---

**Constraint:** GitHub attributes a commit to whichever account currently holds the email address in the commit's author header, not to the account that pushed it or that owns the repository, so a commit authored under an address registered on a different account is displayed, publicly, as that other account's work, and, as observed, a signed commit in that state also shows as unverified until the address sits on the account that holds the signing key.

**Design consequence:** A plan to publish a repository, or to open an issue or pull request that links to a commit, cannot treat "who will this show as" as settled by the pushing account or by `git config user.name`: the doc names the address as the matching key. While a repository is private nobody sees the result, so the mismatch first appears at the moment of publication, where it splits the contributor list and puts another account's name and avatar on every affected commit, including one linked from an outward-facing issue. A content review (secrets, paths, personal data) does not catch it, because nothing in the content is wrong: the check has to be made against the platform, once per distinct author address. The address itself also becomes public in every commit header and in the tagger line of every annotated tag. Signature status follows the same linkage, by observation: while the address sat on the other account the 17 commits read `verified: false` with reason `unknown_key`, although the same key verified the noreply commits, and after the address moved they read `verified: true, valid` with nothing pushed in between. GitHub's REST reference defines `unknown_key` as a key not registered with any user's account, which does not describe this case by its wording, so treat the mechanism as INFERRED (the signature is checked against the keys of the account the address resolves to) and the two observed states as VERIFIED. A verification result is therefore not a property of the commit alone, and it has to be read per commit from the host.

**Sanctioned workarounds:** Before a first publication or any outward link to a commit, list the distinct author addresses (`git log --format=%ae | sort | uniq -c`) and the tagger lines of annotated tags, then read how the host resolves each address: `gh api "repos/OWNER/REPO/commits?per_page=100" --jq '.[] | [.commit.author.email, (.author.login // "NONE")] | @tsv' | sort | uniq -c`. That call is expected to work on a private repository with the owner's token; in the case above it was first run after publication, so that is not proven here. Commit under the account's GitHub noreply address, set repo-locally, from the first commit of any repository that may become public. If the wrong account holds an address, the fix is an account action that only the owner can take (remove the address from one account, add and verify it on the other); commits already on GitHub were re-linked in the case above, although GitHub's page warns that old commits might not be. Rewriting history to change the address is the costly alternative: it moves every hash, tag, release and recorded digest, and it cannot recall forks of a public repository.
