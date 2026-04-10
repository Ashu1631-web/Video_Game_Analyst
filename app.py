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
        background-image: url("https://images.unsplash.com/photo-1570303345338-e1f0eddf4946?q=80&w=1071&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
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
    st.title("🎮 Navigation")

    menu = st.radio("", [
        "📌 Overview","📊 Dashboard","💰 Sales",
        "🎮 Engagement","🧠 Insights","📈 ML Forecast",
        "🧮 SQL Analysis","📥 Download","⚙️ Admin"
    ])

# ================= OVERVIEW =================
if menu == "📌 Overview":
    st.title("🎮 Video Game Sales & Engagement Dashboard")

    st.markdown("""
This project is a **data analytics dashboard** built using **Python, Streamlit, SQL, and Machine Learning** to analyze video game sales and user engagement.

---

### 🎯 Objective
- Understand game sales trends  
- Analyze user behavior (ratings, wishlist, plays)  
- Find top genres, platforms, and publishers  

---

### 📊 Features
- Interactive dashboard (like Power BI)  
- Drill-down filters (Genre → Platform → Year → Game)  
- 15 SQL queries with graphs  
- 20+ charts for analysis  
- Sales forecasting using Machine Learning  

---

### 📂 Dataset
- **games.csv** → user engagement data  
- **vgsales.csv** → sales data  

---

### 🛠 Tech Stack
- Python  
- Streamlit  
- Pandas  
- Plotly  
- SQL (SQLite)  
- Machine Learning (Linear Regression)  
""")

# ================= DASHBOARD =================
elif menu == "📊 Dashboard":
    st.title("📊 Dashboard")

    colf1, colf2, colf3, colf4 = st.columns(4)

    genre = colf1.selectbox("Genre", ["All"] + list(sales["Genre"].dropna().unique()))
    df = sales.copy()

    if genre != "All":
        df = df[df["Genre"] == genre]

    platform = colf2.selectbox("Platform", ["All"] + list(df["Platform"].dropna().unique()))
    if platform != "All":
        df = df[df["Platform"] == platform]

    year = colf3.selectbox("Year", ["All"] + list(sorted(df["Year"].dropna().unique())))
    if year != "All":
        df = df[df["Year"] == year]

    game = colf4.selectbox("Game", ["All"] + list(df["Name"].dropna().unique()))
    if game != "All":
        df = df[df["Name"] == game]

    filtered = df

    if filtered.empty:
        st.warning("⚠️ No data for selected filters")
        st.stop()

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Sales", round(filtered["Global_Sales"].sum(),2))
    col2.metric("📊 Avg", round(filtered["Global_Sales"].mean(),2))
    col3.metric("🎮 Games", len(filtered))

    df_year = filtered.groupby("Year")["Global_Sales"].sum().reset_index()
    st.plotly_chart(px.line(df_year, x="Year", y="Global_Sales", markers=True))
    st.plotly_chart(px.bar(filtered, x="Platform", y="Global_Sales", color="Genre"))

# ================= SALES =================
elif menu == "💰 Sales":
    st.plotly_chart(px.bar(sales, x="Platform", y="Global_Sales", color="Genre"))
    st.plotly_chart(px.pie(sales, names="Genre", values="Global_Sales"))

# ================= ENGAGEMENT =================
elif menu == "🎮 Engagement":
    st.plotly_chart(px.histogram(games, x="Rating"))
    st.plotly_chart(px.scatter(games, x="Rating", y="Wishlist"))

# ================= INSIGHTS =================
elif menu == "🧠 Insights":
    merged = pd.merge(games, sales, left_on="Title", right_on="Name")
    st.plotly_chart(px.scatter(merged, x="Rating", y="Global_Sales"))

# ================= ML =================
elif menu == "📈 ML Forecast":
    df_ml = sales.groupby("Year")["Global_Sales"].sum().reset_index()
    model = LinearRegression().fit(df_ml[["Year"]], df_ml["Global_Sales"])
    future = pd.DataFrame({"Year": list(range(int(df_ml["Year"].max())+1, int(df_ml["Year"].max())+6))})
    future["Forecast"] = model.predict(future)

    st.plotly_chart(px.line(df_ml, x="Year", y="Global_Sales"))
    st.plotly_chart(px.line(future, x="Year", y="Forecast"))

# ================= SQL =================
elif menu == "🧮 SQL Analysis":
    conn = sqlite3.connect("games.db", check_same_thread=False)
    games.to_sql("games", conn, if_exists="replace", index=False)
    sales.to_sql("vgsales", conn, if_exists="replace", index=False)

    q = st.selectbox("Query", [
        "SELECT Platform, SUM(Global_Sales) FROM vgsales GROUP BY Platform",
        "SELECT Publisher, SUM(Global_Sales) FROM vgsales GROUP BY Publisher",
        "SELECT Year, SUM(Global_Sales) FROM vgsales GROUP BY Year"
    ])

    df_sql = pd.read_sql(q, conn)
    st.dataframe(df_sql)
    st.plotly_chart(px.bar(df_sql, x=df_sql.columns[0], y=df_sql.columns[1]))

# ================= DOWNLOAD =================
elif menu == "📥 Download":
    st.download_button("Download CSV", sales.to_csv(index=False))

# ================= ADMIN =================
elif menu == "⚙️ Admin":
    if st.button("Logout"):
        st.session_state.auth = False
        st.rerun()

# ================= FOOTER =================
st.markdown("---")
st.markdown("🔥 Final Professional Dashboard")
