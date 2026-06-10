"""
Lesson 6 - CVE Enrichment via the NVD API
==========================================

GRC problem: You have a list of CVE IDs (from a pen test, a scan, a vendor
advisory) and need authoritative severity data without looking each one up by
hand. The NIST National Vulnerability Database (NVD) has a free REST API.

This tool enriches CVE IDs with CVSS score, severity, vector, and description.
It works OFFLINE against a bundled cache (so the lesson always runs), and can
hit the LIVE NVD API when you pass --live.

Run it:
    python cve_enrich.py CVE-2021-44228 CVE-2014-0160      # offline cache
    python cve_enrich.py --live CVE-2023-23397             # live NVD lookup

Concepts introduced:
- JSON: loading/saving structured data (json module)
- calling a REST API with the `requests` library
- handling network errors and missing data gracefully
- caching results to disk so you don't re-fetch
- separating "get the data" from "use the data"
"""

import json
import sys
from pathlib import Path

CACHE_PATH = Path(__file__).parent / "cve_cache.json"
NVD_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"


def load_cache():
    """Load the local cache of CVE data (a dict keyed by CVE ID)."""
    if CACHE_PATH.exists():
        with open(CACHE_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_cache(cache):
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2, sort_keys=True)


def fetch_live(cve_id):
    """Fetch one CVE from the live NVD API. Returns a normalized dict or None.

    Requires the `requests` library and internet access. We import it inside
    the function so the offline path works even if requests isn't installed.
    """
    try:
        import requests
    except ImportError:
        print("  [error] the 'requests' library is not installed. "
              "Run: pip install requests")
        return None

    try:
        resp = requests.get(NVD_URL, params={"cveId": cve_id}, timeout=20)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:                      # network/JSON errors
        print(f"  [error] live lookup failed for {cve_id}: {e}")
        return None

    # Dig into the NVD response structure defensively - fields may be missing.
    vulns = data.get("vulnerabilities", [])
    if not vulns:
        return None
    cve = vulns[0].get("cve", {})

    description = ""
    for d in cve.get("descriptions", []):
        if d.get("lang") == "en":
            description = d.get("value", "")
            break

    # NVD may return CVSS v3.1, v3.0, or v2 metrics. Try them in order.
    metrics = cve.get("metrics", {})
    for key in ("cvssMetricV31", "cvssMetricV30", "cvssMetricV2"):
        if key in metrics and metrics[key]:
            cvss_data = metrics[key][0].get("cvssData", {})
            return {
                "cvss": cvss_data.get("baseScore"),
                "severity": (cvss_data.get("baseSeverity")
                             or metrics[key][0].get("baseSeverity", "UNKNOWN")),
                "vector": cvss_data.get("vectorString", ""),
                "description": description,
            }
    return {"cvss": None, "severity": "UNKNOWN", "vector": "", "description": description}


def enrich(cve_ids, live=False):
    """Return enriched data for each CVE ID, using cache and optionally live."""
    cache = load_cache()
    results = {}
    for cve_id in cve_ids:
        cve_id = cve_id.upper()
        if cve_id in cache and not live:
            results[cve_id] = cache[cve_id]
        elif live:
            print(f"  [live] querying NVD for {cve_id} ...")
            data = fetch_live(cve_id)
            if data:
                cache[cve_id] = data          # update cache for next time
                results[cve_id] = data
            else:
                results[cve_id] = None
        else:
            results[cve_id] = None            # not in cache, not live
    if live:
        save_cache(cache)
    return results


def main():
    args = sys.argv[1:]
    live = "--live" in args
    cve_ids = [a for a in args if a.upper().startswith("CVE-")]

    if not cve_ids:
        # Default demo set so the lesson runs with no arguments.
        cve_ids = ["CVE-2021-44228", "CVE-2014-0160", "CVE-2020-1472"]

    print("CVE Enrichment (NVD)")
    print("=" * 72)
    print(f"Mode: {'LIVE (api.nvd.nist.gov)' if live else 'OFFLINE cache'}\n")

    results = enrich(cve_ids, live=live)
    for cve_id, data in results.items():
        if data is None:
            print(f"{cve_id}: not found "
                  f"(try --live, or add it to cve_cache.json)")
            continue
        print(f"{cve_id}  [{data['severity']}]  CVSS {data['cvss']}")
        print(f"    vector: {data['vector']}")
        print(f"    {data['description'][:100]}...")
        print()


if __name__ == "__main__":
    main()
