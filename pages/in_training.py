import streamlit as st
from utils.data_loader import load_data

st.set_page_config(page_title="In Training", layout="wide")
st.title("📘 In Training (Weeks 1–5)")

df, _ = load_data()
train_df = df[(df["Status"].str.lower() == "training") & (df["Week"] <= 6)]

if train_df.empty:
    st.info("No trainees currently in early training.")
    st.stop()

for _, row in train_df.iterrows():
    with st.container():
        st.image(row.get("PhotoURL", "https://via.placeholder.com/120"), width=120)
        st.subheader(row["Trainee Name"])
        st.write(f"Week {int(row['Week'])}/5 | Mentor: {row.get('Mentor Name','')}")
        st.progress(min(row["Week"]/5, 1.0))
        st.markdown("---")
