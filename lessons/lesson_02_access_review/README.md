# Lesson 2 — User Access Review (UAR) Helper

**New Python concepts:** reading CSV files (`csv.DictReader`), lists, `for` loops,
dictionaries, command-line arguments (`sys.argv`), a first taste of `datetime`.

## Run it
```bash
python access_review.py                 # uses the bundled sample_users.csv
python access_review.py my_export.csv   # point at your own export
```

## Read it
- Each CSV row becomes a **dictionary** (`row["username"]`, `row["status"]`, …).
- `review_account()` returns a list of exception strings — same "return data, don't
  print" pattern as lesson 1.
- `main()` loops over every row, collects findings, and prints a summary.

## Use it for real
Export your user list from your IdP/AD/SaaS app to CSV with columns like:
`username, full_name, role, department, manager, last_login, is_privileged, status`.
Column names don't have to match exactly — adjust the keys in `review_account()` to match
your export's headers. Run it each quarter to generate your UAR exceptions list.

## Exercises
1. **Change the staleness window:** set `STALE_DAYS = 60` and re-run. Which accounts
   newly appear?
2. **Use today's real date:** replace `TODAY = date(2026, 6, 10)` with `date.today()`.
3. **Add a rule:** flag any account whose `role` contains "Contractor" and whose
   `last_login` is older than 30 days (contractors often need tighter review).
4. **Write the output to a CSV** instead of printing, so you can attach it as evidence.
   (Hint: `csv.writer` — and you'll formalize this in lesson 4.)
5. **Count by department:** build a dictionary that tallies how many exceptions each
   department has.

## Checkpoint
- You can read a CSV and access fields by column name.
- You understand the difference between a list (ordered rows) and a dict (named fields).
- You can add a new exception rule.
