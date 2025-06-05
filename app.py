import streamlit as st
import pandas as pd
import os
import time
from glob import glob
import plotly.express as px

# Set page config
st.set_page_config(page_title="Naukri Job Dashboard", layout="wide")

st.title("📊 Naukri Job Listings Dashboard")
st.markdown("Live summary of Data Analyst job listings scraped from Naukri.com")

# 📁 Load latest CSV file
def get_latest_csv(folder="."):
    csv_files = glob(os.path.join(folder, "*.csv"))
    if not csv_files:
        return None
    return max(csv_files, key=os.path.getmtime)

latest_csv = get_latest_csv()

if latest_csv:
    st.success(f"✅ Loaded: `{os.path.basename(latest_csv)}`")
    df = pd.read_csv(latest_csv)

    # Show last modified timestamp
    last_modified = time.ctime(os.path.getmtime(latest_csv))
    st.caption(f"🕒 **Last Updated:** `{last_modified}`")

    # ========================
    # 🔢 Summary Statistics
    # ========================
    st.subheader("📌 Summary Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📄 Total Jobs", len(df))
    with col2:
        st.metric("🏢 Unique Companies", df['Company'].nunique())
    with col3:
        st.metric("📍 Unique Locations", df['Location'].nunique())

    st.markdown("---")

    # ========================
    # 📊 Charts Section
    # ========================
    st.subheader("📈 Charts")

    # Top 10 Companies
    top_companies = df['Company'].value_counts().nlargest(10).reset_index()
    top_companies.columns = ['Company', 'Job Count']
    fig1 = px.bar(top_companies, x='Company', y='Job Count', title='🏢 Top Hiring Companies', color='Job Count')
    st.plotly_chart(fig1, use_container_width=True)

    # Top 10 Locations
    top_locations = df['Location'].value_counts().nlargest(10).reset_index()
    top_locations.columns = ['Location', 'Job Count']
    fig2 = px.bar(top_locations, x='Location', y='Job Count', title='📍 Top Job Locations', color='Job Count')
    st.plotly_chart(fig2, use_container_width=True)

    # Posted Time Pie Chart
    posted_counts = df['Posted'].value_counts().reset_index()
    posted_counts.columns = ['Posted Time', 'Count']
    fig3 = px.pie(posted_counts, names='Posted Time', values='Count', title='⏳ Posting Time Distribution')
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")

    # ========================
    # 📄 Data Table
    # ========================
    st.subheader("📋 Job Listings Table")
    st.dataframe(df, use_container_width=True)

    # ========================
    # 📥 Download CSV
    # ========================
    csv_download = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Full Job List",
        data=csv_download,
        file_name="naukri_jobs_latest.csv",
        mime="text/csv"
    )

else:
    st.error("⚠️ No CSV file found. Please run the scraper first.")
