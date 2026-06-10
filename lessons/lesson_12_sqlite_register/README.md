# Lesson 12 — Persistent Control Register (SQLite)

**New Python concepts:** relational databases and basic SQL (`CREATE`, `INSERT`,
`UPDATE`, `SELECT`, `GROUP BY`), the built-in `sqlite3` module, **parameterized queries**
(`?`) to prevent SQL injection, transactions (`commit`).

## Run it
```bash
python control_db.py init                 # create controls.db + seed data
python control_db.py list                 # list all controls
python control_db.py report               # status rollup
python control_db.py set CC6.3 Effective  # update a control's status
python control_db.py report               # see the rollup change & persist
```
Run `report` again in a fresh process — the change persisted, because it's in a database,
not memory. (`controls.db` is created locally and is git-ignored.)

## Read it
- `CREATE TABLE IF NOT EXISTS` defines the schema; `INSERT OR IGNORE` makes `init`
  idempotent.
- **Always** use parameterized queries: `execute("... WHERE control_id = ?", (id,))` —
  never f-string user input into SQL. This is the #1 web-app vulnerability (injection).
- `report()` uses `GROUP BY` to roll up counts by status — SQL doing the aggregation for
  you.

## Use it for real
This is a lightweight, free system of record for your control inventory that's more
robust than a spreadsheet and easy to query. You can point lesson 10's Excel generator at
a SQL query instead of a CSV.

## Exercises
1. **History table:** add a `control_history` table and record every status change with a
   timestamp — instant audit trail.
2. **Evidence links:** add an `evidence_url` column and a `link` command.
3. **Query by owner:** add `python control_db.py owner "SecOps"`.
4. **Import:** load `lesson_10`'s `controls_status.csv` into the DB.

## Checkpoint
- You can create a table, insert/update/query rows, and aggregate with SQL.
- You understand why parameterized queries matter for security.
