### **Chapitre 0 : Introduction au Développement Web Moderne**
Ce chapitre offre un aperçu général de ce qu'est le web, de son fonctionnement, ainsi que des technologies et outils de base qu'un développeur utilise.

*   **Temps estimé pour couvrir le sujet :** 20 - 25 minutes

**Contenus abordés :**

1.  **Qu'est-ce que le World Wide Web ?**
    *   Explique que le web est un système mondial de réseaux informatiques interconnectés pour le partage d'informations et de services.
    *   **Exemples :**
        1.  Un système mondial de partage d'informations.
        2.  Une bibliothèque numérique géante.
        3.  Une plateforme d'applications.

2.  **Comment fonctionne le Web**
    *   Utilise une analogie avec la commande d'une pizza pour expliquer le modèle client-serveur.
    *   **Exemples :**
        1.  **Client :** Votre navigateur web (comme Chrome) qui fait une requête.
        2.  **Serveur :** L'ordinateur qui stocke les fichiers du site web et envoie une réponse.
        3.  **HTTP/HTTPS :** Le protocole utilisé pour envoyer la requête et la réponse.

3.  **Les 3 technologies fondamentales**
    *   Présente HTML, CSS et JavaScript comme la base de tout site web.
    *   **Exemples :**
        1.  **HTML (Le Squelette) :** Définit la structure et le contenu. Exemple : `<p>Ceci est un paragraphe.</p>`
        2.  **CSS (Les Vêtements) :** Définit la présentation et le style. Exemple : `p { color: red; }`
        3.  **JavaScript (Le Cerveau) :** Définit le comportement et l'interactivité. Exemple : `button.addEventListener('click', ...)`

4.  **Frontend vs. Backend**
    *   Explique la différence entre le côté client (ce que l'utilisateur voit) et le côté serveur (la logique en coulisses).
    *   **Exemples :**
        1.  **Technologies Frontend :** HTML, CSS, JavaScript, React.
        2.  **Technologies Backend :** Node.js, Python, Bases de données (MongoDB, PostgreSQL).

5.  **Outils essentiels pour les développeurs**
    *   Liste les logiciels fondamentaux dont chaque développeur a besoin.
    *   **Exemples :**
        1.  **Éditeur de code :** Visual Studio Code (VS Code).
        2.  **Navigateur Web :** Chrome ou Firefox, en particulier leurs Outils de Développement (F12).
        3.  **Gestion de versions :** Git pour suivre les changements et GitHub pour héberger le code.

---

### **Chapitre 1 : HTML en détail**
Ce chapitre est une plongée approfondie dans le HTML, couvrant tout, de la syntaxe de base et la structure des documents à des sujets avancés comme les formulaires, les tableaux et les images responsives.

*   **Temps estimé pour couvrir le sujet :** 1,5 - 2 heures

**Contenus abordés :**

1.  **Les fondamentaux de HTML**
    *   Couvre l'anatomie d'un élément HTML (balises, attributs, contenu), les balises auto-fermantes et un bref historique du HTML.
    *   **Exemples :**
        1.  **Anatomie d'un élément :** `<a href="a-propos.html">À propos de nous</a>`
        2.  **Balise auto-fermante :** `<img src="image.jpg" alt="description">`
        3.  **Histoire :** HTML5 est la norme actuelle, maintenue comme un "Standard Vivant".

2.  **Structure de base d'un document HTML5**
    *   Explique la structure de base requise pour chaque page HTML, incluant `<!DOCTYPE>`, `<html>`, `<head>`, et `<body>`.
    *   **Exemples :**
        1.  **Doctype :** `<!DOCTYPE html>` indique au navigateur d'utiliser le dernier standard HTML.
        2.  **Élément racine :** `<html lang="fr">` spécifie la langue de la page pour l'accessibilité.
        3.  **Section des métadonnées :** Le `<head>` contient des informations sur la page.

3.  **La section `<head>`**
    *   Détaille les balises cruciales à l'intérieur de `<head>`, telles que `<meta>`, `<title>`, et le lien vers le CSS.
    *   **Exemples :**
        1.  **Encodage des caractères :** `<meta charset="UTF-8">` (devrait être la première balise).
        2.  **Viewport pour le responsive :** `<meta name="viewport" content="width=device-width, initial-scale=1.0">`.
        3.  **Titre de la page :** `<title>Ma Super Page</title>` (apparaît dans l'onglet du navigateur).
        4.  **Lien vers le CSS :** `<link rel="stylesheet" href="style.css">`.

4.  **Mise en forme du texte et sémantique**
    *   Couvre toutes les balises liées au texte, y compris les titres (`<h1>`-`<h6>`), les paragraphes (`<p>`), et les balises sémantiques comme `<strong>` et `<em>`.
    *   **Exemples :**
        1.  **Titres :** N'utilisez `<h1>` qu'une seule fois par page pour le titre principal.
        2.  **Importance :** Utilisez `<strong>` pour un texte important, pas seulement pour le mettre en gras.
        3.  **Emphase :** Utilisez `<em>` pour accentuer un mot, pas seulement pour le mettre en italique.
        4.  **Code :** Utilisez `<pre><code>...</code></pre>` pour afficher des blocs de code.

5.  **Liens et Images**
    *   Explique comment créer des hyperliens (`<a>`) et intégrer des images (`<img>`), y compris les meilleures pratiques pour l'accessibilité et le design responsive.
    *   **Exemples :**
        1.  **Lien externe :** `<a href="https://google.com" target="_blank" rel="noopener noreferrer">Google</a>`
        2.  **Image avec texte alternatif (`alt`) :** `<img src="chat.jpg" alt="Un chat roux et touffu dormant sur un tapis.">`
        3.  **Image responsive :** Utilisation de `<picture>` ou `srcset` pour servir différentes tailles d'image.

6.  **Listes (non ordonnées, ordonnées, de description)**
    *   Couvre les trois types de listes utilisées pour organiser le contenu.
    *   **Exemples :**
        1.  **Liste non ordonnée :** `<ul><li>Élément 1</li></ul>` (pour des listes à puces).
        2.  **Liste ordonnée :** `<ol><li>Étape 1</li></ol>` (pour des étapes numérotées).
        3.  **Liste de description :** `<dl><dt>Terme</dt><dd>Définition</dd></dl>` (pour des paires clé-valeur).

7.  **Tableaux**
    *   Explique comment structurer des données tabulaires en utilisant `<table>`, `<tr>`, `<th>`, `<td>`, et des balises sémantiques comme `<thead>` et `<tbody>`.
    *   **Exemples :**
        1.  **Structure de base :** Un `<table>` contient des `<tr>` (lignes), qui contiennent des `<td>` (cellules).
        2.  **En-têtes :** Utilisez `<th>` pour les cellules d'en-tête pour les mettre en gras et les centrer.
        3.  **Fusion de cellules :** Utilisez `colspan="2"` pour qu'une cellule s'étende sur deux colonnes.

8.  **Formulaires**
    *   Introduit comment collecter des données utilisateur avec l'élément `<form>` et divers types d'`<input>`. Met l'accent sur l'importance de la balise `<label>`.
    *   **Exemples :**
        1.  **Champ de texte :** `<label for="nom">Nom :</label><input type="text" id="nom" name="username">`
        2.  **Bouton de soumission :** `<input type="submit" value="S'inscrire">`
        3.  **Champ de mot de passe :** `<input type="password" id="pass" name="password">`

---




### **Chapitre 2 : Les Bases de Git et GitHub**
Ceci est une introduction rapide et pratique à l'outil le plus essentiel pour les développeurs. Il couvre le strict minimum nécessaire pour sauvegarder du code et le partager sur GitHub.

*   **Temps estimé pour couvrir le sujet :** 30 - 45 minutes

**Contenus abordés :**

1.  **Qu'est-ce que la gestion de versions ?**
    *   Explique que la gestion de versions est un système qui enregistre les modifications apportées à un fichier ou à un ensemble de fichiers au fil du temps, afin que vous puissiez rappeler des versions spécifiques plus tard. C'est comme une "sauvegarde de partie" pour votre code.
    *   **Exemples :**
        1.  Revenir à une version précédente et fonctionnelle de votre projet si vous introduisez un bug.
        2.  Collaborer avec d'autres développeurs sans écraser mutuellement leur travail.

2.  **Git vs. GitHub**
    *   Clarifie la différence entre les deux.
    *   **Exemples :**
        1.  **Git :** Le logiciel qui s'exécute sur votre ordinateur pour suivre les changements localement. C'est l'outil en ligne de commande.
        2.  **GitHub :** Un site web qui héberge vos projets Git (dépôts). C'est là que vous stockez votre code en ligne pour le sauvegarder et collaborer.

3.  **Le Flux de Travail Local de Base**
    *   Couvre les trois commandes essentielles pour sauvegarder votre travail localement.
    *   **Exemples :**
        1.  **`git init`** : Initialise un nouveau dépôt Git dans votre dossier de projet. Vous ne le faites qu'une seule fois.
        2.  **`git add <fichier>` ou `git add .`** : Ajoute vos fichiers modifiés à la "zone de préparation" (staging area), les préparant à être sauvegardés.
        3.  **`git commit -m "Votre message descriptif"`** : Prend un "instantané" (snapshot) des fichiers préparés et le sauvegarde de manière permanente dans l'historique de votre projet avec un message expliquant ce que vous avez fait. Exemple : `git commit -m "Création du fichier HTML initial"`.

4.  **Le Flux de Travail GitHub de Base**
    *   Couvre comment mettre votre code local sur GitHub.
    *   **Exemples :**
        1.  **Créer un dépôt sur GitHub :** Un guide pas à pas pour créer un nouveau dépôt vide sur le site de GitHub.
        2.  **`git remote add origin <URL>`** : Connecte votre dossier de projet local au dépôt vide sur GitHub.
        3.  **`git push origin main`** : "Pousse" (envoie/upload) vos commits locaux vers votre dépôt GitHub.
        4.  **`git clone <URL>`** : La commande utilisée pour télécharger un projet existant depuis GitHub sur votre ordinateur.





---

### **Chapitre 3 : CSS en détail**
Ce chapitre est une formation complète en CSS, des sélecteurs et du modèle de boîtes aux techniques de mise en page modernes comme Flexbox et Grid, en passant par des concepts avancés comme les variables et les animations.

*   **Temps estimé pour couvrir le sujet :** 2 - 2,5 heures

**Contenus abordés :**

1.  **Les fondamentaux du CSS**
    *   Couvre la "Cascade" (les règles de priorité), l'anatomie d'une règle CSS et les trois façons d'appliquer le CSS (externe, interne, en ligne).
    *   **Exemples :**
        1.  **Règle CSS :** `selecteur { propriete: valeur; }`
        2.  **La Cascade :** Un sélecteur d'ID (`#mon-id`) est plus spécifique qu'un sélecteur de classe (`.ma-classe`).
        3.  **Meilleure pratique :** Utiliser des feuilles de style externes liées via la balise `<link>`.

2.  **Sélecteurs et Combinateurs**
    *   Détaille les différentes manières de sélectionner des éléments HTML, y compris par classe, ID, attribut, et leur relation avec d'autres éléments (descendant, enfant, frère).
    *   **Exemples :**
        1.  **Sélecteur de classe :** `.btn-primary` sélectionne les éléments avec `class="btn-primary"`.
        2.  **Sélecteur de descendant :** `nav a` sélectionne tous les liens à l'intérieur d'une balise `<nav>`.
        3.  **Sélecteur d'enfant :** `ul > li` sélectionne uniquement les `<li>` qui sont des enfants directs d'un `<ul>`.

3.  **Pseudo-classes et Pseudo-éléments**
    *   Explique comment styliser des éléments en fonction de leur état (`:hover`) ou styliser une partie spécifique d'un élément (`::first-letter`).
    *   **Exemples :**
        1.  **État de survol :** `a:hover { text-decoration: underline; }`
        2.  **Styliser les lignes paires :** `tr:nth-child(even) { background-color: #f2f2f2; }`
        3.  **Ajouter du contenu :** `.icone::before { content: '★'; }`

4.  **Le Modèle de Boîtes (Box Model) et le dimensionnement**
    *   Couvre le concept fondamental selon lequel chaque élément est une boîte avec un `contenu`, un `padding` (marge intérieure), une `border` (bordure) et une `margin` (marge extérieure). Introduit la propriété cruciale `box-sizing`.
    *   **Exemples :**
        1.  **Parties de la boîte :** La `margin` est l'espace *à l'extérieur* de la bordure ; le `padding` est l'espace *à l'intérieur*.
        2.  **Meilleure pratique :** Définir `box-sizing: border-box;` pour des mises en page plus intuitives.
        3.  **Unités :** Utiliser `rem` pour des tailles de police et des espacements évolutifs.

5.  **Mise en page (Position, Float, Flexbox, Grid)**
    *   Explique les différentes méthodes pour positionner les éléments sur une page, des méthodes traditionnelles (`position`, `float`) aux plus modernes (`display: flex`, `display: grid`).
    *   **Exemples :**
        1.  **Positionnement :** `position: absolute;` retire un élément du flux normal.
        2.  **Flexbox :** `display: flex; justify-content: space-between;` est excellent pour aligner des éléments sur une ligne.
        3.  **Grid :** `display: grid; grid-template-columns: 1fr 2fr;` est parfait pour les mises en page 2D complexes.

6.  **Transitions, Animations et Variables**
    *   Couvre comment créer des animations simples avec `transition` et des plus complexes avec `@keyframes`. Introduit les variables CSS pour des styles réutilisables.
    *   **Exemples :**
        1.  **Transition :** `transition: background-color 0.3s ease;` pour un changement de couleur fluide au survol.
        2.  **Animation :** `@keyframes slide-in { from { ... } to { ... } }`
        3.  **Variable CSS :** `:root { --couleur-principale: blue; } h1 { color: var(--couleur-principale); }`

7.  **Design Responsive**
    *   Explique comment utiliser les Media Queries pour appliquer différents styles en fonction de la taille de l'écran, ce qui est le fondement du design responsive.
    *   **Exemples :**
        1.  **Approche "Mobile First" :** Écrire les styles de base pour mobile, puis utiliser des media queries pour les écrans plus grands.
        2.  **Syntaxe :** `@media (min-width: 768px) { ... }` applique des styles pour les écrans de 768px et plus.

---

### **Chapitre 4 : JavaScript en détail**
Ce chapitre est une introduction complète au langage JavaScript, couvrant la syntaxe, les fonctions, les structures de données, la manipulation du DOM et la programmation asynchrone moderne avec les Promesses et async/await.

*   **Temps estimé pour couvrir le sujet :** 2,5 - 3 heures

**Contenus abordés :**

1.  **Les fondamentaux de JavaScript**
    *   Couvre les variables (`let`, `const`), les types de données (chaîne de caractères, nombre, booléen, objet), la coercition de type et l'égalité (`==` vs `===`).
    *   **Exemples :**
        1.  **Variables :** Utilisez `const` par défaut ; utilisez `let` si la valeur doit changer. Évitez `var`.
        2.  **Égalité stricte :** Toujours utiliser `===` pour éviter les bugs inattendus dus à la coercition de type (`7 === '7'` est faux).
        3.  **Template Literals :** `` `Bonjour, ${nom} !` `` pour une mise en forme plus facile des chaînes de caractères.

2.  **Fonctions et Portée (Scope)**
    *   Explique les déclarations de fonction, les expressions de fonction, les fonctions fléchées, les paramètres, la portée (où vivent les variables) et les closures.
    *   **Exemples :**
        1.  **Fonction fléchée :** `const addition = (a, b) => a + b;`
        2.  **Closures :** Une fonction qui se "souvient" des variables de son environnement de création.

3.  **Objets et Tableaux (Arrays)**
    *   Une plongée dans les structures de données les plus importantes de JavaScript. Couvre les propriétés d'objet, les méthodes, le mot-clé `this`, et les puissantes méthodes de tableau comme `map`, `filter` et `reduce`.
    *   **Exemples :**
        1.  **Objet :** `const personne = { nom: 'Cline', age: 30 };`
        2.  **`map()` :** Crée un nouveau tableau en transformant chaque élément. `[1, 2, 3].map(x => x * 2)` renvoie `[2, 4, 6]`.
        3.  **`filter()` :** Crée un nouveau tableau avec les éléments qui passent un test.
        4.  **Déstructuration :** `const { nom, age } = personne;` pour créer facilement des variables à partir des propriétés d'un objet.

4.  **Le DOM (Document Object Model)**
    *   Explique comment JavaScript interagit avec la page HTML. Couvre la sélection, la création et la manipulation d'éléments.
    *   **Exemples :**
        1.  **Sélectionner un élément :** `const bouton = document.querySelector('#mon-bouton');`
        2.  **Changer le texte :** `element.textContent = 'Nouveau Texte';`
        3.  **Changer le style :** `element.style.color = 'blue';`
        4.  **Changer la classe :** `element.classList.add('active');`

5.  **Événements**
    *   Couvre comment rendre une page interactive en écoutant les actions de l'utilisateur comme les clics, les pressions de touches et les soumissions de formulaires.
    *   **Exemples :**
        1.  **Écouteur d'événements :** `bouton.addEventListener('click', function() { ... });`
        2.  **Objet événement :** La fonction reçoit un objet `event` avec des détails sur l'événement.
        3.  **Délégation d'événements :** Attacher un seul écouteur à un élément parent pour gérer les événements de tous ses enfants.

6.  **JavaScript Asynchrone**
    *   Explique comment JavaScript gère les tâches de longue durée comme la récupération de données d'un serveur sans figer la page. Couvre les Promesses et la syntaxe moderne `async/await`.
    *   **Exemples :**
        1.  **Promesses :** L'API `fetch()` renvoie une promesse qui se résout avec la réponse du serveur.
        2.  **Chaînage de promesses :** Utilisez `.then()` pour gérer une réponse réussie et `.catch()` pour gérer les erreurs.
        3.  **`async/await` :** Une syntaxe plus propre pour travailler avec les promesses. `async function getData() { const response = await fetch(...); }`

7.  **JS Moderne (Modules, Stockage Web, JSON)**
    *   Couvre les fonctionnalités modernes pour organiser le code et stocker des données.
    *   **Exemples :**
        1.  **Modules :** Utilisez `import` et `export` pour diviser le code en fichiers réutilisables.
        2.  **Stockage Local :** `localStorage.setItem('user', 'Cline')` pour sauvegarder des données dans le navigateur.
        3.  **JSON :** `JSON.stringify()` pour convertir un objet en chaîne de caractères pour le stockage, et `JSON.parse()` pour le reconvertir.

---

### **Chapitre 5 : Projets et Déploiement**
Ce dernier chapitre se concentre sur l'application des compétences acquises en construisant des projets, puis en les rendant publiquement accessibles sur Internet via le déploiement.

*   **Temps estimé pour couvrir le sujet :** 45 - 60 minutes

**Contenus abordés :**

1.  **L'importance des projets**
    *   Souligne que la construction de projets est la meilleure façon de consolider les connaissances et de construire un portfolio. Fournit plusieurs idées de projets.
    *   **Exemples :**
        1.  **Idée de projet 1 :** Une application de liste de tâches (en utilisant la manipulation du DOM et le `localStorage`).
        2.  **Idée de projet 2 :** Une application météo (en utilisant l'API `fetch`).
        3.  **Conseil de portfolio :** Chaque projet sur GitHub devrait avoir un fichier `README.md` détaillé.

2.  **Qu'est-ce que le déploiement ?**
    *   Explique le processus qui consiste à prendre les fichiers d'un projet local et à les mettre sur un serveur web public. Couvre des concepts comme les noms de domaine et l'hébergement web.
    *   **Exemples :**
        1.  **Nom de domaine :** Une adresse lisible par l'homme comme `mon-portfolio.com`.
        2.  **Site statique vs. dynamique :** Une application en pur JS est un site statique.
        3.  **Hébergement :** Le service qui fournit l'espace serveur pour vos fichiers.

3.  **Options de déploiement pour les sites statiques**
    *   Présente des plateformes modernes, gratuites et faciles à utiliser pour déployer des sites statiques.
    *   **Exemples :**
        1.  **GitHub Pages :** Hébergement gratuit directement depuis un dépôt GitHub.
        2.  **Netlify :** Une plateforme puissante avec déploiement continu.
        3.  **Vercel :** Une autre plateforme populaire, similaire à Netlify.

4.  **Déploiement continu et étapes finales**
    *   Explique comment des plateformes comme Netlify peuvent automatiquement mettre à jour votre site en ligne chaque fois que vous poussez des changements sur GitHub. Couvre également l'optimisation des performances et l'audit.
    *   **Exemples :**
        1.  **Déploiement continu :** `git push` vers votre branche principale, et le site se met à jour automatiquement.
        2.  **Optimisation des images :** Compressez les images avec un outil comme TinyPNG avant de les mettre en ligne.
        3.  **Audit :** Utilisez l'outil Lighthouse dans les Outils de Développement de Chrome pour vérifier les performances et l'accessibilité.