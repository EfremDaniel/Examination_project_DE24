import plotly_express as px
from backend.data_processing import query_analytics


def horizontal_number_station_bar_chart(county):
    
    df = query_analytics("nr_charger")

    data = df[df["county"] == county]
    
    fig = px.bar(data, x="antal_ladd_stationer", y="municipality", title="Antal laddstationer för varje kommun", orientation="h")
    
    fig.update_layout(
        height = 35 * len(data) + 150
    )
    
    fig.update_yaxes(automargin= True)
    return fig 
