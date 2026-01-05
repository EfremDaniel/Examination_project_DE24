import streamlit as st


st.set_page_config(
    page_title="Dashboard",
    page_icon="🔌",
    layout="wide",
    initial_sidebar_state="expanded",
)


pages = [
    st.Page("src/frontend/dashboard/home_page.py", title="Laddinfrastruktur i Sverige", icon="🔌"),
    st.Page("src/frontend/dashboard/charger_analys_page.py", title="Charger analysis", icon="⚡"),
]


pg = st.navigation(pages)

pg.run()

