"""
Lesson 2 - User Access Review (UAR) Helper
===========================================

GRC problem: Every quarter you must review who has access to what and flag
violations of least-privilege and joiner/mover/leaver hygiene. Doing this by
eye in a spreadsheet is slow and error-prone.

This tool reads a CSV export of accounts and flags exceptions automatically.

Run it:
    python access_review.py                 # uses sample_users.csv
    python access_review.py my_export.csv   # your own export

Concepts introduced:
- reading a CSV with the built-in `csv` module
- lists and `for` loops
- dictionaries (each CSV row becomes a dict keyed by column name)
- the datetime module (a first taste; lesson 7 goes deep)
- accumulating results in a list
"""

import csv
import sys
from datetime import date, datetime

# ---------------------------------------------------------------------------
# POLICY CONFIG - tune these to your environment's access-review policy.
# ---------------------------------------------------------------------------
STALE_DAYS = 60            # accounts not used in this many days are "stale"
TODAY = date.today()  # pinned so sample output is stable; use date.today() live


def parse_date(text):
    """Turn '2026-06-08' into a date object. Returns None if blank/invalid."""
    text = (text or "").strip()
    if not text:
        return None
    try:
        return datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError:
        return None


def days_since(d):
    """How many days ago was date d? None-safe."""
    if d is None:
        return None
    return (TODAY - d).days


def review_account(row):
    """Return a list of policy-exception strings for a single account row."""
    findings = []

    username = row.get("username", "").strip()
    status = row.get("status", "").strip().lower()
    is_privileged = row.get("is_privileged", "").strip().lower() == "true"
    manager = row.get("manager", "").strip()
    role = row.get("role", "").strip()
    last_login = parse_date(row.get("last_login", ""))
    age = days_since(last_login)

    # 1) Stale active accounts (possible leaver who wasn't deprovisioned)
    if status == "active" and age is not None and age > STALE_DAYS:
        findings.append(f"STALE: active but no login in {age} days (> {STALE_DAYS})")

    # 2) Disabled accounts still present (should be removed after grace period)
    if status == "disabled":
        findings.append("CLEANUP: account disabled but not yet removed")

    # 3) Privileged accounts must have an assigned manager/owner for accountability
    if is_privileged and not manager:
        findings.append("OWNERSHIP: privileged account has no manager/owner assigned")

    # 4) Orphaned accounts (no manager AND not a service account)
    if not manager and "service" not in role.lower():
        findings.append("ORPHAN: no manager and not flagged as a service account")

    # 5) Privileged + stale is a high-priority combination
    if is_privileged and age is not None and age > STALE_DAYS:
        findings.append(f"HIGH RISK: privileged AND stale ({age} days)")
    
    #6) Flag any account whose role contains "Contractor" and 30+ days since last login
    if "Contractor" in role:
        findings.append(f"contractors require tighter review")

    return username, findings


def main():
    # sys.argv lets a user pass a filename: python access_review.py file.csv
    path = sys.argv[1] if len(sys.argv) > 1 else "soulo_sample_users.csv"

    print("User Access Review Helper")
    print("=" * 50)
    print(f"Source: {path}   As of: {TODAY}   Stale threshold: {STALE_DAYS} days\n")

    total = 0
    flagged = 0

    # csv.DictReader turns each row into a dict like {"username": "asmith", ...}
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            username, findings = review_account(row)
            if findings:
                flagged += 1
                print(f"[!] {username}")
                for finding in findings:
                    print(f"      - {finding}")

    print("\n" + "-" * 50)
    print(f"Reviewed {total} accounts. {flagged} have exceptions, "
          f"{total - flagged} are clean.")
    if flagged:
        print("Action: review each flagged account with its owner and document a"
              " decision (keep / modify / remove).")


if __name__ == "__main__":
    main()
