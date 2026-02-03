import plotly.express as px
from utils import df_rec_estado


def graf_map_estado(df):
    df_estado = df_rec_estado(df)

    # normaliza o tamanho das bolhas (escala visual)
    df_estado["tamanho"] = (
        df_estado["Preço"] / df_estado["Preço"].max()
    ) * 140 + 4  # ajuste fino aqui

    fig = px.scatter_mapbox(
        df_estado,
        lat="lat",
        lon="lon",
        size="tamanho",  # agora usa a coluna calculada
        hover_name="Local da compra",
        custom_data=["Preço_formatado"],
        hover_data={
            "lat": False,
            "lon": False,
            "tamanho": False,
            "Preço_formatado": True,
        },
        color="Preço",
        color_continuous_scale="Viridis",
        zoom=3,
        mapbox_style="open-street-map",
        title="Receita por Estado 🗺️",
    )

    fig.update_traces(
        hovertemplate=(
            "<b>%{hovertext}</b><br>" "Receita: %{customdata[0]}" "<extra></extra>"
        )
    )

    fig.update_layout(
        title={
            "x": 0.03,
            "y": 0.92,
            "xanchor": "left",
        },
        margin=dict(l=20, r=0, t=110, b=10),
        coloraxis_colorbar=dict(title="Receita (R$)"),
    )

    return fig
