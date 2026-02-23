import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# Carregamento e limpeza 
dados = pd.read_csv("dataset_vendas.csv", sep=";")
dados["Data"]       = pd.to_datetime(dados["Data"], format="mixed")
dados               = dados.dropna(subset=["Quantidade"])
dados["Quantidade"] = dados["Quantidade"].astype(int)
dados["Total"]      = (dados["Quantidade"] * dados["Preço (R$)"]).round(2)
dados["Mês"]        = dados["Data"].dt.month
dados["Mês_Nome"]   = dados["Data"].dt.strftime("%b")

# Agregações 
vendas_mes      = dados.groupby("Mês").agg(
                      Receita=("Total", "sum"),
                      Quantidade=("Quantidade", "sum")
                  ).reset_index()
meses_label     = ["Jan","Fev","Mar","Abr","Mai","Jun",
                   "Jul","Ago","Set","Out","Nov","Dez"]
vendas_mes["Mês_Nome"] = vendas_mes["Mês"].apply(lambda x: meses_label[x-1])

receita_cat     = dados.groupby("Categoria")["Total"].sum().sort_values(ascending=False)
top5_produtos   = dados.groupby("Produto")["Quantidade"].sum().sort_values(ascending=False).head(5)

COR_LINHA   = "#1F4E79"
COR_AREA    = "#D6E4F0"
COR_BARRAS  = ["#1F4E79","#2E75B6","#4BACC6","#70AD47","#ED7D31"]
COR_PIZZA   = ["#1F4E79","#2E75B6","#4BACC6","#70AD47","#ED7D31"]

fig = plt.figure(figsize=(16, 14))
fig.suptitle("Análise Exploratória de Vendas 2023", fontsize=18, fontweight="bold", y=0.98)

#  Gráfico 1 — Tendência de Receita Mensal  
ax1 = fig.add_subplot(2, 2, (1, 2))
ax1.fill_between(vendas_mes["Mês_Nome"], vendas_mes["Receita"], alpha=0.25, color=COR_AREA)
ax1.plot(vendas_mes["Mês_Nome"], vendas_mes["Receita"],
         marker="o", linewidth=2.5, color=COR_LINHA, markersize=7)

for _, row in vendas_mes.iterrows():
    ax1.annotate(f'R$ {row["Receita"]:,.0f}',
                 xy=(row["Mês_Nome"], row["Receita"]),
                 xytext=(0, 10), textcoords="offset points",
                 ha="center", fontsize=7.5, color=COR_LINHA)

ax1.set_title("Tendência de Receita Mensal", fontsize=13, fontweight="bold", pad=12)
ax1.set_xlabel("Mês", fontsize=10)
ax1.set_ylabel("Receita (R$)", fontsize=10)
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"R$ {x:,.0f}"))
ax1.set_xticks(range(len(vendas_mes)))
ax1.set_xticklabels(vendas_mes["Mês_Nome"])
ax1.grid(axis="y", linestyle="--", alpha=0.5)
ax1.spines[["top","right"]].set_visible(False)

# Gráfico 2 — Receita por Categoria (barras horizontais) 
ax2 = fig.add_subplot(2, 2, 3)
bars = ax2.barh(receita_cat.index, receita_cat.values, color=COR_PIZZA, edgecolor="white")
ax2.set_title("Receita Total por Categoria", fontsize=13, fontweight="bold", pad=12)
ax2.set_xlabel("Receita (R$)", fontsize=10)
ax2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"R$ {x:,.0f}"))
ax2.spines[["top","right"]].set_visible(False)
ax2.grid(axis="x", linestyle="--", alpha=0.5)
for bar, val in zip(bars, receita_cat.values):
    ax2.text(val + 500, bar.get_y() + bar.get_height()/2,
             f"R$ {val:,.0f}", va="center", fontsize=8, color=COR_LINHA)

# Top 5 Produtos mais vendidos 
ax3 = fig.add_subplot(2, 2, 4)
bars3 = ax3.bar(top5_produtos.index, top5_produtos.values, color=COR_BARRAS, edgecolor="white")
ax3.set_title("Top 5 Produtos Mais Vendidos", fontsize=13, fontweight="bold", pad=12)
ax3.set_ylabel("Quantidade Vendida", fontsize=10)
ax3.set_xticklabels(top5_produtos.index, rotation=15, ha="right", fontsize=8)
ax3.spines[["top","right"]].set_visible(False)
ax3.grid(axis="y", linestyle="--", alpha=0.5)
for bar, val in zip(bars3, top5_produtos.values):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
             str(val), ha="center", fontsize=9, fontweight="bold", color=COR_LINHA)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("graficos_vendas.png", dpi=150, bbox_inches="tight")
plt.show()
print("Gráfico salvo em graficos_vendas.png")

#  Insights no terminal 
print("\n" + "="*55)
print("          INSIGHTS DA ANÁLISE DE VENDAS 2023")
print("="*55)

melhor_mes = vendas_mes.loc[vendas_mes["Receita"].idxmax()]
pior_mes   = vendas_mes.loc[vendas_mes["Receita"].idxmin()]
print(f"\nInsight 1 — Sazonalidade nas vendas:")
print(f"   Melhor mês : {melhor_mes['Mês_Nome']} → R$ {melhor_mes['Receita']:,.2f}")
print(f"   Pior mês   : {pior_mes['Mês_Nome']}  → R$ {pior_mes['Receita']:,.2f}")
print(f"   Diferença  : R$ {melhor_mes['Receita'] - pior_mes['Receita']:,.2f}")

top_cat = receita_cat.index[0]
top_cat_pct = (receita_cat.iloc[0] / receita_cat.sum()) * 100
print(f"\nInsight 2 — Concentração de receita por categoria:")
print(f"   '{top_cat}' lidera com R$ {receita_cat.iloc[0]:,.2f}")
print(f"   Representa {top_cat_pct:.1f}% da receita total")

print(f"\nProduto mais vendido: {top5_produtos.index[0]} ({top5_produtos.iloc[0]} unidades)")
print("="*55)
