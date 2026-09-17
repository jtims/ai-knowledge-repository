---
id: CLD-CAP007
platform: Claude Code
domain: deployment
leverage: accelerates
status: active
provenance:
  - type: official-doc
    ref: "code.claude.com/docs/en/skills, section 'Edit a skill during a session', fetched 2026-09-17 through WebFetch (a summarizing fetch). Paraphrase: Claude Code watches skill directories for file changes, except in bare mode; a skill added, edited or removed under ~/.claude/skills/, a project's .claude/skills/, or the .claude/skills/ of an --add-dir directory takes effect inside the current session with no restart. Stated exception: a top-level skills directory that did not exist when the session started needs a restart before it is watched. Stated limitation: live detection covers SKILL.md text only; a skill folder that is also a plugin needs /reload-plugins for its hooks, MCP config, agents and output styles."
    date: 2026-09-17
  - type: session-verified
    ref: "live proof 2026-09-17, owner session 2 (transcript 8e950204), Claude Code desktop app. The session began at 17:10Z. ~/.claude/skills/ dates from 2026-09-15; ~/.claude/skills/rr/ did not exist at session start (directory birth time 17:37Z). SKILL.md was written at 17:36Z to 17:37Z, and at 17:41Z a Skill tool call for rr returned 'Launching skill: rr' in the same session, with no restart in between. Re-read from the transcript and from stat in session 3 the same day."
    date: 2026-09-17
verified: 2026-09-17
related: ["[[CLD-C001_description-hazard-chars-break-frontmatter-parsing]]", "[[CLD-C021_kb-edits-do-not-propagate-to-claude-ai-skills]]"]
---

**Capability:** A personal or project skill that is added, edited or removed under `~/.claude/skills/`, a project's `.claude/skills/`, or the `.claude/skills/` of an `--add-dir` directory is picked up inside the running Claude Code session, with no restart, because the harness watches those directories.

**What it unlocks:** Skill work can be sequenced as install, then verify, in ONE session: write the skill, confirm that the harness registered it (the skills listing, then a Skill tool call that renders the body), run its first dry procedure, and only then close. Without this fact a designer would reasonably plan a restart between the install and the verification. That splits the work across two sessions, loses the install context, and pushes the registry check, which is the only check that catches a [[CLD-C001_description-hazard-chars-break-frontmatter-parsing|CLD-C001]] mis-parse, into a session that did not write the file. It also makes skill tuning a cheap loop: edit `SKILL.md`, invoke again, observe.

**Caveats & linked constraints:** Live pickup is not validation. A description that trips [[CLD-C001_description-hazard-chars-break-frontmatter-parsing|CLD-C001]] can still fail to register, or register with frontmatter keys silently lost, so the same-session registry check is the point of the sequence and not a formality. Documented exceptions: bare mode does not watch; a top-level skills directory created after the session started needs a restart (the proof here used a top-level directory that already existed); live detection covers `SKILL.md` text only, and a skill folder that is also a plugin needs `/reload-plugins` for its hooks, MCP config, agents and output styles. Bundled files that the model reads at use time (a reference file, a script) are read fresh by construction; whether anything about them is cached is UNTESTED. Claude Code only: a claude.ai skill is a separate upload and does not follow local edits ([[CLD-C021_kb-edits-do-not-propagate-to-claude-ai-skills|CLD-C021]]). The live proof is one session on the desktop app; the CLI rests on the official doc alone.
