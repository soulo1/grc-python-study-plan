# Lesson 10 — Compliance Report Generator (Excel)

**New Python concepts:** installing and using a **third-party library** (`openpyxl`),
creating workbooks/sheets, writing and styling cells, conditional (RAG) formatting.

## Setup
```bash
pip install openpyxl     # or: pip install -r ../../requirements.txt
```

## Run it
```bash
python report_generator.py     # reads controls_status.csv -> compliance_report.xlsx
```
Open `compliance_report.xlsx` — a **Summary** sheet with status counts and a **Controls**
sheet with a red/amber/green Status column and a frozen header row.

## Read it
- The `try/except ImportError` shows how to fail with a helpful message when a dependency
  is missing — good practice for tools others will run.
- `STATUS_FILL` maps each control status to a color; the detail sheet applies it per row.
- `ws.freeze_panes` and column widths are small touches that make output look professional.

## Use it for real
Export your control inventory + status to `controls_status.csv` (columns: `control_id,
name, framework, owner, status, last_tested`) and generate your monthly leadership/auditor
report in one command instead of hand-formatting a spreadsheet.

## Exercises
1. **Add a chart:** use `openpyxl.chart.PieChart` to chart the status breakdown on the
   Summary sheet.
2. **Overdue testing:** color `last_tested` red if older than 90 days (reuse lesson 7's
   date math).
3. **Per-framework sheets:** create one sheet per framework.
4. **Title page:** add a cover sheet with report date and your org name.

## Checkpoint
- You can install and use an external package.
- You can generate a styled, shareable Excel artifact from data.
