"""Reconstruit la page des posts Google manuels à partir des posts à venir (champ "google").

Usage : python3 -I google-manuel/build.py   (depuis le dossier zernio)
Écrit google-manuel/posts.json, google-manuel/images/*.jpg et met à jour les fiches
de google-manuel/posts-google.html (l'en-tête et le style de la page sont conservés).
"""
import glob
import html
import json
import os
import re
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from PIL import Image

OUT = 'google-manuel'
URL = 'https://www.construisez.fr/?utm_source=google&utm_medium=gbp&utm_campaign=posts'
PARIS = ZoneInfo('Europe/Paris')
JOURS = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']
MOIS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']

local = {}
for f in glob.glob('visuels/*/urls.json'):
    for name, url in json.load(open(f, encoding='utf-8')).items():
        local[url] = os.path.join(os.path.dirname(f), name)

now = datetime.now(timezone.utc)
posts = []
for f in glob.glob('posts/*.json'):
    if f.endswith('lieux.json'):
        continue
    for p in json.load(open(f, encoding='utf-8')):
        if p.get('google', {}).get('image') and datetime.fromisoformat(p['date']) > now:
            posts.append(p)
posts.sort(key=lambda p: p['date'])

for old in glob.glob(f'{OUT}/images/*.jpg'):
    os.remove(old)
os.makedirs(f'{OUT}/images', exist_ok=True)

entries, cards = [], []
for i, p in enumerate(posts, 1):
    d = datetime.fromisoformat(p['date']).astimezone(PARIS)
    src = local[p['google']['image']]
    image = f"images/{i:02d}-{os.path.splitext(os.path.basename(src))[0]}.jpg"
    Image.open(src).convert('RGB').save(f'{OUT}/{image}', 'JPEG', quality=85)
    e = {
        'id': d.strftime('%Y-%m-%d'),
        'jour': f"{JOURS[d.weekday()]} {d.day} {MOIS[d.month - 1]}",
        'heure': d.strftime('%H:%M'),
        'titre': re.sub(r'^Réalisation : ', '', p['theme']),
        'ville': p.get('city', 'Saint-Maur-des-Fossés (94)'),
        'texte': p['google']['content'],
        'image': image,
    }
    entries.append(e)
    cards.append(f'''
<article class="post" id="p{e['id']}" data-id="{e['id']}">
  <header class="post-head">
    <div class="when"><span class="n">{i:02d}</span><span class="day">{html.escape(e['jour'])}</span><span class="time">dès {e['heure']}</span></div>
    <label class="done"><input type="checkbox" id="done-{e['id']}"> Publié</label>
  </header>
  <h2>{html.escape(e['titre'])}</h2>
  <p class="city">📍 {html.escape(e['ville'])}</p>
  <div class="body">
    <figure><img src="{e['image']}" alt="Image du post : {html.escape(e['titre'])}" loading="lazy" width="1200" height="900"><figcaption>Appui long (téléphone) ou clic droit : « Enregistrer l'image »</figcaption></figure>
    <div class="txt">
      <div class="label-row"><span class="lab">Texte de l'actualité</span><button type="button" class="copy" data-target="t-{e['id']}">Copier le texte</button></div>
      <pre id="t-{e['id']}" class="text">{html.escape(e['texte'])}</pre>
      <div class="label-row"><span class="lab">Bouton : En savoir plus</span><button type="button" class="copy" data-target="u-{e['id']}">Copier le lien</button></div>
      <code id="u-{e['id']}" class="url">{URL}</code>
    </div>
  </div>
</article>''')

json.dump(entries, open(f'{OUT}/posts.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
page = open(f'{OUT}/posts-google.html', encoding='utf-8').read()
start = page.index('<p class="progress" id="progress"></p>') + len('<p class="progress" id="progress"></p>')
end = page.index('</main>')
page = page[:start] + '\n  ' + ''.join(cards) + '\n' + page[end:]
open(f'{OUT}/posts-google.html', 'w', encoding='utf-8').write(page)
print(f'{len(entries)} posts : {entries[0]["jour"]} → {entries[-1]["jour"]}')
