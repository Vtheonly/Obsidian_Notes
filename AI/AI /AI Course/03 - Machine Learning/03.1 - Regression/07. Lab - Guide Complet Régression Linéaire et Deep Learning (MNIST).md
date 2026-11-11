
# Guide Complet : Régression Linéaire et Deep Learning (MNIST)

Ce document sert de référence pour comprendre l'intégralité du code, des concepts théoriques et des implémentations Python réalisées dans le cadre des travaux pratiques sur la régression linéaire avec Scikit-Learn et la classification d'images avec Keras.

---

## Partie 1 : La Régression Linéaire Simple et Multiple

### 1. Théorie et Mathématiques
La régression linéaire est une approche statistique pour modéliser la relation entre une variable dépendante (cible, notée $y$) et une ou plusieurs variables indépendantes (caractéristiques ou features, notées $X$).

**L'équation mathématique :**
Dans le cas simple, le modèle cherche à établir une relation linéaire de la forme :
$$y = \beta_0 + \beta_1 x + \epsilon$$

*   $\beta_0$ (l'ordonnée à l'origine) : La valeur de $y$ lorsque $x$ est nul.
*   $\beta_1$ (le coefficient ou la pente) : Indique de combien $y$ augmente lorsque $x$ augmente d'une unité.
*   $\epsilon$ (le terme d'erreur) : Représente le bruit ou la variabilité que le modèle ne peut pas expliquer.

Dans notre cas (régression multiple avec 3 caractéristiques), l'équation devient vectorielle :
$$y = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \beta_3 x_3$$

**L'objectif de l'algorithme :**
Le but est de trouver les valeurs optimales des coefficients ($\beta$) qui minimisent l'erreur entre les prédictions du modèle et les données réelles. La méthode la plus courante est celle des **Moindres Carrés Ordinaires**, qui cherche à minimiser la somme des carrés des écarts (résidus).

### 2. Analyse du Code (Scikit-Learn)

#### Bloc 1 : Importation des bibliothèques
```python
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_regression
from sklearn.metrics import mean_squared_error
```
*   **NumPy (`np`)** : Bibliothèque fondamentale pour le calcul scientifique en Python. Elle permet de gérer des tableaux multidimensionnels (matrices) de manière performante, ce qui est essentiel car les données sont représentées sous forme de matrices.
*   **Scikit-Learn (`sklearn`)** : La bibliothèque standard pour le machine learning classique en Python.
    *   `LinearRegression` : Une classe qui implémente l'algorithme des moindres carrés.
    *   `make_regression` : Un générateur de données synthétiques utile pour tester des modèles sans avoir besoin de fichiers externes.
    *   `mean_squared_error` : Une fonction mathématique pour évaluer la performance.

#### Bloc 2 : Génération des données
```python
x, y = make_regression(n_samples=100, n_features=3, noise=10, random_state=42)
```
Ce code crée un jeu de données artificiel contrôlé :
*   `n_samples=100` : On génère 100 points de données (lignes).
*   `n_features=3` : Chaque point possède 3 variables explicatives. $X$ est donc une matrice de dimension (100, 3).
*   `noise=10` : Ajoute un bruit gaussien aux données. Sans cela, la relation serait parfaitement linéaire et le modèle aurait une précision de 100%, ce qui n'est pas réaliste. Cela simule les imperfections du monde réel.
*   `random_state=42` : Fixe la graine aléatoire. Cela garantit que les nombres aléatoires générés sont les mêmes à chaque exécution du code, assurant la reproductibilité des résultats.

#### Bloc 3 : Initialisation et Entraînement
```python
model = LinearRegression()
model.fit(x, y)
```
C'est l'étape centrale de l'apprentissage automatique.
*   `model = LinearRegression()` : On crée une instance de la classe. À ce stade, le modèle est une "coquille vide" ; ses paramètres internes (les coefficients $\beta$) ne sont pas encore calculés.
*   `model.fit(x, y)` : Cette méthode lance l'algorithme d'optimisation. Le code prend la matrice $X$ et le vecteur $y$, et calcule mathématiquement les coefficients qui minimisent l'erreur globale. Une fois cette ligne exécutée, le modèle est "entraîné".

#### Bloc 4 : Prédiction
```python
preds = model.predict(x)
```
On utilise le modèle entraîné pour prédire des valeurs. L'algorithme applique l'équation $y = \beta X + \beta_0$ en utilisant les coefficients qu'il vient d'apprendre. Ici, on prédit sur les mêmes données que celles utilisées pour l'entraînement (ce qui est une simplification pour ce TP d'introduction).

#### Bloc 5 : Évaluation (MSE et Score)
```python
mse = mean_squared_error(y, preds)
score = model.score(x, y)
```
Nous utilisons deux métriques pour juger la qualité du modèle :
1.  **MSE (Mean Squared Error)** : C'est la moyenne des carrés des erreurs.
    *   Formule : $\frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2$.
    *   Elle quantifie la "distance" moyenne entre la ligne de régression et les points de données. Plus elle est basse, mieux c'est.
2.  **Score ($R^2$ ou Coefficient de détermination)** :
    *   Il mesure la proportion de la variance de la variable dépendante qui est expliquée par les variables indépendantes.
    *   Un score de 1.0 signifie une prédiction parfaite.
    *   Un score de 0.0 signifie que le modèle ne fait pas mieux qu'une simple moyenne.

---

## Partie 2 : Introduction au Deep Learning (Classification MNIST)

### 1. Théorie et Concepts
Ici, nous passons de la statistique classique aux **Réseaux de Neurones Artificiels**. Le problème est la classification : attribuer une étiquette (un chiffre de 0 à 9) à une image.

**Le Dataset MNIST :**
C'est le "Hello World" du Deep Learning. Il contient 70 000 images de chiffres manuscrits en niveaux de gris. Chaque image fait 28x28 pixels.
*   **Entrées ($X$)** : La valeur de luminosité des pixels (entre 0 et 255).
*   **Sorties ($Y$)** : La catégorie du chiffre (0, 1, ..., 9).

**Le Perceptron Multicouche (MLP) :**
Le modèle utilisé est un réseau dense (fully connected). Chaque neurone d'une couche est connecté à tous les neurones de la couche suivante.
Le calcul effectué par un neurone est :
$$Sortie = FonctionActivation(\sum (Poids \times Entrée) + Biais)$$

### 2. Analyse du Code (Keras/TensorFlow)

#### Bloc 1 : Chargement et division des données
```python
from tensorflow.keras.datasets import mnist
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
```
Cette étape sépare les données en deux ensembles distincts, un principe fondamental en Machine Learning :
1.  **Ensemble d'entraînement (Train)** : 60 000 images utilisées par le réseau pour ajuster ses poids (apprendre).
2.  **Ensemble de test (Test)** : 10 000 images que le réseau ne voit jamais pendant l'apprentissage. Elles servent à vérifier si le modèle sait généraliser sur de nouvelles données et n'a pas simplement "appris par cœur" (overfitting).

#### Bloc 2 : Architecture du Réseau
```python
from tensorflow.keras import models, layers
network = models.Sequential()
network.add(layers.Dense(512, activation='relu', input_shape=(28 * 28,)))
network.add(layers.Dense(10, activation='softmax'))
```
*   `Sequential()` : Indique que le modèle est une pile linéaire de couches. Les données passent de l'une à l'autre dans l'ordre.
*   **Première couche (Cachée)** : `Dense(512, activation='relu')`.
    *   Elle contient 512 neurones. C'est la capacité d'apprentissage du modèle.
    *   `input_shape=(28 * 28,)` : Elle attend un vecteur plat de 784 valeurs (les pixels).
    *   `relu` (Rectified Linear Unit) : Fonction d'activation qui remplace les valeurs négatives par zéro. Elle introduit de la non-linéarité, permettant au réseau d'apprendre des formes complexes.
*   **Dernière couche (Sortie)** : `Dense(10, activation='softmax')`.
    *   Elle contient 10 neurones, correspondant aux 10 classes possibles (chiffres 0 à 9).
    *   `softmax` : Transforme les sorties brutes du réseau en une distribution de probabilités. La somme des 10 sorties vaudra 1. Le neurone avec la valeur la plus haute désigne le chiffre prédit.

#### Bloc 3 : Compilation
```python
network.compile(optimizer='rmsprop',
                loss='categorical_crossentropy',
                metrics=['accuracy'])
```
Cette étape configure le processus d'apprentissage :
*   **Optimizer ('rmsprop')** : C'est l'algorithme qui met à jour les poids du réseau. Il utilise le gradient de l'erreur pour "descendre" vers la solution optimale. RMSprop est une variante avancée de la descente de gradient qui adapte la vitesse d'apprentissage.
*   **Loss ('categorical_crossentropy')** : La fonction de perte. Elle mesure la différence entre la distribution de probabilité prédite par le réseau et la distribution réelle (l'étiquette vraie). C'est cette valeur que l'optimiseur cherche à minimiser.
*   **Metrics ('accuracy')** : La précision (pourcentage de réponses correctes). C'est une mesure interprétable pour l'humain, utilisée pour le monitoring.

#### Bloc 4 : Prétraitement des données (Preprocessing)
```python
train_images = train_images.reshape((60000, 28 * 28))
train_images = train_images.astype('float32') / 255
```
Les données brutes ne sont pas compatibles avec le réseau tel quel :
1.  **Reshape** : Les images sont des matrices 2D (28x28). Le réseau Dense attend des vecteurs 1D. On "aplatit" donc l'image en une ligne de 784 pixels.
2.  **Normalisation** : Les pixels sont encodés de 0 à 255 (entiers). Les réseaux de neurones convergent mieux et plus vite avec des petites valeurs flottantes. On divise par 255 pour ramener toutes les valeurs dans l'intervalle [0, 1].

#### Bloc 5 : Encodage des étiquettes (One-Hot Encoding)
```python
from tensorflow.keras.utils import to_categorical
train_labels = to_categorical(train_labels)
```
Les étiquettes sont initialement des entiers (ex: le chiffre 5). La fonction de perte `categorical_crossentropy` attend un vecteur de probabilités.
`to_categorical` transforme l'entier 5 en vecteur : `[0, 0, 0, 0, 0, 1, 0, 0, 0, 0]`. Seul l'index correspondant à la classe vraie est à 1.

#### Bloc 6 : Entraînement
```python
network.fit(train_images, train_labels, epochs=5, batch_size=128)
```
Le processus d'apprentissage démarre :
*   **Epochs=5** : Le réseau va voir l'intégralité du dataset d'entraînement 5 fois.
*   **Batch_size=128** : Les poids ne sont pas mis à jour après chaque image (trop lent et instable), ni après toutes les images (trop lourd pour la mémoire). Ils sont mis à jour après avoir vu un lot de 128 images.
Pendant cette phase, on observe généralement la `loss` diminuer et l'`accuracy` augmenter.

#### Bloc 7 : Évaluation finale
```python
test_loss, test_acc = network.evaluate(test_images, test_labels)
```
On teste le modèle final sur les 10 000 images de test. Cette étape est cruciale pour valider que le modèle est robuste et performant sur des données inconnues. Une précision élevée ici (proche de celle d'entraînement) confirme le succès de l'opération.