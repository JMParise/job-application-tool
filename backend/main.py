from backend.database import Base, engine
from backend.job_search import fetch_jobs
from backend.scoring import score_all_jobs
from backend.job_search import fetch_jobs, fetch_adzuna_jobs


SEARCH_TERMS = [
    "cybersecurity analyst",
    "soc analyst",
    "security analyst",
    "it support",
    "help desk",
    "systems analyst",
    "data analyst",
    "software developer",
    "software engineer",
    "junior developer",
    "entry level developer",
    "computer science internship",
    "software engineering internship",
    "data analyst internship",
]

LOCATIONS = [
    "Danbury, CT",
    "Stamford, CT",
    "Norwalk, CT",
    "Hartford, CT",
    "New York, NY",
]


def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database created successfully.")


if __name__ == "__main__":
    init_db()

    for term in SEARCH_TERMS:
        print(f"Searching Remotive for: {term}")
        fetch_jobs(keyword=term)

    for term in SEARCH_TERMS:
        for location in LOCATIONS:
            print(f"Searching Adzuna for: {term} in {location}")
            fetch_adzuna_jobs(keyword=term, location=location)

    score_all_jobs()