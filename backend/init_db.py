from utils.db import db  # Import the db instance
import os

def create_tables():
    """Function to create tables in the database"""
    CREATE_TABLES_SQL_PATH = os.getenv('CREATE_TABLES_SQL_PATH', 'sql/create_tables.sql')
    try:
        with open(CREATE_TABLES_SQL_PATH, 'r') as f:
            sql_script = f.read()
            db.engine.execute(sql_script)  # Execute the SQL commands to create tables
            print("Tables created successfully!")
    except FileNotFoundError:
        print(f"Error: The file {CREATE_TABLES_SQL_PATH} does not exist.")
    except Exception as e:
        print(f"An error occurred while executing the SQL: {str(e)}")