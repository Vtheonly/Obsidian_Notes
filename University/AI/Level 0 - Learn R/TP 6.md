Absolument ! Préparons-nous à décortiquer ce TP N°6 sur les Arbres de Décision en détail et en français.

Je vais passer en revue chaque question et chaque nouvelle syntaxe R que vous avez rencontrée.

---

**Fichier : `playTennis.csv`**

Ce fichier CSV contient les données utilisées pour construire l'arbre de décision. Chaque ligne est une observation (un jour), et les colonnes sont des attributs (Outlook, Temperature, etc.) avec une variable cible (PlayTennis) qui indique si on a joué au tennis ou non.

```csv
Day,Outlook,Temperature,Humidity,Wind,PlayTennis
D1,Sunny,Hot,High,Weak,No
D2,Sunny,Hot,High,Strong,No
...
D14,Rain,Mild,High,Strong,No
```

---

**TP N° 6: Arbres de décision**

**But du TP & prérequis :**
*   Implémenter un arbre de décision pour des datasets avec données catégorielles.
*   Installer le package `data.tree` : `install.packages("data.tree", dependencies=T)`
    *   **Explication :** `install.packages()` est la commande R pour télécharger et installer des packages (bibliothèques) depuis CRAN (le référentiel officiel des packages R). `dependencies=T` (ou `TRUE`) assure que toutes les autres bibliothèques dont `data.tree` dépend sont aussi installées. `data.tree` est spécifiquement conçu pour créer et manipuler des structures arborescentes.

---

**A. Étape d'entraînement**

Code initial (lignes 1-8) :
```R
1 library(data.tree)
2 verbose <- FALSE
3 maxHeight <- 3
4 #Example (only categorical datasets)
5 fileName <- "playTennis.csv"
6 rootName <- "PlayTennis"
7 nbrAttr <- 5
8 newObject <- c("Rain", "Mild", "High", "Strong")
```
*   **Ligne 1 : `library(data.tree)`**
    *   **Explication :** Charge le package `data.tree` en mémoire pour que ses fonctions et objets soient utilisables dans la session R actuelle. Si le package n'est pas installé, cette commande échouera.
*   **Ligne 2 : `verbose <- FALSE`**
    *   **Explication :** Crée une variable booléenne nommée `verbose` et lui assigne la valeur `FALSE`. Cette variable est souvent utilisée pour contrôler la quantité d'informations affichées par un script (si `TRUE`, on affiche plus de détails, utile pour le débogage).
*   **Ligne 3 : `maxHeight <- 3`**
    *   **Explication :** Crée une variable `maxHeight` et lui assigne la valeur 3. Elle servira à limiter la profondeur maximale de l'arbre de décision.
*   **Ligne 5 : `fileName <- "playTennis.csv"`**
    *   **Explication :** Stocke le nom du fichier CSV dans la variable `fileName`.
*   **Ligne 6 : `rootName <- "PlayTennis"`**
    *   **Explication :** Stocke le nom qui sera donné au nœud racine de l'arbre (qui correspondra à la variable cible).
*   **Ligne 7 : `nbrAttr <- 5`**
    *   **Explication :** Stocke le nombre d'attributs prédicteurs dans le dataset (Outlook, Temperature, Humidity, Wind, Day). Ici, il semble que `Day` ne soit pas utilisé comme prédicteur, donc on a 5 attributs (Outlook, Temp, Hum, Wind + la classe PlayTennis). Attention, si `Day` est une colonne dans `playTennis.csv` et qu'on lit `nbrAttr+1` colonnes, `nbrAttr` devrait être le nombre de colonnes *avant* la colonne `PlayTennis`. Le CSV a 6 colonnes (Day, Outlook, Temp, Hum, Wind, PlayTennis). Si `Day` est ignoré (comme il devrait l'être pour ID3), et `PlayTennis` est la cible, il y a 4 attributs prédicteurs (Outlook, Temp, Hum, Wind). La variable `nbrAttr` est utilisée plus tard dans `colClasses = rep("character", nbrAttr+1)`. Si `nbrAttr` est 5, cela signifie que `datasetDF` aura 6 colonnes lues comme `character`. Cela correspond aux 5 attributs + la classe, si "Day" est la première colonne et est utilisée comme `row.names=1`.
*   **Ligne 8 : `newObject <- c("Rain", "Mild", "High", "Strong")`**
    *   **Explication :** Crée un vecteur nommé `newObject`. Ce vecteur contient les valeurs des attributs pour un nouvel individu dont on voudra prédire la classe plus tard. L'ordre correspondra à "Outlook", "Temperature", "Humidity", "Wind".

**Q1: En utilisant la console, s'assurer que le fichier s'ouvre bien par la commande : `cat(readChar(fileName, file.info(fileName)$size))`**
*   **`file.info(fileName)` :**
    *   **Explication :** Cette fonction retourne une liste d'informations sur le fichier spécifié (`fileName`).
*   **`file.info(fileName)$size` :**
    *   **Explication :** L'opérateur `$` est utilisé pour accéder à un élément d'une liste par son nom. Ici, on accède à la taille (en octets) du fichier.
*   **`readChar(fileName, file.info(fileName)$size)` :**
    *   **Explication :** `readChar()` lit un certain nombre de caractères depuis une connexion (ici, un fichier). Le premier argument est le nom du fichier, le second est le nombre de caractères à lire. En utilisant `file.info(fileName)$size`, on s'assure de lire l'intégralité du fichier.
*   **`cat(...)` :**
    *   **Explication :** La fonction `cat()` (concatenate and print) affiche ses arguments sur la console. Ici, elle affiche le contenu complet du fichier lu par `readChar()`.
*   **Réponse Q1 :** Cette commande permet de vérifier que R peut accéder au fichier `playTennis.csv` et d'afficher son contenu brut dans la console, confirmant ainsi que le fichier est lisible et que son contenu est celui attendu (les données du tableau "Play Tennis").

**Q2: Exécuter la totalité du code avec le bouton source puis analyser la sortie sur console. Celle-ci correspond-elle au résultat attendu ?**
*   **Réponse Q2 :** La sortie sur console (après exécution de tout le script jusqu'à la ligne 80, qui inclut `print(tree, ...)` et `plot(tree)`) devrait montrer la structure textuelle de l'arbre de décision final et ouvrir une fenêtre avec le graphique de cet arbre.
    ```
    *** Final tree:
        levelName feature obsCount type class
    1 PlayTennis Outlook       14
    2  ¦--Overcast PlayTennis       4 Leaf   Yes  <-- ObsCount est le nb d'exemples pour CE NOEUD Overcast
    3  °--Rain        Wind       5
    4     ¦--Strong PlayTennis       2 Leaf    No
    5     °--Weak   PlayTennis       3 Leaf   Yes
    6  °--Sunny    Humidity       5
    7     ¦--High   PlayTennis       3 Leaf    No
    8     °--Normal PlayTennis       2 Leaf   Yes
    ```
    Oui, cette sortie correspond à un arbre de décision typique pour le dataset PlayTennis, où "Outlook" est choisi comme premier critère de division.

**Q3: Que représente la structure affichée sur console ? Expliquer dans celle-ci chacun des constituants suivants : `levelName`, `feature`, `obsCount`, `type` et `class`.**
*   **Réponse Q3 :** La structure affichée est une représentation textuelle de l'arbre de décision construit.
    *   **`levelName` :** Indique le chemin depuis la racine jusqu'au nœud courant et le nom du nœud. Par exemple, `PlayTennis` est la racine. `¦--Overcast` signifie que "Overcast" est un enfant de "PlayTennis". `Rain/Strong` (non visible ici, mais serait le cas si on affichait plus de détails ou si on naviguait) signifierait le nœud "Strong" sous le nœud "Rain". Les symboles `¦--` et `°--` aident à visualiser la hiérarchie.
    *   **`feature` :**
        *   Pour les nœuds internes (non-feuilles) : C'est l'attribut utilisé pour diviser (splitter) les données à ce nœud (ex: "Outlook" pour la racine, "Wind" pour le nœud "Rain").
        *   Pour les nœuds feuilles : Dans cette sortie spécifique, `feature` pour une feuille semble être le nom de la classe cible elle-même (ex: "PlayTennis" pour la feuille "Overcast"). Cela peut varier selon la configuration de `print.Node`. Si la classe est "Yes", le feature pourrait être "PlayTennis" et la colonne `class` indiquerait "Yes". Ici, il semble que le nom de la classe cible soit utilisé comme "feature" pour les feuilles.
    *   **`obsCount` :** (Observation Count) Le nombre d'exemples (instances/lignes du dataset) qui atteignent ce nœud. La racine "PlayTennis" a 14 observations (tout le dataset). Le nœud "Overcast" en a 4.
    *   **`type` :** Indique si le nœud est une feuille (`Leaf`) ou un nœud interne (auquel cas, cette colonne pourrait être vide ou indiquer autre chose comme "Node").
    *   **`class` :** Pour les nœuds de type `Leaf`, c'est la classe prédite pour les instances qui atteignent cette feuille (ex: "Yes" pour "Overcast", "No" pour "Rain/Strong").

---
Suite du script (fonctions) :

*   **`isPure <- function(data)` (Ligne 11)**
    *   `length(unique(data[,ncol(data)])) == 1`
        *   `ncol(data)`: Renvoie le nombre de colonnes dans le dataframe `data`.
        *   `data[,ncol(data)]`: Sélectionne toutes les lignes de la dernière colonne de `data` (supposée être la colonne de la classe cible).
        *   `unique(...)`: Renvoie un vecteur avec uniquement les valeurs uniques de cette colonne.
        *   `length(...) == 1`: Vérifie si la longueur de ce vecteur de valeurs uniques est égale à 1. Si oui, cela signifie que toutes les instances dans `data` ont la même classe, donc le sous-ensemble est "pur".
*   **`entropy <- function(vls)` (Ligne 14)**
    *   Calcule l'entropie d'un vecteur de fréquences de classes `vls`.
    *   `res <- vls/sum(vls)`: Calcule les probabilités de chaque classe.
    *   `log2(res)`: Calcule le logarithme en base 2 de ces probabilités.
    *   `-sum(res*log2(res))`: Formule de l'entropie.
*   **`Gain <- function(crossTab)` (Ligne 19)**
    *   `crossTab` est une table de contingence (créée par `table(data[,"Attribut"], data[,"Classe"])`).
    *   Cette fonction calcule le gain d'information pour un attribut, basé sur l'entropie. Elle soustrait l'entropie pondérée des sous-ensembles (après division par l'attribut) de l'entropie totale du dataset avant division.
*   **`trainID3 <- function(node, data, maxHeight)` (Ligne 26)**
    *   C'est la fonction principale qui construit l'arbre (algorithme ID3).
    *   `node`: Le nœud `data.tree` courant à traiter.
    *   `data`: Le sous-ensemble de données associé à ce `node`.
    *   `maxHeight`: La profondeur maximale autorisée pour l'arbre.
    *   **Ligne 27 : `node$obsCount <- nrow(data)`**
        *   Stocke le nombre d'observations dans le sous-ensemble `data` comme un attribut `obsCount` de l'objet `node` de `data.tree`.
    *   **Ligne 31 : `if (isPure(data) | node$level == (maxHeight + 1))`**
        *   Condition d'arrêt de la récursion :
            *   `isPure(data)`: Si le sous-ensemble de données est pur.
            *   `node$level`: Attribut de `data.tree` qui donne la profondeur du nœud courant (racine = niveau 1). Si la profondeur atteint `maxHeight + 1` (car `maxHeight` est un index de 0 à `maxHeight-1` niveaux, ou `maxHeight` niveaux de profondeur), on arrête.
    *   **Lignes 37-39 (Nœud feuille) :**
        *   `node$type <- "Leaf"`: Marque le nœud comme une feuille.
        *   **`node$feature <- tail(names(data), 1)` (Ligne 38)** : `names(data)` donne les noms des colonnes. `tail(..., 1)` prend le dernier nom, qui est celui de la colonne classe (ex: "PlayTennis"). Ce sera la "feature" affichée pour ce nœud feuille.
        *   **`node$class <- names(which.max(table(data[,ncol(data)])))` (Ligne 39)** : Détermine la classe majoritaire dans le sous-ensemble `data` et l'assigne à `node$class`.
            *   `table(data[,ncol(data)])`: Fréquence des classes.
            *   `which.max(...)`: Index de la classe la plus fréquente.
            *   `names(...)`: Nom de cette classe.
    *   **Lignes 42-70 (Partitionnement si ce n'est pas une feuille) :**
        *   **Lignes 44-46 : `ig <- sapply(...)`**
            *   `colnames(data)[-ncol(data)]`: Noms de toutes les colonnes sauf la dernière (la classe).
            *   `sapply(X, FUN)`: Applique la fonction `FUN` à chaque élément de `X`. Ici, pour chaque nom de colonne attribut, on calcule le `Gain` d'information.
            *   `function(x) Gain(table(data[,x], data[,ncol(data)]))`: La fonction anonyme passée à `sapply`. `x` est un nom de colonne. `table(data[,x], data[,ncol(data)])` crée la table de contingence pour l'attribut `x` et la classe.
            *   `ig` sera un vecteur de gains d'information, un pour chaque attribut.
        *   **Ligne 48 : `feature <- names(which.max(ig))`**
            *   Trouve l'attribut avec le gain d'information maximal. C'est l'attribut de division.
        *   **Ligne 54 : `node$feature <- feature`**
            *   Stocke cet attribut de division dans le nœud courant.
        *   **Ligne 58 : `childObs <- split(data, data[,feature], drop = TRUE)`**
            *   `split(data_frame, factor, drop = TRUE)`: Divise `data` en une liste de sous-dataframes. Chaque sous-dataframe correspond à une valeur unique de l'attribut `feature`. `data[,feature]` fournit le vecteur facteur pour la division. `drop = TRUE` enlève les niveaux de facteur qui n'ont pas d'observation (utile si certaines valeurs d'attribut ne sont pas présentes dans le sous-ensemble `data` actuel).
        *   **Lignes 64-69 (Boucle `for`) :**
            *   Itère sur chaque sous-ensemble `childObs[[i]]` (correspondant à une valeur de `feature`).
            *   **Ligne 66 : `child <- node$AddChild(names(childObs)[i])`**
                *   `names(childObs)[i]`: Nom de la valeur de l'attribut `feature` (ex: "Sunny", "Overcast", "Rain" si `feature` était "Outlook").
                *   `node$AddChild(...)`: Méthode de `data.tree` pour ajouter un nœud enfant au `node` courant, avec le nom spécifié.
            *   **Ligne 68 : `trainID3(child, childObs[[i]], maxHeight)`**
                *   **Appel récursif** de `trainID3` pour construire le sous-arbre à partir de ce nouveau `child` et du sous-ensemble de données `childObs[[i]]`.

---
**Q4: Combien de fonctions sont définies dans ce script ? Identifier la fonction qui implémente l'algorithme de partitionnement. Quels sont ses arguments ?**
*   **Réponse Q4 :**
    *   Il y a 4 fonctions définies dans ce script (avant la section Prédiction) :
        1.  `isPure(data)`
        2.  `entropy(vls)`
        3.  `Gain(crossTab)`
        4.  `trainID3(node, data, maxHeight)`
    *   La fonction qui implémente l'algorithme de partitionnement (ID3) est `trainID3`.
    *   Ses arguments sont :
        *   `node`: Le nœud `data.tree` actuel qui est en cours de traitement ou d'extension.
        *   `data`: Le sous-ensemble de données (dataframe) filtré qui atteint ce `node`.
        *   `maxHeight`: La profondeur maximale que l'arbre ne doit pas dépasser.

**Q5: Cette fonction est-elle récursive ou itérative ? Justifier.**
*   **Réponse Q5 :** La fonction `trainID3` est **récursive**.
    *   **Justification :** À l'intérieur de la fonction `trainID3` (ligne 68), il y a un appel à elle-même : `trainID3(child, childObs[[i]], maxHeight)`. C'est la définition d'une fonction récursive.

---
Exécution des lignes 1 à 74.

**Q6: Quel est le type de la variable `datasetDF` et quels sont ses constituants ?**
*   **Code (Lignes 74-75) :**
    ```R
    datasetDF<-read.csv(file = fileName, row.names=1,
                       colClasses = rep("character", nbrAttr+1))
    ```
    *   `read.csv(...)`: Lit un fichier CSV et le transforme en dataframe.
    *   `row.names=1`: Indique que la première colonne du CSV doit être utilisée comme noms des lignes du dataframe (ici, D1, D2, etc.).
    *   **`colClasses = rep("character", nbrAttr+1)` :** Argument très important ici.
        *   `rep("character", nbrAttr+1)`: Crée un vecteur de chaînes de caractères où chaque élément est `"character"`. Le vecteur aura `nbrAttr+1` éléments. Si `nbrAttr` est 5, cela fait 6 fois la chaîne "character".
        *   `colClasses`: Permet de spécifier le type de chaque colonne lors de la lecture. En fournissant ce vecteur, toutes les `nbrAttr+1` (donc 6) colonnes du CSV (après avoir utilisé la première pour `row.names`, il reste 5 colonnes de données + 1 colonne classe, soit "Outlook", "Temperature", "Humidity", "Wind", "PlayTennis") seront lues et stockées comme des chaînes de caractères (`character`) dans le dataframe `datasetDF`. C'est un choix fait ici pour simplifier le traitement des données catégorielles, car l'algorithme ID3 travaille nativement avec des catégories.
*   **Réponse Q6 :**
    *   Le type de la variable `datasetDF` est un **data.frame**.
    *   Ses constituants sont :
        *   **Lignes :** 14 observations, nommées de D1 à D14 (grâce à `row.names=1`).
        *   **Colonnes :** 5 variables (ou 6 si `Day` était une variable et non un row.name, mais ici `nbrAttr+1` colonnes lues après `row.names=1` implique les colonnes restantes du CSV : Outlook, Temperature, Humidity, Wind, PlayTennis). L'image montre 5 variables, ce qui est correct si la colonne "Day" a été utilisée pour `row.names`.
            *   `$ Outlook`: chr "Sunny" "Sunny" "Overcast" "Rain" ...
            *   `$ Temperature`: chr "Hot" "Hot" "Hot" "Mild" ...
            *   `$ Humidity`: chr "High" "High" "High" "High" ...
            *   `$ Wind`: chr "Weak" "Strong" "Weak" "Weak" ...
            *   `$ PlayTennis`: chr "No" "No" "Yes" "Yes" ...
        *   Toutes ces colonnes sont de type `character` à cause de l'argument `colClasses`.

---
Exécution de la ligne suivante.

**Q7: Par quelle fonction est créée la variable `tree` ? Utiliser le help pour voir la description de `Node` puis de la méthode `new()`.**
*   **Code (Ligne 76) :**
    ```R
    tree <- Node$new(rootName)
    ```
*   **Réponse Q7 :**
    *   La variable `tree` est créée par la méthode `new()` de la classe `Node` du package `data.tree`.
    *   **Description de `Node` (d'après l'aide `?Node` ou `?data.tree::Node`) :** `Node` est l'objet central du package `data.tree`. Chaque nœud dans un arbre est un objet de type `Node`. Ces objets sont liés entre eux pour former la structure de l'arbre.
    *   **Description de la méthode `new()` (d'après l'aide, souvent `?Node` puis chercher la section sur la création ou les méthodes) :**
        *   `Node$new(name, ...)` est le constructeur pour créer un nouvel objet `Node`.
        *   L'argument `name` est une chaîne de caractères qui donne le nom au nœud qui est créé. Ici, `rootName` (qui vaut "PlayTennis") est utilisé pour nommer le nœud racine de l'arbre.
        *   Cette ligne initialise donc `tree` comme étant le nœud racine de notre arbre de décision, nommé "PlayTennis". À ce stade, il n'a pas encore d'enfants.

---
**Q8: En utilisant la console vérifier le retour des méthodes `name`, `parent`, `children`, `isLeaf`, `isRoot` de la classe Node. Le résultat obtenu, était-il prévisible ?**
*   **Commandes en console (avant l'exécution de `trainID3(tree, datasetDF, maxHeight)`) :**
    ```R
    > tree$name
    [1] "PlayTennis"
    > tree$parent
    NULL
    > tree$children
    NULL  # Ou une liste vide selon l'implémentation de data.tree pour un noeud sans enfants
    > tree$isLeaf
    [1] TRUE
    > tree$isRoot
    [1] TRUE
    ```
*   **Réponse Q8 :**
    *   `tree$name`: Renvoie le nom du nœud, ici "PlayTennis". **Prévisible.**
    *   `tree$parent`: Renvoie l'objet parent du nœud. Pour le nœud racine, il n'y a pas de parent, donc `NULL`. **Prévisible.**
    *   `tree$children`: Renvoie une structure (souvent une liste nommée) des enfants du nœud. Avant que l'arbre ne soit construit par `trainID3`, la racine n'a pas d'enfants, donc `NULL` ou une liste vide. **Prévisible.**
    *   `tree$isLeaf`: Renvoie `TRUE` si le nœud est une feuille (n'a pas d'enfants), `FALSE` sinon. Initialement, la racine est une feuille. **Prévisible.**
    *   `tree$isRoot`: Renvoie `TRUE` si le nœud est la racine (n'a pas de parent), `FALSE` sinon. **Prévisible.**
    *   Oui, ces résultats sont prévisibles pour un nœud racine fraîchement créé avant la construction de l'arbre.

---
Avant d'exécuter la ligne 77, modifier `verbose` à `FALSE`, puis exécuter jusqu'à 78.

**Q9: En utilisant la console vérifier une deuxième fois le retour des méthodes `name`, `parent`, `children`, `isLeaf`, `isRoot` de la classe Node. Le résultat était-il le même que celui obtenu dans la Q8 ?**
*   **Exécution :**
    ```R
    verbose <- FALSE # (déjà fait ou à s'assurer)
    trainID3(tree, datasetDF, maxHeight) # Ligne 77
    # Ligne 78 est cat(...)
    ```
*   **Commandes en console (APRÈS exécution de `trainID3`) :**
    ```R
    > tree$name
    [1] "PlayTennis"
    > tree$parent
    NULL
    > tree$children
    $Overcast
      levelName
    1  PlayTennis/Overcast
    $Rain
      levelName
    1   PlayTennis/Rain
    $Sunny
      levelName
    1  PlayTennis/Sunny
    > tree$isLeaf
    [1] FALSE
    > tree$isRoot
    [1] TRUE
    ```
    (La sortie de `tree$children` est une représentation simplifiée ; elle montre les noms des enfants directs de la racine : "Overcast", "Rain", "Sunny", qui sont eux-mêmes des objets `Node`).
*   **Réponse Q9 :**
    *   `tree$name`: Toujours "PlayTennis". (Même résultat)
    *   `tree$parent`: Toujours `NULL`. (Même résultat)
    *   `tree$children`: **Différent.** Maintenant, la racine a des enfants (Overcast, Rain, Sunny), car `trainID3` a partitionné les données en fonction de "Outlook" (qui était l'attribut avec le gain le plus élevé). La sortie montre ces enfants.
    *   `tree$isLeaf`: **Différent.** Maintenant `FALSE`, car la racine a des enfants.
    *   `tree$isRoot`: Toujours `TRUE`. (Même résultat)
    *   Le résultat n'est donc **pas entièrement le même**. Les attributs `children` et `isLeaf` ont changé, ce qui est attendu après la construction de l'arbre.

---
Modifier `verbose` à `TRUE`, puis réexécuter le script depuis le début jusqu'à la ligne 77.

**Q10: Analyser la sortie sur console et associer chaque output à la partie du code qui en est responsable.**
*   **Exécution :**
    ```R
    verbose <- TRUE
    # ... (initialisation)
    tree <- Node$new(rootName)
    trainID3(tree, datasetDF, maxHeight)
    ```
*   **Analyse de la sortie (exemple basé sur l'image du TP) :**
    *   `*** Current Node: PlayTennis level 1`
        *   **Code responsable :** Vient probablement d'un `print(node)` ou `cat(...)` au début de `trainID3` quand `verbose` est `TRUE` (non explicitement montré dans le snippet de `trainID3` de la page 2, mais typique pour du `verbose`). `node$level` donne le niveau.
    *   `Splitting options :`
        `Outlook Temperature Humidity Wind`
        `0.24674982 0.02922257 0.15183550 0.04812703`
        *   **Code responsable :** Calcul du gain d'information `ig` (lignes 44-46). Le `sapply` calcule le gain pour chaque attribut. Le `print(ig)` (ou similaire si `verbose`) afficherait ces valeurs.
    *   `Winning attribute: Outlook Gain = 0.2467498`
        *   **Code responsable :** Après avoir trouvé `feature <- names(which.max(ig))` (ligne 48). Un `cat` ou `print` conditionné par `verbose` (ligne 49 dans le snippet, mais pourrait être lignes 49-53 dans le code complet) afficherait cela. Et `node$feature <- feature` (ligne 54) est assigné.
    *   `Split PlayTennis by Outlook`
        `got 3 children: Overcast Rain Sunny`
        *   **Code responsable :** Après `childObs <- split(...)` (ligne 58). Un `cat` ou `print` conditionné par `verbose` (ligne 56 du snippet, qui pourrait être 55-57) afficherait les noms des enfants (`names(childObs)`).
    *   `*** Current Node: PlayTennis/Overcast level 2`
        `Type: Leaf, Pure? TRUE Class: Yes`
        *   **Code responsable :** Appel récursif `trainID3(child, ...)` où `child` est "Overcast". La condition `isPure(data)` (pour les données d'"Overcast") est `TRUE`. Donc, les lignes 33, 37, 38, 39 sont exécutées. Le `print` vient d'une section `verbose` dans ce bloc `if leaf`.
    *   `*** Current Node: PlayTennis/Rain level 2`
        *   **Code responsable :** Appel récursif pour l'enfant "Rain". Les données ne sont pas pures.
    *   `Splitting options : Temperature Humidity Wind ...` (pour le nœud Rain)
        *   **Code responsable :** De nouveau, calcul de `ig` (lignes 44-46) mais pour le sous-ensemble de données de "Rain".
    *   `Winning attribute: Wind Gain = 0.9709506` (pour le nœud Rain)
        *   **Code responsable :** Sélection du meilleur attribut pour "Rain" (ligne 48).
    *   `Split Rain by Wind`
        `got 2 children: Strong Weak`
        *   **Code responsable :** `split()` pour "Rain" par "Wind" (ligne 58).
    *   `*** Current Node: PlayTennis/Rain/Strong level 3`
        `Type: Leaf, Pure? TRUE Class: No`
        *   **Code responsable :** Appel récursif pour "Rain/Strong". Devient une feuille.
    *   Et ainsi de suite pour les autres branches ("Rain/Weak", "Sunny", "Sunny/High", "Sunny/Normal").

**Q11: Dans quelles lignes du script les composants de l'arbre de décision sont créés ? Identifier dans celle-ci les fonctions responsables de la construction. Consulter le Help pour voir la description associée.**
*   **Réponse Q11 :**
    *   **Création du nœud racine :**
        *   Ligne 76 : `tree <- Node$new(rootName)`
        *   Fonction responsable : `Node$new()` du package `data.tree`. C'est le constructeur qui crée l'objet `Node` initial.
    *   **Création des nœuds enfants (et donc des branches) :**
        *   Ligne 66 (dans `trainID3`) : `child <- node$AddChild(names(childObs)[i])`
        *   Fonction responsable : `node$AddChild()` (ou plus précisément, la méthode `AddChild` de l'objet `Node`).
        *   **Description de `AddChild` (d'après l'aide `?data.tree::Node` ou en regardant les méthodes de `Node`) :** `AddChild(name)` crée un nouveau nœud avec le `name` donné et l'ajoute comme dernier enfant du nœud sur lequel la méthode est appelée (`node`). Elle retourne le nœud enfant nouvellement créé.
    *   **Assignation des attributs aux nœuds (feature, class, type, obsCount) :**
        *   Ligne 27: `node$obsCount <- nrow(data)`
        *   Ligne 37: `node$type <- "Leaf"`
        *   Ligne 38: `node$feature <- tail(names(data), 1)` (pour les feuilles)
        *   Ligne 39: `node$class <- names(which.max(table(data[,ncol(data)])))` (pour les feuilles)
        *   Ligne 54: `node$feature <- feature` (pour les nœuds internes, l'attribut de division)
        *   Ce ne sont pas des "fonctions de construction" au sens strict, mais des assignations d'attributs aux objets `Node` existants en utilisant l'opérateur `$`.

---
**Q12: Identifier dans la fonction la partie responsable de l'arrêt de la récursion. Quelles sont les conditions d'arrêt associées ?**
*   **Réponse Q12 :**
    *   La partie responsable de l'arrêt de la récursion dans la fonction `trainID3` est la structure conditionnelle `if` à la ligne 31 :
        ```R
        if (isPure(data) | node$level == (maxHeight + 1)){
          # ... code pour créer une feuille ...
        } else {
          # ... code pour partitionner et appeler récursivement ...
        }
        ```
    *   **Conditions d'arrêt associées :**
        1.  **`isPure(data)` :** Si le sous-ensemble de données `data` associé au nœud courant est "pur", c'est-à-dire que toutes les instances de ce sous-ensemble appartiennent à la même classe. Dans ce cas, le nœud devient une feuille et la récursion s'arrête pour cette branche.
        2.  **`node$level == (maxHeight + 1)` :** Si la profondeur (`level`) du nœud courant atteint la profondeur maximale autorisée (`maxHeight + 1`). `node$level` est 1 pour la racine. Si `maxHeight` est 3, cela signifie qu'on autorise des nœuds jusqu'au niveau 3. Si un nœud est au niveau 4 (`maxHeight + 1`), il doit devenir une feuille, même s'il n'est pas pur. Cela empêche l'arbre de devenir trop profond.

**Q13: Que fait la fonction `isPure()` ?**
*   **Code : `length(unique(data[,ncol(data)])) == 1`**
*   **Réponse Q13 :**
    La fonction `isPure(data)` vérifie si toutes les instances dans le sous-ensemble de données `data` appartiennent à la même classe cible.
    *   `data[,ncol(data)]` sélectionne la dernière colonne du dataframe `data` (qui est supposée être la colonne de la classe).
    *   `unique(...)` extrait les valeurs uniques de cette colonne de classe.
    *   `length(...)` compte combien il y a de classes uniques.
    *   `== 1` compare ce nombre à 1. Si le nombre de classes uniques est 1, cela signifie que toutes les instances ont la même classe, et la fonction retourne `TRUE` (le jeu de données est pur). Sinon, elle retourne `FALSE`.

**Q14: En utilisant le Help déterminer ce que fait la fonction `tail(names(data), 1)`.**
*   **Réponse Q14 :**
    *   `names(data)`: Renvoie un vecteur de chaînes de caractères contenant les noms de toutes les colonnes du dataframe `data`.
    *   `tail(vector, n)`: La fonction `tail()` renvoie les `n` derniers éléments d'un vecteur (ou d'un autre objet similaire).
    *   Donc, `tail(names(data), 1)` renvoie le **dernier nom de colonne** du dataframe `data`. Dans le contexte de `trainID3` (ligne 38, quand un nœud devient une feuille), `data` est le sous-ensemble d'apprentissage, et la dernière colonne est la classe cible (par exemple, "PlayTennis"). Ainsi, cette expression récupère le nom de la colonne de la classe cible.

**Q15: Reprendre les commandes suivantes sur votre console, puis déduire ce que fait le code de la ligne 39.**
*   **Commandes console (exemple avec `datasetDF` complet) :**
    ```R
    > table(datasetDF[,ncol(datasetDF)]) # ncol(datasetDF) est 5 (PlayTennis)
    No Yes
     5   9  # 5 "No", 9 "Yes" dans tout le dataset

    > which.max(table(datasetDF[,ncol(datasetDF)]))
    Yes  # 'Yes' est la classe avec la fréquence maximale
     2   # L'index de 'Yes' dans la table est 2 (No est 1, Yes est 2)

    > names(which.max(table(datasetDF[,ncol(datasetDF)])))
    [1] "Yes" # Le nom associé à l'index 2 est "Yes"
    ```
*   **Code de la ligne 39 : `node$class <- names(which.max(table(data[,ncol(data)])))`**
*   **Réponse Q15 :**
    Cette ligne de code détermine et assigne la **classe majoritaire** du sous-ensemble de données `data` au nœud feuille courant.
    1.  `data[,ncol(data)]`: Sélectionne la colonne de la classe cible du sous-ensemble `data`.
    2.  `table(...)`: Crée une table de fréquences des différentes valeurs de classe (par exemple, combien de "Yes" et combien de "No").
    3.  `which.max(...)`: Renvoie l'index de l'élément ayant la valeur maximale dans cette table de fréquences. Si la table est `No: 3, Yes: 7`, `which.max` renverra l'index correspondant à "Yes".
    4.  `names(...)`: Renvoie le nom de l'élément à cet index. Donc, si "Yes" est majoritaire, cela renverra la chaîne `"Yes"`.
    Ce nom de classe majoritaire est ensuite assigné à l'attribut `class` du nœud (`node$class`).

**Q16: Exécuter les lignes 78 et 79 puis vérifier si l'arbre obtenu est celui attendu.**
*   *(Note: L'énoncé original dit lignes 81 et 82, mais l'image de la page 2 montre les lignes 78, 79, 80 pour l'affichage/plot. Je vais suivre l'image de la page 2)*
*   **Code :**
    ```R
    78 cat("\n *** Final tree: \n")
    79 print(tree, "feature", "obsCount", "type", "class")
    80 plot(tree) # (Ligne 80 si on inclut le plot)
    ```
*   **Réponse Q16 :**
    *   L'exécution de la ligne 78 affiche simplement l'en-tête "*** Final tree:***".
    *   L'exécution de la ligne 79 affiche la structure textuelle de l'arbre, comme vu dans la Q2. Les attributs "feature", "obsCount", "type", et "class" sont affichés pour chaque nœud.
    *   Si on exécute aussi la ligne 80, une représentation graphique de l'arbre s'affiche.
    *   Oui, l'arbre obtenu (à la fois textuellement et graphiquement) correspond à l'arbre de décision attendu pour le dataset PlayTennis, généralement avec "Outlook" comme racine, puis des divisions basées sur "Wind" ou "Humidity" etc., menant à des prédictions "Yes" ou "No". L'arbre affiché dans le TP à la page 1/5 est un exemple de ce résultat attendu.

**Q17: Expliquer les informations portées sur la représentation de l'arbre sur la console.**
*   **Réponse Q17 :** (Similaire à Q3, mais peut-être plus focus sur la sortie de `print` de la Q16)
    La représentation de l'arbre sur la console (via `print(tree, "feature", "obsCount", "type", "class")`) montre la hiérarchie de l'arbre de décision.
    *   Chaque ligne représente un nœud.
    *   **`levelName` :** Indique la position hiérarchique du nœud. La racine est au premier niveau (ex: `1 PlayTennis`). Les enfants sont indentés et préfixés par `¦--` ou `°--`. Par exemple, `2  ¦--Overcast` est un enfant de `PlayTennis`. `PlayTennis/Overcast` serait son nom complet de chemin.
    *   **`feature` :**
        *   Pour un nœud interne : L'attribut utilisé pour la division à ce nœud (ex: `Outlook` pour la racine).
        *   Pour un nœud feuille : Le nom de la colonne classe cible (ex: `PlayTennis` si la classe est "Yes" ou "No", ou directement la classe prédite si `node$feature` a été modifié comme tel pour les feuilles). D'après la sortie de Q2, pour les feuilles, `feature` est "PlayTennis" et `class` est "Yes" ou "No".
    *   **`obsCount` :** Le nombre d'instances du jeu de données d'entraînement qui atteignent ce nœud.
    *   **`type` :** `Leaf` si c'est un nœud terminal (une décision), ou vide/autre chose si c'est un nœud interne qui continue de diviser.
    *   **`class` :** Uniquement pertinent pour les nœuds `Leaf`. C'est la prédiction de classe ("Yes" ou "No") pour les instances atteignant cette feuille.

---
On veut apporter des modifications sur le code afin d'avoir la classe de sortie mentionnée sur chaque feuille (voir arbre dans la page suivante - page 6/8 du PDF).

**Q18: A quel endroit faut-il intervenir et comment ? (indication : utiliser la fonction `paste()`)**
*   **Analyse :** L'arbre de la page 6/8 (ex: "PlayTennis.png") montre des feuilles nommées "Overcast-Yes", "Strong-No", "Weak-Yes", etc. Cela signifie que le *nom* du nœud feuille (utilisé par `plot()`) combine la valeur de l'attribut parent qui a mené à cette feuille et la classe prédite à cette feuille.
    La fonction `print()` utilise `levelName` qui est construit à partir des noms des nœuds. Si le nom du nœud change, `levelName` changera aussi.
*   **Endroit où intervenir :** Dans la fonction `trainID3`, lorsque l'on détermine qu'un nœud est une feuille. C'est-à-dire dans le bloc `if (isPure(data) | node$level == (maxHeight + 1))` (lignes 31-40).
*   **Comment intervenir :**
    Après avoir déterminé la classe du nœud (ligne 39 : `node$class <- ...`), il faut modifier le nom du nœud lui-même. Le nom actuel du nœud a été défini lors de sa création par `node$AddChild(NOM_VALEUR_ATTRIBUT)` (ligne 66). Il faut donc concaténer ce nom existant avec la classe.
    ```R
    # Dans trainID3, à l'intérieur du bloc if qui définit une feuille :
    # (ligne 31) if (isPure(data) | node$level == (maxHeight + 1)){
    #   ...
    #   (ligne 37) node$type <- "Leaf"
    #   (ligne 38) node$feature <- tail(names(data), 1) # Nom de la colonne classe
        classe_predite <- names(which.max(table(data[,ncol(data)])))
    #   (ligne 39) node$class <- classe_predite
        # MODIFICATION SUGGÉRÉE ICI :
        node$name <- paste(node$name, classe_predite, sep = "-") # Ex: "Overcast" devient "Overcast-Yes"
    #   if (verbose){...}
    # }
    ```
    `node$name` fait référence au nom du nœud courant. Si ce nœud a été créé avec le nom "Overcast" (par l'appel `AddChild` du parent) et que sa `classe_predite` est "Yes", `paste(node$name, classe_predite, sep = "-")` produira "Overcast-Yes". Ce nouveau nom sera utilisé par `plot()` et dans la construction du `levelName` pour `print()`.

**Q19: Modifier le code puis réexécuter le code tout-entier jusqu'à la ligne 79.**
*   **Réponse Q19 :** Il faut appliquer la modification de Q18, puis relancer tout le script. La sortie de `print(tree, ...)` à la ligne 79 devrait maintenant refléter ces noms modifiés dans la colonne `levelName`.
    Par exemple, au lieu de :
    `2  ¦--Overcast PlayTennis       4 Leaf   Yes`
    On pourrait avoir quelque chose comme :
    `2  ¦--Overcast-Yes PlayTennis       4 Leaf   Yes`
    (Le `levelName` est `PlayTennis/Overcast-Yes`. La colonne `feature` pour la feuille sera toujours "PlayTennis", et `class` sera "Yes").
    Le `plot(tree)` (ligne 80) affichera alors les étiquettes de feuilles comme "Overcast-Yes".

---
**Q20: Quels sont les arguments envoyés lors de l'appel à la fonction de calcul du gain d'information à la ligne 47?**
*   *(Note: la ligne de calcul d'IG est 44-46, l'appel à `Gain` est dans la fonction anonyme)*
    ```R
    # Lignes 44-46
    ig <- sapply(colnames(data)[-ncol(data)],
                 function(x) Gain(table(data[,x], data[,ncol(data)]))
    )
    ```
*   **Réponse Q20 :**
    La fonction `Gain` est appelée avec un seul argument, qui est `table(data[,x], data[,ncol(data)])`.
    *   `x`: est une chaîne de caractères, le nom d'un attribut prédicteur (ex: "Outlook", "Temperature", ...). Il est fourni par `sapply` qui itère sur `colnames(data)[-ncol(data)]`.
    *   `data[,x]`: sélectionne la colonne de l'attribut `x` dans le sous-ensemble de données `data`.
    *   `data[,ncol(data)]`: sélectionne la colonne de la classe cible dans `data`.
    *   `table(data[,x], data[,ncol(data)])`: crée une **table de contingence** (ou tableau croisé) qui compte les occurrences pour chaque combinaison de valeurs de l'attribut `x` et de la classe cible. C'est cette table qui est passée comme argument `crossTab` à la fonction `Gain`.
    *   La sortie console `> colnames(datasetDF)[-ncol(datasetDF)]` montre `[1] "Outlook" "Temperature" "Humidity" "Wind"`. `sapply` va donc appeler `Gain` quatre fois, une fois pour la table de contingence de chacun de ces attributs avec la classe.

**Q21: Que fait le code de la ligne 58 ? Consulter la description qui suit de la fonction `split()` et analyser le retour de la commande suivante :**
*   **Code Ligne 58 : `childObs <- split(data, data[,feature], drop = TRUE)`**
*   **Description de `split(x, f, ...)` :**
    *   `x`: Un vecteur ou un dataframe à diviser.
    *   `f`: Un facteur (ou quelque chose qui peut être converti en facteur) qui définit les groupes. La longueur de `f` doit être la même que le nombre de lignes de `x` si `x` est un dataframe, ou la longueur de `x` si `x` est un vecteur.
    *   `split` divise `x` en une **liste** de composants. Chaque composant de la liste correspond à un niveau du facteur `f`.
*   **Analyse du retour de la commande `> split(datasetDF[,-1], datasetDF[,1])`**
    *   `datasetDF[,1]` : Première colonne de `datasetDF` (qui est "Day" si `row.names=1` n'a pas été appliqué, ou "Outlook" si "Day" a été utilisé comme `row.names`). L'image montre `row.names=1`, donc `datasetDF[,1]` est la colonne "Outlook".
    *   `datasetDF[,-1]` : Toutes les colonnes de `datasetDF` SAUF la première.
    *   Cette commande `split` va donc diviser les colonnes 2 à la fin de `datasetDF` en fonction des valeurs uniques de la première colonne ("Outlook"). Elle créera une liste avec des éléments nommés "Overcast", "Rain", "Sunny". Chaque élément sera un dataframe contenant les lignes de `datasetDF[,-1]` où "Outlook" avait la valeur correspondante.
*   **Réponse Q21 (pour la ligne 58) :**
    *   `data`: Le dataframe actuel (un sous-ensemble des données d'entraînement).
    *   `feature`: Le nom de l'attribut choisi pour la division (ex: "Outlook").
    *   `data[,feature]`: Le vecteur des valeurs de cet attribut pour toutes les instances dans `data`. Ce vecteur sera utilisé comme facteur de division.
    *   `drop = TRUE`: Si certaines valeurs de `feature` ne sont pas présentes dans le `data` actuel (ce qui est peu probable ici car `feature` est choisi à partir de `data`), les groupes vides correspondants ne seraient pas créés dans la liste.
    *   La ligne 58 divise donc le dataframe `data` en une **liste de sous-dataframes**. Chaque sous-dataframe dans la liste `childObs` contient les instances de `data` qui partagent la même valeur pour l'attribut `feature`. Les éléments de la liste `childObs` sont nommés d'après ces valeurs uniques de `feature`. Par exemple, si `feature` est "Outlook", `childObs` contiendra `$Sunny`, `$Overcast`, `$Rain`.

**Q22: Déduire ce que fait le code des lignes 65-66.**
*   *(Note: l'image montre la ligne 64 pour le `for`, 65 pour le commentaire, 66 pour `child <- ...`, 67 pour commentaire, 68 pour appel récursif)*
    ```R
    64 for(i in 1:length(childObs)) {
    65   #construct a child having the name of that feature value
    66   child <- node$AddChild(names(childObs)[i])
    67   #call the algorithm recursively
    68   trainID3(child, childObs[[i]], maxHeight)
    69 }
    ```
*   **Réponse Q22 :**
    Ces lignes itèrent sur chaque groupe de données (chaque `childObs[[i]]`) créé par la division de la ligne 58.
    *   **Ligne 64 : `for(i in 1:length(childObs))`**
        *   Démarre une boucle qui va s'exécuter autant de fois qu'il y a de valeurs uniques pour l'attribut de division `feature` (c'est-à-dire autant d'éléments dans la liste `childObs`).
    *   **Ligne 66 : `child <- node$AddChild(names(childObs)[i])`**
        *   `names(childObs)`: Renvoie un vecteur des noms des éléments de la liste `childObs`. Ces noms sont les valeurs uniques de l'attribut `feature` (ex: "Sunny", "Overcast", "Rain").
        *   `names(childObs)[i]`: Récupère la i-ème valeur de cet attribut (ex: pour `i=1`, si le premier enfant est "Sunny", cela donne "Sunny").
        *   `node$AddChild(...)`: Crée un nouveau nœud enfant sous le `node` courant. Ce nœud enfant est nommé d'après la valeur de l'attribut (`names(childObs)[i]`). Le nœud enfant nouvellement créé est assigné à la variable `child`.
        *   Essentiellement, cette ligne **crée une nouvelle branche dans l'arbre** pour chaque valeur possible de l'attribut de division.

**Q23: Déduire avec quels arguments est fait l'appel récursif ?**
*   **Code Ligne 68 : `trainID3(child, childObs[[i]], maxHeight)`**
*   **Réponse Q23 :**
    L'appel récursif à `trainID3` est fait avec les arguments suivants :
    1.  **`child` :** C'est le premier argument (qui correspond à `node` dans la définition de `trainID3`). Il s'agit du nœud enfant qui vient d'être créé à la ligne 66. La construction de l'arbre continue à partir de ce nouveau nœud.
    2.  **`childObs[[i]]` :** C'est le deuxième argument (qui correspond à `data`). Il s'agit du sous-ensemble de données (un dataframe) qui correspond à la valeur `names(childObs)[i]` de l'attribut de division. C'est sur ce sous-ensemble plus petit que l'algorithme va maintenant travailler pour le nœud `child`.
    3.  **`maxHeight` :** C'est le troisième argument. Il est passé inchangé. La contrainte de profondeur maximale s'applique uniformément à tout l'arbre.

---

**B. Prédiction**

Considérons la suite du code suivante :
```R
82 # Using the final tree for output class prediction
83 predictID3 <- function(tree, features) {
84   node <- tree$children[[features[[tree$feature]]]]
85   if (node$isLeaf)
86     return (node$class)
87   return(predictID3(node, features))
88 }
89
90 names(newObject) <- names(datasetDF)[-ncol(datasetDF)]
91 pred <- predictID3(tree, newObject)
92 cat("\n Pour l'exemple:\n"); print(newObject);
93 cat(" ", names(datasetDF)[ncol(datasetDF)],"?", pred)
```

**Q1: Quelles sont les valeurs d'attributs du nouvel individu ?**
*   **Code :**
    *   Ligne 8: `newObject <- c("Rain", "Mild", "High", "Strong")`
    *   Ligne 90: `names(newObject) <- names(datasetDF)[-ncol(datasetDF)]`
        *   `names(datasetDF)[-ncol(datasetDF)]` donne les noms des colonnes de `datasetDF` sauf la dernière (la classe). Ce sera `c("Outlook", "Temperature", "Humidity", "Wind")`.
        *   Ces noms sont assignés comme noms aux éléments du vecteur `newObject`.
*   **Réponse Q1 :**
    Après la ligne 90, `newObject` est un vecteur nommé :
    *   Outlook: "Rain"
    *   Temperature: "Mild"
    *   Humidity: "High"
    *   Wind: "Strong"
    Les valeurs d'attributs sont donc "Rain", "Mild", "High", "Strong" pour Outlook, Temperature, Humidity, et Wind respectivement. La sortie console `> newObject` le confirme.

**Q2: En utilisant l'arbre obtenu, quelle doit être la valeur de la classe de sortie associée ?**
*   **Arbre obtenu (voir Q2 du TP) :**
    1.  Racine (`PlayTennis`), divise sur `Outlook`. `newObject$Outlook` est "Rain". On suit la branche "Rain".
    2.  Nœud `Rain`, divise sur `Wind`. `newObject$Wind` est "Strong". On suit la branche "Strong".
    3.  Nœud `Rain/Strong` est une feuille. Sa classe est "No".
*   **Réponse Q2 :** La classe de sortie associée doit être **"No"**.

**Q3: Quels sont les arguments envoyés à la fonction `predictID3()`?**
*   **Code Ligne 91 : `pred <- predictID3(tree, newObject)`**
*   **Réponse Q3 :**
    Les arguments envoyés à la fonction `predictID3` lors du premier appel (ligne 91) sont :
    1.  **`tree` :** C'est le premier argument. Il s'agit de l'objet `Node` qui représente la racine de l'arbre de décision complet qui a été construit à l'étape d'entraînement.
    2.  **`newObject` :** C'est le deuxième argument (qui correspond à `features` dans la définition de `predictID3`). Il s'agit du vecteur nommé contenant les valeurs des attributs du nouvel individu pour lequel on veut faire une prédiction.

**Q4: Que fait la ligne de code 84?**
*   **Code Ligne 84 : `node <- tree$children[[features[[tree$feature]]]]`**
*   **Réponse Q4 :** Cette ligne est cruciale pour la navigation dans l'arbre de décision lors de la prédiction. Décortiquons-la :
    1.  **`tree$feature` :** Récupère le nom de l'attribut sur lequel le nœud `tree` actuel effectue sa division (par exemple, si `tree` est la racine, `tree$feature` pourrait être "Outlook").
    2.  **`features[[tree$feature]]` :**
        *   `features` est le vecteur nommé du nouvel individu (ex: `newObject`).
        *   En utilisant le nom de l'attribut (`tree$feature`) comme index (ex: `"Outlook"`), cette partie extrait la valeur de cet attribut pour le nouvel individu (ex: `features[["Outlook"]]` donnerait "Rain" si `newObject$Outlook` est "Rain"). Le résultat est une chaîne de caractères (ex: "Rain").
    3.  **`tree$children[[ ... ]]` :**
        *   `tree$children` est la liste des nœuds enfants du nœud `tree` actuel. Cette liste est nommée par les valeurs de l'attribut de division (ex: les enfants de la racine pourraient être nommés "Sunny", "Overcast", "Rain").
        *   En utilisant la valeur extraite à l'étape précédente (ex: "Rain") comme nom d'index, on sélectionne le nœud enfant approprié.
    4.  **`node <- ...` :** Le nœud enfant sélectionné est assigné à la variable `node`.
    *   Donc, la ligne 84 **fait descendre d'un niveau dans l'arbre**, en choisissant la branche (le nœud enfant) qui correspond à la valeur de l'attribut de division du nœud courant pour l'individu `features`.

**Q5: Quels sont les arguments modifiés lors de l'appel récursif (ligne 87) de la fonction `predictID3()`?**
*   **Code Ligne 87 : `return(predictID3(node, features))`**
*   **Réponse Q5 :**
    Lors de l'appel récursif :
    1.  Le premier argument, qui était `tree` dans l'appel précédent, devient **`node`**. `node` est le nœud enfant qui a été sélectionné à la ligne 84. C'est donc le sous-arbre à partir duquel la prédiction continue. L'argument `tree` est donc **modifié** pour pointer vers un niveau plus profond de l'arbre original.
    2.  Le deuxième argument, `features`, est **passé inchangé**. Les caractéristiques de l'individu à prédire restent les mêmes tout au long de la descente dans l'arbre.

**Important: Restituer la (ou les) ligne de code à son état initial avant la modif effectuée dans Q19.**
*   **Réponse :** Si la modification de Q19 (concernant `node$name <- paste(...)`) a été faite, il faut la commenter ou la supprimer pour que la prédiction (ligne 84) fonctionne correctement, car elle s'attend à ce que les noms des enfants (`tree$children`) correspondent directement aux valeurs des attributs (ex: "Rain", et non "Rain-Yes").
    Donc, la ligne que vous auriez ajoutée ou modifiée dans `trainID3` pour Q18/Q19 doit être remise à son état d'origine (ou la modification doit être faite d'une manière qui n'affecte pas la navigation, par exemple en utilisant un attribut de nœud séparé pour l'affichage si nécessaire).

**Q6: Exécuter le code depuis le début jusqu'à sa fin, puis vérifier si le résultat obtenu est celui attendu.**
*   **Réponse Q6 :**
    Après avoir exécuté tout le script (en s'assurant que la modification de Q19 est annulée ou gérée), la sortie finale (ligne 93) devrait être :
    ```
    PlayTennis ? No
    ```
    Ceci correspond au résultat attendu, comme déterminé manuellement dans la Q2. Le script prédit correctement "No" pour l'individu `newObject`.

---

**C. Étape de test (Homework)**

Cette section vous demande d'étendre le script.

1.  **Décomposition en `trainDataset` et `testDataset` :** Vous devrez utiliser des fonctions comme `sample()` pour sélectionner aléatoirement des lignes pour `trainDataset`. Le reste ira dans `testDataset`. `sampleRate` contrôlera la proportion.
2.  **`sampleRate` :** Une variable pour définir le pourcentage de données à utiliser pour l'entraînement.
3.  **Affichage de la matrice de confusion, accuracy, taux d'erreur :**
    *   Après avoir entraîné l'arbre sur `trainDataset`, vous l'utiliserez pour prédire les classes des instances de `testDataset`.
    *   **Matrice de confusion :** `table(predictions_reelles_test, predictions_faites_par_arbre)`
    *   **Accuracy :** `sum(diag(matrice_confusion)) / sum(matrice_confusion)`
    *   **Taux d'erreur :** `1 - accuracy`
4.  **Prédiction "UnDef" (Undefined) :**
    *   La fonction `predictID3` doit être modifiée. Si à la ligne 84, `features[[tree$feature]]` donne une valeur pour laquelle il n'y a pas d'enfant (c'est-à-dire `tree$children[[VALEUR_INCONNUE]]` est `NULL` ou n'existe pas), alors la fonction doit retourner "UnDef".
    *   Cela peut se produire si une valeur d'attribut dans un individu de test n'a jamais été vue pour cet attribut lors de la division pendant l'entraînement sur cette branche spécifique.
    *   Modification (conceptuelle) pour `predictID3`:
        ```R
        predictID3 <- function(tree, features) {
          valeur_attribut_individu <- features[[tree$feature]]
          enfant_choisi <- tree$children[[valeur_attribut_individu]]

          if (is.null(enfant_choisi)) { # Si la branche n'existe pas pour cette valeur
            return("UnDef")
          }

          if (enfant_choisi$isLeaf) {
            return(enfant_choisi$class)
          }
          return(predictID3(enfant_choisi, features))
        }
        ```
5.  **Gestion de "UnDef" :** Si des prédictions "UnDef" sont produites pour le `testDataset`, le script doit :
    *   Afficher les individus du `testDataset` qui ont conduit à "UnDef".
    *   Demander à l'utilisateur de modifier `trainDataset` (implicitement en augmentant `sampleRate` pour potentiellement inclure plus de diversité dans l'entraînement) et de réessayer.

**Q1 (Homework): Créer un fichier de récupération de votre script puis apporter les modifications nécessaires pour l'extension.**
*   **Réponse :** Cela signifie sauvegarder votre script actuel (celui jusqu'à la partie B), puis commencer à le modifier pour implémenter les points 1 à 5 ci-dessus.

**Q2 (Homework): Pour le cas avec échec, pourquoi l'individu D7 donne un échec de prédiction ?**
*   **Contexte :** L'image de la page 8/8 (droite) montre un scénario où D7 (`Overcast, Cool, Normal, Strong, Yes`) donne un échec. L'arbre de décision qui est montré dans ce cas a `Temperature` comme racine.
*   **Traçage pour D7 sur l'arbre de l'échec (page 8, droite) :**
    1.  Nœud Racine: `Temperature`. Pour D7, `Temperature` est `Cool`. On suit la branche `Cool`.
    2.  Nœud `Temperature:Cool`: Divise sur `Outlook`. Pour D7, `Outlook` est `Overcast`.
    3.  Enfants du nœud `Temperature:Cool` dans cet arbre spécifique : On voit qu'il a des enfants pour `Outlook=Rain` et `Outlook=Sunny`. Il **n'a pas** d'enfant pour `Outlook=Overcast`.
*   **Réponse Q2 :** L'individu D7 (`Outlook=Overcast, Temperature=Cool, ...`) donne un échec de prédiction avec l'arbre de droite (page 8) parce que :
    Après avoir suivi la branche `Temperature=Cool`, l'arbre tente de diviser sur `Outlook`. La valeur d'Outlook pour D7 est `Overcast`. Cependant, dans ce sous-arbre spécifique (sous `Temperature=Cool`), il n'y a pas de branche (pas d'enfant) correspondant à `Outlook=Overcast` qui aurait été apprise lors de la phase d'entraînement (avec le `Training Dataset` plus petit de cet exemple). La fonction `predictID3` (modifiée) trouverait `tree$children[["Overcast"]]` comme étant `NULL` à ce point et retournerait "UnDef".

**Q3 (Homework): Vérifier les résultats de ces deux retours manuellement.**
*   **Réponse :** Cela vous demande de prendre les deux arbres finaux des exemples de la page 8/8, et les `Test Dataset` respectifs, et de "jouer" manuellement à la prédiction pour chaque individu du `Test Dataset` pour construire la matrice de confusion et calculer l'accuracy/taux d'erreur, puis de comparer avec ce que votre script étendu produirait.

---

J'espère que cette explication détaillée et en français vous aide à mieux comprendre chaque aspect de ce TP ! N'hésitez pas si vous avez d'autres questions sur des points spécifiques.