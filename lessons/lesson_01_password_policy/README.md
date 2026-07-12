# Lesson 1 — Password Policy Validator

**New Python concepts:** variables, strings, booleans, `if`/`elif`/`else`, functions,
`print()`, looping over a string, running a script.

## Run it
```bash
python password_policy_validator.py
```
You should see a PASS/FAIL report for several example passwords with reasons.

## Read it
Open `password_policy_validator.py` and read it top to bottom. The three sections are:
1. **Policy config** — variables you can tune.
2. **The check** — a function that *returns* a list of failure reasons.
3. **Run it** — the `main()` that exercises the function.

Key idea: `check_password()` **returns data** (a list) instead of printing. That makes it
reusable — lesson 13 will test it, and other tools can import it.

## Use it for real
- Validate that a proposed standard password meets your written policy.
- Add the candidate password(s) to the `examples` list and re-run.
- Later (lesson 2) you'll learn to read a file, so you can feed in a list instead.

## Exercises (this is where you learn)
1. **Tune the policy:** change `MIN_LENGTH` to 16 and re-run. Watch which passwords now
   fail.
2. **Add a rule:** add a `MAX_LENGTH` check (e.g., reject > 64 chars, a real bcrypt
   limitation). Hint: add a config variable and one `if` block.
3. **Add a contextual rule:** write a new check that fails a password if it contains the
   username. Change `check_password(password)` to `check_password(password, username="")`
   and add an `if username and username.lower() in password.lower():` block.
4. **Strength score:** instead of just PASS/FAIL, return a score 0–5 based on how many
   character classes are present plus a length bonus. Print it in `report()`.

## Checkpoint — you can move on when you can…
- Explain what a function `return`s vs. what it `print`s.
- Add a new policy rule without breaking the others.
- Read the whole file and predict its output before running it.

## Run individual password checks... Soulo 1 7/12/2026
- In order to test an individual password against policy.
- Type: python -i  password_policy_validator.py and hit enter.
- This will allow you to run the script in interactive mode.
- Your terminal prompt will change to >>>. # Your file has now been loaded into memory, and you can test any password you want manually:
- type at the >>> check-password("type a password here") and press enter to test it
- If it does not meet the policy criteria the failure reason will appear
- If it does meet the policy criteria you will see 0 failures.
- Type exit() and hit enter to return to your regular terminal. 
