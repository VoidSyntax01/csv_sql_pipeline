import pandas as pd
import numpy as np
from scipy import stats


def standardize_text(df, columns, case="title"):
    """
    Standardize text columns by removing whitespace
    and applying the selected case format.

    Args:
        df: Input DataFrame
        columns: List of column names
        case: "title" or "lower"

    Returns:
        Cleaned DataFrame

    """

    

    df = df.copy()

    for col in columns:
        df[col] = df[col].str.strip()

        if case == "title":
            df[col] = df[col].str.title()
        elif case == "lower":
            df[col] = df[col].str.lower()

    return df

    
def remove_duplicates(df):
    """
    Remove duplicate rows from DataFrame.

    Args:
        df: Input DataFrame

    Returns:
        DataFrame without duplicate rows
    """

    return df.drop_duplicates().reset_index(drop=True)


def handle_missing_values(df, strategy="drop"):
    """
    Handle missing values in a DataFrame.

    Args:
        df: Input DataFrame
        strategy: drop, mean, median, or forward_fill

    Returns:
        DataFrame after handling missing values
    """

    df = df.copy()

    if strategy == "drop":
        df = df.dropna()

    elif strategy == "mean":
        numeric_cols = df.select_dtypes(include=["number"]).columns
        df[numeric_cols] = df[numeric_cols].fillna(
            df[numeric_cols].mean()
        )

    elif strategy == "median":
        numeric_cols = df.select_dtypes(include=["number"]).columns
        df[numeric_cols] = df[numeric_cols].fillna(
            df[numeric_cols].median()
        )

    elif strategy == "forward_fill":
        df = df.ffill()

    return df
