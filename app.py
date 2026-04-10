import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="🎮 Game Analytics Pro", layout="wide")

# ================= SESSION =================
if "auth" not in st.session_state:
    st.session_state.auth = False

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

# ================= SQL =================
conn = sqlite3.connect("games.db", check_same_thread=False)
games.to_sql("games", conn, if_exists="replace", index=False)
sales.to_sql("vgsales", conn, if_exists="replace", index=False)

# ================= DRILL FILTER =================
st.sidebar.title("🎯 Drill Down Filters")

genre = st.sidebar.selectbox("Genre", ["All"] + list(sales["Genre"].dropna().unique()))
df = sales.copy()
if genre != "All":
    df = df[df["Genre"] == genre]

platform = st.sidebar.selectbox("Platform", ["All"] + list(df["Platform"].dropna().unique()))
if platform != "All":
    df = df[df["Platform"] == platform]

year = st.sidebar.selectbox("Year", ["All"] + list(sorted(df["Year"].dropna().unique())))
if year != "All":
    df = df[df["Year"] == year]

game = st.sidebar.selectbox("Game", ["All"] + list(df["Name"].dropna().unique()))
if game != "All":
    df = df[df["Name"] == game]

filtered = df

# Breadcrumb
st.markdown(f"""
### 🔍 Drill Path:
**Genre → {genre} | Platform → {platform} | Year → {year} | Game → {game}**
""")

# ================= MENU =================
menu = st.sidebar.radio("🎮 Navigation", [
    "📌 Overview","📊 Dashboard","💰 Sales",
    "🎮 Engagement","🧠 Insights","📈 ML Forecast",
    "🧮 SQL Analysis","📥 Download","⚙️ Admin"
])

# ================= OVERVIEW =================
if menu == "📌 Overview":
    st.title("🎮 Project Overview")
    st.markdown("""
    ### Video Game Sales & Engagement Analytics

    🔥 Features:
    - Power BI style drill-down filters
    - 20+ interactive charts
    - SQL analytics
    - ML forecasting

    👉 Use sidebar to explore dashboards
    """)

# ================= DASHBOARD =================
elif menu == "📊 Dashboard":
    st.title("📊 Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Sales", round(filtered["Global_Sales"].sum(),2))
    col2.metric("📊 Avg", round(filtered["Global_Sales"].mean(),2))
    col3.metric("🎮 Games", len(filtered))

    df_year = sales.groupby("Year")["Global_Sales"].sum().reset_index()
    st.plotly_chart(px.line(df_year, x="Year", y="Global_Sales", markers=True))

# ================= SALES =================
elif menu == "💰 Sales":
    st.title("💰 Sales Analysis")

    st.plotly_chart(px.bar(filtered, x="Platform", y="Global_Sales",
                           color="Genre", animation_frame="Year"))

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

    merged = pd.merge(games, sales, left_on="Title", right_on="Name")

    st.plotly_chart(px.scatter(merged, x="Rating", y="Global_Sales", color="Genre"))
    st.plotly_chart(px.sunburst(merged, path=["Genre","Platform"], values="Global_Sales"))

# ================= ML FORECAST =================
elif menu == "📈 ML Forecast":
    st.title("📈 Sales Forecast")

    df_ml = sales.groupby("Year")["Global_Sales"].sum().reset_index()

    model = LinearRegression()
    model.fit(df_ml[["Year"]], df_ml["Global_Sales"])

    future = pd.DataFrame({
        "Year": list(range(int(df_ml["Year"].max())+1, int(df_ml["Year"].max())+6))
    })

    future["Forecast"] = model.predict(future)

    st.plotly_chart(px.line(df_ml, x="Year", y="Global_Sales", title="Past Sales"))
    st.plotly_chart(px.line(future, x="Year", y="Forecast", title="Future Prediction"))

# ================= SQL ANALYSIS =================
elif menu == "🧮 SQL Analysis":
    st.title("🧮 SQL Analysis")

    queries = {
        "Top Rated Games": "SELECT Title, Rating FROM games ORDER BY Rating DESC LIMIT 10",
        "Wishlisted Games": "SELECT Title, Wishlist FROM games ORDER BY Wishlist DESC LIMIT 10",
        "Avg Rating Genre": "SELECT Genres, AVG(Rating) FROM games GROUP BY Genres",
        "Played Games": "SELECT Title, Plays FROM games ORDER BY Plays DESC LIMIT 10",
        "Developer Performance": "SELECT Team, AVG(Rating) FROM games GROUP BY Team",

        "Sales by Platform": "SELECT Platform, SUM(Global_Sales) FROM vgsales GROUP BY Platform",
        "Top Publishers": "SELECT Publisher, SUM(Global_Sales) FROM vgsales GROUP BY Publisher LIMIT 10",
        "Yearly Sales": "SELECT Year, SUM(Global_Sales) FROM vgsales GROUP BY Year",
        "Regional Sales": "SELECT SUM(NA_Sales), SUM(EU_Sales), SUM(JP_Sales) FROM vgsales",
        "Top Games": "SELECT Name, Global_Sales FROM vgsales ORDER BY Global_Sales DESC LIMIT 10",

        "Rating vs Sales": "SELECT g.Title, g.Rating, v.Global_Sales FROM games g JOIN vgsales v ON g.Title=v.Name",
        "Genre Sales": "SELECT Genre, SUM(Global_Sales) FROM vgsales GROUP BY Genre",
        "Platform Rating": "SELECT v.Platform, AVG(g.Rating) FROM games g JOIN vgsales v ON g.Title=v.Name GROUP BY v.Platform",
        "Wishlist vs Sales": "SELECT g.Title, g.Wishlist, v.Global_Sales FROM games g JOIN vgsales v ON g.Title=v.Name",
        "Genre Platform": "SELECT Genre, Platform, SUM(Global_Sales) FROM vgsales GROUP BY Genre, Platform"
    }

    q = st.selectbox("Select Query", list(queries.keys()))
    df_sql = pd.read_sql(queries[q], conn)

    st.dataframe(df_sql)

    if df_sql.shape[1] >= 2:
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
st.markdown("🔥 FINAL ULTRA PREMIUM DASHBOARD READY")
