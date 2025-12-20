import streamlit as st


st.set_page_config(
    page_title="Charger buzz",
    page_icon="🔋",
    layout="wide"
    )

st.title("CHARGER BUZZ", text_alignment="center")
st.markdown("---")
st.markdown("")



st.markdown("## kpi:er för infrastrukturen för laddstationer i Sverige")

st.selectbox(label= "Län", options=["Län"], width= 280)


col1, col2, col3, col4= st.columns(4)
with col1:
    container1 = st.container(border= True)
    container1.write("Antal laddare")
with col2:
    container2= st.container(border=True)
    container2.write("Antal operator")
with col3:
    container3 = st.container(border=True)
    container3.write("antal laddpunkter")
    
with col4:
    container4 = st.container(border=True)
    container4.write("Procentantal för snabb laddare")

# barchart of municipality 
#st.plotly_chart()


st.markdown("## KPI:er för antal laddstationer per 100 bilar")

col5, col6, col7 = st.columns(3)

with col5:
    container5 = st.container(border=True)
    container5.write("Antal laddare per 100 bilar")
    
with col6:
    container6 = st.container(border=True)
    container6.write("Max effekt per 100 bilar")
    
with col7:
    container7 = st.container(border=True)
    container7.write("Antal bilar")



    