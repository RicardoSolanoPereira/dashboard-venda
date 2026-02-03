import plotly.express as px
from utils import df_rec_vendedores


def graf_qt_vendas_vendedor(df):
    """
    Gráfico de barras mostrando quantidade de vendas por vendedor.
    Vendedores abaixo da média são destacados discretamente.
    Legenda indica 'Acima da média' e 'Abaixo da média'.
    """
    # Agregar dados por vendedor
    df_vendedores = df_rec_vendedores(df)

    # Ordenar por quantidade de vendas decrescente
    df_vendedores = df_vendedores.sort_values("qtd_vendas", ascending=False)

    # Calcular média de vendas
    media_vendas = df_vendedores["qtd_vendas"].mean()

    # Categorizar vendedores
    df_vendedores["categoria"] = df_vendedores["qtd_vendas"].apply(
        lambda x: "Acima da média" if x >= media_vendas else "Abaixo da média"
    )

    # Cores discretas e suaves
    cores = {
        "Acima da média": "rgba(44, 123, 229, 0.6)",  # azul suave
        "Abaixo da média": "rgba(255, 77, 79, 0.4)",  # vermelho suave
    }

    # Criar gráfico de barras
    fig = px.bar(
        df_vendedores,
        x="Vendedor",
        y="qtd_vendas",
        text="qtd_vendas",
        color="categoria",
        color_discrete_map=cores,
        custom_data=["perc_receita", "total_receita"],
        title="Vendas por Vendedor 🧾",
    )

    # Layout
    fig.update_layout(
        template="plotly_white",
        height=650,
        margin=dict(l=60, r=0, t=80, b=40),
        xaxis_title="Vendedor",
        yaxis_title="Quantidade de Vendas",
        legend_title_text="Categoria",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        showlegend=True,
    )

    # Textos e hover
    fig.update_traces(
        textposition="outside",
        textfont=dict(size=13, color="#2C7BE5"),
        hovertemplate=(
            "<b>Vendedor:</b> %{x}<br>"
            "<b>Vendas:</b> %{y}<br>"
            "<b>Receita:</b> R$ %{customdata[1]:,.2f}<br>"
            "<b>Participação na Receita:</b> %{customdata[0]:.1f}%<extra></extra>"
        ),
    )

    # Eixo Y começa do zero
    fig.update_yaxes(rangemode="tozero")

    return fig
