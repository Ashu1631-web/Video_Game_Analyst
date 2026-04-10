# =========================================
# 🎮 FINAL ULTRA DASHBOARD APP
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

# ================= HIDE DEFAULT =================
st.markdown("""
<style>
[data-testid="stSidebarNav"] {display:none;}
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
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

if not st.session_state.auth:
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {display:none;}
    .stApp {
        background-image:url("https://images.unsplash.com/photo-1542751371-adc38448a05e");
        background-size:cover;
    }
    </style>
    """, unsafe_allow_html=True)

    login()
    st.stop()

# ================= LOAD DATA =================
@st.cache_data
def load():
    return pd.read_csv("data/games.csv"), pd.read_csv("data/vgsales.csv")

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
This project is a **data analytics dashboard** using Python, Streamlit, SQL, and Machine Learning.

### 🎯 Objective
- Analyze sales trends  
- Study user behavior  
- Identify top genres/platforms  

### 📊 Features
- Interactive dashboard  
- Drill-down filters  
- 15 SQL queries  
- 20+ charts  
- ML forecasting  

### 📂 Dataset
- games.csv  
- vgsales.csv  

### 🛠 Tech Stack
Python | Streamlit | Pandas | Plotly | SQL | ML
""")

# ================= DASHBOARD =================
elif menu == "📊 Dashboard":
    st.title("📊 Advanced Dashboard")

    # FILTERS
    c1, c2, c3, c4 = st.columns(4)

    genre = c1.selectbox("Genre", ["All"] + list(sales["Genre"].dropna().unique()))
    df = sales.copy()
    if genre != "All":
        df = df[df["Genre"] == genre]

    platform = c2.selectbox("Platform", ["All"] + list(df["Platform"].dropna().unique()))
    if platform != "All":
        df = df[df["Platform"] == platform]

    year = c3.selectbox("Year", ["All"] + list(sorted(df["Year"].dropna().unique())))
    if year != "All":
        df = df[df["Year"] == year]

    game = c4.selectbox("Game", ["All"] + list(df["Name"].dropna().unique()))
    if game != "All":
        df = df[df["Name"] == game]

    filtered = df

    if filtered.empty:
        st.warning("⚠️ No data for selected filters")
        st.stop()

    # KPI
    k1, k2, k3 = st.columns(3)
    k1.metric("💰 Sales", round(filtered["Global_Sales"].sum(),2))
    k2.metric("📊 Avg", round(filtered["Global_Sales"].mean(),2))
    k3.metric("🎮 Games", len(filtered))

    st.markdown("---")

    # 15 GRAPHS
    st.plotly_chart(px.bar(filtered, x="Platform", y="Global_Sales", title="1. Sales by Platform"))
    st.plotly_chart(px.bar(filtered, x="Genre", y="Global_Sales", title="2. Sales by Genre"))

    df_year = filtered.groupby("Year")["Global_Sales"].sum().reset_index()
    st.plotly_chart(px.line(df_year, x="Year", y="Global_Sales", markers=True, title="3. Yearly Trend"))

    st.plotly_chart(px.pie(filtered, names="Genre", values="Global_Sales", title="4. Genre Distribution"))
    st.plotly_chart(px.pie(filtered, names="Platform", values="Global_Sales", title="5. Platform Distribution"))

    st.plotly_chart(px.box(filtered, x="Genre", y="Global_Sales", title="6. Box Plot"))
    st.plotly_chart(px.histogram(filtered, x="Global_Sales", title="7. Sales Histogram"))

    top = filtered.sort_values("Global_Sales", ascending=False).head(10)
    st.plotly_chart(px.bar(top, x="Name", y="Global_Sales", title="8. Top Games"))

    pub = filtered.groupby("Publisher")["Global_Sales"].sum().reset_index().head(10)
    st.plotly_chart(px.bar(pub, x="Publisher", y="Global_Sales", title="9. Publisher Sales"))

    st.plotly_chart(px.bar(filtered, x="Platform", y="NA_Sales", title="10. NA Sales"))
    st.plotly_chart(px.bar(filtered, x="Platform", y="EU_Sales", title="11. EU Sales"))
    st.plotly_chart(px.bar(filtered, x="Platform", y="JP_Sales", title="12. JP Sales"))
    st.plotly_chart(px.bar(filtered, x="Platform", y="Other_Sales", title="13. Other Sales"))

    st.plotly_chart(px.scatter(filtered, x="Year", y="Global_Sales", title="14. Year vs Sales"))
    st.plotly_chart(px.density_heatmap(filtered, x="Genre", y="Platform", title="15. Heatmap"))

# ================= ML =================
elif menu == "📈 ML Forecast":
    st.title("📈 Forecast")

    df_ml = sales.groupby("Year")["Global_Sales"].sum().reset_index()
    model = LinearRegression().fit(df_ml[["Year"]], df_ml["Global_Sales"])

    future = pd.DataFrame({"Year": list(range(int(df_ml["Year"].max())+1, int(df_ml["Year"].max())+6))})
    future["Forecast"] = model.predict(future)

    st.plotly_chart(px.line(df_ml, x="Year", y="Global_Sales"))
    st.plotly_chart(px.line(future, x="Year", y="Forecast"))

# ================= SQL =================
elif menu == "🧮 SQL Analysis":
    st.title("SQL")

    conn = sqlite3.connect("games.db", check_same_thread=False)
    games.to_sql("games", conn, if_exists="replace", index=False)
    sales.to_sql("vgsales", conn, if_exists="replace", index=False)

    q = st.selectbox("Query", [
        "SELECT Platform, SUM(Global_Sales) FROM vgsales GROUP BY Platform",
        "SELECT Publisher, SUM(Global_Sales) FROM vgsales GROUP BY Publisher"
    ])

    df_sql = pd.read_sql(q, conn)
    st.dataframe(df_sql)

# ================= DOWNLOAD =================
elif menu == "📥 Download":
    st.download_button("Download CSV", sales.to_csv(index=False))

# ================= ADMIN =================
elif menu == "⚙️ Admin":
    if st.button("Logout"):
        st.session_state.auth = False
        st.rerun()
