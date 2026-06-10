# Lesson 3 — Control Framework Mapper

**New Python concepts:** dictionaries, nested dictionaries, lists inside dicts, **sets**
and set operations (difference), iterating with `.items()` / `.values()`.

## Run it
```bash
python control_mapper.py
```
Prints the crosswalk, the SOC 2 criteria you currently cover, and any **gaps** versus a
required set.

## Read it
- `CROSSWALK` is a dictionary of dictionaries — the core data-modeling skill in GRC
  automation. Each NIST CSF subcategory maps to ISO and SOC 2 controls plus a description.
- `coverage_gap()` uses a **set difference** (`need - have`) — the cleanest way to answer
  "what am I missing?"

## Use it for real
Replace the sample `CROSSWALK` with your real mappings (your GRC tool or a published
crosswalk like the Secure Controls Framework can seed this). Then `coverage_gap()`
instantly tells you what's unmapped for any audit scope.

## Exercises
1. **Add your frameworks:** add a `pci_dss` key to each entry and include it in the
   output.
2. **Reverse lookup:** write `find_by_iso(iso_id)` that returns every NIST CSF entry
   referencing a given ISO control.
3. **Coverage %:** compute what percentage of a required SOC 2 set is covered.
4. **Load from a file:** move `CROSSWALK` into a JSON file and load it (preview of
   lesson 6's JSON skills) so non-developers can edit the mappings.

## Checkpoint
- You can model real GRC relationships as nested dicts.
- You understand when to use a **set** (uniqueness, membership, gaps) vs. a list.
