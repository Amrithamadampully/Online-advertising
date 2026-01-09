import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Online Advertising Dashboard",
    layout="wide"
)

st.title("📊 Online Advertising Performance Dashboard")

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("online_advertising_performance_data.csv")
    return df

df = load_data()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔍 Filters")

month_filter = st.sidebar.multiselect(
    "Select Month",
    options=df["month"].unique(),
    default=df["month"].unique()
)

campaign_filter = st.sidebar.multiselect(
    "Select Campaign",
    options=df["campaign_number"].unique(),
    default=df["campaign_number"].unique()
)

filtered_df = df[
    (df["month"].isin(month_filter)) &
    (df["campaign_number"].isin(campaign_filter))
]

# -----------------------------
# KPI Metrics
# -----------------------------
total_cost = filtered_df["cost"].sum()
total_revenue = filtered_df["revenue"].sum()
total_clicks = filtered_df["clicks"].sum()
total_displays = filtered_df["displays"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Cost", f"{total_cost:,.2f}")
col2.metric("💵 Total Revenue", f"{total_revenue:,.2f}")
col3.metric("🖱️ Total Clicks", f"{total_clicks:,}")
col4.metric("👁️ Total Displays", f"{total_displays:,}")

st.divider()

# -----------------------------
# Campaign-wise Summary
# -----------------------------
st.subheader("📌 Campaign-wise Performance")

campaign_summary = (
    filtered_df
    .groupby("campaign_number")[["cost", "revenue", "clicks"]]
    .sum()
    .reset_index()
)

st.dataframe(campaign_summary, use_container_width=True)

# -----------------------------
# Bar Chart: Cost vs Revenue
# -----------------------------
st.subheader("📈 Cost vs Revenue by Campaign")

fig, ax = plt.subplots()

ax.bar(
    campaign_summary["campaign_number"],
    campaign_summary["cost"],
    label="Cost"
)

ax.bar(
    campaign_summary["campaign_number"],
    campaign_summary["revenue"],
    bottom=campaign_summary["cost"],
    label="Revenue"
)

ax.set_xlabel("Campaign Number")
ax.set_ylabel("Amount")
ax.legend()

st.pyplot(fig)

# -----------------------------
# Clicks by User Engagement
# -----------------------------
st.subheader("🎯 Clicks by User Engagement")

engagement_summary = (
    filtered_df
    .groupby("user_engagement")["clicks"]
    .sum()
    .reset_index()
)

fig2, ax2 = plt.subplots()
ax2.bar(
    engagement_summary["user_engagement"],
    engagement_summary["clicks"]
)
ax2.set_xlabel("User Engagement")
ax2.set_ylabel("Clicks")

st.pyplot(fig2)

# -----------------------------
# Raw Data
# -----------------------------
with st.expander("📄 View Raw Data"):
    st.dataframe(filtered_df, use_container_width=True)
