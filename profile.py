"""
Your profile config. Update this as your skills and preferences evolve.
The Analyst Agent uses this to score every job listing.
"""

PROFILE = {
    "name": "Nisarg Joshi",
    "target_roles": [
        "AI Engineer", "ML Engineer", "Data Scientist",
        "Junior AI Developer", "Data Engineer", "AI Developer",
        "Machine Learning Engineer", "NLP Engineer", "GenAI Developer"
    ],
    "skills": {
        "strong": [
            "Python", "Machine Learning", "NLP", "BERT", "Sentiment Analysis",
            "RAG Pipelines", "LangChain", "LlamaIndex", "CrewAI", "Groq", "Ollama",
            "TensorFlow", "PyTorch", "Scikit-learn", "Streamlit", "SQL",
            "Google Cloud", "Azure", "Prompt Engineering", "Multi-Agent Systems",
            "PostgreSQL", "SQLAlchemy", "VADER", "HuggingFace"
        ],
        "familiar": [
            "TypeScript", "Docker", "FastAPI", "REST APIs", "Git"
        ]
    },
    "experience_years": 1,
    "education": "Master of Engineering, Electrical & Computer Engineering, University of Windsor (2023-2024)",
    "preferred_locations": ["Vancouver", "Burnaby", "Toronto", "Remote", "Canada"],
    "job_type_preference": ["fulltime", "contract"],
    "red_flags": [
        "5+ years required", "7+ years", "10+ years",
        "Java required", "C++ required",
        "Senior level only", "Lead engineer"
    ],
    "green_flags": [
        "Junior", "Entry level", "1-2 years", "0-2 years",
        "New grad", "GenAI", "LLM", "Agentic", "RAG",
        "Python", "NLP", "AI Developer"
    ]
}


def profile_to_text(profile: dict) -> str:
    """Converts the profile dict into a clean text summary for the LLM."""
    return f"""
Candidate: {profile['name']}
Education: {profile['education']}
Years of Experience: {profile['experience_years']}
Target Roles: {', '.join(profile['target_roles'])}
Strong Skills: {', '.join(profile['skills']['strong'])}
Familiar With: {', '.join(profile['skills']['familiar'])}
Preferred Locations: {', '.join(profile['preferred_locations'])}
Job Type Preference: {', '.join(profile['job_type_preference'])}
Green Flags (good signs in a JD): {', '.join(profile['green_flags'])}
Red Flags (bad signs in a JD): {', '.join(profile['red_flags'])}
""".strip()
