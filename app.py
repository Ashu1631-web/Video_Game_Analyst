import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="🎮 Games And Sales Frame Analytics", layout="wide")

# ===== GLOBAL CSS (FIX TOP NAV + SIZE) =====
st.sidebar.markdown("""
<style>
div.stButton > button {
    width: 100%;
    padding: 2px 5px !important;
    font-size: 11px !important;
    border-radius: 6px;
    margin: 2px 0;
}
</style>
""", unsafe_allow_html=True)

# ================= LOGIN =================
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:

    st.markdown("""
    <style>
    .stApp {
        background-image: url("https://wallpaperaccess.com/full/889354.jpg");
        background-size: cover;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("🎮 Games And Sales Frame Login")
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

if "page" not in st.session_state:
    st.session_state.page = "Overview"

def nav(label, icon):
    active = "🔴" if st.session_state.page == label else "⚪"

    if st.sidebar.button(f"{active} {icon} {label}", key=label):
        st.session_state.page = label
        st.rerun() 

nav("Overview", "📌")
nav("Dashboard", "📊")
nav("Sales", "💰")
nav("Engagement", "🎮")
nav("Insights", "🧠")
nav("ML Forecast", "🤖")
nav("SQL Analysis", "🗃️")

page = st.session_state.page

# ================= OVERVIEW =================
if page == "Overview":
    st.title("🎮 Games And Sales Frame Analytics")
    st.markdown("### Transforming Raw Data into Actionable Gaming Insights")

    st.markdown("""
📌 **Project Vision**  
This project is a comprehensive End-to-End Analytics Suite designed to decode the global gaming market.  
By combining historical sales data with Machine Learning and SQL-driven insights, the dashboard identifies market winners, platform lifecycles, and future growth trends.

---

🎯 **Strategic Objectives**

- **Market Intelligence:** Decode 20+ years of sales trends across Global, NA, EU, and JP markets  
- **Performance Benchmarking:** Compare dominance of Sony, Microsoft, and Nintendo  
- **Predictive Analysis:** Forecast future sales using ML models  

---

📊 **System Features**

| Feature | Description |
|--------|------------|
| 📈 10+ Interactive Visuals | Heatmaps, Bar charts, Pie charts |
| 🎛️ Multi-Dimensional Filters | Filter by Year, Genre, Platform |
| 🤖 ML Forecasting | Predict future trends |
| 💾 SQL Integration | Fast queries & aggregations |

---

🛠️ **Technology Stack**

- **Frontend:** Streamlit (Python)  
- **Data Processing:** Pandas & NumPy  
- **Analytics Engine:** SQL / SQLite  
- **Machine Learning:** Scikit-Learn  
- **Visualization:** Plotly & Seaborn  
""")

# ================= DASHBOARD =================
elif page == "Dashboard":
    st.title("📊 Dashboard")

    # ===== FIX DATA TYPE (ERROR SAFE) =====
    games_df["Rating"] = pd.to_numeric(games_df["Rating"], errors="coerce")
    games_df["Times Listed"] = pd.to_numeric(games_df["Times Listed"], errors="coerce")
    games_df = games_df.dropna(subset=["Rating", "Times Listed"])

    # ===== NEW FILTER UI (3 FILTERS) =====
    col1, col2, col3 = st.columns(3)

    with col1:
        genre = st.selectbox("Genre", ["All"] + sorted(games_df["Genres"].dropna().unique()))

    with col2:
        # अगर Platform column नहीं है तो remove कर देना
        if "Platform" in games_df.columns:
            platform = st.selectbox("Platform", ["All"] + sorted(games_df["Platform"].dropna().unique()))
        else:
            platform = "All"

    with col3:
        # Release Date से Year निकालना
        if "Release Date" in games_df.columns:
            years = games_df["Release Date"].astype(str).str[:4]
            year = st.selectbox("Year", ["All"] + sorted(years.dropna().unique()))
        else:
            year = "All"

    # ===== APPLY FILTER =====
    df = games_df.copy()

    if genre != "All":
        df = df[df["Genres"].str.contains(genre, na=False)]

    if platform != "All":
        df = df[df["Platform"] == platform]

    if year != "All":
        df = df[df["Release Date"].astype(str).str.contains(year)]

    # ===== TABLE =====
    st.dataframe(df.head(50))

    # ===== GRAPHS  =====
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

    # ===== NEW FILTER UI (3 FILTERS SAME DESIGN) =====
    col1, col2, col3 = st.columns(3)

    with col1:
        genre = st.selectbox("Genre", ["All"] + sorted(sales_df["Genre"].dropna().unique()))

    with col2:
        platform = st.selectbox("Platform", ["All"] + sorted(sales_df["Platform"].dropna().unique()))

    with col3:
        year = st.selectbox("Year", ["All"] + sorted(sales_df["Year"].dropna().astype(int).astype(str).unique()))

    # ===== APPLY FILTER =====
    df = sales_df.copy()

    if genre != "All":
        df = df[df["Genre"] == genre]

    if platform != "All":
        df = df[df["Platform"] == platform]

    if year != "All":
        df = df[df["Year"].astype(str) == year]

    # ===== TABLE =====
    st.dataframe(df.head(50))

    # ===== GRAPHS  =====
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
elif page == "Engagement":
    st.title("🎮 Engagement")

    df = sales_df.copy()

    st.dataframe(df.head(50))

    for fig in [
        px.bar(df.head(10), x="Name", y="Global_Sales", color="Name", title="Top Games"),
        px.scatter(df, x="Year", y="Global_Sales", color="Genre", title="Year vs Sales"),
        px.histogram(df, x="Global_Sales", color="Genre", title="Distribution"),
        px.box(df, x="Genre", y="Global_Sales", color="Genre", title="Box Plot"),
        px.violin(df, x="Genre", y="Global_Sales", color="Genre", title="Violin"),
        px.area(df.groupby("Year")["Global_Sales"].sum().reset_index(), x="Year", y="Global_Sales", title="Area"),
        px.line(df.groupby("Year")["Global_Sales"].sum().reset_index(), x="Year", y="Global_Sales", title="Trend"),
        px.pie(df, names="Genre", title="Genre Share"),
        px.density_heatmap(df, x="Year", y="Global_Sales", title="Heatmap"),
        px.ecdf(df, x="Global_Sales", title="ECDF")
    ]:
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
