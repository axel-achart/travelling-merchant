from map import G
import networkx as nx


def distance(cycle, graphe):
    """ Somme des poids le long d'un cycle, en refermant la boucle si besoin. """
    total = 0
    for i in range(len(cycle) - 1):
        total += graphe[cycle[i]][cycle[i + 1]]['weight']
    # Si le cycle ne revient pas déjà au point de départ, on ajoute l'arête de retour.
    if cycle[0] != cycle[-1]:
        total += graphe[cycle[-1]][cycle[0]]['weight']
    return total


def main():
    # --- 1. Christofides en une seule ligne ------------------------------------------------
    # nx.approximation.christofides fait exactement les 5 étapes de l'algorithme :
    # MST -> sommets impairs -> couplage parfait -> circuit eulérien -> raccourcis.
    tournee = nx.approximation.christofides(G, weight='weight')
    dist = distance(tournee, G)

    print("Itinéraire de Théobald (Christofides NetworkX) :")
    print(" -> ".join(tournee))
    print(f"\nDistance totale : {dist:.2f} km")

    # --- 2. Affichage de l'itinéraire sur la carte -----------------------------------------
    import matplotlib.pyplot as plt

    # Positions des villes (longitude, latitude) stockées dans le graphe.
    pos = nx.get_node_attributes(G, 'pos')

    # Fond de carte : toutes les villes et toutes les routes possibles.
    nx.draw(G, pos, with_labels=True, node_size=50, font_size=8,
            edge_color='lightgray', node_color='skyblue')

    # On met en rouge les arêtes de la tournée trouvée.
    aretes = [(tournee[i], tournee[i + 1]) for i in range(len(tournee) - 1)]
    if tournee[0] != tournee[-1]:              # sécurité : refermer si besoin
        aretes.append((tournee[-1], tournee[0]))
    H = nx.DiGraph()
    H.add_edges_from(aretes)
    nx.draw_networkx_edges(H, pos, edge_color='red', width=2, arrowstyle='-|>', arrowsize=10)

    plt.title(f"Tournée du marchand (NetworkX) — {dist:.2f} km")
    plt.show()


if __name__ == "__main__":
    main()
