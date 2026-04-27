# Job Application Tool

A Python-based job search assistant that aggregates jobs from multiple sources, scores them based on relevance, and matches them against your resume.

## Features

- Multi-source job aggregation (Remotive + Adzuna)
- Location-based and remote job search
- Smart job scoring system
- Resume-to-job matching with keyword analysis
- Missing keyword detection
- Interactive dashboard with filters (Streamlit)

## How It Works

1. Fetch jobs from APIs  
2. Store in a local database  
3. Score jobs based on relevance  
4. Compare each job against your resume  
5. Display top matches in a dashboard  

## Tech Stack

- Python  
- Streamlit  
- SQLAlchemy (SQLite)  
- Pandas  

## Setup

```bash
git clone <your-repo>
cd job-application-tool
```

### Active Virtual Environment

```bash
python -m venv venv
.\venv\Scripts\activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Create .env file

```bash
ADZUNA_APP_ID=your_id
ADZUNA_APP_KEY=your_key
ADZUNA_COUNTRY=us
```

### Run The App
```bash
python -m backend.main
streamlit run frontend/app.py
```

## Demo
<img width="1280" height="668" alt="image" src="https://github.com/user-attachments/assets/e8f3676c-2e6c-4771-a764-3893df78c00d" />
