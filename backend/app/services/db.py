import psycopg2

def get_connection():
    """
    Connect to PostgreSQL without a password (local, trusted connection)
    """
    return psycopg2.connect(
        dbname="stock_ai",      # Or "postgres" for creating DB
        user="postgres",
        host="localhost",
        port=5432
        # No password here
    )
