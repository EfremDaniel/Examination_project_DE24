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


# =========================
# PLOTLY EXPRESS
# =========================

def stationer_per_kommun_bar(df, county, top_n=15):
    df_muni = prepare_municipality_df(df, county)

    df_plot = (
        df_muni
        .sort_values("ANTAL_LADD_STATIONER", ascending=False)
        .head(top_n)
    )

    fig = px.bar(
        df_plot,
        x="ANTAL_LADD_STATIONER",
        y="MUNICIPALITY",
        orientation="h",
        title="Antal laddstationer per kommun"
    )

    fig.update_layout(yaxis=dict(autorange="reversed"))
    return fig


def snabbladd_andel_per_kommun_bar(df, county, top_n=15):
    df_muni = prepare_municipality_df(df, county)
    df_muni = df_muni[df_muni["ANTAL_LADD_STATIONER"] > 0]

    df_muni["ANDEL_SNABBLADD"] = (
        df_muni["ANTAL_SNABB_LADD_STATIONER"] /
        df_muni["ANTAL_LADD_STATIONER"]
    )

    df_plot = (
        df_muni
        .sort_values("ANDEL_SNABBLADD", ascending=False)
        .head(top_n)
    )

    fig = px.bar(
        df_plot,
        x="ANDEL_SNABBLADD",
        y="MUNICIPALITY",
        orientation="h",
        title="Andel snabbladdare per kommun",
        labels={"ANDEL_SNABBLADD": "Andel"}
    )

    fig.update_layout(
        yaxis=dict(autorange="reversed"),
        xaxis_tickformat=".0%"
    )
    return fig


def laddpunkter_per_station_bar(df, county, top_n=15):
    df_muni = prepare_municipality_df(df, county)
    df_muni = df_muni[df_muni["ANTAL_LADD_STATIONER"] > 0]

    df_muni["LADDPUNKTER_PER_STATION"] = (
        df_muni["LADDPUNKTER"] /
        df_muni["ANTAL_LADD_STATIONER"]
    )

    df_plot = (
        df_muni
        .sort_values("LADDPUNKTER_PER_STATION", ascending=False)
        .head(top_n)
    )

    fig = px.bar(
        df_plot,
        x="LADDPUNKTER_PER_STATION",
        y="MUNICIPALITY",
        orientation="h",
        title="Laddpunkter per station per kommun"
    )

    fig.update_layout(yaxis=dict(autorange="reversed"))
    return fig


# =========================
# ALTAIR
# =========================

def infrastruktur_vs_elbilar_scatter(df_infra, county):
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
            title="Infrastruktur vs elbilar (kommunnivå)",
            width=600,
            height=400
        )
    )

    return chart