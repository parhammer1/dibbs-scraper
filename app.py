"""Streamlit interface for scraping and analyzing DIBBS solicitations."""

import streamlit as st

from scraper import run_scraper
from db_utils import fetch_solicitations, get_solicitation_details
from openai_utils import summarize_solicitation, generate_outreach_email

st.set_page_config(page_title="DIBBS Scraper", layout="wide")

st.title("DIBBS Scraper and Analyzer")

# Run scraper button
if st.button("Run Scraper"):
    st.write("Scraping DIBBS...")
    run_scraper()
    st.success("Scraping complete!")

# Filter inputs
filter_fsc = st.text_input("Filter by FSC")
filter_nsn = st.text_input("Filter by NSN")

data = fetch_solicitations(filter_fsc, filter_nsn)

if data:
    options = [row["solicitation"] for row in data]
    selected = st.selectbox("Select a Solicitation", options)
    selected_data = get_solicitation_details(selected)

    st.write("### Solicitation Details")
    st.json(selected_data)

    if st.button("Summarize with GPT"):
        summary = summarize_solicitation(selected_data.get("description", ""))
        st.write("#### GPT Summary")
        st.write(summary)

    if st.button("Generate Outreach Email"):
        email = generate_outreach_email(selected_data)
        st.write("#### Draft Email")
        st.code(email)
else:
    st.write("No solicitations found.")
