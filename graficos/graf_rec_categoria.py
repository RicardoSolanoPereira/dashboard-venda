import plotly.express as px
from utils import df_rec_categoria, format_preco


def graf_rec_categoria(df):
    df_cat = df_rec_categoria(df)

    # Top 7 categorias
    df_cat = df_cat.head(7)

    df_cat["Preço_formatado"] = df_cat["Preço"].apply(
        format_preco,
    )

    fig = px.bar(
        df_cat,
        x="Categoria do Produto",
        y="Preço",
        text="Preço_formatado",
        custom_data=["Preço_formatado"],
        color="Preço",
        color_continuous_scale=["#DCE9FF", "#2C7BE5"],
        title="Top 7 Categorias por Receita 📊",
    )

    fig.update_layout(
        height=505,
        template="plotly_white",
        xaxis_title="Categoria",
        yaxis_title="Receita (R$)",
        margin=dict(l=175, r=1, t=150, b=80),
        showlegend=False,
        title={
            "text": "Top 7 Categorias por Receita 📊",
            "x": 0.15,
            "y": 0.80,
            "xanchor": "left",
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
            "<b>Categoria:</b> %{x}<br>"
            "<b>Receita:</b> %{customdata[0]}"
            "<extra></extra>"
        ),
    )

    fig.update_yaxes(rangemode="tozero")

    return fig
