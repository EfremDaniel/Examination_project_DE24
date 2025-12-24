import streamlit as st
from backend.data_processing import query_analytics

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
    Välj ett län för att analysera laddstationer, laddpunkter
    och kapacitet i relation till elbilsbeståndet.
    """
)

st.divider()

# =========================
# DATA
# =========================

df_nr_charger = query_analytics("nr_charger")
df_infra = query_analytics("infrastructur")

# =========================
# KONTROLLPANEL
# =========================

with st.container(border=True):
    st.markdown("### 🔧 Kontrollpanel")

    county_options = ["Välj län"] + sorted(df_nr_charger["COUNTY"].unique())

    county = st.selectbox(
        "Län",
        options=county_options,
        index=0,
        help="Välj ett län för att uppdatera alla nyckeltal och analyser."
    )

st.divider()

# =========================
# RESULTAT
# =========================

if county != "Välj län":

    st.subheader("📊 Resultat")

    # KPI:er
    col1, col2, col3 = st.columns(3)

    with col1:
        total_stationer = (
            df_nr_charger
            .groupby("COUNTY")["ANTAL_LADD_STATIONER"]
            .sum()
            .loc[county]
        )
        st.metric("Antal laddstationer", int(total_stationer))

    with col2:
        laddpunkter = (
            df_nr_charger
            .groupby("COUNTY")["LADDPUNKTER"]
            .sum()
            .loc[county]
        )
        st.metric("Antal laddpunkter", int(laddpunkter))

    with col3:
        fast = (
            df_nr_charger
            .groupby("COUNTY")["ANTAL_SNABB_LADD_STATIONER"]
            .sum()
            .loc[county]
        )
        st.metric(
            "Andel snabbladdare",
            f"{round((fast / total_stationer) * 100, 1)} %"
        )

    st.divider()

    # Kapacitet vs elbilar
    st.subheader("🚗 Kapacitet i relation till elbilar")

    col4, col5, col6 = st.columns(3)

    with col4:
        stationer_per_1000 = (
            df_infra
            .groupby("COUNTY")["ANTAL_LADD_STATIONER"]
            .sum()
            .loc[county]
            /
            df_infra
            .groupby("COUNTY")["TOTAL_VEHICLE"]
            .sum()
            .loc[county]
            * 1000
        )
        st.metric(
            "Laddstationer per 1000 elbilar",
            round(stationer_per_1000, 2)
        )

    with col5:
        kw_per_1000 = (
            df_infra
            .groupby("COUNTY")["TOTAL_KW"]
            .sum()
            .loc[county]
            /
            df_infra
            .groupby("COUNTY")["TOTAL_VEHICLE"]
            .sum()
            .loc[county]
            * 1000
        )
        st.metric(
            "Installerad effekt per 1000 elbilar",
            f"{round(kw_per_1000, 1)} kW"
        )

    with col6:
        vehicles = (
            df_infra
            .groupby("COUNTY")["TOTAL_VEHICLE"]
            .sum()
            .loc[county]
        )
        st.metric("Antal elbilar", int(vehicles))

else:
    st.info("⬆️ Välj ett län i kontrollpanelen för att visa analys.")
