import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🚚 Logistics & Distribution Dashboard")

df = pd.read_csv("data/sample_scm_data.csv", parse_dates=["date"])

# Filters
st.sidebar.header("Filters")
locations = st.sidebar.multiselect("Locations", options=df["location"].unique(), default=df["location"].unique()[:3])

filtered = df[df["location"].isin(locations)] if locations else df

k1, k2, k3, k4 = st.columns(4)
k1.metric("On-Time Delivery Rate", f"{filtered['on_time_delivery'].mean()*100:.1f}%")
k2.metric("Average Lead Time", f"{filtered['lead_time_days'].mean():.1f} days")
k3.metric("Total Freight Cost", f"${filtered['freight_cost'].sum():,.0f}")
k4.metric("Delayed Shipments", len(filtered[filtered["status"] == "Delayed"]))

c1, c2 = st.columns(2)
with c1:
    fig = px.histogram(filtered, x="lead_time_days", color="status", title="Lead Time Distribution by Status")
    st.plotly_chart(fig, use_container_width=True)
with c2:
    fig = px.bar(filtered.groupby("location")["on_time_delivery"].mean().reset_index(), 
                 x="location", y="on_time_delivery", title="On-Time Rate by Location")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Shipment Status")
fig = px.pie(filtered, names="status", title="Current Shipment Status")
st.plotly_chart(fig, use_container_width=True)

st.dataframe(filtered, use_container_width=True)
