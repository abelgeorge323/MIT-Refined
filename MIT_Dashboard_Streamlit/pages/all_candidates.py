import streamlit as st
from utils.data_loader import load_data

st.set_page_config(page_title="All Candidates", layout="wide")
st.title("👥 All MIT/SMIT Candidates")

df, _ = load_data()

status_filter = st.multiselect("Filter by Status", options=df["Status"].unique(), default=df["Status"].unique())
loc_filter = st.multiselect("Filter by Location", options=df["Location"].dropna().unique())

filtered_df = df[(df["Status"].isin(status_filter))]
if loc_filter:
    filtered_df = filtered_df[filtered_df["Location"].isin(loc_filter)]

st.dataframe(filtered_df, use_container_width=True, hide_index=True)
