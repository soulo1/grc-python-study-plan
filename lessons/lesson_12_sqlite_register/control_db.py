"""
Lesson 12 - Persistent Control Register (SQLite)
===============================================

GRC problem: Spreadsheets get copied, diverge, and lose history. A small
database gives you a single, queryable system of record for your controls that
persists between runs - with no server to install (SQLite is built into Python).

This tool creates a local controls.db and lets you add/update/query controls.

Run it:
    python control_db.py init       # create the DB and seed sample controls
    python control_db.py list       # list all controls
    python control_db.py report     # status rollup
    python control_db.py set CC6.3 Effective   # update a control's status

Concepts introduced:
- relational databases and basic SQL (CREATE, INSERT, UPDATE, SELECT)
- the built-in sqlite3 module
- parameterized queries (?) to avoid SQL injection
- transactions (commit)
- a tiny command dispatcher
"""

import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(__file__).parent / "controls.db"

SEED = [
    ("CC6.1", "Logical access controls", "SOC 2", "IT Security", "Effective"),
    ("CC6.3", "Least privilege", "SOC 2", "IT Security", "Needs Improvement"),
    ("CC7.2", "System monitoring", "SOC 2", "SecOps", "Effective"),
    ("CC7.3", "Incident evaluation", "SOC 2", "SecOps", "Not Tested"),
    ("CC8.1", "Change management", "SOC 2", "Engineering", "Needs Improvement"),
    ("A.8.24", "Cryptography", "ISO 27001", "Platform", "Not Tested"),
]


def connect():
    """Open a connection. Rows behave like dicts via row_factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init():
    conn = connect()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS controls (
            control_id  TEXT PRIMARY KEY,
            name        TEXT NOT NULL,
            framework   TEXT NOT NULL,
            owner       TEXT,
            status      TEXT NOT NULL DEFAULT 'Not Tested',
            updated_at  TEXT DEFAULT (datetime('now'))
        )
    """)
    # INSERT OR IGNORE so re-running init() doesn't duplicate rows.
    conn.executemany(
        "INSERT OR IGNORE INTO controls "
        "(control_id, name, framework, owner, status) VALUES (?, ?, ?, ?, ?)",
        SEED,
    )
    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM controls").fetchone()[0]
    conn.close()
    print(f"Initialized {DB_PATH.name} with {count} controls.")


def list_controls():
    conn = connect()
    rows = conn.execute(
        "SELECT control_id, name, framework, owner, status "
        "FROM controls ORDER BY framework, control_id"
    ).fetchall()
    conn.close()
    print(f"{'ID':<9}{'FRAMEWORK':<12}{'OWNER':<14}{'STATUS':<20}{'NAME'}")
    print("-" * 72)
    for r in rows:
        print(f"{r['control_id']:<9}{r['framework']:<12}{r['owner'] or '-':<14}"
              f"{r['status']:<20}{r['name']}")


def set_status(control_id, status):
    conn = connect()
    # Parameterized query (?) - never build SQL with string formatting.
    cur = conn.execute(
        "UPDATE controls SET status = ?, updated_at = datetime('now') "
        "WHERE control_id = ?",
        (status, control_id),
    )
    conn.commit()
    conn.close()
    if cur.rowcount:
        print(f"Updated {control_id} -> {status}")
    else:
        print(f"No control with id {control_id}. Try 'list'.")


def report():
    conn = connect()
    rows = conn.execute(
        "SELECT status, COUNT(*) AS n FROM controls GROUP BY status ORDER BY n DESC"
    ).fetchall()
    total = conn.execute("SELECT COUNT(*) FROM controls").fetchone()[0]
    conn.close()
    print("Control Status Rollup")
    print("=" * 40)
    for r in rows:
        pct = r["n"] / total * 100 if total else 0
        print(f"  {r['status']:<20} {r['n']:>3}  ({pct:.0f}%)")
    print("-" * 40)
    print(f"  {'TOTAL':<20} {total:>3}")


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return
    cmd = args[0]
    if cmd == "init":
        init()
    elif cmd == "list":
        list_controls()
    elif cmd == "report":
        report()
    elif cmd == "set" and len(args) >= 3:
        set_status(args[1], " ".join(args[2:]))
    else:
        print("Usage: init | list | report | set <control_id> <status>")


if __name__ == "__main__":
    main()
