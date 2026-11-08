import { readdir, readFile, writeFile, stat } from 'node:fs/promises';
import path from 'node:path';
import { zernio } from './zernio-client.js';

// Envoie les images d'un dossier sur le stockage Zernio et enregistre leurs URL publiques
// dans <dossier>/urls.json ({ "nom.png": "https://..." }). Les fichiers déjà envoyés sont ignorés.
//
// Usage : npm run upload -- visuels/novembre-2026

const dir = process.argv[2];
if (!dir) {
  console.error('Usage : npm run upload -- <dossier d\'images>');
  process.exit(1);
}

const types = { '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.mp4': 'video/mp4' };
const urlsFile = path.join(dir, 'urls.json');
const urls = await readFile(urlsFile, 'utf8').then(JSON.parse).catch(() => ({}));

for (const name of (await readdir(dir)).sort()) {
  const contentType = types[path.extname(name).toLowerCase()];
  if (!contentType || urls[name]) continue;
  const file = path.join(dir, name);
  const { data, error } = await zernio.media.getMediaPresignedUrl({
    body: { filename: name, contentType, size: (await stat(file)).size },
  });
  if (error || !data?.uploadUrl) {
    console.error(`❌ ${name} : ${JSON.stringify(error ?? data)}`);
    continue;
  }
  const res = await fetch(data.uploadUrl, {
    method: 'PUT',
    headers: { 'Content-Type': contentType },
    body: await readFile(file),
  });
  if (!res.ok) {
    console.error(`❌ ${name} : envoi refusé (${res.status})`);
    continue;
  }
  urls[name] = data.publicUrl;
  console.log(`✅ ${name} → ${data.publicUrl}`);
}

await writeFile(urlsFile, JSON.stringify(urls, null, 2) + '\n');
console.log(`\nURL enregistrées dans ${urlsFile}`);
