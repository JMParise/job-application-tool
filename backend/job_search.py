import requests
from backend.database import SessionLocal
from backend.models import Job
import os
from dotenv import load_dotenv

load_dotenv()


def fetch_jobs(keyword="cybersecurity", location="remote"):
    """
    Fetch jobs from a simple public API (Remotive)
    """
    url = f"https://remotive.com/api/remote-jobs?search={keyword}"

    response = requests.get(url)
    data = response.json()

    jobs = data.get("jobs", [])

    db = SessionLocal()

    new_jobs = 0

    for job in jobs:
        # Avoid duplicates by URL
        existing = db.query(Job).filter(Job.job_url == job["url"]).first()
        if existing:
            continue

        new_job = Job(
            title=job["title"],
            company=job["company_name"],
            location=job["candidate_required_location"],
            job_url=job["url"],
            description=job["description"],
            source="Remotive"
        )

        db.add(new_job)
        new_jobs += 1

    db.commit()
    db.close()

    print(f"Added {new_jobs} new jobs.")

def fetch_adzuna_jobs(keyword="data analyst", location="Danbury, CT"):
    app_id = os.getenv("ADZUNA_APP_ID")
    app_key = os.getenv("ADZUNA_APP_KEY")
    country = os.getenv("ADZUNA_COUNTRY", "us")

    if not app_id or not app_key:
        print("Missing Adzuna API credentials.")
        return

    url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"

    params = {
        "app_id": app_id,
        "app_key": app_key,
        "what": keyword,
        "where": location,
        "results_per_page": 25,
        "content-type": "application/json",
    }

    response = requests.get(url, params=params)
    data = response.json()

    jobs = data.get("results", [])

    db = SessionLocal()
    new_jobs = 0

    for job in jobs:
        job_url = job.get("redirect_url")

        if not job_url:
            continue

        existing = db.query(Job).filter(Job.job_url == job_url).first()
        if existing:
            continue

        new_job = Job(
            title=job.get("title", "Unknown Title"),
            company=job.get("company", {}).get("display_name", "Unknown Company"),
            location=job.get("location", {}).get("display_name", location),
            job_url=job_url,
            description=job.get("description", ""),
            source="Adzuna",
        )

        db.add(new_job)
        new_jobs += 1

    db.commit()
    db.close()

    print(f"Added {new_jobs} new Adzuna jobs for {keyword} in {location}.")