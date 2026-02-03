import plotly.graph_objects as go
from utils import df_rec_vendedores, format_preco


def graf_rec_vendedores(df):
    """
    Gráfico elegante de receita por vendedor:
    - Barras discretas
    - Linha da média de receita
    - Hover rico (receita, vendas e %)
    """
    df_vendedores = df_rec_vendedores(df)
    df_vendedores = df_vendedores.sort_values("total_receita", ascending=False)

    receita_total = df_vendedores["total_receita"].sum()
    media_receita = df_vendedores["total_receita"].mean()

    df_vendedores["receita_fmt"] = df_vendedores["total_receita"].apply(format_preco)
    df_vendedores["perc_receita"] = df_vendedores["total_receita"] / receita_total * 100

    fig = go.Figure()

    # Barras principais
    fig.add_trace(
        go.Bar(
            x=df_vendedores["Vendedor"],
            y=df_vendedores["total_receita"],
            name="Receita",
            marker_color="#3A5FCD",  # azul elegante
            opacity=0.85,
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Receita: %{customdata[0]}<br>"
                "Vendas: %{customdata[1]}<br>"
                "Participação: %{customdata[2]:.1f}%<extra></extra>"
            ),
            customdata=df_vendedores[["receita_fmt", "qtd_vendas", "perc_receita"]],
        )
    )

    # Linha da média (bem sutil)
    fig.add_trace(
        go.Scatter(
            x=df_vendedores["Vendedor"],
            y=[media_receita] * len(df_vendedores),
            mode="lines",
            name="Média",
            line=dict(color="#B0B0B0", width=2, dash="dot"),
            hovertemplate=f"Média de Receita: {format_preco(media_receita)}<extra></extra>",
        )
    )

    # Layout clean & premium
    fig.update_layout(
        title="Receita por Vendedor",
        template="simple_white",
        height=460,
        margin=dict(l=20, r=20, t=50, b=30),
        xaxis=dict(
            title="",
            tickfont=dict(size=12),
            showline=False,
        ),
        yaxis=dict(
            title="Receita (R$)",
            tickprefix="R$ ",
            separatethousands=True,
            gridcolor="rgba(0,0,0,0.04)",
        ),
        legend=dict(
            orientation="h",
            y=1.08,
            x=1,
            xanchor="right",
        ),
    )

    return fig
