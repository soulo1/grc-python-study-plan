# Lesson 13 — Testing Your Tools (pytest)

**New Python concepts:** why automated tests matter, `pytest`, test functions, `assert`,
edge-case testing, `@pytest.mark.parametrize`, importing code from other folders.

## Setup
```bash
pip install pytest    # or: pip install -r ../../requirements.txt
```

## Run it
```bash
pytest -v             # from this folder or the project root
```
You should see a list of passing tests.

## Read it
- Each `test_*` function checks one behavior with a plain `assert`. No ceremony.
- We test the **happy path** (a strong password passes) *and* **edge cases** (short,
  common, missing character classes).
- `@pytest.mark.parametrize` runs the same test across several inputs — concise coverage.
- The `load()` helper imports the tools from their lesson folders so the tests can call
  real functions like `pw.check_password()` and `risk.Risk(...)`.

## Why this is the most important lesson
A script you run once and eyeball is fine. But a *tool* you rely on — that flags audit
exceptions or risk-appetite breaches — must be trustworthy. Tests let you change a rule
and instantly know whether you broke anything. This is the line between a script and
production automation.

## Exercises
1. **Break something on purpose:** change `MIN_LENGTH` to 4 in lesson 1 and run `pytest`.
   Watch the length test fail. Revert it.
2. **Add a test:** write a test for your lesson-1 "no username in password" rule.
3. **Test the access review:** write a test that feeds one fabricated row to
   `review_account()` and asserts the right flag appears.
4. **Coverage:** `pip install pytest-cov` then `pytest --cov` to see what's untested.

## Checkpoint
- You can write and run pytest tests.
- You understand regression testing and why it makes automation trustworthy.
