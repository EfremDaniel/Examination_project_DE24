import streamlit as st

# =========================
# PAGE CONFIG (MÅSTE VARA FÖRST)
# =========================
st.set_page_config(
    page_title="Laddinfrastruktur i Sverige",
    page_icon="🔌",
    layout="wide"
)

# =========================
# GLOBAL CSS
# =========================
st.markdown("""
<style>

/* ===== APP BAKGRUND ===== */
.stApp {
    background-color: #DFF5EA;
}

/* ===== TOP BAR / HEADER ===== */
header[data-testid="stHeader"] {
    background-color: #DFF5EA;
    box-shadow: none;
    border-bottom: none;
}

header[data-testid="stHeader"] svg {
    fill: #0F3D2E;
}

header[data-testid="stHeader"] span,
header[data-testid="stHeader"] button {
    color: #0F3D2E;
}

/* ===== SIDEBAR (ENDAST VISUELL) ===== */
section[data-testid="stSidebar"],
section[data-testid="stSidebar"] > div {
    background-color: #0F3D2E;
}

section[data-testid="stSidebar"] * {
    color: #E8FFF6;
}

/* ===== CONTENT KPI-KORT ===== */
.content-kpi {
    background-color: #0F3D2E;
    color: #E8FFF6;
    padding: 1.6rem;
    border-radius: 18px;
    min-height: 190px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.18);
}

.content-kpi h3 {
    margin-top: 0;
    font-size: 1.1rem;
    font-weight: 700;
}

.content-kpi p {
    margin-top: 0.6rem;
    line-height: 1.5;
    opacity: 0.9;
}

/* ===== CTA BUTTON ===== */
button[kind="primary"] {
    background-color: #0F3D2E !important;
    color: #FFFFFF !important;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR (TOM MEDVETET)
# =========================
st.sidebar.empty()

# =========================
# HERO
# =========================
st.title("Sveriges laddinfrastruktur")
st.caption("En kvalitativ översikt av publik laddning i ett elektrifierat samhälle")
st.divider()

# =========================
# RAD 1 – KPI-KORT
# =========================
left, right = st.columns([2, 1], gap="large")

with left:
    st.markdown("""
    <div class="content-kpi">
        <h3>Helhetsbild</h3>
        <p>
            En övergripande beskrivning av hur Sveriges publika
            laddinfrastruktur är uppbyggd och hur den samverkar
            med elektrifieringen av transportsektorn.
        </p>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown("""
    <div class="content-kpi">
        <h3>Regionala skillnader</h3>
        <p>
            Tillgången till laddning varierar mellan olika delar
            av landet beroende på befolkningstäthet, resmönster
            och lokala förutsättningar.
        </p>
    </div>
    """, unsafe_allow_html=True)

# =========================
# RAD 2 – KPI-KORT
# =========================
c1, c2, c3 = st.columns(3, gap="large")

with c1:
    st.markdown("""
    <div class="content-kpi">
        <h3>Elbilsutveckling</h3>
        <p>
            Elektrifieringen av fordonsflottan driver behovet av
            en laddinfrastruktur som är skalbar och långsiktigt hållbar.
        </p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="content-kpi">
        <h3>Laddtyper</h3>
        <p>
            Olika laddlösningar fyller olika funktioner, från
            snabbladdning längs större transportleder till
            vardagsladdning i närmiljö.
        </p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="content-kpi">
        <h3>Kapacitet</h3>
        <p>
            Förhållandet mellan tillgänglig laddkapacitet och
            efterfrågan är centralt för ett stabilt och tillförlitligt
            laddnätverk.
        </p>
    </div>
    """, unsafe_allow_html=True)

# =========================
# CTA
# =========================
st.divider()

cta_l, cta_c, cta_r = st.columns([1, 2, 1])

with cta_c:
    st.subheader("Fördjupa analysen")
    st.write("Utforska hur laddinfrastrukturen är uppbyggd och utvecklas.")
    if st.button(
        "Öppna analysverktyget",
        use_container_width=True,
        type="primary"
    ):
        st.switch_page("pages/charger_analys_page.py")
