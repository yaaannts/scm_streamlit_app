import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📈 Supply Chain Strategy & Planning")

df = pd.read_csv("data/sample_scm_data.csv", parse_dates=["date"])

demand_growth = st.slider("Assumed Demand Growth (%)", 0, 50, 10)

df["projected_demand"] = df["actual_demand"] * (1 + demand_growth/100)

fig = px.line(df.groupby("date")[["actual_demand", "projected_demand"]].mean().reset_index(), 
              x="date", y=["actual_demand", "projected_demand"], title="Demand Forecasting & Scenario")
st.plotly_chart(fig, use_container_width=True)

st.metric("Projected Demand Increase", f"+{demand_growth}%")
