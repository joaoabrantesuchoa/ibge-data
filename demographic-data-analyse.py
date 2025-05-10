import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from math import pi

# Configurar estilo de gráficos
plt.style.use('ggplot')
colors = ['#2ecc71', '#3498db', '#9b59b6']
sns.set_palette(sns.color_palette(colors))

# Função para limpar valores numéricos
def clean_numeric(value):
    if isinstance(value, str):
        return float(value.split()[0].replace('.', '').replace(',', '.'))
    return value

def load_and_clean_data(filepath, numeric_cols, decimal=',', thousands='.', encoding='utf-8'):
    df = pd.read_csv(filepath, decimal=decimal, thousands=thousands, encoding=encoding)
    for col in numeric_cols:
        df[col] = df[col].apply(clean_numeric)

    if 'Hierarquia urbana' in df.columns:
        df['Hierarquia urbana'] = df['Hierarquia urbana'].str.split(' - ').str[0]
    
    return df

# Função para gerar gráficos de barras comparativos
def plot_comparative_bars(df, cidades_alvo, indicadores, municipio_col='Municípios'):
    df_filtrado = df[df[municipio_col].isin(cidades_alvo)]
    plt.figure(figsize=(14, 8))
    for i, indicador in enumerate(indicadores, 1):
        plt.subplot(2, 2, i)
        barplot = sns.barplot(
            x=municipio_col, y=indicador, data=df_filtrado, hue=municipio_col, palette='Set2', dodge=False
        )
        plt.title(indicador.split('(')[0].strip())
        plt.xticks(rotation=45)
        for container in barplot.containers:
            barplot.bar_label(container, fmt='%.3f')
    plt.tight_layout()
    plt.show()

def plot_scatter_density_vs_area(df, x_col, y_col, category_col, highlight_cities=None):
    plt.figure(figsize=(14, 10))
    scatter = sns.scatterplot(
        data=df,
        x=x_col,
        y=y_col,
        hue=category_col,
        palette='Set2',
        s=100,
        alpha=0.8
    )
    plt.title(f'{y_col} vs {x_col} categorizado por {category_col}', fontsize=14)
    plt.xlabel(f'{x_col}', fontsize=12)
    plt.ylabel(f'{y_col} Km²', fontsize=12)

    plt.legend(title=category_col, bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=3)

    # Adicionar nomes das cidades destacadas
    if highlight_cities:
        for _, row in df[df['Municípios'].isin(highlight_cities)].iterrows():
            plt.text(
                row[x_col],
                row[y_col],
                row['Municípios'],
                fontsize=10,
                weight='bold',
                color='black'
            )

    plt.xscale('log')
    plt.tight_layout()
    plt.show()

# Exemplo de uso
if __name__ == "__main__":
    # Configurações iniciais
    numeric_cols = [
        'Índice de Desenvolvimento Humano Municipal (IDHM)',
        'PIB per capita',
        'População no último censo',
        'Densidade demográfica',
        'Área urbanizada',
        'Urbanização de vias públicas',
        'Arborização de vias públicas'
    ]

    comparative_bar_cols = [
        'Índice de Desenvolvimento Humano Municipal (IDHM)',
        'PIB per capita',
        'Densidade demográfica',
        'Área urbanizada',
        'Urbanização de vias públicas',
        'Arborização de vias públicas'
    ]

    cidades_alvo = ['Fortaleza', 'Quixadá', 'Caucaia']

    # Carregar e limpar os dados
    df = load_and_clean_data('data-ceara.csv', numeric_cols)

    # Filtrar cidades-alvo
    df_filtrado = df[df['Municípios'].isin(cidades_alvo)]

    # Análise das trés cidades alvo
    plot_comparative_bars(df, cidades_alvo, comparative_bar_cols[:4])

    # Análise comparativa das cidades alvo com o resto do estado
    plot_scatter_density_vs_area(
    df,
    x_col='Densidade demográfica',
    y_col='Área urbanizada',
    category_col='Mesorregião',
    highlight_cities=['Fortaleza', 'Quixadá', 'Caucaia']
)
    
    plot_scatter_density_vs_area(
    df,
    x_col='Densidade demográfica',
    y_col='Área urbanizada',
    category_col='Hierarquia urbana',
    highlight_cities=['Fortaleza', 'Quixadá', 'Caucaia']
)
