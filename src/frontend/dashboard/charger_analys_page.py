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

st.title("Charger analysis")
st.caption(
    "Interaktiv analys av Sveriges publika laddinfrastruktur. "
    "Fokus på hur kommunerna inom ett län bidrar till omfattning "
    "och typ av laddkapacitet."
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
    st.subheader("Kontrollpanel")

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

    # -------------------------
    # SUMMARY
    # -------------------------

    st.subheader(f"Sammanfattning – {county}")
    st.caption("Övergripande nyckeltal för länets publika laddinfrastruktur.")

    df_nr_charger_county = df_nr_charger[df_nr_charger["COUNTY"] == county]

    total_stationer = df_nr_charger_county["ANTAL_LADD_STATIONER"].sum()
    laddpunkter = df_nr_charger_county["LADDPUNKTER"].sum()
    fast = df_nr_charger_county["ANTAL_SNABB_LADD_STATIONER"].sum()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Laddstationer",
            int(total_stationer),
            help="Totalt antal publika laddstationer i länet."
        )

    with col2:
        st.metric(
            "Laddpunkter",
            int(laddpunkter),
            help="Totalt antal laddpunkter kopplade till publika stationer."
        )

    with col3:
        st.metric(
            "Snabbladdning",
            f"{round((fast / total_stationer) * 100, 1)} %",
            help="Andel laddstationer som erbjuder snabbladdning."
        )

    st.divider()

    # -------------------------
    # MUNICIPAL ANALYSIS
    # -------------------------

    st.subheader("Kommunernas roll i länets laddinfrastruktur")

    st.plotly_chart(
        laddstationer_typ_per_kommun_stacked("nr_charger", county),
        use_container_width=True
    )

    st.caption(
        "Ett fåtal kommuner står för huvuddelen av länets laddinfrastruktur. "
        "Samtidigt uppvisar flera mindre kommuner en relativt hög andel "
        "snabbladdning, vilket tyder på ett fokus på genomfartstrafik "
        "snarare än destinationsladdning."
    )

    st.divider()

    # -------------------------
    # EV VS INFRASTRUCTURE
    # -------------------------

    st.subheader("Infrastruktur i relation till elbilar")

    st.plotly_chart(
        elbil_per_laddpunkt("nr_charger",county),
        theme=None,
       use_container_width=True
    )

    st.caption(
        "Kvoten mellan elbilar och laddpunkter indikerar var efterfrågan "
        "riskerar att överstiga tillgänglig laddkapacitet. Kommuner med "
        "hög kvot kan vara prioriterade för framtida investeringar."
    )

else:
    st.info("Välj ett län i kontrollpanelen för att visa analys.")
