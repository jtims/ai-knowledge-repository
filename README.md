# AI Knowledge Repository

Two platform knowledge ledgers for AI-assisted engineering, built as a validated knowledge graph: a **Constraints Ledger** of hard, design-invalidating platform facts, and a **Capabilities Ledger** of decision-enabling affordances. Every node is atomic, typed, provenance-backed and validated by a contract linter before it counts.

At this snapshot: 84 nodes across 10 platform entries in 2 ledgers, validator PASS with 0 errors. Constraints: 70 nodes over Claude Code, Lovable, reMarkable, Git, n8n, Python and Atlassian, 69 active and 1 superseded. Capabilities: 14 nodes over Claude Code, reMarkable and Lovable.

## Why it exists

A platform fact that sits in memory is not a fact that gets applied. The founding defect was a design shipped on a backend path that a known platform limitation made impossible; the limitation had been recorded weeks earlier and was still missed at design time. The fix was structural: hard constraints became atomic notes with an admission bar and provenance, a hook injects the relevant platform's nodes into context when a prompt names that platform, and no ledger change counts as done until the validator passes.

## How a node is shaped

Frontmatter carries the identity and the evidence: a monotonic per-platform id, platform, domain, severity or leverage, status, one or more provenance entries with type, ref and date, a verified date, and typed edges to related nodes. The body of a constraint carries three required sections: the constraint itself, its design consequence, and the sanctioned workarounds. A capability carries the inverse shape: what it unlocks, and its caveats and linked constraints. Nodes are never deleted; a wrong node is superseded and linked.

```
Platform Constraints Ledger/
  _SCHEMA-Constraints.md          the contract and id registry
  _MOC-Platform-Constraints.md    the global hub, with a dated changelog
  <Platform>/_<Platform>-Constraints-MOC.md
  <Platform>/constraints/<ID>_<slug>.md
  _tooling/validate-ledger.py     the contract validator for both ledgers
Platform Capabilities Ledger/     the same shape, -CAP ids, _SCHEMA-Capabilities.md
```

## Validate

From the repository root:

```bash
python3 "Platform Constraints Ledger/_tooling/validate-ledger.py" .
```

With no argument the validator checks the repository that contains it; pass a path to check another ledger root. Exit 0 is PASS. The tooling notes for each ledger are in [`Platform Constraints Ledger/_tooling/README.md`](Platform%20Constraints%20Ledger/_tooling/README.md) and [`Platform Capabilities Ledger/_tooling/README.md`](Platform%20Capabilities%20Ledger/_tooling/README.md). The validator checks frontmatter parse, required keys, controlled vocabularies, id-to-filename match, non-empty provenance with type, ref and date on every entry, required body sections, and that every node is listed in its platform hub. An unquoted YAML sequence inside a provenance ref once shipped unnoticed; the validator exists because of that.

## How it is used in a session

- An injection hook adds a platform's constraint nodes to context when a prompt names that platform, so the fact is present at decision time rather than recalled from memory.
- A write hook reports the validator result after any change inside either ledger.
- A skill and two standing protocols govern consult-before-design, cite-the-ids in every proposal, and same-turn capture when a new hard constraint surfaces.

Those hooks and the skill live in the operator's Claude Code configuration, not in this repository. The repository is the knowledge and its validator.

## Provenance

Every node names how it is known: an official doc, a live proof in a session, an owner confirmation, or a vendor page, each with a date. When this public copy was made, locators that pointed at private working sessions were generalized to "owner session" with the date kept; the technical evidence is unchanged. A calibration key on the hub distinguishes VERIFIED, REPORTED, INFERRED, ASSUMED and UNKNOWN.

## What this demonstrates

- Knowledge management built for retrieval at decision time, not storage: injection on demand, atomic nodes, typed edges, hubs.
- Governance as tooling: an admission bar, a contract, a validator that gates "done", supersede-never-delete.
- Platform expertise with receipts: dozens of verified, dated facts about Claude Code, Lovable, Git and reMarkable that changed real designs.
- The graph is the product: ids that never renumber, wikilink edges, and a changelog on every hub, so the ledger can be queried and grown without losing its history.

## License

Creative Commons Attribution 4.0 International (CC BY 4.0). See `LICENSE`. Attribution: jtims, github.com/jtims/ai-knowledge-repository.
