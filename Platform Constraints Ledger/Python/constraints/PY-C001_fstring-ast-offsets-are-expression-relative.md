---
id: PY-C001
platform: Python
domain: governance
severity: design-invalidating
status: active
provenance:
  - type: session-verified
    ref: "live proof 2026-08-26, Claude Analytics SSOT s2: an AST-span splice into build_html.py produced an unparseable file, then a corrupted partial overwrite reading Re-dePR.decile_scopene"
    date: 2026-08-26
  - type: official-doc
    ref: "CPython PEP 701, f-strings formalised in the grammar in 3.12; nested expression nodes gain correct absolute positions"
    date: 2026-08-26
verified: 2026-08-26
related: ["[[PY-C002_set-plus-stable-sort-is-nondeterministic]]"]
---

**Constraint:** On CPython below 3.12, `ast` nodes nested inside an f-string expression carry `lineno` and `col_offset` relative to the expression rather than to the file, and `col_offset` is a UTF-8 BYTE offset rather than a character index.

**Design consequence:** Any tool that rewrites source by AST span silently corrupts files whose target literals sit inside f-strings, and the result is a plausible-looking partial overwrite rather than an error. Two failure modes stack independently: byte-versus-character offsets on any line containing non-ASCII, and expression-relative offsets inside f-strings. Measured on Python 3.9.6, a splice of six string literals inside a 700-line f-string landed six bytes off. A codemod, refactoring pass, or migration script built on `ast` spans therefore cannot be trusted on a pre-3.12 interpreter without an independent self-check, and the failure is silent: the corrupted file is written before anything notices.

**Sanctioned workarounds:** Rebuild the exact source literal and replace it only where it occurs EXACTLY once in the file, asserting the count first. Alternatively use `ast.get_source_segment`, which performs the offset arithmetic correctly. Always `ast.parse()` the rewritten source and refuse to write on `SyntaxError`. Where spans are unavoidable, verify that each span re-parses to the value it claims (`ast.literal_eval(span) == node.value`) before splicing.
