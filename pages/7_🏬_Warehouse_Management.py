import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🏬 Warehouse Management")

df = pd.read_csv("data/sample_scm_data.csv", parse_dates=["date"])

k1, k2, k3 = st.columns(3)
k1.metric("Avg Warehouse Utilization", f"{df['warehouse_utilization'].mean():.1f}%")
k2.metric("Total Throughput", f"{df['actual_demand'].sum():,}")
k3.metric("High Utilization Warehouses", len(df[df["warehouse_utilization"] > 85]))

fig = px.histogram(df, x="warehouse_utilization", title="Warehouse Utilization Distribution")
st.plotly_chart(fig, use_container_width=True)

st.dataframe(df[["location", "warehouse_utilization", "inventory_level"]], use_container_width=True)
