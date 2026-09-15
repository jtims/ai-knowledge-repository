---
id: CLD-CAP006
platform: Claude Code
domain: data
leverage: unlocks
status: active
provenance:
  - type: session-verified
    ref: "live 2026-09-03 - read from the shipped 2.1.235 Mach-O. The auto-memory settings chain is Qob() at 277,089,337: function Qob(){let e=Aje(),t=cn('policySettings')?.autoMemoryDirectory??cn('flagSettings')?.autoMemoryDirectory??(e?cn('localSettings')?.autoMemoryDirectory??cn('projectSettings')?.autoMemoryDirectory:undefined)??cn('userSettings')?.autoMemoryDirectory;return N0d(t,true)}. The project and local scopes are consulted only when Aje() is truthy, and userSettings sits at the BOTTOM of the chain"
    date: 2026-09-03
  - type: session-verified
    ref: "live 2026-09-03 - the gate resolved. Aje() at 277,119,179 is function Aje(){if(Rn())return true;return Mf()}. Rn() at 273,946,596 is function Rn(){return !fr.host.launchOptions.isInteractive()}. Mf() at 277,119,086 is function Mf(){if(As.trustAccepted)return true;let e=Cib();if(e)As.setTrustAccepted(true);return e}. So Aje() is true whenever the run is NON-INTERACTIVE, independently of trust, and otherwise true only once the trust dialog has been accepted"
    date: 2026-09-03
  - type: session-verified
    ref: "live 2026-09-03 - behavioural confirmation of the precedence half, by an independent path. With a user-scope autoMemoryDirectory pinned, a resolver replicating Qob() and run from a vault project root still returned the PROJECT store and named projectSettings as the branch (fixture F4b); run from a subdirectory of the same project it returned the user-scope pin (fixture F4). 10 fixtures, 0 failures"
    date: 2026-09-03
verified: 2026-09-03
related: ["[[CLD-CAP003_automemorydirectory-redirects-store-from-subdir]]", "[[CLD-C016_auto-memory-keys-one-store-per-repo-root]]", "[[CLD-C028_project-key-resolution-is-not-single-valued]]", "[[CLD-C027_on-demand-memory-recall-is-remotely-feature-gated]]"]
---

**Capability:** A project-scope `autoMemoryDirectory` redirect **is consulted in non-interactive runs unconditionally**, including headless, print-mode (`-p`) and SDK runs, because the gate that admits project and local settings into the auto-memory chain is `Aje() = !isInteractive() || trustAccepted`, and the non-interactive branch alone satisfies it. A headless run does not need the trust dialog to have been accepted for its project redirect to be honoured. Separately, `userSettings` occupies the **last** position in that chain, so a user-scope pin can never outrank a project-scope redirect.

**What it unlocks:** Two designs that would otherwise be ruled out. First, per-project memory isolation can be relied on **inside automation** - swarm workers, dynamic workflows, cron and SDK runs - rather than only in interactive sessions launched from the project directory. Without this fact you would assume automated runs fall back to the repo-derived store and would either abandon the tiered architecture for automation or build a redundant environment-variable mechanism to carry it. Second, a user-scope `autoMemoryDirectory` pin becomes **safe to add** as a defensive default: it protects the shared store against changes in git topology, which is what otherwise re-keys it, while remaining inert in every directory that carries its own project-scope redirect. That combination - pin the shared default at the bottom of the chain, let project scope win above it - is only available because the precedence order runs in that direction.

**Caveats & linked constraints:** This settles the **precedence** half of the question and not the **loading** half. `--setting-sources` governs whether `cn("projectSettings")` is populated at all, which sits upstream of `Qob()` and is **NOT** answered by this chain; a run that excludes the `project` source has no project settings to consult regardless of `Aje()`. Two further paths outrank the whole chain: `CLAUDE_COWORK_MEMORY_PATH_OVERRIDE` is checked before it, and `policySettings` plus `flagSettings` sit above project scope, so a managed policy or a CLI flag still wins. The store resolver memoizes on the composite key `Va()|Aje()`, so a value observed under one gate state does not establish the value under another. Governing constraints - [[CLD-C028_project-key-resolution-is-not-single-valued]] (three disagreeing key resolvers, so any report of a resolved store must name its branch) and [[CLD-C027_on-demand-memory-recall-is-remotely-feature-gated]] (with recall gated off, a redirected store's `MEMORY.md` index is its only automatic surfacing channel, which is what makes getting the redirect right in automation matter at all).
