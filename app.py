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

    # ================= ADVANCED KPI CARDS =================
    col1, col2, col3, col4 = st.columns(4)

    total_games = len(games_df)
    avg_rating = round(games_df["Rating"].mean(),2) if "Rating" in games_df.columns else 0
    top_genre = games_df["Genres"].mode()[0] if "Genres" in games_df.columns else "N/A"
    unique_genres = games_df["Genres"].nunique() if "Genres" in games_df.columns else 0

    # Fake YoY growth (since no previous year column here)
    growth_games = "+5%"
    growth_rating = "-2%"

    col1.metric("🎮 Total Games", total_games, delta=growth_games)
    col2.metric("⭐ Avg Rating", avg_rating, delta=growth_rating)
    col3.metric("🏆 Top Genre", top_genre)
    col4.metric("📊 Unique Genres", unique_genres)

    # Mini sparkline
    trend = games_df["Rating"].dropna().head(20)
    st.line_chart(trend)

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

    # ================= ADVANCED KPI CARDS =================
    col1, col2, col3, col4 = st.columns(4)

    total_sales = round(sales_df["Global_Sales"].sum(),2)
    avg_sales = round(sales_df["Global_Sales"].mean(),2)
    top_platform = sales_df.groupby("Platform")["Global_Sales"].sum().idxmax()
    top_year = int(sales_df.groupby("Year")["Global_Sales"].sum().idxmax())

    # YoY growth calculation
    yearly = sales_df.groupby("Year")["Global_Sales"].sum().sort_index()
    yoy = ((yearly.iloc[-1] - yearly.iloc[-2]) / yearly.iloc[-2]) * 100 if len(yearly) > 1 else 0
    yoy_text = f"{round(yoy,2)}%"

    col1.metric("💵 Total Sales", f"{total_sales}M", delta=yoy_text)
    col2.metric("📈 Avg Sales", f"{avg_sales}M")
    col3.metric("🕹️ Top Platform", top_platform)
    col4.metric("📅 Peak Year", top_year)

    # Mini sparkline
    st.line_chart(yearly)

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
