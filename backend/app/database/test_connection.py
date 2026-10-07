from backend.app.database.database import get_connection


connection = get_connection()

print("FastAPI database connection successful!")

connection.close()
