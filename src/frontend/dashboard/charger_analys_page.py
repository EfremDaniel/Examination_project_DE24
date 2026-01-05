import streamlit as st
from backend.data_processing import query_analytics
from frontend.graph.chart_utils import (
    laddstationer_typ_per_kommun_stacked,
    elbil_per_laddpunkt
)


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

# =========================
# PAGE CONFIG
# =========================

# st.set_page_config(
#     page_title="Charger analysis",
#     page_icon="⚡",
#     layout="wide"
# )

# =========================
# HEADER
# =========================

st.title("⚡ Charger analysis")

st.markdown(
    """
    **Interaktiv analys av Sveriges publika laddinfrastruktur.**  
    Analysen visar hur kommunerna inom ett län bidrar till både
    omfattning och typ av laddkapacitet.
    """
)

st.divider()

# =========================
# DATA
# =========================

df_nr_charger = query_analytics("nr_charger")

# =========================
# CONTROL PANEL
# =========================

with st.container(border=True):
    st.markdown("### 🔧 Kontrollpanel")

    county_options = ["Välj län"] + sorted(df_nr_charger["COUNTY"].unique())

    county = st.selectbox(
        "Län",
        options=county_options,
        index=0,
        help="Välj ett län för att visa statistik per kommun."
    )

st.divider()

# =========================
# RESULTS
# =========================

if county != "Välj län":

    st.subheader(f"📊 Sammanfattning – {county}")

    df_nr_charger_county = df_nr_charger[df_nr_charger["COUNTY"] == county]

    col1, col2, col3 = st.columns(3)

    with col1:
        total_stationer = df_nr_charger_county["ANTAL_LADD_STATIONER"].sum()
        st.metric("Antal laddstationer", int(total_stationer))

    with col2:
        laddpunkter = df_nr_charger_county["LADDPUNKTER"].sum()
        st.metric("Antal laddpunkter", int(laddpunkter))

    with col3:
        fast = df_nr_charger_county["ANTAL_SNABB_LADD_STATIONER"].sum()
        st.metric(
            "Andel snabbladdare",
            f"{round((fast / total_stationer) * 100, 1)} %"
        )

    st.divider()

    # =========================
    # KOMMUNANALYS
    # =========================

    st.subheader("🏙️ Kommunernas roll i länets laddinfrastruktur")

    st.plotly_chart(
        laddstationer_typ_per_kommun_stacked("nr_charger", county),
        use_container_width=True
    )

    st.caption(
        "Staplarna visar både omfattning och typ av laddinfrastruktur per kommun. "
        "Större kommuner dominerar i volym, medan flera mindre kommuner uppvisar "
        "en relativt hög andel snabbladdning."
    )

    st.divider()

    # st.plotly_chart(
    #     laddpunkter_per_station_bar(df_nr_charger, county),
    #     use_container_width=True
    # )

    # st.caption(
    #     "Grafen visar hur tät laddinfrastrukturen är i genomsnitt. "
    #     "Högre värden indikerar stationer med fler laddpunkter."
    # )

    # st.divider()

    st.subheader("🚗 Infrastruktur i relation till elbilar")

    st.plotly_chart(
        elbil_per_laddpunkt("nr_charger",county),
        theme=None,
        use_container_width=True
    )

    st.caption(
        "Relationen mellan antal elbilar och laddstationer per kommun "
        "indikerar var infrastrukturen är relativt väl- eller underdimensionerad."
    )

else:
    st.info("⬆️ Välj ett län i kontrollpanelen för att visa analys.")
