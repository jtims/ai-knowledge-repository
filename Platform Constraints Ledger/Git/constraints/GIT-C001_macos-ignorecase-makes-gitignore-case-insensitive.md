---
id: GIT-C001
platform: Git
domain: governance
severity: design-invalidating
status: active
provenance:
  - type: session-verified
    ref: "live proof 2026-08-26, claude-analytics-engine repo: git check-ignore -v showed the pattern Claude-Analytics-* matching commands/claude-analytics-cycle.md, and the initial commit shipped 11 of 12 intended files with no error"
    date: 2026-08-26
  - type: official-doc
    ref: "git config core.ignorecase, set to true by git init on case-insensitive filesystems including macOS APFS default"
    date: 2026-08-26
verified: 2026-08-26
related: []
---

**Constraint:** On macOS, git sets `core.ignorecase=true` by default, which makes `.gitignore` pattern matching case-insensitive, so a pattern written for one casing also excludes paths that differ from it only in case.

**Design consequence:** An exclusion glob written to keep data out of a repository also silently excludes source files whose names differ only in case, and `git add` reports no error and no warning. Measured 2026-08-26: the pattern `Claude-Analytics-*`, written to exclude generated workbooks, also matched `commands/claude-analytics-cycle.md`, so an initial commit shipped 11 of 12 intended files and looked successful. The consequential direction for any PII or data-exclusion scheme is that a reviewer cannot determine a pattern's real scope by reading it, and a scheme validated on macOS may behave differently on a case-sensitive filesystem, so the same `.gitignore` gives different results per developer.

**Sanctioned workarounds:** Root-anchor every exclusion pattern (`/_config/`, `/Claude-Adoption-Fact-Table_*.csv`) and target real artifact filenames rather than broad prefixes. Verify BOTH directions with `git check-ignore -v <path>`: confirm every intended data shape is ignored, and confirm every intended source file is not. Compare the staged file count against the intended file count before committing. Never treat a glob's apparent casing as documentation of its scope.
