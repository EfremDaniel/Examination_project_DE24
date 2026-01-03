import plotly_express as px
from backend.data_processing import query_analytics
import altair as alt


def horizontal_number_station_bar_chart(county):
    
    df = query_analytics("nr_charger")

    data = df[df["county"] == county]
    
    fig = px.bar(data, x="antal_ladd_stationer", y="municipality", title="Antal laddstationer för varje kommun", orientation="h")
    
    fig.update_layout(
        height = 35 * len(data) + 150
    )
    
    fig.update_yaxes(automargin= True)
    return fig 


def prepare_municipality_df(df, county):
    """
    Filtrerar på valt län och aggregerar per kommun.
    """
    return (
        df[df["COUNTY"] == county]
        .groupby("MUNICIPALITY", as_index=False)
        .agg({
            "ANTAL_LADD_STATIONER": "sum",
            "LADDPUNKTER": "sum",
            "ANTAL_SNABB_LADD_STATIONER": "sum"
        })
    )


def laddstationer_typ_per_kommun_stacked(df, county):
    """
    Staplad graf som visar vanliga laddstationer och snabbladdare
    per kommun i valt län (alla kommuner).
    """
    df_muni = prepare_municipality_df(df, county)

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
        title="Fördelning av laddstationstyper per kommun",
        labels={
            "ANTAL": "Antal laddstationer",
            "MUNICIPALITY": "Kommun",
            "TYP": "Typ av laddning"
        }
    )

    fig.update_layout(
        yaxis=dict(autorange="reversed"),
        legend_title_text="",
        height=35 * df_muni["MUNICIPALITY"].nunique() + 150
    )

    return fig


def laddpunkter_per_station_bar(df, county):
    """
    Visar genomsnittligt antal laddpunkter per station per kommun.
    """
    df_muni = prepare_municipality_df(df, county)
    df_muni = df_muni[df_muni["ANTAL_LADD_STATIONER"] > 0]

    df_muni["LADDPUNKTER_PER_STATION"] = (
        df_muni["LADDPUNKTER"] /
        df_muni["ANTAL_LADD_STATIONER"]
    )

    df_muni = df_muni.sort_values(
        "LADDPUNKTER_PER_STATION", ascending=False
    )

    fig = px.bar(
        df_muni,
        x="LADDPUNKTER_PER_STATION",
        y="MUNICIPALITY",
        orientation="h",
        title="Laddpunkter per station per kommun",
        labels={
            "LADDPUNKTER_PER_STATION": "Laddpunkter per station",
            "MUNICIPALITY": "Kommun"
        }
    )

    fig.update_layout(
        yaxis=dict(autorange="reversed"),
        height=35 * df_muni["MUNICIPALITY"].nunique() + 150
    )

    return fig


def infrastruktur_vs_elbilar_scatter(df_infra, county):
    """
    Scatterplot som visar relationen mellan antal elbilar
    och antal laddstationer per kommun.
    """
    df_plot = (
        df_infra[df_infra["COUNTY"] == county]
        .groupby("MUNICIPALITY", as_index=False)
        .agg({
            "TOTAL_VEHICLE": "sum",
            "ANTAL_LADD_STATIONER": "sum"
        })
    )

    chart = (
        alt.Chart(df_plot)
        .mark_circle(size=120)
        .encode(
            x=alt.X("TOTAL_VEHICLE:Q", title="Antal elbilar"),
            y=alt.Y("ANTAL_LADD_STATIONER:Q", title="Antal laddstationer"),
            tooltip=[
                "MUNICIPALITY",
                "TOTAL_VEHICLE",
                "ANTAL_LADD_STATIONER"
            ]
        )
        .properties(
            title="Infrastruktur i relation till elbilar (kommunnivå)",
            height=400
        )
    )

    return chart