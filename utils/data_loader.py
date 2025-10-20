import pandas as pd
import streamlit as st


@st.cache_data(ttl=120)
def load_data():
    """
    Load and preprocess candidate roster data from Google Sheets (2025 Leadership Program Roster).
    Handles differences in column names across versions (MIT, SMIT, etc.).
    """

    data_url = (
        "https://docs.google.com/spreadsheets/d/e/"
        "2PACX-1vR0w31eBwBrasgaLS2h9e_Bj8GWC0SqikQ0R_cuV0_B12HxOzDPLJrZm8MWaNf-7zudxrrZfLXNPR3L/"
        "pub?gid=0&single=true&output=csv"
    )

    try:
        df = pd.read_csv(data_url)
        df = df.dropna(how="all")
    except Exception as e:
        st.error(f"❌ Error loading data from Google Sheets: {e}")
        return pd.DataFrame(), "Error"

    # --- Normalize column names ---
    df.columns = [str(c).strip() for c in df.columns]

    # --- Identify key columns dynamically ---
    def find_col(possible_names):
        for col in df.columns:
            if col.strip().lower() in [n.lower() for n in possible_names]:
                return col
        return None

    status_col = find_col(["Status", "Program Status", "Current Status", "Candidate Status"])
    week_col = find_col(["Week", "Training Week", "Current Week", "Week #"])
    salary_col = find_col(["Salary", "Target Salary", "Expected Salary"])
    name_col = find_col(["MIT Name", "Candidate Name", "Name"])
    site_col = find_col(["Training Site", "Site", "Location Site"])
    location_col = find_col(["Location", "City", "Work Location"])
    start_col = find_col(["Start Date", "Training Start", "Date Started"])

    # --- Create canonical columns for dashboard ---
    if name_col: df["MIT Name"] = df[name_col]
    if site_col: df["Training Site"] = df[site_col]
    if location_col: df["Location"] = df[location_col]

    # --- Parse start date & calculate week if missing ---
    if start_col and start_col in df.columns:
        df["Start Date"] = pd.to_datetime(df[start_col], errors="coerce")
    else:
        df["Start Date"] = pd.NaT

    today = pd.Timestamp.now()

    if week_col and week_col in df.columns:
        df["Week"] = pd.to_numeric(df[week_col], errors="coerce")
    else:
        df["Week"] = (today - df["Start Date"]).dt.days // 7
        df["Week"] = df["Week"].fillna(0)

    # --- Handle status ---
    if status_col:
        df["Status"] = df[status_col].astype(str).str.lower().fillna("")
    else:
        df["Status"] = ""

    # --- Handle salary normalization ---
    if salary_col and salary_col in df.columns:
        df["Salary"] = (
            df[salary_col]
            .astype(str)
            .str.replace("$", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.replace("k", "000", regex=False)
        )
        df["Salary"] = pd.to_numeric(df["Salary"], errors="coerce")
    else:
        df["Salary"] = pd.NA

    # --- Filter only MIT or SMIT candidates ---
    training_col = find_col(["Training Program", "Program Type", "Program"])
    if training_col:
        df = df[df[training_col].astype(str).str.upper().isin(["MIT", "SMIT"])]

    # --- Basic validation ---
    df = df.reset_index(drop=True)
    if df.empty:
        st.warning("⚠️ No MIT/SMIT candidates found in the dataset.")

    return df, "Google Sheets"


@st.cache_data(ttl=120)
def load_jobs_data():
    """
    Load open job postings from Google Sheets.
    """
    jobs_url = (
        "https://docs.google.com/spreadsheets/d/e/"
        "2PACX-1vSbD6wUrZEt9kuSQpUT2pw0FMOb7h1y8xeX-hDTeiiZUPjtV0ohK_WcFtCSt_4nuxdtn9zqFS8z8aGw/"
        "pub?gid=116813539&single=true&output=csv"
    )

    try:
        jobs_df = pd.read_csv(jobs_url, skiprows=5)
        jobs_df = jobs_df.loc[:, ~jobs_df.columns.str.contains("^Unnamed")]
        jobs_df = jobs_df.dropna(how="all").fillna("")
    except Exception as e:
        st.error(f"❌ Error loading jobs data: {e}")
        return pd.DataFrame()

    # Clean and rename
    jobs_df.columns = [c.strip() for c in jobs_df.columns]
    if "Job Title" not in jobs_df.columns and "Title" in jobs_df.columns:
        jobs_df = jobs_df.rename(columns={"Title": "Job Title"})

    return jobs_df
