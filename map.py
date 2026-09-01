from matplotlib.pylab import radians
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
from math import radians, sin, cos, sqrt, atan2


"""
1. Chargement et nettoyage rapide du dataset des villes de France avec leurs coordonnées géographiques (latitude et longitude).
2. Affichage de la carte des villes de France sans distance avec matplotlib.
3. Affichage de la carte des villes de France avec distances calculées à l'aide de la formule de Haversine et NetworkX.
"""


# Chargement du dataset
db = pd.read_csv("villes_france_lat_long.csv", sep=",")

# Description du dataset
print(f"Dimensions du dataset : {db.shape}")
print()
print(f"Colonnes du dataset : \n{db.dtypes}")
print()
print(f"Premières lignes du dataset :\n{db.head()}")

# Nettoyage rapide (suppression des lignes avec des valeurs manquantes)
db = db.dropna()
print(f"\nDimensions du dataset après nettoyage : {db.shape}")
print()

"""
# Fonction affichage carte
def plot_map(df, title="Carte des villes de France"):
    plt.figure(figsize=(10, 7))
    plt.scatter(df['Longitude'], df['Latitude'], alpha=0.5)
    plt.title(title)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid()
    for i, txt in enumerate(df['Ville']):
        plt.text(df['Longitude'].iloc[i] + 0.1, df['Latitude'].iloc[i], txt, fontsize=10)
    plt.show()

# Lancement de l'affichage carte
plot_map(db)
"""


# Fonction affichage carte avec NetworkX
G = nx.Graph()

def haversine_distance(lat1, lon1, lat2, lon2):
    # Rayon de la Terre en kilomètres
    R = 6371.0

    # Conversion des coordonnées en radians
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    # Calcul des différences
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    # Formule de Haversine
    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance


def networkx_map(df):
    # Ajout des villes au graphe
    for index, row in df.iterrows():
        G.add_node(row['Ville'], pos=(row['Longitude'], row['Latitude']))

    # Ajout des arêtes (distances) entre les villes
    for i in range(len(df)):
        for j in range(i + 1, len(df)):
            distance = haversine_distance(df.iloc[i]['Latitude'], df.iloc[i]['Longitude'],
                                          df.iloc[j]['Latitude'], df.iloc[j]['Longitude'])
            G.add_edge(df.iloc[i]['Ville'], df.iloc[j]['Ville'], weight=distance)

    # Récupération des positions des noeuds
    pos = nx.get_node_attributes(G, 'pos')

    # Dessin du graphe
    plt.figure(figsize=(12, 7))
    nx.draw(G, pos, node_size=50, alpha=0.7, edge_color='gray')
    for i, txt in enumerate(df['Ville']):
            plt.text(df['Longitude'].iloc[i] + 0.1, df['Latitude'].iloc[i], txt, fontsize=10)
    plt.title("Carte des villes de France avec NetworkX")
    plt.show()


# Lancement de l'affichage carte NetworkX
networkx_map(db)