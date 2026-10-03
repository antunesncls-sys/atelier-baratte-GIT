#!/usr/bin/env python3
"""Génère le site statique JMC Couverture.

Usage : python3 _build/build.py   (depuis le dossier jmc-couverture/)

Les pages gardent les URL de l'ancien site (/charpente/, /couverture/, ...)
pour conserver le référencement acquis. Chaque page sort dans <slug>/index.html.
"""
import json
import subprocess
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://jmccouverture.com"
TODAY = date.today().isoformat()

BIZ = {
    "name": "JMC Couverture",
    "legal": "Société JMC",
    "phone": "01 64 21 38 37",
    "phone_intl": "+33164213837",
    "email": "contact@jmccouverture.com",
    "street": "97 rue Charles Van Wyngene",
    "zip": "77181",
    "city": "Courtry",
    # Fiche Google Business Profile (kgmid /g/11y2n5k3zl)
    "gbp": "https://www.google.com/search?kgmid=/g/11y2n5k3zl&q=JMC+COUVERTURE",
    # Adresse du compte Instagram (ex. "https://www.instagram.com/xxx/") : les liens s'affichent dès qu'elle est renseignée
    "instagram": "",
}

CITIES = [
    "Courtry", "Chelles", "Le Pin", "Villeparisis", "Vaujours", "Coubron",
    "Montfermeil", "Clichy-sous-Bois", "Livry-Gargan", "Sevran", "Brou-sur-Chantereine",
    "Vaires-sur-Marne", "Claye-Souilly", "Mitry-Mory", "Le Raincy", "Villemomble",
    "Gagny", "Neuilly-sur-Marne", "Noisy-le-Grand", "Noisy-le-Sec", "Torcy",
    "Lagny-sur-Marne", "Pontault-Combault", "Nogent-sur-Marne", "Maisons-Alfort", "Paris",
]

DEPTS = ("Paris", "Seine-et-Marne", "Yvelines", "Essonne", "Hauts-de-Seine", "Seine-Saint-Denis", "Val-de-Marne", "Val-d'Oise")

NAV = [
    ("/renovation-toiture/", "Rénovation"),
    ("/nettoyage-toiture/", "Nettoyage"),
    ("/toiture-maison-neuve/", "Maison neuve"),
    ("/couverture/", "Couverture"),
    ("/charpente/", "Charpente"),
    ("/zinguerie/", "Zinguerie"),
    ("/nos-references/", "Références"),

]

# ---------------------------------------------------------------- icônes SVG
ICON = {
    "roof": '<svg viewBox="0 0 24 24" fill="none" stroke="#d41d22" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 12 12 4l10 8"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/></svg>',
    "beam": '<svg viewBox="0 0 24 24" fill="none" stroke="#d41d22" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 20 12 5l9 15"/><path d="M7 13h10"/><path d="M12 5v15"/></svg>',
    "drop": '<svg viewBox="0 0 24 24" fill="none" stroke="#d41d22" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 6h18v3a3 3 0 0 1-3 3H6a3 3 0 0 1-3-3z"/><path d="M17 12v9"/><path d="M15 21h4"/></svg>',
    "alert": '<svg viewBox="0 0 24 24" fill="none" stroke="#d41d22" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3 2 20h20z"/><path d="M12 10v4"/><path d="M12 17h.01"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="#d41d22" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/><path d="m9 12 2 2 4-4"/></svg>',
    "leaf": '<svg viewBox="0 0 24 24" fill="none" stroke="#d41d22" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 19c9 0 14-6 14-15C10 4 5 9 5 19z"/><path d="M5 19 13 11"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="#d41d22" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    "doc": '<svg viewBox="0 0 24 24" fill="none" stroke="#d41d22" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 3h9l4 4v14H6z"/><path d="M9 12h6M9 16h6"/></svg>',
}
HERO_ART = ('<svg class="hero-art" viewBox="0 0 400 260" aria-hidden="true"><path d="M10 150 200 20l190 130" fill="none" '
            'stroke="#fff" stroke-width="14"/><path d="M50 130v120h300V130" fill="none" stroke="#fff" stroke-width="10"/>'
            '<path d="M280 70V20h40v80" fill="none" stroke="#fff" stroke-width="10"/></svg>')


# ---------------------------------------------------------------- photos
# Déposer les fichiers dans assets/photos/ avec ces noms (jpg, jpeg, webp ou png) puis relancer le build :
# chaque photo n'est intégrée que si le fichier existe.
PHOTOS = {
    "pavillon": ("toiture-pavillon-renovation-jmc",
                 "Pavillon dont la toiture a été rénovée par JMC Couverture",
                 "Rénovation de la toiture d'un pavillon."),
    "mansarde": ("toiture-mansardee-lucarnes-zinc-jmc",
                 "Maison bourgeoise à toiture mansardée avec lucarnes habillées de zinc",
                 "Toiture mansardée : brisis et lucarnes habillées de zinc."),
    "meuliere": ("maison-meuliere-couverture-tuiles-jmc",
                 "Maison en meulière avec couverture en tuiles refaite par JMC",
                 "Maison en meulière : couverture en tuiles et zinguerie."),
    "depot": ("depot-flotte-vehicules-jmc-couverture",
              "Les locaux et la flotte de véhicules de l'entreprise JMC Couverture",
              "Nos locaux et notre flotte de véhicules d'intervention."),
}


def photo_src(key):
    base = PHOTOS[key][0]
    for ext in ("webp", "jpg", "jpeg", "png"):
        if (ROOT / "assets" / "photos" / f"{base}.{ext}").exists():
            return f"/assets/photos/{base}.{ext}"
    return None


def photo(key, eager=False):
    src = photo_src(key)
    if not src:
        return ""
    _, alt, cap = PHOTOS[key]
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    w, h = photo_dims(src)
    return (f'<figure class="photo"><img src="{src}" alt="{alt}" {load} decoding="async" width="{w}" height="{h}">'
            f'<figcaption>{cap}</figcaption></figure>')


def photo_dims(src):
    out = subprocess.run(["identify", "-format", "%w %h", str(ROOT / src.lstrip("/"))], capture_output=True, text=True).stdout
    return tuple(out.split()) if out else (1200, 800)


def hero_mosaic():
    keys = [k for k in ("meuliere", "mansarde", "pavillon", "depot") if photo_src(k)]
    if not keys:
        return ""
    items = "".join(
        f'<figure><img src="{photo_src(k)}" alt="{PHOTOS[k][1]}" fetchpriority="high" decoding="async" '
        f'width="{photo_dims(photo_src(k))[0]}" height="{photo_dims(photo_src(k))[1]}"><figcaption>{PHOTOS[k][2]}</figcaption></figure>'
        for k in keys)
    return f'<div class="mosaic">{items}</div>'


def insta_link(sep=""):
    if not BIZ["instagram"]:
        return ""
    return f'{sep}<a href="{BIZ["instagram"]}" target="_blank" rel="noopener">Suivez-nous sur Instagram</a>'


def insta_top():
    if not BIZ["instagram"]:
        return ""
    return f' · <a href="{BIZ["instagram"]}" target="_blank" rel="noopener">Instagram</a>'


def hero_style(key):
    src = photo_src(key)
    return f' style="--hero-img:url({src})"' if src else ""


# ---------------------------------------------------------------- JSON-LD
def org_ld():
    return {
        "@context": "https://schema.org",
        "@type": "RoofingContractor",
        "@id": SITE + "/#entreprise",
        "name": BIZ["name"],
        "legalName": BIZ["legal"],
        "url": SITE + "/",
        "logo": SITE + "/assets/logo-jmc-40ans.png",
        "foundingDate": "1985",
        "image": SITE + "/assets/og-jmc-couverture.jpg",
        "telephone": BIZ["phone_intl"],
        "email": BIZ["email"],
        "priceRange": "Devis gratuit",
        "sameAs": [u for u in (BIZ["gbp"], BIZ["instagram"]) if u],
        "hasMap": BIZ["gbp"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": BIZ["street"],
            "postalCode": BIZ["zip"],
            "addressLocality": BIZ["city"],
            "addressRegion": "Île-de-France",
            "addressCountry": "FR",
        },
        "areaServed": [{"@type": "State", "name": "Île-de-France"}]
        + [{"@type": "AdministrativeArea", "name": n} for n in DEPTS]
        + [{"@type": "City", "name": c} for c in CITIES],
        "knowsAbout": ["Couverture", "Charpente", "Zinguerie", "Rénovation de toiture",
                       "Remplacement de toiture", "Nettoyage de toiture", "Démoussage", "Isolation de toiture", "Gouttières", "Toiture zinc", "Ardoise", "Tuiles"],
        "hasCredential": [
            {"@type": "EducationalOccupationalCredential", "credentialCategory": "Qualification", "name": "QUALIBAT"},
            {"@type": "EducationalOccupationalCredential", "credentialCategory": "Label", "name": "RGE - Reconnu Garant de l'Environnement"},
        ],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Travaux de toiture",
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n, "url": SITE + u}}
                for n, u in (("Couverture et rénovation de toiture", "/couverture/"),
                             ("Charpente bois et métallique", "/charpente/"),
                             ("Zinguerie et gouttières", "/zinguerie/"),
                             ("Nettoyage et démoussage de toiture", "/nettoyage-toiture/"),
                             ("Rénovation et remplacement de toiture", "/renovation-toiture/"),
                             ("Toiture de maison neuve", "/toiture-maison-neuve/"))
            ],
        },
    }


def website_ld():
    return {"@context": "https://schema.org", "@type": "WebSite", "@id": SITE + "/#site",
            "url": SITE + "/", "name": BIZ["name"], "inLanguage": "fr-FR",
            "publisher": {"@id": SITE + "/#entreprise"}}


def crumbs_ld(trail):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u}
                                for i, (u, n) in enumerate(trail)]}


def faq_ld(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}


def service_ld(name, url, desc):
    return {"@context": "https://schema.org", "@type": "Service", "name": name, "serviceType": name,
            "description": desc, "url": SITE + url, "provider": {"@id": SITE + "/#entreprise"},
            "areaServed": [{"@type": "State", "name": "Île-de-France"}]
            + [{"@type": "AdministrativeArea", "name": n} for n in DEPTS]}


# ---------------------------------------------------------------- gabarits
def head(title, desc, path, lds, robots="index,follow"):
    canonical = SITE + path
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#ee2428">
<meta name="geo.region" content="FR-77">
<meta name="geo.placename" content="Courtry">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="{BIZ['name']}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/assets/og-jmc-couverture.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;700;800&display=swap">
<link rel="stylesheet" href="/assets/style.css">
{ld}
</head>
<body>
<a class="skip" href="#contenu">Aller au contenu</a>"""


def header(path):
    cur = ' aria-current="page"'
    links = "".join(f'<a href="{u}"{cur if u == path else ""}>{n}</a>' for u, n in NAV)
    return f"""
<div class="topbar"><div class="wrap">
  <span>Couvreur certifié QUALIBAT &amp; RGE · Intervention dans toute l'Île-de-France{insta_top()}</span>
  <span>Devis gratuit : <a href="tel:{BIZ['phone_intl']}"><strong>{BIZ['phone']}</strong></a></span>
</div></div>
<header class="site-header"><div class="wrap">
  <a class="logo" href="/" aria-label="JMC Couverture, accueil"><img src="/assets/logo-jmc-40ans.svg" alt="JMC Couverture – 40 ans, 1985-2025" width="141" height="63"></a>
  <button class="menu-toggle" aria-label="Ouvrir le menu" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
  <nav class="nav" id="nav" aria-label="Navigation principale">{links}<a class="btn btn-primary" href="/contact/">Devis gratuit</a></nav>
</div></header>
<main id="contenu">"""


def breadcrumb(trail):
    items = []
    for i, (u, n) in enumerate(trail):
        if i == len(trail) - 1:
            items.append(f'<li aria-current="page">{n}</li>')
        else:
            items.append(f'<li><a href="{u}">{n}</a></li>')
    return f'<nav class="breadcrumb" aria-label="Fil d\'Ariane"><ol>{"".join(items)}</ol></nav>'


def page_hero(trail, eyebrow, h1, lead, cta=True):
    btns = (f'<div class="hero-cta"><a class="btn btn-primary" href="/contact/">Demander un devis gratuit</a>'
            f'<a class="btn btn-ghost" href="tel:{BIZ["phone_intl"]}">Appeler le {BIZ["phone"]}</a></div>') if cta else ""
    return f"""
<section class="hero page-hero">{HERO_ART}<div class="wrap"><div>
  {breadcrumb(trail)}
  <span class="eyebrow">{eyebrow}</span>
  <h1>{h1}</h1>
  <p class="lead">{lead}</p>
  {btns}
</div></div></section>"""


def cta_band(title="Un projet de toiture ? Parlons-en.",
             text="Visite sur place et devis détaillé gratuits, sans engagement."):
    return f"""
<section class="cta-band"><div class="wrap">
  <div><h2>{title}</h2><p>{text}</p></div>
  <div class="hero-cta" style="margin:0"><a class="btn btn-dark" href="/contact/">Demander mon devis</a>
  <a class="btn btn-ghost" href="tel:{BIZ['phone_intl']}">{BIZ['phone']}</a></div>
</div></section>"""


def faq_html(faq, title="Questions fréquentes"):
    items = "".join(f"<details><summary>{q}</summary><div><p>{a}</p></div></details>" for q, a in faq)
    return f'<section class="section-alt"><div class="wrap prose"><h2>{title}</h2>{items}</div></section>'


def aside(title="Pourquoi choisir JMC ?"):
    return f"""
<aside class="aside">
  <h2>{title}</h2>
  <ul class="checks">
    <li>40 ans d'expérience (depuis 1985)</li>
    <li>Entreprise certifiée QUALIBAT et RGE</li>
    <li>Garantie décennale et responsabilité civile</li>
    <li>Plus de 1 500 chantiers réalisés</li>
    <li>Isolation RGE : aides possibles</li>
    <li>Devis gratuit et détaillé</li>
  </ul>
  <p><a class="btn btn-primary" href="/contact/">Devis gratuit</a></p>
  <p class="small">Ou par téléphone : <a href="tel:{BIZ['phone_intl']}"><strong>{BIZ['phone']}</strong></a></p>
</aside>"""


def footer():
    city_links = ", ".join(CITIES[:12])
    return f"""
</main>
<footer class="site-footer"><div class="wrap">
  <div class="footer-grid">
    <div>
      <a class="logo logo-footer" href="/"><img src="/assets/logo-jmc-40ans.svg" alt="JMC Couverture" width="180" height="80" loading="lazy"></a>
      <p style="margin-top:16px">Entreprise de couverture, charpente et zinguerie basée à Courtry (77), intervenant dans toute l'Île-de-France. Depuis 1985, 40 ans d'expérience au service des particuliers, des collectivités et des professionnels en Île-de-France.</p>
    </div>
    <div><h2>Nos métiers</h2><ul>
      <li><a href="/couverture/">Couverture &amp; rénovation de toiture</a></li>
      <li><a href="/charpente/">Charpente</a></li>
      <li><a href="/zinguerie/">Zinguerie &amp; gouttières</a></li>
      <li><a href="/renovation-toiture/">Rénovation &amp; remplacement de toiture</a></li>
      <li><a href="/nettoyage-toiture/">Nettoyage &amp; démoussage de toiture</a></li>
      <li><a href="/toiture-maison-neuve/">Toiture de maison neuve</a></li>
    </ul></div>
    <div><h2>L'entreprise</h2><ul>
      <li><a href="/nos-references/">Nos références</a></li>
      <li><a href="/zones-intervention/">Zones d'intervention</a></li>
      <li><a href="/contact/">Contact &amp; devis</a></li>
      <li><a href="/mentions-legales/">Mentions légales</a></li>
    </ul></div>
    <div><h2>Contact</h2>
      <address style="font-style:normal">{BIZ['legal']}<br>{BIZ['street']}<br>{BIZ['zip']} {BIZ['city']}</address>
      <p style="margin-top:10px"><a href="tel:{BIZ['phone_intl']}"><strong>{BIZ['phone']}</strong></a><br>
      <a href="mailto:{BIZ['email']}">{BIZ['email']}</a><br>
      <a href="{BIZ['gbp']}" target="_blank" rel="noopener">Notre fiche Google</a>{insta_link("<br>")}</p>
    </div>
  </div>
  <p class="small" style="margin-top:28px;color:#8c98a4">Couvreur à {city_links} et dans toute l'Île-de-France : Paris, Seine-et-Marne, Yvelines, Essonne, Hauts-de-Seine, Seine-Saint-Denis, Val-de-Marne et Val-d'Oise.</p>
  <div class="legal"><span>© {date.today().year} {BIZ['legal']} — Tous droits réservés</span><span>Certifiée QUALIBAT · RGE · Garantie décennale</span></div>
</div></footer>
<a class="btn btn-primary call-fab" href="tel:{BIZ['phone_intl']}">Appeler JMC : {BIZ['phone']}</a>
<script>
(function(){{var b=document.querySelector('.menu-toggle'),n=document.getElementById('nav');
if(b&&n)b.addEventListener('click',function(){{var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o)}});}})();
</script>
</body>
</html>
"""


def write(path, html):
    out = ROOT / path.strip("/") / "index.html" if path.endswith("/") else ROOT / path.lstrip("/")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print("écrit", out.relative_to(ROOT))


def service_card(icon, title, url, text, items):
    li = "".join(f"<li>{i}</li>" for i in items)
    return f"""<article class="card"><div class="icon">{ICON[icon]}</div><h3><a href="{url}" style="color:inherit;text-decoration:none">{title}</a></h3>
<p>{text}</p><ul>{li}</ul><a class="more" href="{url}">En savoir plus →</a></article>"""


REVIEWS = [
    ("José Pereira", "Travail parfait, exécuté dans les règles de l'art."),
    ("M. Goncalves", "Très bon travail, réalisé dans les délais malgré les conditions météorologiques."),
    ("Mme Perraud", "Satisfaite du rendu de ma toiture."),
    ("Michel et Claude Baudry", "Nos remerciements aux équipes de JMC pour la qualité de leurs interventions."),
    ("Valérie Foshia", "Comme toujours, un travail de qualité."),
    ("Mme Lefalher", "Nous avons été très satisfaits de votre intervention et de son efficacité."),
    ("Mme Montes", "Nos remerciements aux couvreurs qui ont accompli les travaux avec sérieux."),
]


def reviews_html(n=3):
    cards = "".join(
        f'<blockquote class="review"><p>« {t} »</p><cite>— {a}</cite></blockquote>' for a, t in REVIEWS[:n])
    return cards


# ================================================================ PAGES
def home():
    faq = [
        ("Quelle zone couvre JMC Couverture ?",
         "Notre entreprise est basée à Courtry (77181) et intervient dans toute l'Île-de-France : Paris, Seine-et-Marne, Yvelines, Essonne, Hauts-de-Seine, Seine-Saint-Denis, Val-de-Marne et Val-d'Oise."),
        ("Le devis est-il gratuit ?",
         "Oui. Nous nous déplaçons pour diagnostiquer votre toiture et nous vous remettons un devis détaillé, gratuit et sans engagement."),
        ("Faut-il nettoyer ou remplacer ma toiture ?",
         "Si la couverture est saine mais couverte de mousse, un nettoyage avec traitement suffit et prolonge sa durée de vie. Si les tuiles sont poreuses, cassées sur de grandes surfaces ou si la toiture a plus de 30 à 50 ans, un remplacement est plus judicieux. Nous vous conseillons honnêtement après une visite gratuite."),
        ("Vos travaux sont-ils garantis ?",
         "Tous nos travaux sont couverts par notre garantie décennale et notre assurance responsabilité civile professionnelle. Nous sommes également certifiés QUALIBAT et RGE."),
        ("Pourquoi faire appel à un couvreur RGE ?",
         "Le label RGE (Reconnu Garant de l'Environnement) est exigé pour que vos travaux d'isolation de toiture puissent bénéficier des aides publiques à la rénovation énergétique, sous réserve des conditions d'éligibilité en vigueur."),
    ]
    lds = [org_ld(), website_ld(), faq_ld(faq)]
    html = head("Rénovation et nettoyage de toiture à Courtry (77) | Couvreur JMC",
                "Couvreur depuis 1985 à Courtry (77) : remplacement de toiture, nettoyage et démoussage, charpente, zinguerie. QUALIBAT & RGE. Devis gratuit ☎ 01 64 21 38 37.",
                "/", lds)
    html += header("/")
    html += f"""
<section class="hero">{HERO_ART}<div class="wrap">
  <div>
    <span class="eyebrow">40 ans · 1985–2025 · Couvreur à Courtry (77)</span>
    <h1>Rénovation et nettoyage de toiture en Île-de-France</h1>
    <p class="lead">Remplacement complet de toiture, démoussage et traitement, charpente et zinguerie neuve : depuis 1985, la société JMC rénove et construit les toitures des maisons de toute l'Île-de-France, avec un seul interlocuteur et une garantie décennale.</p>
    <div class="hero-cta"><a class="btn btn-primary" href="/contact/">Demander un devis gratuit</a>
    <a class="btn btn-ghost" href="tel:{BIZ['phone_intl']}">Appeler le {BIZ['phone']}</a></div>
    <ul class="badges"><li>QUALIBAT</li><li>RGE</li><li>Garantie décennale</li><li>Devis gratuit</li></ul>
  </div>
  {hero_mosaic()}
</div></section>

<section class="visit-band"><div class="wrap">
  <div><strong>Votre toiture a plus de 30 ans ou est couverte de mousse ?</strong>
  <span>Un couvreur se déplace gratuitement pour vous conseiller : nettoyage ou remplacement, avis honnête et devis détaillé.</span></div>
  <a class="btn btn-primary" href="/contact/">Demander une visite gratuite</a>
</div></section>

<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">Nos métiers</span>
  <h2>Rénovation, nettoyage, charpente, zinguerie : un seul interlocuteur pour votre toit</h2>
  <p>De l'entretien de votre couverture à son remplacement complet, nos équipes maîtrisent tous les métiers du toit : un chantier coordonné, des délais tenus et une seule garantie.</p></div>
  <div class="grid g3" style="margin-bottom:24px">
  {service_card("roof", "Rénovation et remplacement de toiture", "/renovation-toiture/", "Réfection complète de votre couverture, de la charpente aux gouttières, avec isolation RGE en option.",
                ["Dépose de l'ancienne couverture", "Contrôle et renfort de charpente", "Écran sous-toiture et couverture neuve", "Isolation de toiture (aides possibles)"])}
  {service_card("leaf", "Nettoyage et démoussage de toiture", "/nettoyage-toiture/", "Redonnez à votre toit son aspect d'origine et prolongez sa durée de vie.",
                ["Démoussage adapté au matériau", "Remplacement des tuiles abîmées", "Traitement anti-mousse et hydrofuge", "Nettoyage des gouttières"])}
  {service_card("beam", "Toiture de maison neuve", "/toiture-maison-neuve/", "Vous faites construire ? Profitez de notre expérience auprès des promoteurs immobiliers.",
                ["Charpente, couverture, zinguerie", "Mise hors d'eau rapide", "Coordination avec votre architecte", "Attestations pour la dommages-ouvrage"])}
  </div>
  <div class="grid g3">
  {service_card("doc", "Couverture", "/couverture/", "Pose de toiture neuve, quel que soit le matériau.",
                ["Tuiles plates et mécaniques", "Ardoise naturelle ou synthétique", "Zinc, bac acier", "Toiture terrasse (membrane EPDM)"])}
  {service_card("beam", "Charpente", "/charpente/", "Charpentes traditionnelles et industrielles, neuves ou à reprendre.",
                ["Pose de charpente neuve", "Renfort et traitement", "Modification pour extension", "Aménagement de combles"])}
  {service_card("drop", "Zinguerie", "/zinguerie/", "Évacuation des eaux pluviales et étanchéité des points singuliers.",
                ["Gouttières et descentes", "Chéneaux et noues", "Entourages de cheminée", "Habillages et bardages zinc"])}
  </div>
</div></section>

<section class="section-dark"><div class="wrap">
  <div class="stats">
    <div><strong>40</strong><span>ans d'expérience</span></div>
    <div><strong>1 500+</strong><span>chantiers réalisés</span></div>
    <div><strong>1 000+</strong><span>clients satisfaits</span></div>
    <div><strong>10 ans</strong><span>garantie décennale</span></div>
  </div>
</div></section>

<section><div class="wrap split">
  <div class="prose">
    <span class="eyebrow">L'entreprise</span>
    <h2>Une entreprise de toiture familière des maisons d'Île-de-France</h2>
    <p>Installée au <strong>{BIZ['street']} à {BIZ['city']}</strong>, la société JMC accompagne depuis 1985 les propriétaires, syndics, collectivités et promoteurs de l'est parisien. Pavillons en tuiles de Chelles ou du Pin, immeubles en zinc à Paris, écoles et bâtiments publics de Seine-Saint-Denis : nous connaissons les matériaux, les règles d'urbanisme et les contraintes de chaque type de bâti.</p>
    <p>Notre approche est simple : <strong>confier vos travaux à des professionnels</strong>. Chaque chantier commence par un diagnostic honnête de votre toiture. Nous vous expliquons ce qui doit être fait tout de suite, ce qui peut attendre, et nous vous remettons un devis clair, poste par poste.</p>
    <h3>Nos engagements</h3>
    <ul class="checks">
      <li><strong>Qualité certifiée</strong> : qualification QUALIBAT et label RGE.</li>
      <li><strong>Sécurité</strong> : garantie décennale et responsabilité civile professionnelle.</li>
      <li><strong>Conseil honnête</strong> : nettoyage ou remplacement, nous vous recommandons la solution adaptée.</li>
      <li><strong>Transparence</strong> : devis gratuit, détaillé et sans engagement.</li>
      <li><strong>Propreté</strong> : chantier protégé, nettoyé et gravats évacués.</li>
    </ul>
  </div>
  {aside()}
</div></section>

<section class="section-alt"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Méthode</span><h2>Comment se déroule votre projet de toiture</h2></div>
  <ol class="steps grid g2">
    <li><strong>Prise de contact</strong><br>Par téléphone ou via le formulaire, vous nous décrivez votre besoin.</li>
    <li><strong>Visite et diagnostic</strong><br>Un couvreur inspecte votre toiture, votre charpente et votre zinguerie.</li>
    <li><strong>Devis détaillé gratuit</strong><br>Matériaux, surfaces, délais : tout est chiffré clairement.</li>
    <li><strong>Travaux et réception</strong><br>Chantier sécurisé, finitions soignées, nettoyage et garantie décennale.</li>
  </ol>
</div></section>

<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">Avis clients</span><h2>Ils nous ont confié leur toiture</h2></div>
  <div class="grid g3">{reviews_html(3)}</div>
  <p style="margin-top:24px"><a class="more" href="/nos-references/">Voir nos références et tous les avis →</a>
  &nbsp;·&nbsp; <a class="more" href="{BIZ['gbp']}" target="_blank" rel="noopener">Nos avis sur Google →</a></p>
</div></section>

<section class="section-alt"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Zone d'intervention</span>
  <h2>Couvreur dans toute l'Île-de-France</h2>
  <p>Depuis notre siège de Courtry, nos équipes interviennent à Paris et dans les huit départements franciliens.</p></div>
  <ul class="cities">{"".join(f"<li>Couvreur {c}</li>" for c in CITIES[:16])}</ul>
  <p><a class="more" href="/zones-intervention/">Toutes nos zones d'intervention →</a></p>
</div></section>
"""
    html += faq_html(faq)
    html += cta_band()
    html += footer()
    write("/", html)


def couverture():
    trail = [("/", "Accueil"), ("/couverture/", "Couverture")]
    faq = [
        ("Quand faut-il refaire sa toiture ?",
         "Plusieurs signes doivent alerter : tuiles cassées, glissées ou poreuses, mousse abondante, traces d'humidité dans les combles, faîtage dégradé ou fuites répétées. Selon le matériau, une couverture dure de 30 ans (bac acier ancien, tuiles béton) à plus de 100 ans (ardoise naturelle, zinc bien entretenu)."),
        ("Combien coûte une réfection de toiture ?",
         "Le prix dépend de la surface, du matériau choisi, de l'accessibilité et de l'état de la charpente. Après visite, nous établissons un devis gratuit et détaillé, poste par poste."),
        ("Peut-on isoler la toiture en même temps ?",
         "Oui, c'est même le moment idéal. Entreprise RGE, nous pouvons intégrer l'isolation par l'extérieur (sarking) ou sous rampants, ce qui peut ouvrir droit à des aides à la rénovation énergétique selon votre situation."),
        ("Quel matériau choisir pour ma toiture ?",
         "Le choix dépend du style de la maison, de la pente du toit, des règles du PLU de votre commune et de votre budget. Nous vous conseillons lors de la visite entre tuiles, ardoise, zinc ou bac acier."),
    ]
    desc = "Réfection, rénovation et réparation de toiture en tuiles, ardoise, zinc, bac acier et toit-terrasse."
    lds = [org_ld(), crumbs_ld(trail), service_ld("Couverture et rénovation de toiture", "/couverture/", desc), faq_ld(faq)]
    html = head("Couvreur Seine-et-Marne : tuiles, ardoise, zinc, bac acier | JMC",
                "Couvreur à Courtry (77) : pose de toiture en tuiles, ardoise, zinc, bac acier et toit-terrasse EPDM. Entreprise QUALIBAT & RGE, garantie décennale. Devis gratuit.",
                "/couverture/", lds)
    html += header("/couverture/")
    html += page_hero(trail, "Couverture", "Couvreur en Seine-et-Marne : toitures en tuiles, ardoise, zinc et bac acier",
                      "Pose neuve ou réfection complète : nos couvreurs travaillent tous les matériaux de couverture, dans le respect des DTU et des règles d'urbanisme locales.")
    html += f"""
<section><div class="wrap split">
  <article class="prose">
    {photo("pavillon", eager=True)}
    <h2>Votre toiture, première protection de votre maison</h2>
    <p>L'intégrité d'une maison dépend en grande partie de la solidité de sa toiture. Elle protège des intempéries, assure la stabilité de la structure, évite les remontées d'humidité et préserve la valeur de votre bien. Une couverture négligée, c'est le risque d'infiltrations, de charpente dégradée et de pertes de chaleur importantes.</p>
    <p>Couvreur à Courtry depuis 1985, JMC intervient sur les pavillons, les immeubles et les bâtiments publics de Seine-et-Marne, de Seine-Saint-Denis et de Paris.</p>

    <h2>Les couvertures que nous posons et rénovons</h2>
    <h3>Toiture en tuiles plates et mécaniques</h3>
    <p>Matériau le plus répandu en Île-de-France, la tuile terre cuite offre une excellente longévité. Nous posons et remplaçons tuiles plates, tuiles mécaniques à emboîtement et tuiles canal, avec reprise du liteaunage, de l'écran sous-toiture et des faîtages.</p>
    <h3>Toiture en ardoise naturelle ou synthétique</h3>
    <p>L'ardoise naturelle, posée au crochet ou au clou, peut durer plus d'un siècle. L'ardoise synthétique (fibres-ciment) constitue une alternative plus économique. Nous intervenons en neuf comme en rénovation, y compris sur les brisis et les lucarnes.</p>
    {photo("meuliere")}
    <h3>Couverture en zinc</h3>
    <p>Signature des toits parisiens, dont le savoir-faire des couvreurs-zingueurs est inscrit au patrimoine culturel immatériel de l'UNESCO, la couverture zinc à joint debout ou à tasseaux convient aussi aux toitures à faible pente et aux extensions contemporaines.</p>
    <h3>Bac acier</h3>
    <p>Léger, rapide à poser et très durable, le bac acier, simple ou isolé (panneaux sandwich), est idéal pour les garages, ateliers, bâtiments industriels et extensions.</p>
    <h3>Toiture terrasse et étanchéité EPDM</h3>
    <p>Pour les toits plats, nous réalisons l'étanchéité par membrane EPDM : une seule pièce, sans joint, résistante aux UV et aux écarts de température.</p>

    <h2>Nos prestations de couverture</h2>
    <ul class="checks">
      <li>Réfection complète de toiture (dépose, écran sous-toiture, liteaunage, couverture neuve)</li>
      <li>Réparation de toiture et remplacement de tuiles ou d'ardoises cassées</li>
      <li>Reprise de faîtage, d'arêtiers et de rives</li>
      <li>Pose de fenêtres de toit et de lucarnes</li>
      <li>Isolation de toiture par l'extérieur (entreprise RGE)</li>
      <li>Nettoyage, démoussage et traitement hydrofuge</li>
    </ul>
    <p>Votre toiture est à bout de souffle ? Voir notre page <a href="/renovation-toiture/">rénovation et remplacement de toiture</a>. Elle est simplement encrassée ? Pensez au <a href="/nettoyage-toiture/">nettoyage et démoussage</a>. Vos gouttières débordent ? Découvrez nos travaux de <a href="/zinguerie/">zinguerie</a>. Votre toiture s'affaisse ? Il faut sans doute reprendre la <a href="/charpente/">charpente</a>.</p>
  </article>
  {aside()}
</div></section>
"""
    html += faq_html(faq, "Questions fréquentes sur la rénovation de toiture")
    html += cta_band("Votre toiture a besoin d'un diagnostic ?")
    html += footer()
    write("/couverture/", html)


def charpente():
    trail = [("/", "Accueil"), ("/charpente/", "Charpente")]
    faq = [
        ("Comment savoir si ma charpente est abîmée ?",
         "Une toiture qui ondule ou s'affaisse, des bois fendus, une poussière de bois au sol des combles, des traces d'humidité ou de champignons sont autant de signes qui imposent un diagnostic par un professionnel."),
        ("Peut-on renforcer une charpente plutôt que la remplacer ?",
         "Souvent, oui. Quand l'essentiel de la structure est sain, nous renforçons ou remplaçons uniquement les pièces dégradées (chevrons, pannes, entraits), ce qui est plus économique qu'une charpente neuve."),
        ("Peut-on modifier une charpente pour aménager des combles ?",
         "Oui. Une charpente à fermettes peut être transformée pour libérer l'espace des combles. Ces travaux nécessitent une étude de structure et, selon les cas, une déclaration préalable ou un permis de construire."),
    ]
    desc = "Pose de charpente neuve traditionnelle ou industrielle, renfort, réparation et modification de charpente."
    lds = [org_ld(), crumbs_ld(trail), service_ld("Charpente", "/charpente/", desc), faq_ld(faq)]
    html = head("Charpentier à Courtry (77) : pose et renfort de charpente | JMC",
                "Charpentier couvreur en Seine-et-Marne : charpente neuve traditionnelle ou industrielle, renfort, traitement, modification pour combles et extension. Devis gratuit.",
                "/charpente/", lds)
    html += header("/charpente/")
    html += page_hero(trail, "Charpente", "Charpentier en Seine-et-Marne : pose, renfort et réparation de charpente",
                      "La charpente porte votre toiture. Nos charpentiers la posent, la renforcent et l'adaptent à vos projets d'agrandissement ou d'aménagement de combles.")
    html += f"""
<section><div class="wrap split">
  <article class="prose">
    <h2>La charpente, squelette de votre toiture</h2>
    <p>Qu'elle soit en bois, en métal ou en béton, la charpente supporte le poids de la couverture, la neige et le vent. Son bon état conditionne la durabilité de tout le toit. Chez JMC, charpente et couverture sont réalisées par la même entreprise : vous gagnez en coordination, en délais et en garantie.</p>

    <h2>Nos travaux de charpente</h2>
    <h3>Pose de charpente neuve traditionnelle ou industrielle</h3>
    <p>Pour une construction neuve, une extension ou une surélévation, nous posons des charpentes traditionnelles (assemblages en bois massif, pannes et chevrons) ou industrielles (fermettes), selon la portée, le budget et l'usage prévu des combles.</p>
    <h3>Renfort de charpente</h3>
    <p>Lorsque le bois a perdu de sa résistance (humidité, insectes xylophages, surcharge après changement de couverture), nous renforçons la structure : moisage, doublage de chevrons, ajout de pannes ou de jambes de force, puis traitement curatif et préventif.</p>
    <h3>Reprise et modification de charpente</h3>
    <p>Agrandissement, création de lucarnes, aménagement de combles : nous modifions la charpente existante pour l'adapter à votre projet, en toute sécurité.</p>

    <h2>Les signes qui doivent vous alerter</h2>
    <ul class="checks">
      <li>Ligne de faîtage ou versants qui se déforment</li>
      <li>Bois fendus, vermoulus ou présentant des galeries</li>
      <li>Traces d'humidité, de moisissure ou de champignons dans les combles</li>
      <li>Fuites récurrentes malgré des réparations de couverture</li>
    </ul>
    <p>Dans ces situations, un diagnostic complet s'impose avant toute <a href="/couverture/">réfection de couverture</a>.</p>

    <h2>Quelques chantiers de charpente</h2>
    <p>Rue de la Croix-Nivert et rue Raffet à Paris, pavillon à Maisons-Alfort, groupes scolaires à Montfermeil… Découvrez <a href="/nos-references/">nos références</a>.</p>
  </article>
  {aside()}
</div></section>
"""
    html += faq_html(faq, "Questions fréquentes sur la charpente")
    html += cta_band()
    html += footer()
    write("/charpente/", html)


def zinguerie():
    trail = [("/", "Accueil"), ("/zinguerie/", "Zinguerie")]
    faq = [
        ("Quel matériau choisir pour mes gouttières ?",
         "Le zinc est le plus courant en Île-de-France pour sa durabilité et son esthétique. Le cuivre est le plus noble et le plus durable. Le PVC et l'aluminium laqué sont des alternatives économiques ou décoratives. Nous vous conseillons selon votre maison et votre budget."),
        ("À quelle fréquence nettoyer ses gouttières ?",
         "Au minimum une fois par an, idéalement à l'automne après la chute des feuilles, et davantage si votre maison est entourée d'arbres. Des gouttières bouchées provoquent des débordements et des infiltrations en façade."),
        ("Pourquoi y a-t-il une fuite autour de ma cheminée ?",
         "L'entourage de cheminée (abergement) est l'un des points les plus sensibles d'une toiture. Un solin fissuré ou un abergement mal raccordé laisse passer l'eau : nous le reprenons en zinc ou en plomb."),
    ]
    desc = "Gouttières, descentes d'eaux pluviales, chéneaux, noues, entourages de cheminée et habillages en zinc et cuivre."
    lds = [org_ld(), crumbs_ld(trail), service_ld("Zinguerie et gouttières", "/zinguerie/", desc), faq_ld(faq)]
    html = head("Zinguerie et gouttières en Seine-et-Marne | JMC Couverture",
                "Zingueur à Courtry (77) : pose et remplacement de gouttières, descentes, chéneaux, noues, entourages de cheminée, habillages zinc et cuivre. Devis gratuit.",
                "/zinguerie/", lds)
    html += header("/zinguerie/")
    html += page_hero(trail, "Zinguerie", "Zinguerie et gouttières : zinc, cuivre, chéneaux et habillages",
                      "Évacuer l'eau de pluie et rendre étanches les points sensibles du toit : la zinguerie protège vos façades, vos fondations et votre charpente.")
    html += f"""
<section><div class="wrap split">
  <article class="prose">
    {photo("mansarde", eager=True)}
    <h2>Le rôle essentiel de la zinguerie</h2>
    <p>La zinguerie regroupe tous les ouvrages métalliques qui recueillent et évacuent l'eau de pluie, ainsi que les raccords d'étanchéité entre la couverture et les autres éléments du bâtiment. Une gouttière percée ou un chéneau mal entretenu suffit à abîmer une façade, à créer des infiltrations ou à fragiliser les fondations.</p>
    <p>Nos zingueurs façonnent et posent sur mesure chaque élément, majoritairement en <strong>zinc</strong> et en <strong>cuivre</strong>, choisis pour leur résistance aux intempéries et leur longévité. Selon le projet et l'esthétique recherchée, nous proposons aussi le PVC et l'aluminium.</p>

    <h2>Nos prestations de zinguerie</h2>
    <h3>Gouttières et descentes d'eaux pluviales</h3>
    <p>Pose, remplacement et réparation de gouttières pendantes, havraises ou nantaises, et de descentes avec leurs dauphins.</p>
    <h3>Chéneaux et noues</h3>
    <p>Réfection des chéneaux encaissés et des noues, zones où l'eau se concentre et qui sont à l'origine de nombreuses fuites.</p>
    <h3>Entourages de cheminée et de fenêtres de toit</h3>
    <p>Abergements, solins et bavettes pour assurer une étanchéité parfaite autour des cheminées, des lucarnes et des fenêtres de toit.</p>
    <h3>Habillages, rives et bardages zinc</h3>
    <p>Habillage de rives, de bandeaux, d'appuis de fenêtres et bardage de façade en zinc, pour une protection durable et une finition élégante.</p>
    <h3>Couvertures zinc et balcons en plomb</h3>
    <p>Nous réalisons également des <a href="/couverture/">couvertures en zinc</a> ainsi que des ouvrages en plomb, comme les balcons du boulevard de Sébastopol à Paris.</p>

    <h2>Entretien de vos gouttières</h2>
    <ul class="checks">
      <li>Nettoyage et débouchage des gouttières et descentes</li>
      <li>Contrôle des pentes et des fixations</li>
      <li>Reprise des soudures et des joints de dilatation</li>
      <li>Pose de crapaudines et de grilles pare-feuilles</li>
    </ul>
  </article>
  {aside()}
</div></section>
"""
    html += faq_html(faq, "Questions fréquentes sur la zinguerie")
    html += cta_band()
    html += footer()
    write("/zinguerie/", html)


def renovation():
    trail = [("/", "Accueil"), ("/renovation-toiture/", "Rénovation de toiture")]
    faq = [
        ("Quand faut-il remplacer sa toiture plutôt que la réparer ?",
         "Quand les défauts se généralisent : tuiles poreuses ou gélives sur l'ensemble des versants, liteaux pourris, absence d'écran sous-toiture, réparations qui se succèdent. Au-delà de 30 à 50 ans pour une couverture en tuiles, une réfection complète revient souvent moins cher à terme qu'une succession de réparations."),
        ("Combien coûte le remplacement d'une toiture ?",
         "Le prix dépend de la surface, du matériau choisi, de la pente, de l'accès au chantier, de l'état de la charpente et des options (isolation, fenêtres de toit, zinguerie neuve). Nous établissons un devis gratuit, détaillé poste par poste, après une visite sur place."),
        ("Combien de temps durent les travaux ?",
         "Pour un pavillon, une réfection complète de couverture dure généralement d'une à trois semaines selon la surface, la complexité du toit et la météo. Votre maison reste protégée pendant toute la durée du chantier."),
        ("Faut-il une autorisation de la mairie ?",
         "Si vous changez l'aspect extérieur (matériau, couleur, ajout de fenêtres de toit), une déclaration préalable de travaux est en général nécessaire. Une réfection à l'identique en est souvent dispensée, mais les règles dépendent du PLU de votre commune : nous vous aidons à vérifier."),
        ("Peut-on bénéficier d'aides pour refaire sa toiture ?",
         "Le remplacement de la couverture seul n'est pas aidé, mais l'isolation de la toiture réalisée en même temps par une entreprise RGE comme JMC peut ouvrir droit à des aides à la rénovation énergétique (MaPrimeRénov', primes CEE, éco-prêt à taux zéro), selon vos revenus et les conditions en vigueur."),
    ]
    desc = "Remplacement et réfection complète de toiture : dépose, contrôle de charpente, écran sous-toiture, couverture neuve, zinguerie et isolation RGE."
    lds = [org_ld(), crumbs_ld(trail), service_ld("Rénovation et remplacement de toiture", "/renovation-toiture/", desc), faq_ld(faq)]
    html = head("Rénovation et remplacement de toiture en Île-de-France | JMC",
                "Remplacement et réfection complète de toiture à Courtry, Chelles, Montfermeil et en Île-de-France. Tuiles, ardoise, zinc, isolation RGE. 40 ans d'expérience. Devis gratuit.",
                "/renovation-toiture/", lds)
    html += header("/renovation-toiture/")
    html += page_hero(trail, "Rénovation de toiture", "Rénovation et remplacement de toiture en Île-de-France",
                      "Votre toiture a fait son temps ? Nous la remplaçons entièrement, de la charpente aux gouttières, avec une seule entreprise, un seul devis et une garantie décennale.")
    html += f"""
<section><div class="wrap split">
  <article class="prose">
    {photo("meuliere", eager=True)}
    <h2>Pourquoi refaire sa toiture ?</h2>
    <p>Une toiture en tuiles dure en moyenne 30 à 50 ans, parfois davantage pour l'ardoise ou le zinc. Passé ce cap, les matériaux deviennent poreux, les liteaux se fragilisent et les réparations successives ne suffisent plus. Remplacer la couverture, c'est :</p>
    <ul class="checks">
      <li><strong>Protéger durablement</strong> la maison et sa charpente pour plusieurs décennies</li>
      <li><strong>Mieux isoler</strong> : la toiture représente jusqu'à 30 % des pertes de chaleur d'une maison mal isolée</li>
      <li><strong>Valoriser votre bien</strong> : une toiture neuve est un argument fort à la revente</li>
      <li><strong>Changer d'aspect</strong> : nouvelle teinte, nouveau matériau, ajout de fenêtres de toit</li>
    </ul>

    <h2>Les signes qu'il est temps de remplacer votre toiture</h2>
    <ul class="checks">
      <li>Tuiles poreuses, effritées ou cassées sur de grandes surfaces</li>
      <li>Toiture qui ondule ou s'affaisse</li>
      <li>Absence d'écran sous-toiture sur une couverture ancienne</li>
      <li>Combles mal isolés et factures de chauffage élevées</li>
      <li>Toiture de plus de 30 ans qui n'a jamais été rénovée</li>
    </ul>
    <p>Si votre couverture est saine mais simplement encrassée, un <a href="/nettoyage-toiture/">nettoyage et démoussage</a> peut suffire : nous vous le dirons honnêtement lors de la visite.</p>

    <h2>Les étapes d'une réfection complète</h2>
    <ol class="steps">
      <li><strong>Visite, diagnostic et devis gratuit</strong><br>État de la couverture, de la charpente, de la zinguerie et de l'isolation.</li>
      <li><strong>Installation du chantier</strong><br>Échafaudage, protections, benne à gravats.</li>
      <li><strong>Dépose de l'ancienne couverture</strong><br>Tuiles, liteaux et éléments usés sont retirés et évacués.</li>
      <li><strong>Contrôle et renfort de la charpente</strong><br>Remplacement des bois abîmés, traitement si nécessaire (voir <a href="/charpente/">charpente</a>).</li>
      <li><strong>Isolation (option RGE)</strong><br>Isolation par l'extérieur (sarking) ou sous rampants.</li>
      <li><strong>Écran sous-toiture, liteaunage et couverture neuve</strong><br>Pose dans les règles de l'art (DTU), faîtages et rives.</li>
      <li><strong>Zinguerie neuve et réception</strong><br>Gouttières, descentes, noues et abergements (voir <a href="/zinguerie/">zinguerie</a>), nettoyage du chantier.</li>
    </ol>

    <h2>Quel matériau pour votre nouvelle toiture ?</h2>
    <p>Tuiles terre cuite plates ou mécaniques, ardoise naturelle ou synthétique, zinc, bac acier : nous vous conseillons selon le style de la maison, la pente et le PLU de votre commune. Découvrez le détail de chaque matériau sur notre page <a href="/couverture/">couverture</a>.</p>
  </article>
  {aside()}
</div></section>
"""
    html += faq_html(faq, "Questions fréquentes sur le remplacement de toiture")
    html += cta_band("Votre toiture a plus de 30 ans ?", "Faites-la diagnostiquer gratuitement par un couvreur certifié QUALIBAT et RGE.")
    html += footer()
    write("/renovation-toiture/", html)


def nettoyage():
    trail = [("/", "Accueil"), ("/nettoyage-toiture/", "Nettoyage de toiture")]
    faq = [
        ("À quelle fréquence faut-il nettoyer sa toiture ?",
         "En Île-de-France, un nettoyage avec traitement anti-mousse tous les 5 à 10 ans suffit généralement, davantage si la maison est entourée d'arbres ou si un versant est orienté au nord. Les gouttières, elles, se nettoient chaque année."),
        ("Le nettoyage haute pression abîme-t-il les tuiles ?",
         "Un jet trop puissant peut décaper la surface des tuiles en terre cuite et les rendre plus poreuses. Nous adaptons la méthode au matériau : brossage, pression modérée et produits adaptés, puis traitement."),
        ("Le démoussage suffit-il à prolonger la vie d'une toiture ?",
         "Sur une couverture saine, oui : un toit entretenu peut gagner de nombreuses années. Si les tuiles sont déjà poreuses, cassées ou si la toiture s'affaisse, un nettoyage ne suffira pas et nous vous conseillerons plutôt une rénovation."),
        ("Quelle est la meilleure période pour nettoyer son toit ?",
         "Le printemps et le début de l'automne sont idéaux : temps sec et températures douces permettent au traitement anti-mousse et à l'hydrofuge d'agir correctement."),
    ]
    desc = "Nettoyage de toiture, démoussage, traitement anti-mousse et hydrofuge, nettoyage des gouttières par des couvreurs professionnels."
    lds = [org_ld(), crumbs_ld(trail), service_ld("Nettoyage et démoussage de toiture", "/nettoyage-toiture/", desc), faq_ld(faq)]
    html = head("Nettoyage et démoussage de toiture en Île-de-France | JMC",
                "Nettoyage de toit, démoussage, traitement anti-mousse et hydrofuge à Courtry, Chelles, Villeparisis, Montfermeil… Par de vrais couvreurs, 40 ans d'expérience. Devis gratuit.",
                "/nettoyage-toiture/", lds)
    html += header("/nettoyage-toiture/")
    html += page_hero(trail, "Nettoyage de toiture", "Nettoyage et démoussage de toiture par des couvreurs professionnels",
                      "Mousses, lichens, traces noires : redonnez à votre toit son aspect d'origine et prolongez sa durée de vie, avec une entreprise de couverture qui sait aussi vérifier et remplacer les tuiles abîmées.")
    html += f"""
<section><div class="wrap split">
  <article class="prose">
    {photo("pavillon", eager=True)}
    <h2>Pourquoi faire nettoyer sa toiture ?</h2>
    <p>Les mousses et lichens retiennent l'humidité dans les tuiles. Avec le gel, l'eau fait éclater la terre cuite, les tuiles deviennent poreuses et la couverture vieillit prématurément. Un nettoyage régulier :</p>
    <ul class="checks">
      <li>prolonge la durée de vie de votre couverture ;</li>
      <li>évite que les débris bouchent les gouttières et les descentes ;</li>
      <li>redonne à la maison un aspect propre et soigné, un atout pour sa valeur.</li>
    </ul>

    <h2>Notre prestation de nettoyage de toit</h2>
    <ol class="steps">
      <li><strong>Inspection de la toiture</strong><br>Nous vérifions l'état des tuiles, des faîtages et de la zinguerie avant d'intervenir.</li>
      <li><strong>Démoussage</strong><br>Retrait des mousses par brossage et nettoyage à pression adaptée au matériau.</li>
      <li><strong>Remplacement des tuiles abîmées</strong><br>Les tuiles cassées ou poreuses repérées sont remplacées : c'est l'avantage de faire appel à un couvreur.</li>
      <li><strong>Traitement anti-mousse et hydrofuge</strong><br>Pour retarder la repousse et protéger les tuiles de l'humidité.</li>
      <li><strong>Nettoyage des gouttières</strong><br>Évacuation des débris, contrôle des descentes et des fixations.</li>
    </ol>

    <h2>Tous types de toitures</h2>
    <p>Tuiles mécaniques ou plates en terre cuite, tuiles béton, ardoises, toitures terrasses : chaque matériau demande une méthode et des produits spécifiques. Nos couvreurs les connaissent tous (voir nos <a href="/couverture/">types de couverture</a>).</p>

    <h2>Nettoyer ou remplacer ?</h2>
    <p>Un nettoyage est efficace sur une toiture saine. Si nous constatons que les tuiles sont trop dégradées, que la toiture s'affaisse ou qu'elle n'a pas d'écran sous-toiture, nous vous le dirons et vous proposerons un devis de <a href="/renovation-toiture/">rénovation de toiture</a>. Vous pourrez comparer les deux options en toute transparence.</p>
  </article>
  {aside()}
</div></section>
"""
    html += faq_html(faq, "Questions fréquentes sur le nettoyage de toiture")
    html += cta_band("Votre toit est envahi par la mousse ?", "Demandez un devis de nettoyage gratuit et sans engagement.")
    html += footer()
    write("/nettoyage-toiture/", html)


def maison_neuve():
    trail = [("/", "Accueil"), ("/toiture-maison-neuve/", "Toiture de maison neuve")]
    faq = [
        ("Je fais construire ma maison : puis-je choisir mon couvreur ?",
         "Oui si vous construisez avec un architecte, un maître d'œuvre ou en lots séparés : vous signez directement avec chaque entreprise. Avec un contrat de construction de maison individuelle (CCMI), c'est en principe le constructeur qui choisit ses sous-traitants, mais vous pouvez lui demander de travailler avec nous."),
        ("À quel moment du chantier intervenez-vous ?",
         "Dès que la maçonnerie est arasée et les murs prêts : nous posons la charpente, puis la couverture et la zinguerie pour mettre la maison hors d'eau, avant l'intervention des menuisiers et des plaquistes. Contactez-nous dès l'obtention du permis de construire pour réserver votre créneau."),
        ("Quels documents fournissez-vous pour mon assurance dommages-ouvrage ?",
         "Nous vous remettons notre attestation d'assurance décennale et de responsabilité civile en cours de validité, ainsi que nos qualifications QUALIBAT et RGE, avant le démarrage du chantier."),
        ("Pouvez-vous aussi réaliser l'isolation de la toiture ?",
         "Oui. Entreprise RGE, nous pouvons intégrer l'isolation de la toiture à votre construction, en cohérence avec les exigences de la réglementation environnementale RE2020 définies par votre bureau d'études thermiques."),
        ("Travaillez-vous aussi sur les extensions et surélévations ?",
         "Oui, nous réalisons la charpente, la couverture et la zinguerie des extensions, surélévations et aménagements de combles, avec le même niveau d'exigence que pour une maison neuve."),
    ]
    desc = "Charpente, couverture et zinguerie de maisons neuves pour les particuliers qui font construire, avec le savoir-faire acquis sur les programmes des promoteurs immobiliers."
    lds = [org_ld(), crumbs_ld(trail), service_ld("Toiture de maison neuve", "/toiture-maison-neuve/", desc), faq_ld(faq)]
    html = head("Toiture de maison neuve en Île-de-France : charpente et couverture | JMC",
                "Vous faites construire ? JMC, couvreur des promoteurs immobiliers depuis 1985, réalise la charpente, la couverture et la zinguerie de votre maison neuve en Île-de-France. Devis gratuit.",
                "/toiture-maison-neuve/", lds)
    html += header("/toiture-maison-neuve/")
    html += page_hero(trail, "Maison neuve · Construction", "Toiture de maison neuve : l'expertise des promoteurs au service des particuliers",
                      "Depuis 1985, les grands promoteurs immobiliers nous confient la charpente et la couverture de leurs programmes neufs. Vous faites construire votre maison ? Profitez du même savoir-faire, en direct.")
    html += f"""
<section><div class="wrap split">
  <article class="prose">
    {photo("depot", eager=True)}
    <h2>Le savoir-faire de la promotion immobilière, pour votre maison</h2>
    <p>Bouygues Immobilier, Kaufman &amp; Broad, Nexity : la société JMC travaille depuis des années pour des promoteurs et des architectes sur des programmes de logements neufs en Île-de-France. Ces chantiers exigent une rigueur particulière : respect strict des plannings, conformité aux normes, contrôles de bureaux de contrôle, finitions irréprochables.</p>
    <p>C'est cette même organisation que nous mettons au service des <strong>particuliers qui font construire leur maison</strong>. Vous bénéficiez d'une entreprise structurée, équipée et assurée, avec l'écoute et la souplesse d'une entreprise familiale.</p>

    <h2>Ce que nous réalisons sur votre maison neuve</h2>
    <ul class="checks">
      <li><strong>Charpente</strong> traditionnelle ou industrielle (fermettes), adaptée à vos plans et à l'usage des combles (voir <a href="/charpente/">charpente</a>)</li>
      <li><strong>Couverture</strong> en tuiles, ardoise, zinc ou bac acier, selon le PLU et le style de la maison (voir <a href="/couverture/">couverture</a>)</li>
      <li><strong>Zinguerie</strong> : gouttières, descentes, noues, abergements, habillages (voir <a href="/zinguerie/">zinguerie</a>)</li>
      <li><strong>Fenêtres de toit</strong> et lucarnes</li>
      <li><strong>Isolation de toiture</strong> par une entreprise RGE, en cohérence avec la RE2020</li>
      <li><strong>Mise hors d'eau</strong> rapide pour ne pas retarder les autres corps de métier</li>
    </ul>

    <h2>Pourquoi nous confier la toiture de votre construction</h2>
    <ul class="checks">
      <li><strong>Une seule entreprise</strong> pour la charpente, la couverture et la zinguerie : moins d'interfaces, moins de risques</li>
      <li><strong>Des délais tenus</strong> : nos équipes et notre flotte de véhicules sont dimensionnées pour les plannings exigeants de la promotion immobilière</li>
      <li><strong>Une coordination facilitée</strong> avec votre architecte, votre maçon et votre menuisier</li>
      <li><strong>Des garanties solides</strong> : assurance décennale, QUALIBAT et RGE, attestations fournies pour votre dommages-ouvrage</li>
      <li><strong>40 ans d'expérience</strong> et plus de 1 500 chantiers réalisés</li>
    </ul>

    <h2>Comment ça se passe ?</h2>
    <ol class="steps">
      <li><strong>Envoyez-nous vos plans</strong><br>Plans du permis de construire, coupes et notice descriptive suffisent pour un premier chiffrage.</li>
      <li><strong>Étude et devis gratuit</strong><br>Choix du type de charpente, du matériau de couverture et des options, devis détaillé.</li>
      <li><strong>Planification</strong><br>Nous calons notre intervention avec votre maçon pour enchaîner sans temps mort.</li>
      <li><strong>Pose et mise hors d'eau</strong><br>Charpente, couverture et zinguerie, puis réception des travaux.</li>
    </ol>
    <p>Également pour vos <strong>extensions, surélévations et aménagements de combles</strong>. Découvrez nos <a href="/nos-references/">références</a>.</p>
  </article>
  {aside("Vous faites construire ?")}
</div></section>
"""
    html += faq_html(faq, "Questions fréquentes sur la toiture d'une maison neuve")
    html += cta_band("Vous avez obtenu votre permis de construire ?", "Envoyez-nous vos plans : étude et devis gratuits pour la toiture de votre maison.")
    html += footer()
    write("/toiture-maison-neuve/", html)


REFS = [
    ("Charpente", "Rue de la Croix-Nivert", "Paris 15e", "Travaux de charpente sur immeuble parisien."),
    ("Charpente", "Nexity – rue Raffet", "Paris 16e", "Charpente pour un programme immobilier Nexity."),
    ("Charpente", "Provini", "Maisons-Alfort", "Reprise de charpente sur une maison individuelle."),
    ("Couverture", "École rue de Courtais", "Montfermeil", "Travaux de toiture d'un établissement scolaire."),
    ("Couverture", "École Jules Ferry", "Île-de-France", "Rénovation de la toiture d'une école."),
    ("Couverture", "École Saint-Charles", "Île-de-France", "Couverture du collège."),
    ("Zinguerie", "Boulevard de Sébastopol", "Paris", "Réfection de balcons en plomb sur immeuble haussmannien."),
]


def references():
    trail = [("/", "Accueil"), ("/nos-references/", "Nos références")]
    lds = [org_ld(), crumbs_ld(trail)]
    html = head("Nos références : chantiers de toiture en Île-de-France | JMC",
                "Découvrez les chantiers de JMC : charpente à Paris et Maisons-Alfort, toitures d'écoles à Montfermeil, zinguerie boulevard de Sébastopol. Avis clients et partenaires.",
                "/nos-references/", lds)
    html += header("/nos-references/")
    html += page_hero(trail, "Références", "Nos références : 1 500 chantiers de toiture en Île-de-France",
                      "Particuliers, collectivités, promoteurs et architectes nous font confiance pour leurs travaux de couverture, de charpente et de zinguerie, dans le respect des normes en vigueur.")
    cards = "".join(
        f'<article class="ref"><div class="thumb">{ICON["roof" if t == "Couverture" else "beam" if t == "Charpente" else "drop"]}</div>'
        f'<div class="body"><span class="tag">{t} · {c}</span><h3>{n}</h3><p>{d}</p></div></article>'
        for t, n, c, d in REFS)
    gallery = "".join(
        f'<article class="ref"><div class="thumb"><img src="{photo_src(k)}" alt="{PHOTOS[k][1]}" loading="lazy" width="800" height="500"></div>'
        f'<div class="body"><span class="tag">Réalisation</span><h3>{PHOTOS[k][2]}</h3></div></article>'
        for k in ("pavillon", "mansarde", "meuliere") if photo_src(k))
    gallery = (f'<section class="section-alt"><div class="wrap"><div class="section-head"><h2>Nos réalisations en images</h2>'
               f'<p>Quelques toitures réalisées par nos équipes.</p></div><div class="refs">{gallery}</div></div></section>') if gallery else ""
    clients = ["Bouygues Immobilier", "Kaufman &amp; Broad", "Nexity", "Archicrea", "Ville de Montfermeil",
               "Ville de Nogent-sur-Marne", "Ville de Villemomble", "Maison Fochia", "Archi Noisy"]
    html += f"""
<section><div class="wrap">
  <div class="section-head"><h2>Quelques chantiers récents</h2>
  <p>Logements, immeubles parisiens, établissements scolaires : un aperçu de nos réalisations.</p></div>
  <div class="refs">{cards}</div>
</div></section>
{gallery}
<section><div class="wrap">
  <div class="section-head"><h2>Ils nous font confiance</h2>
  <p>Promoteurs, architectes et collectivités de l'est parisien.</p></div>
  <ul class="clients">{"".join(f"<li>{c}</li>" for c in clients)}</ul>
</div></section>
<section class="section-alt"><div class="wrap">
  <div class="section-head"><h2>Avis de nos clients</h2></div>
  <div class="grid g3">{reviews_html(len(REVIEWS))}</div>
  <p style="margin-top:24px"><a class="btn btn-dark" href="{BIZ['gbp']}" target="_blank" rel="noopener">Lire et laisser un avis sur Google</a></p>
</div></section>
"""
    html += cta_band("Votre chantier sera notre prochaine référence")
    html += footer()
    write("/nos-references/", html)


def zones():
    trail = [("/", "Accueil"), ("/zones-intervention/", "Zones d'intervention")]
    lds = [org_ld(), crumbs_ld(trail)]
    groups = [
        ("Seine-et-Marne (77)", ["Courtry", "Chelles", "Le Pin", "Villeparisis", "Brou-sur-Chantereine",
                                 "Vaires-sur-Marne", "Claye-Souilly", "Mitry-Mory", "Torcy",
                                 "Lagny-sur-Marne", "Pontault-Combault", "Annet-sur-Marne"]),
        ("Seine-Saint-Denis (93)", ["Vaujours", "Coubron", "Montfermeil", "Clichy-sous-Bois", "Livry-Gargan",
                                    "Sevran", "Le Raincy", "Villemomble", "Gagny", "Neuilly-sur-Marne",
                                    "Noisy-le-Grand", "Noisy-le-Sec", "Aulnay-sous-Bois", "Tremblay-en-France"]),
        ("Paris (75)", ["Tous les arrondissements"]),
        ("Val-de-Marne (94)", ["Nogent-sur-Marne", "Le Perreux-sur-Marne", "Fontenay-sous-Bois", "Maisons-Alfort",
                               "Vincennes", "Saint-Maur-des-Fossés", "Créteil", "Champigny-sur-Marne"]),
        ("Hauts-de-Seine (92)", ["Neuilly-sur-Seine", "Boulogne-Billancourt", "Rueil-Malmaison", "Nanterre",
                                 "Courbevoie", "Antony", "Sceaux", "Colombes"]),
        ("Val-d'Oise (95)", ["Cergy", "Argenteuil", "Enghien-les-Bains", "Montmorency", "Roissy-en-France",
                             "Sarcelles", "Pontoise", "L'Isle-Adam"]),
        ("Yvelines (78)", ["Versailles", "Saint-Germain-en-Laye", "Le Vésinet", "Maisons-Laffitte",
                           "Rambouillet", "Poissy", "Le Chesnay-Rocquencourt", "Chatou"]),
        ("Essonne (91)", ["Évry-Courcouronnes", "Massy", "Palaiseau", "Corbeil-Essonnes",
                          "Brunoy", "Yerres", "Savigny-sur-Orge", "Étampes"]),
    ]
    blocks = "".join(
        f'<div class="card"><h3>{g}</h3><ul class="cities" style="columns:2 140px">'
        + "".join(f"<li>{c}</li>" for c in cs) + "</ul></div>" for g, cs in groups)
    html = head("Couvreur en Île-de-France : Paris, 77, 78, 91, 92, 93, 94, 95 | JMC",
                "JMC, couvreur basé à Courtry (77), intervient dans toute l'Île-de-France : Paris, Seine-et-Marne, Yvelines, Essonne, Hauts-de-Seine, Seine-Saint-Denis, Val-de-Marne, Val-d'Oise.",
                "/zones-intervention/", lds)
    html += header("/zones-intervention/")
    html += page_hero(trail, "Zones d'intervention", "Couvreur dans toute l'Île-de-France",
                      "Depuis notre siège de Courtry (77), nos équipes et notre flotte de véhicules interviennent à Paris et dans les huit départements franciliens, pour les particuliers comme pour les professionnels.")
    html += f"""
<section><div class="wrap">
  <div class="grid g3">{blocks}</div>
  <div class="prose" style="margin-top:48px">
    <h2>Un couvreur francilien depuis 1985</h2>
    <p>Travailler en Île-de-France depuis 40 ans, c'est connaître les maisons du secteur : pavillons en meulière et tuiles mécaniques de Chelles et du Raincy, maisons de ville de Gagny et Villemomble, résidences récentes de Villeparisis et Claye-Souilly, immeubles en zinc de Paris et de la petite couronne. C'est aussi pouvoir suivre de près chaque <a href="/renovation-toiture/">rénovation de toiture</a> et chaque <a href="/nettoyage-toiture/">nettoyage de toit</a>.</p>
    <p>Votre commune n'apparaît pas dans la liste ? Pas d'inquiétude : ces villes ne sont que des exemples, <a href="/contact/">contactez-nous</a>, nous intervenons partout en Île-de-France pour vos chantiers de <a href="/couverture/">couverture</a>, de <a href="/charpente/">charpente</a> et de <a href="/zinguerie/">zinguerie</a>.</p>
  </div>
</div></section>
<section class="section-alt" style="padding:0"><iframe class="map" style="border-radius:0;height:380px" title="Localisation de JMC Couverture à Courtry"
  loading="lazy" referrerpolicy="no-referrer-when-downgrade"
  src="https://www.google.com/maps?q=97+rue+Charles+Van+Wyngene+77181+Courtry&amp;output=embed"></iframe></section>
"""
    html += cta_band()
    html += footer()
    write("/zones-intervention/", html)


def contact():
    trail = [("/", "Accueil"), ("/contact/", "Contact")]
    contact_ld = {"@context": "https://schema.org", "@type": "ContactPage", "url": SITE + "/contact/",
                  "about": {"@id": SITE + "/#entreprise"}}
    lds = [org_ld(), crumbs_ld(trail), contact_ld]
    html = head("Contact et devis toiture gratuit à Courtry (77) | JMC Couverture",
                "Demandez votre devis gratuit pour vos travaux de couverture, charpente ou zinguerie. JMC, 97 rue Charles Van Wyngene, 77181 Courtry. ☎ 01 64 21 38 37.",
                "/contact/", lds)
    html += header("/contact/")
    html += page_hero(trail, "Contact", "Demandez votre devis de toiture gratuit",
                      "Décrivez votre projet en quelques lignes : nous vous recontactons rapidement pour organiser une visite et établir un devis détaillé, gratuit et sans engagement.", cta=False)
    html += f"""
<section><div class="wrap split">
  <div>
    <h2>Formulaire de demande de devis</h2>
    <form class="quote" name="devis" method="POST" action="/merci/" data-netlify="true" netlify-honeypot="societe-web">
      <input type="hidden" name="form-name" value="devis">
      <p class="skip"><label>Ne pas remplir : <input name="societe-web"></label></p>
      <div class="form-row">
        <label>Nom et prénom *<input name="nom" autocomplete="name" required></label>
        <label>Téléphone *<input name="telephone" type="tel" autocomplete="tel" required></label>
      </div>
      <div class="form-row">
        <label>E-mail<input name="email" type="email" autocomplete="email"></label>
        <label>Ville du chantier *<input name="ville" autocomplete="address-level2" required></label>
      </div>
      <label>Type de travaux
        <select name="travaux">
          <option>Remplacement / rénovation de toiture</option>
          <option>Nettoyage / démoussage de toiture</option>
          <option>Toiture de maison neuve / extension</option>
          <option>Charpente</option>
          <option>Zinguerie / gouttières</option>
          <option>Isolation de toiture</option>
          <option>Autre</option>
        </select></label>
      <label>Votre projet *<textarea name="message" rows="6" required placeholder="Surface approximative, matériau actuel, problème constaté…"></textarea></label>
      <label style="display:flex;gap:10px;align-items:flex-start;font-weight:400"><input type="checkbox" name="rgpd" required style="width:auto;margin-top:5px">
        J'accepte que mes données soient utilisées pour être recontacté au sujet de ma demande (voir <a href="/mentions-legales/">mentions légales</a>).</label>
      <button class="btn btn-primary" type="submit" style="justify-self:start">Envoyer ma demande</button>
      <p class="small">* Champs obligatoires. Réponse rapide, du lundi au samedi.</p>
    </form>
  </div>
  <aside class="aside">
    <h2>Nos coordonnées</h2>
    <p><strong>{BIZ['legal']} – {BIZ['name']}</strong><br>{BIZ['street']}<br>{BIZ['zip']} {BIZ['city']}</p>
    <p>Téléphone : <a href="tel:{BIZ['phone_intl']}"><strong>{BIZ['phone']}</strong></a><br>
    E-mail : <a href="mailto:{BIZ['email']}">{BIZ['email']}</a></p>
    <p><strong>Devis gratuit et sans engagement</strong> · <a href="{BIZ['gbp']}" target="_blank" rel="noopener">Fiche Google</a>{insta_link(" · ")}</p>
    {photo("depot")}
    <iframe class="map" title="Plan d'accès JMC Couverture, Courtry" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
      src="https://www.google.com/maps?q=97+rue+Charles+Van+Wyngene+77181+Courtry&amp;output=embed"></iframe>
  </aside>
</div></section>
"""
    html += footer()
    write("/contact/", html)


def merci():
    html = head("Demande envoyée | JMC Couverture", "Votre demande de devis a bien été envoyée.", "/merci/",
                [], robots="noindex,follow")
    html += header("/merci/")
    html += page_hero([("/", "Accueil"), ("/merci/", "Merci")], "Merci", "Votre demande a bien été envoyée",
                      "Nous vous recontactons très rapidement pour organiser la visite de votre toiture.")
    html += footer()
    write("/merci/", html)


def mentions():
    trail = [("/", "Accueil"), ("/mentions-legales/", "Mentions légales")]
    html = head("Mentions légales | JMC Couverture", "Mentions légales et politique de confidentialité du site jmccouverture.com.",
                "/mentions-legales/", [crumbs_ld(trail)], robots="noindex,follow")
    html += header("/mentions-legales/")
    html += page_hero(trail, "Informations", "Mentions légales", "Informations légales et protection des données personnelles.", cta=False)
    html += f"""
<section><div class="wrap prose">
  <h2>Éditeur du site</h2>
  <p>{BIZ['legal']}<br>{BIZ['street']}, {BIZ['zip']} {BIZ['city']}<br>Téléphone : {BIZ['phone']} – E-mail : {BIZ['email']}<br>
  SIRET : <em>[à compléter]</em> – RCS : <em>[à compléter]</em> – Directeur de la publication : <em>[à compléter]</em></p>
  <p>Assurance décennale : <em>[assureur et numéro de contrat à compléter]</em>, couverture géographique : France métropolitaine.</p>
  <h2>Hébergement</h2>
  <p><em>[Nom, adresse et téléphone de l'hébergeur à compléter]</em></p>
  <h2>Données personnelles</h2>
  <p>Les informations transmises via le formulaire de contact sont utilisées uniquement pour répondre à votre demande de devis. Elles ne sont ni cédées ni vendues et sont conservées au maximum 3 ans après le dernier contact. Conformément au RGPD, vous disposez d'un droit d'accès, de rectification et de suppression en écrivant à {BIZ['email']}.</p>
  <h2>Cookies</h2>
  <p>Ce site n'utilise pas de cookies de mesure d'audience ou publicitaires. Les cartes intégrées (Google Maps) peuvent déposer des cookies tiers lors de leur affichage.</p>
</div></section>
"""
    html += footer()
    write("/mentions-legales/", html)


def notfound():
    html = head("Page introuvable | JMC Couverture", "Cette page n'existe pas ou a été déplacée.", "/404.html", [], robots="noindex")
    html += header("")
    html += page_hero([("/", "Accueil"), ("/404.html", "Page introuvable")], "Erreur 404", "Cette page est introuvable",
                      "Elle a peut-être été déplacée. Retrouvez nos services de couverture, charpente et zinguerie depuis le menu.")
    html += footer()
    write("/404.html", html)


SITEMAP = [("/", "1.0"), ("/couverture/", "0.9"), ("/charpente/", "0.9"), ("/zinguerie/", "0.9"),
           ("/renovation-toiture/", "0.95"), ("/nettoyage-toiture/", "0.95"), ("/toiture-maison-neuve/", "0.9"), ("/zones-intervention/", "0.7"), ("/nos-references/", "0.7"),
           ("/contact/", "0.8")]


def seo_files():
    urls = "\n".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod><priority>{p}</priority></url>"
                     for u, p in SITEMAP)
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n',
        encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /merci/\n\nSitemap: {SITE}/sitemap.xml\n",
                                     encoding="utf-8")
    print("écrit sitemap.xml, robots.txt")


if __name__ == "__main__":
    for fn in (home, couverture, charpente, zinguerie, renovation, nettoyage, maison_neuve, references, zones, contact, merci, mentions, notfound):
        fn()
    seo_files()
