import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import sqlite3
from streamlit_option_menu import option_menu

# ================= CONFIG =================
st.set_page_config(page_title="Game Analytics Pro", layout="wide")

# ================= LOGIN =================
def login():
    st.title("🔐 Login System")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("Login"):
        if u == "admin" and p == "1234":
            st.session_state.auth = True
        else:
            st.error("Invalid Credentials")

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    login()
    st.stop()

# ================= LOAD DATA =================
@st.cache_data
def load():
    g = pd.read_csv("data/games.csv")
    s = pd.read_csv("data/vgsales.csv")
    return g, s

games, sales = load()

# ================= SQL SETUP =================
conn = sqlite3.connect("games.db", check_same_thread=False)
games.to_sql("games", conn, if_exists="replace", index=False)
sales.to_sql("vgsales", conn, if_exists="replace", index=False)

# ================= FILTERS =================
st.sidebar.header("Filters")
genre = st.sidebar.multiselect("Genre", sales['Genre'].unique())
year = st.sidebar.slider("Year", int(sales['Year'].min()), int(sales['Year'].max()), (2000, 2015))
platform = st.sidebar.multiselect("Platform", sales['Platform'].unique())

filtered = sales.copy()
if genre:
    filtered = filtered[filtered['Genre'].isin(genre)]
if platform:
    filtered = filtered[filtered['Platform'].isin(platform)]
filtered = filtered[(filtered['Year']>=year[0]) & (filtered['Year']<=year[1])]

# ================= MENU =================
with st.sidebar:
    selected = option_menu("Menu",
        ["Dashboard","Sales","Engagement","Insights","SQL Analysis","Download","Admin"])

# ================= DASHBOARD =================
if selected == "Dashboard":
    st.title("📊 Dashboard")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total Sales", round(filtered['Global_Sales'].sum(),2))
    c2.metric("Avg Sales", round(filtered['Global_Sales'].mean(),2))
    c3.metric("Top Genre", filtered.groupby('Genre')['Global_Sales'].sum().idxmax())
    c4.metric("Top Platform", filtered.groupby('Platform')['Global_Sales'].sum().idxmax())

    st.plotly_chart(px.line(filtered.groupby('Year')['Global_Sales'].sum().reset_index(), x='Year', y='Global_Sales'))

# ================= SALES =================
elif selected == "Sales":
    st.title("💰 Sales Analysis")

    st.plotly_chart(px.bar(filtered.groupby('Platform')['Global_Sales'].sum().reset_index(), x='Platform', y='Global_Sales'))
    st.plotly_chart(px.pie(filtered, names='Genre', values='Global_Sales'))
    st.plotly_chart(px.box(filtered, x='Genre', y='Global_Sales'))
    st.plotly_chart(px.area(filtered.groupby('Year')['Global_Sales'].sum().reset_index(), x='Year', y='Global_Sales'))
    st.plotly_chart(px.scatter(filtered, x='Year', y='Global_Sales', color='Genre'))

# ================= ENGAGEMENT =================
elif selected == "Engagement":
    st.title("🎮 Engagement")

    st.plotly_chart(px.histogram(games, x='Rating'))
    st.plotly_chart(px.scatter(games, x='Rating', y='Wishlist'))
    st.plotly_chart(px.box(games, x='Genres', y='Rating'))
    st.plotly_chart(px.bar(games.nlargest(10,'Wishlist'), x='Title', y='Wishlist'))

# ================= INSIGHTS =================
elif selected == "Insights":
    st.title("🧠 Insights")
    merged = pd.merge(games, sales, left_on="Title", right_on="Name")

    st.plotly_chart(px.scatter(merged, x='Rating', y='Global_Sales', color='Genre'))
    st.plotly_chart(px.density_heatmap(merged, x='Genre', y='Platform'))
    st.plotly_chart(px.sunburst(merged, path=['Genre','Platform'], values='Global_Sales'))
    st.plotly_chart(px.treemap(merged, path=['Publisher','Genre'], values='Global_Sales'))

# ================= SQL =================
elif selected == "SQL Analysis":
    st.title("🧮 SQL Analysis")

    queries = {
        "Top Platforms": "SELECT Platform, SUM(Global_Sales) as total_sales FROM vgsales GROUP BY Platform ORDER BY total_sales DESC",
        "Top Publishers": "SELECT Publisher, SUM(Global_Sales) as total_sales FROM vgsales GROUP BY Publisher ORDER BY total_sales DESC LIMIT 10",
        "Yearly Trend": "SELECT Year, SUM(Global_Sales) as total_sales FROM vgsales GROUP BY Year",
        "Top Rated Games": "SELECT Title, Rating FROM games ORDER BY Rating DESC LIMIT 10",
        "Wishlist vs Sales": "SELECT g.Title, g.Wishlist, v.Global_Sales FROM games g JOIN vgsales v ON g.Title = v.Name"
    }

    choice = st.selectbox("Select Query", list(queries.keys()))
    df = pd.read_sql(queries[choice], conn)

    st.dataframe(df)
    st.plotly_chart(px.bar(df, x=df.columns[0], y=df.columns[1]), use_container_width=True)

# ================= DOWNLOAD =================
elif selected == "Download":
    st.title("📥 Download Data")
    st.download_button("Download CSV", filtered.to_csv(index=False), "filtered_data.csv")

# ================= ADMIN =================
elif selected == "Admin":
    st.title("⚙️ Admin Panel")
    if st.button("Logout"):
        st.session_state.auth=False
        st.rerun()

# ================= FOOTER =================
st.markdown("---")
st.markdown("🚀 Final Production Dashboard")
