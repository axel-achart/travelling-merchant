import random

def fitness(tour, distances):
    return sum(distances[tour[i]][tour[i+1]] for i in range(len(tour)-1))

def selection(pop, distances, k=3):
    # Tournoi : on tire k individus, on garde le meilleur
    return min(random.sample(pop, k), key=lambda t: fitness(t, distances))

def order_crossover(p1, p2):
    size = len(p1)
    start, end = sorted(random.sample(range(size), 2))
    child = [-1] * size
    # Copie de la sous-chaîne du parent 1
    child[start:end] = p1[start:end]
    # Remplissage avec les éléments du parent 2
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
            if random.random() < 0.05: child = mutate(child)  # mutation 5%
            new_pop.append(child)
        pop = new_pop
    return min(pop, key=lambda t: fitness(t, distances))

import matplotlib.pyplot as plt
import math

#1 génération de test ( 15 villes aux coordonnées aléatoires)
villes = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(15)]

#2. Calcul de la matrices des distances entre chaque ville
distances = []
for i in range(len(villes)):
    row = []
    for j in range(len(villes)):
        dist =math.hypot(villes[i][0] - villes[j][0], villes[i][1] - villes[j][1])
        row.append(dist)
    distances.append(row)

#3. Exécution de l'algorithme génétique pour trouver le meilleur itinéraire
meilleur_parcours = genetic_algorithm(villes, distances, pop_size=100, generations=500)
meilleur_distance = fitness(meilleur_parcours, distances)

#4. Affichage texte
print(f"Meilleur ordre de visite des villes : {meilleur_parcours}")
print(f" distance totale : {meilleur_distance:.2f}")

#affichage graphique
def afficher_parcours(tour, villes, distance):
    #récupération des coordonnées des villes dans l'ordre du parcours
    tour_coords = [villes[i] for i in tour] 
    #Revenir à la ville de départ pour fermer le circuit
    tour_coords.append(tour_coords[0])
    
   
    