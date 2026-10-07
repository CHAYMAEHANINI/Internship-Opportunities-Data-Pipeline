from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.services.internship_service import (
    get_all_internships,
    get_locations,
    get_statistics,
)


app = FastAPI(
    title="Internship Opportunities API",
    description="Backend API for the Internship Opportunities Finder",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
@app.get("/locations")
def get_locations_endpoint():
    return {
        "data": get_locations()
    }

@app.get("/stats")
def get_stats():
    return get_statistics()