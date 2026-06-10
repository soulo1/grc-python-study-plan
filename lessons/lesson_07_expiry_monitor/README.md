# Lesson 7 — Compliance Expiry Monitor

**New Python concepts:** the `datetime` module in depth (parsing, date math,
`timedelta`, comparison, formatting), bucketing data, ANSI terminal colors, simple
CLI flags.

## Run it
```bash
python expiry_monitor.py               # uses obligations.csv, 30-day window
python expiry_monitor.py --window 14   # "due soon" = next 14 days
```
Output is color-coded: red = expired, yellow = due soon, green = healthy.

## Read it
- `classify()` is pure date math: `(due - TODAY).days` tells you how far out something is.
- Items are bucketed and sorted by urgency.
- `get_window()` shows how to read a simple `--window N` flag by hand (lesson 11 does this
  properly with `argparse`).

## Use it for real
Maintain `obligations.csv` (or export it from your GRC tool / a shared sheet) with
columns `item, type, owner, due_date`. Run it weekly — ideally on a schedule (cron / Task
Scheduler) so you get an early warning before anything lapses. Switch `TODAY` to
`date.today()` for live use.

## Exercises
1. **Live date:** change `TODAY` to `date.today()` and confirm the buckets shift.
2. **Per-owner digest:** group obligations by `owner` so each team sees only theirs.
3. **Escalation tiers:** add a "CRITICAL (≤7 days)" bucket above "DUE SOON".
4. **Email/Slack hook (stretch):** instead of printing, format the "expired + due soon"
   list as a message you could send (you'll learn the sending part later).

## Checkpoint
- You're comfortable parsing, comparing, and doing math with dates.
- You can bucket and sort records by a computed value.
