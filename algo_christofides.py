import networkx as nx
from networkx.algorithms.approximation import traveling_salesman_problem
from map import filtre_data, networkx_map, haversine_distance
import pandas as pd

# MST Construire l'arbre couvrant minimum
# IMPAIRS Isoler les sommets de degré impar
# COUPLAGE Apparier ces sommets impairs 2 à 2, optimalement (avec une somme de distance la  plus petite possible)
# CIRCUIT Eulérien puis Hamiltonien (parcourt chaque arête 1 fois, et chaque sommet 1 fois)

db = pd.read_csv("villes_france_lat_long.csv", sep=",")
a = filtre_data(db)
b = networkx_map(db)    # Affichage de la map avec arête

# 1 Récupération des données
for _ in range(len(db)):
    villes = list(zip(db['Latitude'], db['Longitude']))
    noms_villes = db['Ville'].tolist()


# 2 Récupération du graphe
G = nx.complete_graph(len(villes))
for i in range(len(villes)):
    for j in range(i+1, len(villes)):
        distance = haversine_distance(*villes[i], *villes[j])   # ici 2 paramètres au lieu de 4 demandés dans la fonction, mais comme y a '*' ça règle
        G[i][j]['weight'] = distance

# 3 Christofides en 1 appel : NetworkX enchaîne MST + Couplage + Eulérien + Hamiltonnien
circuit = traveling_salesman_problem(G, method=nx.approximation.christofides)

#4 Distance totale du circuit obtenu
total = sum(G[circuit[i]][circuit[i+1]]['weight'] for i in range(len(circuit) - 1))
print(f"Distance : {total:.2f} km - garantie <= 1,5 x optimum")     # Ca ne depassera pas le pire circuit, il sera bon mais pas le plus optimal possible