---
id: CLD-C021
platform: Claude Code
domain: deployment
severity: design-invalidating
status: active
provenance:
  - type: owner-confirmed
    ref: "owner statement 2026-08-24, given as 100 percent verified: skills in claude.ai are not controlled by synced-folder changes; the owner must manually update them for changes to take effect. Volunteered as a direct correction to a driver claim that a synced folder skill's description frontmatter is what claude.ai loads at discovery"
    date: 2026-08-24
  - type: session-verified
    ref: "local propagation topology measured 2026-08-24: of 21 skill dirs under ~/.claude/skills/, 12 are DIRECTORY SYMLINKS into the synced skills folder (readlink resolves each into Claude Skills/Personal or Org-agnostic) and 9 are real local directories; validate-agent-roster.py independently counts 21 skills. So a synced folder edit is instantly live for the 12 symlinked skills in Claude Code and has no effect on the 9 forked ones - three different propagation behaviours from one edit, none of which reaches claude.ai"
    date: 2026-08-24
verified: 2026-08-24
related: ["[[CLD-C001_description-hazard-chars-break-frontmatter-parsing]]"]
---

**Constraint:** Editing a skill in the synced skills folder does **not** update that skill on claude.ai. claude.ai skills are refreshed **only** by a manual upload performed by the owner. One folder edit therefore produces three different outcomes at once: it is immediately live in Claude Code for the 12 skills whose local directory is a symlink into the synced folder, it has no effect on the 9 skills that are real local directories (deliberate platform forks, not drift), and it has **no effect at all on claude.ai** until someone uploads the file. Claude Desktop is **UNKNOWN** - it was not verified in either direction and must not be assumed to match claude.ai.

**Design consequence:** A version number is not a deployment. Any design, audit, or drift check that treats the synced folder as the live source for claude.ai is invalid, and the failure is silent and long-lived: claude.ai keeps serving the previous version indefinitely while every local instrument reports the skill as fixed, because in Claude Code it genuinely is. This inverts what a folder version bump means - the bump records that a correction is *available to upload*, not that it is in force. The specific trap is a skill's `description` frontmatter, which is the discovery surface that decides whether a skill loads at all: correcting a stale `description` in the synced folder does nothing for claude.ai, so a session can rewrite the discovery text, watch every local validator pass, and leave the surface that actually reads that field completely unchanged. It follows that **a session which bumps a synced folder skill version owes the owner an explicit re-upload list**, and that a version table which is correct in the synced folder and stale on claude.ai is worse than no version table, because it reads as authoritative for both.

**Sanctioned workarounds:** (1) End any session that touches a synced-folder skill with an explicit per-skill re-upload list for claude.ai, naming the file and the new version - the owner cannot act on "skills were updated". (2) State the propagation class whenever a skill is edited: symlinked-into-synced folder (live in Claude Code immediately), real local directory (Claude Code only, synced folder untouched), or synced folder-only (nothing live anywhere until uploaded). (3) Never cite a synced folder version as evidence of claude.ai behaviour, and never diagnose a claude.ai skill problem from the synced folder file - fetch or inspect what claude.ai actually holds. (4) Treat Claude Desktop and Cowork as separate distribution channels with their own propagation rules; Cowork needs a `.skill` repackage, and Desktop is UNKNOWN pending verification. (5) `/drift-audit` compares skill versions across synced folder, Claude Code and claude.ai precisely because these three can disagree; run it rather than assuming they agree. (6) The reverse direction is also unverified: whether a claude.ai-side edit can be exported back to the synced folder is **UNKNOWN**, so treat the synced folder as the authoring surface and claude.ai as a publish target, never as a two-way sync.
