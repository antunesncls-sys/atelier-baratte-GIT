#!/usr/bin/env python3
"""Génère le site statique JMC Couverture.

Usage : python3 _build/build.py   (depuis le dossier jmc-couverture/)

Les pages gardent les URL de l'ancien site (/charpente/, /couverture/, ...)
pour conserver le référencement acquis. Chaque page sort dans <slug>/index.html.
"""
import json
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
}

CITIES = [
    "Courtry", "Chelles", "Le Pin", "Villeparisis", "Vaujours", "Coubron",
    "Montfermeil", "Clichy-sous-Bois", "Livry-Gargan", "Sevran", "Brou-sur-Chantereine",
    "Vaires-sur-Marne", "Claye-Souilly", "Mitry-Mory", "Le Raincy", "Villemomble",
    "Gagny", "Neuilly-sur-Marne", "Noisy-le-Grand", "Noisy-le-Sec", "Torcy",
    "Lagny-sur-Marne", "Pontault-Combault", "Nogent-sur-Marne", "Maisons-Alfort", "Paris",
]

NAV = [
    ("/", "Accueil"),
    ("/couverture/", "Couverture"),
    ("/charpente/", "Charpente"),
    ("/zinguerie/", "Zinguerie"),
    ("/nos-references/", "Références"),
    ("/zones-intervention/", "Zones"),
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
    return (f'<figure class="photo"><img src="{src}" alt="{alt}" {load} decoding="async" width="1200" height="800">'
            f'<figcaption>{cap}</figcaption></figure>')


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
        "sameAs": [BIZ["gbp"]],
        "hasMap": BIZ["gbp"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": BIZ["street"],
            "postalCode": BIZ["zip"],
            "addressLocality": BIZ["city"],
            "addressRegion": "Île-de-France",
            "addressCountry": "FR",
        },
        "areaServed": [{"@type": "City", "name": c} for c in CITIES]
        + [{"@type": "AdministrativeArea", "name": n} for n in
           ("Seine-et-Marne", "Seine-Saint-Denis", "Val-de-Marne", "Paris")],
        "knowsAbout": ["Couverture", "Charpente", "Zinguerie", "Rénovation de toiture",
                       "Recherche de fuite", "Gouttières", "Toiture zinc", "Ardoise", "Tuiles"],
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
                             ("Dépannage fuite de toiture", "/urgence-fuite-toiture/"))
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
            "areaServed": [{"@type": "AdministrativeArea", "name": n} for n in
                           ("Seine-et-Marne", "Seine-Saint-Denis", "Val-de-Marne", "Paris")]}


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
  <span>Couvreur certifié QUALIBAT &amp; RGE · Seine-et-Marne, Seine-Saint-Denis, Paris</span>
  <span>Urgence 7j/7 : <a href="tel:{BIZ['phone_intl']}"><strong>{BIZ['phone']}</strong></a></span>
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
    <li>Intervention d'urgence 7j/7</li>
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
      <p style="margin-top:16px">Entreprise de couverture, charpente et zinguerie à Courtry (77). Depuis 1985, 40 ans d'expérience au service des particuliers, des collectivités et des professionnels en Île-de-France.</p>
    </div>
    <div><h2>Nos métiers</h2><ul>
      <li><a href="/couverture/">Couverture &amp; rénovation de toiture</a></li>
      <li><a href="/charpente/">Charpente</a></li>
      <li><a href="/zinguerie/">Zinguerie &amp; gouttières</a></li>
      <li><a href="/urgence-fuite-toiture/">Urgence fuite de toiture</a></li>
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
      <a href="{BIZ['gbp']}" target="_blank" rel="noopener">Notre fiche Google</a></p>
    </div>
  </div>
  <p class="small" style="margin-top:28px;color:#8c98a4">Couvreur à {city_links} et dans toute la Seine-et-Marne et la Seine-Saint-Denis.</p>
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
         "Notre entreprise est basée à Courtry (77181). Nous intervenons dans un rayon d'environ 30 km : Seine-et-Marne (Chelles, Le Pin, Villeparisis, Claye-Souilly…), Seine-Saint-Denis (Montfermeil, Livry-Gargan, Villemomble, Gagny…), Val-de-Marne et Paris."),
        ("Le devis est-il gratuit ?",
         "Oui. Nous nous déplaçons pour diagnostiquer votre toiture et nous vous remettons un devis détaillé, gratuit et sans engagement."),
        ("Intervenez-vous en urgence ?",
         "Oui, nous assurons des interventions d'urgence 7j/7 en cas de fuite, de tuiles arrachées après une tempête ou de dégât des eaux venant de la toiture : bâchage, mise hors d'eau puis réparation durable."),
        ("Vos travaux sont-ils garantis ?",
         "Tous nos travaux sont couverts par notre garantie décennale et notre assurance responsabilité civile professionnelle. Nous sommes également certifiés QUALIBAT et RGE."),
        ("Pourquoi faire appel à un couvreur RGE ?",
         "Le label RGE (Reconnu Garant de l'Environnement) est exigé pour que vos travaux d'isolation de toiture puissent bénéficier des aides publiques à la rénovation énergétique, sous réserve des conditions d'éligibilité en vigueur."),
    ]
    lds = [org_ld(), website_ld(), faq_ld(faq)]
    html = head("Couvreur à Courtry (77) – Couverture, Charpente, Zinguerie | JMC",
                "Couvreur charpentier zingueur à Courtry (77) depuis 1985 : rénovation de toiture, fuite, gouttières. QUALIBAT & RGE. Devis gratuit ☎ 01 64 21 38 37.",
                "/", lds)
    html += header("/")
    html += f"""
<section class="hero"{hero_style("meuliere")}>{HERO_ART}<div class="wrap">
  <div>
    <span class="eyebrow">40 ans · 1985–2025 · Couvreur charpentier zingueur</span>
    <h1>Votre couvreur à Courtry et en Île-de-France depuis 1985</h1>
    <p class="lead">Réfection de toiture, réparation de fuite, charpente et zinguerie : la société JMC réalise tous vos travaux de toiture en Seine-et-Marne, en Seine-Saint-Denis et à Paris, pour les particuliers comme pour les professionnels.</p>
    <div class="hero-cta"><a class="btn btn-primary" href="/contact/">Demander un devis gratuit</a>
    <a class="btn btn-ghost" href="tel:{BIZ['phone_intl']}">Appeler le {BIZ['phone']}</a></div>
    <ul class="badges"><li>QUALIBAT</li><li>RGE</li><li>Garantie décennale</li><li>Urgence 7j/7</li></ul>
  </div>
  <div class="hero-card">
    <h2>Fuite, tuiles envolées, gouttière bouchée ?</h2>
    <p>Nos couvreurs interviennent rapidement pour mettre votre maison hors d'eau, puis réparer durablement.</p>
    <ul class="checks"><li>Diagnostic sur place</li><li>Bâchage d'urgence</li><li>Devis gratuit et détaillé</li></ul>
    <a class="btn btn-dark" href="/urgence-fuite-toiture/">Urgence toiture</a>
  </div>
</div></section>

<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">Nos métiers</span>
  <h2>Couverture, charpente et zinguerie : un seul interlocuteur pour votre toit</h2>
  <p>Une toiture saine repose sur trois savoir-faire complémentaires. Nos équipes les maîtrisent tous, ce qui vous garantit un chantier coordonné, des délais tenus et une seule garantie.</p></div>
  <div class="grid g3">
  {service_card("roof", "Couverture", "/couverture/", "Pose, rénovation et réparation de toiture, quel que soit le matériau.",
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
    <div><strong>7j/7</strong><span>intervention d'urgence</span></div>
  </div>
</div></section>

<section><div class="wrap split">
  <div class="prose">
    {photo("depot")}
    <span class="eyebrow">L'entreprise</span>
    <h2>Une entreprise de toiture familière des maisons d'Île-de-France</h2>
    <p>Installée au <strong>{BIZ['street']} à {BIZ['city']}</strong>, la société JMC accompagne depuis 1985 les propriétaires, syndics, collectivités et promoteurs de l'est parisien. Pavillons en tuiles de Chelles ou du Pin, immeubles en zinc à Paris, écoles et bâtiments publics de Seine-Saint-Denis : nous connaissons les matériaux, les règles d'urbanisme et les contraintes de chaque type de bâti.</p>
    <p>Notre approche est simple : <strong>confier vos travaux à des professionnels</strong>. Chaque chantier commence par un diagnostic honnête de votre toiture. Nous vous expliquons ce qui doit être fait tout de suite, ce qui peut attendre, et nous vous remettons un devis clair, poste par poste.</p>
    <h3>Nos engagements</h3>
    <ul class="checks">
      <li><strong>Qualité certifiée</strong> : qualification QUALIBAT et label RGE.</li>
      <li><strong>Sécurité</strong> : garantie décennale et responsabilité civile professionnelle.</li>
      <li><strong>Réactivité</strong> : intervention d'urgence 7 jours sur 7.</li>
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
  <h2>Couvreur en Seine-et-Marne, Seine-Saint-Denis et Paris</h2>
  <p>Depuis Courtry, nous intervenons rapidement dans tout l'est de l'Île-de-France.</p></div>
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
    html = head("Couvreur Seine-et-Marne : rénovation de toiture | JMC",
                "Couvreur à Courtry (77) : réfection de toiture, tuiles, ardoise, zinc, bac acier, toit-terrasse EPDM. Entreprise QUALIBAT & RGE, garantie décennale. Devis gratuit.",
                "/couverture/", lds)
    html += header("/couverture/")
    html += page_hero(trail, "Couverture", "Couvreur en Seine-et-Marne : rénovation et réparation de toiture",
                      "Pose neuve, réfection complète ou simple réparation : nos couvreurs travaillent tous les matériaux de couverture, dans le respect des DTU et des règles d'urbanisme locales.")
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
      <li>Recherche et réparation de fuites</li>
      <li>Reprise de faîtage, d'arêtiers et de rives</li>
      <li>Pose de fenêtres de toit et de lucarnes</li>
      <li>Isolation de toiture par l'extérieur (entreprise RGE)</li>
      <li>Nettoyage, démoussage et traitement hydrofuge</li>
    </ul>
    <p>Une fuite ? Consultez notre page <a href="/urgence-fuite-toiture/">urgence fuite de toiture</a>. Vos gouttières débordent ? Découvrez nos travaux de <a href="/zinguerie/">zinguerie</a>. Votre toiture s'affaisse ? Il faut sans doute reprendre la <a href="/charpente/">charpente</a>.</p>
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


def urgence():
    trail = [("/", "Accueil"), ("/urgence-fuite-toiture/", "Urgence fuite de toiture")]
    faq = [
        ("Que faire en attendant le couvreur en cas de fuite ?",
         "Coupez l'électricité dans la zone touchée si l'eau approche d'installations électriques, placez des récipients sous les gouttes, protégez vos meubles et prenez des photos pour votre assurance. Ne montez jamais sur un toit mouillé."),
        ("Mon assurance prend-elle en charge la fuite ?",
         "Les dommages causés par une tempête, la grêle ou la neige sont en général couverts par l'assurance habitation, selon votre contrat. Déclarez le sinistre rapidement ; nous vous fournissons un devis et un rapport d'intervention pour votre dossier."),
        ("Intervenez-vous le week-end ?",
         "Oui, nous assurons les urgences 7 jours sur 7 pour mettre votre toiture hors d'eau."),
    ]
    desc = "Intervention d'urgence 7j/7 en cas de fuite de toiture, de tuiles arrachées ou de dégâts après tempête : bâchage, mise hors d'eau et réparation."
    lds = [org_ld(), crumbs_ld(trail), service_ld("Dépannage fuite de toiture", "/urgence-fuite-toiture/", desc), faq_ld(faq)]
    html = head("Fuite de toiture : couvreur en urgence 7j/7 (77, 93) | JMC",
                "Fuite de toit, tuiles arrachées, dégâts de tempête ? Couvreur d'urgence 7j/7 à Courtry, Chelles, Montfermeil et alentours : bâchage et réparation. ☎ 01 64 21 38 37.",
                "/urgence-fuite-toiture/", lds)
    html += header("/urgence-fuite-toiture/")
    html += page_hero(trail, "Urgence 7j/7", "Fuite de toiture : un couvreur en urgence, 7 jours sur 7",
                      f"Infiltration, tuiles envolées après un coup de vent, gouttière arrachée : appelez le <a href=\"tel:{BIZ['phone_intl']}\" style=\"color:#fff\"><strong>{BIZ['phone']}</strong></a>. Nous mettons votre toiture hors d'eau puis réparons durablement.")
    html += f"""
<section><div class="wrap split">
  <article class="prose">
    <h2>Notre intervention d'urgence en 3 étapes</h2>
    <ol class="steps">
      <li><strong>Mise en sécurité et hors d'eau</strong><br>Bâchage de la toiture, remplacement provisoire des tuiles manquantes, sécurisation des éléments menaçant de tomber.</li>
      <li><strong>Recherche de fuite</strong><br>Inspection de la couverture, des noues, des faîtages, des abergements de cheminée et de la zinguerie pour trouver l'origine réelle de l'infiltration.</li>
      <li><strong>Réparation durable et rapport</strong><br>Réparation définitive et devis détaillé, utilisable pour votre déclaration de sinistre auprès de votre assurance.</li>
    </ol>

    <h2>Les urgences toiture que nous traitons</h2>
    <ul class="checks">
      <li>Fuite de toit et infiltration d'eau au plafond</li>
      <li>Tuiles ou ardoises arrachées après une tempête</li>
      <li>Faîtage descellé, rive ou cheminée endommagée</li>
      <li>Gouttière arrachée ou chéneau qui déborde</li>
      <li>Fenêtre de toit qui fuit</li>
      <li>Chute d'arbre ou de branche sur la toiture</li>
    </ul>

    <h2>Où intervenons-nous en urgence ?</h2>
    <p>Depuis notre base de Courtry, nous rejoignons rapidement Chelles, Le Pin, Villeparisis, Vaujours, Coubron, Montfermeil, Clichy-sous-Bois, Livry-Gargan, Sevran, Le Raincy, Villemomble, Gagny et les communes voisines. Voir <a href="/zones-intervention/">toutes nos zones d'intervention</a>.</p>
  </article>
  {aside("Besoin d'aide maintenant ?")}
</div></section>
"""
    html += faq_html(faq, "Questions fréquentes en cas de fuite")
    html += cta_band("Une fuite en ce moment ?", "Appelez-nous directement, nous intervenons 7j/7.")
    html += footer()
    write("/urgence-fuite-toiture/", html)


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
        ("Val-de-Marne (94) et Paris (75)", ["Nogent-sur-Marne", "Le Perreux-sur-Marne", "Fontenay-sous-Bois",
                                             "Maisons-Alfort", "Vincennes", "Paris"]),
    ]
    blocks = "".join(
        f'<div class="card"><h3>{g}</h3><ul class="cities" style="columns:2 140px">'
        + "".join(f"<li>{c}</li>" for c in cs) + "</ul></div>" for g, cs in groups)
    html = head("Couvreur Chelles, Montfermeil, Villeparisis… | JMC Couverture",
                "JMC, couvreur basé à Courtry, intervient à Chelles, Le Pin, Villeparisis, Montfermeil, Livry-Gargan, Gagny, Villemomble et dans tout le 77, 93, 94 et Paris.",
                "/zones-intervention/", lds)
    html += header("/zones-intervention/")
    html += page_hero(trail, "Zones d'intervention", "Couvreur à Courtry et dans tout l'est de l'Île-de-France",
                      "Basée à Courtry, à la frontière de la Seine-et-Marne et de la Seine-Saint-Denis, notre entreprise intervient rapidement dans un rayon d'environ 30 km.")
    html += f"""
<section><div class="wrap">
  <div class="grid g3">{blocks}</div>
  <div class="prose" style="margin-top:48px">
    <h2>Un couvreur de proximité</h2>
    <p>Être implanté localement, c'est connaître les maisons du secteur : pavillons en meulière et tuiles mécaniques de Chelles et du Raincy, maisons de ville de Gagny et Villemomble, résidences récentes de Villeparisis et Claye-Souilly, immeubles en zinc de Paris et de la petite couronne. C'est aussi pouvoir intervenir vite en cas de <a href="/urgence-fuite-toiture/">fuite de toiture</a>.</p>
    <p>Votre commune n'apparaît pas dans la liste ? <a href="/contact/">Contactez-nous</a> : nous étudions toutes les demandes en Île-de-France, en particulier pour les chantiers de <a href="/couverture/">couverture</a>, de <a href="/charpente/">charpente</a> et de <a href="/zinguerie/">zinguerie</a> d'envergure.</p>
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
          <option>Réparation / fuite de toiture</option>
          <option>Réfection complète de toiture</option>
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
    <p><strong>Urgences toiture 7j/7</strong> · <a href="{BIZ['gbp']}" target="_blank" rel="noopener">Fiche Google</a></p>
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
                      "Nous vous recontactons très rapidement. Pour une urgence, appelez-nous directement.")
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
           ("/urgence-fuite-toiture/", "0.9"), ("/zones-intervention/", "0.7"), ("/nos-references/", "0.7"),
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
    for fn in (home, couverture, charpente, zinguerie, urgence, references, zones, contact, merci, mentions, notfound):
        fn()
    seo_files()
