# Lesson 9 — Log & PII/Secrets Scanner

**New Python concepts:** regular expressions (`re`) — compiling patterns, `finditer`,
`sub` for redaction — reading files line by line, a dictionary of detectors.

## Run it
```bash
python pii_scanner.py                        # scans ./sample_logs
python pii_scanner.py /path/to/folder
python pii_scanner.py ./sample_logs --redact # also writes *.redacted copies
```

## Read it
- `DETECTORS` maps a name to a **compiled regex**. Regexes are the fundamental tool for
  finding patterns in text/logs — learn to read them: `\bAKIA[0-9A-Z]{16}\b` matches an
  AWS access key.
- `scan_file()` reads **line by line** so it works on huge logs without loading them all
  into memory.
- The report **masks** the matched value so the report itself isn't a new leak.
- `--redact` uses `pattern.sub("[REDACTED]", line)` to produce a safe copy.

## Use it for real
Run it on a copy of a log bundle, a code export, or a config directory before sharing
them or during a DLP review. Rotate any CRITICAL secrets it finds.

> Safety: scan a **copy**, store the output securely, and only scan data you're authorized
> to access. The credit-card and SSN patterns are heuristic — expect false positives.

## Exercises
1. **Add a detector:** add a pattern for your cloud provider's tokens or for phone numbers.
2. **Reduce false positives:** add a Luhn-checksum check so "credit-card-like" numbers
   that fail Luhn are dropped.
3. **Allowlist:** skip known-safe values (e.g., `noreply@example.com`).
4. **JSON output:** write findings to `findings.json` for a ticketing pipeline.

## Checkpoint
- You can read and write basic regular expressions.
- You can stream a large file and transform it (redaction).
