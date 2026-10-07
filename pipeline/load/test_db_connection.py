import psycopg


connection = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="internship_finder",
    user="postgres",
    password="root",
)

print("Database connection successful!")

connection.close()