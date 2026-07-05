import streamlit as st
import json
import pandas as pd
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Admin Dashboard - PII Logs",
    page_icon="🔐",
    layout="wide",
)

# ---------------- LOAD LOGS ----------------
def load_logs():
    try:
        with open("../gateway/incidents.json", "r") as f:
            data = json.load(f)
        return pd.DataFrame(data)
    except FileNotFoundError:
        st.error("❌ `incidents.json` not found. Check path: `../gateway/incidents.json`.")
        return None
    except Exception as e:
        st.error(f"❌ Error loading logs: `{e}`")
        return None

# ---------------- HEADER ----------------
st.title("🔐 Admin Dashboard - PII Logs")
st.caption("Review and filter PII‑related incidents from the gateway.")

df = load_logs()

if df is None or len(df) == 0:
    st.warning("No logs are available yet.")
    st.stop()

# Ensure timestamp is datetime and sort newest first
if "timestamp" in df.columns:
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.sort_values("timestamp", ascending=False)

# ---------------- OVERVIEW METRICS ----------------
st.subheader("📊 Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Logs", len(df))
col2.metric("High Risk", len(df[df["risk_level"] == "HIGH"]))
col3.metric("Medium Risk", len(df[df["risk_level"] == "MEDIUM"]))
col4.metric("Low Risk", len(df[df["risk_level"] == "LOW"]))

# Risk‑level bar chart (optional)
if "risk_level" in df.columns:
    risk_counts = df["risk_level"].value_counts().sort_index()
    st.bar_chart(risk_counts, use_container_width=True)

st.divider()

# ---------------- FILTERS ----------------
st.subheader("🔍 Filter Logs")

# Multi‑column layout for filters
col1, col2, col3 = st.columns(3)

with col1:
    risk_filter = st.selectbox(
        "Risk Level",
        ["ALL", "LOW", "MEDIUM", "HIGH"],
        index=0,
    )

with col2:
    # Optional: endpoint filter if present
    if "endpoint" in df.columns:
        endpoints = ["ALL"] + sorted(df["endpoint"].dropna().unique().tolist())
        endpoint_filter = st.selectbox("Endpoint", endpoints)
    else:
        endpoint_filter = "ALL"

with col3:
    # Optional: user filter if present
    if "user" in df.columns:
        users = ["ALL"] + sorted(df["user"].dropna().unique().tolist())
        user_filter = st.selectbox("User", users)
    else:
        user_filter = "ALL"

# Free‑text search across all string columns
search = st.text_input(
    "Search by user, action, IP, or any text (case‑insensitive)",
    placeholder="e.g., 'admin', '192.168', 'login'",
    help="Search across all text fields (case‑insensitive partial match).",
).strip()

# Apply filters
filtered_df = df.copy()

if risk_filter != "ALL":
    filtered_df = filtered_df[filtered_df["risk_level"] == risk_filter]

if endpoint_filter != "ALL" and "endpoint" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["endpoint"] == endpoint_filter]

if user_filter != "ALL" and "user" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["user"] == user_filter]

if search:
    # Apply search on any column that is text‑like
    mask = (
        filtered_df.astype(str)
        .apply(lambda row: row.str.contains(search, case=False, na=False).any(), axis=1)
    )
    filtered_df = filtered_df[mask]

st.write(f"**Found {len(filtered_df)} matching records.**")

# ---------------- MASKED PII PREVIEW ----------------
#st.markdown("### 🔐 Masked PII Preview")

#if "masked_text" in filtered_df.columns:
#    valid_df = filtered_df.dropna(subset=["masked_text"])

#for i, row in valid_df.head(5).iterrows():
#    st.code(row["masked_text"], language="text")
#    st.code(row["masked_text"], language="text")
#else:
#    st.info("No masked data available yet.")
    
# ---------------- ORIGINAL VS MASKED ----------------
st.markdown("### 🆚 Original vs Masked (Preview)")

if "original_text" in filtered_df.columns and "masked_text" in filtered_df.columns:
    
    valid_df = filtered_df.dropna(subset=["original_text", "masked_text"])

    for i, row in valid_df.head(3).iterrows():
        col1, col2 = st.columns(2)

        with col1:
            st.caption("Original")
            st.code(row["original_text"])

        with col2:
            st.caption("Masked")
            st.code(row["masked_text"])

# ---------------- PAGINATION ----------------
st.markdown("### 📄 Logs Table (Paginated)")

col1, col2 = st.columns([1, 4])

with col1:
    page_size = st.slider("Rows per page", min_value=5, max_value=100, value=10)

total_pages = max(1, (len(filtered_df) + page_size - 1) // page_size)
page_num = st.number_input(
    "Page",
    min_value=1,
    max_value=total_pages,
    value=1,
    step=1,
    help="Navigate between pages of logs.",
)

start = (page_num - 1) * page_size
end = start + page_size
paginated_df = filtered_df.iloc[start:end].copy()

# Wrap long text in cells
st.markdown(
    """
    <style>
    div[data-testid="stDataFrame"] div[role="gridcell"] {
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: unset !important;
        line-height: 1.4 !important;
        padding-top: 8px !important;
        padding-bottom: 8px !important;
    }

    div[data-testid="stDataFrame"] div[role="columnheader"] {
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: unset !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

display_df = paginated_df.drop(columns=["input", "original_text", "masked_text"], errors="ignore")

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    height="content",
)