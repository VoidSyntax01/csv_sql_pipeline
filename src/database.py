
import sqlite3


def save_to_database(df, database_file):
    """
    Create the employees table and insert valid records.
    Duplicate or constraint-violating records are ignored.
    """

    connection = None

    try:
        # Open SQLite connection
        connection = sqlite3.connect(database_file)
        cursor = connection.cursor()

        # Create employees table if it does not exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                ID INTEGER PRIMARY KEY,
                Name TEXT NOT NULL,
                Department TEXT,
                Salary REAL,
                Email TEXT
            )
        """)

        # SQL insertion query
        insert_query = """
            INSERT OR IGNORE INTO employees
            (ID, Name, Department, Salary, Email)
            VALUES (?, ?, ?, ?, ?)
        """

        # Remove validation-only column
        records = df.drop(
            columns=["rejection_reason"],
            errors="ignore"
        )

        # Convert DataFrame rows into tuples
        employee_records = list(
            records[["ID", "Name", "Department", "Salary", "Email"]]
            .itertuples(index=False, name=None)
        )

        # Insert records
        cursor.executemany(insert_query, employee_records)

        # Count inserted and skipped records
        inserted_count = cursor.rowcount
        skipped_count = len(employee_records) - inserted_count

        # Save changes
        connection.commit()

        print("\n========== DATABASE SUMMARY ==========")
        print(f"Records processed: {len(employee_records)}")
        print(f"Records inserted:  {inserted_count}")
        print(f"Records skipped:   {skipped_count}")
        print("======================================")

    except sqlite3.Error as error:
        print(f"Database error: {error}")

        if connection is not None:
            connection.rollback()

    finally:
        # Always close the connection
        if connection is not None:
            connection.close()
            print("Database connection closed.")
