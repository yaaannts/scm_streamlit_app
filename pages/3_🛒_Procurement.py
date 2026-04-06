import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🛒 Procurement Dashboard")

df = pd.read_csv("data/sample_scm_data.csv", parse_dates=["date"])

filtered = df  # Add filters as needed

k1, k2, k3 = st.columns(3)
k1.metric("Total PO Value", f"${filtered['po_value'].sum():,.0f}")
k2.metric("Avg Lead Time", f"{filtered['lead_time_days'].mean():.1f} days")
k3.metric("Active Suppliers", len(filtered["supplier"].unique()))

c1, c2 = st.columns(2)
with c1:
    fig = px.bar(filtered.groupby("supplier")["po_value"].sum().reset_index().sort_values("po_value", ascending=False).head(10),
                 x="supplier", y="po_value", title="Spend by Supplier")
    st.plotly_chart(fig, use_container_width=True)
with c2:
    fig = px.box(filtered, x="supplier", y="lead_time_days", title="Lead Time by Supplier")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Procurement Table")
st.dataframe(filtered[["supplier", "product", "po_value", "lead_time_days", "unit_cost"]], use_container_width=True)
