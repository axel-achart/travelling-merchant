import networkx as nx
from networkx.algorithms.approximation import traveling_salesman_problem
import map

# MST Construire l'arbre couvrant minimum
# IMPAIRS Isoler les sommets de degré impar
# COUPLAGE Apparier ces sommets impairs 2 à 2, optimalement (avec une somme de distance la  plus petite possible)
# CIRCUIT Eulérien puis Hamiltonien (parcourt chaque arête 1 fois, et chaque sommet 1 fois)


# 1 Récupération du graphe
G = nx.complete_graph(len(villes))