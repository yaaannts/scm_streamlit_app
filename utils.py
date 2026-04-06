import pandas as pd
import plotly.express as px

def load_data():
    return pd.read_csv("data/sample_scm_data.csv", parse_dates=["date"])

def apply_filters(df, date_range=None, products=None, suppliers=None):
    if date_range:
        df = df[df["date"].between(*date_range)]
    if products:
        df = df[df["product"].isin(products)]
    if suppliers:
        df = df[df["supplier"].isin(suppliers)]
    return df
