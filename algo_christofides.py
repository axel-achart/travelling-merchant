#Résolution avec l'Algorithme de Christofides :
# Implémentez l'algorithme de Christofides pour trouver l’itinéraire
# le plus court pour Théobald.
# Quelle est la distance totale de votre solution presque optimale ?
# Affichez l'itinéraire sur la carte du marchand.
#  Expliquez les étapes de l'algorithme, et justifiez pourquoi cet
# algorithme est pertinent dans ce contexte.
#----------------------------------------------------------------------------------------------------------------
from map import G
import networkx as nx


def sommets_degre_impair(arbre):
    """ Renvoie une liste des sommets de degré impair dans le graphe arbre. """
    return [v for v, d in arbre.degree() if d % 2 == 1]


def main():
    # 1. Construire un arbre couvrant minimal (MST) à partir du graphe complet.
    T = nx.minimum_spanning_tree(G, weight='weight')

    # 2. Trouver les sommets de degré impair dans le MST.
    sommets_impairs = sommets_degre_impair(T)

    # 3. Trouver un appariement parfait minimum pour ces sommets de degré impair.

    # 3a. Construire un sous-graphe avec les sommets de degré impair.
    G_impair = G.subgraph(sommets_impairs)

    # 3b. Trouver un appariement parfait de poids minimum.
    matching = nx.min_weight_matching(G_impair, weight='weight')

    # 3c. Ajouter les arêtes de l'appariement parfait au MST pour obtenir un graphe eulérien.

    # On crée un multigraphe : il peut contenir PLUSIEURS arêtes entre deux mêmes sommets.
    # C'est indispensable car l'appariement peut relier deux sommets déjà reliés dans le MST,
    # créant ainsi deux arêtes "parallèles" entre eux.
    G_eulerien = nx.MultiGraph()

    # On copie d'abord tous les nœuds du MST dans le multigraphe.
    G_eulerien.add_nodes_from(T.nodes(data=True))

    # Puis on copie toutes les arêtes du MST (avec leur poids 'weight').
    G_eulerien.add_edges_from(T.edges(data=True))

    # On ajoute maintenant les arêtes de l'appariement parfait.
    for u, v in matching:
        poids = G[u][v]['weight']          # Distance entre u et v dans le graphe d'origine
        G_eulerien.add_edge(u, v, weight=poids)

    # Vérification : tous les sommets doivent maintenant avoir un degré PAIR.
    # C'est la condition nécessaire pour qu'un circuit eulérien existe.
    degres_pairs = all(d % 2 == 0 for _, d in G_eulerien.degree())
    print("Tous les sommets ont un degré pair ?", degres_pairs)

    # 4. Circuit Eulérien puis Hamiltonien : chaque arête 1 fois, puis chaque sommet 1 fois.

    # 4a. Circuit eulérien : nx.eulerian_circuit renvoie la liste des arêtes (u, v)
    #     du parcours qui traverse CHAQUE arête exactement une fois.
    circuit_eulerien = list(nx.eulerian_circuit(G_eulerien))

    # On transforme la liste d'arêtes en liste de villes.
    # Le circuit eulérien est une suite d'arêtes (a, b), (b, c), ..., (z, a) :
    # en prenant la première extrémité de chaque arête puis la seconde extrémité
    # de la dernière, on obtient a -> b -> c -> ... -> a (boucle fermée).
    circuit = [arete[0] for arete in circuit_eulerien] + [circuit_eulerien[-1][1]]

    # 4b. Circuit hamiltonien : on parcourt le circuit eulérien et on SAUTE
    #     toute ville déjà visitée. Chaque ville n'apparaît qu'une fois.
    itineraire = []
    villes_visitees = set()

    for ville in circuit:
        if ville not in villes_visitees:
            itineraire.append(ville)          # On garde la ville seulement si inédite
            villes_visitees.add(ville)

    # On referme la boucle en revenant à la ville de départ.
    itineraire.append(itineraire[0])

    # 5. Distance totale + affichage de l'itinéraire sur la carte.

    # 5a. Calcul de la distance totale de l'itinéraire.
    distance_totale = 0
    for i in range(len(itineraire) - 1):
        u, v = itineraire[i], itineraire[i + 1]
        distance_totale += G[u][v]['weight']    # On additionne le poids de chaque étape

    print("\nItinéraire de Théobald :")
    print(" -> ".join(itineraire))
    print(f"\nDistance totale (approximation de Christofides) : {distance_totale:.2f} km")

    # 5b. Affichage de l'itinéraire sur la carte du marchand.
    import matplotlib.pyplot as plt

    # Positions des villes (longitude, latitude) stockées dans le graphe.
    pos = nx.get_node_attributes(G, 'pos')

    # On trace d'abord TOUTES les villes et toutes les routes (fond de carte).
    nx.draw(G, pos, with_labels=True, node_size=50, font_size=8,
            edge_color='lightgray', node_color='skyblue')

    # On superpose l'itinéraire trouvé en rouge, plus épais, pour le mettre en valeur.
    aretes_itineraire = [(itineraire[i], itineraire[i + 1])
                         for i in range(len(itineraire) - 1)]
    nx.draw_networkx_edges(G, pos, edgelist=aretes_itineraire,
                           edge_color='red', width=2)

    plt.title(f"Tournée du marchand — {distance_totale:.2f} km")
    plt.show()


if __name__ == "__main__":
    main()


