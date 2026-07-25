import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress


def draw_plot():
    # 1. Importation des données depuis epa-sea-level.csv
    df = pd.read_csv('epa-sea-level.csv')

    # 2. Création du nuage de points (Scatter Plot)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(df['Year'], df['CSIRO Adjusted Sea Level'], color='blue', label='Données observées')

    # 3. Première droite de régression (Toutes les données : de 1880 à la fin)
    res_all = linregress(df['Year'], df['CSIRO Adjusted Sea Level'])
    years_extended = pd.Series(range(1880, 2051))
    sea_levels_all = res_all.intercept + res_all.slope * years_extended
    ax.plot(years_extended, sea_levels_all, 'r', label='Tendance globale (1880-2050)')

    # 4. Seconde droite de régression (Données récentes : de 2000 à la fin)
    df_recent = df[df['Year'] >= 2000]
    res_recent = linregress(df_recent['Year'], df_recent['CSIRO Adjusted Sea Level'])
    years_recent = pd.Series(range(2000, 2051))
    sea_levels_recent = res_recent.intercept + res_recent.slope * years_recent
    ax.plot(years_recent, sea_levels_recent, 'green', label='Tendance récente (2000-2050)')

    # 5. Étiquettes des axes, titre et légendes
    ax.set_xlabel('Year')
    ax.set_ylabel('Sea Level (inches)')
    ax.set_title('Rise in Sea Level')

    # 6. Enregistrement et retour de la figure
    plt.savefig('sea_level_plot.png')
    return ax.get_figure()