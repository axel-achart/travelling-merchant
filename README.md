# Le marchand ambulant

> *Pourquoi le marchand ambulant a-t-il toujours une boussole ? Parce qu’il ne voulait pas que ses affaires « tournent » mal !*

Résolution du **problème du voyageur de commerce (TSP)** sur 20 villes françaises, par deux approches comparées : l’**algorithme de Christofides** et un **algorithme génétique**.

---

## Contexte du projet

Théobald est un marchand ambulant de la France médiévale. Son succès dépend de sa capacité à planifier ses tournées : chaque détour inutile coûte du temps, de l’argent, et augmente son exposition aux bandits et aux intempéries.

Son problème est le **TSP** : trouver le circuit le plus court qui visite chaque ville exactement une fois avant de revenir au point de départ. Le TSP est **NP-difficile** — il n’existe aucun algorithme connu capable de le résoudre efficacement pour toutes les instances. Ici, le nombre de circuits possibles est de `(n-1)! = 19! ≈ 1,2 × 10¹⁷`. Les énumérer tous est hors de question : l’objectif est de trouver le meilleur chemin **sans les évaluer tous**.

### Modélisation

| Élément | Choix |
|---|---|
| Sommets | 20 villes françaises (`villes_france_lat_long.csv`) |
| Arêtes | Graphe **complet** : 190 arêtes (toute ville est joignable depuis toute autre) |
| Poids | Distance de **Haversine** (distance orthodromique, rayon terrestre 6371 km) |
| Objectif | Circuit hamiltonien de poids minimal |

Les 20 villes : Paris, Marseille, Lyon, Toulouse, Nice, Nantes, Strasbourg, Montpellier, Bordeaux, Lille, Rennes, Reims, Le Havre, Saint-Étienne, Toulon, Grenoble, Dijon, Angers, Nîmes, Clermont-Ferrand.

### Structure du dépôt

| Fichier | Rôle |
|---|---|
| `map.py` | Construit le graphe complet pondéré depuis le CSV (Haversine) — base commune aux deux algorithmes |
| `algo_christofides.py` | Christofides implémenté étape par étape |
| `algo_christofides_networkx.py` | Variante en une ligne (`nx.approximation.christofides`), pour vérification |
| `algo_genetique.py` | Algorithme génétique (sélection par tournoi, croisement OX, mutation par échange) |
| `villes_france_lat_long.csv` | Les 20 villes et leurs coordonnées |
| `theorie_des_graphes.md` | Notes de théorie des graphes |
| `fiche_revision_algo_genetique.md` | Fiche de révision sur les algorithmes génétiques |

```bash
pip install -r requirements.txt
```

```bash
python algo_christofides.py
```

```bash
python algo_genetique.py
```

Les deux algorithmes importent le **même graphe** depuis `map.py` : mêmes villes, mêmes distances en km, donc résultats directement comparables.

---

## Les algorithmes utilisés

### 1. Algorithme de Christofides

#### Pourquoi cet algorithme est pertinent ici

Christofides garantit une solution **au pire 1,5 fois plus longue que l’optimum**. Cette garantie n’est valable qu’à une condition : les distances doivent respecter l’**inégalité triangulaire** (aller de A à C directement ne doit jamais être plus long que passer par B).

C’est vérifié dans notre cas : la distance de Haversine est une distance géodésique, et le contrôle sur les **8000 triplets** de villes donne **0 violation**. L’algorithme est donc pleinement applicable — c’est la raison pour laquelle on peut l’utiliser ici et pas sur n’importe quel réseau routier.

#### Les 5 étapes, avec les valeurs obtenues

| Étape | Principe | Résultat mesuré |
|---|---|---|
| **1. Arbre couvrant minimal (ACM)** | Relier les 20 villes au coût total minimal, sans cycle (Prim / Kruskal) | 19 arêtes, **2665,05 km** |
| **2. Sommets de degré impair** | Un circuit eulérien exige que tous les degrés soient pairs | **12 sommets** : Lyon, Nice, Strasbourg, Bordeaux, Lille, Reims, Saint-Étienne, Grenoble, Dijon, Angers, Nîmes, Clermont-Ferrand |
| **3. Couplage parfait de poids minimum** | Apparier ces 12 sommets deux à deux, au coût minimal | 6 arêtes, **1142,03 km** |
| **4. Multigraphe eulérien** | ACM + couplage → tous les degrés deviennent pairs, un circuit eulérien existe | 25 arêtes, **3807,08 km** |
| **5. Raccourcis (*shortcutting*)** | Parcourir le circuit eulérien en sautant les villes déjà visitées → circuit hamiltonien | 3807,08 → **3445,60 km** (−361,48 km) |

Le couplage retenu à l’étape 3 :

| Paire appariée | Distance |
|---|---:|
| Lyon – Grenoble | 94,3 km |
| Saint-Étienne – Clermont-Ferrand | 107,9 km |
| Lille – Reims | 167,6 km |
| Nice – Nîmes | 233,4 km |
| Strasbourg – Dijon | 245,2 km |
| Bordeaux – Angers | 293,6 km |

#### Résultat

**Itinéraire de Théobald :**

`Paris → Le Havre → Rennes → Nantes → Angers → Bordeaux → Toulouse → Montpellier → Nîmes → Nice → Toulon → Marseille → Saint-Étienne → Clermont-Ferrand → Lyon → Grenoble → Dijon → Strasbourg → Reims → Lille → Paris`

**Distance totale : 3445,60 km**

| Mesure | Valeur |
|---|---|
| Temps d’exécution (moyenne sur 20 exécutions) | **1,8 ms** (min 1,6 / max 2,2) |
| Écart-type sur 20 exécutions | **0,00 km** — l’algorithme est **déterministe** |
| Écart à l’optimum exact | +288,48 km, soit **+9,14 %** |
| Ratio obtenu / garantie théorique | 1,0914 pour une garantie ≤ 1,5 |
| Borne inférieure (poids de l’ACM) | 2665,05 km |

La variante `algo_christofides_networkx.py` donne exactement la même distance (3445,60 km), ce qui valide l’implémentation étape par étape.

**Complexité** : dominée par le couplage de poids minimum, en `O(n³)`. Mesuré : 1,6 ms à 20 villes, 3,5 s à 500 villes — la dégradation est douce et prévisible.

---

### 2. Algorithme génétique

#### Principe

Un **individu** = un parcours complet (une permutation des 20 villes), autrement dit un « Théobald d’univers parallèle ». On fait évoluer une population de parcours :

| Mécanisme | Choix d’implémentation |
|---|---|
| Population initiale | Parcours aléatoires (permutations) |
| Fonction de coût | Distance totale du circuit fermé |
| Sélection | **Tournoi** : on tire `k` individus au hasard, le meilleur devient parent |
| Croisement | **OX (Order Crossover)** — adapté au TSP : chaque ville reste présente une seule fois |
| Mutation | Échange (*swap*) de deux villes au hasard |
| Élitisme | Le meilleur individu est recopié tel quel à chaque génération |

#### Paramètres de référence

- Population : `100`
- Générations : `500`
- Mutation : `0,25`
- Tournoi : `k=3`
- Résultat de référence : **3157,12 km**

#### Test de différentes configurations

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

#### Résultat

**Distance totale : 3157,12 km** — soit, comme le montre la section suivante, **l’optimum exact** du problème.

Mesures de performance et de robustesse sur **10 exécutions indépendantes** avec la configuration de référence :

| Mesure | Valeur |
|---|---|
| Temps par exécution | **1,04 s** |
| Moyenne | 3215,51 km (+1,85 % de l’optimum) |
| Meilleur / pire | 3157,12 / 3386,83 km |
| Écart-type | **90,22 km** |
| Optimum atteint | **7 exécutions sur 10** |

> **Point important sur la robustesse.** Les tableaux ci-dessus affichent moyenne = meilleur = pire pour les bons réglages, ce qui pourrait laisser croire à un résultat garanti. Ce n’est pas le cas : sur 10 graines aléatoires indépendantes, l’optimum n’est atteint que **7 fois sur 10**. L’algorithme génétique reste **stochastique** — deux exécutions identiques donnent deux résultats différents.
>
> C’est précisément ce qui justifie la stratégie retenue dans `algo_genetique.py` : **relancer 5 fois et garder le meilleur parcours**. Avec un taux de réussite de 70 % par exécution, 5 essais portent la probabilité d’atteindre l’optimum à environ **99,8 %**, pour un coût total de ~5,2 s.

---

### 3. Référence exacte : à quoi comparer ?

Pour mesurer objectivement la qualité des deux heuristiques, il faut connaître le **vrai optimum**. Pour n = 20, l’énumération des `19! ≈ 1,2 × 10¹⁷` circuits est impossible, mais la **programmation dynamique de Held-Karp** (`O(n² · 2ⁿ)`) le calcule exactement :

**Optimum exact : 3157,12 km, calculé en 1,1 s.**

`Paris → Le Havre → Rennes → Angers → Nantes → Bordeaux → Toulouse → Montpellier → Nîmes → Marseille → Toulon → Nice → Grenoble → Lyon → Saint-Étienne → Clermont-Ferrand → Dijon → Strasbourg → Reims → Lille → Paris`

Cette valeur permet deux conclusions solides :

1. L’algorithme génétique ne trouve pas une solution « presque optimale » — **il trouve l’optimum réel**. Ce n’est plus une supposition, c’est démontré.
2. Christofides se situe à **+9,14 %** de cet optimum, très loin de sa borne théorique de +50 %.

---

## Analyse comparative

| Critère | Christofides | Algorithme génétique |
|---|---|---|
| **Distance totale** | 3445,60 km | 3157,12 km (meilleur) / 3215,51 km (moyenne) |
| **Écart à l’optimum** | +9,14 % | 0 % au mieux, +1,85 % en moyenne |
| **Temps d’exécution** | **1,8 ms** | 1,04 s par essai, ~5,2 s pour la stratégie à 5 essais |
| **Déterminisme** | Oui — écart-type 0,00 km | Non — écart-type 90,22 km |
| **Robustesse** | Résultat identique à chaque lancement | Optimum atteint 7 fois sur 10 |
| **Garantie théorique** | ≤ 1,5 × optimum, **prouvée** | Aucune |
| **Paramètres à régler** | **Aucun** | 4 (population, générations, mutation, `k`) |
| **Facilité d’implémentation** | Plus exigeante : ACM, couplage de poids minimum, circuit eulérien, raccourcis | Plus simple à comprendre, mais OX et élitisme sont des pièges classiques |
| **Passage à l’échelle** | `O(n³)` : 1,6 ms à n=20, 3,5 s à n=500 | Budget (population × générations) à augmenter avec n, sinon la qualité s’effondre |

### Avantages et inconvénients dans le contexte de Théobald

**Christofides**
- ✅ Résultat immédiat (1,8 ms) et **toujours le même** : Théobald peut recalculer sa tournée autant de fois qu’il veut, il obtient le même itinéraire.
- ✅ **Borne d’erreur connue à l’avance** : même sans connaître l’optimum, il sait qu’il ne fait jamais plus de 50 % de détour. C’est une garantie commerciale, pas une espérance.
- ✅ Aucun réglage : rien à calibrer, rien à re-calibrer si les villes changent.
- ❌ **+288 km de détour inutile** sur cette tournée — ce n’est pas négligeable pour un marchand.
- ❌ Ne sait traiter **que** la minimisation de distance : aucune contrainte annexe ne peut être exprimée.

**Algorithme génétique**
- ✅ **Trouve l’optimum** (3157,12 km).
- ✅ Extensible : accepte n’importe quelle fonction de coût.
- ❌ ~580 fois plus lent, et **aléatoire** : une exécution unique est un pari (3 chances sur 10 de finir sur un parcours moins bon).
- ❌ Demande un calibrage de 4 paramètres, dont les tableaux ci-dessus montrent qu’un mauvais choix coûte cher (`k=1` → 4743 km, mutation nulle → 3799 km).

### Le meilleur des deux : Christofides + 2-opt

Les deux approches ne sont pas concurrentes. Christofides produit une tournée déjà géographiquement cohérente, dans laquelle il ne reste que quelques croisements à défaire — exactement ce que fait une optimisation locale **2-opt** (inverser un segment quand cela raccourcit le trajet) :

| Méthode | Distance | Temps |
|---|---|---|
| Christofides seul | 3445,60 km (+9,14 %) | 1,8 ms |
| Algorithme génétique (5 essais) | 3157,12 km (optimum) | ~5,2 s |
| **Christofides + 2-opt** | **3157,12 km (optimum)** | **1,9 ms** |

Le post-traitement 2-opt atteint l’optimum pour **0,1 ms supplémentaire** : même qualité que l’algorithme génétique, environ **2700 fois plus vite**, et sans aucun aléa.

---

## Conclusion

**Recommandation pour Théobald : Christofides suivi d’une optimisation locale 2-opt.**

Sur ses 20 villes, cette combinaison donne la tournée optimale de **3157,12 km en moins de 2 ms**, de façon reproductible et sans aucun paramètre à régler. L’algorithme génétique atteint la même distance, mais demande ~5 secondes, 4 paramètres calibrés et 5 essais pour fiabiliser le résultat. À qualité égale, le choix est sans ambiguïté.

Trois points à retenir au-delà de la recommandation :

1. **À 20 villes, le problème est en réalité exactement soluble.** Held-Karp donne l’optimum certifié en 1,1 s. Les deux heuristiques ne servent donc pas vraiment à « résoudre » le cas de Théobald : elles préparent le cas où sa tournée grandit. Au-delà d’environ 25 villes, le terme `2ⁿ` rend l’exact impraticable et les heuristiques deviennent les seules options viables.

2. **Christofides seul ne suffit pas, mais sa valeur n’est pas sa précision.** +9,14 %, soit 288 km de détour, c’est trop pour un marchand. Ce que Christofides apporte, c’est une **garantie** (≤ 1,5 ×) et un **déterminisme** qu’aucun algorithme génétique ne peut offrir. C’est un excellent point de départ, pas un point d’arrivée — d’où l’intérêt de l’associer à 2-opt.

3. **L’algorithme génétique garde un avantage décisif hors de ce cadre.** Il accepte des contraintes que Christofides ne sait pas représenter : fenêtres horaires, routes dangereuses à éviter, capacité de charge, profits différents selon les marchés. Dès que l’objectif de Théobald cesse d’être « la tournée la plus courte » pour devenir « la tournée la plus rentable », Christofides ne s’applique plus — et l’algorithme génétique reste utilisable tel quel, en changeant simplement la fonction de coût.

En résumé : **Christofides + 2-opt pour la tournée quotidienne**, l’algorithme génétique **le jour où le problème se complique**.
