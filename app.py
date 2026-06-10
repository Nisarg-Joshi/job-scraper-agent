import streamlit as st
import os
from dotenv import load_dotenv
from crew import run_pipeline
from profile import PROFILE

load_dotenv()

st.set_page_config(page_title="Job Scraper Agent", page_icon="🤖", layout="wide")

st.markdown('<h1>🤖 Job Scraper Agent</h1>', unsafe_allow_html=True)
st.markdown('<p>Scrapes Indeed, LinkedIn & ZipRecruiter · Scores every job · Ranks your best opportunities</p>', unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Search Settings")
    search_term = st.text_input("Job Title / Keywords", value="AI Engineer")
    location = st.text_input("Location", value="Canada")
    results_per_site = st.slider("Results per job portal", 5, 25, 10)

    st.divider()
    st.header("👤 Your Profile")
    st.markdown(f"**{PROFILE['name']}**")

    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key:
        st.warning("⚠️ GROQ_API_KEY not found in .env")
    else:
        st.success("✅ GROQ API key loaded")

    run_button = st.button("🚀 Run Agent", type="primary")

if run_button:
    if not os.getenv("GROQ_API_KEY"):
        st.error("Please add your GROQ_API_KEY to the .env file.")
        st.stop()

    st.info(f"🔍 Searching for **{search_term}** in **{location}**")

    with st.spinner("Running pipeline: Scraping → Analysing → Reporting..."):
        try:
            report = run_pipeline(search_term, location, results_per_site)
            st.success("✅ Done!")
            st.divider()
            st.markdown(report)
            st.download_button(
                label="⬇️ Download Report",
                data=report,
                file_name=f"job_report_{search_term.replace(' ', '_')}.md",
                mime="text/markdown",
            )
        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")
            st.exception(e)
else:
    st.markdown("""
### How it works
1. Configure your search in the sidebar
2. Hit Run Agent
3. Scraper pulls listings from Indeed, LinkedIn & ZipRecruiter
4. Analyst scores each job 0-100 against your profile
5. Reporter gives you a ranked digest with apply links
""")