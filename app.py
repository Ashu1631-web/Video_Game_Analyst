import streamlit as st
import os

st.set_page_config(page_title="Enterprise Gaming Analytics", layout="wide")

st.title("🎮 Enterprise Gaming Analytics Platform")

st.markdown("""
### Modules:
- Dashboard
- ML Prediction
- Forecasting
- Recommendation
""")

# Show SQL file content
if os.path.exists("sql/schema.sql"):
    with st.expander("View SQL Schema"):
        with open("sql/schema.sql", "r") as f:
            st.code(f.read(), language="sql")
