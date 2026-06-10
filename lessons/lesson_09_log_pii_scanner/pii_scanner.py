"""
Lesson 9 - Log & PII/Secrets Scanner
====================================

GRC problem: Secrets and PII leak into logs, config files, and code. Before an
audit (or a breach) you want to find exposed AWS keys, API tokens, emails,
SSNs, and credit-card-like numbers - and be able to produce a redacted copy.

This tool scans files for sensitive patterns using regular expressions.

Run it:
    python pii_scanner.py                       # scans ./sample_logs
    python pii_scanner.py /path/to/folder
    python pii_scanner.py ./sample_logs --redact # also write *.redacted copies

Concepts introduced:
- regular expressions (the `re` module): the core skill for text/log analysis
- compiling patterns, named groups, finditer
- reading files line by line (memory-friendly for big logs)
- a dictionary of detectors
- redaction (replacing matches with ****)
"""

import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Detectors: a name -> compiled regex. Add your own organization's patterns.
# These are intentionally simple/illustrative; tune for your real data.
# ---------------------------------------------------------------------------
DETECTORS = {
    "AWS Access Key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "Generic API token": re.compile(r"\b(?:sk|pk|rk)_(?:live|test)_[0-9A-Za-z]{16,}\b"),
    "Private key header": re.compile(r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----"),
    "Password assignment": re.compile(r"(?i)\bpassword\s*[=:]\s*\S+"),
    "Email address": re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"),
    "US SSN": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "Credit-card-like": re.compile(r"\b(?:\d[ -]*?){13,16}\b"),
}

# Severity hint per detector (for sorting/triage).
SEVERITY = {
    "AWS Access Key": "CRITICAL",
    "Generic API token": "CRITICAL",
    "Private key header": "CRITICAL",
    "Password assignment": "HIGH",
    "US SSN": "HIGH",
    "Credit-card-like": "HIGH",
    "Email address": "LOW",
}


def scan_text(text):
    """Yield (detector_name, matched_string, start, end) for every match."""
    for name, pattern in DETECTORS.items():
        for m in pattern.finditer(text):
            yield name, m.group(0), m.start(), m.end()


def redact_line(line):
    """Return the line with all detected secrets/PII replaced by [REDACTED]."""
    for name, pattern in DETECTORS.items():
        line = pattern.sub("[REDACTED]", line)
    return line


def scan_file(path, redact=False):
    """Scan one file line by line. Returns a list of findings."""
    findings = []
    redacted_lines = []
    with open(path, encoding="utf-8", errors="replace") as f:
        for lineno, line in enumerate(f, start=1):
            for name, match, _start, _end in scan_text(line):
                findings.append({
                    "file": str(path),
                    "line": lineno,
                    "type": name,
                    "severity": SEVERITY.get(name, "MEDIUM"),
                    "match": match.strip(),
                })
            if redact:
                redacted_lines.append(redact_line(line))

    if redact:
        out = path.with_suffix(path.suffix + ".redacted")
        out.write_text("".join(redacted_lines), encoding="utf-8")

    return findings


def main():
    args = sys.argv[1:]
    redact = "--redact" in args
    targets = [a for a in args if not a.startswith("--")]
    root = Path(targets[0]) if targets else Path("sample_logs")

    print("Log & PII/Secrets Scanner")
    print("=" * 72)
    print(f"Target: {root}   Redaction: {'ON' if redact else 'off'}\n")

    all_findings = []
    files = [root] if root.is_file() else [p for p in root.rglob("*") if p.is_file()]
    for path in files:
        if path.suffix == ".redacted":
            continue
        all_findings.extend(scan_file(path, redact=redact))

    # Sort CRITICAL first.
    order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    all_findings.sort(key=lambda f: order.get(f["severity"], 9))

    for f in all_findings:
        # Mask the actual sensitive value so the report itself isn't a leak.
        shown = f["match"][:4] + "..." if len(f["match"]) > 6 else "***"
        print(f"  [{f['severity']:<8}] {f['type']:<20} {f['file']}:{f['line']}"
              f"  ({shown})")

    print("-" * 72)
    by_sev = {}
    for f in all_findings:
        by_sev[f["severity"]] = by_sev.get(f["severity"], 0) + 1
    print(f"{len(all_findings)} finding(s): " +
          ", ".join(f"{k}={v}" for k, v in sorted(by_sev.items())))
    if redact:
        print("Redacted copies written next to each file (*.redacted).")
    if any(f["severity"] == "CRITICAL" for f in all_findings):
        print("Action: rotate any exposed secrets immediately and purge them from logs.")


if __name__ == "__main__":
    main()
