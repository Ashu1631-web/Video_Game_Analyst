import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Video Game Analytics", layout="wide")

# ================= LOGIN =================
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.markdown("""
    <style>
    .stApp {
        background-image: url("https://wallpaperaccess.com/full/236603.jpg");
        background-size: cover;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("🎮 Login Page")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if u == "admin" and p == "1234":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Wrong Credentials")
    st.stop()

# ================= LOAD =================
@st.cache_data
def load_games():
    return pd.read_csv("data/games.csv")

@st.cache_data
def load_sales():
    return pd.read_csv("data/vgsales.csv")

games_df = load_games()
sales_df = load_sales()

# ================= NAV =================
st.sidebar.title("🎮 Navigation")
page = st.sidebar.radio("Go to", ["Overview","Dashboard","Sales","Engagement", "Insights", "ML Forecast", "SQL Analysis"])

# ================= OVERVIEW =================
if page == "Overview":
    st.title("🎮 Video Game Sales & Market Analytics")

# ================= DASHBOARD =================
elif page == "Dashboard":
    st.title("📊 Dashboard")

    genre = st.selectbox("Genre", ["All"] + list(games_df["Genres"].dropna().unique()), key="d1")
    df = games_df.copy()
    if genre != "All":
        df = df[df["Genres"].str.contains(genre, na=False)]

    st.dataframe(df.head(50))

    for fig in [
        px.bar(df.head(10), x="Title", y="Rating", color="Title", title="Top Ratings"),
        px.histogram(df, x="Rating", color="Genres", title="Rating Distribution"),
        px.pie(df.head(10), names="Genres", title="Genre Share"),
        px.box(df, x="Genres", y="Rating", color="Genres", title="Genre vs Rating"),
        px.scatter(df, x="Rating", y="Rating", color="Genres", title="Scatter"),
        px.violin(df, x="Genres", y="Rating", color="Genres", title="Violin"),
        px.density_heatmap(df, x="Rating", y="Rating", title="Heatmap"),
        px.ecdf(df, x="Rating", title="ECDF"),
        px.area(df.head(20), x="Title", y="Rating", color="Genres", title="Area"),
        px.line(df.head(20), x="Title", y="Rating", color="Genres", title="Line")
    ]:
        st.plotly_chart(fig, use_container_width=True)

# ================= SALES =================
elif page == "Sales":
    st.title("💰 Sales")

    genre = st.selectbox("Genre", ["All"] + list(sales_df["Genre"].dropna().unique()), key="s1")
    df = sales_df.copy()
    if genre != "All":
        df = df[df["Genre"] == genre]

    st.dataframe(df.head(50))

    grouped = df.groupby("Platform")["Global_Sales"].sum().reset_index()

    for fig in [
        px.bar(grouped, x="Platform", y="Global_Sales", color="Platform", title="Platform Sales"),
        px.pie(df, names="Genre", title="Genre Share"),
        px.line(df.groupby("Year")["Global_Sales"].sum().reset_index(), x="Year", y="Global_Sales", title="Trend"),
        px.histogram(df, x="Global_Sales", color="Genre", title="Distribution"),
        px.box(df, x="Genre", y="Global_Sales", color="Genre", title="Genre vs Sales"),
        px.scatter(df, x="Year", y="Global_Sales", color="Genre", title="Scatter"),
        px.area(df.groupby("Year")["Global_Sales"].sum().reset_index(), x="Year", y="Global_Sales", title="Area"),
        px.violin(df, x="Genre", y="Global_Sales", color="Genre", title="Violin"),
        px.density_heatmap(df, x="Year", y="Global_Sales", title="Heatmap"),
        px.ecdf(df, x="Global_Sales", title="ECDF")
    ]:
        st.plotly_chart(fig, use_container_width=True)

# ================= ENGAGEMENT =================

    df = sales_df.copy()

    st.subheader("📊 Engagement Data")
    st.dataframe(df.head(50))

    charts = [
        px.bar(df.head(10), x="Name", y="Global_Sales", color="Name", title="Top Games by Sales"),
        px.scatter(df, x="Year", y="Global_Sales", color="Genre", title="Year vs Sales"),
        px.histogram(df, x="Global_Sales", color="Genre", title="Sales Distribution"),
        px.box(df, x="Genre", y="Global_Sales", color="Genre", title="Genre vs Sales"),
        px.violin(df, x="Genre", y="Global_Sales", color="Genre", title="Violin Plot"),
        px.area(df.groupby("Year")["Global_Sales"].sum().reset_index(), x="Year", y="Global_Sales", title="Area Trend"),
        px.line(df.groupby("Year")["Global_Sales"].sum().reset_index(), x="Year", y="Global_Sales", title="Line Trend"),
        px.pie(df, names="Genre", title="Genre Share"),
        px.density_heatmap(df, x="Year", y="Global_Sales", title="Heatmap"),
        px.ecdf(df, x="Global_Sales", title="ECDF")
    ]

    for fig in charts:
        st.plotly_chart(fig, use_container_width=True)

# ================= INSIGHTS =================
elif page == "Insights":
    st.title("🧠 Insights")

    top_genre = sales_df.groupby("Genre")["Global_Sales"].sum().idxmax()
    top_platform = sales_df.groupby("Platform")["Global_Sales"].sum().idxmax()
    peak_year = int(sales_df.groupby("Year")["Global_Sales"].sum().idxmax())
    total_sales = round(sales_df["Global_Sales"].sum(),2)

    st.markdown(f"""
    ### 📊 Key Business Insights

    - 🎯 **Top Genre:** {top_genre}
    - 🕹️ **Top Platform:** {top_platform}
    - 📅 **Peak Sales Year:** {peak_year}
    - 💰 **Total Global Sales:** {total_sales} Million

    ### 📈 Observations
    - Action & Sports dominate global market
    - Sales peak observed around early 2010s
    - North America contributes highest revenue
    """)

# ================= ML FORECAST =================
elif page == "ML Forecast":
    st.title("🤖 ML Forecast")

    year_range = st.slider("Select Year Range", int(sales_df.Year.min()), int(sales_df.Year.max()), (2000,2015))

    df = sales_df[(sales_df["Year"] >= year_range[0]) & (sales_df["Year"] <= year_range[1])]

    trend = df.groupby("Year")["Global_Sales"].sum().reset_index()

    st.subheader("📈 Sales Trend Forecast")
    st.plotly_chart(px.line(trend, x="Year", y="Global_Sales", color_discrete_sequence=["cyan"], title="Sales Trend"), use_container_width=True)

# ================= SQL =================
elif page == "SQL Analysis":
    st.title("🗃️ SQL Analysis")

    # 30 Queries with Questions
    queries = {
        "Q1": ("Top 10 highest selling games?", sales_df.sort_values("Global_Sales", ascending=False).head(10)),
        "Q2": ("Total sales by genre?", sales_df.groupby("Genre")["Global_Sales"].sum().reset_index()),
        "Q3": ("Total sales by platform?", sales_df.groupby("Platform")["Global_Sales"].sum().reset_index()),
        "Q4": ("Sales trend over years?", sales_df.groupby("Year")["Global_Sales"].sum().reset_index()),
        "Q5": ("Top 5 publishers?", sales_df.groupby("Publisher")["Global_Sales"].sum().nlargest(5).reset_index()),
        "Q6": ("Average sales per genre?", sales_df.groupby("Genre")["Global_Sales"].mean().reset_index()),
        "Q7": ("Games count per platform?", sales_df.groupby("Platform")["Name"].count().reset_index()),
        "Q8": ("Max sales by year?", sales_df.groupby("Year")["Global_Sales"].max().reset_index()),
        "Q9": ("Min sales by year?", sales_df.groupby("Year")["Global_Sales"].min().reset_index()),
        "Q10": ("Top genres by NA sales?", sales_df.groupby("Genre")["NA_Sales"].sum().reset_index()),
        "Q11": ("Top genres by EU sales?", sales_df.groupby("Genre")["EU_Sales"].sum().reset_index()),
        "Q12": ("Top genres by JP sales?", sales_df.groupby("Genre")["JP_Sales"].sum().reset_index()),
        "Q13": ("Top 10 games in NA?", sales_df.sort_values("NA_Sales", ascending=False).head(10)),
        "Q14": ("Top 10 games in EU?", sales_df.sort_values("EU_Sales", ascending=False).head(10)),
        "Q15": ("Top 10 games in JP?", sales_df.sort_values("JP_Sales", ascending=False).head(10)),
        "Q16": ("Year with highest NA sales?", sales_df.groupby("Year")["NA_Sales"].sum().reset_index()),
        "Q17": ("Year with highest EU sales?", sales_df.groupby("Year")["EU_Sales"].sum().reset_index()),
        "Q18": ("Year with highest JP sales?", sales_df.groupby("Year")["JP_Sales"].sum().reset_index()),
        "Q19": ("Top publishers in NA?", sales_df.groupby("Publisher")["NA_Sales"].sum().reset_index()),
        "Q20": ("Top publishers in EU?", sales_df.groupby("Publisher")["EU_Sales"].sum().reset_index()),
        "Q21": ("Top publishers in JP?", sales_df.groupby("Publisher")["JP_Sales"].sum().reset_index()),
        "Q22": ("Genre count?", sales_df["Genre"].value_counts().reset_index()),
        "Q23": ("Platform count?", sales_df["Platform"].value_counts().reset_index()),
        "Q24": ("Publisher count?", sales_df["Publisher"].value_counts().reset_index()),
        "Q25": ("Sales distribution?", sales_df[["Global_Sales"]]),
        "Q26": ("Correlation between regions?", sales_df[["NA_Sales","EU_Sales","JP_Sales"]].corr()),
        "Q27": ("Top year by global sales?", sales_df.groupby("Year")["Global_Sales"].sum().reset_index()),
        "Q28": ("Average sales per year?", sales_df.groupby("Year")["Global_Sales"].mean().reset_index()),
        "Q29": ("Top game per platform?", sales_df.sort_values("Global_Sales", ascending=False).drop_duplicates("Platform")),
        "Q30": ("Overall dataset preview?", sales_df.head(50))
    }

    selected = st.selectbox("Select Query", list(queries.keys()))

    st.subheader("❓ Question")
    st.info(queries[selected][0])

    st.subheader("📊 Result")
    st.dataframe(queries[selected][1])
