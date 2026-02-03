import streamlit as st
from dataset import df as df_raw
from utils import format_number
from graficos.graf_map_estado import graf_map_estado
from graficos.graf_rec_mensal import graf_rec_mensal
from graficos.graf_rec_estado import graf_rec_estado
from graficos.graf_rec_categoria import graf_rec_categoria
from graficos.graf_rec_vendedores import graf_rec_vendedores

# =========================
# CONFIGURAÇÃO DA PÁGINA
# =========================

st.set_page_config(
    page_title="Dashboard de Vendas",
    layout="wide",
)

st.title("Dashboard de Vendas 🛒")
st.caption("Análise de desempenho comercial")


# =========================
# CONSTANTES DE LAYOUT
# =========================

HEIGHT_MAP = 500
HEIGHT_BAR = 450
HEIGHT_LINE = 530


# =========================
# CARGA DE DADOS (CACHE)
# =========================


@st.cache_data
def load_data():
    return df_raw.copy()


df = load_data()

# =========================
# SIDEBAR — FILTRO
# =========================
st.sidebar.title("Filtros")

filtro_vendedor = st.sidebar.multiselect(
    "Vendedores",
    options=sorted(df["Vendedor"].unique()),
)

if filtro_vendedor:
    df = df[df["Vendedor"].isin(filtro_vendedor)]


# =========================
# ABAS
# =========================

aba_dataset, aba_receita, aba_vendedores = st.tabs(
    ["📄 Dataset", "💰 Receita", "👥 Vendedores"]
)


# =========================
# ABA 1 — DATASET
# =========================

with aba_dataset:
    st.dataframe(df, use_container_width=True)


# =========================
# ABA 2 — RECEITA
# =========================

with aba_receita:
    col_esq, col_dir = st.columns([6, 7])

    # ----- COLUNA ESQUERDA
    with col_esq:
        st.metric(
            label="Receita Total 💰",
            value=format_number(df["Preço"].sum(), "R$"),
        )

        fig_map = graf_map_estado(df)
        fig_map.update_layout(height=HEIGHT_MAP)

        st.plotly_chart(
            fig_map,
            use_container_width=True,
            config={"scrollZoom": True},
        )

        st.plotly_chart(
            graf_rec_estado(df),
            use_container_width=True,
        )

    # ----- COLUNA DIREITA
    with col_dir:
        _, col_metric = st.columns([1, 7])
        with col_metric:
            st.metric(
                label="Quantidade Total de Vendas 🧾",
                value=format_number(len(df)),
            )

        st.plotly_chart(
            graf_rec_mensal(df),
            use_container_width=True,
        )

        st.plotly_chart(
            graf_rec_categoria(df),
            use_container_width=True,
        )


# =========================
# ABA 3 — VENDEDORES
# =========================

from utils import df_rec_vendedores
from graficos.graf_rec_vendedores import graf_rec_vendedores
from graficos.graf_qt_vendas_vendedor import graf_qt_vendas_vendedor

with aba_vendedores:
    col_esq, col_dir = st.columns([1, 1])

    # Obter dados agregados de vendedores
    df_vendedores = df_rec_vendedores(df)
    df_vendedores["perc_receita"] = (
        df_vendedores["total_receita"] / df_vendedores["total_receita"].sum() * 100
    )

    # ----- COLUNA ESQUERDA — Receita
    with col_esq:
        st.metric(
            label="Receita Total 💰",
            value=format_number(df_vendedores["total_receita"].sum(), "R$"),
        )
        st.metric(
            label="Maior Receita de um Vendedor 💰",
            value=format_number(df_vendedores["total_receita"].max(), "R$"),
        )

        # Gráfico de receita por vendedor
        st.plotly_chart(
            graf_rec_vendedores(df),
            use_container_width=True,
        )

    # ----- COLUNA DIREITA — Quantidade de vendas
    with col_dir:
        st.metric(
            label="Quantidade Total de Vendas 🧾",
            value=format_number(df_vendedores["qtd_vendas"].sum()),
        )
        st.metric(
            label="Média de Vendas por Vendedor 🧾",
            value=format_number(df_vendedores["qtd_vendas"].mean()),
        )

        # Gráfico de quantidade de vendas por vendedor
        st.plotly_chart(
            graf_qt_vendas_vendedor(df),
            use_container_width=True,
        )
