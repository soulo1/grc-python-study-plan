# Lesson 4 — Evidence Collector & Manifest

**New Python concepts:** `pathlib` (modern paths), reading binary files, hashing with
`hashlib` (SHA-256), `datetime` timestamps, writing both CSV and JSON output.

## Run it
```bash
python evidence_collector.py                 # walks ./sample_evidence
python evidence_collector.py /path/to/folder
```
Produces `evidence_manifest.csv` and `evidence_manifest.json` inside the folder.

## Read it
- `sha256_of()` reads a file in chunks and produces a fingerprint. If even one byte
  changes, the hash changes — that's what makes the manifest tamper-evident.
- `collect()` uses `Path.rglob("*")` to walk a folder recursively.
- We write **two** formats: CSV for humans/auditors, JSON for tools.

## Use it for real
Point it at the folder where you stash audit evidence (screenshots, config exports,
policy PDFs). The manifest records each file's hash and collection time — give it to your
auditor as proof of integrity, and re-run later to detect changes.

## Exercises
1. **Verify mode:** add a `--verify` flag that re-hashes files and reports any whose hash
   differs from a previously saved manifest.
2. **Filter by type:** only include certain extensions (`.png`, `.pdf`, `.csv`).
3. **Add metadata:** prompt for (or accept as an argument) the control ID each evidence
   file supports, and add it as a column.
4. **Zip it:** after building the manifest, package the folder into a timestamped `.zip`
   (look up the `zipfile` module).

## Checkpoint
- You understand why hashing provides integrity evidence.
- You can read and write files and produce both CSV and JSON.
