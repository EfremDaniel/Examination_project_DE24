import streamlit as st
from backend.data_processing import query_analytics
from frontend.graph.chart_utils import (
    stationer_per_kommun_bar,
    snabbladd_andel_per_kommun_bar,
    laddpunkter_per_station_bar,
    infrastruktur_vs_elbilar_scatter
)

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Charger analysis",
    page_icon="⚡",
    layout="wide"
)

# =========================
# HEADER
# =========================

st.title("⚡ Charger analysis")

st.markdown(
    """
    **Interaktiv analys av Sveriges publika laddinfrastruktur.**  
    Välj ett län för att analysera hur kommunerna inom länet
    bidrar till laddkapacitet och tillgänglighet.
    """
)

st.divider()

# =========================
# DATA
# =========================

df_nr_charger = query_analytics("nr_charger")
df_infra = query_analytics("infrastructur")

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

    # Filtrera tidigt
    df_nr_charger_county = df_nr_charger[df_nr_charger["COUNTY"] == county]
    df_infra_county = df_infra[df_infra["COUNTY"] == county]

    # =========================
    # KPI:er (län-total via kommuner)
    # =========================

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
    # GRAFER – KOMMUNNIVÅ
    # =========================

    st.subheader("🏙️ Fördelning mellan kommuner")

    st.plotly_chart(
        stationer_per_kommun_bar(df_nr_charger, county),
        use_container_width=True
    )

    st.plotly_chart(
        snabbladd_andel_per_kommun_bar(df_nr_charger, county),
        use_container_width=True
    )

    st.plotly_chart(
        laddpunkter_per_station_bar(df_nr_charger, county),
        use_container_width=True
    )

    st.divider()

    # =========================
    # INFRASTRUKTUR VS ELBILAR
    # =========================

    st.subheader("🚗 Infrastruktur i relation till elbilar")

    st.altair_chart(
        infrastruktur_vs_elbilar_scatter(df_infra, county),
        use_container_width=True
    )

else:
    st.info("⬆️ Välj ett län i kontrollpanelen för att visa analys.")
