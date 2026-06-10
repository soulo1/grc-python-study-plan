"""
Lesson 5 - Vulnerability Triage Tool
====================================

GRC problem: Your scanner spits out hundreds of findings. Which do you fix
first, and which are breaching your remediation SLA? You need a prioritized,
SLA-aware worklist.

This tool reads a scan export (CSV), assigns a remediation due date from your
SLA policy, and produces a ranked list with OVERDUE items flagged.

Run it:
    python vuln_triage.py                 # uses sample_scan.csv
    python vuln_triage.py myscan.csv

Concepts introduced:
- try/except error handling (bad rows shouldn't crash the run)
- enum (a fixed set of named severities)
- sorting with a key function
- list comprehensions
- date math to compute SLA due dates
"""

import csv
import sys
from datetime import date, datetime, timedelta
from enum import IntEnum


# ---------------------------------------------------------------------------
# Severity as an IntEnum: named values that also sort numerically. Higher =
# more severe, so sorting is easy.
# ---------------------------------------------------------------------------
class Severity(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


# Remediation SLA in days, per severity. Tune to your policy.
SLA_DAYS = {
    Severity.CRITICAL: 7,
    Severity.HIGH: 30,
    Severity.MEDIUM: 90,
    Severity.LOW: 180,
}

TODAY = date(2026, 6, 10)  # pinned for stable demo output; use date.today() live


def parse_severity(text):
    """Map a free-text severity to our Severity enum. Defaults to MEDIUM."""
    return {
        "critical": Severity.CRITICAL,
        "high": Severity.HIGH,
        "medium": Severity.MEDIUM,
        "low": Severity.LOW,
    }.get((text or "").strip().lower(), Severity.MEDIUM)


def parse_date(text):
    return datetime.strptime(text.strip(), "%Y-%m-%d").date()


def triage_row(row):
    """Turn a raw CSV row into an enriched finding dict. Raises on bad data."""
    severity = parse_severity(row["severity"])
    first_seen = parse_date(row["first_seen"])
    due = first_seen + timedelta(days=SLA_DAYS[severity])
    days_to_due = (due - TODAY).days
    return {
        "cve": row["cve"].strip(),
        "host": row["host"].strip(),
        "severity": severity,
        "cvss": float(row.get("cvss", 0) or 0),
        "first_seen": first_seen,
        "due": due,
        "days_to_due": days_to_due,
        "overdue": days_to_due < 0,
        "description": row.get("description", "").strip(),
    }


def load_findings(path):
    findings = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=2):  # start=2: header is line 1
            try:
                findings.append(triage_row(row))
            except (KeyError, ValueError) as e:
                # Don't let one malformed row kill the whole run - log and skip.
                print(f"  [skip] line {i}: could not parse row ({e})")
    return findings


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "sample_scan.csv"
    print("Vulnerability Triage")
    print("=" * 72)
    print(f"Source: {path}   As of: {TODAY}")
    print(f"SLA (days): " + ", ".join(f"{s.name}={d}" for s, d in SLA_DAYS.items()))
    print()

    findings = load_findings(path)

    # Sort: overdue first, then by severity (desc), then by soonest due date.
    findings.sort(key=lambda f: (not f["overdue"], -f["severity"], f["days_to_due"]))

    header = f"{'CVE':<16}{'HOST':<14}{'SEV':<9}{'CVSS':<6}{'DUE':<12}{'STATUS'}"
    print(header)
    print("-" * 72)
    for f in findings:
        if f["overdue"]:
            status = f"OVERDUE by {abs(f['days_to_due'])}d"
        else:
            status = f"due in {f['days_to_due']}d"
        print(f"{f['cve']:<16}{f['host']:<14}{f['severity'].name:<9}"
              f"{f['cvss']:<6}{str(f['due']):<12}{status}")

    # A list comprehension: keep only the overdue findings.
    overdue = [f for f in findings if f["overdue"]]
    crit_open = [f for f in findings if f["severity"] == Severity.CRITICAL]
    print("-" * 72)
    print(f"Total: {len(findings)} | Overdue: {len(overdue)} | "
          f"Critical: {len(crit_open)}")
    if overdue:
        print("Action: overdue items breach SLA - escalate to system owners today.")


if __name__ == "__main__":
    main()
