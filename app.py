import streamlit as st

from ui.dashboard import show_dashboard

st.set_page_config(
    page_title="RecruitRankAI",
    page_icon="RR",
    layout="wide",
    initial_sidebar_state="expanded",
)

show_dashboard()
