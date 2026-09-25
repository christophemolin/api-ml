// Menu principal du site (en-tête et pied de page)
export const navigation = [
  { label: 'Accueil', href: '/' },
  { label: 'Projets', href: '/projets/' },
  { label: 'Écoles', href: '/ecoles/' },
  { label: 'Partenariats', href: '/partenariats/' },
  { label: 'Contacts', href: '/contacts/' },
  { label: 'Nous rejoindre', href: '/nous-rejoindre/', cta: true },
];

export const niveaux = {
  maternelle: 'Maternelles',
  elementaire: 'Élémentaires',
  college: 'Collèges',
} as const;
