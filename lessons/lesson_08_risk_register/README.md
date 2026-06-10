# Lesson 8 — Risk Register Engine (OOP)

**New Python concepts:** classes and objects, `@dataclass`, methods, computed
`@property` values, a `@classmethod` factory, enums, composing two classes.

## Run it
```bash
python risk_register.py    # uses risks.csv
```
Prints risks ranked by residual score, a by-category rollup, and the items above your
risk appetite.

## Read it
- `Risk` is a **class** that bundles data (`likelihood`, `impact`) with behavior. The
  `@property` methods (`inherent_score`, `residual_score`, `level`) compute values from
  that data — so scoring is identical for every risk, every time.
- `residual_score = inherent_score * (1 - control_effectiveness)` encodes the idea that
  controls reduce inherent risk.
- `RiskRegister` manages many `Risk` objects. `from_csv()` is a **factory** classmethod —
  a common, clean way to build objects from a file.

## Use it for real
Replace `risks.csv` with your register (columns: `id, title, category, likelihood, impact,
control_effectiveness, owner`). Adjust `RISK_APPETITE` and the `level` thresholds to your
methodology. Now your scoring is consistent and reproducible.

## Exercises
1. **Add a treatment field:** add `treatment` ("accept/mitigate/transfer/avoid") to `Risk`
   and show it in the output.
2. **Trend:** add a `previous_score` and compute whether each risk went up or down.
3. **Export:** add `RiskRegister.to_csv()` that writes the computed scores back out.
4. **Validation:** make `Risk` reject likelihood/impact outside 1–5 (raise `ValueError`).
   Then write a test for it in lesson 13.

## Checkpoint
- You understand what a class, an instance, a method, and a property are.
- You can model a GRC concept as an object and compute derived values from it.
