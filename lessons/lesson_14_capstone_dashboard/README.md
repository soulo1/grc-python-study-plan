# Lesson 14 — Capstone: Compliance Posture Dashboard

**Concepts:** integration — combining multiple modules, reusing the logic you already
wrote, generating Markdown and HTML, rolling data up into a single RAG status.

## Run it
```bash
python dashboard.py     # writes posture.md and posture.html
```
Open `posture.html` in a browser for a one-page, color-banded compliance snapshot.

## Read it
- `dashboard.py` **reuses** the real functions from lessons 2, 5, 7, and 8 instead of
  reimplementing them — the payoff for writing reusable, return-data functions all along.
- Each `gather_*()` returns a small summary dict; `overall_rag()` rolls them into one
  Red/Amber/Green status.
- It emits both Markdown (for tickets/wikis/PRs) and HTML (for a browser/email).

## Use it for real
This is your weekly/monthly "state of compliance" report — automated. Combine it with
lesson 11's CLI and a scheduler (cron / Task Scheduler / GitHub Actions) so it runs and
publishes itself. Swap the sample CSVs for live data pulls and it becomes a real
dashboard.

## Exercises
1. **Real Markdown→HTML:** `pip install markdown` and render proper HTML tables instead of
   the `<pre>` block.
2. **Trend over time:** append each run's totals to a CSV and chart the trend.
3. **Thresholds:** make the RAG thresholds configurable; exit non-zero on RED so a
   scheduler can alert.
4. **Email/Slack:** send `posture.md` to a channel or mailing list (learn `smtplib` or a
   Slack webhook).
5. **Pull live data:** replace one sample CSV with a real API pull (reuse lesson 6's
   patterns).

## Congratulations
You've built eleven working GRC tools and learned Python from variables to OOP, APIs,
databases, and testing — entirely through real compliance problems. See the project
`STUDY_PLAN.md` ("where to go next") for your continued path.
