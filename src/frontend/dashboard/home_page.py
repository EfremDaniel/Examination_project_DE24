import streamlit as st

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Laddinfrastruktur i Sverige",
    page_icon="🔌",
    layout="wide"
)

# =========================
# IMAGE SET (LUGN, NORDIC)
# =========================

IMAGES = [
    "https://cdn.pixabay.com/photo/2019/11/08/21/41/tesla-4609538_1280.jpg",   # elbil vid laddstation :contentReference[oaicite:3]{index=3}
    "https://images.pexels.com/photos/110844/pexels-photo-110844.jpeg",       # EV laddar på offentlig punkt :contentReference[oaicite:4]{index=4}
    "https://images.unsplash.com/photo-1549921296-3c44cc60910b"                # elbil + laddstation foto :contentReference[oaicite:5]{index=5}
]


if "img_idx" not in st.session_state:
    st.session_state.img_idx = 0

# =========================
# HERO
# =========================

st.title("Sveriges laddinfrastruktur")
st.caption("Överblick av publik laddning i ett elektrifierat samhälle")

st.divider()

# =========================
# BENTO RAD 1
# =========================

left, right = st.columns([2, 1], gap="large")

with left:
    with st.container(border=True):
        st.subheader("Helhetsbild")
        st.write("Nationell översikt av laddinfrastrukturens struktur.")

with right:
    with st.container(border=True):
        st.subheader("Regionala skillnader")
        st.write("Tillgången till laddning varierar mellan län.")

# =========================
# BENTO RAD 2
# =========================

c1, c2, c3 = st.columns(3, gap="large")

with c1:
    with st.container(border=True):
        st.subheader("Elbilsutveckling")
        st.write("Antalet elbilar ökar snabbt.")

with c2:
    with st.container(border=True):
        st.subheader("Laddtyper")
        st.write("Snabbladdning och normalladdning.")

with c3:
    with st.container(border=True):
        st.subheader("Kapacitet")
        st.write("Hur väl möts behov och infrastruktur?")

# =========================
# BENTO RAD 3 – BILDKORT
# =========================

text_col, image_col = st.columns([1, 2], gap="large")

with text_col:
    with st.container(border=True):
        st.subheader("Visuell kontext")
        st.write("Bilder används för att sätta sammanhang – inte visa data.")


# =========================
# CTA
# =========================

st.divider()

cta_l, cta_c, cta_r = st.columns([1, 2, 1])

with cta_c:
    with st.container(border=True):
        st.subheader("Utforska analysen")
        st.write("Fördjupa dig i hur laddinfrastrukturen är fördelad.")
        if st.button(
            "Öppna analysverktyget",
            use_container_width=True,
            type="primary"  # blå accent
        ):
            st.switch_page("pages/charger_analys_page.py")
