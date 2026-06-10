# Python for GRC — Learn by Building Real Compliance Tools

A hands-on Python curriculum for GRC / security / compliance professionals. You learn
Python by building **14 working automation tools** that solve real Governance, Risk, and
Compliance problems — no prior programming experience required.

Every lesson ends with a script you can run immediately and adapt to your own data.

## Start here
1. Read **[`STUDY_PLAN.md`](STUDY_PLAN.md)** — the full curriculum, lesson by lesson.
2. Do the lessons in order, in `lessons/`. Each folder has its own `README.md` with what's
   new, how to run it, how to use it for real, and exercises.

## Quick setup
```bash
python3 --version                 # need 3.10+ (3.12 recommended)
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt   # only lessons 6, 10, 13 need these

# run your first tool
cd lessons/lesson_01_password_policy && python password_policy_validator.py
```

## The 14 tools you'll build
| # | Tool | Python you learn |
|---|------|------------------|
| 1 | Password Policy Validator | variables, strings, functions, conditionals |
| 2 | User Access Review Helper | lists, loops, reading CSV |
| 3 | Control Framework Mapper | dicts, sets, data modeling |
| 4 | Evidence Collector & Manifest | files, hashing, pathlib |
| 5 | Vulnerability Triage Tool | error handling, sorting, enums |
| 6 | CVE Enrichment (NVD API) | JSON, HTTP APIs, caching |
| 7 | Compliance Expiry Monitor | dates & times |
| 8 | Risk Register Engine | classes & OOP |
| 9 | Log & PII/Secrets Scanner | regular expressions |
| 10 | Compliance Report Generator | third-party libs, Excel |
| 11 | GRC CLI Toolkit | argparse, subprocess, exit codes |
| 12 | Persistent Control Register | SQLite & SQL |
| 13 | Test suite for your tools | pytest |
| 14 | Capstone: Posture Dashboard | integration, reporting |

## Run everything at once (smoke test)
```bash
./run_all.sh        # runs every tool against its bundled sample data
```

## Safety note
These tools touch sensitive data (credentials, PII, vulnerabilities). Never commit real
exports, secrets, or `.env` files. Load API keys from environment variables. Only scan
data and systems you're authorized to access. See the end of `STUDY_PLAN.md` for details.
