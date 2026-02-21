import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Sales & Engagement Dashboard")

@st.cache_data
def load():
    games = pd.read_csv("data/games.csv")
    sales = pd.read_csv("data/vgsales.csv")
    sales.rename(columns={"Name":"Title"}, inplace=True)
    merged = pd.merge(games, sales, on="Title", how="inner")
    return merged

df = load()

# Advanced Filters
st.sidebar.header("Advanced Filters")

genre = st.sidebar.multiselect("Genre", df["Genre"].dropna().unique())
platform = st.sidebar.multiselect("Platform", df["Platform"].dropna().unique())
publisher = st.sidebar.multiselect("Publisher", df["Publisher"].dropna().unique())

if genre:
    df = df[df["Genre"].isin(genre)]
if platform:
    df = df[df["Platform"].isin(platform)]
if publisher:
    df = df[df["Publisher"].isin(publisher)]

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Sales", "🎮 Engagement", "🌍 Regional"])

with tab1:
    st.subheader("Top 10 Global Sales")
    top10 = df.sort_values("Global_Sales", ascending=False).head(10)
    fig = px.bar(top10, x="Global_Sales", y="Title", orientation="h")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    fig2 = px.scatter(df, x="Rating", y="Global_Sales",
                      size="Wishlist", color="Genre")
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    regional = df.groupby("Genre")[["NA_Sales","EU_Sales","JP_Sales"]].sum()
    fig3 = px.imshow(regional)
    st.plotly_chart(fig3, use_container_width=True)
