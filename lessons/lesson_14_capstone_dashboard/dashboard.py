"""
Lesson 14 - Capstone: Compliance Posture Dashboard
==================================================

GRC problem: Leadership wants a single, regular "state of compliance" snapshot
- not five separate tool outputs. This capstone ORCHESTRATES the earlier tools
and assembles a one-page posture report in Markdown and HTML.

This ties together everything: file I/O, dicts, classes, dates, functions, and
integrating modules.

Run it:
    python dashboard.py
    -> writes posture.md and posture.html

Concepts introduced / reinforced:
- integrating multiple modules into one program
- reusing the logic you already wrote (don't repeat yourself)
- generating Markdown and HTML output
- summarizing data into a single RAG (red/amber/green) status
"""

import importlib.util
from datetime import date
from pathlib import Path

LESSONS = Path(__file__).resolve().parent.parent
OUT_DIR = Path(__file__).resolve().parent


def load(rel_path, name):
    spec = importlib.util.spec_from_file_location(name, LESSONS / rel_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Reuse the real logic from earlier lessons.
access = load("lesson_02_access_review/access_review.py", "access")
triage = load("lesson_05_vuln_triage/vuln_triage.py", "triage")
expiry = load("lesson_07_expiry_monitor/expiry_monitor.py", "expiry")
risk = load("lesson_08_risk_register/risk_register.py", "risk")

import csv  # noqa: E402  (after dynamic imports for clarity)


# ---------------------------------------------------------------------------
# Each gather_* function returns a small summary dict for one domain.
# ---------------------------------------------------------------------------
def gather_access():
    path = LESSONS / "lesson_02_access_review/sample_users.csv"
    flagged = 0
    total = 0
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            total += 1
            _user, findings = access.review_account(row)
            if findings:
                flagged += 1
    return {"name": "User Access", "total": total, "issues": flagged}


def gather_vulns():
    path = LESSONS / "lesson_05_vuln_triage/sample_scan.csv"
    findings = triage.load_findings(str(path))
    overdue = [f for f in findings if f["overdue"]]
    return {"name": "Vulnerabilities", "total": len(findings), "issues": len(overdue)}


def gather_expiry():
    path = LESSONS / "lesson_07_expiry_monitor/obligations.csv"
    items = expiry.load_obligations(str(path))
    overdue = 0
    soon = 0
    for it in items:
        bucket, _ = expiry.classify(it["due"], expiry.DEFAULT_WINDOW_DAYS)
        if bucket == "EXPIRED":
            overdue += 1
        elif bucket == "DUE SOON":
            soon += 1
    return {"name": "Compliance Calendar", "total": len(items),
            "issues": overdue + soon, "expired": overdue, "soon": soon}


def gather_risk():
    path = LESSONS / "lesson_08_risk_register/risks.csv"
    register = risk.RiskRegister.from_csv(str(path))
    over = register.above_appetite()
    top = register.ranked()[:3]
    return {"name": "Risk Register", "total": len(register.risks),
            "issues": len(over),
            "top": [(r.id, r.title, r.residual_score, r.level.value) for r in top]}


def overall_rag(domains):
    """Roll the domains up into one Red/Amber/Green status."""
    total_issues = sum(d["issues"] for d in domains)
    if total_issues == 0:
        return "GREEN"
    if total_issues <= 5:
        return "AMBER"
    return "RED"


def build_markdown(domains, rag):
    today = date.today().isoformat()
    lines = [
        f"# Compliance Posture Snapshot — {today}",
        "",
        f"**Overall status: {rag}**",
        "",
        "| Domain | Items reviewed | Open issues |",
        "|--------|---------------:|------------:|",
    ]
    for d in domains:
        lines.append(f"| {d['name']} | {d['total']} | {d['issues']} |")
    lines.append("")

    # Highlights
    cal = next(d for d in domains if d["name"] == "Compliance Calendar")
    lines += [
        "## Highlights",
        f"- **{cal['expired']}** obligations expired, **{cal['soon']}** due soon.",
    ]
    risk_dom = next(d for d in domains if d["name"] == "Risk Register")
    lines.append(f"- **{risk_dom['issues']}** risk(s) above appetite.")
    lines.append("")
    lines.append("### Top risks")
    for rid, title, score, level in risk_dom["top"]:
        lines.append(f"- `{rid}` {title} — residual **{score}** ({level})")
    lines.append("")
    lines.append("_Generated automatically by the GRC Python toolkit (lesson 14)._")
    return "\n".join(lines)


def build_html(markdown_text, rag):
    color = {"GREEN": "#2e7d32", "AMBER": "#f9a825", "RED": "#c62828"}[rag]
    # Minimal conversion: wrap the markdown in <pre> plus a colored banner.
    # (A real tool would use the `markdown` library; we keep dependencies light.)
    body = markdown_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Compliance Posture</title>
<style>
 body {{ font-family: system-ui, sans-serif; margin: 2rem; color: #222; }}
 .banner {{ background: {color}; color: white; padding: 1rem; border-radius: 8px;
            font-size: 1.4rem; font-weight: bold; }}
 pre {{ background: #f5f5f5; padding: 1rem; border-radius: 8px; white-space: pre-wrap; }}
</style></head>
<body>
 <div class="banner">Overall compliance status: {rag}</div>
 <pre>{body}</pre>
</body></html>"""


def main():
    print("Compliance Posture Dashboard")
    print("=" * 50)
    domains = [gather_access(), gather_vulns(), gather_expiry(), gather_risk()]
    rag = overall_rag(domains)

    for d in domains:
        print(f"  {d['name']:<22} {d['issues']} issue(s) / {d['total']} reviewed")
    print(f"\n  OVERALL: {rag}")

    md = build_markdown(domains, rag)
    (OUT_DIR / "posture.md").write_text(md, encoding="utf-8")
    (OUT_DIR / "posture.html").write_text(build_html(md, rag), encoding="utf-8")

    print("-" * 50)
    print(f"Wrote {OUT_DIR / 'posture.md'}")
    print(f"Wrote {OUT_DIR / 'posture.html'}  (open in a browser)")
    print("Schedule this weekly for an automated state-of-compliance report.")


if __name__ == "__main__":
    main()
