# Le marchand ambulant

## Contexte du projet
/

## Les algorithmes utilisés
/
**Référence**

- Population : `100`
- Générations : `500`
- Mutation : `0,25`
- Tournoi : `k=3`
- Résultat de référence : **3157,12 km**

**1. Taille de population `pop_size`**

| Valeur | Moyenne | Meilleur | Pire |
|---:|---:|---:|---:|
| 20 | 3534,64 km | 3157,12 | 3751,28 |
| 50 | 3452,19 km | 3157,12 | 3640,11 |
| 100 | 3157,12 km | 3157,12 | 3157,12 |
| 200 | 3157,12 km | 3157,12 | 3157,12 |
| 400 | 3387,25 km | 3157,12 | 3617,21 |

- **Petite population** : exécution plus rapide, mais diversité faible et risque de convergence prématurée.
- **Population moyenne** : meilleur équilibre entre diversité et coût de calcul.
- **Grande population** : davantage de solutions explorées, mais coût beaucoup plus élevé. Ici, `400` n’améliore pas le résultat, car 500 générations suffisent déjà à trouver la meilleure solution.
- **Conclusion** : `100` est un bon compromis.

**2. Nombre de générations `generations`**

| Valeur | Moyenne | Meilleur | Pire |
|---:|---:|---:|---:|
| 50 | 3468,81 km | 3367,10 | 3594,50 |
| 100 | 3171,01 km | 3157,12 | 3198,79 |
| 250 | 3157,12 km | 3157,12 | 3157,12 |
| 500 | 3157,12 km | 3157,12 | 3157,12 |
| 1000 | 3157,12 km | 3157,12 | 3157,12 |

- **Peu de générations** : calcul rapide, mais l’algorithme n’a pas le temps d’affiner les parcours.
- **100 générations** : amélioration importante, mais quelques résultats restent légèrement moins bons.
- **250 générations** : la solution optimale est déjà atteinte dans les essais.
- **500 ou 1000 générations** : aucun gain observé ; 1000 augmente seulement le temps de calcul.
- **Conclusion** : `250` semble suffisant pour ce problème, tandis que `500` offre une marge de sécurité.

**3. Taux de mutation `taux_mutation`**

| Valeur | Moyenne | Meilleur | Pire |
|---:|---:|---:|---:|
| 0,00 | 3799,04 km | 3679,61 | 3983,18 |
| 0,05 | 3292,72 km | 3157,12 | 3386,83 |
| 0,15 | 3554,45 km | 3334,20 | 3682,35 |
| 0,25 | 3157,12 km | 3157,12 | 3157,12 |
| 0,50 | 3157,12 km | 3157,12 | 3157,12 |

- **Mutation nulle** : la population perd rapidement sa diversité et reste bloquée dans un optimum local.
- **5 %** : réintroduit un peu de diversité, mais pas toujours suffisamment.
- **15 %** : meilleur potentiel d’exploration, mais résultats plus irréguliers dans cette expérience.
- **25 %** : très bon équilibre entre exploration et conservation des bons parcours.
- **50 %** : forte exploration ; l’élitisme protège toutefois le meilleur individu. Peut devenir excessif sur d’autres problèmes, car beaucoup d’enfants sont fortement modifiés.
- **Conclusion** : `0,25` est le réglage le plus équilibré ici.

**4. Taille du tournoi de sélection `k`**

| Valeur | Moyenne | Meilleur | Pire |
|---:|---:|---:|---:|
| 1 | 4743,16 km | 4527,74 | 4907,04 |
| 2 | 3310,26 km | 3157,12 | 3386,83 |
| 3 | 3157,12 km | 3157,12 | 3157,12 |
| 5 | 3390,77 km | 3157,12 | 3627,77 |
| 10 | 3577,47 km | 3387,42 | 3849,15 |

- **`k=1`** : sélection aléatoire, donc pression de sélection presque inexistante.
- **`k=2`** : commence à favoriser les bons individus, mais reste variable.
- **`k=3`** : équilibre entre sélection des meilleurs et conservation de diversité.
- **`k=5`** : pression de sélection plus forte, avec un risque de perdre trop rapidement la diversité.
- **`k=10`** : sélection très agressive ; convergence prématurée et résultats moins réguliers.
- **Conclusion** : `k=3` est le meilleur compromis.


## Conclusion
/