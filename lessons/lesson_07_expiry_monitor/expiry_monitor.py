"""
Lesson 7 - Compliance Expiry Monitor
====================================

GRC problem: Compliance is full of deadlines - cert expiries, annual policy
reviews, vendor reassessments, access reviews, training. Miss one and you have
an audit finding. You need an early-warning report.

This tool reads time-bound obligations and buckets them into EXPIRED, DUE SOON,
and HEALTHY, sorted by urgency, with colored terminal output.

Run it:
    python expiry_monitor.py                  # uses obligations.csv
    python expiry_monitor.py --window 14      # "due soon" = next 14 days

Concepts introduced:
- the datetime module in depth (date, timedelta, parsing, formatting)
- date arithmetic and comparison
- grouping data into buckets
- ANSI color codes for terminal output
- simple command-line flags
"""

import csv
import sys
from datetime import date, datetime

# Pinned "today" for stable demo output. Switch to date.today() for live use.
TODAY = date(2026, 6, 10)
DEFAULT_WINDOW_DAYS = 30

# ANSI colors so the report is scannable in a terminal.
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
BOLD = "\033[1m"
RESET = "\033[0m"


def parse_date(text):
    return datetime.strptime(text.strip(), "%Y-%m-%d").date()


def classify(due, window_days):
    """Return ('EXPIRED'|'DUE SOON'|'HEALTHY', days_remaining)."""
    days = (due - TODAY).days
    if days < 0:
        return "EXPIRED", days
    if days <= window_days:
        return "DUE SOON", days
    return "HEALTHY", days


def load_obligations(path):
    items = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            items.append({
                "item": row["item"].strip(),
                "type": row["type"].strip(),
                "owner": row["owner"].strip(),
                "due": parse_date(row["due_date"]),
            })
    return items


def get_window():
    """Read an optional --window N flag; default 30 days."""
    args = sys.argv
    if "--window" in args:
        try:
            return int(args[args.index("--window") + 1])
        except (IndexError, ValueError):
            print("  [warn] --window needs a number; using default")
    return DEFAULT_WINDOW_DAYS


def main():
    path = "obligations.csv"
    # Allow a positional filename that isn't the --window value.
    for a in sys.argv[1:]:
        if a.endswith(".csv"):
            path = a
    window = get_window()

    print(f"{BOLD}Compliance Expiry Monitor{RESET}")
    print("=" * 64)
    print(f"As of {TODAY}. 'Due soon' window: {window} days.\n")

    items = load_obligations(path)
    for it in items:
        bucket, days = classify(it["due"], window)
        it["bucket"], it["days"] = bucket, days

    # Sort by days remaining (most negative / soonest first).
    items.sort(key=lambda x: x["days"])

    buckets = {"EXPIRED": RED, "DUE SOON": YELLOW, "HEALTHY": GREEN}
    for bucket, color in buckets.items():
        group = [x for x in items if x["bucket"] == bucket]
        if not group:
            continue
        print(f"{color}{BOLD}{bucket} ({len(group)}){RESET}")
        for x in group:
            if x["days"] < 0:
                when = f"{abs(x['days'])}d ago"
            else:
                when = f"in {x['days']}d"
            print(f"  {color}- {x['due']}  ({when:>9})  {x['item']}"
                  f"  [{x['type']}, owner: {x['owner']}]{RESET}")
        print()

    expired = sum(1 for x in items if x["bucket"] == "EXPIRED")
    soon = sum(1 for x in items if x["bucket"] == "DUE SOON")
    print("-" * 64)
    print(f"{len(items)} obligations | {RED}{expired} expired{RESET} | "
          f"{YELLOW}{soon} due soon{RESET}")
    if expired or soon:
        print("Action: assign owners and dates for expired/soon items now.")


if __name__ == "__main__":
    main()
