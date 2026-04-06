import streamlit as st
import plotly.express as px
import pandas as pd

st.title("🚚 Logistics & Distribution Dashboard")

df = pd.read_csv("data/sample_scm_data.csv")
df["date"] = pd.to_datetime(df["date"])

# Filters (same pattern as above - copy & adapt)
selected_locations = st.sidebar.multiselect("Locations", df["location"].unique())

filtered = df  # apply filters similarly...

k1, k2, k3, k4 = st.columns(4)
k1.metric("On-Time Delivery Rate", f"{(filtered['on_time_delivery'].mean()*100):.1f}%")
k2.metric("Avg Lead Time", f"{filtered['lead_time_days'].mean():.1f} days")
k3.metric("Total Freight Cost", f"${filtered['freight_cost'].sum():,.0f}")
k4.metric("Delayed Shipments", len(filtered[filtered["status"] == "Delayed"]))

c1, c2 = st.columns(2)
with c1:
    fig = px.histogram(filtered, x="lead_time_days", color="status", title="Lead Time Distribution")
    st.plotly_chart(fig, use_container_width=True)
with c2:
    fig = px.bar(filtered.groupby("location")["on_time_delivery"].mean().reset_index(), 
                 x="location", y="on_time_delivery", title="OTD by Location")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Shipment Status")
fig = px.pie(filtered, names="status", title="Shipment Status Breakdown")
st.plotly_chart(fig, use_container_width=True)
