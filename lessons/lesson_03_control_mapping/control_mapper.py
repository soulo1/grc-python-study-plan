"""
Lesson 3 - Control Framework Mapper
===================================

GRC problem: You run a SOC 2 program but a customer asks about ISO 27001 and
NIST CSF. You need a crosswalk: "what we already do covers which controls in
the other frameworks, and where are the gaps?"

This tool models a control crosswalk as Python dictionaries and answers those
questions.

Run it:
    python control_mapper.py

Concepts introduced:
- dictionaries (key -> value) and nested dictionaries
- lists inside dictionaries
- sets and set operations (to compute coverage gaps)
- functions that return data structures
- iterating over dict items
"""

# ---------------------------------------------------------------------------
# A small crosswalk. Each entry is keyed by a NIST CSF subcategory and maps to
# the equivalent ISO 27001:2022 Annex A controls and SOC 2 Trust Services
# Criteria. This is illustrative - extend it with your real mappings.
# ---------------------------------------------------------------------------
CROSSWALK = {
    "PR.AC-1 (Identity & credential management)": {
        "iso27001": ["A.5.16 Identity management", "A.5.17 Authentication info"],
        "soc2": ["CC6.1", "CC6.2", "CC6.3"],
        "description": "Identities and credentials are issued, managed, and revoked.",
    },
    "PR.AC-4 (Least privilege / access permissions)": {
        "iso27001": ["A.5.15 Access control", "A.8.2 Privileged access rights"],
        "soc2": ["CC6.1", "CC6.3"],
        "description": "Access permissions follow least privilege and separation of duties.",
    },
    "PR.DS-1 (Data-at-rest protection)": {
        "iso27001": ["A.8.24 Use of cryptography"],
        "soc2": ["CC6.1", "C1.1"],
        "description": "Data at rest is protected (e.g., encryption).",
    },
    "DE.CM-1 (Network monitoring)": {
        "iso27001": ["A.8.16 Monitoring activities"],
        "soc2": ["CC7.2"],
        "description": "Networks and systems are monitored to detect events.",
    },
    "RS.RP-1 (Incident response plan)": {
        "iso27001": ["A.5.24 Incident management planning"],
        "soc2": ["CC7.3", "CC7.4"],
        "description": "An incident response plan is executed during/after an incident.",
    },
}


def lookup(csf_id):
    """Return the crosswalk entry for a NIST CSF subcategory, or None."""
    return CROSSWALK.get(csf_id)


def all_soc2_criteria_covered():
    """Return the SET of SOC 2 criteria referenced anywhere in the crosswalk."""
    covered = set()
    for entry in CROSSWALK.values():
        for criterion in entry["soc2"]:
            covered.add(criterion)
    return covered


def coverage_gap(required_soc2):
    """Given the SOC 2 criteria you are *required* to meet, return the set you
    do NOT yet have a mapped control for. This is a set difference."""
    have = all_soc2_criteria_covered()
    need = set(required_soc2)
    return need - have   # items in `need` that are missing from `have`


def print_crosswalk():
    print("Control Framework Crosswalk (NIST CSF -> ISO 27001 / SOC 2)")
    print("=" * 64)
    for csf_id, entry in CROSSWALK.items():
        print(f"\nNIST CSF: {csf_id}")
        print(f"  what:  {entry['description']}")
        print(f"  ISO 27001: {', '.join(entry['iso27001'])}")
        print(f"  SOC 2 TSC: {', '.join(entry['soc2'])}")


def main():
    print_crosswalk()

    print("\n" + "=" * 64)
    print("Coverage analysis")
    print("-" * 64)

    covered = all_soc2_criteria_covered()
    print(f"SOC 2 criteria currently mapped: {sorted(covered)}")

    # Pretend your auditor requires these SOC 2 criteria:
    required = ["CC6.1", "CC6.2", "CC6.3", "CC7.1", "CC7.2", "CC7.3", "CC7.4", "CC8.1"]
    gaps = coverage_gap(required)
    print(f"Required by audit scope:        {sorted(required)}")
    if gaps:
        print(f"\nGAPS (no mapped control yet):   {sorted(gaps)}")
        print("Action: add controls/mappings for these before your audit.")
    else:
        print("\nNo gaps - every required criterion has a mapped control.")

    # Example lookup
    print("\n" + "-" * 64)
    target = "PR.AC-4 (Least privilege / access permissions)"
    entry = lookup(target)
    print(f"Lookup '{target}':")
    print(f"  -> ISO 27001: {entry['iso27001']}")
    print(f"  -> SOC 2:     {entry['soc2']}")


if __name__ == "__main__":
    main()
