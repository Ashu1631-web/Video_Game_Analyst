import streamlit as st
import os

st.set_page_config(page_title="Enterprise Gaming Analytics", layout="wide")

st.title("🎮 Enterprise Gaming Analytics Platform")

# Safety check for data
if not os.path.exists("data/games.csv"):
    st.error("❌ games.csv not found in data folder")
    st.stop()

if not os.path.exists("data/vgsales.csv"):
    st.error("❌ vgsales.csv not found in data folder")
    st.stop()

st.success("✅ Data files loaded successfully")

# Show SQL file
if os.path.exists("sql/schema.sql"):
    with st.expander("📄 View SQL Schema"):
        with open("sql/schema.sql", "r") as f:
            st.code(f.read(), language="sql")
