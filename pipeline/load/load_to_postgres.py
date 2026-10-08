
import os
import json
from pathlib import Path
from html import escape

import psycopg

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from pipeline.notifications.email_service import send_email


# --------------------------------------------------
# Paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "internships.json"


# --------------------------------------------------
# Database connection
# --------------------------------------------------

def get_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5433"),
        dbname=os.getenv("DB_NAME", "internship_finder"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "root"),
    )


# --------------------------------------------------
# Email notification
# --------------------------------------------------

def notify_new_offer(offer):
    title = offer.get("title") or "New Internship"
    company = offer.get("company") or "Not specified"
    location = offer.get("location") or "Not specified"
    internship_type = offer.get("internship_type") or "Not specified"
    url = offer.get("url") or ""

    subject = f"New Internship: {title}"

    content = f"""
    <html>
      <body>
        <h2>New Internship Opportunity!</h2>
        <p><strong>Title:</strong> {escape(str(title))}</p>
        <p><strong>Company:</strong> {escape(str(company))}</p>
        <p><strong>Location:</strong> {escape(str(location))}</p>
        <p><strong>Type:</strong> {escape(str(internship_type))}</p>
        <p>
          <a href="{escape(str(url), quote=True)}">
            View Internship Offer
          </a>
        </p>
      </body>
    </html>
    """

    send_email(subject=subject, content=content)


# --------------------------------------------------
# SQL: insert new offers only
# --------------------------------------------------

QUERY = """
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
ON CONFLICT (id) DO NOTHING
RETURNING id;
"""


# --------------------------------------------------
# Main loader
# --------------------------------------------------

def load_internships():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        internships = json.load(file)

    print(f"Loaded {len(internships)} internships from JSON.")

    new_offers = []

    with get_connection() as connection:
        with connection.cursor() as cursor:
            for internship in internships:
                cursor.execute(QUERY, internship)

                # PostgreSQL returns an ID only for a new offer.
                if cursor.fetchone() is not None:
                    new_offers.append(internship)

    # The database transaction has committed successfully here.
    print(f"New offers saved: {len(new_offers)}")

    for offer in new_offers:
        try:
            notify_new_offer(offer)
            print(f"Email sent: {offer.get('title')}")
        except Exception as error:
            print(
                f"Email failed for {offer.get('title')}: {error}"
            )

    print("Data loading completed.")


if __name__ == "__main__":
    load_internships()