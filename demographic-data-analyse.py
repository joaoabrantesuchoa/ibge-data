import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from math import pi

# Função para limpar valores numéricos
def clean_numeric(value):
    if isinstance(value, str):
        return float(value.split()[0].replace('.', '').replace(',', '.'))
    return value

# Carregar e processar os dados
df = pd.read_csv('data-ceara.csv', 
                 decimal=',', 
                 thousands='.', 
                 encoding='utf-8')

# Lista de colunas numéricas para limpeza
numeric_cols = [
    'Índice de Desenvolvimento Humano Municipal (IDHM)',
    'PIB per capita',
    'População no último censo',
    'Densidade demográfica',
    'Área urbanizada',
    'Urbanização de vias públicas',
    'Arborização de vias públicas'
]

# Aplicar limpeza nas colunas numéricas
for col in numeric_cols:
    df[col] = df[col].apply(clean_numeric)

# Configurações de estilo
plt.style.use('ggplot')
colors = ['#2ecc71', '#3498db', '#9b59b6']
sns.set_palette(sns.color_palette(colors))

# Análise 1: Comparativo entre as cidades selecionadas
cidades_alvo = ['Fortaleza', 'Quixadá', 'Caucaia']
df_filtrado = df[df['Municípios'].isin(cidades_alvo)]

# Gráfico de Barras Comparativo
indicadores = [
    'Índice de Desenvolvimento Humano Municipal (IDHM)',
    'PIB per capita',
    'Densidade demográfica',
    'População no último censo'
]

plt.figure(figsize=(14, 8))
for i, indicador in enumerate(indicadores, 1):
    plt.subplot(2, 2, i)
    barplot = sns.barplot(x='Municípios', y=indicador, data=df_filtrado)
    plt.title(indicador.split('(')[0].strip())
    plt.xticks(rotation=45)
    barplot.bar_label(barplot.containers[0], fmt='%.3f')
plt.tight_layout()
plt.show()

# Análise 2: Radar Chart Multidimensional
categories = [
    'IDHM',
    'PIB per capita', 
    'Densidade demográfica',
    'Área urbanizada',
    'Urbanização de vias públicas'
]

# Preparar dados para o radar chart
angles = [n / len(categories) * 2 * pi for n in range(len(categories))]
angles += angles[:1]

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, polar=True)
plt.xticks(angles[:-1], categories, color='grey', size=12)

# Plotar cada cidade
for idx, cidade in enumerate(df_filtrado['Municípios']):
    valores = df_filtrado[df_filtrado['Municípios'] == cidade][[
        'Índice de Desenvolvimento Humano Municipal (IDHM)',
        'PIB per capita',
        'Densidade demográfica',
        'Área urbanizada',
        'Urbanização de vias públicas'
    ]].values.flatten().tolist()
    
    valores += valores[:1]
    ax.plot(angles, valores, linewidth=2, linestyle='solid', label=cidade)
    ax.fill(angles, valores, alpha=0.25)

plt.title('Comparação Multidimensional das Cidades', size=15, y=1.1)
plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
plt.show()

# Análise 3: Distribuição com Destaque para Cidades Selecionadas
plt.figure(figsize=(14, 6))
for i, var in enumerate(['PIB per capita', 'Densidade demográfica'], 1):
    plt.subplot(1, 2, i)
    
    # Boxplot para toda a distribuição
    sns.boxplot(x=var, data=df, color='#bdc3c7', width=0.4)
    
    # Swarmplot para as cidades destacadas
    sns.swarmplot(x=var, data=df_filtrado, size=8, edgecolor='black', linewidth=1)
    
    plt.title(f'Distribuição de {var}')
    plt.xlabel('')
plt.tight_layout()
plt.show()

# Análise 4: Relação IDHM vs PIB per capita
plt.figure(figsize=(12, 8))
scatter = sns.scatterplot(
    x='Índice de Desenvolvimento Humano Municipal (IDHM)',
    y='PIB per capita',
    size='População no último censo',
    hue='Mesorregião',
    data=df,
    palette='Set2',
    sizes=(30, 400),
    alpha=0.8
)

# Destacar as cidades-alvo
for _, row in df_filtrado.iterrows():
    scatter.text(
        x=row['Índice de Desenvolvimento Humano Municipal (IDHM)'] + 0.005,
        y=row['PIB per capita'] + 500,
        s=row['Municípios'],
        fontsize=10,
        color='black',
        ha='left',
        va='center'
    )

plt.title('Relação entre Desenvolvimento Humano e Riqueza Municipal', size=14)
plt.xlabel('Índice de Desenvolvimento Humano (IDHM)', size=12)
plt.ylabel('PIB per capita (R$)', size=12)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()