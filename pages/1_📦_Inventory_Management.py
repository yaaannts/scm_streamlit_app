import streamlit as st
import plotly.express as px
from datetime import datetime, timedelta
# from utils import load_data, apply_filters   # uncomment if using utils

st.title("📦 Inventory Management Dashboard")

df = pd.read_csv("data/sample_scm_data.csv")
df["date"] = pd.to_datetime(df["date"])

# Filters
st.sidebar.header("Filters")
date_range = st.sidebar.date_input("Date Range", 
    [df["date"].min().date(), df["date"].max().date()])
selected_products = st.sidebar.multiselect("Products", options=df["product"].unique(), default=df["product"].unique()[:4])
selected_suppliers = st.sidebar.multiselect("Suppliers", options=df["supplier"].unique())

filtered = df.copy()
if date_range:
    filtered = filtered[filtered["date"].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1]))]
if selected_products:
    filtered = filtered[filtered["product"].isin(selected_products)]
if selected_suppliers:
    filtered = filtered[filtered["supplier"].isin(selected_suppliers)]

# KPIs
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Inventory Value", f"${(filtered['inventory_level'] * filtered['unit_cost']).sum():,.0f}")
k2.metric("Inventory Turnover", f"{(filtered['actual_demand'].sum() / (filtered['inventory_level'].mean() + 1)):.1f}x")
k3.metric("Stockout Items", len(filtered[filtered["inventory_level"] < 100]))
k4.metric("Days of Inventory", f"{(filtered['inventory_level'].mean() / (filtered['actual_demand'].mean() + 1)):.0f}")

tabs = st.tabs(["Overview Charts", "Trends", "Recommendations"])

with tabs[0]:
    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(filtered.groupby("product")["inventory_level"].sum().reset_index(), 
                     x="product", y="inventory_level", title="Inventory Level by Product")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.pie(filtered, names="category", values="inventory_level", title="Inventory by Category")
        st.plotly_chart(fig, use_container_width=True)

with tabs[1]:
    fig = px.line(filtered.sort_values("date").groupby("date")["inventory_level"].mean().reset_index(), 
                  x="date", y="inventory_level", title="Average Inventory Trend")
    st.plotly_chart(fig, use_container_width=True)

with tabs[2]:
    st.subheader("Reorder Recommendations")
    low_stock = filtered[filtered["inventory_level"] < 300]
    if not low_stock.empty:
        st.warning(f"⚠️ {len(low_stock)} items need attention!")
        st.dataframe(low_stock[["product", "inventory_level", "actual_demand", "supplier"]])
    else:
        st.success("All inventory levels look healthy!")

st.dataframe(filtered, use_container_width=True)
