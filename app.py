import streamlit as st
import os

st.set_page_config(page_title="Enterprise Gaming Analytics", layout="wide")

st.title("🎮 Enterprise Gaming Intelligence Platform")

st.markdown("""
Welcome to the Enterprise Gaming Analytics System.

Modules:
- 📊 Interactive Dashboard
- 🤖 ML Sales Prediction
- 🎯 Recommendation Engine
""")

if not os.path.exists("data/games.csv"):
    st.error("games.csv missing")
    st.stop()

if not os.path.exists("data/vgsales.csv"):
    st.error("vgsales.csv missing")
    st.stop()

st.success("System Ready")

with st.expander("View SQL Schema"):
    if os.path.exists("sql/schema.sql"):
        with open("sql/schema.sql", "r") as f:
            st.code(f.read(), language="sql")
