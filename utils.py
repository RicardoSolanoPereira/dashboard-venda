import pandas as pd
import streamlit as st
import time

# =========================
# FORMATADORES
# =========================


def format_number(value, prefix=""):
    """
    Formata um número grande com sufixos (mil, mi, bi).
    """
    try:
        value = float(value)
    except (TypeError, ValueError):
        return f"{prefix}0"

    units = ["", " mil", " mi", " bi"]
    for unit in units:
        if abs(value) < 1000:
            return f"{prefix}{value:.2f}{unit}".strip()
        value /= 1000

    return f"{prefix}{value:.2f} bi"


def format_preco(valor):
    """
    Formata valores monetários no padrão brasileiro.
    """
    try:
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (TypeError, ValueError):
        return "R$ 0,00"


# =========================
# DATAFRAMES AGREGADOS
# =========================


def df_rec_estado(df: pd.DataFrame) -> pd.DataFrame:
    """
    Retorna DataFrame de receita por estado com latitude e longitude.
    """
    df_estado = (
        df.groupby("Local da compra", as_index=False)["Preço"]
        .sum()
        .merge(
            df[["Local da compra", "lat", "lon"]].drop_duplicates(),
            on="Local da compra",
            how="left",
        )
        .sort_values("Preço", ascending=False)
    )
    df_estado["Preço_formatado"] = df_estado["Preço"].apply(format_preco)
    return df_estado


def df_rec_mensal(df: pd.DataFrame) -> pd.DataFrame:
    """
    Retorna DataFrame de receita agrupada por mês.
    """
    df = df.copy()
    df["Data da Compra"] = pd.to_datetime(df["Data da Compra"])
    df_mensal = (
        df.set_index("Data da Compra")
        .groupby(pd.Grouper(freq="ME"))["Preço"]
        .sum()
        .reset_index()
    )
    df_mensal["Ano"] = df_mensal["Data da Compra"].dt.year
    df_mensal["Mes"] = df_mensal["Data da Compra"].dt.month

    meses_pt = {
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

    df_mensal["Mes_nome"] = df_mensal["Mes"].map(meses_pt)

    return df_mensal


def df_rec_categoria(df: pd.DataFrame) -> pd.DataFrame:
    """
    Retorna DataFrame de receita por categoria.
    """
    df_categoria = (
        df.groupby("Categoria do Produto", as_index=False)["Preço"]
        .sum()
        .sort_values("Preço", ascending=False)
    )
    df_categoria["Preço_formatado"] = df_categoria["Preço"].apply(format_preco)
    return df_categoria


def df_rec_vendedores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Retorna DataFrame com total de receita, quantidade de vendas e participação percentual por vendedor.
    """
    df_vendedores = (
        df.groupby("Vendedor")["Preço"]
        .agg(total_receita="sum", qtd_vendas="count")
        .reset_index()
    )
    df_vendedores["total_receita_formatado"] = df_vendedores["total_receita"].apply(
        format_preco
    )
    df_vendedores["perc_receita"] = (
        df_vendedores["total_receita"] / df_vendedores["total_receita"].sum() * 100
    )
    return df_vendedores


# Função para converter arquivo csv
@st.cache_data
def convert_csv(df):
    return df.to_csv(index=False).encode("utf-8")


def mensagem_sucesso():
    success = st.success(
        "Arquivo baixado com sucesso",
        icon="✅",
    )
    time.sleep(3)
    success.empty()
