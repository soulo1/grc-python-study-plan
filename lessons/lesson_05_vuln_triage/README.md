# Lesson 5 — Vulnerability Triage Tool

**New Python concepts:** `try`/`except` error handling, `enum.IntEnum`, sorting with a
`key` function and `lambda`, list comprehensions, date math (`timedelta`).

## Run it
```bash
python vuln_triage.py              # uses sample_scan.csv
python vuln_triage.py myscan.csv   # your scanner's export
```

## Read it
- `Severity(IntEnum)` gives you named severities that also **sort numerically**.
- `SLA_DAYS` encodes your remediation policy; `triage_row()` computes each finding's due
  date and whether it's overdue.
- The sort key `lambda f: (not f["overdue"], -f["severity"], f["days_to_due"])` puts
  overdue + most-severe + soonest-due at the top.
- `try`/`except` means one malformed row is skipped (with a note) instead of crashing the
  whole report — essential for messy real-world exports.

## Use it for real
Export findings from Nessus/Qualys/OpenVAS/Defender to CSV. Map your columns to
`cve, host, severity, cvss, first_seen, description` (or edit the keys in `triage_row()`).
Run it to get a ranked, SLA-aware remediation worklist.

## Exercises
1. **Change the SLA:** make Critical 3 days. Who becomes overdue?
2. **Group by host:** print a per-host count of open findings, sorted worst-first.
3. **Export the worklist** to a new CSV (`triage_output.csv`) for your ticketing system.
4. **Asset weighting:** add an asset-criticality column and bump priority for crown-jewel
   hosts even at lower severity.

## Checkpoint
- You can sort complex records by multiple keys.
- You can write defensive code that survives bad input rows.
