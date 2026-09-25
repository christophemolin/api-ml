const formatMoisAnnee = new Intl.DateTimeFormat('fr-FR', { month: 'long', year: 'numeric', timeZone: 'UTC' });

/** « décembre 2025 » */
export function formaterDate(date: Date): string {
  return formatMoisAnnee.format(date);
}
