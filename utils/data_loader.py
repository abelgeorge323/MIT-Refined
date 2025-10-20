import pandas as pd
import streamlit as st

@st.cache_data(ttl=120)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR0w31eBwBrasgaLS2h9e_Bj8GWC0SqikQ0R_cuV0_B12HxOzDPLJrZm8MWaNf-7zudxrrZfLXNPR3L/pub?gid=0&single=true&output=csv"
    try:
        df = pd.read_csv(url)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame(), "Error"

    df.columns = df.columns.str.strip()
    df = df[df["Training Program"].isin(["MIT", "SMIT"])]

    for col in ["Week", "Mock QBR Score", "Assessment Score", "Perf Evaluation Score", "Confidence Score", "Skill Ranking"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df["Status"] = df["Status"].astype(str).str.lower().fillna("")
    df["Salary"] = df["Salary"].astype(str).str.replace("$", "").str.replace(",", "").replace("nan", "")
    return df, "Google Sheets"

@st.cache_data(ttl=120)
def load_jobs_data():
    try:
        url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSbD6wUrZEt9kuSQpUT2pw0FMOb7h1y8xeX-hDTeiiZUPjtV0ohK_WcFtCSt_4nuxdtn9zqFS8z8aGw/pub?gid=116813539&single=true&output=csv"
        df = pd.read_csv(url)
        return df
    except Exception:
        return pd.DataFrame()
