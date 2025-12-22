import streamlit as st
from backend.data_processing import query_analytics

def list_county(df):
    county = df["county"].unique()
    return county

def station_county(df, county):
    
    count_county = df.groupby("county")["antal_ladd_stationer"].sum()
    
    return count_county.loc[county].astype(int)
    
def ladd_punkter(df, county):
    
    count_ladd_punkter = df.groupby("county")["laddpunkter"].sum()
    
    return count_ladd_punkter.loc[county].astype(int)


def ladd_stationer_elbilar(df, county):
    
    load_station = df.groupby("county")["antal_ladd_stationer"].sum()
    amount_vehicle = df.groupby("county")["total_vehicle"].sum()
    
    return round(load_station.loc[county] / amount_vehicle.loc[county] * 1000, 2)

def pr_snabb_ladd_stationer(df, county):
    
    
    count_total_charger_county = df.groupby("county")["antal_ladd_stationer"].sum()
    count_fast_charger_county = df.groupby("county")["antal_snabb_ladd_stationer"].sum()
    
    return f"{round(100 * (count_fast_charger_county.loc[county]/count_total_charger_county.loc[county]),2)}%"

def kw_ladd_stationer(df, county):
    
    kw = df.groupby("county")["total_kw"].sum()
    
    car = df.groupby("county")["total_vehicle"].sum()
    
    return f"{round((kw.loc[county]/car.loc[county]) * 1000,2)}kW" 

def vehicle_per_county(df, county):
    
    amount_vehicle = df.groupby("county")["total_vehicle"].sum()
    
    return amount_vehicle.loc[county].astype(int)

def layout():
    
    df_nr_charger = query_analytics("nr_charger")
    df_infrastructur = query_analytics("infrastructur")
    
    st.title("CHARGER BUZZ", text_alignment="center")
    st.markdown("---")
    st.markdown("")



    st.markdown("## kpi:er för antal ladd stationer ladd punkter och procent för snabb ladd stationer i Sverige")

    county = st.selectbox(label= "Län", options=list_county(df_nr_charger), width= 280)


    col1, col2, col3 = st.columns(3)
    with col1:
        container1 = st.container(border= True)
        container1.metric(label= "Antal ladd stationer", value= station_county(df= df_nr_charger, county= county))
    with col2:
        container2= st.container(border=True)
        container2.metric(label= "Antal ladd punkter", value= ladd_punkter(df= df_nr_charger, county= county))
        
    with col3:
        container4 = st.container(border=True)
        container4.metric(label= "Procentantal för snabb laddare", value= pr_snabb_ladd_stationer(df= df_nr_charger, county= county))

    # barchart of municipality antal ladd stationer      # barchart of municipality procentantal ladd stationer
    #st.plotly_chart()                


    st.markdown("## KPI:er för antal laddstationer per 1000 bilar")

    col5, col6, col7 = st.columns(3)

    with col5:
        container5 = st.container(border=True)
        container5.metric(label="Antal laddstationer per 1000 bilar", value= ladd_stationer_elbilar(df = df_infrastructur, county= county))
        
    with col6:
        container6 = st.container(border=True)
        container6.metric(label="Installerad laddeffekt (kW) per 1000 elbilar", value= kw_ladd_stationer(df= df_infrastructur, county= county))
        
    with col7:
        container7 = st.container(border=True)
        container7.metric(label="Antal laddfordom", value= vehicle_per_county(df = df_infrastructur, county= county))



if __name__=="__main__":
    
    st.set_page_config(
    page_title="Charger buzz",
    page_icon="🔋",
    layout="wide"
    )
    layout()