# Lesson 11 — GRC CLI Toolkit

**New Python concepts:** `argparse` (arguments, subcommands, `--flags`, auto `--help`),
locating sibling files with `pathlib`, running another script with `subprocess`, process
**exit codes** for automation.

## Run it
```bash
python grc.py --help
python grc.py access-review
python grc.py triage
python grc.py expiry --window 14
python grc.py scan --redact
python grc.py risk
```

## Read it
- `build_parser()` defines a parent parser plus one **subparser** per tool. argparse gives
  you `--help` for free at every level.
- `run_tool()` launches the underlying lesson script with `subprocess.run`, in that
  script's own directory (so its sample-data paths resolve), and **forwards its exit code**.
- `sys.exit(code)` propagates that code — so a future "fail if overdue" exit can break a
  CI build or trigger a cron alert.

## Use it for real
This is the front door to scheduling your automation (lesson 14 + cron/Task Scheduler/CI).
Add new subcommands as you build more tools. Teammates only need to learn one command.

## Exercises
1. **Meaningful exit codes:** modify `vuln_triage.py` to `sys.exit(1)` when overdue items
   exist, then run `grc triage; echo $?` to see the code.
2. **Global `--csv` option:** let `access-review` and `triage` take a `--csv PATH` and
   forward it.
3. **`grc all`:** add a subcommand that runs every tool in sequence and returns non-zero
   if any failed.
4. **Install it as a real command:** add a `pyproject.toml` with a console-script entry
   point so you can type `grc` anywhere (stretch).

## Checkpoint
- You can build a multi-command CLI with `argparse`.
- You understand exit codes and why automation depends on them.
