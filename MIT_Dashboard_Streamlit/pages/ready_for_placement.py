import streamlit as st
import plotly.express as px
from utils.data_loader import load_data

st.set_page_config(page_title="Ready for Placement", layout="wide")
st.title("✅ Ready for Placement Candidates")

df, _ = load_data()
ready_df = df[(df["Week"] > 6) & (~df["Status"].isin(["offer accepted", "offer pending"]))]

if ready_df.empty:
    st.info("No candidates currently ready for placement.")
    st.stop()

for _, row in ready_df.iterrows():
    with st.container():
        st.image(row.get("PhotoURL", "https://via.placeholder.com/120"), width=120)
        st.subheader(row["Trainee Name"])
        st.write(f"🏢 {row.get('Training Site', '')} | 📍 {row.get('Location', '')}")
        st.write(f"💼 {row.get('Title','')} | 💰 {row.get('Salary','')} | Week {int(row['Week'])}")

        if "Readiness Index" in ready_df.columns:
            st.progress(min(row["Readiness Index"]/100, 1.0))
        st.markdown("---")

if "Location" in ready_df.columns and "Readiness Index" in ready_df.columns:
    avg_by_loc = ready_df.groupby("Location")["Readiness Index"].mean().reset_index()
    st.plotly_chart(px.bar(avg_by_loc, x="Location", y="Readiness Index", title="Avg Readiness by Location"))
