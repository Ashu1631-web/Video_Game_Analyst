import streamlit as st
import os

st.set_page_config(page_title="Enterprise Gaming Analytics", layout="wide")

st.title("🎮 Enterprise Gaming Analytics Platform")

if not os.path.exists("data/games.csv"):
    st.error("games.csv not found in data folder")
    st.stop()

if not os.path.exists("data/vgsales.csv"):
    st.error("vgsales.csv not found in data folder")
    st.stop()

st.success("Data files detected successfully.")
