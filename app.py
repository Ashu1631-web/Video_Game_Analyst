import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Video Game Analytics", layout="wide")

# ================= CACHE =================
@st.cache_data
def load_games():
    return pd.read_csv("games.csv")

@st.cache_data
def load_sales():
    return pd.read_csv("vgsales.csv")

# ================= LOAD DATA =================
games_df = load_games()
sales_df = load_sales()

# ================= SIDEBAR =================
st.sidebar.title("🎮 Navigation")
page = st.sidebar.radio("Go to", ["Overview","Dashboard","Sales","Engagement","Insights","ML Forecast","SQL Analysis"])

# ================= OVERVIEW =================
if page == "Overview":
    st.title("🎮 Video Game Sales & Market Analytics")
    st.markdown("### Transforming Raw Data into Actionable Gaming Insights")

    st.markdown("""
📌 Project Vision  
End-to-End Analytics Suite for global gaming market.

🎯 Strategic Objectives
- Analyze 20+ years sales
- Compare Sony, Microsoft, Nintendo
- Predict future trends

📊 Features
- 10+ Interactive Visuals
- Filters (Year, Genre, Platform)
- ML Forecasting
- SQL Analysis

🛠️ Tech Stack
- Streamlit, Pandas, Plotly, Scikit-learn
""")

# ================= DASHBOARD =================
elif page == "Dashboard":
    st.title("📊 Dashboard")

    # ================= KPI CARDS =================
    col1, col2, col3, col4 = st.columns(4)

    total_games = len(games_df)
    avg_rating = round(games_df["Rating"].mean(),2) if "Rating" in games_df.columns else 0
    top_genre = games_df["Genres"].mode()[0] if "Genres" in games_df.columns else "N/A"
    unique_genres = games_df["Genres"].nunique() if "Genres" in games_df.columns else 0

    col1.metric("🎮 Total Games", total_games)
    col2.metric("⭐ Avg Rating", avg_rating)
    col3.metric("🏆 Top Genre", top_genre)
    col4.metric("📊 Unique Genres", unique_genres)

    genre = st.selectbox("Genre", ["All"] + list(games_df["Genres"].dropna().unique()))
    st.title("📊 Dashboard")

    genre = st.selectbox("Genre", ["All"] + list(games_df["Genres"].dropna().unique()))

    df = games_df.copy()

    if genre != "All":
        df = df[df["Genres"].str.contains(genre, na=False)]

    if df.empty:
        st.warning("No data available")
        st.stop()

    st.dataframe(df.head(50))

    # 10 GRAPHS
    st.plotly_chart(px.bar(df.head(10), x="Title", y="Rating", title="Top Ratings", color="Title"))
    st.plotly_chart(px.histogram(df, x="Rating", title="Rating Distribution"))
    st.plotly_chart(px.pie(df.head(10), names="Genres", title="Genre Share"))
    st.plotly_chart(px.box(df, x="Genres", y="Rating", title="Genre vs Rating"))
    st.plotly_chart(px.scatter(df, x="Rating", y="Rating", title="Rating Scatter"))
    st.plotly_chart(px.violin(df, x="Genres", y="Rating", title="Violin Plot"))
    st.plotly_chart(px.density_heatmap(df, x="Rating", y="Rating", title="Heatmap"))
    st.plotly_chart(px.ecdf(df, x="Rating", title="ECDF"))
    st.plotly_chart(px.area(df.head(20), x="Title", y="Rating", title="Area Plot"))
    st.plotly_chart(px.line(df.head(20), x="Title", y="Rating", title="Line Plot"))

# ================= SALES =================
elif page == "Sales":
    st.title("💰 Sales")

    # ================= KPI CARDS =================
    col1, col2, col3, col4 = st.columns(4)

    total_sales = round(sales_df["Global_Sales"].sum(),2)
    avg_sales = round(sales_df["Global_Sales"].mean(),2)
    top_platform = sales_df.groupby("Platform")["Global_Sales"].sum().idxmax()
    top_year = int(sales_df.groupby("Year")["Global_Sales"].sum().idxmax())

    col1.metric("💵 Total Sales", f"{total_sales}M")
    col2.metric("📈 Avg Sales", f"{avg_sales}M")
    col3.metric("🕹️ Top Platform", top_platform)
    col4.metric("📅 Peak Year", top_year)

    genre = st.selectbox("Genre", ["All"] + list(sales_df["Genre"].dropna().unique()))
    st.title("💰 Sales")

    genre = st.selectbox("Genre", ["All"] + list(sales_df["Genre"].dropna().unique()))

    df = sales_df.copy()

    if genre != "All":
        df = df[df["Genre"] == genre]

    if df.empty:
        st.warning("No data")
        st.stop()

    st.dataframe(df.head(50))

    grouped = df.groupby("Platform")["Global_Sales"].sum().reset_index()

    # 10 GRAPHS
    st.plotly_chart(px.bar(grouped, x="Platform", y="Global_Sales", title="Platform Sales", color="Platform"))
    st.plotly_chart(px.pie(df, names="Genre", title="Genre Share"))
    st.plotly_chart(px.line(df.groupby("Year")["Global_Sales"].sum().reset_index(), x="Year", y="Global_Sales", title="Trend"))
    st.plotly_chart(px.histogram(df, x="Global_Sales", title="Distribution"))
    st.plotly_chart(px.box(df, x="Genre", y="Global_Sales", title="Genre vs Sales"))
    st.plotly_chart(px.scatter(df, x="Year", y="Global_Sales", title="Year vs Sales"))
    st.plotly_chart(px.area(df.groupby("Year")["Global_Sales"].sum().reset_index(), x="Year", y="Global_Sales", title="Area Trend"))
    st.plotly_chart(px.violin(df, x="Genre", y="Global_Sales", title="Violin"))
    st.plotly_chart(px.density_heatmap(df, x="Year", y="Global_Sales", title="Heatmap"))
    st.plotly_chart(px.ecdf(df, x="Global_Sales", title="ECDF"))

# ================= ENGAGEMENT =================
elif page == "Engagement":
    st.title("🎮 Engagement")

    df = sales_df.copy()

    # 10 GRAPHS
    st.plotly_chart(px.bar(df.head(10), x="Name", y="Global_Sales", title="Top Games"))
    st.plotly_chart(px.scatter(df, x="Year", y="Global_Sales", title="Scatter"))
    st.plotly_chart(px.histogram(df, x="Global_Sales", title="Histogram"))
    st.plotly_chart(px.box(df, x="Genre", y="Global_Sales", title="Box"))
    st.plotly_chart(px.violin(df, x="Genre", y="Global_Sales", title="Violin"))
    st.plotly_chart(px.area(df.groupby("Year")["Global_Sales"].sum().reset_index(), x="Year", y="Global_Sales", title="Area"))
    st.plotly_chart(px.line(df.groupby("Year")["Global_Sales"].sum().reset_index(), x="Year", y="Global_Sales", title="Line"))
    st.plotly_chart(px.pie(df, names="Genre", title="Pie"))
    st.plotly_chart(px.density_heatmap(df, x="Year", y="Global_Sales", title="Heatmap"))
    st.plotly_chart(px.ecdf(df, x="Global_Sales", title="ECDF"))

# ================= INSIGHTS =================
elif page == "Insights":
    st.title("🧠 Insights")

    st.write("Top Genre:", sales_df.groupby("Genre")["Global_Sales"].sum().idxmax())
    st.write("Top Platform:", sales_df.groupby("Platform")["Global_Sales"].sum().idxmax())
    st.write("Peak Year:", sales_df.groupby("Year")["Global_Sales"].sum().idxmax())

# ================= ML FORECAST =================
elif page == "ML Forecast":
    st.title("🤖 ML Forecast")

    year_range = st.slider("Year Range", int(sales_df.Year.min()), int(sales_df.Year.max()), (2000,2015))
    df = sales_df[(sales_df["Year"] >= year_range[0]) & (sales_df["Year"] <= year_range[1])]

    st.plotly_chart(px.line(df.groupby("Year")["Global_Sales"].sum().reset_index(), x="Year", y="Global_Sales", title="Forecast Trend"))

# ================= SQL =================
elif page == "SQL Analysis":
    st.title("🗃️ SQL Analysis")

    queries = {
        "Top Games": ("Top selling games", sales_df.sort_values("Global_Sales", ascending=False).head(10)),
        "Genre Sales": ("Sales per genre", sales_df.groupby("Genre")["Global_Sales"].sum().reset_index())
    }

    q = st.selectbox("Select Query", list(queries.keys()))
    st.info(queries[q][0])
    st.dataframe(queries[q][1])
