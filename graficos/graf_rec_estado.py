import plotly.express as px
from utils import df_rec_estado


def graf_rec_estado(df):
    df_estado = df_rec_estado(df)

    # Top 7 estados por receita
    df_plot = df_estado.sort_values("Preço", ascending=False).head(7)

    fig = px.bar(
        df_plot,
        x="Local da compra",
        y="Preço",
        custom_data=["Preço_formatado"],
        text="Preço_formatado",
        color="Preço",
        color_continuous_scale=["#DCE9FF", "#2C7BE5"],
        title="Top 7 Estados por Receita 🗺️",
    )

    fig.update_layout(
        height=540,
        template="plotly_white",
        xaxis_title="Estado",
        yaxis_title="Receita (R$)",
        margin=dict(l=60, r=30, t=190, b=20),
        showlegend=False,
        title={
            "x": 0.075,
            "y": 0.78,
            "xanchor": "left",
            "pad": {"t": 20},
        },
        yaxis=dict(
            tickprefix="R$ ",
            tickformat=",.0f",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.06)",
        ),
    )

    fig.update_traces(
        textposition="outside",
        textfont=dict(size=13, color="#2C7BE5"),
        marker=dict(opacity=0.9),
        hovertemplate=(
            "<b>Estado:</b> %{x}<br>"
            "<b>Receita:</b> %{customdata[0]}"
            "<extra></extra>"
        ),
    )

    fig.update_yaxes(rangemode="tozero")

    return fig
