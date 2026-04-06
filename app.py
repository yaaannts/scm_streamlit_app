import streamlit as st
import pandas as pd
from faker import Faker
import os

st.set_page_config(
    page_title="SCM Dashboard Hub",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🚀 Supply Chain Management (SCM) Templates & Dashboards")
st.markdown("""
Welcome to the **SCM Dashboard Hub** — a comprehensive Streamlit app with interactive templates for key supply chain areas.
""")

# Generate sample data if not exists
if not os.path.exists("data/sample_scm_data.csv"):
    fake = Faker()
    data = []
    for _ in range(1000):
        data.append({
            "date": fake.date_between(start_date="-2y", end_date="today"),
            "product": fake.word(ext_word_list=["Widget A", "Widget B", "Gadget X", "Part Y"]),
            "category": fake.random_element(["Electronics", "Raw Materials", "Finished Goods"]),
            "inventory_level": fake.random_int(50, 5000),
            "demand": fake.random_int(100, 2000),
            "supplier": fake.company(),
            "location": fake.city(),
            "cost": round(fake.random_number(digits=4) / 10, 2),
            "lead_time_days": fake.random_int(5, 45),
            "status": fake.random_element(["On Time", "Delayed", "In Transit", "Stockout"]),
            "risk_score": fake.random_int(1, 100)
        })
    df = pd.DataFrame(data)
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/sample_scm_data.csv", index=False)
    st.success("Sample SCM data generated!")

df = pd.read_csv("data/sample_scm_data.csv")
df["date"] = pd.to_datetime(df["date"])

st.sidebar.success("Select a module from the sidebar →")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Products", len(df["product"].unique()))
with col2:
    st.metric("Avg Inventory Level", f"{df['inventory_level'].mean():.0f}")
with col3:
    st.metric("On-Time Delivery Rate", f"{(df['status'] == 'On Time').mean()*100:.1f}%")

st.subheader("Quick Overview")
st.dataframe(df.head(10), use_container_width=True)

st.info("👈 Use the sidebar to navigate to specific SCM modules. Each page includes KPIs, charts, filters, and actionable insights.")
