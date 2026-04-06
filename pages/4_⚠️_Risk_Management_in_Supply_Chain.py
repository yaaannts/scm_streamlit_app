import streamlit as st
import pandas as pd
import plotly.express as px

st.title("⚠️ Risk Management in Supply Chain")

df = pd.read_csv("data/sample_scm_data.csv", parse_dates=["date"])

risk_threshold = st.slider("Risk Score Threshold", 0, 100, 70)

high_risk = df[df["risk_score"] > risk_threshold]

k1, k2 = st.columns(2)
k1.metric("High Risk Items", len(high_risk))
k2.metric("Average Risk Score", f"{df['risk_score'].mean():.1f}")

fig = px.scatter(df, x="lead_time_days", y="risk_score", color="supplier", 
                 size="inventory_level", hover_data=["product"],
                 title="Risk vs Lead Time")
st.plotly_chart(fig, use_container_width=True)

st.subheader("High Risk Suppliers")
st.dataframe(high_risk[["supplier", "product", "risk_score", "lead_time_days"]].sort_values("risk_score", ascending=False), use_container_width=True)
