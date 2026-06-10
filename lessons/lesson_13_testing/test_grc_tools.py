"""
Lesson 13 - Testing Your Tools (pytest)
=======================================

GRC problem: If you're going to TRUST automation - run it unattended, base
decisions on it, hand its output to an auditor - you need confidence it's
correct and stays correct when you change it. Automated tests give you that.

This file tests three earlier tools: the password validator (L1), the vuln
triage logic (L5), and the risk engine (L8).

Run it (from this folder, or the project root):
    pip install pytest
    pytest -v

Concepts introduced:
- why automated tests matter (regression safety)
- pytest: test functions named test_*, plain `assert`
- testing the happy path AND edge cases
- importing code that lives in sibling lesson folders
"""

import importlib.util
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Helper: load a module from another lesson folder by file path. (Normally
# you'd structure code as an installable package; this keeps lessons standalone.)
# ---------------------------------------------------------------------------
LESSONS = Path(__file__).resolve().parent.parent


def load(rel_path, name):
    spec = importlib.util.spec_from_file_location(name, LESSONS / rel_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


pw = load("lesson_01_password_policy/password_policy_validator.py", "pw")
triage = load("lesson_05_vuln_triage/vuln_triage.py", "triage")
risk = load("lesson_08_risk_register/risk_register.py", "risk")


# ---------------------------------------------------------------------------
# Lesson 1: password policy
# ---------------------------------------------------------------------------
def test_strong_password_passes():
    assert pw.check_password("correct-horse-Battery9!") == []


def test_short_password_fails_on_length():
    failures = pw.check_password("Ab1!")
    assert any("too short" in f for f in failures)


def test_common_password_is_blocked():
    failures = pw.check_password("password")
    assert any("blocklist" in f for f in failures)


def test_missing_character_classes_are_reported():
    failures = pw.check_password("alllowercaseletters")  # long, but no upper/digit/symbol
    assert any("uppercase" in f for f in failures)
    assert any("digit" in f for f in failures)
    assert any("symbol" in f for f in failures)


# ---------------------------------------------------------------------------
# Lesson 5: vuln triage SLA logic
# ---------------------------------------------------------------------------
def test_critical_has_shortest_sla():
    assert triage.SLA_DAYS[triage.Severity.CRITICAL] < triage.SLA_DAYS[triage.Severity.LOW]


def test_overdue_detection():
    row = {
        "cve": "CVE-0000-0001", "host": "h1", "severity": "Critical",
        "cvss": "9.9", "first_seen": "2026-01-01", "description": "test",
    }
    finding = triage.triage_row(row)
    # Critical SLA is 7 days from 2026-01-01, long before the pinned TODAY.
    assert finding["overdue"] is True


def test_unknown_severity_defaults_to_medium():
    assert triage.parse_severity("banana") == triage.Severity.MEDIUM


# ---------------------------------------------------------------------------
# Lesson 8: risk scoring
# ---------------------------------------------------------------------------
def test_inherent_score_is_likelihood_times_impact():
    r = risk.Risk(id="R", title="t", category="c", likelihood=4, impact=5)
    assert r.inherent_score == 20


def test_controls_reduce_residual_score():
    r = risk.Risk(id="R", title="t", category="c", likelihood=4, impact=5,
                  control_effectiveness=0.5)
    assert r.residual_score == 10.0
    assert r.residual_score < r.inherent_score


def test_high_residual_is_above_appetite():
    r = risk.Risk(id="R", title="t", category="c", likelihood=5, impact=5,
                  control_effectiveness=0.0)  # residual 25
    assert r.above_appetite is True


@pytest.mark.parametrize("likelihood,impact,expected_level", [
    (1, 1, "Low"),
    (3, 3, "Medium"),
    (5, 5, "Critical"),
])
def test_levels(likelihood, impact, expected_level):
    r = risk.Risk(id="R", title="t", category="c",
                  likelihood=likelihood, impact=impact)
    assert r.level.value == expected_level
