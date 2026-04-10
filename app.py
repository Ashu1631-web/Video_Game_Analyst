# ======================================================
# 🎮 GAME SALES PRO - FINAL CLEAN (NO ERRORS)
# ======================================================

import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Game Sales Pro", layout="wide")

# ---------------- LOGIN ----------------
def login_user(u, p):
    return u == "admin" and p == "1234"

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/games.csv")
    df.dropna(inplace=True)
    return df

# ---------------- EXPORT ----------------
def to_excel(df):
    output = BytesIO()
    df.to_excel(output, index=False)
    return output.getvalue()

# ---------------- LOGIN PAGE ----------------
def login_page():
    st.markdown("""
    <style>
    .stApp {background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);} 
    .box {background: rgba(0,0,0,0.7); padding:40px; border-radius:20px; width:420px; margin:auto; margin-top:80px; text-align:center}
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='box'>", unsafe_allow_html=True)
    st.markdown("## 🎮 Video Game Sales Analysis")
    st.markdown("### Secure Admin Access")

    with st.form("login_form"):
        u = st.text_input("Username", key="login_user")
        p = st.text_input("Password", type="password", key="login_pass")
        submit = st.form_submit_button("Login")

        if submit:
            if login_user(u, p):
                st.session_state.logged_in = True
                st.success("Welcome Admin ✅")
                st.rerun()
            else:
                st.error("Invalid Credentials ❌")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- FILTER ----------------
def apply_filters(df):
    st.sidebar.header("Filters")
    years = st.sidebar.multiselect("Year", sorted(df.Year.unique()), default=sorted(df.Year.unique()))
    genres = st.sidebar.multiselect("Genre", df.Genre.unique(), default=df.Genre.unique())
    platforms = st.sidebar.multiselect("Platform", df.Platform.unique(), default=df.Platform.unique())

    return df[(df.Year.isin(years)) & (df.Genre.isin(genres)) & (df.Platform.isin(platforms))]

# ---------------- DASHBOARD ----------------
def dashboard(df):
    st.title("Dashboard")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Sales", round(df.Global_Sales.sum(), 2))
    c2.metric("Games", len(df))
    c3.metric("Platforms", df.Platform.nunique())

    charts = [
        px.bar(df, x="Genre", y="Global_Sales"),
        px.line(df, x="Year", y="Global_Sales"),
        px.pie(df, names="Platform"),
        px.scatter(df, x="NA_Sales", y="EU_Sales"),
        px.box(df, x="Genre", y="Global_Sales"),
        px.histogram(df, x="Global_Sales"),
        px.sunburst(df, path=["Genre", "Platform"], values="Global_Sales"),
        px.area(df, x="Year", y="Global_Sales"),
        px.violin(df, y="Global_Sales", x="Genre"),
        px.treemap(df, path=["Platform", "Genre"], values="Global_Sales"),
        px.scatter_3d(df, x="NA_Sales", y="EU_Sales", z="JP_Sales"),
        px.density_heatmap(df, x="NA_Sales", y="EU_Sales"),
        px.ecdf(df, x="Global_Sales"),
        px.bar(df.groupby("Platform").sum(numeric_only=True).reset_index(), x="Platform", y="Global_Sales"),
        px.line(df.groupby("Year").sum(numeric_only=True).reset_index(), x="Year", y="Global_Sales")
    ]

    for fig in charts:
        st.plotly_chart(fig, use_container_width=True)

# ---------------- SQL ----------------
def sql_section(df):
    st.title("SQL Analysis")

    options = {
        "Total Games": lambda: len(df),
        "Total Sales": lambda: df.Global_Sales.sum(),
        "Top 10": lambda: df.sort_values("Global_Sales", ascending=False).head(10),
        "Genre Sales": lambda: df.groupby("Genre").Global_Sales.sum(),
        "Year Trend": lambda: df.groupby("Year").Global_Sales.sum(),
        "Top Platform": lambda: df.groupby("Platform").Global_Sales.sum().idxmax(),
        "Average Sales": lambda: df.Global_Sales.mean(),
        "NA vs EU": lambda: df[["NA_Sales", "EU_Sales"]].sum(),
        "After 2010": lambda: df[df.Year > 2010],
        "Max Game": lambda: df.loc[df.Global_Sales.idxmax()],
        "Min Game": lambda: df.loc[df.Global_Sales.idxmin()],
        "Genre Count": lambda: df.Genre.value_counts(),
        "Platform Count": lambda: df.Platform.value_counts(),
        "Top 3 Genre": lambda: df.groupby("Genre").Global_Sales.sum().nlargest(3),
        "Year Count": lambda: df.Year.value_counts()
    }

    choice = st.selectbox("Select Query", list(options.keys()))
    st.write(options[choice]())

# ---------------- AI ----------------
def ai_section(df):
    st.title("AI Insights")
    st.success(f"Top Genre: {df.groupby('Genre').Global_Sales.sum().idxmax()}")
    st.info(f"Average Sales: {round(df.Global_Sales.mean(), 2)}")

# ---------------- MAIN ----------------
def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.markdown("<style>section[data-testid='stSidebar']{display:none}</style>", unsafe_allow_html=True)
        login_page()
        return

    df = load_data()
    df = apply_filters(df)

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go", ["Dashboard", "SQL", "AI", "Export"])

    if page == "Dashboard":
        dashboard(df)
    elif page == "SQL":
        sql_section(df)
    elif page == "AI":
        ai_section(df)
    elif page == "Export":
        st.download_button("Download Excel", to_excel(df), "data.xlsx")

# ---------------- RUN ----------------
if __name__ == "__main__":
    main()
