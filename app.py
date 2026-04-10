# =========================================
# 🎮 FINAL STREAMLIT APP (FILTER FIXED)
# =========================================

import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="🎮 Game Analytics Pro", layout="wide")

# ================= SESSION =================
if "auth" not in st.session_state:
    st.session_state.auth = False

# ================= HIDE DEFAULT MENU =================
st.markdown("""
<style>
[data-testid="stSidebarNav"] {display: none;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ================= LOGIN =================
def login():
    st.markdown("## 🔐 Gaming Login")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if u == "admin" and p == "1234":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Invalid Credentials")

# ================= HIDE SIDEBAR BEFORE LOGIN =================
if not st.session_state.auth:
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {display: none;}
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1542751371-adc38448a05e");
        background-size: cover;
    }
    </style>
    """, unsafe_allow_html=True)

    login()
    st.stop()

# ================= LOAD DATA =================
@st.cache_data
def load():
    g = pd.read_csv("data/games.csv")
    s = pd.read_csv("data/vgsales.csv")
    return g, s

games, sales = load()

# ================= SIDEBAR =================
with st.sidebar:

    # 🎮 NAVIGATION
    st.title("🎮 Navigation")

    menu = st.radio("", [
        "📌 Overview","📊 Dashboard","💰 Sales",
        "🎮 Engagement","🧠 Insights","📈 ML Forecast",
        "🧮 SQL Analysis","📥 Download","⚙️ Admin"
    ])

    st.markdown("---")

    # 🎯 FILTERS
    st.title("🎯 Drill Down Filters")

    genre = st.selectbox("Genre", ["All"] + list(sales["Genre"].dropna().unique()))
    df = sales.copy()

    if genre != "All":
        df = df[df["Genre"] == genre]

    platform = st.selectbox("Platform", ["All"] + list(df["Platform"].dropna().unique()))
    if platform != "All":
        df = df[df["Platform"] == platform]

    year = st.selectbox("Year", ["All"] + list(sorted(df["Year"].dropna().unique())))
    if year != "All":
        df = df[df["Year"] == year]

    game = st.selectbox("Game", ["All"] + list(df["Name"].dropna().unique()))
    if game != "All":
        df = df[df["Name"] == game]

    filtered = df

# ================= EMPTY CHECK =================
if filtered.empty:
    st.warning("⚠️ No data for selected filters")
    st.stop()

# ================= BREADCRUMB =================
st.markdown(f"""
### 🔍 Drill Path:
**Genre → {genre} | Platform → {platform} | Year → {year} | Game → {game}**
""")

# ================= OVERVIEW =================
if menu == "📌 Overview":
    st.title("🎮 Project Overview")
    st.write("Power BI style dashboard with working filters")

# ================= DASHBOARD =================
elif menu == "📊 Dashboard":
    st.title("📊 Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Sales", round(filtered["Global_Sales"].sum(),2))
    col2.metric("📊 Avg", round(filtered["Global_Sales"].mean(),2))
    col3.metric("🎮 Games", len(filtered))

    df_year = filtered.groupby("Year")["Global_Sales"].sum().reset_index()
    st.plotly_chart(px.line(df_year, x="Year", y="Global_Sales", markers=True))

# ================= SALES =================
elif menu == "💰 Sales":
    st.title("💰 Sales Analysis")

    st.plotly_chart(px.bar(filtered, x="Platform", y="Global_Sales", color="Genre"))
    st.plotly_chart(px.pie(filtered, names="Genre", values="Global_Sales"))
    st.plotly_chart(px.box(filtered, x="Genre", y="Global_Sales"))

# ================= ENGAGEMENT =================
elif menu == "🎮 Engagement":
    st.title("🎮 Engagement")

    st.plotly_chart(px.histogram(games, x="Rating"))
    st.plotly_chart(px.scatter(games, x="Rating", y="Wishlist"))

# ================= INSIGHTS =================
elif menu == "🧠 Insights":
    st.title("🧠 Insights")

    merged = pd.merge(games, filtered, left_on="Title", right_on="Name")

    st.plotly_chart(px.scatter(merged, x="Rating", y="Global_Sales", color="Genre"))
    st.plotly_chart(px.sunburst(merged, path=["Genre","Platform"], values="Global_Sales"))

# ================= ML FORECAST =================
elif menu == "📈 ML Forecast":
    st.title("📈 Sales Forecast")

    df_ml = filtered.groupby("Year")["Global_Sales"].sum().reset_index()

    model = LinearRegression()
    model.fit(df_ml[["Year"]], df_ml["Global_Sales"])

    future = pd.DataFrame({
        "Year": list(range(int(df_ml["Year"].max())+1, int(df_ml["Year"].max())+6))
    })

    future["Forecast"] = model.predict(future)

    st.plotly_chart(px.line(df_ml, x="Year", y="Global_Sales", title="Past"))
    st.plotly_chart(px.line(future, x="Year", y="Forecast", title="Forecast"))

# ================= SQL =================
elif menu == "🧮 SQL Analysis":
    st.title("🧮 SQL Analysis")

    conn = sqlite3.connect("games.db")
    games.to_sql("games", conn, if_exists="replace", index=False)
    sales.to_sql("vgsales", conn, if_exists="replace", index=False)

    queries = {
        "Top Platforms": "SELECT Platform, SUM(Global_Sales) FROM vgsales GROUP BY Platform",
        "Top Publishers": "SELECT Publisher, SUM(Global_Sales) FROM vgsales GROUP BY Publisher",
        "Yearly Sales": "SELECT Year, SUM(Global_Sales) FROM vgsales GROUP BY Year"
    }

    q = st.selectbox("Select Query", list(queries.keys()))
    df_sql = pd.read_sql(queries[q], conn)

    st.dataframe(df_sql)
    st.plotly_chart(px.bar(df_sql, x=df_sql.columns[0], y=df_sql.columns[1]))

# ================= DOWNLOAD =================
elif menu == "📥 Download":
    st.download_button("Download CSV", filtered.to_csv(index=False))

# ================= ADMIN =================
elif menu == "⚙️ Admin":
    if st.button("Logout"):
        st.session_state.auth = False
        st.rerun()

# ================= FOOTER =================
st.markdown("---")
st.markdown("🔥 FINAL FILTER WORKING DASHBOARD")
