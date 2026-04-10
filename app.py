# ======================================================
# 🎮 GAME SALES PRO - FINAL PORTFOLIO (ULTRA PRO VERSION)
# Features: Login | 15 SQL | 15+ Charts | Filters | Export | AI | UI
# ======================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO

st.set_page_config(page_title="Game Sales Ultra Pro", layout="wide")

# ---------------- LOGIN ----------------
def login_user(u,p): return u=="admin" and p=="1234"

# ---------------- DATA ----------------
@st.cache_data
def load():
    df = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/games.csv")
    df.dropna(inplace=True)
    return df

# ---------------- EXPORT ----------------
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

# ---------------- LOGIN PAGE ----------------
def login_page():
    st.markdown("""
    <style>
    .stApp{background:linear-gradient(135deg,#0f2027,#203a43,#2c5364);} 
    .box{background:rgba(0,0,0,0.7);padding:40px;border-radius:20px;width:420px;margin:auto;margin-top:80px;text-align:center}
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='box'>", unsafe_allow_html=True)
    st.markdown("## 🎮 Video Game Sales Analysis")

    u=st.text_input("Username", key="login_username")
    p=st.text_input("Password",type="password", key="login_password")

    if st.button("Login", key="login_btn"):
        if login_user(u,p):
            st.session_state.logged_in=True
            st.success("Welcome Admin")
        else:
            st.error("Invalid Credentials")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- FILTER ----------------
def filters(df):
    st.sidebar.header("🎯 Filters")
    years=st.sidebar.multiselect("Year",sorted(df.Year.unique()),default=sorted(df.Year.unique()))
    genres=st.sidebar.multiselect("Genre",df.Genre.unique(),default=df.Genre.unique())
    plats=st.sidebar.multiselect("Platform",df.Platform.unique(),default=df.Platform.unique())
    return df[(df.Year.isin(years))&(df.Genre.isin(genres))&(df.Platform.isin(plats))]

# ---------------- DASHBOARD ----------------
def dashboard(df):
    st.title("📊 Ultra Dashboard")

    c1,c2,c3=st.columns(3)
    c1.metric("Sales",round(df.Global_Sales.sum(),2))
    c2.metric("Games",len(df))
    c3.metric("Platforms",df.Platform.nunique())

    charts=[
        px.bar(df,x="Genre",y="Global_Sales"),
        px.line(df,x="Year",y="Global_Sales"),
        px.pie(df,names="Platform"),
        px.scatter(df,x="NA_Sales",y="EU_Sales"),
        px.box(df,x="Genre",y="Global_Sales"),
        px.histogram(df,x="Global_Sales"),
        px.sunburst(df,path=["Genre","Platform"],values="Global_Sales"),
        px.density_heatmap(df,x="NA_Sales",y="EU_Sales"),
        px.area(df,x="Year",y="Global_Sales"),
        px.violin(df,y="Global_Sales",x="Genre"),
        px.treemap(df,path=["Platform","Genre"],values="Global_Sales"),
        px.ecdf(df,x="Global_Sales"),
        px.scatter_3d(df,x="NA_Sales",y="EU_Sales",z="JP_Sales"),
        px.line(df.groupby("Year").sum(numeric_only=True).reset_index(),x="Year",y="Global_Sales"),
        px.bar(df.groupby("Platform").sum(numeric_only=True).reset_index(),x="Platform",y="Global_Sales")
    ]

    for fig in charts: st.plotly_chart(fig,use_container_width=True)

# ---------------- SQL ----------------
def sql(df):
    st.title("🧠 SQL Engine")
    queries={
        "Total Games":lambda:len(df),
        "Total Sales":lambda:df.Global_Sales.sum(),
        "Top 10":lambda:df.sort_values("Global_Sales",ascending=False).head(10),
        "Genre Sales":lambda:df.groupby("Genre").Global_Sales.sum(),
        "Year Trend":lambda:df.groupby("Year").Global_Sales.sum(),
        "Top Platform":lambda:df.groupby("Platform").Global_Sales.sum().idxmax(),
        "Avg Sales":lambda:df.Global_Sales.mean(),
        "NA vs EU":lambda:df[["NA_Sales","EU_Sales"]].sum(),
        "Top Publisher":lambda:df.groupby("Publisher").Global_Sales.sum().idxmax() if 'Publisher'in df else "N/A",
        "After 2010":lambda:df[df.Year>2010],
        "Max Game":lambda:df.loc[df.Global_Sales.idxmax()],
        "Min Game":lambda:df.loc[df.Global_Sales.idxmin()],
        "Genre Count":lambda:df.Genre.value_counts(),
        "Platform Count":lambda:df.Platform.value_counts(),
        "Top 3 Genre":lambda:df.groupby("Genre").Global_Sales.sum().nlargest(3)
    }

    choice=st.selectbox("Query",list(queries.keys()))
    res=queries[choice]()
    st.write(res)

# ---------------- AI ----------------
def ai(df):
    st.title("🤖 AI Insights")
    st.success(f"Top Genre: {df.groupby('Genre').Global_Sales.sum().idxmax()}")
    st.info(f"Avg Sales: {round(df.Global_Sales.mean(),2)}")
    st.warning("Insight: Action games dominate market.")

# ---------------- MAIN ----------------
def main():
    if 'logged_in' not in st.session_state: st.session_state.logged_in=False

    if not st.session_state.logged_in:
        st.markdown("<style>section[data-testid='stSidebar']{display:none}</style>",unsafe_allow_html=True)
        login_page()
    else:
        df=filters(load())

        st.sidebar.title("Navigation")
        page=st.sidebar.radio("Go",["Dashboard","SQL","AI","Export"])

        if page=="Dashboard": dashboard(df)
        elif page=="SQL": sql(df)
        elif page=="AI": ai(df)
        elif page=="Export":
            st.download_button("Download Excel",to_excel(df),"data.xlsx")

if __name__=="__main__": main()
