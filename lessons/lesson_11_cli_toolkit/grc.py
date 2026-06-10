"""
Lesson 11 - GRC CLI Toolkit
===========================

GRC problem: You now have several scripts scattered across folders. You (and
your teammates) want ONE consistent command - with --help, flags, and proper
exit codes - so the tools can run in cron/CI.

This wraps the earlier lessons behind a single `grc` command using argparse and
subcommands. It runs each underlying tool and forwards its exit code, so a
non-zero exit (e.g., overdue items found) can fail a CI job.

Run it:
    python grc.py --help
    python grc.py access-review
    python grc.py triage
    python grc.py expiry --window 14
    python grc.py scan

Concepts introduced:
- argparse: arguments, subcommands (subparsers), --flags, --help
- structuring a project / locating sibling files with pathlib
- running another script with subprocess and forwarding its exit code
- process exit codes (sys.exit) for automation
"""

import argparse
import subprocess
import sys
from pathlib import Path

# The lessons live as siblings of this file's parent (../lesson_XX_.../).
LESSONS = Path(__file__).resolve().parent.parent

# Map each subcommand to (working_dir, script_name).
COMMANDS = {
    "access-review": (LESSONS / "lesson_02_access_review", "access_review.py"),
    "triage":        (LESSONS / "lesson_05_vuln_triage", "vuln_triage.py"),
    "expiry":        (LESSONS / "lesson_07_expiry_monitor", "expiry_monitor.py"),
    "scan":          (LESSONS / "lesson_09_log_pii_scanner", "pii_scanner.py"),
    "risk":          (LESSONS / "lesson_08_risk_register", "risk_register.py"),
}


def run_tool(name, extra_args):
    """Run the underlying lesson script in its own directory; return exit code."""
    workdir, script = COMMANDS[name]
    script_path = workdir / script
    if not script_path.exists():
        print(f"[error] expected tool not found: {script_path}")
        return 2
    # We pass through any extra args (e.g., --window 14) to the underlying tool.
    result = subprocess.run(
        [sys.executable, str(script_path), *extra_args],
        cwd=str(workdir),
    )
    return result.returncode


def build_parser():
    parser = argparse.ArgumentParser(
        prog="grc",
        description="GRC automation toolkit - one command for your compliance tools.",
    )
    sub = parser.add_subparsers(dest="command", required=True,
                                help="which tool to run")

    sub.add_parser("access-review", help="run the user access review")
    sub.add_parser("triage", help="prioritize vulnerability findings")

    expiry = sub.add_parser("expiry", help="report expiring compliance obligations")
    expiry.add_argument("--window", type=int, default=30,
                        help="'due soon' window in days (default 30)")

    scan = sub.add_parser("scan", help="scan files for secrets/PII")
    scan.add_argument("--redact", action="store_true",
                      help="also write redacted copies")

    sub.add_parser("risk", help="score and rank the risk register")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    # Rebuild the flags to forward to the underlying tool.
    extra = []
    if args.command == "expiry":
        extra = ["--window", str(args.window)]
    elif args.command == "scan" and getattr(args, "redact", False):
        extra = ["--redact"]

    code = run_tool(args.command, extra)
    # Forward the underlying tool's exit code so cron/CI can react to it.
    sys.exit(code)


if __name__ == "__main__":
    main()
