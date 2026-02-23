import pandas as pd

dados = pd.read_csv("dataset_vendas.csv", sep=";")

# Converter a coluna DATA de object para um tipo DATETIME
dados["Data"] = pd.to_datetime(dados["Data"], format="%Y-%m-%d")
# Remove linhas com NaN antes de converter
dados = dados.dropna(subset=["Quantidade"])

# Converter a coluna QUANTIDADE para um tipo INTEGER
dados["Quantidade"] = dados["Quantidade"].astype(int)


# Criar coluna 'TOTAL', calculando quantidade * preco
dados['Total'] = dados['Quantidade'] * dados['Preço (R$)']

# Converte a coluna total para duas casas decimais
dados['Total'] = dados['Total'].round(2)

#dados.to_csv("dataset_vendas.csv", sep=";", index=False, encoding="utf-8-sig")

# Produto com maior número de vendas totais
maior_venda = dados.groupby("Produto")["Quantidade"].sum().idxmax()
quantidade  = dados.groupby("Produto")["Quantidade"].sum().max()

print(f"Produto mais vendido: {maior_venda} com {quantidade} unidades vendidas")

