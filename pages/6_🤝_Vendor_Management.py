import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🤝 Vendor Management")

df = pd.read_csv("data/sample_scm_data.csv", parse_dates=["date"])

vendor_perf = df.groupby("supplier").agg({
    "on_time_delivery": "mean",
    "quality_score": "mean",
    "risk_score": "mean",
    "po_value": "sum"
}).reset_index()

vendor_perf["overall_score"] = (vendor_perf["on_time_delivery"]*40 + vendor_perf["quality_score"]*40 + (100 - vendor_perf["risk_score"])*20)

fig = px.bar(vendor_perf.sort_values("overall_score", ascending=False), 
             x="supplier", y="overall_score", title="Vendor Overall Score")
st.plotly_chart(fig, use_container_width=True)

st.dataframe(vendor_perf, use_container_width=True)
