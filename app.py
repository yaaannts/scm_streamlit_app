import streamlit as st
import pandas as pd
import os
from faker import Faker
from datetime import datetime

st.set_page_config(page_title="SCM Hub", page_icon="📦", layout="wide")

st.title("🚀 Supply Chain Management Dashboard Hub")
st.markdown("Comprehensive interactive templates for **Inventory • Logistics • Procurement • Risk • Strategy • Vendor • Warehouse**")

# Generate richer sample data
data_path = "data/sample_scm_data.csv"
if not os.path.exists(data_path):
    fake = Faker()
    Faker.seed(42)
    data = []
    products = ["Widget A", "Widget B", "Gadget X", "Part Y", "Component Z", "Module P"]
    categories = ["Electronics", "Raw Materials", "Finished Goods", "Packaging"]
    statuses = ["On Time", "Delayed", "In Transit", "Stockout", "Delivered"]
    suppliers = ["GlobalTech Supplies", "AsiaParts Ltd", "EuroLogistics", "PrimeMaterials Inc", "SwiftShip Co"]

    for _ in range(5000):
        data.append({
            "date": fake.date_between(start_date="-2y", end_date="today"),
            "product": fake.random_element(products),
            "category": fake.random_element(categories),
            "inventory_level": fake.random_int(0, 10000),
            "demand_forecast": fake.random_int(200, 5000),
            "actual_demand": fake.random_int(150, 4500),
            "supplier": fake.random_element(suppliers),
            "location": fake.random_element(["Malé", "Singapore", "Dubai", "Rotterdam", "Los Angeles"]),
            "unit_cost": round(fake.random_number(digits=4) / 10, 2),
            "lead_time_days": fake.random_int(3, 60),
            "status": fake.random_element(statuses),
            "risk_score": fake.random_int(10, 95),
            "on_time_delivery": fake.boolean(chance_of_getting_true=85),
            "warehouse_utilization": fake.random_int(40, 98),
            "freight_cost": round(fake.random_number(digits=4) / 5, 2),
        })
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    os.makedirs("data", exist_ok=True)
    df.to_csv(data_path, index=False)
    st.toast("✅ Rich sample SCM dataset generated (5,000 rows)!", icon="📊")

df = pd.read_csv(data_path)
df["date"] = pd.to_datetime(df["date"])

st.sidebar.header("📌 Navigation")
st.sidebar.success("Choose a module below")

# Global filters on home
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total SKUs", len(df["product"].unique()))
with col2:
    st.metric("Avg Inventory", f"{df['inventory_level'].mean():,.0f}")
with col3:
    st.metric("OTIF Rate", f"{(df['on_time_delivery'].mean()*100):.1f}%")
with col4:
    st.metric("Avg Risk Score", f"{df['risk_score'].mean():.1f}")

st.subheader("Recent Activity")
st.dataframe(df.sort_values("date", ascending=False).head(10), use_container_width=True)

st.info("👈 Navigate using the sidebar to explore detailed dashboards for each SCM area.")
