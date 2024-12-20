import pyodbc
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

print("Script started...")
print("Environment variables loaded...")


def get_db_connection():
    DB_CONFIG = {
        'server': os.getenv('DB_HOST'),
        'database': os.getenv('DB_NAME'),
        'port': os.getenv('DB_PORT'),
        'username': os.getenv('DB_USERNAME'),
        'password': os.getenv('DB_PASSWORD')
    }

    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={DB_CONFIG['server']},{DB_CONFIG['port']};"
        f"DATABASE={DB_CONFIG['database']};"
        f"UID={DB_CONFIG['username']};"
        f"PWD={DB_CONFIG['password']};"
        "TrustServerCertificate=yes"
    )
    return pyodbc.connect(conn_str)


def test_database_connection():
    try:
        conn = get_db_connection()
        print("Successfully connected to the database!")
        conn.close()
        return True
    except Exception as e:
        print(f"Error connecting to the database: {str(e)}")
        return False

def drop_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            IF OBJECT_ID('oneliners', 'U') IS NOT NULL 
            DROP TABLE oneliners
        """)
        conn.commit()
        print("Table 'oneliners' dropped successfully.")
    except Exception as e:
        print(f"Error dropping table: {str(e)}")
    finally:
        cursor.close()
        conn.close()

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'oneliners')
            CREATE TABLE oneliners (
                number INT IDENTITY(1,1) PRIMARY KEY,
                category NVARCHAR(80) NOT NULL,
                joke NVARCHAR(MAX) NOT NULL
            )
        """)
        conn.commit()
        print("Table 'oneliners' created or already exists.")
    except Exception as e:
        print(f"Error creating table: {str(e)}")
    finally:
        cursor.close()
        conn.close()


def verify_table_structure():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM oneliners WHERE 1=0")
        columns = [column[0] for column in cursor.description]
        print("Table structure:", columns)
        return True
    except Exception as e:
        print(f"Error verifying table structure: {str(e)}")
        return False
    finally:
        cursor.close()
        conn.close()


def verify_csv_content():
    try:
        df = pd.read_csv('oneLiners/dad_jokes_oneliners.csv')
        print("CSV content preview:")
        print(df.head())
        return True
    except Exception as e:
        print(f"Error reading CSV: {str(e)}")
        return False


def load_jokes_from_csv():
    print("Starting to load jokes from CSV...")
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        print("Clearing existing data...")
        cursor.execute("DELETE FROM oneliners")
        conn.commit()
        print("Existing data cleared.")

        print("Reading CSV file...")
        df = pd.read_csv('oneLiners/dad_jokes_oneliners.csv')
        total_jokes = len(df)
        print(f"Found {total_jokes} jokes to insert")

        for index, row in df.iterrows():
            if index % 10 == 0:  # Print progress every 10 records
                print(f"Inserting joke {index + 1} of {total_jokes}")
            try:
                cursor.execute(
                    "INSERT INTO oneliners (category, joke) VALUES (?, ?)",
                    (row['category'], row['joke'])
                )
            except Exception as e:
                print(f"Error inserting joke #{index + 1}: {str(e)}")
                print(f"Problematic row: {row}")
                raise e

        print("All jokes inserted, committing transaction...")
        conn.commit()
        print("Successfully loaded jokes from CSV!")
        return True
    except Exception as e:
        print(f"Error loading jokes from CSV: {str(e)}")
        return False
    finally:
        print("Closing database connection...")
        cursor.close()
        conn.close()
        print("Database connection closed.")


def verify_database_content():
    print("Verifying database content...")
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM oneliners")
        count = cursor.fetchone()[0]
        print(f"Total jokes in database: {count}")

        cursor.execute("SELECT TOP 5 * FROM oneliners")
        rows = cursor.fetchall()
        print("\nFirst 5 jokes in database:")
        for row in rows:
            print(f"Number: {row[0]}, Category: {row[1]}, Joke: {row[2]}")
    except Exception as e:
        print(f"Error verifying database content: {str(e)}")
    finally:
        cursor.close()
        conn.close()
        print("Verification complete.")


if __name__ == "__main__":
    print("\n1. Testing database connection...")
    test_database_connection()

    print("\n2. Dropping tables...")
    drop_tables()

    print("\n3. Creating tables...")
    create_tables()

    print("\n4. Verifying table structure...")
    verify_table_structure()

    print("\n5. Verifying CSV content...")
    verify_csv_content()

    print("\n6. Loading jokes from CSV...")
    load_jokes_from_csv()

    print("\n7. Verifying database content...")
    verify_database_content()

    print("\nScript completed!")
