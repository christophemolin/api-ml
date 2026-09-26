# Guide d'édition du site api-ml.info

Ce guide s'adresse aux **bénévoles de l'API** qui veulent mettre à jour le site sans connaissances techniques.
Tout se fait **depuis votre navigateur**, sur le site github.com. Il n'y a rien à installer.

---

## Sommaire

1. [Le principe](#1-le-principe)
2. [Modifier un fichier existant](#2-modifier-un-fichier-existant)
3. [Modifier le texte de l'accueil ou de « Nous rejoindre »](#3-modifier-le-texte-de-laccueil-ou-de--nous-rejoindre-)
4. [Ajouter un projet](#4-ajouter-un-projet)
5. [Masquer ou supprimer un projet](#5-masquer-ou-supprimer-un-projet)
6. [Modifier un contact ou ajouter une école](#6-modifier-un-contact-ou-ajouter-une-école)
7. [Ajouter ou modifier un partenaire](#7-ajouter-ou-modifier-un-partenaire)
8. [Changer le lien Facebook ou l'e-mail général](#8-changer-le-lien-facebook-ou-le-mail-général)
9. [Aide-mémoire Markdown](#9-aide-mémoire-markdown)
10. [Ça n'a pas marché ?](#10-ça-na-pas-marché-)

---

## 1. Le principe

Le site est construit à partir de **fichiers texte** rangés dans le dépôt GitHub :

| Je veux modifier… | Fichier(s) |
|---|---|
| Le texte de la page d'accueil | `src/content/pages/accueil.md` |
| Le texte de la page « Nous rejoindre » | `src/content/pages/nous-rejoindre.md` |
| Les projets | `src/content/projets/` (un fichier par projet) |
| Les écoles et les e-mails des équipes | `src/data/ecoles.json` |
| Les partenaires | `src/data/partenaires.json` |
| Le lien Facebook, l'e-mail général, le slogan | `src/data/site.json` |
| Les images | `public/images/` |

Quand vous **enregistrez** une modification (bouton « Commit changes »), le site est **reconstruit et mis en ligne automatiquement en 1 à 2 minutes**.

Pour suivre la mise en ligne, ouvrez l'onglet **Actions** en haut du dépôt :
- 🟡 rond jaune : en cours ;
- ✅ coche verte : c'est en ligne ;
- ❌ croix rouge : il y a une erreur, et **le site en ligne n'a pas changé** (voir la [section 10](#10-ça-na-pas-marché-)).

> 💡 Pour être éditeur, il faut un compte GitHub (gratuit) **ajouté comme collaborateur** du dépôt. Demandez-le au responsable du site.

---

## 2. Modifier un fichier existant

1. Connectez-vous sur [github.com](https://github.com) et ouvrez le dépôt du site.
2. Naviguez dans les dossiers en cliquant dessus (par exemple `src`, puis `data`, puis `ecoles.json`).
3. Cliquez sur l'**icône crayon ✏️** (« Edit this file ») en haut à droite du fichier.
4. Faites votre modification.
5. Cliquez sur le bouton vert **« Commit changes… »** en haut à droite.
6. Dans la fenêtre qui s'ouvre, écrivez une courte description (ex. « Nouvel e-mail pour Colbert »), laissez « Commit directly to the main branch » coché, puis cliquez sur **« Commit changes »**.
7. Attendez 1 à 2 minutes et rechargez le site.

> 💡 L'onglet **« Preview »** de l'éditeur permet de voir le rendu d'un fichier Markdown avant d'enregistrer.

---

## 3. Modifier le texte de l'accueil ou de « Nous rejoindre »

Ouvrez `src/content/pages/accueil.md` ou `src/content/pages/nous-rejoindre.md`.

Le fichier a **deux parties** :

```markdown
---
title: "Accueil"
description: "Phrase de présentation utilisée par Google et Facebook."
points:
  - titre: "Le bien-être des enfants"
    texte: "Notre priorité : que chaque enfant…"
    image: "/images/illustrations/bien-etre.jpg"
  - titre: "…"
    texte: "…"
    image: "…"
---

Ici le texte libre de la page, en **Markdown**.
```

- **Entre les deux lignes `---`** se trouve l'**en-tête**, avec des informations structurées :
  - `description` : résumé affiché dans les résultats Google ;
  - `points` : les cartes illustrées, où chaque bloc commence par `- titre:`.
- **Après le second `---`** se trouve le **texte libre** de la page (voir l'[aide-mémoire Markdown](#9-aide-mémoire-markdown)).

⚠️ Dans l'en-tête :
- gardez les **guillemets** `"` autour des textes ;
- respectez le **décalage** des lignes (espaces au début), en utilisant des espaces et non des tabulations ;
- si votre texte contient lui-même des guillemets, utilisez des guillemets français « … » à la place.

---

## 4. Ajouter un projet

### Étape 1 : créer le fichier

1. Ouvrez le dossier `src/content/projets/`.
2. Ouvrez le fichier **`_exemple.md`** (le modèle) et copiez tout son contenu (Ctrl+A puis Ctrl+C, ou Cmd+A puis Cmd+C sur Mac).
3. Revenez au dossier `src/content/projets/`, cliquez sur **« Add file » → « Create new file »**.
4. Donnez un nom au fichier :
   - en **minuscules**, **sans accents ni espaces**, avec des tirets ;
   - terminé par **`.md`** ;
   - exemples : `collecte-de-jouets.md`, `carnaval-2026.md`.

   ➜ Ce nom devient l'adresse de la page : `api-ml.info/projets/collecte-de-jouets/`.
5. Collez le contenu du modèle.

### Étape 2 : remplir l'en-tête

```markdown
---
title: "Collecte de jouets"
date: 2026-11-20
summary: "En novembre, nous collectons des jouets dans les écoles pour les familles dans le besoin."
image: "/images/projets/collecte-jouets.jpg"
imageAlt: "Des cartons remplis de jouets"
draft: false
---
```

| Champ | Obligatoire ? | Explication |
|---|---|---|
| `title` | ✅ oui | Titre du projet |
| `date` | ✅ oui | Format **AAAA-MM-JJ**. Sert à trier les projets, du plus récent au plus ancien. |
| `summary` | ✅ oui | 1 ou 2 phrases, affichées sur la carte du projet |
| `image` | non | Chemin de l'image (voir étape 3). Supprimez la ligne s'il n'y a pas d'image. |
| `imageAlt` | non | Courte description de l'image, pour les personnes malvoyantes |
| `draft` | non | `true` = projet masqué, `false` = projet visible |

Vous pouvez supprimer les lignes de commentaires du modèle (celles qui commencent par `#`).

### Étape 3 : ajouter une image (facultatif)

1. Préparez une image **JPG ou PNG**, idéalement de **moins de 500 Ko** et d'environ **1200 pixels de large**.
   Nommez-la en minuscules, sans accents ni espaces (ex. `collecte-jouets.jpg`).
2. Ouvrez le dossier `public/images/projets/`.
3. Cliquez sur **« Add file » → « Upload files »**, déposez l'image, puis **« Commit changes »**.
4. Dans l'en-tête du projet, indiquez : `image: "/images/projets/collecte-jouets.jpg"`.
   ⚠️ Le chemin commence par `/images/…` et **pas** par `public/`.

### Étape 4 : écrire le texte et enregistrer

Sous le second `---`, écrivez la description du projet en Markdown, puis **« Commit changes »**.

Le projet apparaît automatiquement sur la page **Projets**. S'il fait partie des 3 plus récents, il s'affiche aussi sur la page d'**accueil**.

> 📷 **Droit à l'image** : ne publiez pas de photo d'enfant identifiable sans l'accord écrit de ses parents.

---

## 5. Masquer ou supprimer un projet

- **Masquer temporairement** : dans l'en-tête du projet, mettez `draft: true`. Pour le réafficher, remettez `draft: false`.
- **Supprimer définitivement** : ouvrez le fichier, cliquez sur **« … »** en haut à droite, puis **« Delete file »** et **« Commit changes »**.

---

## 6. Modifier un contact ou ajouter une école

Ouvrez `src/data/ecoles.json`. Chaque école est décrite dans un bloc `{ … }` :

```json
{
  "id": "maternelle-colbert",
  "nom": "École maternelle Jean-Baptiste Colbert",
  "niveau": "maternelle",
  "email": "api.maternellecolbert@gmail.com",
  "adresse": "Place Colbert, 78600 Maisons-Laffitte",
  "telephone": "01 34 93 85 26",
  "emailEcole": "ce.0781281U@ac-versailles.fr",
  "photo": "/images/ecoles/maternelle-colbert.jpg",
  "eleves": 74,
  "classes": 3
}
```

| Champ | Explication |
|---|---|
| `id` | Identifiant **unique**, en minuscules, sans accents ni espaces |
| `nom` | Nom affiché de l'établissement |
| `niveau` | **Une seule** de ces trois valeurs : `maternelle`, `elementaire` ou `college` (sans accent) |
| `email` | Adresse e-mail de l'**équipe API** (affichée sur les pages Écoles et Contacts) |
| `adresse` | *(facultatif)* Adresse postale |
| `telephone` | *(facultatif)* Téléphone de l'établissement |
| `emailEcole` | *(facultatif)* E-mail officiel de l'établissement |
| `site` | *(facultatif)* Site de l'établissement, commençant par `https://` |
| `photo` | *(facultatif)* Photo de l'école, déposée dans `public/images/ecoles/` (même principe que les images de projets, [section 4](#4-ajouter-un-projet)) |
| `eleves`, `classes` | *(facultatif)* Effectifs de l'année : **un nombre sans guillemets** (ex. `74`, pas `"74"`) |

👉 **À chaque rentrée**, pensez à mettre à jour les effectifs (`eleves`, `classes`) et les e-mails des équipes.

- **Changer un e-mail** : modifiez simplement le texte entre guillemets après `"email":`.
- **Ajouter une école** : copiez un bloc `{ … }` existant, collez-le juste en dessous (avec une virgule entre les deux blocs) et modifiez les valeurs.
- **Retirer une école** : supprimez son bloc.

Les pages **Écoles** et **Contacts** sont mises à jour toutes les deux, et les écoles y sont triées automatiquement.

### ⚠️ Les pièges du JSON

Le format JSON est très strict. Une seule erreur empêche la mise à jour du site :

1. **Une virgule entre chaque ligne**, et **pas de virgule après la dernière** :
   ```json
   [
     { … },    ← virgule
     { … },    ← virgule
     { … }     ← PAS de virgule sur la dernière
   ]
   ```
2. **Toujours des guillemets droits** `"` et jamais `'`, ni les guillemets typographiques “ ” (attention au copier-coller depuis Word).
3. Ne supprimez pas les crochets `[` `]` ni les accolades `{` `}`.

> 💡 En cas de doute, collez le contenu du fichier sur [jsonlint.com](https://jsonlint.com) pour le vérifier avant d'enregistrer.

---

## 7. Ajouter ou modifier un partenaire

Ouvrez `src/data/partenaires.json` :

```json
{
  "id": "mairie",
  "nom": "Mairie de Maisons-Laffitte",
  "categorie": "institutions",
  "description": "Texte de présentation du partenaire.",
  "site": "https://www.maisonslaffitte.fr"
}
```

| Champ | Explication |
|---|---|
| `id` | Identifiant unique (minuscules, sans accents ni espaces) |
| `nom` | Nom affiché |
| `categorie` | `parents` (associations de parents), `institutions`, `solidarite` (associations aidées) ou `soutien` (partenaires qui reversent une partie des achats à l'API), sans accent |
| `description` | Quelques phrases de présentation |
| `site` | *(facultatif)* Adresse du site, commençant par `https://`. Supprimez la ligne s'il n'y en a pas, **en retirant aussi la virgule** à la fin de la ligne précédente. |
| `logo` | *(facultatif)* Logo du partenaire, déposé dans `public/images/partenaires/` (ex. `"/images/partenaires/mon-logo.png"`). Formats : PNG, JPG ou SVG, idéalement au moins 200 pixels de haut. Il s'affiche en haut de la carte. |
| `reseaux` | *(facultatif)* Liens vers les réseaux sociaux du partenaire (voir ci-dessous) |

### Ajouter les réseaux sociaux d'un partenaire

Ajoutez un bloc `reseaux` après la ligne `site`. Vous pouvez y mettre `facebook`, `instagram` et/ou `linkedin` : seuls les réseaux présents s'affichent, sous forme d'icônes à côté de « Visiter le site ».

```json
{
  "id": "handi-cap-prevention",
  "nom": "Handi-Cap-Prévention",
  "categorie": "solidarite",
  "description": "Texte de présentation du partenaire.",
  "site": "https://www.handicaprevention.com",
  "reseaux": {
    "facebook": "https://www.facebook.com/…",
    "instagram": "https://www.instagram.com/…"
  }
}
```

⚠️ N'oubliez pas la **virgule** à la fin de la ligne `"site": …` avant le bloc `reseaux`, ni l'**accolade fermante** `}` du bloc.

Les mêmes [pièges du JSON](#6-modifier-un-contact-ou-ajouter-une-école) (section 6) s'appliquent.

---

## 8. Changer le lien Facebook ou l'e-mail général

Ouvrez `src/data/site.json` :

```json
{
  "nom": "API Maisons-Laffitte",
  "nomComplet": "Association des Parents Indépendants de Maisons-Laffitte",
  "slogan": "Ensemble, améliorons au quotidien l'environnement scolaire de nos enfants",
  "emailGeneral": "contact@exemple.fr",
  "facebook": "https://www.facebook.com/…"
}
```

- `emailGeneral` : e-mail affiché sur la page Contacts et en bas de page. Laissez `""` pour ne rien afficher.
- `facebook` : adresse complète de la page Facebook. Laissez `""` pour masquer le lien.

---

## 9. Aide-mémoire Markdown

| J'écris… | J'obtiens… |
|---|---|
| `**texte important**` | **texte important** |
| `*texte en italique*` | *texte en italique* |
| `## Mon sous-titre` | un sous-titre |
| `### Un plus petit titre` | un titre de niveau inférieur |
| `- un élément` | une liste à puces |
| `1. premier` | une liste numérotée |
| `[texte du lien](https://exemple.fr)` | un lien vers un autre site |
| `[page Contacts](/contacts/)` | un lien vers une page du site |
| `[écrire à l'équipe](mailto:adresse@gmail.com)` | un lien e-mail |
| `![description](/images/projets/photo.jpg)` | une image dans le texte |

- Laissez une **ligne vide** entre deux paragraphes.
- Pas besoin de `#` (titre principal) : le titre de la page vient du champ `title`.

Adresses internes utiles : `/`, `/projets/`, `/ecoles/`, `/partenariats/`, `/contacts/`, `/nous-rejoindre/`.

---

## 10. Ça n'a pas marché ?

### Le site n'a pas changé

- Attendez 2 minutes, puis rechargez la page en vidant le cache : **Ctrl+F5**, ou **Cmd+Shift+R** sur Mac.
- Regardez l'onglet **Actions** du dépôt.

### Une croix rouge ❌ apparaît dans « Actions »

Pas de panique : **le site en ligne n'a pas été modifié**, il garde sa version précédente.

1. Cliquez sur la ligne en erreur, puis sur **« build »**.
2. Dépliez l'étape en rouge et cherchez le message d'erreur. Il indique généralement **le fichier et le champ en cause**, par exemple :
   - `ecoles → …` puis `email: Invalid email address` → adresse e-mail mal écrite ;
   - `niveau: Invalid option: expected one of "maternelle"|"elementaire"|"college"` → niveau mal orthographié (attention aux accents) ;
   - `date: Expected type "date"` → la date n'est pas au format AAAA-MM-JJ ;
   - `Le fichier ./src/data/… n'est pas un JSON valide` → virgule ou guillemet en trop ou manquant dans ce fichier `.json` ;
   - `title: Required` → le champ `title` est absent de l'en-tête d'un projet.
3. Corrigez le fichier concerné et enregistrez à nouveau.

### Revenir à la version précédente d'un fichier

1. Ouvrez le fichier, puis cliquez sur **« History »** en haut à droite.
2. Cliquez sur la version précédente, puis sur **« View file »** (ou l'icône `<>`).
3. Copiez son contenu, revenez au fichier actuel, cliquez sur le crayon ✏️, remplacez tout le contenu et enregistrez.

### Toujours bloqué ?

Contactez le responsable technique du site en lui indiquant le fichier modifié et une capture d'écran du message d'erreur.
