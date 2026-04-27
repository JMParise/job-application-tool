from backend.database import SessionLocal
from backend.models import Job


POSITIVE_KEYWORDS = [
    "cybersecurity",
    "security",
    "soc",
    "analyst",
    "systems analyst",
    "system analyst",
    "data analyst",
    "software developer",
    "software engineer",
    "developer",
    "python",
    "javascript",
    "sql",
    "linux",
    "network",
    "help desk",
    "it support",
    "entry level",
    "junior",
    "intern",
    "internship",
]

NEGATIVE_KEYWORDS = [
    "sr",
    "Sr",
    "senior",
    "lead",
    "manager",
    "principal",
    "staff",
    "director",
    "5+ years",
    "6+ years",
    "7+ years",
    "8+ years",
    "10+ years",
    "sales",
    "marketing",
]


def score_job(job):
    score = 0

    text = f"{job.title} {job.description} {job.location}".lower()

    for keyword in NEGATIVE_KEYWORDS:
        if keyword in text:
            return 0

    for keyword in POSITIVE_KEYWORDS:
        if keyword in text:
            score += 15

    if "entry level" in text or "junior" in text or "intern" in text:
        score += 25

    if "remote" in text:
        score += 5

    return score


def score_all_jobs():
    db = SessionLocal()
    jobs = db.query(Job).all()

    for job in jobs:
        job.match_score = score_job(job)

    db.commit()
    db.close()

    print(f"Scored {len(jobs)} jobs.")