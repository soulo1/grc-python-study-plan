# Python for GRC: Learn by Building Real Compliance Tools

A hands-on, project-driven curriculum that teaches you Python by building automation
tools you can use immediately in Governance, Risk, and Compliance (GRC) work. There is
no "toy" code here — every lesson ends with a working script that solves an actual
compliance problem.

## Who this is for

- GRC analysts, security/compliance professionals, and auditors who want to stop doing
  things by hand in spreadsheets.
- You do **not** need any prior programming experience. Lesson 1 starts from zero.
- You **do** need to understand GRC concepts (controls, risk, evidence, access reviews,
  vulnerabilities). That domain knowledge is what makes this fast — you already know
  *what* the tool should do; you're learning *how* to make the computer do it.

## How to use this plan

1. Do the lessons **in order**. Each one introduces 1–3 new Python concepts and reuses
   everything from before.
2. For each lesson:
   - **Read** the "Concepts" section so you know what's new.
   - **Run** the provided tool against the sample data (`python <tool>.py`).
   - **Read the code** top-to-bottom. The code is commented to teach, not just to run.
   - **Do the exercises** at the bottom of each lesson's `README.md`. This is where the
     learning actually happens — modify the tool to fit *your* environment.
   - **Use it for real**: point the tool at your own data (a CSV export, an API, a log
     file). Each lesson explains how.
3. Budget roughly **2–4 hours per lesson**. The whole plan is ~6–8 weeks at a few hours
   a week, or a focused 2–3 weeks full time.

## Setup (one time, ~10 minutes)

```bash
# 1. Confirm you have Python 3.10+ (3.12 recommended)
python3 --version

# 2. From the project root, create an isolated environment
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install the few third-party libraries the later lessons need
pip install -r requirements.txt

# 4. Sanity check — run lesson 1 against its sample data
cd lessons/lesson_01_password_policy
python password_policy_validator.py
```

If lesson 1 prints a report, you're ready.

---

## The progression at a glance

| #  | Python concepts | GRC tool you build | Immediately useful for |
|----|-----------------|--------------------|------------------------|
| 1  | Variables, strings, `if`/`else`, functions, running a script | **Password Policy Validator** | Checking creds against NIST/CIS complexity rules |
| 2  | Lists, loops, reading CSV files | **User Access Review Helper** | Flagging stale/privileged/orphaned accounts |
| 3  | Dictionaries, sets, data modeling | **Control Framework Mapper** | Crosswalking NIST CSF ↔ ISO 27001 ↔ SOC 2 |
| 4  | File I/O, the `pathlib` & `csv` modules, writing reports | **Evidence Collector & Manifest** | Building auditable evidence packages |
| 5  | Error handling, sorting, enumerations | **Vulnerability Triage Tool** | Prioritizing scan findings by CVSS/SLA |
| 6  | JSON, HTTP APIs with `requests` | **CVE Enrichment (NVD API)** | Auto-pulling CVE severity from live data |
| 7  | Dates & times with `datetime` | **Compliance Expiry Monitor** | Tracking cert/policy/access-review due dates |
| 8  | Classes & objects (OOP) | **Risk Register Engine** | Scoring & ranking risks consistently |
| 9  | Regular expressions | **Log & PII/Secrets Scanner** | Detecting exposed secrets/PII in files & logs |
| 10 | Third-party libs, Excel with `openpyxl` | **Compliance Report Generator** | Auditor-ready XLSX status reports |
| 11 | CLI design with `argparse`, packaging | **GRC CLI Toolkit** | Turning your scripts into real commands |
| 12 | Databases with `sqlite3` | **Persistent Control Register** | A queryable system of record |
| 13 | Automated testing with `pytest` | **Test suite for your tools** | Trusting your automation in production |
| 14 | Putting it together | **Capstone: Compliance Dashboard** | A single posture snapshot across all data |

---

## Lesson 1 — Password Policy Validator
**New concepts:** variables, strings, booleans, `if`/`elif`/`else`, functions, `print`,
running a script from the terminal.

**Why this first:** it's the smallest possible *useful* program — pure logic, no files
or libraries — so you can focus on syntax. And every GRC person needs to reason about
password/credential policy.

**What you build:** a script that takes a password (or a list of them) and checks it
against configurable complexity rules (length, upper/lower/digit/symbol, common-password
blocklist) modeled on NIST SP 800-63B and CIS Benchmarks, then prints PASS/FAIL with the
specific reasons it failed.

**Use it immediately:** paste in a proposed standard password, or feed it an exported
list, to validate that your password standard is actually being enforced.

**Run:** `python password_policy_validator.py`

**Exercises** (in the lesson README): add a max-length rule, a "no username inside
password" rule, and make the minimum length a variable at the top of the file.

---

## Lesson 2 — User Access Review Helper
**New concepts:** lists, `for` loops, reading a CSV with the `csv` module, comparing
dates as strings vs. properly (preview of lesson 7).

**What you build:** a tool that reads a CSV export of user accounts (username, role,
last_login, department, is_privileged, status) and flags accounts that violate least-
privilege / access-review policy: stale logins, disabled-but-not-removed, privileged
accounts without justification, and orphaned accounts (no manager/department).

**Use it immediately:** export your IdP / AD / SaaS user list to CSV and run the tool
to produce your quarterly User Access Review (UAR) exceptions list.

**Run:** `python access_review.py` (uses `sample_users.csv`)

---

## Lesson 3 — Control Framework Mapper
**New concepts:** dictionaries, nested data, `sets`, membership tests, helper functions
that return data instead of printing.

**What you build:** a crosswalk tool that maps controls between frameworks (e.g., NIST
CSF subcategory → ISO 27001 Annex A → SOC 2 TSC). Given a control in one framework, it
tells you the equivalent controls in the others, and reports coverage gaps.

**Use it immediately:** when a customer asks "are you ISO 27001 aligned?" and you have a
SOC 2 program, this shows you what you already cover and what's missing.

**Run:** `python control_mapper.py`

---

## Lesson 4 — Evidence Collector & Manifest
**New concepts:** `pathlib`, reading/writing files, hashing with `hashlib`, writing a
CSV/JSON report, timestamps.

**What you build:** a tool that walks an "evidence" folder, records each file's name,
size, SHA-256 hash, and collection time, and produces a tamper-evident manifest
(`evidence_manifest.csv` + `.json`). Auditors love this.

**Use it immediately:** point it at the folder where you drop screenshots/exports for an
audit and generate a manifest proving integrity and collection date.

**Run:** `python evidence_collector.py ./sample_evidence`

---

## Lesson 5 — Vulnerability Triage Tool
**New concepts:** `try`/`except` error handling, sorting with keys, `enum`, list
comprehensions, computing remediation SLAs.

**What you build:** a tool that ingests a vulnerability scan export (CSV from Nessus/
Qualys/etc.), normalizes severity, computes the remediation due date from a configurable
SLA policy (e.g., Critical = 7 days), and outputs a prioritized, overdue-flagged
worklist.

**Use it immediately:** drop in your scanner's CSV export and get a ranked remediation
queue with SLA breaches highlighted.

**Run:** `python vuln_triage.py sample_scan.csv`

---

## Lesson 6 — CVE Enrichment via the NVD API
**New concepts:** JSON, calling a REST API with `requests`, handling rate limits &
network errors, caching responses to disk.

**What you build:** a tool that takes a list of CVE IDs and queries the public NVD API
to pull the official CVSS score, vector, and description, then merges that into your
triage output from lesson 5.

**Use it immediately:** enrich a list of CVEs (from a pen-test report or scan) with
authoritative severity data without manual lookups.

**Run:** `python cve_enrich.py CVE-2021-44228 CVE-2014-0160`
*(works offline against a bundled cache; live mode hits api.nvd.nist.gov)*

---

## Lesson 7 — Compliance Expiry Monitor
**New concepts:** the `datetime` module, date math, timedeltas, formatting dates,
sorting by date.

**What you build:** a tool that reads a list of time-bound compliance obligations
(certificates, policy review dates, vendor reassessments, access reviews, training) and
reports what's expired, what's due soon (configurable window), and what's healthy —
color-coded in the terminal.

**Use it immediately:** never miss a SOC 2 policy annual review or a TLS cert expiry
again. Run it weekly.

**Run:** `python expiry_monitor.py`

---

## Lesson 8 — Risk Register Engine (OOP)
**New concepts:** classes, objects, methods, `__init__`, properties, `@dataclass`,
encapsulating logic.

**What you build:** a `Risk` class with likelihood/impact scoring, an inherent-vs-
residual model, and a `RiskRegister` that loads risks from CSV/JSON, computes scores,
ranks them, and reports the top risks and risk-appetite breaches.

**Use it immediately:** replace your risk spreadsheet's manual scoring with consistent,
repeatable calculations.

**Run:** `python risk_register.py`

---

## Lesson 9 — Log & PII/Secrets Scanner
**New concepts:** regular expressions (`re`), pattern matching, reading large files line
by line, redaction.

**What you build:** a scanner that searches files/logs for exposed secrets (API keys,
AWS keys, private keys) and PII (emails, SSNs, credit-card-like numbers), reports
findings with file/line, and can output a redacted copy.

**Use it immediately:** scan a code export, a log bundle, or a shared drive sample for
data-leak / DLP findings before an audit.

**Run:** `python pii_scanner.py ./sample_logs`

---

## Lesson 10 — Compliance Report Generator (Excel)
**New concepts:** installing & using a third-party library (`openpyxl`), structured
output, styling, multiple sheets.

**What you build:** a tool that takes control status data and produces a polished,
auditor-ready `.xlsx` workbook with a summary sheet, conditional formatting (red/amber/
green), and a per-control detail sheet.

**Use it immediately:** generate your monthly control-status report for leadership or
your auditor in seconds instead of hours.

**Run:** `python report_generator.py` → produces `compliance_report.xlsx`

---

## Lesson 11 — GRC CLI Toolkit
**New concepts:** `argparse`, subcommands, exit codes, structuring a multi-file project,
making scripts reusable.

**What you build:** wrap several earlier tools behind one command, `grc`, with
subcommands: `grc access-review`, `grc triage`, `grc expiry`, `grc scan`. Proper
`--help`, flags, and exit codes so it can run in CI/cron.

**Use it immediately:** a single tool you (and teammates) can run consistently; the
foundation for scheduling automation.

**Run:** `python grc.py --help`

---

## Lesson 12 — Persistent Control Register (SQLite)
**New concepts:** databases, SQL basics, `sqlite3`, CRUD, queries, transactions.

**What you build:** a local database that stores controls, their status, owners, and
evidence links, with functions to add/update/query controls and produce status rollups —
a lightweight system of record that survives between runs.

**Use it immediately:** a queryable home for your control inventory that's more robust
than a spreadsheet and free.

**Run:** `python control_db.py init && python control_db.py report`

---

## Lesson 13 — Testing Your Tools (pytest)
**New concepts:** why testing matters, `pytest`, assertions, fixtures, testing edge
cases, regression tests.

**What you build:** a real test suite for the password validator, vuln triage, and risk
engine — so when you change a rule you know instantly if you broke something.

**Use it immediately:** trust your automation enough to run it unattended. This is the
difference between a script and a *tool*.

**Run:** `pytest -v`

---

## Lesson 14 — Capstone: Compliance Posture Dashboard
**New concepts:** integration — combining modules, generating an HTML/Markdown summary,
orchestration.

**What you build:** a single command that runs the access review, vuln triage, expiry
monitor, and risk register, then assembles a one-page **posture snapshot** (Markdown +
HTML) summarizing open exceptions, overdue items, top risks, and an overall RAG status.

**Use it immediately:** your weekly/monthly "state of compliance" report, fully
automated, ready to schedule.

**Run:** `python dashboard.py`

---

## After the capstone — where to go next

- **Schedule it:** run the dashboard weekly via cron (Linux/Mac) or Task Scheduler
  (Windows), or in CI (GitHub Actions). Lesson 11's exit codes make this clean.
- **Connect real sources:** swap sample CSVs for live API pulls (Okta, AWS Config,
  Jira, your GRC platform). The patterns from lessons 2, 5, and 6 generalize directly.
- **Harden it:** add logging, config files (`.env` / YAML), and more tests.
- **Topics to learn next, in rough order:** virtual environments & dependency pinning →
  `logging` module → working with APIs that need auth (OAuth tokens) → `pandas` for
  heavier data wrangling → packaging your toolkit with `pyproject.toml` → simple web UI
  with FastAPI/Streamlit if you want dashboards in the browser.

## A note on doing this safely

These tools touch sensitive data (credentials, PII, vulnerabilities). As you adapt them
to real data:
- Never commit real exports, secrets, or `.env` files to version control.
- Run the PII/secrets scanner on a copy, and store outputs securely.
- Treat API keys (e.g., NVD) as secrets — load them from environment variables, not code.
- Get authorization before scanning systems or data you don't own.
