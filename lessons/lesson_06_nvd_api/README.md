# Lesson 6 — CVE Enrichment via the NVD API

**New Python concepts:** JSON (`json` module), calling a REST API with `requests`,
handling network/missing-data errors, caching results to disk.

## Run it
```bash
python cve_enrich.py CVE-2021-44228 CVE-2014-0160   # offline, from cve_cache.json
python cve_enrich.py --live CVE-2023-23397          # live NVD lookup (needs internet)
```
With no arguments it enriches a default demo set from the bundled cache, so it always
runs even offline.

## Read it
- `load_cache()` / `save_cache()` read and write a JSON file — your first taste of
  persisting structured data.
- `fetch_live()` calls the NVD API with `requests`, then **defensively** digs through the
  response (`.get(...)` everywhere) because real API responses have missing/variable
  fields (CVSS v3.1 vs v3.0 vs v2).
- Results are cached so you don't re-fetch the same CVE — important because NVD
  rate-limits anonymous requests.

## Use it for real
Feed in CVEs from a pen-test report or your scan (lesson 5's output). Run `--live` to pull
authoritative CVSS data, then merge it into your triage worklist. For heavier use, request
a free NVD API key and send it as a header (see exercise 3).

## Exercises
1. **Combine with lesson 5:** read `sample_scan.csv`, pull each CVE, and replace the
   scanner's severity with NVD's authoritative score.
2. **Be polite to the API:** add a `time.sleep(6)` between live requests (NVD asks for
   ~6s without a key) and handle HTTP 403/429.
3. **Use an API key:** read `NVD_API_KEY` from an environment variable and send it as the
   `apiKey` header. **Never hard-code keys in the script.**
4. **Cache freshness:** store a fetch timestamp and re-fetch entries older than 30 days.

## Checkpoint
- You can call an API and parse JSON safely.
- You understand caching and why you never commit API keys to code.
