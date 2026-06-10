"""
Custom CrewAI tool that wraps jobspy to scrape jobs from
LinkedIn, Indeed, Glassdoor, and ZipRecruiter in one call.
"""

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from jobspy import scrape_jobs


class JobScraperInput(BaseModel):
    search_term: str = Field(description="Job title or keywords to search for, e.g. 'AI Engineer'")
    location: str = Field(description="Location to search in, e.g. 'Vancouver, BC' or 'Canada'")
    results_wanted: int = Field(default=15, description="Number of results to fetch per site")
    hours_old: int = Field(default=72, description="Only return jobs posted within this many hours")


class JobScraperTool(BaseTool):
    name: str = "Job Scraper Tool"
    description: str = (
        "Scrapes job listings from LinkedIn, Indeed, Glassdoor, and ZipRecruiter. "
        "Returns a JSON list of job listings with title, company, location, description, and URL."
    )
    args_schema: Type[BaseModel] = JobScraperInput

    def _run(
        self,
        search_term: str,
        location: str,
        results_wanted: int = 15,
        hours_old: int = 72,
    ) -> str:
        try:
            jobs = scrape_jobs(
                site_name=["indeed", "linkedin", "glassdoor", "zip_recruiter"],
                search_term=search_term,
                location=location,
                results_wanted=results_wanted,
                hours_old=hours_old,
                country_indeed="Canada",
                verbose=False,
            )

            if jobs is None or jobs.empty:
                return "No jobs found for the given search criteria."

            # Keep only the columns we care about
            keep_cols = [
                "title", "company", "location", "job_type",
                "date_posted", "description", "job_url", "site"
            ]
            available = [c for c in keep_cols if c in jobs.columns]
            jobs = jobs[available].fillna("")

            # Truncate descriptions to 600 chars to keep token usage manageable
            if "description" in jobs.columns:
                jobs["description"] = jobs["description"].str[:600]

            # Drop exact duplicates (same title + company)
            jobs = jobs.drop_duplicates(subset=["title", "company"])

            return jobs.to_json(orient="records", indent=2)

        except Exception as e:
            return f"Error during scraping: {str(e)}"
