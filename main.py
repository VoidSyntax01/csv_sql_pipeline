
import argparse
import os
import pandas as pd

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

    print(df.head())
    print(df.shape)
    print(df.columns)
    print(df.dtypes)
    print(df.isnull().sum())
    print(df.duplicated().sum())


    print("Input CSV:", input_file)
    print("Database:", database_file)


if __name__ == "__main__":
    main()
