import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# 1. Import des données et définition de l'index sur la colonne 'date'
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# 2. Nettoyage des données (exclusion des 2,5 % supérieurs et inférieurs)
df = df[
    (df['value'] >= df['value'].quantile(0.025)) &
    (df['value'] <= df['value'].quantile(0.975))
]


# 3. Graphique linéaire (Line Plot)
def draw_line_plot():
    df_line = df.copy()

    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df_line.index, df_line['value'], color='red', linewidth=1)

    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    # Enregistrement et retour de la figure
    fig.savefig('line_plot.png')
    return fig


# 4. Graphique à barres (Bar Plot)
def draw_bar_plot():
    df_bar = df.copy()

    # Préparation des colonnes d'année et de mois
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.strftime('%B')

    # Regroupement et calcul de la moyenne quotidienne par mois et par année
    df_groupby = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Ordre correct des mois pour la légende
    months_order = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    df_groupby = df_groupby.reindex(columns=months_order)

    # Création du graphique
    fig = df_groupby.plot(kind='bar', figsize=(7, 7)).get_figure()
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    plt.legend(title="Months")

    # Enregistrement et retour de la figure
    fig.savefig('bar_plot.png')
    return fig


# 5. Diagrammes en boîte (Box Plot)
def draw_box_plot():
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Ordre chronologique des mois abrégés
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Création de deux sous-graphiques côte à côte
    fig, axes = plt.subplots(1, 2, figsize=(20, 6))

    # Premier graphique : Par année (Tendance)
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    # Second graphique : Par mois (Saisonnalité)
    sns.boxplot(x='month', y='value', data=df_box, order=month_order, ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    # Enregistrement et retour de la figure
    fig.savefig('box_plot.png')
    return fig