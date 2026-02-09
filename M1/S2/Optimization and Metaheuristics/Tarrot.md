
# Note Technique : Architecture et Implémentation du Projet "Tarot Africain"

## 1. Analyse de l'Infrastructure et Configuration (Analyse des Fichiers Racines)

L'ossature du projet repose sur une configuration rigoureuse garantissant la maintenabilité et la compatibilité multiplateforme.

### 1.1 Gestion des Dépendances (`pubspec.yaml`)
Le projet s'appuie sur le framework **Flutter (SDK >=3.1.5)**. L'analyse du fichier de configuration révèle des choix architecturaux précis :
- **GetX (`get: ^4.6.6`)** : Utilisé comme pilier central pour la gestion d'état, la navigation et l'injection de dépendances. Ce choix permet de découpler la logique métier (Controller) de la couche de présentation (View).
- **Assets** : L'arborescence des ressources est centralisée sous `image/cartes-tarot/`, permettant une gestion dynamique des textures des 78 cartes.

### 1.2 Qualité de Code (`analysis_options.yaml`)
Le projet intègre le package `flutter_lints`. Les règles d'analyse statique sont configurées pour imposer les *best practices* de Dart, notamment :
- Le respect des constantes pour les widgets immuables.
- La prévention des impressions console en production (`avoid_print`).
- La cohérence syntaxique (utilisation des simples quotes, typage explicite).

---

## 2. Architecture du Système de Jeu (Logique Dart)

La logique logicielle est structurée pour simuler fidèlement les phases de jeu du Tarot Africain (Manches, Tours, Plis).

### 2.1 Modélisation des Données (Models)
Le code définit des entités structurées pour représenter l'état du jeu :
- **CardModel** : Gère la valeur (2 à Roi + As pour les ordinaires, 1 à 21 pour les atouts) et l'identifiant de ressource.
- **PlayerModel** : Encapsule l'état réactif de chaque participant (score, main actuelle, contrat annoncé).

### 2.2 Contrôleur de Jeu (Logiciel de Contrôle)
L'implémentation utilise un `GameController` qui pilote la machine à états :
1. **Phase de Distribution** : Algorithme gérant la décrémentation des cartes par tour (de 5 cartes à 1 seule).
2. **Phase d'Annonce** : Gestion de la contrainte algorithmique où la somme des paris ne peut égaler le nombre de cartes en jeu.
3. **Phase de Pli** : Logique de comparaison de forces entre les enseignes, les atouts et l'Excuse.

---

## 3. Implémentation des Spécificités du Tarot Africain

### 3.1 Algorithme de Validation des Paris
La règle de la "somme interdite" est implémentée via une validation dynamique. Pour le dernier joueur, le code calcule :
$$ValeurInterdite = CartesDistribuees - \sum (ParisPrecedents)$$
L'interface utilisateur (UI) est programmée pour désactiver l'entrée correspondant à cette valeur, empêchant ainsi tout contrat invalide avant même sa soumission.

### 3.2 Gestion du "Tour Aveugle" (Tour 5)
Lors du dernier tour (1 seule carte), une condition logique modifie le comportement du rendu :
- L'index de la carte du joueur local est masqué via un widget `Visibility` ou une transformation graphique (affichage du dos de la carte).
- Les cartes des adversaires sont révélées en clair, permettant au joueur de parier sur la base d'informations partielles.

---

## 4. Intégration Native et Plugins (Couche Physique)

L'examen du fichier `GeneratedPluginRegistrant.java` confirme l'intégration de fonctionnalités avancées nécessaires à une application robuste :

- **Persistence des Données** : L'utilisation de `sqflite` et `shared_preferences` permet la sauvegarde des scores historiques et des préférences utilisateur (ex: mode sombre).
- **Permissions et Système** : Intégration de `permission_handler` et `path_provider` pour la gestion des fichiers locaux sur Android et iOS.
- **Cycle de vie** : `flutter_plugin_android_lifecycle` assure que le moteur de jeu se met en pause correctement lors d'un appel entrant ou d'un changement d'application.

---

## 5. Environnement d'Exécution et Déploiement

### 5.1 Configuration Android (`build.gradle`)
Le projet est calibré pour les standards modernes :
- **Namespace** : `com.example.cartes_tarot`
- **SDK Cible** : Niveau 34 (Android 14), assurant la compatibilité avec les dernières exigences du Play Store.
- **Compatibilité Java** : Utilisation de la version 17 de Java pour la compilation des sources Kotlin/Android.

### 5.2 Sécurité et Distribution
Le fichier `.gitignore` est exhaustif, excluant les fichiers de build, les clés de signature (`key.properties`, `.keystore`) et les artefacts de développement (IDEA, VS Code), garantissant la propreté du dépôt de code.

---

## 6. Synthèse des Choix Techniques

| Composant | Technologie | Justification Académique |
| :--- | :--- | :--- |
| **Framework** | Flutter 3.x | Développement multiplateforme avec performance native. |
| **State Management** | GetX | Réactivité élevée et simplification du cycle de vie des contrôleurs. |
| **Base de données** | SQLite | Stockage structuré pour les statistiques et les parties en cours. |
| **Architecture** | Clean Architecture / MVC | Séparation stricte entre les modèles de données et la logique de jeu. |
| **Linter** | Flutter Lints | Garantie d'un code uniforme et conforme aux standards de l'industrie. |
