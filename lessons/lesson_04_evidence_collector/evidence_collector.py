"""
Lesson 4 - Evidence Collector & Manifest
========================================

GRC problem: During an audit you collect dozens of screenshots/exports. The
auditor wants proof of *what* was collected, *when*, and that it hasn't been
altered. A manifest with cryptographic hashes provides exactly that.

This tool walks an evidence folder and produces a tamper-evident manifest in
both CSV (for spreadsheets) and JSON (for tooling).

Run it:
    python evidence_collector.py                  # walks ./sample_evidence
    python evidence_collector.py /path/to/folder

Concepts introduced:
- the pathlib module (modern file paths)
- reading file bytes and hashing with hashlib (SHA-256)
- the datetime module for timestamps
- writing both CSV and JSON output files
- f-strings for formatting
"""

import csv
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def sha256_of(path):
    """Return the SHA-256 hex digest of a file's contents.

    We read in chunks so this also works on large files.
    """
    h = hashlib.sha256()
    with open(path, "rb") as f:        # "rb" = read binary
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def collect(folder):
    """Return a list of evidence records (one dict per file)."""
    base = Path(folder)
    if not base.exists():
        raise FileNotFoundError(f"Evidence folder not found: {base}")

    collected_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    records = []
    # rglob("*") walks the folder recursively. We skip directories and the
    # manifest files themselves.
    for path in sorted(base.rglob("*")):
        if path.is_dir():
            continue
        if path.name.startswith("evidence_manifest"):
            continue
        stat = path.stat()
        records.append({
            "file": str(path.relative_to(base)),
            "size_bytes": stat.st_size,
            "sha256": sha256_of(path),
            "modified": datetime.fromtimestamp(
                stat.st_mtime, timezone.utc).isoformat(timespec="seconds"),
            "collected_at": collected_at,
        })
    return records, base


def write_manifest(records, base):
    """Write evidence_manifest.csv and .json into the evidence folder."""
    csv_path = base / "evidence_manifest.csv"
    json_path = base / "evidence_manifest.json"

    fields = ["file", "size_bytes", "sha256", "modified", "collected_at"]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(records)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)

    return csv_path, json_path


def main():
    folder = sys.argv[1] if len(sys.argv) > 1 else "sample_evidence"
    print("Evidence Collector & Manifest")
    print("=" * 50)

    records, base = collect(folder)
    for r in records:
        print(f"  {r['file']}")
        print(f"      size: {r['size_bytes']} bytes   sha256: {r['sha256'][:16]}...")

    csv_path, json_path = write_manifest(records, base)
    print("-" * 50)
    print(f"Collected {len(records)} file(s).")
    print(f"Manifest written to:\n  {csv_path}\n  {json_path}")
    print("\nThe SHA-256 hashes prove the files were not altered after collection.")
    print("Re-run later and compare hashes to detect tampering.")


if __name__ == "__main__":
    main()
