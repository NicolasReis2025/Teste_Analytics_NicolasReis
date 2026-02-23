import pandas as pd
import sqlite3

#  Carregar CSV e criar banco SQLite em memória 
dados = pd.read_csv("dataset_vendas.csv", sep=";")
dados["Data"]       = pd.to_datetime(dados["Data"], format="mixed")
dados               = dados.dropna(subset=["Quantidade"])
dados["Quantidade"] = dados["Quantidade"].astype(int)
dados["Total"]      = (dados["Quantidade"] * dados["Preço (R$)"]).round(2)

con = sqlite3.connect(":memory:")
dados.to_sql("vendas", con, index=False, if_exists="replace")

#  Consulta 1 — Total de vendas por produto 
query1 = """
    SELECT
        Produto,
        Categoria,
        SUM(Quantidade)                      AS Total_Quantidade,
        ROUND(SUM(Quantidade * "Preço (R$)"), 2) AS Total_Vendas
    FROM vendas
    GROUP BY Produto, Categoria
    ORDER BY Total_Vendas DESC
"""

resultado1 = pd.read_sql_query(query1, con)

print("=" * 65)
print("  CONSULTA 1 — Total de Vendas por Produto (ordem decrescente)")
print("=" * 65)
print(resultado1.to_string(index=False))

#  Consulta 2 — Produtos que menos venderam em junho de 2023 
query2 = """
    SELECT
        Produto,
        Categoria,
        SUM(Quantidade) AS Total_Quantidade,
        ROUND(SUM(Quantidade * "Preço (R$)"), 2) AS Total_Vendas
    FROM vendas
    WHERE strftime('%Y', Data) = '2023'
      AND strftime('%m', Data) = '06'
    GROUP BY Produto, Categoria
    ORDER BY Total_Quantidade ASC
"""

resultado2 = pd.read_sql_query(query2, con)

print("\n" + "=" * 65)
print("  CONSULTA 2 — Produtos que Menos Venderam em Junho/2023")
print("=" * 65)
if resultado2.empty:
    print("  Nenhuma venda registrada em junho de 2023.")
else:
    print(resultado2.to_string(index=False))

con.close()
