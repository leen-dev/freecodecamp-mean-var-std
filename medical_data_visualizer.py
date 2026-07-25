import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1. Import des données depuis le fichier CSV
df = pd.read_csv('medical_examination.csv')

# 2. Ajout de la colonne 'overweight' (IMC = poids (kg) / (taille (m))^2)
# Si IMC > 25 -> 1 (surpoids), sinon 0
bmi = df['weight'] / ((df['height'] / 100) ** 2)
df['overweight'] = (bmi > 25).astype(int)

# 3. Normalisation des données pour 'cholesterol' et 'gluc'
# Si la valeur est 1 (normal) -> 0, si la valeur est > 1 -> 1
df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
df['gluc'] = (df['gluc'] > 1).astype(int)


# 4. Fonction pour tracer le graphique catégoriel
def draw_cat_plot():
    # 5. Création du DataFrame fondu (melted) pour le graphique
    df_cat = pd.melt(
        df,
        id_vars=['cardio'],
        value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight']
    )

    # 6. Regroupement et comptage des occurrences par catégorie
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name='total')

    # 7. Création du graphique catégoriel avec sns.catplot
    g = sns.catplot(
        x='variable',
        y='total',
        hue='value',
        col='cardio',
        data=df_cat,
        kind='bar'
    )

    # 8. Récupération de la figure
    fig = g.fig

    # 9. Ne pas modifier les lignes suivantes
    fig.savefig('catplot.png')
    return fig


# 10. Fonction pour tracer la carte thermique (Heatmap)
def draw_heat_map():
    # 11. Nettoyage des données
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]

    # 12. Calcul de la matrice de corrélation
    corr = df_heat.corr()

    # 13. Génération du masque pour le triangle supérieur
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # 14. Configuration de la figure Matplotlib
    fig, ax = plt.subplots(figsize=(12, 12))

    # 15. Affichage de la Heatmap avec Seaborn
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt='.1f',
        square=True,
        linewidths=0.5,
        cbar_kws={'shrink': 0.5},
        ax=ax
    )

    # 16. Ne pas modifier les lignes suivantes
    fig.savefig('heatmap.png')
    return fig