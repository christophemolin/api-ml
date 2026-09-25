# api-ml.info : site de l'API Maisons-Laffitte

Site vitrine de l'**Association des Parents Indépendants** (API) de Maisons-Laffitte.

- **Technologie** : [Astro](https://astro.build) (générateur de site statique), sans base de données.
- **Hébergement** : GitHub Pages (gratuit), déployé automatiquement à chaque modification de la branche `main`.
- **Contenu** : fichiers Markdown (`.md`) et JSON (`.json`) dans le dépôt.

> 👉 **Vous voulez juste modifier un texte, un contact ou ajouter un projet ?**
> Lisez le [guide d'édition pour les non-développeurs](docs/GUIDE-EDITION.md). Aucune installation n'est nécessaire, tout se fait depuis le site github.com.

---

## Pages du site

| Page | Adresse | Contenu modifiable dans |
|---|---|---|
| Accueil | `/` | `src/content/pages/accueil.md` |
| Projets | `/projets/` | `src/content/projets/*.md` (un fichier par projet) |
| Écoles | `/ecoles/` | `src/data/ecoles.json` |
| Partenariats | `/partenariats/` | `src/data/partenaires.json` |
| Contacts | `/contacts/` | `src/data/ecoles.json` + `src/data/site.json` |
| Nous rejoindre | `/nous-rejoindre/` | `src/content/pages/nous-rejoindre.md` |

## Structure du projet

```
├── .github/workflows/deploy.yml   Déploiement automatique sur GitHub Pages
├── brand/                         Logos originaux (.ai / .pdf), non publiés sur le site
├── docs/GUIDE-EDITION.md          Guide pour les éditeurs non développeurs
├── public/                        Fichiers servis tels quels
│   ├── CNAME                      Nom de domaine (api-ml.info)
│   ├── logos/                     Logos PNG
│   └── images/                    Illustrations et images des projets
└── src/
    ├── content.config.ts          Schémas de validation du contenu
    ├── content/
    │   ├── pages/                 Textes des pages Accueil et Nous rejoindre
    │   └── projets/               Un fichier .md par projet (_exemple.md = modèle)
    ├── data/
    │   ├── site.json              Nom, slogan, e-mail général, lien Facebook
    │   ├── ecoles.json            Écoles et e-mails des équipes API
    │   └── partenaires.json       Partenaires
    ├── components/                En-tête, pied de page, cartes…
    ├── layouts/BaseLayout.astro   Gabarit commun (balises <head>, SEO)
    ├── pages/                     Une page .astro par adresse du site
    ├── styles/global.css          Couleurs et styles globaux
    └── navigation.ts              Menu principal
```

Le contenu est **validé à la construction** (`src/content.config.ts`). Une erreur, par exemple un e-mail mal formé, une date invalide ou un champ obligatoire manquant, fait échouer la construction avec un message explicite. Dans ce cas, le site en ligne n'est pas modifié.

## Développement local

Prérequis : **Node.js 22.12 ou plus** (`node -v`).

```bash
npm install        # installe les dépendances
npm run dev        # site de développement sur http://localhost:4321 (rechargement automatique)
npm run build      # construit le site statique dans dist/
npm run preview    # sert le contenu de dist/ pour vérifier avant mise en ligne
```

## Déploiement

Le fichier `.github/workflows/deploy.yml` construit le site et le publie sur GitHub Pages **à chaque push sur `main`**. Il peut aussi être lancé à la main depuis l'onglet *Actions*, via « Run workflow ».

### Première mise en ligne

1. Créer le dépôt sur GitHub et y pousser le code (branche `main`).
2. Dans **Settings → Pages**, choisir *Source : GitHub Actions*.
3. Vérifier dans l'onglet **Actions** que le déploiement passe au vert.
4. Dans **Settings → Pages → Custom domain**, saisir `api-ml.info` (déjà présent dans `public/CNAME`).
5. Chez le registrar du domaine, configurer les DNS :
   - 4 enregistrements **A** pour `api-ml.info` : `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - (optionnel, IPv6) 4 enregistrements **AAAA** : `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`
   - 1 enregistrement **CNAME** pour `www` pointant vers `<compte-github>.github.io`
6. Une fois les DNS propagés (de quelques minutes à 24 h), cocher **Enforce HTTPS** dans Settings → Pages.

> Le site utilise des liens à la racine (`/contacts/`…). Il est donc prévu pour être servi sur le domaine `api-ml.info`, et non sur une adresse du type `compte.github.io/depot/`. Pour le vérifier avant de basculer les DNS, utilisez `npm run build && npm run preview` en local.

## Points d'attention

- Le dossier `API/` (anciens documents de travail) est dans `.gitignore` et **ne doit jamais être publié** : il contient des données personnelles. Le site n'en dépend pas.
- Le dépôt est public : n'y mettez que des informations destinées à être publiques.
- Les images déposées dans `public/images/` doivent être raisonnablement légères (moins de 500 Ko si possible).
