import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📦 Inventory Management Dashboard")

df = pd.read_csv("data/sample_scm_data.csv")  # Reuse shared data
df["date"] = pd.to_datetime(df["date"])

# Filters
col1, col2 = st.columns(2)
with col1:
    selected_products = st.multiselect("Filter Products", options=df["product"].unique(), default=df["product"].unique()[:3])
with col2:
    min_inventory = st.slider("Minimum Inventory Level", 0, 5000, 100)

filtered_df = df[df["product"].isin(selected_products) & (df["inventory_level"] >= min_inventory)]

# KPIs
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Current Inventory", f"{filtered_df['inventory_level'].sum():,}")
kpi2.metric("Stockout Risk Items", len(filtered_df[filtered_df["inventory_level"] < 200]))
kpi3.metric("Avg Reorder Point", "150")  # Placeholder
kpi4.metric("Turnover Ratio", f"{(filtered_df['demand'].sum() / filtered_df['inventory_level'].mean()):.1f}")

# Charts
tab1, tab2, tab3 = st.tabs(["Inventory Levels", "Demand vs Inventory", "Stock Movement"])

with tab1:
    fig = px.bar(filtered_df.groupby("product")["inventory_level"].sum().reset_index(), 
                 x="product", y="inventory_level", title="Inventory by Product")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    fig = px.scatter(filtered_df, x="inventory_level", y="demand", color="product", 
                     title="Demand vs Inventory Levels")
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    fig = px.line(filtered_df.sort_values("date"), x="date", y="inventory_level", color="product", 
                  title="Inventory Trend Over Time")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Inventory Table")
st.dataframe(filtered_df, use_container_width=True)

# Simple reorder suggestion
st.subheader("Reorder Recommendations")
low_stock = filtered_df[filtered_df["inventory_level"] < 300]
if not low_stock.empty:
    st.warning(f"{len(low_stock)} items below reorder threshold!")
    st.dataframe(low_stock[["product", "inventory_level", "demand"]])
