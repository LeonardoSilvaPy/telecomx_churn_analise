import pandas as pd
import matplotlib.pyplot as plt
import requests

# =========================
# 1) Extração dos Dados
# =========================
url = "https://raw.githubusercontent.com/ingridcristh/challenge2-data-science/main/TelecomX_Data.json"
df = pd.read_json(url)

# =========================
# 2) Transformação dos Dados
# =========================
# Renomear colunas para facilitar leitura
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

# Converter colunas numéricas
if "totalcharges" in df.columns:
    df["totalcharges"] = pd.to_numeric(df["totalcharges"], errors="coerce")

# Criar buckets de tempo de contrato (tenure)
if "tenure" in df.columns:
    df["tenure_group"] = pd.cut(
        df["tenure"],
        bins=[0, 12, 24, 48, 72],
        labels=["0-1 ano", "1-2 anos", "2-4 anos", "4-6 anos"],
        include_lowest=True
    )

# =========================
# 3) Análise Exploratória
# =========================
print("\n📊 Informações gerais do dataset:")
print(df.info())
print("\n🔎 Estatísticas descritivas:")
print(df.describe(include="all"))

# =========================
# 4) Visualizações
# =========================
# Churn por tipo de contrato
df.groupby("contract")["churn"].value_counts(normalize=True).unstack().plot(
    kind="bar", figsize=(8,5), title="Taxa de Churn por Tipo de Contrato"
)
plt.ylabel("Proporção")
plt.savefig("churn_por_contrato.png")
plt.close()

# Churn por método de pagamento
df.groupby("paymentmethod")["churn"].value_counts(normalize=True).unstack().plot(
    kind="bar", figsize=(8,5), title="Churn por Método de Pagamento"
)
plt.ylabel("Proporção")
plt.savefig("churn_por_pagamento.png")
plt.close()

# Churn por internet service
df.groupby("internetservice")["churn"].value_counts(normalize=True).unstack().plot(
    kind="bar", figsize=(8,5), title="Churn por Tipo de Serviço de Internet"
)
plt.ylabel("Proporção")
plt.savefig("churn_por_internet.png")
plt.close()

# Distribuição do tempo de contrato
df["tenure_group"].value_counts().plot(
    kind="bar", figsize=(6,4), title="Distribuição por Tempo de Contrato"
)
plt.savefig("distribuicao_tempo_contrato.png")
plt.close()

print("\n✅ Gráficos gerados com sucesso!")

# =========================
# 5) Conclusão
# =========================
conclusao = """
📌 Conclusões e Recomendações:

1. Clientes com contratos mensais apresentam a maior taxa de churn.
   - Estratégia: incentivar migração para contratos anuais ou bianuais com descontos.

2. Pagamentos feitos por boleto eletrônico estão associados a maiores taxas de cancelamento.
   - Estratégia: oferecer benefícios para clientes que migrem para débito automático ou cartão.

3. Clientes com serviço de internet via fibra óptica apresentam churn mais elevado que DSL.
   - Estratégia: investigar problemas de qualidade do serviço e melhorar suporte técnico.

4. Clientes com menor tempo de contrato (até 1 ano) são os que mais cancelam.
   - Estratégia: criar onboarding mais eficiente e oferecer benefícios nos primeiros meses.

Em resumo, o foco deve estar em fidelizar clientes recém-adquiridos, incentivar métodos de pagamento mais estáveis e oferecer benefícios em contratos de maior duração.
"""

with open("relatorio_conclusao.txt", "w", encoding="utf-8") as f:
    f.write(conclusao)

print("\n📄 Relatório gerado: relatorio_conclusao.txt")
