from networkx.algorithms.approximation import traveling_salesman_problem
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from map import haversine_distance
import numpy as np

db = pd.read_csv("villes_france_lat_long.csv", sep=',')

print(db)

for _ in range(len(db)):
    villes=list(zip(db['Latitude'], db["Longitude"]))
    noms_villes=db['Ville'].tolist()
dict_villes=db.set_index('Ville')[['Latitude','Longitude']].T.to_dict('list')
print(f"\nDictionnaire : {dict_villes}")
G = nx.Graph()

for ville, (lat, lon) in dict_villes.items():
    G.add_node(ville, pos=(lon,lat))

for i in range(len(noms_villes)):
    for j in range(i+1, len(noms_villes)):
        c1 = noms_villes[i]
        c2 = noms_villes[j]
        d = haversine_distance(
            dict_villes[c1][0], dict_villes[c1][1],
            dict_villes[c2][0],dict_villes[c2][1]
        )
        G.add_edge(c1,c2,weight=d)


pos = nx.get_node_attributes(G,'pos')
circuit = traveling_salesman_problem(G, method=nx.approximation.christofides)
print(circuit)
plt.figure(figsize=(12,7))
nx.draw(
    G,
    pos,
    with_labels=True,
    node_size=50,
    edge_color="gray",
    width=1
)
plt.show()

print(G)

H = nx.DiGraph()
H.add_nodes_from(G)
for i in range(len(circuit)-1):
    c1 = circuit[i]
    c2 = circuit[i+1]
    d = haversine_distance(
        dict_villes[c1][0], dict_villes[c1][1],
        dict_villes[c2][0],dict_villes[c2][1]
    )
    H.add_edge(c1,c2,weight=d)
    print(H)
print(H)


pos = nx.get_node_attributes(G,'pos')

plt.figure(figsize=(12,7))
nx.draw(
    H,
    pos,
    with_labels=True,
    node_size=50,
    edge_color="gray",
    width=1
)
plt.show()