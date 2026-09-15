---
id: CLD-C022
platform: Claude Code
domain: governance
severity: design-invalidating
status: active
provenance:
  - type: session-verified
    ref: "live proof 2026-08-26 - a 'transcript view: verbose' key sat in the frontmatter of ~/.claude/output-styles/<style>.md across sessions with zero effect and zero warning, and the owner reasonably believed verbose transcript view was configured. git show HEAD proved the line an uncommitted local addition, so deleting it returned the file to HEAD rather than changing it"
    date: 2026-08-26
  - type: official-doc
    ref: "code.claude.com/docs/en/output-styles - the Frontmatter table enumerates exactly four supported fields (name, description, keep-coding-instructions, force-for-plugin) and states nothing about how unrecognized keys are handled"
    date: 2026-08-26
verified: 2026-08-26
related: ["[[CLD-C001_description-hazard-chars-break-frontmatter-parsing]]"]
---

**Constraint:** An output style's frontmatter supports exactly four fields, `name`, `description`, `keep-coding-instructions` and `force-for-plugin`. Every other key is silently ignored, with no error, no warning, and no observable difference from a key being honoured. An output style modifies only the system prompt and can configure no harness behaviour.

**Design consequence:** No behavioural or display setting can be delivered through an output style, and attempting it fails in the worst available way. The file parses, the style loads, and the dead key reads as configuration for as long as nobody re-derives it. The failure is doubly invisible from inside a session, because the harness surfaces the style body only, so the frontmatter is never rendered where a mis-set key could be noticed. Any governance scheme that ships behaviour through output-style frontmatter is inert by construction, and an audit that reads output-style files for intent will report settings that do not exist.

**Sanctioned workarounds:** Put behaviour and display configuration in a settings file and nowhere else, using the key name the vendor reference names for that behaviour. Verify by reading back the effective key with `jq` and confirming nothing higher in the precedence chain (managed, command line, project-local, shared-project, user) overrides it, rather than by confirming the text exists somewhere. Treat output-style frontmatter as metadata for the `/config` picker only. Adjacent trap from the same session: a settings key can also be outranked by session-sticky UI state that no file records, which is why `verbose: true` produced no verbose transcript and `viewMode: "verbose"` was required.
