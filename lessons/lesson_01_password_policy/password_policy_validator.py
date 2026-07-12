"""
Lesson 1 - Password Policy Validator
=====================================

GRC problem: You publish a password standard (length, complexity, no common
passwords). How do you actually *check* whether a given password meets it?

This is the smallest useful program in the course. It uses only the absolute
basics of Python: variables, strings, booleans, if/elif/else, functions, and
print(). No files, no libraries. Read it top to bottom.

Run it:
    python password_policy_validator.py

Concepts introduced:
- variables and types (str, int, bool)
- functions (def ... return ...)
- conditionals (if / elif / else)
- string methods (.isupper(), .isdigit(), etc.)
- looping over characters in a string
"""

# ---------------------------------------------------------------------------
# 1) POLICY CONFIG
# These are "variables" - named values you can change in one place. A GRC
# analyst should be able to tune the policy here without touching the logic.
# Modeled on NIST SP 800-63B and CIS password guidance.
# ---------------------------------------------------------------------------
MIN_LENGTH = 12          # NIST recommends long passphrases over arbitrary complexity
MAX_LENGTH = 45          # Adding maximum pw length control 
REQUIRE_UPPER = True
REQUIRE_LOWER = True
REQUIRE_DIGIT = True
REQUIRE_SYMBOL = True

# A tiny blocklist of common/breached passwords. In real life you'd load a big
# list (e.g., the "Have I Been Pwned" top passwords) - we do that in later
# lessons once you've learned to read files.
COMMON_PASSWORDS = {
    "password", "password1", "123456", "qwerty", "letmein", "MickeyMouse",
    "admin", "welcome", "iloveyou", "monday1", "changeme",
}

SYMBOLS = "!@#$%^&*()-_=+[]{};:,.<>/?\\|`~'\""


# ---------------------------------------------------------------------------
# 2) THE CHECK
# A function takes input (a password) and RETURNS data (a list of reasons it
# failed). Returning data instead of printing keeps logic reusable - we'll
# lean on this heavily in later lessons.
# ---------------------------------------------------------------------------
def check_password(password):
    """Return a list of human-readable reasons the password fails policy.

    An empty list means the password PASSES.
    """
    failures = []

    # Length check
    if len(password) < MIN_LENGTH:
        failures.append(f"too short: {len(password)} chars (need >= {MIN_LENGTH})")
    elif len(password) > MAX_LENGTH:
        failures.append(f"too long: {len(password)} chars (need <= {MAX_LENGTH})")

    # Character-class checks. We scan the password once and set flags.
    has_upper = False
    has_lower = False
    has_digit = False
    has_symbol = False
    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
        elif char in SYMBOLS:
            has_symbol = True

    if REQUIRE_UPPER and not has_upper:
        failures.append("missing an uppercase letter")
    if REQUIRE_LOWER and not has_lower:
        failures.append("missing a lowercase letter")
    if REQUIRE_DIGIT and not has_digit:
        failures.append("missing a digit")
    if REQUIRE_SYMBOL and not has_symbol:
        failures.append("missing a symbol")

    # Blocklist check (case-insensitive)
    if password.lower() in COMMON_PASSWORDS:
        failures.append("appears on the common/breached password blocklist")

    return failures

def report(password):
    """Print a PASS/FAIL report for a single password."""
    failures = check_password(password)
    # We mask the password in output so we don't leak it to logs/screens.
    masked = password[0] + "*" * (len(password) - 1) if password else "(empty)"
    if not failures:
        print(f"[PASS] {masked}")
    else:
        print(f"[FAIL] {masked}")
        for reason in failures:
            print(f"        - {reason}")


# ---------------------------------------------------------------------------
# 3) RUN IT
# This block runs only when you execute the file directly. We test a handful
# of example passwords so you can see PASS and FAIL outputs immediately.
# ---------------------------------------------------------------------------
def main():
    print("Password Policy Validator")
    print("=" * 40)
    print(f"Policy: min length {MIN_LENGTH}, "
          f"Policy: max length {MAX_LENGTH}, "
          f"upper={REQUIRE_UPPER}, lower={REQUIRE_LOWER}, "
          f"digit={REQUIRE_DIGIT}, symbol={REQUIRE_SYMBOL}\n")

    examples = [
        "password",                 # on blocklist, too short, no complexity
        "Spring2024",               # too short-ish, no symbol
        "Tr0ub4dor&3",              # decent but short of 12
        "correct-horse-Battery9!",  # strong passphrase
        "ALLUPPERCASE123!",         # no lowercase
        "9x#K2m!vP$8bQ&zW4t*N7xY@1pL_3fC%6vR(9jKs)2mN!5bQ"   # password is too long
                                ]
    for pw in examples:
        report(pw)

    print("\nTip: edit the POLICY CONFIG at the top of this file and re-run.")
    print("Try your own password by adding it to the 'examples' list,")
    print("or import check_password() from your own script.")


if __name__ == "__main__":
    main()
