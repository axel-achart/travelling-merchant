import networkx as nx
from networkx.algorithms.approximation import traveling_salesman_problem
import networkx.algorithms.approximation as nx_app
from map import filtre_data, networkx_map, haversine_distance
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import haversine_distances
import numpy as np


# MST Construire l'arbre couvrant minimum
# IMPAIRS Isoler les sommets de degré impar
# COUPLAGE Apparier ces sommets impairs 2 à 2, optimalement (avec une somme de distance la  plus petite possible)
# CIRCUIT Eulérien puis Hamiltonien (parcourt chaque arête 1 fois, et chaque sommet 1 fois)


db = pd.read_csv("villes_france_lat_long.csv", sep=",")
"""a = filtre_data(db)
b = networkx_map(db)    # Affichage de la map avec arête"""


# Récupération des données et mise en dictionnaire
for _ in range(len(db)):
    villes = list(zip(db['Latitude'], db['Longitude']))
    noms_villes = db['Ville'].tolist()
dict_villes = db.set_index('Ville')[['Latitude', 'Longitude']].T.to_dict('list')
print(f"\nListe de coordonnées : {villes}")
print(f"\nListe des villes initiales : {noms_villes}")
print(f"\nDictionnaire : {dict_villes}")

# Mise en liste juste pour compter en N villes
liste_villes = list(dict_villes.keys())
N = len(liste_villes)

# Création de Matrice en NxN où N est le nombre de ville
matrice_distances = np.zeros((N, N))

# Double boucle pour remplir la matrice de distance
for i in range(N):
    for j in range(i, N):
        if i == j:
            # La distance d'une ville à elle-même = 0
            matrice_distances[i][j] = 0.0
        else:
            ville1 = liste_villes[i]
            ville2 = liste_villes[j]
            
            # Récupération des coordonnées depuis dictionnaire
            lat1, lon1 = dict_villes[ville1]
            lat2, lon2 = dict_villes[ville2]
            
            # Calcul de la distance
            d = haversine_distance(lat1, lon1, lat2, lon2)
            
            # Remplissage symétrique de la matrice
            matrice_distances[i][j] = d
            matrice_distances[j][i] = d

# Affichage du résultat
print("\nMatrice des distances (en km) :")
print(matrice_distances)



"""
# Récupération du graphe
G = nx.Graph()
for i in range(len(villes)):
    for j in range(i+1, len(villes)):
        distance = haversine_distance(*villes[i], *villes[j])   # ici 2 paramètres au lieu de 4 demandés dans la fonction, mais comme y a '*' ça règle
        G[i][j]['weight'] = distance
        G[i][j]['label'] = noms_villes[i]

# Christofides en 1 appel : NetworkX enchaîne MST + Couplage + Eulérien + Hamiltonnien
circuit = traveling_salesman_problem(G, method=nx.approximation.christofides)

# Distance totale du circuit obtenu
total = sum(G[circuit[i]][circuit[i+1]]['weight'] for i in range(len(circuit) - 1))
print(f"\n\nDistance : {total:.2f} km - garantie <= 1,5 x optimum")     # Ca ne depassera pas le pire circuit, il sera bon mais pas le plus optimal possible

print(f"\nLe meilleur circuit (en index) est : {circuit}")

for i in range(len(villes) + 1):
     circuit[i] = noms_villes[circuit[i]]

print(f"\nLe meilleur circuit final est : {circuit}")
print(G)
print(G.nodes)
"""

# Graphique circuit final
# Ajout des villes au graphe
"""
for index, row in db.iterrows():
    G.add_node(row['Ville'], pos=(row['Longitude'], row['Latitude']))
print(G)
for i in range(len(db)):
    for j in range(i + 1, len(db)):
        distance = haversine_distance(db.iloc[i]['Latitude'], db.iloc[i]['Longitude'],
                                    db.iloc[j]['Latitude'], db.iloc[j]['Longitude'])
        G.add_edge(db.iloc[i]['Ville'], db.iloc[j]['Ville'], weight=distance)

pos = nx.get_node_attributes(G, 'pos')
print(pos)
print(G.nodes)

plt.figure(figsize=(12, 7))
nx.draw(G, pos, node_size=50, alpha=0.7, edge_color='gray')
plt.show()
"""

#nouveau graph orienté 
#pos[0] = Paris(0,0)
#for i in range(len(circuit))
#add node 
# [pos=villes[coords[circuit[i]],
# label=villes[noms_villes[circuit[i]]]]
#flèche (arrêt) depuis le node précédent