import pandas as pd
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# 1. Import du fichier CSV /les colonnes : Ville, Latitude, Longitude.
# ---------------------------------------------------------------------------
df = pd.read_csv('villes_france_lat_long.csv')

# ---------------------------------------------------------------------------
# 2. Fonction haversine : calcul de la distance réelle entre deux points
#    sur la Terre à partir de leurs coordonnées (latitude, longitude).
# ---------------------------------------------------------------------------
def haversine(lat1, lon1, lat2, lon2):
    """ Calcule la distance entre deux points sur la surface de la Terre
        en utilisant la formule de Haversine.
        - Entrées : latitude et longitude en degrés
        - Sortie : distance en kilomètres. """
    R = 6371  # Rayon de la Terre 
    # Conversion des écarts de latitude/longitude de degrés en radians.
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    # Formule de Haversine : a = sin²(dlat/2) + cos(lat1)·cos(lat2)·sin²(dlon/2)
    a = np.sin(dlat / 2) ** 2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon / 2) ** 2
    # c = angle central entre les deux points (en radians).
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    # La distance = angle central × rayon terrestre.
    return R * c

# ---------------------------------------------------------------------------
# 3. Création du graphe vide G.
#    - Un "sommet" (nœud) représentera une VILLE.
#    - Une "arête" représentera un trajet entre deux villes,
#      pondéré par la distance en km.
# ---------------------------------------------------------------------------
G = nx.Graph()

# ---------------------------------------------------------------------------
# 4. Fonction CreateGraphFromCSV : remplit le graphe G à partir du CSV.
# ---------------------------------------------------------------------------
def CreateGraphFromCSV():
    """ Crée un graphe à partir du fichier CSV.
        - Chaque ville devient un nœud, avec sa position (longitude, latitude).
        - Chaque paire de villes est reliée par une arête dont le poids
          est la distance de Haversine entre les deux villes. """

    # 4a. Ajout des SOMMETS : une ville = un nœud.
    #     On stocke sa position dans l'attribut 'pos' (pour l'affichage).
    for _, row in df.iterrows():
        G.add_node(row['Ville'], pos=(row['Longitude'], row['Latitude']))

    # 4b. Ajout des ARÊTES : on relie CHAQUE paire de villes entre elles.
    #     Le graphe final est donc COMPLET (toutes les villes sont connectées).
    villes = df['Ville'].tolist()
    for i in range(len(villes)):
        # On commence j à i+1 pour ne traiter chaque paire QU'UNE seule fois
        # (pas de doublon (A,B) et (B,A)).
        for j in range(i + 1, len(villes)):
            vi, vj = villes[i], villes[j]

            # Récupération des coordonnées (lat, lon) des deux villes.
            lat1, lon1 = df.loc[df['Ville'] == vi, ['Latitude', 'Longitude']].values[0]
            lat2, lon2 = df.loc[df['Ville'] == vj, ['Latitude', 'Longitude']].values[0]

            # Distance réelle entre les deux villes.
            distance = haversine(lat1, lon1, lat2, lon2)

            # Création de l'arête avec son poids (la distance en km).
            G.add_edge(vi, vj, weight=distance)

# ---------------------------------------------------------------------------
# 5. Appel de la fonction : le graphe G est construit.
# ---------------------------------------------------------------------------
CreateGraphFromCSV()

# ---------------------------------------------------------------------------
#    Il affiche toutes les villes et toutes les routes.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Récupère la position (longitude, latitude) de chaque ville.
    pos = nx.get_node_attributes(G, 'pos')
    # Dessine le graphe complet : toutes les villes et toutes les routes.
    nx.draw(G, pos, with_labels=True, node_size=50, font_size=8)
    plt.show()


 
    


  
        



    