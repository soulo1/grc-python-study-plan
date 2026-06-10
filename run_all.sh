#!/usr/bin/env bash
# Smoke test: run every lesson's tool against its bundled sample data.
# Useful to confirm your environment is set up. Run from the project root.
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="${PYTHON:-python3}"

run() {
  echo ""
  echo "######################################################################"
  echo "# $1"
  echo "######################################################################"
  ( cd "$ROOT/$2" && shift 2 && "$PY" "$@" )
}

run "Lesson 1 - Password Policy Validator" lessons/lesson_01_password_policy password_policy_validator.py
run "Lesson 2 - Access Review"             lessons/lesson_02_access_review access_review.py
run "Lesson 3 - Control Mapper"            lessons/lesson_03_control_mapping control_mapper.py
run "Lesson 4 - Evidence Collector"        lessons/lesson_04_evidence_collector evidence_collector.py
run "Lesson 5 - Vuln Triage"               lessons/lesson_05_vuln_triage vuln_triage.py
run "Lesson 6 - CVE Enrichment (offline)"  lessons/lesson_06_nvd_api cve_enrich.py
run "Lesson 7 - Expiry Monitor"            lessons/lesson_07_expiry_monitor expiry_monitor.py
run "Lesson 8 - Risk Register"             lessons/lesson_08_risk_register risk_register.py
run "Lesson 9 - PII/Secrets Scanner"       lessons/lesson_09_log_pii_scanner pii_scanner.py
run "Lesson 10 - Excel Report"             lessons/lesson_10_excel_report report_generator.py
run "Lesson 11 - CLI Toolkit (--help)"     lessons/lesson_11_cli_toolkit grc.py --help
run "Lesson 12 - SQLite Register"          lessons/lesson_12_sqlite_register control_db.py init
run "Lesson 12 - SQLite Register (report)" lessons/lesson_12_sqlite_register control_db.py report
run "Lesson 14 - Capstone Dashboard"       lessons/lesson_14_capstone_dashboard dashboard.py

echo ""
echo "######################################################################"
echo "# Lesson 13 - pytest"
echo "######################################################################"
( cd "$ROOT" && "$PY" -m pytest lessons/lesson_13_testing -q )

echo ""
echo "All lessons executed. Review output above for any errors."
