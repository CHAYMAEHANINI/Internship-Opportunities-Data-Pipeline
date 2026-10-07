from backend.app.database.database import get_connection
import math

def get_all_internships(location=None, source=None , work_mode=None , internship_type=None , search=None , page=1, limit=10):

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
    """

    conditions = []
    parameters = {}

    # Optional location filter
    if location:
        conditions.append("location ILIKE %(location)s")
        parameters["location"] = f"%{location}%"

    # Optional source filter
    if source:
        conditions.append("source ILIKE %(source)s")
        parameters["source"] = f"%{source}%"

    # Optional work mode filter
    if work_mode:
        conditions.append("work_mode ILIKE %(work_mode)s")
        parameters["work_mode"] = f"%{work_mode}%"

    # Optional internship type filter
    if internship_type:
        conditions.append("internship_type ILIKE %(internship_type)s")
        parameters["internship_type"] = f"%{internship_type}%"

    # Optional search
    if search:
        conditions.append("""
            (
                title ILIKE %(search)s
                OR company ILIKE %(search)s
                OR description ILIKE %(search)s
                OR skills ILIKE %(search)s
            )
        """)
        parameters["search"] = f"%{search}%"
    
    # Add WHERE only if filters exist
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    count_query = """
        SELECT COUNT(*)
        FROM internships
    """

    if conditions:
        count_query += " WHERE " + " AND ".join(conditions)

    with connection.cursor() as cursor:
         cursor.execute(count_query, parameters)
         total = cursor.fetchone()[0]
    total_pages = math.ceil(total / limit)

    offset = (page - 1) * limit

    query += """
       ORDER BY published_at DESC
       LIMIT %(limit)s
       OFFSET %(offset)s;
     """

    parameters["limit"] = limit
    parameters["offset"] = offset

    with connection.cursor() as cursor:
        cursor.execute(query, parameters)
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

    return {
        "data": internships,
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages
    }