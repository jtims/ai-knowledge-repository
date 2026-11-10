#!/usr/bin/env python3
"""validate-ledger.py — contract lint for the AI Knowledge Repository ledgers.

Validates BOTH the Platform Constraints Ledger and the Platform Capabilities
Ledger against their schemas (`_SCHEMA-Constraints.md` / `_SCHEMA-Capabilities.md`).
One validator, two profiles — the Capabilities Ledger SHARES this control rather
than forking it (single-source-by-construction; `~/.claude/hooks/validate-ledger.py`
is a symlink to this canonical copy).

Usage:
    python3 "Platform Constraints Ledger/_tooling/validate-ledger.py" [<root>]

With no <root>, it validates the repository that contains this script (found
through any symlink to it). <root> may be:
  * the AI Knowledge Repository parent  -> validates EVERY ledger under it (default)
  * a single ledger root                -> validates just that ledger (profile auto-detected)

WHY THIS EXISTS: on 2026-08-06 a newly authored node (CLD-C006) shipped with an
unquoted ': ' inside a provenance `ref`, a YAML syntax error. Nothing checked it,
because the ledger had no validator. A ledger whose nodes silently fail to parse
cannot be an SSOT: the injection hook concatenates raw node text, so a broken node
reaches the model looking authoritative while any tooling that parses it errors or skips it.

Profiles (auto-detected per ledger by its `_SCHEMA-*.md` marker or node subdir):
  constraints   nodes in */constraints/*.md  · MOC `_*-Constraints-MOC.md`
                axis `severity` {design-invalidating|costly|friction}
                body **Constraint:** / **Design consequence:** / **Sanctioned workarounds:**
  capabilities  nodes in */capabilities/*.md · MOC `_*-Capabilities-MOC.md`
                axis `leverage` {unlocks|accelerates|convenience}
                body **Capability:** / **What it unlocks:** / **Caveats & linked constraints:**

Checks (contract from each ledger's `_SCHEMA-*.md`):
  E1  frontmatter missing, or not strict-YAML parseable
  E2  required key missing: id, platform, domain, <axis>, status, provenance, verified, related
  E3  controlled-vocabulary violation (domain / <axis> / status / provenance type)
  E4  `id` does not match the filename prefix
  E5  provenance absent, empty, or an entry missing type/ref/date
  E6  a required body section missing
  E7  node not listed in its platform MOC (link rot — the hub is the entry point)
  W1  `verified` not an ISO date
  W2  a `related` wikilink target does not resolve to a node in EITHER ledger (cross-ledger links OK)
  W3  unquoted ': ' or ' #' in the frontmatter (diagnostic — runs only after a real parse failure)

Exit 0 = PASS (warnings allowed). Exit 1 = FAIL (any error).
v2.0 | 2026-08-10 | Owner: jtims  (generalized to two ledgers; v1.x was constraints-only)
"""
import glob
import os
import re
import sys

try:
    import yaml
except ImportError:
    yaml = None

# The repository that contains this script: <repo>/Platform Constraints Ledger/_tooling/
# realpath follows a ~/.claude/hooks symlink back to the canonical copy.
DEFAULT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

DOMAINS = {"access", "credentials", "deployment", "data", "governance", "cost"}
STATUSES = {"active", "superseded", "retired"}
PROV_TYPES = {"official-doc", "owner-confirmed", "session-verified"}
BASE_REQUIRED = {"id", "platform", "domain", "status", "provenance", "verified", "related"}
ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# Per-ledger contract profile. The constraints profile is byte-identical in
# behaviour to validator v1.x; the capabilities profile is its inverse-polarity twin.
PROFILES = {
    "constraints": {
        "subdir": "constraints",
        "moc_glob": "_*-Constraints-MOC.md",
        "axis": "severity",
        "axis_vocab": {"design-invalidating", "costly", "friction"},
        "body": ["**Constraint:**", "**Design consequence:**", "**Sanctioned workarounds:**"],
    },
    "capabilities": {
        "subdir": "capabilities",
        "moc_glob": "_*-Capabilities-MOC.md",
        "axis": "leverage",
        "axis_vocab": {"unlocks", "accelerates", "convenience"},
        "body": ["**Capability:**", "**What it unlocks:**", "**Caveats & linked constraints:**"],
    },
}


def ledger_profile(d):
    """Return 'constraints' / 'capabilities' / None for a directory that may be a ledger."""
    if os.path.exists(os.path.join(d, "_SCHEMA-Capabilities.md")):
        return "capabilities"
    if os.path.exists(os.path.join(d, "_SCHEMA-Constraints.md")):
        return "constraints"
    if glob.glob(os.path.join(d, "*", "capabilities", "*.md")):
        return "capabilities"
    if glob.glob(os.path.join(d, "*", "constraints", "*.md")):
        return "constraints"
    return None


def discover_ledgers(root):
    """If root is itself a ledger, return [(root, profile)]; else treat it as the
    parent and return every immediate child that is a ledger."""
    p = ledger_profile(root)
    if p:
        return [(root, p)]
    out = []
    for child in sorted(glob.glob(os.path.join(root, "*", ""))):
        child = child.rstrip(os.sep)
        cp = ledger_profile(child)
        if cp:
            out.append((child, cp))
    return out


def validate_ledger(ledger_root, profile, all_stems, findings):
    """Run every node in one ledger through the contract for its profile.
    Returns (node_count, platform_count). Appends (level, code, target, detail) to findings."""
    prof = PROFILES[profile]
    required = BASE_REQUIRED | {prof["axis"]}
    nodes = sorted(glob.glob(os.path.join(ledger_root, "*", prof["subdir"], "*.md")))

    def add(level, code, target, detail):
        findings.append((level, code, target, detail))

    for path in nodes:
        base = os.path.basename(path)
        platform_dir = os.path.basename(os.path.dirname(os.path.dirname(path)))
        text = open(path, encoding="utf-8", errors="replace").read()
        m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if not m:
            add("ERROR", "E1", base, "no YAML frontmatter block")
            continue
        fm, body = m.group(1), text[m.end():]

        if yaml is None:
            continue
        try:
            y = yaml.safe_load(fm)
            if not isinstance(y, dict):
                add("ERROR", "E1", base, "frontmatter is not a mapping")
                continue
        except Exception as exc:
            add("ERROR", "E1", base, "strict-YAML parse failed: %s" % str(exc).split("\n")[0])
            # W3 is DIAGNOSTIC, not detective: it runs only after a real parse failure,
            # to point at the offending line. Scanning unconditionally produced 18 false
            # positives on valid YAML flow mappings (`- {type: x, ref: "y", date: z}`),
            # and a warning class that cries wolf is worse than no warning at all.
            for line in fm.split("\n"):
                if not line.strip() or line.lstrip().startswith("#"):
                    continue
                v = (line.split(":", 1)[1] if ":" in line else "").strip()
                if v and not v.startswith(("'", '"', "[", "{")):
                    if ": " in v:
                        add("WARN", "W3", base, "likely cause — unquoted ': ' in: %s" % line.strip()[:70])
                    if " #" in v:
                        add("WARN", "W3", base, "likely cause — unquoted ' #' in: %s" % line.strip()[:70])
            continue

        missing = required - set(y)
        if missing:
            add("ERROR", "E2", base, "missing key(s): %s" % sorted(missing))

        if y.get("domain") not in DOMAINS:
            add("ERROR", "E3", base, "domain %r not in %s" % (y.get("domain"), sorted(DOMAINS)))
        axis = prof["axis"]
        if y.get(axis) not in prof["axis_vocab"]:
            add("ERROR", "E3", base, "%s %r not in %s" % (axis, y.get(axis), sorted(prof["axis_vocab"])))
        if y.get("status") not in STATUSES:
            add("ERROR", "E3", base, "status %r not in %s" % (y.get("status"), sorted(STATUSES)))

        nid = y.get("id")
        if nid and not base.startswith(str(nid) + "_"):
            add("ERROR", "E4", base, "id %r does not match the filename prefix" % nid)

        prov = y.get("provenance")
        if not isinstance(prov, list) or not prov:
            add("ERROR", "E5", base, "provenance must be a non-empty list")
        else:
            for i, e in enumerate(prov):
                if not isinstance(e, dict):
                    add("ERROR", "E5", base, "provenance[%d] is not a mapping" % i); continue
                for k in ("type", "ref", "date"):
                    if not e.get(k):
                        add("ERROR", "E5", base, "provenance[%d] missing %s" % (i, k))
                if e.get("type") and e["type"] not in PROV_TYPES:
                    add("ERROR", "E3", base, "provenance[%d] type %r not in %s"
                        % (i, e["type"], sorted(PROV_TYPES)))

        for sec in prof["body"]:
            if sec not in body:
                add("ERROR", "E6", base, "body missing section %s" % sec)

        if y.get("verified") is not None and not ISO.match(str(y["verified"])):
            add("WARN", "W1", base, "verified %r is not an ISO date" % y["verified"])

        rel = y.get("related") or []
        if isinstance(rel, list):
            for r in rel:
                tgt = str(r).split("|")[0].strip("[]").strip()
                if tgt and tgt not in all_stems and not tgt.startswith("_"):
                    add("WARN", "W2", base, "related target %r does not resolve" % tgt)

        # E7 — the platform MOC must list this node
        mocs = glob.glob(os.path.join(ledger_root, platform_dir, prof["moc_glob"]))
        if mocs:
            moc = open(mocs[0], encoding="utf-8", errors="replace").read()
            if base[:-3] not in moc:
                add("ERROR", "E7", base, "not listed in %s" % os.path.basename(mocs[0]))
        else:
            add("ERROR", "E7", base, "platform %s has no %s" % (platform_dir, prof["moc_glob"]))

    platforms = len({os.path.basename(os.path.dirname(os.path.dirname(p))) for p in nodes})
    return len(nodes), platforms


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_ROOT
    root = os.path.expanduser(root)
    if not os.path.isdir(root):
        print("ERROR | -- | %s | not a directory" % root)
        return 1

    ledgers = discover_ledgers(root)
    if not ledgers:
        print("ERROR | -- | %s | no ledger found (need a */constraints/ or */capabilities/ "
              "tree or a _SCHEMA-*.md marker)" % root)
        return 1

    # Cross-ledger wikilink resolution: index every node across ALL ledgers under the
    # vault so a capability's `related: [[LOV-C002_...]]` (a constraints node) resolves.
    vault_root = os.path.dirname(ledgers[0][0]) if len(ledgers) == 1 else root
    all_stems = set()
    for sub in ("constraints", "capabilities"):
        for p in glob.glob(os.path.join(vault_root, "**", sub, "*.md"), recursive=True):
            all_stems.add(os.path.basename(p)[:-3])

    findings = []
    counts = []
    for lr, prof in ledgers:
        n, pf = validate_ledger(lr, prof, all_stems, findings)
        counts.append((os.path.basename(lr), prof, n, pf))

    errors = sum(1 for f in findings if f[0] == "ERROR")
    warns = len(findings) - errors
    for level, code, target, detail in findings:
        print("%s | %s | %s | %s" % (level, code, target, detail))
    if yaml is None:
        print("WARN | -- | -- | pyyaml absent; only the W3 raw-text scan ran")
    for name, prof, n, pf in counts:
        print("  · %s [%s]: %d node(s), %d platform(s)" % (name, prof, n, pf))
    total_nodes = sum(c[2] for c in counts)
    total_pf = sum(c[3] for c in counts)
    print("%s | %d node(s) across %d platform(s) in %d ledger(s) | %d error(s), %d warning(s)"
          % ("FAIL" if errors else "PASS", total_nodes, total_pf, len(ledgers), errors, warns))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
