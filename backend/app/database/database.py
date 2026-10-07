import psycopg


DATABASE_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "internship_finder",
    "user": "postgres",
    "password": "root",
}


def get_connection():
    return psycopg.connect(**DATABASE_CONFIG)

