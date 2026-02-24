# 📊 Análise de Dados de Vendas 2023

Projeto de análise exploratória de um dataset simulado de vendas, desenvolvido em Python com pandas, matplotlib e SQLite.

---

## 📁 Estrutura do Projeto

```
projeto/
├── dataset_vendas.csv       # Dataset simulado com 100 registros de vendas
├── main.py                  # Limpeza e tratamento dos dados
├── graficos_vendas.py       # Visualizações e gráficos
├── consultas_sql.py         # Consultas SQL com SQLite
└── relatorio_insights.pdf   # Relatório final com insights


## 📌 O que cada script faz

### `main.py`
- Lê o dataset CSV
- Converte a coluna `Data` para `datetime`
- Converte `Quantidade` para `integer`
- Cria a coluna `Total` (Quantidade × Preço)
- Salva o dataset atualizado

### `graficos_vendas.py`
- Gráfico de linha com tendência de receita mensal
- Gráfico de barras com receita por categoria
- Gráfico de barras com Top 5 produtos mais vendidos
- Exibe os principais insights no terminal

### `consultas_sql.py`
- Carrega o CSV em um banco SQLite em memória
- **Consulta 1:** total de vendas por produto em ordem decrescente
- **Consulta 2:** produtos que menos venderam em junho de 2023

---

## 🔍 Principais Insights

- **Sazonalidade:** julho foi o mês de maior receita (R$ 61.970), enquanto setembro registrou apenas R$ 2.101
- **Categoria dominante:** Eletrônicos representa ~49% da receita total, com o maior ticket médio

---

## 🛠️ Tecnologias Utilizadas

- Python 
- pandas
- matplotlib
- SQLite3
- reportlab
```

---

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais.
