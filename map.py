import pandas as pd
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('villes_france_lat_long.csv')#colonnes: Ville, Latitude, Longitude
print(df.head())

def haversine(lat1, lon1, lat2, lon2):
    """ Calcule la distance entre deux points sur la surface de la Terre en utilisant la formule de Haversine. Les coordonnées doivent être fournies en degrés. La distance est renvoyée en kilomètres. """
    R = 6371  # Rayon de la Terre en kilomètres
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = np.sin(dlat / 2) ** 2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c

G= nx.Graph()

#Sommets : villes
def CreateGraphFromCSV():
    """ Crée un graphe à partir d'un fichier csv contenant les colonnes 'Ville', 'Latitude' et 'Longitude'. Chaque ville est ajoutée comme un nœud du graphe, et les arêtes sont créées entre chaque paire de villes avec la distance euclidienne comme poids. """
    for _, row in df.iterrows():
        G.add_node(row['Ville'], pos=(row['Longitude'], row['Latitude']))

# Arêtes : distances entre les villes

    villes = df['Ville'].tolist()
    for i in range(len(villes)):
        for j in range(i + 1, len(villes)):
            vi, vj = villes[i], villes[j]
            lat1, lon1 = df.loc[df['Ville'] == vi, ['Latitude', 'Longitude']].values[0]
            lat2, lon2 = df.loc[df['Ville'] == vj, ['Latitude', 'Longitude']].values[0]
            distance = haversine(lat1, lon1, lat2, lon2)
            G.add_edge(vi, vj, weight=distance)

CreateGraphFromCSV()
pos = nx.get_node_attributes(G, 'pos')
nx.draw(G, pos, with_labels=True, node_size=50, font_size=8)
plt.show()

 
    


  
        



    