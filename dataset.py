import json
import pandas as pd

# Carregar arquivo JSON de forma segura
with open("dados/vendas.json", encoding="utf-8") as file:
    data = json.load(file)

# Criar DataFrame
df = pd.DataFrame(data)

# Converter coluna de datas para datetime
df["Data da Compra"] = pd.to_datetime(
    df.get(
        "Data da Compra",
    ),
    format="%d/%m/%Y",
    errors="coerce",
)

# Ordenar por data
df = df.sort_values("Data da Compra")

# Criar colunas auxiliares para análise
df["Ano"] = df["Data da Compra"].dt.year
df["Mês"] = df["Data da Compra"].dt.month

# Visualizar as primeiras linhas
# print(df.head())

# Opcional: mostrar datas que não foram convertidas
invalid_dates = df[df["Data da Compra"].isna()]
if not invalid_dates.empty:
    print("Registros com datas inválidas:")
    print(invalid_dates)
