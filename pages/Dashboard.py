import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title("📊 Sales & Engagement Dashboard")

games = pd.read_csv("data/games.csv")
sales = pd.read_csv("data/vgsales.csv")

sales.rename(columns={"Name": "Title"}, inplace=True)

df = pd.merge(games, sales, on="Title", how="inner")

df.replace([np.inf, -np.inf], np.nan, inplace=True)

for col in ["Rating", "Wishlist", "Global_Sales"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df.dropna(subset=["Rating", "Wishlist", "Global_Sales"], inplace=True)

fig = px.scatter(
    df,
    x="Rating",
    y="Global_Sales",
    size="Wishlist",
    color="Genre"
)

st.plotly_chart(fig, use_container_width=True)
