

> Basé sur : *Plan de Cours Complet - Développement Web Moderne*  
> Objectif : Maîtriser les bases de **HTML**, **CSS visuel**, et **JavaScript interactif**  
> Niveau : Débutant (aucun concept avancé, uniquement du concret visuel et logique simple)

---

##  Session 1 : HTML – Structure de Base du Web

- Structure d’une page HTML
  - `<!DOCTYPE>`, `<html>`, `<head>`, `<body>`

- Éléments essentiels
  - Titres (`<h1>` à `<h6>`), paragraphes (`<p>`), séparateurs (`<hr>`, `<br>`)
  - Liens (`<a>`), images (`<img>`), listes (`<ul>`, `<ol>`, `<li>`)

- Regroupement du contenu
  - `<div>`, `<span>`, `<section>`, `<header>`, `<footer>`, `<main>`

- Formulaires simples
  - `<form>`, `<input>`, `<textarea>`, `<label>`, `<button>`

---

##  Session 2 : CSS – Mise en Forme Visuelle Simple

- Syntaxe CSS de base
  - Sélecteurs : élément, `.classe`, `#id`
  - Syntaxe : `sélecteur { propriété: valeur; }`

- Mise en forme du texte
  - `color`, `font-family`, `font-size`, `font-weight`, `text-align`

- Mise en page / boîte CSS
  - `width`, `height`, `padding`, `margin`, `border`

- Couleurs & fonds
  - `background-color`, `background-image`, `opacity`

- Bordures & effets visuels
  - `border-radius`, `box-shadow`, `text-shadow`

- Positionnement simple
  - `position`, `top`, `left`, `right`, `bottom`
  - `transform: rotate(...)`, `scale(...)`, `translate(...)`

- Transitions simples
  - `transition`, `:hover`

---

##  Session 3 : JavaScript – Dynamique & Logique Débutante

###  Fondamentaux JavaScript

- Variables
  - `let`, `const`  
  - Types : texte (string), nombre (number), booléen (boolean)

- Opérations de base
  - Addition `+`, Soustraction `-`, Multiplication `*`, Division `/`
  - Concaténation de texte avec `+`
  - Comparaison : `===`, `!==`, `>`, `<`

- Fonctions
  - Déclaration (`function nom() {}`)  
  - Appel, paramètres simples, retour

- Conditions
  - `if`, `else if`, `else`

---

###  Tableaux & Boucles

- Tableaux (`[]`)
  - Création : `let fruits = ['pomme', 'banane']`
  - Accès : `fruits[0]`, `fruits.length`

- Boucles
  - `for (let i = 0; i < ...; i++)`
  - `while (...) { ... }`
  - Parcourir un tableau (`for`, `for...of`)

---

###  DOM – Interaction avec la Page

- Sélection d’éléments
  - `document.querySelector()`, `getElementById()`

- Changement de contenu
  - `.innerText`, `.innerHTML`

- Modification du style
  - `.style.color`, `.style.backgroundColor`, `.style.fontSize`

- Classes CSS dynamiques
  - `.classList.add()`, `.remove()`, `.toggle()`

---

###  Événements

- `addEventListener('click', ...)`
- Autres événements utiles : `mouseover`, `change`, `submit`

---

###  Interactions Débutantes à Réaliser

- Changer un texte ou une couleur au clic
- Masquer/afficher une image
- Afficher un message personnalisé
- Créer une fonction de "mode sombre"
- Parcourir une liste (tableau) et l’afficher dans le HTML
- Créer une fonction qui fait une addition
- Réagir à un champ vide dans un formulaire

---

>  Objectif final :
> Créer une page web interactive, 100% HTML/CSS/JS natif, sans framework.

