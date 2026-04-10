# =========================================
# 🎮 ULTRA PREMIUM FINAL APP (DRILL + ML)
# =========================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import sqlite3
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="🎮 Game Analytics Ultra", layout="wide")

# ================= LOGIN =================
def login():
    st.title("🔐 Login")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("Login"):
        if u == "admin" and p == "1234":
            st.session_state.auth = True
        else:
            st.error("Invalid")

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    login()
    st.stop()

# ================= LOAD =================
@st.cache_data
def load():
    g = pd.read_csv("data/games.csv")
    s = pd.read_csv("data/vgsales.csv")
    return g, s

games, sales = load()

# ================= SQL =================
conn = sqlite3.connect("games.db", check_same_thread=False)
games.to_sql("games", conn, if_exists="replace", index=False)
sales.to_sql("vgsales", conn, if_exists="replace", index=False)

# ================= DRILL FILTER =================
st.sidebar.title("🎯 Drill Down Filters")

selected_genre = st.sidebar.selectbox("Genre", ["All"] + list(sales["Genre"].dropna().unique()))
df = sales.copy()
if selected_genre != "All":
    df = df[df["Genre"] == selected_genre]

selected_platform = st.sidebar.selectbox("Platform", ["All"] + list(df["Platform"].dropna().unique()))
if selected_platform != "All":
    df = df[df["Platform"] == selected_platform]

selected_year = st.sidebar.selectbox("Year", ["All"] + list(sorted(df["Year"].dropna().unique())))
if selected_year != "All":
    df = df[df["Year"] == selected_year]

selected_game = st.sidebar.selectbox("Game", ["All"] + list(df["Name"].dropna().unique()))
if selected_game != "All":
    df = df[df["Name"] == selected_game]

filtered = df

# ================= MENU =================
menu = st.sidebar.radio("Menu",
    ["Overview","Dashboard","Sales","Engagement","Insights","ML Forecast","SQL","Download","Admin"])

# ================= OVERVIEW =================
if menu == "Overview":
    st.title("🎮 Project Overview")
    st.write("Advanced Gaming Analytics Dashboard with ML + Drill Down")

# ================= DASHBOARD =================
elif menu == "Dashboard":
    st.title("📊 Dashboard")

    c1,c2,c3 = st.columns(3)
    c1.metric("Sales", round(filtered['Global_Sales'].sum(),2))
    c2.metric("Avg", round(filtered['Global_Sales'].mean(),2))
    c3.metric("Games", len(filtered))

    st.plotly_chart(px.line(filtered.groupby("Year")["Global_Sales"].sum().reset_index(),
                             x="Year", y="Global_Sales", markers=True))

# ================= SALES =================
elif menu == "Sales":
    st.title("💰 Sales")

    st.plotly_chart(px.bar(filtered, x="Platform", y="Global_Sales", color="Genre", animation_frame="Year"))
    st.plotly_chart(px.pie(filtered, names="Genre", values="Global_Sales"))
    st.plotly_chart(px.box(filtered, x="Genre", y="Global_Sales"))

# ================= ENGAGEMENT =================
elif menu == "Engagement":
    st.title("🎮 Engagement")

    st.plotly_chart(px.histogram(games, x="Rating"))
    st.plotly_chart(px.scatter(games, x="Rating", y="Wishlist"))

# ================= INSIGHTS =================
elif menu == "Insights":
    st.title("🧠 Insights")

    merged = pd.merge(games, sales, left_on="Title", right_on="Name")
    st.plotly_chart(px.scatter(merged, x="Rating", y="Global_Sales", color="Genre"))

# ================= ML FORECAST =================
elif menu == "ML Forecast":
    st.title("📈 Sales Forecast (ML)")

    df_ml = sales.dropna(subset=["Year","Global_Sales"])
    df_ml = df_ml.groupby("Year")["Global_Sales"].sum().reset_index()

    X = df_ml[["Year"]]
    y = df_ml["Global_Sales"]

    model = LinearRegression()
    model.fit(X, y)

    future_years = pd.DataFrame({"Year": list(range(int(df_ml["Year"].max())+1, int(df_ml["Year"].max())+6))})
    preds = model.predict(future_years)

    future_years["Predicted_Sales"] = preds

    st.plotly_chart(px.line(df_ml, x="Year", y="Global_Sales", title="Past Sales"))
    st.plotly_chart(px.line(future_years, x="Year", y="Predicted_Sales", title="Forecast"))

# ================= SQL =================
elif menu == "SQL":
    st.title("SQL Analysis")

    query = st.selectbox("Query", [
        "Top Platforms","Top Publishers","Yearly Trend"
    ])

    if query == "Top Platforms":
        q = "SELECT Platform, SUM(Global_Sales) as sales FROM vgsales GROUP BY Platform"
    elif query == "Top Publishers":
        q = "SELECT Publisher, SUM(Global_Sales) as sales FROM vgsales GROUP BY Publisher"
    else:
        q = "SELECT Year, SUM(Global_Sales) as sales FROM vgsales GROUP BY Year"

    df_sql = pd.read_sql(q, conn)
    st.dataframe(df_sql)
    st.plotly_chart(px.bar(df_sql, x=df_sql.columns[0], y=df_sql.columns[1]))

# ================= DOWNLOAD =================
elif menu == "Download":
    st.download_button("Download CSV", filtered.to_csv(index=False))

# ================= ADMIN =================
elif menu == "Admin":
    if st.button("Logout"):
        st.session_state.auth = False
        st.rerun()

# ================= FOOTER =================
st.markdown("---")
st.markdown("🔥 Ultra Premium with ML + Drill Down")
