"""
Lesson 8 - Risk Register Engine (Object-Oriented)
=================================================

GRC problem: Risk scoring in spreadsheets is inconsistent - everyone computes
inherent/residual risk slightly differently. Encapsulating the logic in a Risk
*class* makes scoring repeatable and auditable.

This is your introduction to Object-Oriented Programming (OOP): we model a Risk
as an object with data (likelihood, impact) and behavior (compute its score).

Run it:
    python risk_register.py                 # uses risks.csv

Concepts introduced:
- classes and objects
- @dataclass for concise data classes
- methods and computed @property values
- a second class (RiskRegister) that manages many Risk objects
- enums for risk levels
"""

import csv
from dataclasses import dataclass, field
from enum import Enum


class RiskLevel(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


# Risk appetite: scores above this are "above appetite" and need treatment.
RISK_APPETITE = 12


@dataclass
class Risk:
    """A single risk. Likelihood and impact are 1-5 scales.

    control_effectiveness is 0.0-1.0 (how much existing controls reduce the
    risk) and is used to compute residual risk from inherent risk.
    """
    id: str
    title: str
    category: str
    likelihood: int          # 1-5
    impact: int              # 1-5
    control_effectiveness: float = 0.0   # 0.0 (none) .. 1.0 (fully mitigated)
    owner: str = ""

    @property
    def inherent_score(self):
        """Risk before controls: likelihood x impact (range 1-25)."""
        return self.likelihood * self.impact

    @property
    def residual_score(self):
        """Risk after applying control effectiveness."""
        return round(self.inherent_score * (1 - self.control_effectiveness), 1)

    @property
    def level(self):
        """Map the residual score to a qualitative level."""
        s = self.residual_score
        if s >= 17:
            return RiskLevel.CRITICAL
        if s >= 10:
            return RiskLevel.HIGH
        if s >= 5:
            return RiskLevel.MEDIUM
        return RiskLevel.LOW

    @property
    def above_appetite(self):
        return self.residual_score > RISK_APPETITE


@dataclass
class RiskRegister:
    """Manages a collection of Risk objects."""
    risks: list = field(default_factory=list)

    @classmethod
    def from_csv(cls, path):
        """Build a register by reading a CSV file. A 'factory' method."""
        risks = []
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                risks.append(Risk(
                    id=row["id"].strip(),
                    title=row["title"].strip(),
                    category=row["category"].strip(),
                    likelihood=int(row["likelihood"]),
                    impact=int(row["impact"]),
                    control_effectiveness=float(row["control_effectiveness"]),
                    owner=row["owner"].strip(),
                ))
        return cls(risks)

    def ranked(self):
        """Risks sorted by residual score, highest first."""
        return sorted(self.risks, key=lambda r: r.residual_score, reverse=True)

    def above_appetite(self):
        return [r for r in self.risks if r.above_appetite]

    def by_category(self):
        """Return {category: total residual score} for a heatmap-style view."""
        totals = {}
        for r in self.risks:
            totals[r.category] = round(totals.get(r.category, 0) + r.residual_score, 1)
        return totals


def main():
    register = RiskRegister.from_csv("risks.csv")

    print("Risk Register")
    print("=" * 78)
    print(f"Risk appetite threshold (residual): {RISK_APPETITE}\n")

    header = (f"{'ID':<7}{'TITLE':<40}{'INHERENT':<10}"
              f"{'RESIDUAL':<10}{'LEVEL'}")
    print(header)
    print("-" * 78)
    for r in register.ranked():
        flag = "  <-- ABOVE APPETITE" if r.above_appetite else ""
        title = (r.title[:37] + "...") if len(r.title) > 40 else r.title
        print(f"{r.id:<7}{title:<40}{r.inherent_score:<10}"
              f"{r.residual_score:<10}{r.level.value}{flag}")

    print("-" * 78)
    print("Residual risk by category:")
    for cat, total in sorted(register.by_category().items(),
                             key=lambda kv: kv[1], reverse=True):
        print(f"  {cat:<14} {total}")

    over = register.above_appetite()
    print(f"\n{len(over)} risk(s) above appetite require a treatment plan:")
    for r in over:
        print(f"  - {r.id} {r.title} (owner: {r.owner})")


if __name__ == "__main__":
    main()
