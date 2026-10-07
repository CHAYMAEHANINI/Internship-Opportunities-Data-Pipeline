
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
def get_internships():
    return get_all_internships()
