import { defineCollection } from 'astro:content';
import { file, glob } from 'astro/loaders';
import { z } from 'astro/zod';
import { readFile } from 'node:fs/promises';

// Le loader `file()` d'Astro se contente d'un avertissement si le JSON est
// invalide (le site serait publié sans écoles ni partenaires). On vérifie donc
// la syntaxe nous-mêmes pour faire échouer la construction.
function fichierJson(chemin: string) {
  const loader = file(chemin);
  return {
    ...loader,
    load: async (contexte: Parameters<typeof loader.load>[0]) => {
      try {
        JSON.parse(await readFile(chemin, 'utf-8'));
      } catch (erreur) {
        throw new Error(
          `Le fichier ${chemin} n'est pas un JSON valide (virgule ou guillemet en trop ou manquant ?) : ${(erreur as Error).message}`,
        );
      }
      return loader.load(contexte);
    },
  };
}

// Textes des pages (Accueil, Nous rejoindre…) : src/content/pages/*.md
const pages = defineCollection({
  loader: glob({ pattern: '*.md', base: './src/content/pages' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    // Blocs illustrés affichés sous forme de cartes (optionnel)
    points: z
      .array(
        z.object({
          titre: z.string(),
          texte: z.string(),
          image: z.string().optional(),
        }),
      )
      .default([]),
  }),
});

// Projets : un fichier .md par projet dans src/content/projets/
// Les fichiers commençant par "_" (ex. _exemple.md) sont ignorés.
const projets = defineCollection({
  loader: glob({ pattern: '[!_]*.md', base: './src/content/projets' }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    summary: z.string(),
    image: z.string().optional(),
    imageAlt: z.string().optional(),
    draft: z.boolean().default(false),
  }),
});

// Écoles et adresses e-mail des équipes API : src/data/ecoles.json
const ecoles = defineCollection({
  loader: fichierJson('./src/data/ecoles.json'),
  schema: z.object({
    nom: z.string(),
    niveau: z.enum(['maternelle', 'elementaire', 'college']),
    email: z.email(),
    site: z.url().optional(),
  }),
});

// Partenaires : src/data/partenaires.json
const partenaires = defineCollection({
  loader: fichierJson('./src/data/partenaires.json'),
  schema: z.object({
    nom: z.string(),
    categorie: z.enum(['parents', 'institutions', 'solidarite']),
    description: z.string(),
    site: z.url().optional(),
  }),
});

export const collections = { pages, projets, ecoles, partenaires };
