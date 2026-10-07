from backend.app.database.database import get_connection


def get_all_internships():
    connection = get_connection()

    query = """
        SELECT
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
        FROM internships
        ORDER BY published_at DESC;
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    connection.close()

    internships = []

    for row in rows:
        internships.append({
            "id": row[0],
            "title": row[1],
            "company": row[2],
            "location": row[3],
            "work_mode": row[4],
            "stipend": row[5],
            "internship_type": row[6],
            "description": row[7],
            "skills": row[8],
            "published_at": row[9],
            "application_deadline": row[10],
            "url": row[11],
            "source": row[12],
            "scraped_at": row[13],
        })

    return internships
