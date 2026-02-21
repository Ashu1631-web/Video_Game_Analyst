import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title("📊 Enterprise Sales & Engagement Dashboard")

@st.cache_data
def load_data():
    games = pd.read_csv("data/games.csv")
    sales = pd.read_csv("data/vgsales.csv")
    sales.rename(columns={"Name": "Title"}, inplace=True)
    df = pd.merge(games, sales, on="Title", how="inner")
    return df

df = load_data()

df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.dropna(inplace=True)

# Sidebar Filters
st.sidebar.header("Advanced Filters")

search_game = st.sidebar.text_input("Search Game Title")

if search_game:
    df = df[df["Title"].str.contains(search_game, case=False)]

genre = st.sidebar.multiselect("Genre", df["Genre"].unique(), default=df["Genre"].unique())
platform = st.sidebar.multiselect("Platform", df["Platform"].unique(), default=df["Platform"].unique())

df = df[df["Genre"].isin(genre) & df["Platform"].isin(platform)]

# KPIs
c1,c2,c3,c4 = st.columns(4)
c1.metric("Total Games", df["Title"].nunique())
c2.metric("Global Sales (M)", round(df["Global_Sales"].sum(),2))
c3.metric("Avg Rating", round(df["Rating"].mean(),2))
c4.metric("Total Wishlist", int(df["Wishlist"].sum()))

st.markdown("---")

# Tabs
tab1,tab2,tab3 = st.tabs(["Sales","Engagement","Trends"])

with tab1:
    st.plotly_chart(px.bar(df.groupby("Genre")["Global_Sales"].sum().reset_index(),
                           x="Genre",y="Global_Sales"))
    st.plotly_chart(px.bar(df.groupby("Platform")["Global_Sales"].sum().reset_index(),
                           x="Platform",y="Global_Sales"))
    st.plotly_chart(px.histogram(df,x="Global_Sales"))
    st.plotly_chart(px.bar(df.sort_values("Global_Sales",ascending=False).head(10),
                           x="Global_Sales",y="Title",orientation="h"))

with tab2:
    st.plotly_chart(px.scatter(df,x="Rating",y="Global_Sales",
                               size="Wishlist",color="Genre"))
    st.plotly_chart(px.histogram(df,x="Wishlist"))
    st.plotly_chart(px.box(df,x="Genre",y="Rating"))

with tab3:
    yearly = df.groupby("Year")["Global_Sales"].sum().reset_index()
    st.plotly_chart(px.line(yearly,x="Year",y="Global_Sales"))
    st.plotly_chart(px.line(df.groupby("Year")["Rating"].mean().reset_index(),
                            x="Year",y="Rating"))

# Download Option
st.download_button("Download Filtered Data",
                   df.to_csv(index=False),
                   "filtered_data.csv",
                   "text/csv")
