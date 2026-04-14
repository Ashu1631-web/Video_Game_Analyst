import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sqlite3
from sklearn.linear_model import LinearRegression
import numpy as np

st.set_page_config(
    page_title="NEXUS | Game Analytics",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── PREMIUM GLOBAL CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;400;500;600;700&family=Exo+2:wght@100;200;300;400;500;600&family=Share+Tech+Mono&display=swap');

:root {
    --bg-primary:   #03040a;
    --bg-card:      #080c18;
    --bg-glass:     rgba(8, 12, 24, 0.85);
    --accent:       #00f5c4;
    --accent2:      #7c3aed;
    --accent3:      #f59e0b;
    --red:          #ef4444;
    --text-primary: #e2e8f0;
    --text-muted:   #64748b;
    --border:       rgba(0, 245, 196, 0.12);
    --border-glow:  rgba(0, 245, 196, 0.35);
    --font-head:    'Rajdhani', sans-serif;
    --font-body:    'Exo 2', sans-serif;
    --font-mono:    'Share Tech Mono', monospace;
}

html, body, .stApp {
    background: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: var(--font-body) !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #06091a 0%, #03040a 100%) !important;
    border-right: 1px solid var(--border-glow) !important;
    box-shadow: 4px 0 40px rgba(0,245,196,0.06) !important;
}
section[data-testid="stSidebar"] * { font-family: var(--font-head) !important; }

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stSidebarNav"] { display: none; }

/* ── Radio buttons ── */
div[data-testid="stRadio"] label {
    background: transparent !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    padding: 10px 16px !important;
    margin: 3px 0 !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    color: var(--text-muted) !important;
    font-family: var(--font-head) !important;
    font-size: 14px !important;
    letter-spacing: 0.5px !important;
    display: flex !important;
    align-items: center !important;
}
div[data-testid="stRadio"] label:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
    background: rgba(0,245,196,0.05) !important;
    box-shadow: 0 0 12px rgba(0,245,196,0.1) !important;
}
div[data-testid="stRadio"] label[data-checked="true"],
div[data-testid="stRadio"] input:checked + div {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
    background: rgba(0,245,196,0.08) !important;
}
div[data-testid="stRadio"] input { display: none !important; }

/* ── Selectboxes ── */
div[data-testid="stSelectbox"] > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-glow) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    font-family: var(--font-mono) !important;
    font-size: 13px !important;
}
div[data-testid="stSelectbox"] > div > div:hover {
    border-color: var(--accent) !important;
    box-shadow: 0 0 16px rgba(0,245,196,0.12) !important;
}

/* ── Metric cards ── */
div[data-testid="stMetric"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-glow) !important;
    border-radius: 12px !important;
    padding: 20px !important;
    box-shadow: 0 0 30px rgba(0,245,196,0.06), inset 0 1px 0 rgba(255,255,255,0.04) !important;
}
div[data-testid="stMetric"] label {
    color: var(--text-muted) !important;
    font-family: var(--font-mono) !important;
    font-size: 11px !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: var(--accent) !important;
    font-family: var(--font-head) !important;
    font-size: 32px !important;
    font-weight: 700 !important;
}

/* ── DataFrames ── */
div[data-testid="stDataFrame"] {
    border: 1px solid var(--border-glow) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--accent2); border-radius: 2px; }

/* ── Page title animation ── */
@keyframes glow-pulse {
    0%, 100% { text-shadow: 0 0 20px rgba(0,245,196,0.4), 0 0 40px rgba(0,245,196,0.2); }
    50%       { text-shadow: 0 0 30px rgba(0,245,196,0.7), 0 0 60px rgba(0,245,196,0.35); }
}
.page-title {
    font-family: var(--font-head) !important;
    font-size: 42px !important;
    font-weight: 700 !important;
    color: var(--accent) !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    animation: glow-pulse 3s ease-in-out infinite !important;
    margin-bottom: 4px !important;
}
.page-sub {
    font-family: var(--font-mono);
    font-size: 12px;
    color: var(--text-muted);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 32px;
}
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--accent), transparent);
    margin: 24px 0;
    opacity: 0.4;
}
.section-label {
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--accent);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 12px;
    opacity: 0.8;
}
.stat-card {
    background: var(--bg-card);
    border: 1px solid var(--border-glow);
    border-radius: 12px;
    padding: 20px 24px;
    box-shadow: 0 0 30px rgba(0,245,196,0.05);
    position: relative;
    overflow: hidden;
}
.stat-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent), transparent);
}
.stat-num {
    font-family: var(--font-head);
    font-size: 36px;
    font-weight: 700;
    color: var(--accent);
}
.stat-lbl {
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--text-muted);
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-top: 4px;
}
.insight-card {
    background: var(--bg-card);
    border: 1px solid var(--border-glow);
    border-left: 3px solid var(--accent);
    border-radius: 10px;
    padding: 18px 22px;
    margin: 10px 0;
    font-family: var(--font-body);
    color: var(--text-primary);
    font-size: 15px;
}
.logo-text {
    font-family: var(--font-head);
    font-size: 26px;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: 4px;
    text-transform: uppercase;
}
.logo-sub {
    font-family: var(--font-mono);
    font-size: 9px;
    color: var(--text-muted);
    letter-spacing: 3px;
    text-transform: uppercase;
}
.login-box {
    background: linear-gradient(135deg, #06091a, #0d0f1f);
    border: 1px solid var(--border-glow);
    border-radius: 16px;
    padding: 48px 40px;
    box-shadow: 0 0 80px rgba(0,245,196,0.1), 0 0 160px rgba(124,58,237,0.08);
    max-width: 420px;
    margin: 0 auto;
}
</style>
""", unsafe_allow_html=True)

# ─── CHART THEME ──────────────────────────────────────────────────────────────
CHART_COLORS = ["#00f5c4","#7c3aed","#f59e0b","#ef4444","#3b82f6","#10b981","#f97316","#8b5cf6","#06b6d4","#ec4899"]

def style_chart(fig, title=""):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(8,12,24,0.6)",
        font=dict(family="Exo 2, sans-serif", color="#94a3b8", size=12),
        title=dict(text=title, font=dict(family="Rajdhani, sans-serif", size=20, color="#00f5c4"), x=0.02, y=0.97),
        margin=dict(l=16, r=16, t=50, b=16),
        colorway=CHART_COLORS,
        legend=dict(
            bgcolor="rgba(8,12,24,0.8)",
            bordercolor="rgba(0,245,196,0.2)",
            borderwidth=1,
            font=dict(family="Share Tech Mono, monospace", size=11, color="#94a3b8")
        ),
        xaxis=dict(
            gridcolor="rgba(255,255,255,0.04)",
            linecolor="rgba(0,245,196,0.2)",
            tickfont=dict(family="Share Tech Mono, monospace", size=10, color="#64748b"),
        ),
        yaxis=dict(
            gridcolor="rgba(255,255,255,0.04)",
            linecolor="rgba(0,245,196,0.2)",
            tickfont=dict(family="Share Tech Mono, monospace", size=10, color="#64748b"),
        ),
        hoverlabel=dict(
            bgcolor="#080c18",
            bordercolor="#00f5c4",
            font=dict(family="Share Tech Mono, monospace", size=12, color="#e2e8f0")
        ),
        transition_duration=400,
    )
    return fig

def bar_chart(df, x, y, title, color_col=None, orientation='v'):
    if orientation == 'h':
        fig = px.bar(df, x=y, y=x, orientation='h',
                     color=x if color_col is None else color_col,
                     color_discrete_sequence=CHART_COLORS,
                     text=y)
        fig.update_traces(texttemplate='<b>%{text:.2s}</b>', textposition='outside',
                          textfont=dict(family="Share Tech Mono, monospace", size=11, color="#e2e8f0"),
                          marker=dict(line=dict(width=0)),
                          hovertemplate=f"<b>%{{y}}</b><br>{y}: %{{x:.2f}}M<extra></extra>")
    else:
        fig = px.bar(df, x=x, y=y,
                     color=x if color_col is None else color_col,
                     color_discrete_sequence=CHART_COLORS,
                     text=y)
        fig.update_traces(texttemplate='<b>%{text:.2s}</b>', textposition='outside',
                          textfont=dict(family="Share Tech Mono, monospace", size=11, color="#e2e8f0"),
                          marker=dict(line=dict(width=0)),
                          hovertemplate=f"<b>%{{x}}</b><br>{y}: %{{y:.2f}}M<extra></extra>")
    return style_chart(fig, title)

def line_chart(df, x, y, title):
    fig = px.line(df, x=x, y=y, color_discrete_sequence=["#00f5c4"])
    fig.update_traces(
        line=dict(width=2.5, color="#00f5c4"),
        mode='lines+markers',
        marker=dict(size=5, color="#00f5c4", line=dict(width=1.5, color="#03040a")),
        fill='tozeroy',
        fillcolor='rgba(0,245,196,0.06)',
        hovertemplate=f"<b>%{{x}}</b><br>{y}: %{{y:.2f}}M<extra></extra>"
    )
    return style_chart(fig, title)

def pie_chart(df, names, values, title):
    fig = px.pie(df, names=names, values=values,
                 color_discrete_sequence=CHART_COLORS,
                 hole=0.5)
    fig.update_traces(
        textfont=dict(family="Share Tech Mono, monospace", size=11, color="#e2e8f0"),
        hovertemplate="<b>%{label}</b><br>Sales: %{value:.2f}M<br>Share: %{percent}<extra></extra>",
        marker=dict(line=dict(color="#03040a", width=2))
    )
    fig.update_layout(
        annotations=[dict(text=title.split()[-1], x=0.5, y=0.5, font=dict(
            family="Rajdhani, sans-serif", size=16, color="#00f5c4"), showarrow=False)]
    )
    return style_chart(fig, title)

def scatter_chart(df, x, y, title):
    fig = px.scatter(df, x=x, y=y,
                     color=y,
                     color_continuous_scale=["#7c3aed","#00f5c4","#f59e0b"],
                     size_max=12)
    fig.update_traces(
        marker=dict(size=6, line=dict(width=0)),
        hovertemplate=f"<b>%{{x}}</b><br>{y}: %{{y:.2f}}M<extra></extra>"
    )
    return style_chart(fig, title)

def box_chart(df, x, y, title):
    fig = px.box(df, x=x, y=y, color=x,
                 color_discrete_sequence=CHART_COLORS,
                 notched=True)
    fig.update_traces(
        hovertemplate=f"<b>%{{x}}</b><br>{y}: %{{y:.2f}}M<extra></extra>",
        marker=dict(size=4, opacity=0.5)
    )
    return style_chart(fig, title)

def hist_chart(df, x, title):
    fig = px.histogram(df, x=x, nbins=40,
                       color_discrete_sequence=["#7c3aed"])
    fig.update_traces(
        marker=dict(line=dict(width=0.5, color="#03040a")),
        hovertemplate=f"{x}: %{{x:.2f}}<br>Count: %{{y}}<extra></extra>"
    )
    return style_chart(fig, title)

# ─── SESSION ──────────────────────────────────────────────────────────────────
if "auth" not in st.session_state:
    st.session_state.auth = False

# ─── LOGIN ────────────────────────────────────────────────────────────────────
if not st.session_state.auth:
    st.markdown("""
    <style>
    .stApp { background: radial-gradient(ellipse at 30% 40%, rgba(124,58,237,0.12) 0%, #03040a 60%), radial-gradient(ellipse at 70% 70%, rgba(0,245,196,0.08) 0%, transparent 50%) !important; }
    </style>
    """, unsafe_allow_html=True)

    col_l, col_c, col_r = st.columns([1, 1.2, 1])
    with col_c:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div class='login-box'>
            <div style='text-align:center; margin-bottom:32px;'>
                <div class='logo-text'>NEXUS</div>
                <div class='logo-sub'>Game Intelligence Platform</div>
                <div style='margin-top:16px; font-family:var(--font-mono); font-size:11px; color:rgba(0,245,196,0.5); letter-spacing:2px;'>── SECURE ACCESS ──</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            user = st.text_input("USERNAME", placeholder="Enter username")
            pwd  = st.text_input("PASSWORD", type="password", placeholder="••••••••")
            submitted = st.form_submit_button("INITIATE SESSION →", use_container_width=True)

            if submitted:
                if user == "admin" and pwd == "1234":
                    st.session_state.auth = True
                    st.rerun()
                else:
                    st.error("ACCESS DENIED — Invalid credentials")
    st.stop()

# ─── DATA ─────────────────────────────────────────────────────────────────────
@st.cache_data
def load():
    g = pd.read_csv("data/games.csv")
    s = pd.read_csv("data/vgsales.csv")
    return g, s

games, sales = load()

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 20px 8px 24px;'>
        <div class='logo-text'>NEXUS</div>
        <div class='logo-sub'>Game Analytics</div>
        <div style='margin-top:12px; height:1px; background:linear-gradient(90deg,transparent,rgba(0,245,196,0.4),transparent);'></div>
    </div>
    """, unsafe_allow_html=True)

    menu = st.radio("", [
        "📌  Overview",
        "📊  Dashboard",
        "💰  Sales",
        "🎮  Engagement",
        "🧠  Insights",
        "📈  ML Forecast",
        "🧮  SQL Analysis",
    ], label_visibility="collapsed")

    st.markdown("""
    <div style='position:absolute; bottom:24px; left:16px; right:16px;'>
        <div style='font-family:var(--font-mono); font-size:9px; color:rgba(100,116,139,0.6); letter-spacing:1px; text-align:center; text-transform:uppercase;'>
            NEXUS v2.0 · NEXUS Corp 2025
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def page_header(title, subtitle=""):
    st.markdown(f"""
    <div class='page-title'>{title}</div>
    <div class='page-sub'>{subtitle}</div>
    <div class='divider'></div>
    """, unsafe_allow_html=True)

def chart_card(fig):
    st.markdown('<div style="background:var(--bg-card);border:1px solid var(--border-glow);border-radius:14px;padding:8px;box-shadow:0 0 30px rgba(0,245,196,0.04);">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

def filter_row(key_prefix):
    c1, c2, c3 = st.columns(3)
    genre    = c1.selectbox("GENRE",    ["All"] + sorted(sales["Genre"].dropna().unique().tolist()),    key=f"{key_prefix}_g")
    platform = c2.selectbox("PLATFORM", ["All"] + sorted(sales["Platform"].dropna().unique().tolist()), key=f"{key_prefix}_p")
    year_opt = [str(int(y)) for y in sorted(sales["Year"].dropna().unique())]
    year     = c3.selectbox("YEAR",     ["All"] + year_opt, key=f"{key_prefix}_y")
    df = sales.copy()
    if genre    != "All": df = df[df["Genre"] == genre]
    if platform != "All": df = df[df["Platform"] == platform]
    if year     != "All": df = df[df["Year"] == float(year)]
    return df

# ═══════════════════════════════════════════════════════════════════════════════
# OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
if "Overview" in menu:
    page_header("NEXUS ANALYTICS", "Video Game Intelligence Platform · Global Sales Data")

    c1, c2, c3, c4 = st.columns(4)
    total_sales  = sales["Global_Sales"].sum()
    total_games  = len(sales)
    top_platform = sales.groupby("Platform")["Global_Sales"].sum().idxmax()
    top_genre    = sales.groupby("Genre")["Global_Sales"].sum().idxmax()

    c1.metric("GLOBAL SALES", f"{total_sales:.0f}M")
    c2.metric("TITLES TRACKED", f"{total_games:,}")
    c3.metric("LEADING PLATFORM", top_platform)
    c4.metric("TOP GENRE", top_genre)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='section-label'>Platform Overview</div>", unsafe_allow_html=True)
        df_plat = sales.groupby("Platform")["Global_Sales"].sum().reset_index().sort_values("Global_Sales", ascending=False).head(12)
        chart_card(bar_chart(df_plat, "Platform", "Global_Sales", "Sales by Platform (Top 12)"))

    with col2:
        st.markdown("<div class='section-label'>Yearly Trend</div>", unsafe_allow_html=True)
        df_yr = sales.groupby("Year")["Global_Sales"].sum().reset_index().dropna()
        chart_card(line_chart(df_yr, "Year", "Global_Sales", "Global Sales Trend by Year"))

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class='insight-card'>🎯 &nbsp; This platform analyzes <b>16,500+</b> video game titles spanning 40+ years of industry data — covering platform sales, regional performance, publisher rankings, and genre trends.</div>
    <div class='insight-card'>📡 &nbsp; Built with Streamlit · Plotly · scikit-learn · SQLite — a full-stack analytics suite designed for game industry intelligence.</div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
elif "Dashboard" in menu:
    page_header("DASHBOARD", "Multi-dimensional sales analytics with live filters")

    st.markdown("<div class='section-label'>Active Filters</div>", unsafe_allow_html=True)
    df = filter_row("dash")

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("FILTERED SALES", f"{df['Global_Sales'].sum():.1f}M")
    c2.metric("TITLES", f"{len(df):,}")
    c3.metric("PUBLISHERS", f"{df['Publisher'].nunique():,}")

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    charts = [
        bar_chart(df.groupby("Platform")["Global_Sales"].sum().reset_index().sort_values("Global_Sales",ascending=False).head(12), "Platform","Global_Sales","Sales by Platform"),
        bar_chart(df.groupby("Genre")["Global_Sales"].sum().reset_index().sort_values("Global_Sales",ascending=False), "Genre","Global_Sales","Sales by Genre"),
        line_chart(df.dropna(subset=["Year"]).groupby("Year")["Global_Sales"].sum().reset_index(), "Year","Global_Sales","Yearly Sales Trend"),
        pie_chart(df, "Genre","Global_Sales","Genre Distribution"),
        box_chart(df,"Genre","Global_Sales","Sales Spread by Genre"),
        hist_chart(df,"Global_Sales","Sales Distribution"),
        scatter_chart(df,"Year","Global_Sales","Year vs Sales"),
        bar_chart(df.groupby("Publisher")["Global_Sales"].sum().reset_index().sort_values("Global_Sales",ascending=False).head(10), "Publisher","Global_Sales","Top 10 Publishers", orientation='h'),
        bar_chart(df.groupby("Platform")["NA_Sales"].sum().reset_index().sort_values("NA_Sales",ascending=False).head(10), "Platform","NA_Sales","North America Sales"),
        bar_chart(df.groupby("Platform")["EU_Sales"].sum().reset_index().sort_values("EU_Sales",ascending=False).head(10), "Platform","EU_Sales","Europe Sales"),
    ]

    for i, fig in enumerate(charts):
        with col1 if i % 2 == 0 else col2:
            chart_card(fig)
            st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SALES
# ═══════════════════════════════════════════════════════════════════════════════
elif "Sales" in menu:
    page_header("SALES INTELLIGENCE", "Regional and global revenue breakdown")

    df = filter_row("sales")
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("GLOBAL",        f"{df['Global_Sales'].sum():.1f}M")
    c2.metric("NORTH AMERICA", f"{df['NA_Sales'].sum():.1f}M")
    c3.metric("EUROPE",        f"{df['EU_Sales'].sum():.1f}M")
    c4.metric("JAPAN",         f"{df['JP_Sales'].sum():.1f}M")

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    # Regional comparison radar
    region_df = pd.DataFrame({
        "Region": ["NA Sales", "EU Sales", "JP Sales", "Other Sales", "Global"],
        "Sales": [
            df["NA_Sales"].sum(), df["EU_Sales"].sum(),
            df["JP_Sales"].sum(), df["Other_Sales"].sum(),
            df["Global_Sales"].sum()
        ]
    })
    fig_radar = go.Figure(go.Scatterpolar(
        r=region_df["Sales"].values,
        theta=region_df["Region"].values,
        fill='toself',
        fillcolor='rgba(0,245,196,0.08)',
        line=dict(color="#00f5c4", width=2),
        marker=dict(color="#00f5c4", size=8)
    ))
    fig_radar = style_chart(fig_radar, "Regional Sales Radar")
    fig_radar.update_layout(polar=dict(
        bgcolor="rgba(8,12,24,0.6)",
        angularaxis=dict(color="#64748b", gridcolor="rgba(255,255,255,0.06)"),
        radialaxis=dict(color="#64748b", gridcolor="rgba(255,255,255,0.06)")
    ))

    charts_sales = [
        bar_chart(df.groupby("Platform")["Global_Sales"].sum().reset_index().sort_values("Global_Sales",ascending=False).head(12), "Platform","Global_Sales","Global Sales by Platform"),
        pie_chart(df, "Genre","Global_Sales","Genre Share"),
        box_chart(df,"Genre","Global_Sales","Genre Sales Spread"),
        hist_chart(df,"Global_Sales","Sales Distribution"),
        scatter_chart(df,"Year","Global_Sales","Sales Over Time"),
        bar_chart(df.groupby("Platform")["NA_Sales"].sum().reset_index().sort_values("NA_Sales",ascending=False).head(10),"Platform","NA_Sales","North America"),
        bar_chart(df.groupby("Platform")["EU_Sales"].sum().reset_index().sort_values("EU_Sales",ascending=False).head(10),"Platform","EU_Sales","Europe"),
        bar_chart(df.groupby("Platform")["JP_Sales"].sum().reset_index().sort_values("JP_Sales",ascending=False).head(10),"Platform","JP_Sales","Japan"),
        bar_chart(df.groupby("Platform")["Other_Sales"].sum().reset_index().sort_values("Other_Sales",ascending=False).head(10),"Platform","Other_Sales","Other Regions"),
        line_chart(df.dropna(subset=["Year"]).groupby("Year")["Global_Sales"].sum().reset_index(),"Year","Global_Sales","Yearly Trend"),
    ]

    with col1:
        chart_card(fig_radar)
        st.markdown("<br>", unsafe_allow_html=True)
    with col2:
        chart_card(charts_sales[0])
        st.markdown("<br>", unsafe_allow_html=True)

    for i, fig in enumerate(charts_sales[1:]):
        with col1 if i % 2 == 0 else col2:
            chart_card(fig)
            st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# ENGAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════
elif "Engagement" in menu:
    page_header("ENGAGEMENT", "Top performing titles by global sales volume")

    top_n = st.slider("Show Top N Games", 5, 30, 15)

    top_games = (
        sales.groupby("Name")["Global_Sales"].sum()
        .reset_index()
        .sort_values("Global_Sales", ascending=True)
        .tail(top_n)
    )

    fig = px.bar(top_games, x="Global_Sales", y="Name", orientation='h',
                 color="Global_Sales", color_continuous_scale=["#7c3aed","#00f5c4","#f59e0b"],
                 text="Global_Sales")
    fig.update_traces(
        texttemplate='<b>%{text:.2f}M</b>', textposition='outside',
        textfont=dict(family="Share Tech Mono, monospace", size=11, color="#e2e8f0"),
        marker=dict(line=dict(width=0)),
        hovertemplate="<b>%{y}</b><br>Sales: %{x:.2f}M<extra></extra>"
    )
    fig = style_chart(fig, f"Top {top_n} Games by Global Sales")
    fig.update_layout(height=max(400, top_n * 32), coloraxis_showscale=False, yaxis=dict(tickfont=dict(size=11)))

    chart_card(fig)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>Publisher Engagement</div>", unsafe_allow_html=True)

    pub_df = sales.groupby("Publisher").agg(
        Total_Sales=("Global_Sales","sum"),
        Titles=("Name","count")
    ).reset_index().sort_values("Total_Sales",ascending=False).head(20)

    fig2 = px.scatter(pub_df, x="Titles", y="Total_Sales", size="Total_Sales",
                      color="Total_Sales", text="Publisher",
                      color_continuous_scale=["#7c3aed","#00f5c4"],
                      size_max=50)
    fig2.update_traces(
        textposition='top center',
        textfont=dict(family="Share Tech Mono, monospace", size=9, color="#94a3b8"),
        hovertemplate="<b>%{text}</b><br>Titles: %{x}<br>Sales: %{y:.1f}M<extra></extra>"
    )
    fig2 = style_chart(fig2, "Publisher — Titles vs Revenue")
    fig2.update_layout(coloraxis_showscale=False)
    chart_card(fig2)

# ═══════════════════════════════════════════════════════════════════════════════
# INSIGHTS
# ═══════════════════════════════════════════════════════════════════════════════
elif "Insights" in menu:
    page_header("INSIGHTS", "Key findings from the global gaming dataset")

    insights = [
        ("🎯", "Action & Sports dominate", f"Action games account for {sales[sales['Genre']=='Action']['Global_Sales'].sum():.0f}M units — the highest of any genre globally."),
        ("📈", "Peak era: 2005–2012", "The gaming industry hit peak revenue between 2005 and 2012, driven by PS3, Xbox 360 and Wii adoption."),
        ("🎮", "PS2 is the GOAT platform", f"PS2 leads all platforms with {sales[sales['Platform']=='PS2']['Global_Sales'].sum():.0f}M units sold globally."),
        ("🌎", "North America leads revenue", f"NA contributes {sales['NA_Sales'].sum()/sales['Global_Sales'].sum()*100:.1f}% of global revenue — the single largest market."),
        ("🏆", "Nintendo dominates Japan", f"JP_Sales total {sales['JP_Sales'].sum():.0f}M — with Nintendo titles consistently topping charts."),
        ("📦", "Publisher concentration", f"Top 10 publishers control {sales.groupby('Publisher')['Global_Sales'].sum().sort_values(ascending=False).head(10).sum()/sales['Global_Sales'].sum()*100:.0f}% of total sales."),
    ]

    for icon, title, body in insights:
        st.markdown(f"""
        <div class='insight-card'>
            <div style='font-family:var(--font-head); font-size:16px; color:var(--accent); font-weight:600; margin-bottom:6px;'>{icon} &nbsp; {title}</div>
            <div style='font-family:var(--font-body); font-size:14px; color:var(--text-muted); line-height:1.6;'>{body}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='section-label'>Genre Leaders</div>", unsafe_allow_html=True)
        g_df = sales.groupby("Genre")["Global_Sales"].sum().reset_index().sort_values("Global_Sales", ascending=False)
        chart_card(bar_chart(g_df, "Genre", "Global_Sales", "Genre Total Sales", orientation='v'))
    with col2:
        st.markdown("<div class='section-label'>Top Publishers</div>", unsafe_allow_html=True)
        p_df = sales.groupby("Publisher")["Global_Sales"].sum().reset_index().sort_values("Global_Sales", ascending=False).head(12)
        chart_card(bar_chart(p_df, "Publisher", "Global_Sales", "Top Publisher Revenue", orientation='h'))

# ═══════════════════════════════════════════════════════════════════════════════
# ML FORECAST
# ═══════════════════════════════════════════════════════════════════════════════
elif "ML Forecast" in menu:
    page_header("ML FORECAST", "Linear regression model — global sales projection")

    df_ml = sales.dropna(subset=["Year"]).groupby("Year")["Global_Sales"].sum().reset_index()
    df_ml["Year"] = df_ml["Year"].astype(int)

    X = df_ml[["Year"]]
    y = df_ml["Global_Sales"]
    model = LinearRegression()
    model.fit(X, y)
    r2 = model.score(X, y)

    last_year    = int(df_ml["Year"].max())
    future_years = pd.DataFrame({"Year": list(range(last_year + 1, last_year + 6))})
    preds        = model.predict(future_years)

    c1, c2, c3 = st.columns(3)
    c1.metric("MODEL TYPE",   "Linear Regression")
    c2.metric("R² SCORE",     f"{r2:.3f}")
    c3.metric("FORECAST YRS", "5 years")

    st.markdown("<br>", unsafe_allow_html=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_ml["Year"], y=df_ml["Global_Sales"],
        mode='lines+markers', name='Historical',
        line=dict(color="#00f5c4", width=2.5),
        marker=dict(size=6, color="#00f5c4"),
        fill='tozeroy', fillcolor='rgba(0,245,196,0.05)',
        hovertemplate="<b>%{x}</b><br>Sales: %{y:.2f}M<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=list(future_years["Year"]), y=list(preds),
        mode='lines+markers', name='Forecast',
        line=dict(color="#f59e0b", width=2.5, dash='dot'),
        marker=dict(size=8, color="#f59e0b", symbol='diamond'),
        hovertemplate="<b>%{x} (Forecast)</b><br>Sales: %{y:.2f}M<extra></extra>"
    ))
    # Confidence band
    fig.add_trace(go.Scatter(
        x=list(future_years["Year"]) + list(future_years["Year"])[::-1],
        y=list(preds * 1.1) + list(preds * 0.9)[::-1],
        fill='toself', fillcolor='rgba(245,158,11,0.06)',
        line=dict(color='rgba(0,0,0,0)'), showlegend=False,
        hoverinfo='skip', name='Confidence Band'
    ))
    fig = style_chart(fig, "Global Sales Forecast — 5 Year Projection")
    fig.update_layout(height=480, legend=dict(orientation="h", y=1.05))
    chart_card(fig)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>Forecast Values</div>", unsafe_allow_html=True)

    forecast_df = pd.DataFrame({
        "Year": future_years["Year"].values,
        "Projected Sales (M)": [f"{p:.2f}" for p in preds],
        "vs Last Known": [f"{((p - df_ml['Global_Sales'].iloc[-1]) / df_ml['Global_Sales'].iloc[-1] * 100):+.1f}%" for p in preds]
    })
    st.dataframe(forecast_df, use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SQL ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════
elif "SQL" in menu:
    page_header("SQL ANALYSIS", "Live query engine — 15 analytical queries")

    conn = sqlite3.connect(":memory:")
    games.to_sql("games",  conn, if_exists="replace", index=False)
    sales.to_sql("vgsales", conn, if_exists="replace", index=False)

    QUERIES = {
        "01 · Games table sample":                  "SELECT * FROM games LIMIT 10",
        "02 · VGSales table sample":                "SELECT * FROM vgsales LIMIT 10",
        "03 · Revenue by Genre":                    "SELECT Genre, ROUND(SUM(Global_Sales),2) AS Global_Sales FROM vgsales GROUP BY Genre ORDER BY Global_Sales DESC",
        "04 · Revenue by Platform":                 "SELECT Platform, ROUND(SUM(Global_Sales),2) AS Global_Sales FROM vgsales GROUP BY Platform ORDER BY Global_Sales DESC",
        "05 · Revenue by Publisher":                "SELECT Publisher, ROUND(SUM(Global_Sales),2) AS Global_Sales FROM vgsales GROUP BY Publisher ORDER BY Global_Sales DESC LIMIT 20",
        "06 · Annual Sales Trend":                  "SELECT Year, ROUND(SUM(Global_Sales),2) AS Global_Sales FROM vgsales WHERE Year IS NOT NULL GROUP BY Year ORDER BY Year",
        "07 · Top 10 Best-Selling Titles":          "SELECT Name, ROUND(Global_Sales,2) AS Global_Sales FROM vgsales ORDER BY Global_Sales DESC LIMIT 10",
        "08 · Avg Sales by Genre":                  "SELECT Genre, ROUND(AVG(Global_Sales),3) AS Avg_Sales FROM vgsales GROUP BY Genre ORDER BY Avg_Sales DESC",
        "09 · Avg Sales by Platform":               "SELECT Platform, ROUND(AVG(Global_Sales),3) AS Avg_Sales FROM vgsales GROUP BY Platform ORDER BY Avg_Sales DESC",
        "10 · Total title count":                   "SELECT COUNT(*) AS Total_Titles FROM vgsales",
        "11 · Title count by Genre":                "SELECT Genre, COUNT(*) AS Titles FROM vgsales GROUP BY Genre ORDER BY Titles DESC",
        "12 · Title count by Platform":             "SELECT Platform, COUNT(*) AS Titles FROM vgsales GROUP BY Platform ORDER BY Titles DESC",
        "13 · Title count by Year":                 "SELECT Year, COUNT(*) AS Titles FROM vgsales WHERE Year IS NOT NULL GROUP BY Year ORDER BY Year",
        "14 · Title count by Publisher":            "SELECT Publisher, COUNT(*) AS Titles FROM vgsales GROUP BY Publisher ORDER BY Titles DESC LIMIT 20",
        "15 · Genre × Platform cross sales":        "SELECT Genre, Platform, ROUND(SUM(Global_Sales),2) AS Global_Sales FROM vgsales GROUP BY Genre, Platform ORDER BY Global_Sales DESC LIMIT 30",
    }

    selected = st.selectbox("SELECT QUERY", list(QUERIES.keys()))
    sql_text = QUERIES[selected]

    st.markdown(f"""
    <div style='background:var(--bg-card);border:1px solid var(--border-glow);border-radius:10px;padding:14px 18px;margin:12px 0 16px;'>
        <div style='font-family:var(--font-mono);font-size:12px;color:var(--accent);letter-spacing:0.5px;line-height:1.6;'>{sql_text}</div>
    </div>
    """, unsafe_allow_html=True)

    df_sql = pd.read_sql(sql_text, conn)
    st.dataframe(df_sql, use_container_width=True, hide_index=True)

    # Auto chart if numeric col exists
    num_cols = df_sql.select_dtypes(include="number").columns.tolist()
    str_cols = df_sql.select_dtypes(exclude="number").columns.tolist()
    if num_cols and str_cols and len(df_sql) > 1:
        st.markdown("<br>", unsafe_allow_html=True)
        fig_sql = px.bar(df_sql.head(20), x=str_cols[0], y=num_cols[0],
                         color=num_cols[0], color_continuous_scale=["#7c3aed","#00f5c4"],
                         text=num_cols[0])
        fig_sql.update_traces(
            texttemplate='<b>%{text:.2s}</b>', textposition='outside',
            textfont=dict(family="Share Tech Mono, monospace", size=10),
            marker=dict(line=dict(width=0)),
        )
        fig_sql = style_chart(fig_sql, f"{str_cols[0]} vs {num_cols[0]}")
        fig_sql.update_layout(coloraxis_showscale=False)
        chart_card(fig_sql)

    conn.close()
