import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.title("📦 Inventory Management Dashboard")

# Load / Generate data
if not os.path.exists("data/sample_scm_data.csv"):
    st.warning("Generating sample data...")
    # (Data generation code is in the next section - run once)

df = pd.read_csv("data/sample_scm_data.csv", parse_dates=["date"])

# Sidebar Filters
st.sidebar.header("Filters")
date_range = st.sidebar.date_input("Select Date Range", 
    [df["date"].min().date(), df["date"].max().date()], 
    min_value=df["date"].min().date(), max_value=df["date"].max().date())

products = st.sidebar.multiselect("Products", options=sorted(df["product"].unique()), default=df["product"].unique()[:5])
suppliers = st.sidebar.multiselect("Suppliers", options=df["supplier"].unique())

filtered = df.copy()
if date_range:
    filtered = filtered[filtered["date"].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1]))]
if products:
    filtered = filtered[filtered["product"].isin(products)]
if suppliers:
    filtered = filtered[filtered["supplier"].isin(suppliers)]

# KPIs
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Inventory Value", f"${(filtered['inventory_level'] * filtered['unit_cost']).sum():,.0f}")
k2.metric("Inventory Turnover", f"{(filtered['actual_demand'].sum() / (filtered['inventory_level'].mean()+1)):.2f}x")
k3.metric("Low Stock Items", len(filtered[filtered["inventory_level"] < 200]))
k4.metric("Days of Supply", f"{(filtered['inventory_level'].mean() / (filtered['actual_demand'].mean()+1)):.0f}")

tab1, tab2, tab3 = st.tabs(["Charts", "Trends", "Recommendations"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(filtered.groupby("product")["inventory_level"].sum().reset_index(), 
                     x="product", y="inventory_level", title="Inventory by Product")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.pie(filtered, names="category", values="inventory_level", title="Inventory Distribution by Category")
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    fig = px.line(filtered.groupby("date")["inventory_level"].mean().reset_index(), 
                  x="date", y="inventory_level", title="Inventory Level Trend")
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Reorder Alerts")
    low = filtered[filtered["inventory_level"] < 250]
    if len(low) > 0:
        st.error(f"⚠️ {len(low)} items below safety stock!")
        st.dataframe(low[["product", "inventory_level", "actual_demand", "supplier"]])
    else:
        st.success("Inventory levels are healthy.")

st.dataframe(filtered.sort_values("inventory_level"), use_container_width=True)
