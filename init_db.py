import os
import pandas as pd
import pyodbc
import time
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'server': os.getenv('DB_HOST'),  # Changed from DB_SERVER to DB_HOST
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_NAME'),
    'username': os.getenv('DB_USERNAME'),
    'password': os.getenv('DB_PASSWORD')
}


def get_db_connection():
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={DB_CONFIG['server']},{DB_CONFIG['port']};"
        f"DATABASE={DB_CONFIG['database']};"
        f"UID={DB_CONFIG['username']};"
        f"PWD={DB_CONFIG['password']};"
        "TrustServerCertificate=yes;"
        "LoginTimeout=30;"
        "ConnectRetryCount=3;"
        "ConnectRetryInterval=10"
    )
    print(
        f"Attempting to connect to database: {DB_CONFIG['server']},{DB_CONFIG['port']}")
    try:
        connection = pyodbc.connect(conn_str)
        print("Connection successful!")
        return connection
    except pyodbc.Error as e:
        print(
            f"Connection string used (with password hidden): {conn_str.replace(DB_CONFIG['password'], '****')}")
        print(f"Detailed error: {str(e)}")
        raise


MAX_RETRIES = 3
BATCH_SIZE = 1000


@contextmanager
def get_db_connection_context():
    conn = None
    try:
        conn = get_db_connection()
        yield conn
    finally:
        if conn:
            conn.close()


def test_connection_parameters():
    """Test and print connection parameters"""
    print("\nTesting connection parameters:")
    print(f"Server: {DB_CONFIG['server']}")
    print(f"Port: {DB_CONFIG['port']}")
    print(f"Database: {DB_CONFIG['database']}")
    print(f"Username: {DB_CONFIG['username']}")
    print("Password: [HIDDEN]")

    # Test if all required parameters are present
    required_params = ['server', 'port', 'database', 'username', 'password']
    missing_params = [param for param in required_params if
                      not DB_CONFIG.get(param)]

    if missing_params:
        print(f"❌ Missing required parameters: {', '.join(missing_params)}")
        return False

    return True


def create_tables():
    print("Creating tables...")
    try:
        with get_db_connection_context() as conn:
            cursor = conn.cursor()

            # Create oneliners table
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[oneliners]') AND type in (N'U'))
                CREATE TABLE oneliners (
                    number INT IDENTITY(1,1) PRIMARY KEY,
                    category NVARCHAR(80) NOT NULL,
                    joke NVARCHAR(MAX) NOT NULL
                );
            """)
            conn.commit()
            print("✓ Tables created successfully!")

    except Exception as e:
        print(f"❌ Error creating tables: {str(e)}")
        raise


def load_jokes_from_csv():
    print("Starting to load jokes from CSV...")

    try:
        print("\nReading CSV file...")
        df = pd.read_csv('oneLiners/dad_jokes_oneliners.csv')
        total_jokes = len(df)
        print(f"✓ Found {total_jokes} jokes to insert")

        # Process in batches
        batch_number = 0
        records_processed = 0

        while records_processed < total_jokes:
            retry_count = 0
            success = False

            while not success and retry_count < MAX_RETRIES:
                try:
                    with get_db_connection_context() as conn:
                        cursor = conn.cursor()

                        # Clear existing data only on first batch
                        if batch_number == 0:
                            print("Clearing existing data...")
                            cursor.execute("DELETE FROM oneliners")
                            conn.commit()
                            print("✓ Existing data cleared successfully\n")

                        # Process batch
                        start_idx = records_processed
                        end_idx = min(records_processed + BATCH_SIZE,
                                      total_jokes)
                        batch_df = df.iloc[start_idx:end_idx]

                        print(
                            f"\nProcessing batch {batch_number + 1} (records {start_idx + 1} to {end_idx})...")

                        for _, row in batch_df.iterrows():
                            cursor.execute(
                                "INSERT INTO oneliners (category, joke) VALUES (?, ?)",
                                (row['category'], row['joke'])
                            )
                            records_processed += 1

                            if records_processed % 100 == 0:
                                print(
                                    f"Progress: {records_processed}/{total_jokes} jokes inserted")

                        conn.commit()
                        print(f"✓ Committed batch {batch_number + 1}")
                        success = True
                        batch_number += 1

                except Exception as e:
                    retry_count += 1
                    print(
                        f"\n⚠️ Error on batch {batch_number + 1}, attempt {retry_count}: {str(e)}")
                    if retry_count < MAX_RETRIES:
                        print(f"Retrying in 5 seconds...")
                        time.sleep(5)
                    else:
                        raise Exception(
                            f"Failed to process batch after {MAX_RETRIES} attempts")

        print("\n✓ All jokes inserted successfully!")

        # Final verification
        with get_db_connection_context() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM oneliners")
            final_count = cursor.fetchone()[0]
            print(f"\nFinal verification:")
            print(f"- Total jokes in CSV: {total_jokes}")
            print(f"- Total jokes in database: {final_count}")

    except Exception as e:
        print(f"\n❌ Error loading jokes: {str(e)}")
        raise


def verify_database_content():
    print("\nVerifying database content...")

    try:
        with get_db_connection_context() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM oneliners")
            total = cursor.fetchone()[0]
            print(f"Total jokes in database: {total}")

            cursor.execute("SELECT TOP 3 * FROM oneliners")
            sample = cursor.fetchall()
            print("\nSample of first 3 jokes:")
            for joke in sample:
                print(f"Number: {joke[0]}")
                print(f"Category: {joke[1]}")
                print(f"Joke: {joke[2]}")
                print("-" * 50)

    except Exception as e:
        print(f"❌ Verification error: {str(e)}")


def init_db():
    print("Initializing database...")
    create_tables()
    load_jokes_from_csv()
    verify_database_content()
    print("\nDatabase initialization complete!")


if __name__ == "__main__":
    print("Testing database connection before initialization...")
    if not test_connection_parameters():
        print("❌ Connection parameters check failed!")
        exit(1)

    try:
        # Test connection first
        test_connection = get_db_connection()
        test_connection.close()
        print("✓ Connection test successful!")

        # Proceed with initialization
        init_db()
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
        exit(1)
