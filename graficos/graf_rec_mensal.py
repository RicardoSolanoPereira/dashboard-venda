import plotly.express as px
import pandas as pd
from utils import df_rec_mensal, format_preco

# Mapeamento fixo dos meses para o eixo X
MESES_PT = {
    1: "Jan",
    2: "Fev",
    3: "Mar",
    4: "Abr",
    5: "Mai",
    6: "Jun",
    7: "Jul",
    8: "Ago",
    9: "Set",
    10: "Out",
    11: "Nov",
    12: "Dez",
}


def graf_rec_mensal(df):
    df_mensal = df_rec_mensal(df)

    # Ordenação por Ano e Mês
    df_mensal = df_mensal.sort_values(["Ano", "Mes"])

    # Criar coluna de nomes dos meses
    df_mensal["Mes_nome"] = df_mensal["Mes"].map(MESES_PT)

    # Garantir ordem cronológica do eixo X
    df_mensal["Mes_nome"] = pd.Categorical(
        df_mensal["Mes_nome"],
        categories=list(
            MESES_PT.values(),
        ),
        ordered=True,
    )

    # Preço formatado para hover
    df_mensal["Preço_formatado"] = df_mensal["Preço"].apply(
        format_preco,
    )

    # Criar gráfico de linha
    fig = px.line(
        df_mensal,
        x="Mes_nome",  # usa agora o nome do mês
        y="Preço",
        markers=True,
        color="Ano",
        line_dash="Ano",
        custom_data=["Ano", "Preço_formatado"],
        title="Receita Mensal 🗓️",
    )

    # Layout
    fig.update_layout(
        hovermode="x unified",
        template="plotly_white",
        height=530,
        margin=dict(l=160, r=20, t=150, b=40),
        title=dict(
            text="Receita Mensal 🗓️",
            x=0.01,
            xanchor="left",
            y=0.95,
            yanchor="top",
            pad=dict(l=85, t=10),
        ),
        xaxis=dict(
            title="Mês",
            categoryorder="array",
            categoryarray=list(MESES_PT.values()),
            showspikes=True,
            spikemode="across",
            spikesnap="data",
            spikecolor="rgba(0,0,0,0.4)",
            spikethickness=1,
        ),
        yaxis=dict(
            title="Receita (R$)",
            tickprefix="R$ ",
            tickformat=",.0f",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.08)",
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
        legend_title_text="Ano",
    )

    # Hover personalizado
    fig.update_traces(
        hovertemplate=(
            "<b>Mês:</b> %{x}<br>"
            "<b>Ano:</b> %{customdata[0]}<br>"
            "<b>Receita:</b> %{customdata[1]}<extra></extra>"
        )
    )

    return fig
