import streamlit as st
import pandas as pd
from utils.data_loader import load_data, load_jobs_data
from utils.helpers import metric_card

st.set_page_config(page_title="MIT Candidate Training Dashboard", layout="wide")

df, data_source = load_data()
jobs_df = load_jobs_data()

if df.empty:
    st.error("❌ Unable to load candidate data.")
    st.stop()

st.title("🎓 MIT Candidate Training Dashboard")
st.success(f"📊 Data Source: {data_source} | Last Updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")

offer_pending = len(df[df["Status"].str.lower() == "offer pending"])
offer_accepted = len(df[df["Status"].str.lower() == "offer accepted"])
in_training = len(df[(df["Status"].str.lower() == "training") & (df["Week"] <= 6)])
ready = len(df[(df["Week"] > 6) & (~df["Status"].isin(["offer accepted", "offer pending"]))])
total_candidates = len(df[df["Training Program"].isin(["MIT", "SMIT"])])
open_positions = len(jobs_df)

col1, col2, col3, col4, col5 = st.columns(5)
metric_card(col1, "👥 Total Candidates", total_candidates, "pages/all_candidates.py")
metric_card(col2, "🏢 Open Positions", open_positions)
metric_card(col3, "✅ Ready for Placement", ready, "pages/ready_for_placement.py")
metric_card(col4, "📘 In Training (Weeks 1–5)", in_training, "pages/in_training.py")
metric_card(col5, "🤝 Offer Pending", offer_pending)
