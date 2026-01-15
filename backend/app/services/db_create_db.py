import psycopg2

# Connect to default database 'postgres' first
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="your_password_here",
    host="localhost",
    port=5432
)
conn.autocommit = True  # Needed to CREATE DATABASE
cur = conn.cursor()

# Create 'stock_ai' database if it doesn't exist
cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'stock_ai'")
exists = cur.fetchone()
if not exists:
    cur.execute("CREATE DATABASE stock_ai")
    print("Database 'stock_ai' created!")
else:
    print("Database 'stock_ai' already exists.")

cur.close()
conn.close()
