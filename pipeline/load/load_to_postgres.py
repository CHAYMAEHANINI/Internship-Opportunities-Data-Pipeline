import os
import json
from pathlib import Path

import psycopg


# --------------------------------------------------
# Paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "internships.json"


# --------------------------------------------------
# Database connection
# --------------------------------------------------

connection = psycopg.connect(
    host=os.getenv("DB_HOST", "localhost"),
    port=os.getenv("DB_PORT", "5433"),
    dbname=os.getenv("DB_NAME", "internship_finder"),
    user=os.getenv("DB_USER", "postgres"),
    password=os.getenv("DB_PASSWORD", "root"),
)


# --------------------------------------------------
# Read processed JSON
# --------------------------------------------------

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    internships = json.load(file)


print(f"Loaded {len(internships)} internships from JSON.")


# --------------------------------------------------
# SQL query
# --------------------------------------------------

query = """
INSERT INTO internships (
    id,
    title,
    company,
    location,
    work_mode,
    stipend,
    internship_type,
    description,
    skills,
    published_at,
    application_deadline,
    url,
    source,
    scraped_at
)
VALUES (
    %(id)s,
    %(title)s,
    %(company)s,
    %(location)s,
    %(work_mode)s,
    %(stipend)s,
    %(internship_type)s,
    %(description)s,
    %(skills)s,
    %(published_at)s,
    %(application_deadline)s,
    %(url)s,
    %(source)s,
    %(scraped_at)s
)
ON CONFLICT (id)
DO UPDATE SET
    title = EXCLUDED.title,
    company = EXCLUDED.company,
    location = EXCLUDED.location,
    work_mode = EXCLUDED.work_mode,
    stipend = EXCLUDED.stipend,
    internship_type = EXCLUDED.internship_type,
    description = EXCLUDED.description,
    skills = EXCLUDED.skills,
    published_at = EXCLUDED.published_at,
    application_deadline = EXCLUDED.application_deadline,
    url = EXCLUDED.url,
    source = EXCLUDED.source,
    scraped_at = EXCLUDED.scraped_at;
"""


# --------------------------------------------------
# Insert / update data
# --------------------------------------------------

with connection.cursor() as cursor:

    for internship in internships:
        cursor.execute(query, internship)


# --------------------------------------------------
# Commit changes
# --------------------------------------------------

connection.commit()

print("Data successfully loaded into PostgreSQL.")


# --------------------------------------------------
# Close connection
# --------------------------------------------------

connection.close()