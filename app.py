import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="SCM Hub", page_icon="📦", layout="wide")

st.title("🚀 Supply Chain Management (SCM) Templates & Dashboards")
st.markdown("**Professional interactive dashboards** for Inventory, Logistics, Procurement, Risk, Strategy, Vendor & Warehouse Management.")

data_path = "data/sample_scm_data.csv"

if not os.path.exists(data_path):
    st.warning("Generating rich sample dataset for demonstration...")
    # Sample data will be generated inside the first page that runs, but we create empty folder
    os.makedirs("data", exist_ok=True)
    st.info("Please navigate to any dashboard page to generate sample data.")

try:
    df = pd.read_csv(data_path, parse_dates=["date"])
except:
    df = pd.DataFrame()
    st.info("Sample data not yet generated. Go to any module to create it.")

st.sidebar.title("📌 Modules")
st.sidebar.success("Select a dashboard")

if not df.empty:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total SKUs", len(df["product"].unique()))
    with col2:
        st.metric("Avg Inventory", f"{df['inventory_level'].mean():,.0f}")
    with col3:
        st.metric("OTIF", f"{df['on_time_delivery'].mean()*100:.1f}%")
    with col4:
        st.metric("Avg Risk Score", f"{df['risk_score'].mean():.1f}")

    st.subheader("Recent Transactions")
    st.dataframe(df.sort_values("date", ascending=False).head(8), use_container_width=True)

st.caption("Built with Streamlit • Fully customizable • Add your own CSV later")
