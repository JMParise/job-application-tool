import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))

from backend.database import SessionLocal
from backend.models import Job
from backend.resume_matcher import load_resume_text, calculate_resume_match


st.set_page_config(page_title="Job Application Tool", layout="wide")

st.title("Job Application Tool")
st.subheader("Recommended Jobs")


db = SessionLocal()

jobs = (
    db.query(Job)
    .order_by(Job.match_score.desc())
    .all()
)

data = []
resume_text = load_resume_text()

for job in jobs:
    resume_match, matched_keywords, missing_keywords = calculate_resume_match(resume_text, job)
    
    data.append({
        "Score": job.match_score,
        "Resume Match %": resume_match,
        "Title": job.title,
        "Company": job.company,
        "Location": job.location,
        "Source": job.source,
        "Status": job.status,
        "Missing Keywords": ", ".join(missing_keywords),
        "Link": job.job_url,
    })

db.close()

st.sidebar.header("Filters")

min_score = st.sidebar.slider("Minimum Score", 0, 100, 20)

remote_only = st.sidebar.checkbox("Remote Only")

keyword_filter = st.sidebar.text_input("Keyword (e.g. security, analyst)")

df = pd.DataFrame(data)

# Base filtering
df = df[df["Score"] >= min_score]

# Remove duplicates
df = df.drop_duplicates(subset=["Title", "Company"])

if remote_only:
    df = df[df["Location"].str.lower().str.contains("remote", na=False)]

if keyword_filter:
    df = df[
        df["Title"].str.lower().str.contains(keyword_filter.lower(), na=False)
    ]

df = df.sort_values(by="Score", ascending=False)
df = df.head(50)

if df.empty:
    st.info("No jobs found yet. Run the backend job search first.")
else:
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Link": st.column_config.LinkColumn("Job Link")
        }
    )