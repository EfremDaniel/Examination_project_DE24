import streamlit as st

st.set_page_config(
    page_title="Laddinfrastruktur i Sverige – Översikt",
    page_icon="🔌",
    layout="wide"
)

st.title("🔌 Laddinfrastruktur i Sverige", text_alignment= "center")

col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    st.image(
        "https://media.cnn.com/api/v1/images/stellar/prod/231128120835-tesla-sweden-charging-station.jpg?c=original",
        caption="Publik elbilsladdningsstation i Stockholm"
    )

st.markdown(
    """
    Denna dashboard är framtagen för att ge en **strukturerad och datadriven överblick**
    av den publika laddinfrastrukturen för elfordon i Sverige.

    Syftet är att stödja **analys, planering och uppföljning** av hur laddinfrastrukturen
    utvecklas geografiskt och över tid, samt att skapa bättre förutsättningar för jämförelser
    mellan regioner och kommuner.

    I samband med Sveriges mål att **förbjuda försäljning av nya bensin- och dieselbilar
    från och med år 2035** ökar kraven på en tillgänglig och väl dimensionerad
    laddinfrastruktur. Dashboarden är avsedd att fungera som ett faktabaserat
    analysunderlag för att förstå hur denna omställning påverkar behov, kapacitet
    och geografisk fördelning av laddmöjligheter.
    """
)

st.divider()


st.subheader("🎯 Syfte och inriktning")

st.markdown(
    """
    Dashboardens huvudsakliga syfte är att möjliggöra en **systematisk analys av Sveriges
    publika laddinfrastruktur** med fokus på både omfattning och kapacitet.

    Analysen är inriktad på att:
    - Ge en översikt av hur laddinfrastrukturen är uppbyggd
    - Synliggöra skillnader mellan snabbladdning och normalladdning
    - Möjliggöra jämförelser mellan kommuner
    - Relatera laddkapacitet till antalet elbilar
    """
)

st.divider()


st.subheader("🗂️ Datainnehåll och visualisering")

st.markdown(
    """
    Dashboarden visualiserar den publika laddinfrastrukturen med fokus på följande
    datatyper och analysvyer:
    """
)

st.markdown(
    """
    **Laddinfrastruktur**
    - Publika laddstationer och laddpunkter
    - Uppdelning mellan snabbladdare (DC) och normalladdare (AC)
    - Filtrering via dropdown-menyer (t.ex. laddtyp och kommun)

    **Nyckeltal (KPI:er)**
    - Totalt antal laddare
    - Antal snabbladdare
    - Antal laddoperatörer
    - Andel snabbladdare i procent

    **Kapacitet i relation till efterfrågan**
    - Stapeldiagram som visar maximal laddeffekt (kW) per 100 elbilar
    - Jämförelser mellan valda kommuner
    - Möjlighet att välja kommuner via dropdown  
      *(två kommuner visas alltid, med Stockholm och Göteborg som standardval)*
    """
)

st.divider()


st.subheader("👥 Målgrupp")

st.markdown(
    """
    Dashboarden är framtagen för användare som arbetar med analys och planering
    kopplat till elektrifiering och transportomställning.

    Exempel på målgrupper:
    - Kommuner och regioner
    - Myndigheter och offentliga aktörer
    - Energibolag och laddoperatörer
    - Konsulter, analytiker och forskare

    Dashboarden kan användas både för strategisk planering och för uppföljning
    av pågående utbyggnad av laddinfrastruktur.
    """
)

