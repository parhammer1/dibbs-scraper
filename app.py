"""Streamlit app to view DIBBS data from SQLite."""

import os
from datetime import datetime

import pandas as pd
import streamlit as st

from db_utils import fetch_solicitations, DB_PATH

st.set_page_config(page_title="DIBBS Data Viewer", layout="wide")
st.title("DIBBS Data Viewer")

if os.path.exists(DB_PATH):
    records = fetch_solicitations()
    df = pd.DataFrame(records)
    last_updated = datetime.fromtimestamp(os.path.getmtime(DB_PATH))
    st.write(f"Last updated: {last_updated.strftime('%Y-%m-%d %H:%M:%S')}")
else:
    df = pd.DataFrame()
    st.write("No data found. Run the scraper to generate solicitations.db.")

fsc_filter = st.text_input("Filter by FSC")
nsn_filter = st.text_input("Filter by NSN")

filtered = df.copy()
if not df.empty:
    if fsc_filter:
        filtered = filtered[filtered["fsc"].astype(str).str.contains(fsc_filter)]
    if nsn_filter:
        filtered = filtered[filtered["nsn"].astype(str).str.contains(nsn_filter)]

st.dataframe(filtered)
