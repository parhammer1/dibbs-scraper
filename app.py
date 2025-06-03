"""Streamlit app to view DIBBS data from CSV."""

import os
from datetime import datetime

import pandas as pd
import streamlit as st

DATA_PATH = "data/dibbs_data.csv"

st.set_page_config(page_title="DIBBS Data Viewer", layout="wide")
st.title("DIBBS Data Viewer")

if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)
    last_updated = datetime.fromtimestamp(os.path.getmtime(DATA_PATH))
    st.write(f"Last updated: {last_updated.strftime('%Y-%m-%d %H:%M:%S')}")
else:
    df = pd.DataFrame()
    st.write("No data found. Run the scraper to generate dibbs_data.csv.")

fsc_filter = st.text_input("Filter by FSC")
nsn_filter = st.text_input("Filter by NSN")
quantity_filter = st.number_input("Minimum Quantity", min_value=0, value=0)

filtered = df.copy()
if not df.empty:
    if fsc_filter:
        filtered = filtered[filtered["fsc"].astype(str).str.contains(fsc_filter)]
    if nsn_filter:
        filtered = filtered[filtered["nsn"].astype(str).str.contains(nsn_filter)]
    if quantity_filter:
        filtered = filtered[filtered["quantity"] >= quantity_filter]

st.dataframe(filtered)
