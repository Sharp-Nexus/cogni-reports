import pg8000
import os

def get_db_connection():
    """
    Creates and returns a database connection using environment variables.
    Returns None if connection fails.
    """
    try:
        connection = pg8000.connect(
            host=os.environ.get('DB_HOST'),
            database=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD')
        )
        return connection
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None 