
from fastapi import FastAPI

from backend.app.services.internship_service import (
    get_all_internships,
)


app = FastAPI(
    title="Internship Opportunities API",
    description="Backend API for the Internship Opportunities Finder",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "Internship Opportunities API is running"
    }


@app.get("/internships")
def get_internships(
    location: str | None = None,
    source: str | None = None,
    work_mode: str | None = None,
    internship_type: str | None = None,
    search: str | None = None,
    page: int = 1,
    limit: int = 10
):
    return get_all_internships(
       location=location,
       source=source,
       work_mode=work_mode,
       internship_type=internship_type,
       search=search,
       page=page,
       limit=limit
)