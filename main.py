
import argparse
import os
import pandas as pd
from src.cleaner import standardize_text, remove_duplicates
from src.validator import validate_employees
from src.database import save_to_database


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="CSV Data Cleaning and SQL Pipeline"
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to the input CSV file"
    )

    parser.add_argument(
        "--db",
        required=True,
        help="Path to the SQLite database"
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    input_file = args.input
    database_file = args.db

    # Check whether input file exists
    if os.path.exists(input_file):
        print("Input file found.")
    else:
        print("Error: Input file not found.")
        return
    
    # Read CSV file
    df = pd.read_csv(input_file)

    original_row_count = len(df)

    # Standardize text columns
    df = standardize_text(df, ["Name", "Department"], case="title")
    df = standardize_text(df, ["Email"], case="lower")

    # Remove duplicate rows
    df = remove_duplicates(df)
    cleaned_row_count = len(df)

    # Validate employee records
    valid_rows, rejected_rows = validate_employees(df)


    accepted_count = len(valid_rows)
    rejected_count = len(rejected_rows)

    print("\n========== CLEANING & VALIDATION SUMMARY ==========")
    print(f"Original rows:          {original_row_count}")
    print(f"Rows after cleaning:    {cleaned_row_count}")
    print(f"Duplicate rows removed: {original_row_count - cleaned_row_count}")
    print(f"Accepted records:       {accepted_count}")
    print(f"Rejected records:       {rejected_count}")
    print("===================================================")


    # Create output folder if it does not exist
    os.makedirs("output", exist_ok=True)

    # Save rejected employee records
    rejected_rows.to_csv(
        "output/rejected_rows.csv",
        index=False
    )

    print("\nRejected records saved to output/rejected_rows.csv")

    # Save accepted records to SQLite
    save_to_database(valid_rows, database_file)


    


    print("Input CSV:", input_file)
    print("Database:", database_file)


if __name__ == "__main__":
    main()
