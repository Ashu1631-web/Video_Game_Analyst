# =========================================
# 🎮 FINAL ULTRA DASHBOARD APP (PREMIUM UI)
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

# ================= PREMIUM UI =================
st.markdown("""
<style>

/* ORANGE GRADIENT AFTER LOGIN */
.stApp {
    background: linear-gradient(135deg, #ff7e00, #ff3c00);
}

/* GLASS CARD */
.card {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(12px);
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 10px;
    box-shadow: 0 0 15px rgba(0,0,0,0.3);
}

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
        background-position:center;
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
        font=dict(color="white"),
        title_font=dict(size=20),
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
    st.title("🎮 Navigation")
    menu = st.radio("", [
        "📌 Overview","📊 Dashboard","💰 Sales",
        "🎮 Engagement","🧠 Insights","📈 ML Forecast",
        "🧮 SQL Analysis"
    ])

# ================= OVERVIEW =================
if menu == "📌 Overview":
    st.title("🎮 Video Game Dashboard")
    st.info("Premium Gaming Analytics UI 🚀")

# ================= DASHBOARD =================
elif menu == "📊 Dashboard":

    st.title("📊 Advanced Dashboard")

    c1, c2 = st.columns(2)

    with c1:
        fig = px.bar(sales, x="Platform", y="Global_Sales", title="Sales by Platform")
        fig = premium(fig)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        fig = px.bar(sales, x="Genre", y="Global_Sales", title="Sales by Genre")
        fig = premium(fig)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ================= SALES =================
elif menu == "💰 Sales":

    st.title("💰 Sales Analysis")

    col1, col2 = st.columns(2)

    with col1:
        fig = px.pie(sales, names="Genre", values="Global_Sales")
        fig = premium(fig)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        fig = px.box(sales, x="Genre", y="Global_Sales")
        fig = premium(fig)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ================= ENGAGEMENT =================
elif menu == "🎮 Engagement":

    st.title("🎮 Engagement")

    col1, col2 = st.columns(2)

    with col1:
        fig = px.histogram(games, x="Rating")
        fig = premium(fig)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        fig = px.scatter(games, x="Rating", y="Wishlist")
        fig = premium(fig)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ================= INSIGHTS =================
elif menu == "🧠 Insights":

    st.title("🧠 Insights")

    merged = pd.merge(games, sales, left_on="Title", right_on="Name")

    col1, col2 = st.columns(2)

    with col1:
        fig = px.scatter(merged, x="Rating", y="Global_Sales")
        fig = premium(fig)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        fig = px.sunburst(merged, path=["Genre", "Platform"], values="Global_Sales")
        fig = premium(fig)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ================= ML =================
elif menu == "📈 ML Forecast":

    st.title("📈 Forecast")

    df_ml = sales.groupby("Year")["Global_Sales"].sum().reset_index()
    model = LinearRegression().fit(df_ml[["Year"]], df_ml["Global_Sales"])

    future = pd.DataFrame({"Year": list(range(int(df_ml["Year"].max())+1, int(df_ml["Year"].max())+6))})
    future["Forecast"] = model.predict(future)

    col1, col2 = st.columns(2)

    with col1:
        fig = px.line(df_ml, x="Year", y="Global_Sales")
        fig = premium(fig)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        fig = px.line(future, x="Year", y="Forecast")
        fig = premium(fig)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ================= SQL =================
elif menu == "🧮 SQL Analysis":

    st.title("🧮 SQL Analysis")

    conn = sqlite3.connect("games.db", check_same_thread=False)
    games.to_sql("games", conn, if_exists="replace", index=False)
    sales.to_sql("vgsales", conn, if_exists="replace", index=False)

    df_sql = pd.read_sql("SELECT Platform, SUM(Global_Sales) as total_sales FROM vgsales GROUP BY Platform", conn)

    fig = px.bar(df_sql, x="Platform", y="total_sales")
    fig = premium(fig)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
