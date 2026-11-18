
import sqlite3


def save_to_database(df, database_file):
    """
    Save valid employee records into an SQLite database.
    """

    connection = sqlite3.connect(database_file)

    # Remove validation-only column before saving
    df = df.drop(columns=["rejection_reason"], errors="ignore")

    # Save employee records into the employees table
    df.to_sql(
        "employees",
        connection,
        if_exists="replace",
        index=False
    )

    connection.close()

    print("Employee records saved to SQLite successfully.")
