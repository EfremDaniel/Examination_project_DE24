import plotly_express as px
from backend.data_processing import query_analytics

    

def prepare_municipality_df(mart, county):
    """
    Filtrerar på valt län och aggregerar per kommun.
    """
    df = query_analytics(mart)
    return (
        df[df["COUNTY"] == county]
        .groupby("MUNICIPALITY", as_index=False)
        .agg({
            "ANTAL_LADD_STATIONER": "sum",
            "LADDPUNKTER": "sum",
            "ANTAL_SNABB_LADD_STATIONER": "sum"
        })
    )


def laddstationer_typ_per_kommun_stacked(mart, county):
    df_muni = prepare_municipality_df(mart, county)

    df_muni["VANLIGA_LADDSTATIONER"] = (
        df_muni["ANTAL_LADD_STATIONER"] - df_muni["ANTAL_SNABB_LADD_STATIONER"]
    )

    df_muni = df_muni.sort_values(
        "ANTAL_LADD_STATIONER", ascending=False
    )

    df_long = df_muni.melt(
        id_vars="MUNICIPALITY",
        value_vars=[
            "VANLIGA_LADDSTATIONER",
            "ANTAL_SNABB_LADD_STATIONER"
        ],
        var_name="TYP",
        value_name="ANTAL"
    )

    df_long["TYP"] = df_long["TYP"].replace({
        "VANLIGA_LADDSTATIONER": "Vanliga laddstationer",
        "ANTAL_SNABB_LADD_STATIONER": "Snabbladdstationer"
    })

    fig = px.bar(
        df_long,
        x="ANTAL",
        y="MUNICIPALITY",
        color="TYP",
        orientation="h",
        barmode="stack",
        labels={
            "ANTAL": "",
            "MUNICIPALITY": "",
            "TYP": "Typ av laddning"
        },
        color_discrete_map={
            "Vanliga laddstationer": "#4E342E",
            "Snabbladdstationer": "#F26B1D"
        },
        template="simple_white"
    )

    # Annotering för x-label
    fig.add_annotation(
        text= "ANTAL LADDSTATIONER",
        font= dict(
            size= 13,
            color="black",
            family= "Ariel, sans-serif"
            ), 
        xref= "paper",
        yref= "paper",
        x= 0.0,
        y= 0.0,
        opacity=0.8,
        xanchor="left",
        yanchor= "top",
        yshift= -50,
        showarrow=False
    )


    # Axlar
    fig.update_xaxes(
        showline=True,
        linewidth=1,
        linecolor="rgba(0,0,0,0.3)",
        title_font=dict(
            size=13,
            family="Arial",
            color="black"   # 🔑 x-label svart
        ),
        title_standoff=20
    )

    fig.update_yaxes(
        showline=False,
        categoryorder="total ascending"
    )

    # Y-label som annotation
    fig.add_annotation(
        text="KOMMUN",
        font=dict(size=13, color="black", family="Arial"),
        xref="paper",
        yref="paper",
        x=0,
        y=1,
        xanchor="center",
        yanchor="top",
        xshift= -50,
        yshift=30,
        opacity=0.8,
        showarrow=False
    )

    # Titel – vänster, men inte för nära y-label
    fig.update_layout(
        title=dict(
            text="Fördelning av laddstationstyper per kommun",
            xref = "paper",
            yref = "paper",
            x=0,
            y=1,
            xanchor="left",
            yanchor="top",
            pad = dict(l=0, t=-50),
            font=dict(
                size=15,
                family="Arial, sans-serif",
                color= "#292B2F"
            )
        ),
        legend_title_text="",
        margin=dict(l=160, b=80, t=100),
        height=35 * df_muni["MUNICIPALITY"].nunique() + 150
    )

    return fig


def elbil_per_laddpunkt(mart, county):
    """Create a scatter plot for how electricities car per charging point.
    It show how many vehicle there is on one charging point."""
    
    df = query_analytics(mart)
    df_county = df.query(f"COUNTY == '{county}'")[["MUNICIPALITY", "LADDPUNKTER", "TOTAL_VEHICLE", "ANTAL_SNABB_LADD_STATIONER", "ANTAL_LADD_STATIONER"]]
    
    df_county["ELBIL_PER_LADDPUNKT"] = df_county["TOTAL_VEHICLE"]/ df_county["LADDPUNKTER"]
    df_county["PROCENT_SNABB"] = round(df_county["ANTAL_SNABB_LADD_STATIONER"] / df_county["ANTAL_LADD_STATIONER"] * 100, 2)
    
    ticksval_x = [1,2,5,10,20,50,100,200,500,1000,2000,5000,10000]
    ticksval_y = [5, 10, 15, 20, 30, 50, 100]


    fig = px.scatter(
        df_county,
        x="LADDPUNKTER",
        y="ELBIL_PER_LADDPUNKT",
        hover_name="MUNICIPALITY",
        color= "MUNICIPALITY",
        size_max=30,
        opacity=0.6,
        template="plotly_white",
        hover_data= {
            "LADDPUNKTER": ":.0f",
            "ELBIL_PER_LADDPUNKT": ":.1f",
            "PROCENT_SNABB": ":.1f",
            "MUNICIPALITY": False
        },
        labels= {
            "LADDPUNKTER": "Laddpunkter",
            "ELBIL_PER_LADDPUNKT": "Elbilar per laddpunkter",
            "PROCENT_SNABB": "Andel sanbbladdare (%)",
            "MUNICIPALITY": "Kommuner"
        }
    )



    # Add line where elbil per laddpunkt is 10. 
    fig.add_hline(y=10, line_width= 2, line_color= "#02010F", opacity=0.6)


    fig.update_traces(marker=dict(line=dict(width=0)))

    # update y- and x-axel
    fig.update_xaxes(type="log", tickmode= "array",  tickvals= ticksval_x, ticktext= [str(v) for v in ticksval_x], ticks= "", title_text= "")
    fig.update_xaxes(showline= True, linewidth= 1, linecolor="rgba(0,0,0,0.3)")
    fig.update_yaxes(type= "log", tickmode= "array", tickvals= ticksval_y, ticktext= [str(v) for v in ticksval_y], ticks= "",title_text= "")
    fig.update_yaxes(showline= True, linewidth=1, linecolor="rgba(0,0,0,0.3)")
    


    # Give titel to y-axel
    fig.add_annotation(
        text= "ELBILAR PER<br>""LADDPUNKT",
        font= dict(
            size= 13,
            color= "black",
            family= "Ariel, sans-serif"
        ),
        xref= "paper",
        yref= "paper",
        x= 0.0,
        y= 1,
        xanchor="left",
        yanchor= "top",
        xshift= -110,
        yshift= 40,
        opacity= 0.8,
        showarrow=False
    )

    # Give title to x-axel
    fig.add_annotation(
        text= "ANTAL LADDPUNKTER",
        font= dict(
            size= 13,
            color="black",
            family= "Ariel, sans-serif"
            ), 
        xref= "paper",
        yref= "paper",
        x= 0.0,
        y= 0.0,
        opacity=0.8,
        xanchor="left",
        yanchor= "top",
        yshift= -30,
        showarrow=False
    )

    

    # update title 
    fig.update_layout(
        title=dict(
            text= "Horisontell linje visar EU:s referenspunkt för cirka 10 elbilar per laddpunkt.<br>",
            y= 0.90,
            x= 0.0,
            xanchor= "left",
            yanchor= "top",
            xref= "paper",
            pad=dict(l=0),
            font= dict(
                size= 17,
                family= "Ariel, sans-serif",
                color= "#292B2F" 
            )
            
        ),
        margin= dict(l= 110, b= 70, t= 100),
    )
    
    fig.update_traces(
    marker=dict(
        size= 14,
        opacity=0.8,
    )
                  )

    return fig
  