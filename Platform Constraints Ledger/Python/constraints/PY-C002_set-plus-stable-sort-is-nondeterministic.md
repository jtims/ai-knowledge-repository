---
id: PY-C002
platform: Python
domain: governance
severity: design-invalidating
status: active
provenance:
  - type: session-verified
    ref: "live proof 2026-08-26, Claude Analytics SSOT s2: 5 PYTHONHASHSEED values produced 4 distinct orderings of one 3-item tie group, swapping two rows of a generated workbook between runs"
    date: 2026-08-26
  - type: official-doc
    ref: "CPython docs, PYTHONHASHSEED and hash randomisation; sorted() documented as stable"
    date: 2026-08-26
verified: 2026-08-26
related: ["[[PY-C001_fstring-ast-offsets-are-expression-relative]]"]
---

**Constraint:** CPython randomises `set` iteration order per process, and `sorted()` is stable, so keys that TIE on the sort key inherit the set's arbitrary order and the sorted result differs between runs of the same program on the same input.

**Design consequence:** Any artifact produced by sorting a set is not reproducible, which removes regenerate-and-diff as a verification technique for that artifact. Measured 2026-08-26: five hash seeds produced four distinct orderings of a three-item tie group; two rows of a generated workbook swapped between runs along with their alternating row shading, so a byte-level diff intended to prove a refactor behaviour-preserving instead flagged a change nobody had made. The defect is invisible whenever a downstream filter happens to drop the tied items, so a passing build is not evidence of absence, and it will surface later when the data changes.

**Sanctioned workarounds:** Give every sort an explicit final tiebreak that totally orders the keys, for example `key=lambda k: (-a.get(k,0), -b.get(k,0), k)`. Verify by fingerprinting output across several `PYTHONHASHSEED` values rather than by a single re-run. When fingerprinting a container format, exclude only genuinely non-content metadata such as an archive's embedded modification timestamp, and state which members were excluded.
