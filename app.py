"""Streamlit web interface for the DIBBS scraper and AI tools."""

import pandas as pd
import streamlit as st

from dibbs_scraper import scrape_latest
from database import init_db, insert_solicitation, fetch_all
from ai_utils import summarize_solicitation, generate_email

# Initialize database on startup
init_db()

st.set_page_config(page_title="DIBBS Scraper", layout="wide")

st.title("DIBBS Scraper and Analyzer")

if st.button("Scrape Latest Solicitations"):
    with st.spinner("Scraping..."):
        items = scrape_latest(limit=5)
        for item in items:
            insert_solicitation(item)
        st.success(f"Scraped {len(items)} items and stored them in the database.")

# Fetch data from database
solicitations = fetch_all()
if solicitations:
    df = pd.DataFrame(solicitations)
    st.subheader("Stored Solicitations")
    st.dataframe(df)

    selected = st.selectbox(
        "Select a solicitation for AI analysis",
        options=df["solicitation"],
    )
    record = next((s for s in solicitations if s["solicitation"] == selected), None)
    if record:
        if st.button("Summarize Solicitation"):
            summary = summarize_solicitation(record.get("description", ""))
            st.write(summary)
        if st.button("Generate Outreach Email"):
            email = generate_email(record)
            st.text_area("Draft Email", value=email, height=200)
else:
    st.info("No data available. Click 'Scrape Latest Solicitations' to begin.")
