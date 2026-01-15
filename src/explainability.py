import numpy as np


def explain_decision(row, decision):
    """Generate explanation for a single loan decision"""

    reasons = []

    if row["income"] < 200:
        reasons.append("Low income")

    if row["debt"] > 10:
        reasons.append("High debt")

    if row["credit_score"] < 2:
        reasons.append("Low credit score")

    if decision == 1 and not reasons:
        return "Approved by model with acceptable risk"

    return "Rejected due to: " + ", ".join(reasons)
