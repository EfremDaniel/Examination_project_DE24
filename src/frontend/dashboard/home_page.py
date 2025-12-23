import streamlit as st

st.set_page_config(
    page_title="Laddinfrastruktur i Sverige",
    page_icon="🔌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# SIDEBAR – ORIENTERING
# =========================

with st.sidebar:
    st.markdown("## 🔌 Laddinfrastruktur i Sverige")

    st.markdown(
        """
        Nationell översikt av Sveriges **publika laddinfrastruktur**
        för elfordon.
        """
    )

    st.divider()

    st.markdown("### 🎯 Syfte")
    st.markdown(
        """
        • Jämföra laddkapacitet mellan län  
        • Synliggöra skillnader i laddtyper  
        • Relatera laddning till elbilsbestånd  
        """
    )

    st.divider()

    st.caption("Dashboard för analys och planering")



st.title("Laddinfrastruktur i Sverige", text_alignment="center")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.image(
        "https://media.cnn.com/api/v1/images/stellar/prod/231128120835-tesla-sweden-charging-station.jpg?c=original",
        caption="Publik elbilsladdningsstation i Stockholm",
        use_container_width=True
    )

st.markdown(
    """
    **En samlad vy över hur Sveriges publika laddinfrastruktur är uppbyggd
    och hur väl den möter efterfrågan från elbilsflottan.**
    """
)

st.divider()

# =========================
# CTA – STARTA ANALYS
# =========================

# =========================
# CTA – HUVUDFUNKTION
# =========================

st.subheader("⚡ Starta analysverktyget")

cta_col1, cta_col2, cta_col3 = st.columns([1, 2, 1])

with cta_col2:
    with st.container(border=True):
        st.markdown(
            """
            ### Charger analysis
            Ett interaktivt analysverktyg för att utvärdera
            Sveriges publika laddinfrastruktur.

            **Du kan:**
            - Jämföra laddstationer mellan län
            - Analysera snabbladdning vs normalladdning
            - Relatera laddkapacitet till antal elbilar
            """
        )

        st.markdown("")

        if st.button(
            "▶ Öppna analysverktyget",
            use_container_width=True,
            type="primary"
        ):
            st.switch_page("pages/charger_analys_page.py")

st.divider()

# =========================
# AVSLUT – VAD KAN DU GÖRA
# =========================

st.subheader("Vad kan du göra här?")

st.markdown(
    """
    - Få en överblick av laddinfrastrukturens omfattning  
    - Identifiera regionala skillnader  
    - Använda data som underlag för planering och uppföljning  
    """
)

st.info("➡️ Klicka på **Charger analys** för att börja utforska data.")
