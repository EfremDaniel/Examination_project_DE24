import streamlit as st
from pathlib import Path


st.markdown(
    """
    <style>
    /* ===== SIDEBAR ===== */
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div {
        background-color: #0F3D2E;
    }

    section[data-testid="stSidebar"] * {
        color: #E8FFF6;
    }
    </style>
    """,
    unsafe_allow_html=True
)



# st.set_page_config(
#     page_title="Laddinfrastruktur i Sverige",
#     page_icon="🔌",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# =========================
# SIDEBAR – ORIENTERING
# =========================

with st.sidebar:
    st.markdown("## 🔌 Laddinfrastruktur i Sverige")

    st.markdown(
        """
        Dashboarden ger en samlad analys av hur den publika laddinfrastrukturen är utbyggd och
        hur dess omfattning varierar mellan olika områden.

        Den visualiserar antal laddstationer, fördelningen mellan snabbladdning och 
        normalladdning samt genomsnittligt antal laddpunkter per station.
        """
    )

    st.divider()

    st.caption("Dashboard för analys och planering")

# =========================
# HERO
# =========================

st.title("Laddinfrastruktur i Sverige")
st.caption("Överblick av publik laddning i ett elektrifierat samhälle")
st.divider()

# =========================
# INTRO
# =========================

st.markdown(
    """
    **En samlad vy över Sveriges publika laddare omkring Sverige.**
    """
)
BASE_DIR = Path(__file__).resolve().parents[2]
ASSETS_DIR = BASE_DIR / "backend" / "assets"

# =========================
# HERO IMAGES – BREDVID VARANDRA
# =========================

img_col1, img_col2 = st.columns(
    [1, 1],
    gap="small"   # <-- VIKTIGT: minimerar avstånd
)

with img_col1:
    st.image(
        str(ASSETS_DIR / "hero_urban_charging_evening.png"),
        use_container_width=True
    )

with img_col2:
    st.image(
        str(ASSETS_DIR / "urban_charging_row_city.png"),
        use_container_width=True
    )



# =========================
# SEKTION: ÖVERSIKT
# =========================

col1, col2 = st.columns(2, gap="large")

with col1:
    with st.container(border=True):
        st.subheader("Helhetsbild")
        st.write(
            "Nationell översikt av laddinfrastrukturens omfattning, "
            "fördelning och kapacitet."
        )

with col2:
    with st.container(border=True):
        st.subheader("Regionala skillnader")
        st.write(
            "Tillgången till laddning varierar mellan län och kommuner "
            "beroende på lokala förutsättningar."
        )


# =========================
# SEKTION: VAD KAN DU ANALYSERA
# =========================

c1, c2, c3 = st.columns(3, gap="large")

with c1:
    with st.container(border=True):
        st.subheader("Elbilsutveckling")
        st.write("Antalet elbilar ökar snabbt i hela landet.")

with c2:
    with st.container(border=True):
        st.subheader("Laddtyper")
        st.write("Snabbladdning och normalladdning fyller olika behov.")

with c3:
    with st.container(border=True):
        st.subheader("EU:s rekommendation")
        st.write("Hur länens infrastruktur följer EU:s riktmärke")

st.divider()

# =========================
# CTA – STARTA ANALYS
# =========================


cta_col1, cta_col2, cta_col3 = st.columns([1, 2, 1])

with cta_col2:
    with st.container(border=True):
        st.write(
            """
            Gå vidare till **Charger analysis** för att analysera
            laddstationer, laddpunkter och kapacitet per län
            och kommun.
            """
        )

        if st.button(
            "▶ Öppna analysverktyget",
            use_container_width=True,
            type="primary"
        ):
            st.switch_page("src/frontend/dashboard/charger_analys_page.py")


