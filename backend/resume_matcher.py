from backend.database import SessionLocal
from backend.models import Job


IMPORTANT_KEYWORDS = [
    "python", "sql", "excel", "linux", "windows",
    "network", "networking", "cybersecurity", "security",
    "soc", "siem", "splunk", "incident response",
    "data analysis", "data analyst", "tableau", "power bi",
    "software", "developer", "javascript", "html", "css",
    "api", "git", "github", "fastapi", "streamlit",
]


def load_resume_text(path="resumes/resume.txt"):
    with open(path, "r", encoding="utf-8") as file:
        return file.read().lower()


def get_keyword_matches(resume_text, job_text):
    matched = []
    missing = []

    for keyword in IMPORTANT_KEYWORDS:
        if keyword in job_text:
            if keyword in resume_text:
                matched.append(keyword)
            else:
                missing.append(keyword)

    return matched, missing


def calculate_resume_match(resume_text, job):
    job_text = f"{job.title} {job.description}".lower()

    matched, missing = get_keyword_matches(resume_text, job_text)

    total = len(matched) + len(missing)

    if total == 0:
        return 0, matched, missing

    match_score = round((len(matched) / total) * 100)

    return match_score, matched, missing


def match_resume_to_jobs():
    resume_text = load_resume_text()

    db = SessionLocal()
    jobs = (
    db.query(Job)
    .filter(Job.match_score >= 20)
    .order_by(Job.match_score.desc())
    .all()
    )

    results = []

    for job in jobs:
        score, matched, missing = calculate_resume_match(resume_text, job)

        results.append({
            "job_id": job.id,
            "title": job.title,
            "company": job.company,
            "resume_match": score,
            "matched_keywords": matched,
            "missing_keywords": missing,
        })

    db.close()

    return results

if __name__ == "__main__":
    results = match_resume_to_jobs()

    for result in results[:10]:
        print(result)