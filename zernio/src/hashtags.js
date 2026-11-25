// Instagram limite progressivement les légendes à 5 hashtags (annonce de décembre 2025), et TikTok
// conseille quelques hashtags précis plutôt qu'une longue liste. On garde donc 5 hashtags au plus :
// jusqu'à 3 hashtags propres au sujet, #permisdeconstruire, puis un hashtag local (département, sinon #iledefrance).
const GENERIC = new Set(['#urbanisme', '#construction', '#renovation', '#maison', '#architecture', '#mairie', '#travaux',
  '#conseilimmobilier', '#immobilier', '#iledefrance', '#permisdeconstruire', '#declarationprealable']);
const LOCAL = new Set(['#valdoise', '#seineetmarne', '#essonne', '#valdemarne', '#yvelines', '#hautsdeseine', '#seinesaintdenis', '#paris']);
export const MAX_TAGS = 5;

export function pickTags(tags) {
  const uniq = [...new Set(tags.map((t) => t.toLowerCase()))];
  const local = uniq.find((t) => LOCAL.has(t)) ?? '#iledefrance';
  const specific = uniq.filter((t) => !GENERIC.has(t) && !LOCAL.has(t)).slice(0, 3);
  const fill = ['#declarationprealable', '#urbanisme', '#renovation'].filter((t) => uniq.includes(t));
  const head = [...new Set([...specific, '#permisdeconstruire', ...fill])].slice(0, MAX_TAGS - 1);
  return [...head, local];
}

// Remplace la dernière ligne de hashtags d'une légende par une sélection de 5 au plus.
export function limitHashtags(text) {
  if (!text) return text;
  const lines = text.split('\n');
  const i = lines.map((l) => /^\s*#/.test(l)).lastIndexOf(true);
  if (i < 0) return text;
  const tags = lines[i].match(/#[\p{L}\d_]+/gu) ?? [];
  if (tags.length <= MAX_TAGS) return text;
  lines[i] = pickTags(tags).join(' ');
  return lines.join('\n');
}
