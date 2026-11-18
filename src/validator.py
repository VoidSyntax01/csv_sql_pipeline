import re
import pandas as pd


def is_valid_email(email):
    """
    Check whether an email address is valid.
    """

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}$'

    return bool(re.match(pattern, str(email)))


def validate_employees(df):
    """
    Validate employee records.

    Missing salary is allowed.
    Invalid non-empty salary is rejected.
    """

    df = df.copy()

    # Keep original salary values for validation
    original_salary = df["Salary"].copy()

    # Convert salary into numeric values
    df["Salary"] = pd.to_numeric(df["Salary"], errors="coerce")

    rejection_reasons = []

    for index, row in df.iterrows():
        reasons = []

        if pd.isna(row["ID"]):
            reasons.append("Missing employee ID")

        if pd.isna(row["Name"]):
            reasons.append("Missing employee name")

        # Reject invalid salary text, but allow missing salary
        if (
            not pd.isna(original_salary.loc[index])
            and pd.isna(row["Salary"])
        ):
            reasons.append("Invalid salary")

        if not is_valid_email(row["Email"]):
            reasons.append("Invalid email")

        rejection_reasons.append(", ".join(reasons))

    df["rejection_reason"] = rejection_reasons

    valid_rows = df[df["rejection_reason"] == ""].copy()
    rejected_rows = df[df["rejection_reason"] != ""].copy()

    return valid_rows, rejected_rows


