# 🤖 Job Scraper Agent

A 3-agent CrewAI pipeline that scrapes job listings from LinkedIn, Indeed, Glassdoor, and ZipRecruiter, scores each one against your profile, and delivers a ranked digest.

**Built with:** CrewAI · JobSpy · Groq (llama-3.3-70b) · Streamlit

---

## Architecture

```
Streamlit UI
     │
     ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Scraper Agent│────▶│Analyst Agent │────▶│Reporter Agent│
│              │     │              │     │              │
│ Uses JobSpy  │     │ Scores 0-100 │     │ Markdown     │
│ tool to pull │     │ against your │     │ digest with  │
│ raw listings │     │ profile      │     │ ranked cards │
└──────────────┘     └──────────────┘     └──────────────┘
```

**Score breakdown per job:**
- Skills match: 0–40 pts
- Seniority fit: 0–25 pts
- Role alignment: 0–20 pts
- Location fit: 0–15 pts

---

## Setup

### 1. Clone / download the project

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your Groq API key
```bash
cp .env.example .env
# Open .env and paste your key from https://console.groq.com
```

### 5. Run the app
```bash
streamlit run app.py
```

---

## Updating Your Profile

Open `profile.py` and edit the `PROFILE` dict:
- Add new skills to `skills.strong` as you learn them
- Update `preferred_locations` if you move
- Adjust `red_flags` / `green_flags` to tune scoring

---

## Known Limitations

- LinkedIn and Glassdoor may occasionally block scrapers — Indeed and ZipRecruiter are more reliable
- Job descriptions are truncated to 600 characters before LLM analysis (keeps API costs low)
- Results depend on how recently jobs were posted; try increasing `hours_old` if results are thin
