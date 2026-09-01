import os
import json
from groq import Groq
from jobspy import scrape_jobs as jobspy_scrape
from profile import PROFILE, profile_to_text


def scrape(search_term, location, results_wanted=10):
    print(f"[Scraper] Fetching jobs for '{search_term}' in '{location}'...")
    jobs = jobspy_scrape(
        site_name=["indeed", "linkedin", "zip_recruiter"],
        search_term=search_term,
        location=location,
        results_wanted=results_wanted,
        hours_old=72,
        country_indeed="Canada",
        verbose=False,
    )
    if jobs is None or jobs.empty:
        return []
    keep = ["title", "company", "location", "job_type", "date_posted", "description", "job_url", "site"]
    available = [c for c in keep if c in jobs.columns]
    jobs = jobs[available].fillna("")
    jobs = jobs.drop_duplicates(subset=["title", "company"])
    if "description" in jobs.columns:
        jobs["description"] = jobs["description"].str[:250]
    if "date_posted" in jobs.columns:
        jobs["date_posted"] = jobs["date_posted"].astype(str)
    result = jobs.to_dict(orient="records")
    result = [{k: str(v) if hasattr(v, "isoformat") else v for k, v in job.items()} for job in result]
    # Cap at 8 to stay within Groq's on-demand tier TPM limit (8000 tokens/request)
    result = result[:8]
    print(f"[Scraper] Found {len(result)} jobs.")
    return result


def analyse(jobs):
    if not jobs:
        return []
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    profile_summary = profile_to_text(PROFILE)
    print(f"[Analyst] Scoring {len(jobs)} jobs...")
    prompt = f"""
You are a technical recruiter scoring job listings for a candidate.

Candidate profile:
{profile_summary}

Here are the job listings in JSON:
{json.dumps(jobs, indent=2)}

For EACH job, return a JSON object with:
- title, company, location, site, job_url
- score: integer 0-100
- reasoning: 1-2 sentences explaining the score
- green_flags: list of up to 3 matching positives
- red_flags: list of up to 3 concerns

Return ONLY a valid JSON array sorted by score descending.
No markdown, no explanation, just the raw JSON array.
Keep each reasoning field short (under 30 words).
"""
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=3000,
    )
    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1]
        raw = raw.rsplit("```", 1)[0]
    try:
        scored = json.loads(raw)
    except json.JSONDecodeError:
        # Try to salvage partial JSON
        try:
            last_brace = raw.rfind("},")
            if last_brace > 0:
                raw = raw[:last_brace + 1] + "]"
                scored = json.loads(raw)
            else:
                return []
        except Exception:
            return []
    print("[Analyst] Scoring complete.")
    return scored


def generate_report(scored_jobs, search_term, location):
    if not scored_jobs:
        return "## No jobs found. Try a different search term or location."
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    print("[Reporter] Generating digest...")
    prompt = f"""
You are producing a job digest report. Here are scored job listings in JSON:
{json.dumps(scored_jobs[:8], indent=2)}

Produce a clean markdown report:

## Job Match Report
**Search:** {search_term} | **Location:** {location}

---

For the TOP 10 jobs by score:

### [Rank]. [Job Title] — [Company]
**Score:** [score]/100 | **Location:** [location] | **Source:** [site]
**[Apply Here]([job_url])**

**Why it matches:** [reasoning]

**Green Flags:** [green_flags joined by comma or None]
**Red Flags:** [red_flags joined by comma or None]

---

End with a **Summary**:
- Total jobs analysed
- Jobs scoring 70+
- Top pick
- One sentence of advice
"""
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=3000,
    )
    return response.choices[0].message.content.strip()


def run_pipeline(search_term, location, results_wanted=10):
    jobs = scrape(search_term, location, results_wanted)
    if not jobs:
        return "## No jobs found. Try a different search term or location."
    scored = analyse(jobs)
    report = generate_report(scored, search_term, location)
    return report
