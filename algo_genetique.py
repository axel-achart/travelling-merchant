# ---------------------------------------------------------------------------
# Résolution avec un ALGORITHME GÉNÉTIQUE (à comparer avec Christofides)
#
# Idée : on fait évoluer une POPULATION de parcours possibles sur plusieurs
# générations, comme une sélection naturelle :
#   - un individu = un ordre de visite des villes (une permutation) ;
#   - les meilleurs individus (circuit le plus court) se reproduisent ;
#   - le croisement OX mélange deux parents en gardant un bout de chacun ;
#   - la mutation échange 2 villes au hasard pour explorer de nouvelles pistes.
#
# Ce script utilise LE MÊME graphe que les scripts Christofides (via map.py) :
# mêmes villes, mêmes distances en km -> les résultats sont comparables.
#
# Deux petites adaptations par rapport au code d'origine, pour de meilleurs
# résultats : le taux de mutation passe de 5 % à 25 %, et l'algorithme est
# relancé 5 fois (il est aléatoire) en gardant le meilleur parcours.
# ---------------------------------------------------------------------------
import random

import networkx as nx
import matplotlib.pyplot as plt

from map import G          # graphe complet : villes + distances Haversine (km)

# ---------------------------------------------------------------------------
# 1. Préparation des données : liste des villes et matrice des distances.
# ---------------------------------------------------------------------------
VILLES = list(G.nodes)     # les noms des villes, dans l'ordre des nœuds du graphe
N = len(VILLES)            # nombre de villes à visiter (20 ici)

# Matrice des distances en km : DISTANCES[i][j] = distance entre VILLES[i] et VILLES[j].
# On lit simplement le poids des arêtes du graphe (Haversine, déjà calculé dans map.py).
# Note : le graphe ne contient pas d'arête d'une ville vers elle-même, donc la
# diagonale (distance d'une ville à elle-même) vaut 0.
DISTANCES = [[0.0 if i == j else G[VILLES[i]][VILLES[j]]['weight']
              for j in range(N)] for i in range(N)]


# ---------------------------------------------------------------------------
# 2. Fonction de coût (fitness) : distance totale d'un circuit.
# ---------------------------------------------------------------------------
def fitness(tour, distances):
    """ Distance totale du CIRCUIT FERMÉ (retour à la ville de départ inclus).
        - tour : une liste d'INDICES de villes, ex. [3, 0, 7, ...].
        - Pour chaque ville, on ajoute la distance vers la suivante ; grâce au
          modulo, la dernière ville est reliée à la première.
        - C'est exactement la même mesure que la distance affichée par les
          scripts Christofides, donc les résultats sont comparables. """
    total = 0
    for i in range(len(tour)):
        ville_actuelle = tour[i]
        ville_suivante = tour[(i + 1) % len(tour)]   # % : la dernière revient vers la première
        total += distances[ville_actuelle][ville_suivante]
    return total

# ---------------------------------------------------------------------------
# 3. Sélection par TOURNOI : quels individus deviennent parents ?
# ---------------------------------------------------------------------------
def selection(population, distances, k=3):
    """ On tire k individus au hasard et on garde le meilleur (le plus court).
        Le hasard évite de toujours sélectionner les mêmes individus :
        cela garde de la diversité dans la population. """
    return min(random.sample(population, k), key=lambda t: fitness(t, distances))

# ---------------------------------------------------------------------------
# 4. Croisement OX (Order Crossover) : créer un enfant à partir de 2 parents.
# ---------------------------------------------------------------------------
def croisement_ox(parent1, parent2):
    """ Croisement adapté au TSP : chaque ville doit apparaître UNE SEULE fois.
        1. On tire 2 points de coupe au hasard.
        2. L'enfant COPIE le segment central du parent 1 (positions [debut:fin]).
        3. On complète les positions libres avec les villes du parent 2, dans
           leur ordre, en IGNORANT celles déjà présentes. """
    taille = len(parent1)
    debut, fin = sorted(random.sample(range(taille), 2))   # les deux points de coupe

    enfant = [-1] * taille                    # -1 = position pas encore remplie
    enfant[debut:fin] = parent1[debut:fin]    # 2. le bout d'itinéraire du parent 1

    # 3. villes du parent 2 pas encore utilisées, dans leur ordre d'apparition
    restantes = [ville for ville in parent2 if ville not in enfant]
    enfant[:debut] = restantes[:debut]        # remplit avant le segment...
    enfant[fin:] = restantes[debut:]          # ...et après le segment
    return enfant

# ---------------------------------------------------------------------------
# 5. Mutation : petite perturbation aléatoire d'un individu.
# ---------------------------------------------------------------------------
def mutation(tour):
    """ Échange deux villes au hasard. Le parcours change très peu mais cela
        permet de tester des solutions que le croisement seul ne produirait
        jamais (exploration, sortie des optimums locaux). """
    i, j = random.sample(range(len(tour)), 2)
    tour[i], tour[j] = tour[j], tour[i]      # échange (swap) des deux villes
    return tour

# ---------------------------------------------------------------------------
# 6. L'algorithme génétique : la boucle d'évolution.
# ---------------------------------------------------------------------------
def algorithme_genetique(pop_size=100, generations=500, taux_mutation=0.25):
    """ Fait évoluer une population de parcours et renvoie le meilleur trouvé.
        - pop_size      : nombre d'individus par génération ;
        - generations   : nombre de cycles d'évolution ;
        - taux_mutation : probabilité qu'un enfant subisse une mutation.
          On est passé de 5 % à 25 % : avec seulement 5 %, la population perd
          vite sa diversité et se bloque sur une solution moyenne. """
    # Population de départ : pop_size parcours aléatoires, chacun visitant
    # toutes les villes une seule fois (random.sample garantit l'unicité).
    population = [random.sample(range(N), N) for _ in range(pop_size)]

    for gen in range(generations):

        # ÉLITISME : on recopie tel quel le meilleur individu de la génération
        # précédente. Sans cela, il pourrait disparaître (croisement/mutation)
        # et le résultat final serait moins bon.
        nouvelle_population = [min(population, key=lambda t: fitness(t, DISTANCES))]

        # Création des enfants jusqu'à retrouver une population complète.
        while len(nouvelle_population) < pop_size:
            parent1 = selection(population, DISTANCES)
            parent2 = selection(population, DISTANCES)
            enfant = croisement_ox(parent1, parent2)
            if random.random() < taux_mutation:      # mutation (25 % de chance)
                enfant = mutation(enfant)
            nouvelle_population.append(enfant)

        population = nouvelle_population             # remplacement générationnel

        # Suivi de la convergence : meilleure distance affichée régulièrement.
        if (gen + 1) % 250 == 0:
            meilleure = fitness(population[0], DISTANCES)
            print(f"  génération {gen + 1:>4} — meilleure distance : {meilleure:7.2f} km")

    return population[0]    # le meilleur individu de la dernière génération

# ---------------------------------------------------------------------------
# 7. Programme principal : lancement, résultats texte, affichage graphique.
# ---------------------------------------------------------------------------
def main():
    # random.seed(42)   # à décommenter pour obtenir toujours les mêmes résultats

    print(f"Algorithme génétique — {N} villes à visiter\n")

    # L'algorithme est ALÉATOIRE : deux lancements donnent deux résultats différents.
    # On le relance donc plusieurs fois et on garde le meilleur parcours trouvé.
    NOMBRE_ESSAIS = 5
    meilleur = None

    for essai in range(NOMBRE_ESSAIS):
        print(f"--- Essai {essai + 1}/{NOMBRE_ESSAIS} ---")
        candidat = algorithme_genetique(pop_size=100, generations=500, taux_mutation=0.25)
        if meilleur is None or fitness(candidat, DISTANCES) < fitness(meilleur, DISTANCES):
            meilleur = candidat
        print(f"    essai : {fitness(candidat, DISTANCES):.2f} km"
              f"  |  meilleur jusqu'ici : {fitness(meilleur, DISTANCES):.2f} km\n")

    # Conversion des indices en noms de villes (un individu ne contient que des numéros).
    itineraire = [VILLES[i] for i in meilleur]

    # Distance totale du circuit fermé, en km (comparable à Christofides).
    distance_totale = fitness(meilleur, DISTANCES)

    # --- Affichage texte -----------------------------------------------------
    print("\nItinéraire de Théobald (algorithme génétique) :")
    print(" -> ".join(itineraire) + " -> " + itineraire[0])   # on referme la boucle
    print(f"\nDistance totale (algorithme génétique) : {distance_totale:.2f} km")
    print("À comparer avec la distance donnée par les scripts Christofides.")

    # --- Affichage graphique sur la carte du marchand -------------------------
    afficher_parcours(meilleur, VILLES, distance_totale)

# ---------------------------------------------------------------------------
# 8. Affichage graphique : l'itinéraire trouvé en rouge sur la carte.
# ---------------------------------------------------------------------------
def afficher_parcours(tour, villes, distance):
    """ Affiche la carte du marchand avec l'itinéraire en rouge.
        - tour     : liste d'indices de villes (un individu de l'algorithme) ;
        - villes   : liste des noms de villes (VILLES), indexée par les indices ;
        - distance : distance totale du circuit, affichée dans le titre. """
    # Récupération des noms de villes dans l'ordre du parcours.
    tour_coords = [villes[i] for i in tour] 
    # Revenir à la ville de départ pour fermer le circuit.
    tour_coords.append(tour_coords[0])

    # Fond de carte : toutes les villes et toutes les routes possibles.
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw(G, pos, with_labels=True, node_size=50, font_size=8,
            edge_color='lightgray', node_color='skyblue')

    # On met en rouge les arêtes de l'itinéraire trouvé.
    aretes = [(tour_coords[i], tour_coords[i + 1]) for i in range(len(tour_coords) - 1)]
    H = nx.DiGraph()
    H.add_edges_from(aretes)
    nx.draw_networkx_edges(H, pos, edge_color='red', width=2, arrowstyle='-|>', arrowsize=10)

    plt.title(f"Tournée du marchand (algorithme génétique) — {distance:.2f} km")
    plt.show()


if __name__ == "__main__":
    main()
    
   
    