import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title("Sales & Engagement Dashboard")

@st.cache_data
def load():
    games = pd.read_csv("data/games.csv")
    sales = pd.read_csv("data/vgsales.csv")
    sales.rename(columns={"Name":"Title"}, inplace=True)
    df = pd.merge(games, sales, on="Title", how="inner")
    return df

df = load()

# SAFE CLEANING
df.replace([np.inf, -np.inf], np.nan, inplace=True)

numeric_cols = ["Rating","Wishlist","Global_Sales"]
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

df.dropna(subset=numeric_cols, inplace=True)

# Scatter Plot
fig = px.scatter(
    df,
    x="Rating",
    y="Global_Sales",
    size="Wishlist",
    color="Genre"
)

st.plotly_chart(fig, use_container_width=True)
