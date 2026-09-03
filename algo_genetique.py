import random

def fitness(tour, distances):
    return sum(distances[tour[i]][tour[i+1]] for i in range(len(tour)-1))

def selection(pop, distances, k=3):
    # Tournoi : on tire k individus, on garde le meilleur
    return min(random.sample(pop, k), key=lambda t: fitness(t, distances))

def order_crossover(p1, p2):
    size = len(p1)
    start, end= sorted(random.sample(range(size), 2))
    child = [-1] * size
    # Copie de la sous-chaîne du parent 1
    child[start:end] = p1[start:end]
    # Remplissage avvec les éléments du parent 2
    p2_filtered = [x for x in p2 if x not in child]
    child[:start] = p2_filtered[:start]
    child[end:] = p2_filtered[start:]
    return child

def mutate(child):
    # Mutation par échange (swap) de deux gènes
    idx1, idx2 = random.sample(range(len(child)), 2)
    child[idx1], child[idx2] = child[idx2], child[idx1]
    return child

def genetic_algorithm(villes, distances, pop_size=100, generations=500):
    pop = [random.sample(range(len(villes)), len(villes)) for _ in range(pop_size)]
    for gen in range(generations):
        new_pop = []
        for _ in range(pop_size):
            p1, p2 = selection(pop, distances), selection(pop, distances)
            child = order_crossover(p1, p2)
            if random.random() < 0.05:  child = mutate(child) # mutation 5%
            new_pop.append(child)
        pop = new_pop

    return min(pop, key=lambda t: fitness(t, distances))


import math
import matplotlib.pyplot as plt

# 1 Génération de données de test (15 villes aux coordonnées aléatoires)
villes = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(15)]

# 2 Calcul de la matrice des distances entre chaque ville
distances = []
for i in range(len(villes)):
    row = []
    for j in range(len(villes)):
        dist = math.hypot(villes[i][0] - villes[j][0], villes[i][1] - villes[j][1])
        row.append(dist)
    distances.append(row)

# 3 Exécution de l'algo
meilleur_parcours = genetic_algorithm(villes, distances, pop_size=100, generations=300)
meilleure_distance = fitness(meilleur_parcours, distances)

# 4 Affichage texte
print(f"Meilleur ordre de visite : {meilleur_parcours}")
print(f"Distance totale : {meilleure_distance:.2f}")

# 5 Affichage graphique
def afficher_parcours(tour, villes, distance):
    # Récupérer les coordonnées dans l'ordre du parcours
    tour_coords = [villes[i] for i in tour]
    # Revenir à la ville de départ pour fermer la boucle
    tour_coords.append(tour_coords[0])

    x, y = zip(*tour_coords)

    plt.figure(figsize=(8, 6))
    plt.plot(x, y, marker='o', linestyle='-', color='b', markerfacecolor='r')

    # numéroter les villes
    for i, (cx, cy) in enumerate(villes):
        plt.text(cx + 1.5, cy + 1.5, str(i), fontsize=10, color='darkred')

    plt.title(f"Résultat du Voyageur de Commerce (Distance:  {distance:.2f})")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()

afficher_parcours(meilleur_parcours, villes, meilleure_distance)