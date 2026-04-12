# =========================================
# 🎮 FINAL ULTRA DASHBOARD (ALL FEATURES)
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

# ================= GLOBAL UI =================
st.markdown("""
<style>

/* ORANGE GRADIENT AFTER LOGIN */
.stApp {
    background: linear-gradient(135deg, #ff7e00, #ff3c00);
}

/* GLASS CARD */
.card {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 10px;
    box-shadow: 0 0 15px rgba(0,0,0,0.3);
}

/* Hide default */
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
        background-image:url("https://images.unsplash.com/photo-1608889825205-eebdb9fc5806?q=80&w=1974");
        background-size:cover;
    }
    </style>
    """, unsafe_allow_html=True)

    login()
    st.stop()

# ================= PREMIUM FUNCTION =================
def premium(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        transition_duration=500
    )
    return fig

# ================= LOAD DATA =================
@st.cache_data
def load():
    return pd.read_csv("data/games.csv"), pd.read_csv("data/vgsales.csv")

games, sales = load()

# ================= SIDEBAR =================
with st.sidebar:
    menu = st.radio("", [
        "📌 Overview","📊 Dashboard","💰 Sales",
        "🎮 Engagement","🧠 Insights","📈 ML Forecast",
        "🧮 SQL Analysis"
    ])

# ================= OVERVIEW =================
if menu == "📌 Overview":
    st.title("🎮 Game Analytics Pro")

# ================= DASHBOARD =================
elif menu == "📊 Dashboard":

    st.title("📊 Dashboard")

    c1,c2,c3 = st.columns(3)
    genre = c1.selectbox("Genre", ["All"] + list(sales["Genre"].dropna().unique()))
    platform = c2.selectbox("Platform", ["All"] + list(sales["Platform"].dropna().unique()))
    year = c3.selectbox("Year", ["All"] + list(sorted(sales["Year"].dropna().unique())))

    df = sales.copy()
    if genre!="All": df=df[df["Genre"]==genre]
    if platform!="All": df=df[df["Platform"]==platform]
    if year!="All": df=df[df["Year"]==year]

    charts = [
        px.bar(df,x="Platform",y="Global_Sales",title="1. Platform Sales"),
        px.bar(df,x="Genre",y="Global_Sales",title="2. Genre Sales"),
        px.line(df.groupby("Year")["Global_Sales"].sum().reset_index(),x="Year",y="Global_Sales",title="3. Year Trend"),
        px.pie(df,names="Genre",values="Global_Sales",title="4. Genre Distribution"),
        px.box(df,x="Genre",y="Global_Sales",title="5. Box Plot"),
        px.histogram(df,x="Global_Sales",title="6. Histogram"),
        px.scatter(df,x="Year",y="Global_Sales",title="7. Scatter Plot"),
        px.bar(df.groupby("Publisher")["Global_Sales"].sum().reset_index().head(10),x="Publisher",y="Global_Sales",title="8. Top Publishers"),
        px.bar(df,x="Platform",y="NA_Sales",title="9. NA Sales"),
        px.bar(df,x="Platform",y="EU_Sales",title="10. EU Sales")
    ]

    col1,col2 = st.columns(2)
    for i,fig in enumerate(charts):
        with col1 if i%2==0 else col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.plotly_chart(premium(fig),use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

# ================= SALES =================
elif menu == "💰 Sales":

    st.title("💰 Sales Analysis")

    genre = st.selectbox("Genre", ["All"] + list(sales["Genre"].unique()))
    df = sales if genre=="All" else sales[sales["Genre"]==genre]

    charts = [
        px.bar(df,x="Platform",y="Global_Sales",title="1. Platform Sales"),
        px.pie(df,names="Genre",values="Global_Sales",title="2. Genre"),
        px.box(df,x="Genre",y="Global_Sales",title="3. Box"),
        px.histogram(df,x="Global_Sales",title="4. Histogram"),
        px.scatter(df,x="Year",y="Global_Sales",title="5. Scatter"),
        px.bar(df,x="Platform",y="NA_Sales",title="6. NA"),
        px.bar(df,x="Platform",y="EU_Sales",title="7. EU"),
        px.bar(df,x="Platform",y="JP_Sales",title="8. JP"),
        px.bar(df,x="Platform",y="Other_Sales",title="9. Other"),
        px.line(df.groupby("Year")["Global_Sales"].sum().reset_index(),x="Year",y="Global_Sales",title="10. Trend")
    ]

    col1,col2 = st.columns(2)
    for i,fig in enumerate(charts):
        with col1 if i%2==0 else col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.plotly_chart(premium(fig),use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

# ================= SQL =================
elif menu == "🧮 SQL Analysis":

    st.title("🧮 SQL Analysis (15 Queries)")

    conn = sqlite3.connect("games.db")
    games.to_sql("games",conn,if_exists="replace",index=False)
    sales.to_sql("vgsales",conn,if_exists="replace",index=False)

    queries = {
        f"Query {i}": q for i,q in enumerate([
            "SELECT * FROM games LIMIT 10",
            "SELECT * FROM vgsales LIMIT 10",
            "SELECT Genre, SUM(Global_Sales) FROM vgsales GROUP BY Genre",
            "SELECT Platform, SUM(Global_Sales) FROM vgsales GROUP BY Platform",
            "SELECT Publisher, SUM(Global_Sales) FROM vgsales GROUP BY Publisher",
            "SELECT Year, SUM(Global_Sales) FROM vgsales GROUP BY Year",
            "SELECT Name, Global_Sales FROM vgsales ORDER BY Global_Sales DESC LIMIT 10",
            "SELECT Genre, AVG(Global_Sales) FROM vgsales GROUP BY Genre",
            "SELECT Platform, AVG(Global_Sales) FROM vgsales GROUP BY Platform",
            "SELECT COUNT(*) FROM vgsales",
            "SELECT Genre, COUNT(*) FROM vgsales GROUP BY Genre",
            "SELECT Platform, COUNT(*) FROM vgsales GROUP BY Platform",
            "SELECT Year, COUNT(*) FROM vgsales GROUP BY Year",
            "SELECT Publisher, COUNT(*) FROM vgsales GROUP BY Publisher",
            "SELECT Genre, Platform, SUM(Global_Sales) FROM vgsales GROUP BY Genre, Platform"
        ],1)
    }

    q = st.selectbox("Select Query", list(queries.keys()))
    df_sql = pd.read_sql(queries[q],conn)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.dataframe(df_sql)
    st.markdown('</div>', unsafe_allow_html=True)
