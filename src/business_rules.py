import numpy as np


def apply_business_rules(X_test, model_predictions, income_idx, debt_idx):
    """
    Apply banking rules to override ML predictions

    Rules:
    - Income < threshold → Reject
    - Debt > threshold → Reject
    """

    final_predictions = model_predictions.copy()

    for i in range(len(final_predictions)):
        income = X_test[i, income_idx]
        debt = X_test[i, debt_idx]

        if income < -0.5:  # scaled low income
            final_predictions[i] = 0

        if debt > 1.5:  # scaled high debt
            final_predictions[i] = 0

    return final_predictions
