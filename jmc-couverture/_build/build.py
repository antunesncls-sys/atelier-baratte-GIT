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
    "instagram": "https://www.instagram.com/jmc.couverture/",
    "facebook": "https://www.facebook.com/p/Jmccouverture-61562122535882/",
    "tiktok": "https://www.tiktok.com/@jmc.couverture",
    "rating": "4,9",
    "reviews_count": 29,
    "lat": 48.91026,
    "lng": 2.60351,
    # Lien qui ouvre directement les avis Google
    "reviews": "https://www.google.com/search?q=JMC+COUVERTURE&si=APenkKm7iecQ4G6P-TsbSMFKIQtv3EFIqRAFw-i8uEbk55Z-_z7JmPqeUzDTnHoL-AHEND9IN_pJEkKMpBT7mre-X88bywTgDYzOnAFZNhQvQbswAGrB0L0%3D&uds=AJ5uw18ugXvqDbJNSvbGMdx0hJ41f-qXCR4HVoYBDPpyUtSRzRQhwkfQHV7Yrf4TO3LhXsXsXmx4pMpHqnqoZqW14LzyjpwDXQvPJj37nIfjRU76yoYsoIg",
}

CITIES = [
    "Saint-Maur-des-Fossés", "Nogent-sur-Marne", "Le Perreux-sur-Marne", "Vincennes", "Saint-Mandé",
    "Bry-sur-Marne", "Joinville-le-Pont", "Le Raincy", "Lagny-sur-Marne", "Ozoir-la-Ferrière",
    "Bussy-Saint-Georges", "Gretz-Armainvilliers", "Lésigny", "Ferrières-en-Brie", "Serris",
    "Thorigny-sur-Marne", "Fontainebleau", "Courtry", "Chelles", "Le Pin", "Claye-Souilly",
    "Villemomble", "Gagny", "Paris",
]

FOOTER_CITIES = {"Saint-Maur-des-Fossés", "Nogent-sur-Marne", "Le Perreux-sur-Marne", "Versailles", "Neuilly-sur-Seine",
                 "Saint-Germain-en-Laye", "Le Vésinet", "Fontainebleau", "Lagny-sur-Marne"}

DEPTS = ("Paris", "Seine-et-Marne", "Yvelines", "Essonne", "Hauts-de-Seine", "Seine-Saint-Denis", "Val-de-Marne", "Val-d'Oise")

SAVOIR_FAIRE = [
    ("/chien-assis-lucarne/", "Chien-assis et lucarnes"),
    ("/toiture-mansardee-brisis-terrasson/", "Toiture mansardée"),
    ("/cheneau-noue-zinc/", "Chéneaux et noues en zinc"),
    ("/souche-cheminee-solin-abergement/", "Souche de cheminée"),
    ("/etancheite-toiture-terrasse/", "Étanchéité toiture terrasse"),
    ("/toiture-avant-panneaux-photovoltaiques/", "Toiture avant photovoltaïque"),
    ("/fenetre-de-toit-velux-lucarnes/", "Pose de VELUX"),
    ("/couverture-zinc-bardage/", "Zinc joint debout et bardage"),
]

NAV = [
    ("/renovation-toiture/", "Rénovation"),
    ("/isolation-toiture/", "Isolation"),
    ("/toiture-maison-neuve/", "Maison neuve"),
    ("/couverture-zinc-bardage/", "Zinc &amp; bardage"),
    ("/couvreur-copropriete-syndic/", "Copropriétés"),
    ("/nos-references/", "Réalisations"),
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
    "drone": ("toiture-ardoise-lucarnes-zinc-vue-drone-jmc",
              "Vue aérienne d'une toiture en ardoise avec trois lucarnes habillées de zinc, en finition sous échafaudage par JMC Couverture en Île-de-France",
              "Toiture en ardoise et lucarnes en zinc, chantier JMC vu du ciel."),
    "mansarde": ("toiture-mansardee-lucarnes-zinc-jmc",
                 "Maison bourgeoise rénovée en Île-de-France : toiture mansardée en ardoise et lucarnes en zinc réalisées par JMC Couverture",
                 "Maison bourgeoise : toiture mansardée en ardoise et lucarnes en zinc."),
    "meuliere": ("maison-meuliere-couverture-tuiles-jmc",
                 "Maison en pierre meulière avec couverture en tuiles terre cuite et zinguerie, panneau de chantier JMC Couverture devant la façade",
                 "Maison en meulière : réfection complète de la toiture en tuiles."),
    "pavillon": ("toiture-pavillon-renovation-jmc",
                 "Pavillon avec toiture rénovée en tuiles anthracite, VELUX et gouttières remplacés par JMC Couverture, panneau de chantier sur le portail",
                 "Rénovation de toiture avec remplacement des VELUX et des gouttières."),
    "depot": ("depot-flotte-vehicules-jmc-couverture",
              "Siège de l'entreprise JMC Couverture avec atelier et flotte de camionnettes d'intervention",
              "Notre siège, notre atelier et notre flotte de véhicules."),
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
    keys = [k for k in ("mansarde", "meuliere", "pavillon", "depot") if photo_src(k)]
    if not keys:
        return ""
    items = "".join(
        f'<figure><img src="{photo_src(k)}" alt="{PHOTOS[k][1]}" loading="lazy" decoding="async" '
        f'width="{photo_dims(photo_src(k))[0]}" height="{photo_dims(photo_src(k))[1]}"><figcaption>{PHOTOS[k][2]}</figcaption></figure>'
        for k in keys)
    return f'<div class="mosaic">{items}</div>'


FB_SVG = ('<svg class="ig" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="currentColor">'
          '<path d="M14 8h3V4h-3c-2.8 0-4.5 1.9-4.5 4.6V11H7v4h2.5v8h4v-8h3l.5-4h-3.5V8.8c0-.5.3-.8.5-.8z"/></svg>')
TT_SVG = ('<svg class="ig" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="currentColor">'
          '<path d="M16.6 3c.4 2.2 1.8 3.7 4 3.9v3.3a7.4 7.4 0 0 1-4-1.2v6.3A6.2 6.2 0 1 1 10.4 9v3.4a2.9 2.9 0 1 0 2.9 2.9V3h3.3z"/></svg>')


def socials():
    out = []
    for key, svg, label in (("instagram", INSTA_SVG, "Instagram"), ("facebook", FB_SVG, "Facebook"), ("tiktok", TT_SVG, "TikTok")):
        if BIZ.get(key):
            out.append(f'<a class="ig-link" href="{BIZ[key]}" target="_blank" rel="noopener" '
                       f'aria-label="{label} JMC Couverture">{svg}{label}</a>')
    return out


def insta_link(sep=""):
    links = socials()
    return f'{sep}<span class="socials">Suivez-nous : {" ".join(links)}</span>' if links else ""


def insta_top():
    links = socials()
    return f' · <span class="socials">{" ".join(links)}</span>' if links else ""


def hero_bg():
    src = photo_src("drone")
    if not src:
        return ""
    small = src.replace(".jpg", "-800.jpg")
    return (f'<img class="hero-bg" src="{src}" srcset="{small} 800w, {src} 1605w" sizes="100vw" '
            f'alt="{PHOTOS["drone"][1]}" fetchpriority="high" decoding="async" width="1605" height="857">')


INSTA_SVG = ('<svg class="ig" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="none" stroke="currentColor" '
             'stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/>'
             '<circle cx="17.5" cy="6.5" r="1.2" fill="currentColor" stroke="none"/></svg>')


def labels():
    return ('<div class="labels"><img src="/assets/logo-qualibat.svg" alt="Entreprise certifiée QUALIBAT" width="60" height="63">'
            '<img src="/assets/logo-rge.png" alt="Label RGE – Reconnu Garant de l\'Environnement" width="56" height="60"></div>')


def google_badge(light=False):
    cls = "gbadge light" if light else "gbadge"
    return (f'<a class="{cls}" href="{BIZ["reviews"]}" target="_blank" rel="noopener">'
            f'<span class="g">G</span><span class="stars">★★★★★</span>'
            f'<strong>{BIZ["rating"]}/5</strong><span>· {BIZ["reviews_count"]} avis Google</span></a>')


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
        "priceRange": "€€",
        "geo": {"@type": "GeoCoordinates", "latitude": BIZ["lat"], "longitude": BIZ["lng"]},
        "sameAs": [u for u in (BIZ["gbp"], BIZ["instagram"], BIZ["facebook"], BIZ["tiktok"]) if u],
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
        + [{"@type": "City", "name": c} for c in dict.fromkeys([v["name"] for v in VILLES] + CITIES)],
        "knowsAbout": ["Couverture", "Charpente", "Zinguerie", "Rénovation de toiture",
                       "Remplacement de toiture", "Nettoyage de toiture", "Démoussage", "Isolation de toiture", "Couverture zinc", "Bardage zinc", "Maison d'architecte", "Toiture maison neuve", "Isolation des combles", "Isolation des combles perdus", "Isolation des rampants", "Soufflage", "Fenêtre de toit", "VELUX", "Lucarnes", "Copropriété", "Promotion immobilière", "Chien-assis", "Toiture mansardée", "Chéneau", "Noue", "Souche de cheminée", "Étanchéité toiture terrasse", "EPDM", "Descentes d'eaux pluviales", "Photovoltaïque", "Gouttières", "Toiture zinc", "Ardoise", "Tuiles"],
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
                             ("Toiture de maison neuve", "/toiture-maison-neuve/"),
                             ("Isolation de toiture", "/isolation-toiture/"),
                             ("Couverture zinc et bardage", "/couverture-zinc-bardage/"),
                             ("Toiture et isolation pour copropriétés", "/couvreur-copropriete-syndic/"),
                             ("Fenêtres de toit VELUX et lucarnes", "/fenetre-de-toit-velux-lucarnes/"),
                             ("Couverture pour la promotion immobilière", "/couvreur-promotion-immobiliere/"),
                             ("Étanchéité de toiture terrasse", "/etancheite-toiture-terrasse/"),
                             ("Isolation des combles perdus", "/isolation-combles-perdus/"),
                             ("Isolation des rampants", "/isolation-rampants/"),
                             ("Toiture avant panneaux photovoltaïques", "/toiture-avant-panneaux-photovoltaiques/"))
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
<link rel="preload" href="/assets/fonts/archivo-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" as="image" href="/assets/photos/toiture-ardoise-lucarnes-zinc-vue-drone-jmc.jpg" imagesrcset="/assets/photos/toiture-ardoise-lucarnes-zinc-vue-drone-jmc-800.jpg 800w, /assets/photos/toiture-ardoise-lucarnes-zinc-vue-drone-jmc.jpg 1605w" imagesizes="100vw">
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
<section class="hero page-hero has-photo">{hero_bg()}<div class="wrap"><div>
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
  {labels()}
  <ul class="checks">
    <li>40 ans d'expérience (depuis 1985)</li>
    <li>Entreprise certifiée QUALIBAT et RGE</li>
    <li>Garantie décennale et responsabilité civile</li>
    <li>Plus de 1 500 chantiers réalisés</li>
    <li>Les équipes et la structure de la promotion immobilière</li>
    <li>Équipe SAV et qualité dédiée, en interne</li>
    <li>Équipes formées à la sécurité et à la propreté</li>
    <li>Démarches en mairie gérées pour vous</li>
    <li>Isolation RGE : aides possibles</li>
    <li>Devis gratuit et détaillé</li>
  </ul>
  {google_badge(light=True)}
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
      {labels()}
      <p style="margin-top:16px">Entreprise de couverture, charpente et zinguerie basée à Courtry (77), intervenant dans toute l'Île-de-France. Depuis 1985, 40 ans d'expérience au service des particuliers, des collectivités et des professionnels en Île-de-France.</p>
    </div>
    <div><h2>Nos spécialités</h2><ul>
      <li><a href="/renovation-toiture/">Rénovation &amp; remplacement de toiture</a></li>
      <li><a href="/isolation-toiture/">Isolation de toiture</a></li>
      <li><a href="/isolation-rampants/">Isolation des rampants</a> · <a href="/isolation-combles-perdus/">Combles perdus</a></li>
      <li><a href="/toiture-maison-neuve/">Toiture de maison neuve</a></li>
      <li><a href="/couverture-zinc-bardage/">Couverture zinc &amp; bardage</a></li>
      <li><a href="/couvreur-copropriete-syndic/">Copropriétés &amp; syndics</a></li>
      <li><a href="/couvreur-promotion-immobiliere/">Promotion immobilière</a></li>
      <li><a href="/fenetre-de-toit-velux-lucarnes/">Fenêtres de toit VELUX &amp; lucarnes</a></li>
      <li><a href="/nettoyage-toiture/">Nettoyage &amp; démoussage</a></li>
      <li><a href="/couverture/">Couverture</a> · <a href="/charpente/">Charpente</a> · <a href="/zinguerie/">Zinguerie</a></li>
    </ul><h2 style="margin-top:18px">Savoir-faire</h2><ul>
      {"".join(f'<li><a href="{u}">{n}</a></li>' for u, n in SAVOIR_FAIRE[:4])}
    </ul></div>
    <div><h2>Couvreur par ville</h2><ul>
      {"".join(f'<li><a href="/{v["slug"]}/">Couvreur {v["name"]}</a></li>' for v in VILLES if v["name"] in FOOTER_CITIES)}
      <li><a href="/zones-intervention/"><strong>Toutes nos villes →</strong></a></li>
    </ul><h2 style="margin-top:18px">Départements</h2><ul>
      {"".join(f'<li><a href="/{d["slug"]}/">Couvreur {d["num"]} {d["name"] if d["num"] != "75" else ""}</a></li>' for d in DEPTS_PAGES)}
    </ul></div>
    <div><h2>L'entreprise</h2><ul>
      <li><a href="/notre-methode-sav-qualite/">Notre méthode, SAV &amp; qualité</a></li>
      <li><a href="/nos-references/">Nos références</a></li>
      <li><a href="/zones-intervention/">Zones d'intervention</a></li>
      <li><a href="/contact/">Contact &amp; devis</a></li>
      <li><a href="/mentions-legales/">Mentions légales</a></li>
    </ul></div>
    <div><h2>Contact</h2>
      <address style="font-style:normal">{BIZ['legal']}<br>{BIZ['street']}<br>{BIZ['zip']} {BIZ['city']}</address>
      <p style="margin-top:10px"><a href="tel:{BIZ['phone_intl']}"><strong>{BIZ['phone']}</strong></a><br>
      <a href="mailto:{BIZ['email']}">{BIZ['email']}</a><br>
      <a href="{BIZ['reviews']}" target="_blank" rel="noopener">Nos avis Google</a>{insta_link("<br>")}</p>
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


GOOGLE_REVIEWS = {
    "lily": {"name": "Lily", "date": "février 2026", "travaux": "Réfection complète de toiture",
             "text": "Réfection complète de ma toiture par l'entreprise JMC à Courtry. Je suis plus que ravie du résultat ! Le devis est clair, détaillé et le tarif est compétitif. Les délais des travaux sont respectés avec une organisation sans faille impressionnante et ceux-ci sont réalisés dans les règles de l'art. Le gérant et les couvreurs qui sont intervenus sont charmants, ponctuels, rigoureux, professionnels et respectueux des lieux (le chantier est protégé et nettoyé chaque soir). Je recommande vivement cette société.",
             "short": "Le devis est clair, détaillé et le tarif est compétitif. Les délais sont respectés avec une organisation sans faille […] respectueux des lieux (le chantier est protégé et nettoyé chaque soir). Je recommande vivement cette société."},
    "richard": {"name": "Richard K.", "date": "juin 2026", "travaux": "Réfection de toiture, 3 VELUX et isolation",
                "text": "Réfection totale de la toiture avec remplacement de 3 velux et isolation. Équipe ponctuelle, agréable et serviable. Chantier toujours très propre à la fin de la journée. Merci pour ces travaux."},
    "larry": {"name": "Larry H.", "date": "mai 2026", "travaux": "Travaux de toiture",
              "text": "Travail très soigné, très professionnel et de surcroît très honnête sur les prix. Je recommande cette entreprise à 100 %."},
    "marcelino": {"name": "Marcelino D.", "date": "juillet 2024", "travaux": "Rénovation de toiture, VELUX et gouttières",
                  "text": "Nous avons fait appel à JMC Couverture pour la rénovation de notre toiture avec le remplacement de velux et gouttières. Professionnel, sérieux et à l'écoute. Je recommande !"},
}


def google_review(k, short=False):
    r = GOOGLE_REVIEWS[k]
    txt = r.get("short") if short and r.get("short") else r["text"]
    return (f'<blockquote class="review greview"><div class="stars">★★★★★</div><p>« {txt} »</p>'
            f'<cite>{r["name"]}</cite><span class="rmeta">{r["travaux"]} · {r["date"]} · '
            f'<a href="{BIZ["reviews"]}" target="_blank" rel="noopener">Avis Google</a></span></blockquote>')


def reviews_block(keys, title="Ce que nos clients en disent"):
    return (f'<h2>{title}</h2><div class="grid g2">{"".join(google_review(k, short=True) for k in keys)}</div>'
            f'<p style="margin-top:18px">{google_badge(light=True)}</p>')


def reviews_html(n=3, old=False):
    if old:
        return "".join(f'<blockquote class="review"><p>« {t} »</p><cite>— {a}</cite></blockquote>' for a, t in REVIEWS[:n])
    keys = ["lily", "richard", "larry", "marcelino"][:n]
    return "".join(google_review(k, short=True) for k in keys)



def secu_proprete():
    return """
<section class="section-dark"><div class="wrap">
  <div class="section-head"><span class="eyebrow" style="color:var(--gold-light)">Chez vous, en toute confiance</span>
  <h2>Des équipes formées à la sécurité et à la propreté</h2>
  <p>Intervenir sur votre maison, c'est entrer chez vous. Nos compagnons sont formés pour travailler en toute sécurité et laisser votre maison et votre jardin aussi propres qu'à leur arrivée.</p>
  <p class="pullquote">« Chantier toujours très propre à la fin de la journée. » <span>— Richard K., avis Google</span><br>« Le chantier est protégé et nettoyé chaque soir. » <span>— Lily, avis Google</span></p></div>
  <div class="grid g2">
    <div class="card card-dark"><h3>Sécurité</h3><ul class="checks">
      <li>Équipes formées au travail en hauteur et aux règles de sécurité</li>
      <li>Échafaudages, garde-corps et protections collectives adaptés</li>
      <li>Chantier balisé pour la sécurité de votre famille et de vos voisins</li>
      <li>Matériel contrôlé et entretenu</li>
    </ul></div>
    <div class="card card-dark"><h3>Propreté</h3><ul class="checks">
      <li>Protection des abords, des façades, des terrasses et des jardins</li>
      <li>Rangement et nettoyage du chantier chaque jour</li>
      <li>Gravats et déchets évacués et triés</li>
      <li>Maison rendue propre à la fin des travaux</li>
    </ul></div>
  </div>
</div></section>"""


def bouche_oreille():
    return f"""
<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">Bouche-à-oreille</span>
  <h2>Notre meilleure publicité : vos recommandations</h2>
  {google_badge(light=True)}
  <p>Une grande partie de nos chantiers nous est confiée grâce au <strong>bouche-à-oreille</strong> : un voisin qui a vu notre panneau, un ami satisfait, un client qui revient pour une autre maison. C'est la preuve la plus sincère de la qualité de notre travail.</p></div>
  <div class="grid g3">{reviews_html(3)}</div>
  <div class="wom">
    <div><strong>On vous a recommandé JMC ?</strong><span>Dites-le-nous dans votre demande de devis : nous serons ravis de savoir qui remercier.</span></div>
    <div class="hero-cta" style="margin:0"><a class="btn btn-primary" href="/contact/">Demander un devis</a>
    <a class="btn btn-dark" href="{BIZ['reviews']}" target="_blank" rel="noopener">Laisser un avis Google</a></div>
  </div>
  <p style="margin-top:18px"><a class="more" href="/nos-references/">Voir nos références et tous les avis →</a>{insta_link(" &nbsp;·&nbsp; ")}</p>
</div></section>"""


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
    html = head("Couvreur Île-de-France : rénovation, isolation, toiture zinc | JMC",
                "Couvreur depuis 1985 en Île-de-France : rénovation, isolation, maison neuve, zinc et bardage d'architecte. QUALIBAT & RGE. Devis gratuit ☎ 01 64 21 38 37.",
                "/", lds)
    html += header("/")
    html += f"""
<section class="hero has-photo">{hero_bg()}<div class="wrap">
  <div>
    <span class="eyebrow">40 ans · 1985–2025 · Couvreur charpentier zingueur</span>
    <h1>Couvreur en Île-de-France : rénovation, isolation et toitures zinc</h1>
    <p class="lead">Rénovation, isolation, maisons neuves, zinc et bardage d'architecte : depuis 1985, JMC met au service des particuliers la structure et les équipes qui réalisent les toitures des programmes de promotion immobilière, partout en Île-de-France.</p>
    <div class="hero-cta"><a class="btn btn-primary" href="/contact/">Demander un devis gratuit</a>
    <a class="btn btn-ghost" href="tel:{BIZ['phone_intl']}">Appeler le {BIZ['phone']}</a></div>
    <div class="hero-labels">{labels()}{google_badge()}<ul class="badges"><li>Garantie décennale</li><li>Devis gratuit</li></ul></div>
  </div>
</div></section>

<section class="gallery-band"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Nos réalisations</span><h2>Des toitures qui valorisent votre maison</h2></div>
  {hero_mosaic()}
  <p style="margin-top:18px"><a class="more" href="/nos-references/">Voir toutes nos réalisations →</a>{insta_link(" &nbsp;·&nbsp; ")}</p>
</div></section>

<section class="section-alt"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Nos spécialités</span>
  <h2>Nos spécialités : un seul interlocuteur pour votre toit</h2>
  <p>De la maison neuve à la demeure de caractère, nos couvreurs, charpentiers et zingueurs réalisent l'ensemble de votre toiture : un chantier coordonné, des délais tenus et une seule garantie décennale.</p></div>
  <div class="grid g4" style="margin-bottom:24px">
  {service_card("roof", "Rénovation et remplacement de toiture", "/renovation-toiture/", "Réfection complète de votre couverture, de la charpente aux gouttières.",
                ["Dépose de l'ancienne couverture", "Contrôle et renfort de charpente", "Tuiles, ardoise ou zinc neufs", "Isolation intégrée possible"])}
  {service_card("shield", "Isolation de toiture", "/isolation-toiture/", "Isolation par l'extérieur ou sous rampants, par une entreprise RGE.",
                ["Sarking lors de la rénovation", '<a href="/isolation-rampants/">Isolation des rampants</a>', '<a href="/isolation-combles-perdus/">Isolation des combles perdus</a>', "Aides possibles (RGE)"])}
  {service_card("beam", "Toiture de maison neuve", "/toiture-maison-neuve/", "Le savoir-faire des promoteurs immobiliers, au service des particuliers.",
                ["Charpente, couverture, zinguerie", "Mise hors d'eau rapide", "Coordination avec l'architecte", "Attestations dommages-ouvrage"])}
  {service_card("doc", "Maison d'architecte : zinc et bardage", "/couverture-zinc-bardage/", "Couverture zinc à joint debout, bardage de façade et habillages sur mesure.",
                ["Toitures faible pente et courbes", "Bardage zinc ventilé", "Lucarnes et brisis", "Calepinage avec l'architecte"])}
  {service_card("leaf", "Nettoyage et démoussage", "/nettoyage-toiture/", "Redonnez à votre toit son aspect d'origine et prolongez sa durée de vie.",
                ["Démoussage adapté au matériau", "Remplacement des tuiles abîmées", "Traitement hydrofuge", "Nettoyage des gouttières"])}
  {service_card("doc", "Copropriétés et syndics", "/couvreur-copropriete-syndic/", "Réfection, réparation et isolation des combles pour les immeubles.",
                ["Devis détaillés pour l'AG", "Isolation des combles RGE", "Travaux en site occupé", "Suivi avec le syndic"])}
  {service_card("roof", "Fenêtres de toit VELUX et lucarnes", "/fenetre-de-toit-velux-lucarnes/", "Plus de lumière et de confort sous les toits.",
                ["Remplacement de VELUX", "Création de fenêtres de toit", "Restauration de lucarnes", "Habillage zinc"])}
  {service_card("drop", "Couverture, charpente, zinguerie", "/couverture/", "Tous les métiers du toit, maîtrisés par nos propres équipes.",
                ['<a href="/couverture/">Couverture</a> : tuiles, ardoise, zinc', '<a href="/charpente/">Charpente</a> traditionnelle ou industrielle', '<a href="/zinguerie/">Zinguerie</a> et gouttières', "Fenêtres de toit et lucarnes"])}
  </div>
</div></section>

<section class="savoir"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Savoir-faire de couvreur-zingueur</span>
  <h2>Les ouvrages que peu d'entreprises maîtrisent encore</h2>
  <p>Chien-assis, lucarnes, mansardes, chéneaux, noues, cheminées : ces détails font la qualité et la durée de vie d'une toiture. Nos couvreurs-zingueurs les réalisent dans les règles de l'art.</p></div>
  <div class="city-links">{"".join(f'<a href="{u}">{n}</a>' for u, n in SAVOIR_FAIRE)}</div>
</div></section>

<section class="section-dark"><div class="wrap">
  <div class="stats">
    <div><strong>40</strong><span>ans d'expérience</span></div>
    <div><strong>1 500+</strong><span>chantiers réalisés</span></div>
    <div><strong>1 000+</strong><span>clients, promoteurs et particuliers</span></div>
    <div><strong>10 ans</strong><span>garantie décennale</span></div>
  </div>
</div></section>

<section><div class="wrap split">
  <div class="prose">
    <span class="eyebrow">L'entreprise</span>
    <h2>La structure de la promotion immobilière, au service des particuliers</h2>
    {photo("depot")}
    <p>Depuis 1985, la société JMC réalise la charpente, la couverture et la zinguerie de programmes de <a href="/couvreur-promotion-immobiliere/">promotion immobilière</a> pour Bouygues Immobilier, Kaufman &amp; Broad, Nexity ou Archicrea, ainsi que pour des architectes et des collectivités. Pour tenir ces chantiers, nous avons bâti à Courtry une vraie structure : <strong>des équipes de couvreurs, charpentiers et zingueurs, un atelier, une flotte de véhicules et un encadrement de chantier</strong>.</p>
    <p>Cette organisation, nous la mettons aussi au service des <strong>particuliers</strong> : vous bénéficiez de la capacité et de la rigueur d'une entreprise habituée aux grands chantiers, avec un interlocuteur dédié et l'écoute d'une entreprise familiale. Nous travaillons aussi avec les <strong>maîtres d'œuvre</strong> et les architectes, pouvons <strong>gérer vos démarches en mairie</strong> et vous recommander des prestataires compétents pour préparer au mieux vos travaux.</p>
    <p>Notre approche est simple : <strong>confier vos travaux à des professionnels</strong>. Chaque chantier commence par un diagnostic honnête de votre toiture. Nous vous expliquons ce qui doit être fait tout de suite, ce qui peut attendre, et nous vous remettons un devis clair, poste par poste.</p>
    <h3>Nos engagements</h3>
    <ul class="checks">
      <li><strong>Qualité certifiée</strong> : qualification QUALIBAT et label RGE.</li>
      <li><strong>Sécurité</strong> : garantie décennale et responsabilité civile professionnelle.</li>
      <li><strong>Conseil honnête</strong> : nettoyage ou remplacement, nous vous recommandons la solution adaptée.</li>
      <li><strong>Transparence</strong> : devis gratuit, détaillé et sans engagement.</li>
      <li><strong>Sécurité</strong> : des équipes formées pour intervenir chez vous en toute sécurité.</li>
      <li><strong>Propreté</strong> : chantier protégé, nettoyé chaque jour, gravats évacués.</li>
      <li><strong>Suivi après travaux</strong> : une <a href="/notre-methode-sav-qualite/">équipe SAV et qualité dédiée</a>, en interne.</li>
    </ul>
  </div>
  {aside()}
</div></section>

<section class="section-alt"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Notre process</span><h2>De la visite au SAV : un suivi complet par nos équipes</h2>
  <p>Une méthode éprouvée sur les chantiers de promotion immobilière, et une <strong>équipe SAV et qualité dédiée en interne</strong> qui contrôle chaque chantier et reste votre interlocutrice après les travaux.</p></div>
  {process_html()}
  <p style="margin-top:22px"><a class="more" href="/notre-methode-sav-qualite/">Découvrir notre méthode, notre SAV et notre suivi qualité →</a></p>
</div></section>

{secu_proprete()}
{bouche_oreille()}

<section class="section-alt"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Zone d'intervention</span>
  <h2>Couvreur dans toute l'Île-de-France</h2>
  <p>Depuis notre siège de Courtry, nos équipes interviennent à Paris et dans les huit départements franciliens, en particulier dans les communes des bords de Marne et de Seine-et-Marne.</p></div>
  {city_groups()}
  <ul class="cities">{"".join(f"<li>{c}</li>" for c in CITIES[3:])}</ul>
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
    <p>Pour les toits plats, nous réalisons l'<a href="/etancheite-toiture-terrasse/">étanchéité des toitures terrasses</a> par membrane EPDM ou bitumineuse, avec reprise des descentes d'eaux pluviales.</p>

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
    <p>Pose, remplacement et réparation de gouttières pendantes, havraises ou nantaises, et reprise des <a href="/etancheite-toiture-terrasse/">descentes d'eaux pluviales</a> avec leurs dauphins.</p>
    <h3>Chéneaux et noues</h3>
    <p>Réfection des <a href="/cheneau-noue-zinc/">chéneaux encaissés et des noues</a>, zones où l'eau se concentre et qui sont à l'origine de nombreuses fuites.</p>
    <h3>Entourages de cheminée et de fenêtres de toit</h3>
    <p>Abergements, <a href="/souche-cheminee-solin-abergement/">solins de cheminée</a> et bavettes pour assurer une étanchéité parfaite autour des cheminées, des lucarnes et des fenêtres de toit.</p>
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
         "Si vous changez l'aspect extérieur (matériau, couleur, ajout de fenêtres de toit), une déclaration préalable de travaux est en général nécessaire. Une réfection à l'identique en est souvent dispensée, mais les règles dépendent du PLU de votre commune : nous vérifions pour vous et pouvons gérer les démarches auprès de la mairie."),
        ("Peut-on bénéficier d'aides pour refaire sa toiture ?",
         "Le remplacement de la couverture seul n'est pas aidé, mais l'isolation de la toiture réalisée en même temps par une entreprise RGE comme JMC peut ouvrir droit à des aides à la rénovation énergétique (MaPrimeRénov', primes CEE, éco-prêt à taux zéro), selon vos revenus et les conditions en vigueur."),
    ]
    desc = "Remplacement et réfection complète de toiture : dépose, contrôle de charpente, écran sous-toiture, couverture neuve, zinguerie et isolation RGE."
    lds = [org_ld(), crumbs_ld(trail), service_ld("Rénovation et remplacement de toiture", "/renovation-toiture/", desc), faq_ld(faq)]
    html = head("Rénovation et remplacement de toiture en Île-de-France | JMC",
                "Remplacement et réfection complète de toiture en Île-de-France : tuiles, ardoise, zinc, isolation RGE. 40 ans d'expérience. Devis gratuit.",
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
    <p>Vous prévoyez des panneaux solaires ? Pensez à <a href="/toiture-avant-panneaux-photovoltaiques/">rénover la toiture avant leur installation</a>.</p>
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
    {reviews_block(['lily', 'richard'])}
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
                "Nettoyage de toit, démoussage, traitement anti-mousse et hydrofuge en Île-de-France, par de vrais couvreurs. 40 ans d'expérience. Devis gratuit.",
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
                "Vous faites construire ? JMC, couvreur des promoteurs depuis 1985, réalise la charpente, la couverture et la zinguerie de votre maison neuve. Devis gratuit.",
                "/toiture-maison-neuve/", lds)
    html += header("/toiture-maison-neuve/")
    html += page_hero(trail, "Maison neuve · Construction", "Toiture de maison neuve : l'expertise des promoteurs au service des particuliers",
                      "Depuis 1985, les grands promoteurs immobiliers nous confient la charpente et la couverture de leurs programmes neufs. Vous faites construire votre maison ? Profitez du même savoir-faire, en direct.")
    html += f"""
<section><div class="wrap split">
  <article class="prose">
    {photo("depot", eager=True)}
    <h2>Le savoir-faire de la promotion immobilière, pour votre maison</h2>
    <p>Bouygues Immobilier, Kaufman &amp; Broad, Nexity : la société JMC intervient depuis des années dans la <a href="/couvreur-promotion-immobiliere/">promotion immobilière</a>, pour des promoteurs et des architectes, sur des programmes de logements neufs en Île-de-France. Ces chantiers exigent une rigueur particulière : respect strict des plannings, conformité aux normes, contrôles de bureaux de contrôle, finitions irréprochables.</p>
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
      <li><strong>Contrôle qualité et SAV</strong><br>Vérification par notre équipe qualité interne avant réception, puis suivi par notre SAV.</li>
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


def isolation():
    trail = [("/", "Accueil"), ("/isolation-toiture/", "Isolation de toiture")]
    faq = [
        ("Quelle est la différence entre le sarking et l'isolation sous rampants ?",
         "Le sarking consiste à poser l'isolant par l'extérieur, au-dessus des chevrons, lors de la réfection de la couverture : il supprime les ponts thermiques et préserve le volume habitable. L'isolation sous rampants se pose par l'intérieur, entre et sous les chevrons : elle est adaptée quand la couverture est en bon état."),
        ("Quelles aides pour isoler sa toiture ?",
         "Réalisés par une entreprise RGE comme JMC, vos travaux d'isolation peuvent ouvrir droit à MaPrimeRénov', aux primes CEE, à l'éco-prêt à taux zéro et à une TVA réduite à 5,5 %, selon vos revenus, votre logement et les conditions en vigueur au moment des travaux. Une résistance thermique minimale est exigée (en général R ≥ 6 m².K/W en rampants et R ≥ 7 m².K/W en combles perdus)."),
        ("Isoler la toiture, est-ce utile aussi en été ?",
         "Oui. Avec un isolant dense comme la fibre de bois, la chaleur met plus longtemps à traverser la toiture : les pièces sous les combles restent nettement plus fraîches pendant les fortes chaleurs."),
        ("Peut-on isoler sans refaire la couverture ?",
         "Oui, par l'intérieur (sous rampants ou combles perdus). Mais si votre couverture doit être refaite dans les prochaines années, il est plus judicieux de combiner les deux chantiers : l'échafaudage est mutualisé et l'isolation par l'extérieur devient possible."),
    ]
    desc = "Isolation de toiture par l'extérieur (sarking), sous rampants et combles, par une entreprise RGE : confort, économies d'énergie et aides financières."
    lds = [org_ld(), crumbs_ld(trail), service_ld("Isolation de toiture", "/isolation-toiture/", desc), faq_ld(faq)]
    html = head("Isolation de toiture, rampants et combles perdus, RGE | JMC",
                "Isolation de toiture par l'extérieur (sarking) ou sous rampants par un couvreur RGE en Île-de-France. Confort, économies, aides possibles. Devis gratuit.",
                "/isolation-toiture/", lds)
    html += header("/isolation-toiture/")
    html += page_hero(trail, "Isolation · Entreprise RGE", "Isolation de toiture par un couvreur RGE en Île-de-France",
                      "Jusqu'à 30 % des pertes de chaleur d'une maison mal isolée passent par le toit. Nous isolons votre toiture par l'extérieur ou par l'intérieur, idéalement en même temps que sa rénovation.")
    html += f"""
<section><div class="wrap split">
  <article class="prose">
    {photo("drone", eager=True)}
    <h2>Pourquoi isoler votre toiture ?</h2>
    <ul class="checks">
      <li><strong>Moins de dépenses de chauffage</strong> : la toiture est le premier poste de déperdition d'une maison non isolée.</li>
      <li><strong>Un vrai confort d'été</strong> : des combles habitables enfin vivables pendant les canicules.</li>
      <li><strong>Une maison mieux valorisée</strong> : l'isolation améliore l'étiquette du DPE, déterminante à la vente comme à la location.</li>
      <li><strong>Des aides financières</strong> : parce que nous sommes certifiés RGE.</li>
    </ul>

    <h2>Nos techniques d'isolation de toiture</h2>
    <h3>Isolation par l'extérieur (sarking)</h3>
    <p>Lors d'une <a href="/renovation-toiture/">rénovation de toiture</a>, la couverture est déposée et des panneaux isolants rigides (fibre de bois, polyuréthane) sont posés en continu au-dessus des chevrons, avant la nouvelle couverture. Avantages : aucun pont thermique, aucun volume perdu à l'intérieur, charpente apparente préservée.</p>
    <h3><a href="/isolation-rampants/">Isolation sous rampants</a></h3>
    <p>Pour des combles aménagés dont la couverture est saine, nous posons l'isolant entre et sous les chevrons (laine minérale, fibre de bois, ouate de cellulose), avec un pare-vapeur soigneusement raccordé pour garantir l'étanchéité à l'air.</p>
    <h3><a href="/isolation-combles-perdus/">Isolation des combles perdus</a></h3>
    <p>Pour des combles non aménagés, l'isolant est déroulé ou soufflé sur le plancher : une solution rapide et très rentable. Voir notre page dédiée à l'<a href="/isolation-combles-perdus/">isolation des combles perdus par soufflage</a>.</p>

    <h2>Isolation et rénovation : le bon moment</h2>
    <p>Le meilleur moment pour isoler, c'est quand on refait la couverture. L'échafaudage est déjà en place, la charpente est accessible et l'isolation par l'extérieur devient possible. C'est aussi vrai pour une <a href="/toiture-maison-neuve/">maison neuve</a>, où nous intégrons l'isolation de la toiture aux exigences de la RE2020.</p>

    {reviews_block(['richard', 'lily'])}
    <h2>Aides financières</h2>
    <p>Entreprise <strong>RGE</strong>, JMC vous permet de prétendre aux aides à la rénovation énergétique : MaPrimeRénov', primes CEE, éco-prêt à taux zéro et TVA à 5,5 %, selon votre situation et les règles en vigueur. Nous vous remettons un devis conforme aux exigences de ces dispositifs.</p>
  </article>
  {aside("Isolation par un couvreur RGE")}
</div></section>
"""
    html += faq_html(faq, "Questions fréquentes sur l'isolation de toiture")
    html += cta_band("Envie d'une maison plus confortable ?", "Étude gratuite de l'isolation de votre toiture, aides comprises.")
    html += footer()
    write("/isolation-toiture/", html)


def zinc_bardage():
    trail = [("/", "Accueil"), ("/couverture-zinc-bardage/", "Couverture zinc et bardage")]
    faq = [
        ("Quelle est la durée de vie d'une couverture en zinc ?",
         "Bien conçue et bien posée, une couverture en zinc dure couramment de 50 à 100 ans. Le zinc se protège naturellement par sa patine et demande très peu d'entretien."),
        ("Le zinc convient-il à une toiture à faible pente ?",
         "Oui, c'est l'un de ses grands atouts : posé à joint debout, le zinc s'adapte aux toitures à faible pente, aux monopentes et aux formes courbes, très prisées en architecture contemporaine."),
        ("Peut-on associer bardage zinc et isolation par l'extérieur ?",
         "Oui. Le bardage zinc se pose en façade ventilée : l'isolant est fixé sur le mur, une lame d'air circule derrière le zinc, ce qui protège l'isolant et assure la durabilité de l'ensemble."),
        ("Quelles précautions avec le zinc ?",
         "Le zinc ne doit pas recevoir l'eau de ruissellement d'une surface en cuivre, ni être en contact direct avec certains bois acides (chêne, châtaignier, red cedar), le plâtre ou le ciment frais. Ces points font partie de notre étude de détail."),
        ("Travaillez-vous avec mon architecte ?",
         "Oui, c'est notre quotidien. Nous étudions les plans, proposons des solutions techniques, réalisons le calepinage et les échantillons, et respectons les intentions architecturales jusque dans les détails d'exécution."),
    ]
    desc = "Couverture zinc à joint debout, bardage zinc de façade et habillages pour maisons d'architecte, en neuf comme en rénovation."
    lds = [org_ld(), crumbs_ld(trail), service_ld("Couverture zinc et bardage zinc", "/couverture-zinc-bardage/", desc), faq_ld(faq)]
    html = head("Toiture zinc joint debout et bardage, maison d'architecte | JMC",
                "Couvreur-zingueur pour maisons d'architecte : couverture zinc à joint debout, bardage de façade, lucarnes et habillages, partout en Île-de-France.",
                "/couverture-zinc-bardage/", lds)
    html += header("/couverture-zinc-bardage/")
    html += page_hero(trail, "Maison d'architecte", "Maison d'architecte : couverture zinc et bardage",
                      "Toitures à joint debout, façades en zinc, lucarnes et habillages sur mesure : nos couvreurs-zingueurs donnent forme aux projets des architectes, en neuf comme en rénovation.")
    html += f"""
<section><div class="wrap split">
  <article class="prose">
    {photo("mansarde", eager=True)}
    <h2>Le zinc, matériau de prédilection des architectes</h2>
    <p>Durable, léger, recyclable, le zinc se plie à toutes les formes : toitures à faible pente, monopentes, courbes, brisis de mansardes, façades entières. Sa patine naturelle, ou ses versions prépatinées gris clair et anthracite, s'accordent aussi bien avec une maison bourgeoise qu'avec une architecture contemporaine.</p>
    <p>C'est aussi un savoir-faire profondément francilien : celui des couvreurs-zingueurs parisiens est inscrit depuis 2024 au patrimoine culturel immatériel de l'UNESCO.</p>

    <h2>Nos réalisations en zinc</h2>
    <h3>Couverture zinc à joint debout ou à tasseaux</h3>
    <p>Pose traditionnelle sur voligeage ventilé, pour toitures neuves, extensions et surélévations, avec tous les accessoires : faîtages, rives, noues, chéneaux encaissés.</p>
    <h3>Bardage zinc de façade</h3>
    <p>Joint debout vertical ou horizontal, cassettes, clins : nous habillons vos façades en zinc sur ossature ventilée, compatible avec l'isolation thermique par l'extérieur.</p>
    <h3>Zinc naturel, quartz, anthracite ou coloré</h3>
    <p>Zinc naturel qui se patine avec le temps, zinc prépatiné gris clair (type quartz) ou anthracite, zinc pigmenté de couleur : nous vous présentons les aspects possibles et réalisons des échantillons avec votre architecte.</p>
    <h3>Extension et surélévation en zinc</h3>
    <p>Pour une extension contemporaine ou une surélévation, le zinc à joint debout habille toiture et façades d'un seul matériau, avec une grande légèreté pour la structure existante.</p>
    <h3>Lucarnes, brisis et habillages</h3>
    <p>Lucarnes et brisis de <a href="/toiture-mansardee-brisis-terrasson/">toitures mansardées</a>, <a href="/chien-assis-lucarne/">chiens-assis</a>, couronnements d'acrotères, encadrements de baies, avancées de toit et ornements : le zinc permet des finitions d'une grande précision.</p>
    {photo("drone")}

    <h2>Une méthode pensée pour les projets d'architecte</h2>
    <ul class="checks">
      <li><strong>Étude des plans</strong> et des détails avec l'architecte dès la conception</li>
      <li><strong>Choix des finitions</strong> : aspect, teinte, largeur des bacs, sens de pose</li>
      <li><strong>Calepinage</strong> et échantillons avant fabrication</li>
      <li><strong>Façonnage sur mesure</strong> et pose par nos propres zingueurs</li>
      <li><strong>Respect des règles de l'art</strong> (DTU) : ventilation, dilatation, compatibilité des matériaux</li>
    </ul>
    <p>Ce même savoir-faire sert aussi aux <a href="/toiture-maison-neuve/">maisons neuves</a> plus classiques et à la <a href="/zinguerie/">zinguerie</a> de tous types de toitures.</p>
  </article>
  {aside("Votre projet en zinc")}
</div></section>
"""
    html += faq_html(faq, "Questions fréquentes sur le zinc et le bardage")
    html += cta_band("Un projet d'architecte en zinc ?", "Envoyez-nous vos plans : étude technique et devis gratuits.")
    html += footer()
    write("/couverture-zinc-bardage/", html)


VILLES = [
    {"slug": "couvreur-saint-maur-des-fosses", "name": "Saint-Maur-des-Fossés", "dept": "Val-de-Marne", "num": "94",
     "cp": "94100 / 94210",
     "lead": "Maisons bourgeoises, villas du début du XXe siècle et pavillons en meulière : nous rénovons, isolons et entretenons les toitures de Saint-Maur-des-Fossés, de La Varenne au Parc-Saint-Maur.",
     "texte": [
         "Nichée dans une boucle de la Marne, Saint-Maur-des-Fossés compte parmi les communes les plus résidentielles du Val-de-Marne. Ses rues bordées de villas et de maisons de maître offrent une grande variété de toitures : ardoise, tuile plate, tuile mécanique, brisis en zinc, lucarnes ouvragées et épis de faîtage.",
         "Ces couvertures anciennes demandent un vrai savoir-faire de couvreur-zingueur : respecter le caractère de la maison tout en lui apportant l'étanchéité et l'isolation d'aujourd'hui. C'est exactement ce que nous faisons depuis 1985.",
     ],
     "quartiers": ["La Varenne-Saint-Hilaire", "Le Parc-Saint-Maur", "Adamville", "Champignol", "La Pie", "Saint-Maur-Créteil", "Les Mûriers"],
     "voisines": ["Joinville-le-Pont", "Champigny-sur-Marne", "Créteil", "Bonneuil-sur-Marne", "Chennevières-sur-Marne"]},
    {"slug": "couvreur-nogent-sur-marne", "name": "Nogent-sur-Marne", "dept": "Val-de-Marne", "num": "94", "cp": "94130",
     "lead": "Maisons de maître, villas Belle Époque et pavillons en meulière des coteaux de la Marne : votre couvreur à Nogent-sur-Marne pour la rénovation, l'isolation et les toitures en zinc.",
     "texte": [
         "Sur les coteaux qui dominent la Marne, Nogent-sur-Marne mêle demeures bourgeoises, villas du début du XXe siècle, pavillons en meulière et petits immeubles de caractère. Les toitures y sont souvent complexes : fortes pentes, brisis d'ardoise, lucarnes, chéneaux et ornements en zinc.",
         "Nous intervenons à Nogent-sur-Marne pour des réfections complètes, des isolations par l'extérieur, des travaux de zinguerie fine et l'entretien de toitures anciennes, avec le souci de préserver l'élégance de ces maisons.",
     ],
     "quartiers": [],
     "voisines": ["Le Perreux-sur-Marne", "Fontenay-sous-Bois", "Vincennes", "Joinville-le-Pont", "Champigny-sur-Marne"]},
    {"slug": "couvreur-le-perreux-sur-marne", "name": "Le Perreux-sur-Marne", "dept": "Val-de-Marne", "num": "94", "cp": "94170",
     "lead": "Maisons en meulière, villas des bords de Marne et maisons contemporaines : votre couvreur au Perreux-sur-Marne pour rénover, isoler et entretenir votre toiture.",
     "texte": [
         "Commune résidentielle des bords de Marne, Le Perreux-sur-Marne est réputé pour ses maisons en meulière, ses villas du début du XXe siècle et ses rues pavillonnaires arborées. Beaucoup de ces toitures en tuiles mécaniques ou en ardoise approchent de l'âge d'une réfection complète.",
         "Nous accompagnons les propriétaires perreuxiens dans la rénovation de leur couverture, l'isolation de leurs combles et la réalisation d'extensions et de surélévations en zinc, en respectant l'architecture de chaque maison.",
     ],
     "quartiers": [],
     "voisines": ["Nogent-sur-Marne", "Bry-sur-Marne", "Neuilly-Plaisance", "Fontenay-sous-Bois", "Champigny-sur-Marne"]},
    {"slug": "couvreur-lagny-sur-marne", "name": "Lagny-sur-Marne", "dept": "Seine-et-Marne", "num": "77", "cp": "77400",
     "lead": "Centre historique, maisons bourgeoises des bords de Marne et quartiers pavillonnaires : votre couvreur à Lagny-sur-Marne, tout près de notre siège de Courtry.",
     "texte": [
         "Ville historique des bords de Marne, Lagny-sur-Marne associe un centre ancien aux toitures de tuiles plates, des maisons bourgeoises et des quartiers pavillonnaires plus récents. Chaque époque a ses matériaux et ses points faibles, que nos couvreurs connaissent bien.",
         "Implantés à quelques kilomètres, à Courtry, nous intervenons rapidement à Lagny-sur-Marne et dans les communes voisines pour la rénovation, l'isolation, le nettoyage de toiture et la construction de maisons neuves.",
     ],
     "quartiers": [],
     "voisines": ["Thorigny-sur-Marne", "Saint-Thibault-des-Vignes", "Pomponne", "Montévrain", "Conches-sur-Gondoire", "Chanteloup-en-Brie"]},
    {"slug": "couvreur-ozoir-la-ferriere", "name": "Ozoir-la-Ferrière", "dept": "Seine-et-Marne", "num": "77", "cp": "77330",
     "lead": "Villas, maisons individuelles et constructions récentes en bordure de la forêt d'Armainvilliers : votre couvreur à Ozoir-la-Ferrière pour rénover, isoler et construire.",
     "texte": [
         "Commune résidentielle en bordure de la forêt d'Armainvilliers, Ozoir-la-Ferrière est composée en grande partie de maisons individuelles, des villas anciennes aux maisons contemporaines. L'environnement boisé favorise les mousses et l'encrassement des gouttières : l'entretien de la toiture y est essentiel.",
         "Nous intervenons à Ozoir-la-Ferrière pour le nettoyage et le démoussage, la rénovation complète de toitures, l'isolation par l'extérieur et la toiture des maisons neuves, avec des finitions dignes des plus belles propriétés.",
     ],
     "quartiers": [],
     "voisines": ["Gretz-Armainvilliers", "Lésigny", "Pontault-Combault", "Roissy-en-Brie", "Férolles-Attilly", "Tournan-en-Brie"]},
    {"slug": "couvreur-bussy-saint-georges", "name": "Bussy-Saint-Georges", "dept": "Seine-et-Marne", "num": "77", "cp": "77600",
     "lead": "Maisons individuelles récentes, programmes neufs et constructions d'architecte : votre couvreur à Bussy-Saint-Georges, au cœur du Val de Marne-la-Vallée.",
     "texte": [
         "Ville nouvelle du secteur de Marne-la-Vallée, Bussy-Saint-Georges s'est fortement développée depuis les années 1990. Ses nombreuses maisons individuelles arrivent à l'âge du premier gros entretien de toiture, tandis que de nouvelles constructions continuent de sortir de terre.",
         "Notre expérience des programmes de promotion immobilière est un atout pour les Buxangeorgiens : toiture de maison neuve, extensions, nettoyage et traitement des toitures des années 1990-2000, isolation et zinguerie.",
     ],
     "quartiers": [],
     "voisines": ["Ferrières-en-Brie", "Collégien", "Jossigny", "Montévrain", "Bussy-Saint-Martin", "Lagny-sur-Marne"]},
]



def _v(name, dept, num, cp, lead, p1, p2, voisines):
    import unicodedata
    slug = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
    slug = "couvreur-" + "".join(c if c.isalnum() else "-" for c in slug).strip("-").replace("--", "-")
    return {"slug": slug, "name": name, "dept": dept, "num": num, "cp": cp, "lead": lead,
            "texte": [p1, p2], "quartiers": [], "voisines": voisines}


ABF = ("Une grande partie de la commune est couverte par des protections patrimoniales : les travaux de toiture y sont "
       "souvent soumis à l'avis de l'Architecte des Bâtiments de France. Nous connaissons ces exigences (matériaux, teintes, "
       "lucarnes, zinguerie) et pouvons gérer pour vous le dossier de déclaration préalable.")

VILLES += [
    _v("Fontainebleau", "Seine-et-Marne", "77", "77300",
       "Hôtels particuliers, maisons bourgeoises et villas en lisière de forêt : votre couvreur à Fontainebleau pour des toitures dignes de la cité impériale.",
       "Autour de son château, inscrit au patrimoine mondial de l'UNESCO, Fontainebleau aligne hôtels particuliers, maisons de maître et villas cachées dans la verdure de la forêt. Ardoise, tuile plate de pays, brisis, lucarnes ouvragées et zinguerie fine composent des toitures exigeantes.",
       ABF, ["Avon", "Samois-sur-Seine", "Bois-le-Roi", "Barbizon", "Héricy", "Thomery"]),
    _v("Barbizon", "Seine-et-Marne", "77", "77630",
       "Maisons en pierre, longères et propriétés du village des peintres : votre couvreur à Barbizon pour rénover et préserver les toitures anciennes.",
       "Village des peintres de l'École de Barbizon, à l'orée de la forêt de Fontainebleau, Barbizon a conservé ses maisons en pierre, ses longères et ses belles propriétés aux toitures de tuiles plates anciennes. Leur rénovation exige de respecter le caractère des lieux, des matériaux à la pose.",
       ABF, ["Fontainebleau", "Chailly-en-Bière", "Saint-Martin-en-Bière", "Arbonne-la-Forêt", "Cély"]),
    _v("Versailles", "Yvelines", "78", "78000",
       "Hôtels particuliers, immeubles anciens et villas des quartiers résidentiels : votre couvreur à Versailles pour la rénovation, l'isolation et les toitures en ardoise et zinc.",
       "Des quartiers Notre-Dame et Saint-Louis aux villas de Montreuil, Clagny-Glatigny ou Porchefontaine, Versailles réunit un patrimoine bâti exceptionnel : hôtels particuliers des XVIIe et XVIIIe siècles, immeubles à combles mansardés, maisons bourgeoises. Ardoise, zinc, lucarnes et brisis y sont la règle.",
       ABF, ["Le Chesnay-Rocquencourt", "Viroflay", "Buc", "Saint-Cyr-l'École", "Vélizy-Villacoublay"]),
    _v("Le Vésinet", "Yvelines", "78", "78110",
       "Villas de la ville-parc, maisons de maître et demeures du XIXe siècle : votre couvreur au Vésinet pour des toitures à la hauteur de ce cadre unique.",
       "Conçu au XIXe siècle comme une ville-parc, avec ses lacs, ses rivières et ses grandes pelouses, Le Vésinet est l'une des communes résidentielles les plus prisées de l'ouest parisien. Ses villas présentent des toitures variées et souvent complexes : ardoise, tuiles, épis de faîtage, lucarnes et zinguerie décorative.",
       ABF, ["Chatou", "Croissy-sur-Seine", "Le Pecq", "Montesson", "Saint-Germain-en-Laye"]),
    _v("Saint-Germain-en-Laye", "Yvelines", "78", "78100",
       "Hôtels particuliers du centre historique, villas et maisons bourgeoises : votre couvreur à Saint-Germain-en-Laye pour la rénovation et l'isolation de votre toiture.",
       "Entre son château, sa terrasse dessinée par Le Nôtre et sa forêt domaniale, Saint-Germain-en-Laye offre un patrimoine résidentiel remarquable : hôtels particuliers du centre ancien, immeubles de caractère et grandes villas. Couvertures en ardoise et en tuile plate, combles mansardés et lucarnes y demandent un savoir-faire traditionnel.",
       ABF, ["Le Pecq", "Le Vésinet", "Chambourcy", "Mareil-Marly", "Maisons-Laffitte"]),
    _v("Maisons-Laffitte", "Yvelines", "78", "78600",
       "Villas du Parc, maisons de maître et propriétés de la cité du cheval : votre couvreur à Maisons-Laffitte.",
       "Autour de son château et de son célèbre Parc loti au XIXe siècle, Maisons-Laffitte, la « cité du cheval », alterne grandes villas, maisons de maître et propriétés arborées le long de larges avenues. Les toitures y sont souvent anciennes, en ardoise ou en tuiles, avec lucarnes et ornements de zinc.",
       "Nous rénovons ces couvertures en respectant leur caractère, en y intégrant une isolation performante et une zinguerie neuve, pour des maisons plus confortables et mieux valorisées.",
       ["Sartrouville", "Le Mesnil-le-Roi", "Saint-Germain-en-Laye", "Montesson", "Herblay-sur-Seine"]),
    _v("Le Chesnay-Rocquencourt", "Yvelines", "78", "78150",
       "Maisons individuelles, villas et résidences aux portes de Versailles : votre couvreur au Chesnay-Rocquencourt.",
       "Aux portes de Versailles, Le Chesnay-Rocquencourt associe quartiers pavillonnaires recherchés, villas et résidences en copropriété. Beaucoup de toitures datent des années 1960 à 1990 et arrivent à l'âge de la rénovation ou de l'isolation.",
       "Nous intervenons aussi bien pour les propriétaires de maisons que pour les syndics de copropriété : réfection de couverture, isolation des combles, fenêtres de toit et zinguerie.",
       ["Versailles", "La Celle-Saint-Cloud", "Bailly", "Louveciennes", "Vaucresson"]),
    _v("Chatou", "Yvelines", "78", "78400",
       "Villas des bords de Seine, maisons bourgeoises et pavillons : votre couvreur à Chatou pour rénover, isoler et entretenir votre toiture.",
       "Ville des Impressionnistes, célèbre pour son île et la Maison Fournaise, Chatou a gardé de belles villas des bords de Seine et des maisons bourgeoises du début du XXe siècle, aux toitures en tuiles mécaniques, en ardoise ou en zinc.",
       "L'humidité des bords de Seine sollicite fortement les couvertures et la zinguerie : nous assurons leur rénovation complète, leur isolation et leur entretien.",
       ["Croissy-sur-Seine", "Le Vésinet", "Rueil-Malmaison", "Montesson", "Carrières-sur-Seine"]),
    _v("Croissy-sur-Seine", "Yvelines", "78", "78290",
       "Villas, maisons bourgeoises et propriétés des bords de Seine : votre couvreur à Croissy-sur-Seine.",
       "Commune résidentielle nichée dans une boucle de la Seine, Croissy-sur-Seine compte de nombreuses villas et maisons bourgeoises entourées de jardins. Leurs toitures, souvent anciennes, mêlent tuiles, ardoises, lucarnes et zinguerie travaillée.",
       "Nous les rénovons dans les règles de l'art, avec la possibilité d'isoler la toiture par l'extérieur lors de la réfection, sans perdre de volume dans les combles.",
       ["Chatou", "Le Vésinet", "Bougival", "Le Pecq", "Rueil-Malmaison"]),
    _v("Louveciennes", "Yvelines", "78", "78430",
       "Propriétés de caractère et villas des coteaux de Seine : votre couvreur à Louveciennes.",
       "Sur les coteaux qui dominent la Seine, Louveciennes conserve un cadre exceptionnel : grandes propriétés, maisons de caractère et villas, à l'ombre de son aqueduc et du pavillon de Madame du Barry. Les toitures, anciennes et souvent complexes, demandent un savoir-faire traditionnel.",
       ABF, ["Marly-le-Roi", "Bougival", "Le Chesnay-Rocquencourt", "Port-Marly", "La Celle-Saint-Cloud"]),
    _v("Marly-le-Roi", "Yvelines", "78", "78160",
       "Maisons de caractère du centre ancien, villas et propriétés : votre couvreur à Marly-le-Roi.",
       "Riche de son domaine national et de son centre ancien, Marly-le-Roi est une commune résidentielle où se côtoient maisons de caractère, villas et propriétés boisées. Toitures en tuile plate, en ardoise et lucarnes anciennes y sont fréquentes.",
       ABF, ["Louveciennes", "Le Port-Marly", "Mareil-Marly", "L'Étang-la-Ville", "Saint-Germain-en-Laye"]),
    _v("Bougival", "Yvelines", "78", "78380",
       "Villas des bords de Seine et maisons de coteau : votre couvreur à Bougival pour rénover et isoler votre toiture.",
       "Entre Seine et coteaux, Bougival a inspiré les peintres impressionnistes et conserve de belles villas, des maisons de bord de Seine et des propriétés étagées sur la pente. Leurs toitures exposées au vent et à l'humidité méritent une attention particulière.",
       "Nous intervenons pour la rénovation complète de ces couvertures, leur isolation, la reprise de la zinguerie et la création ou le remplacement de fenêtres de toit et de lucarnes.",
       ["Louveciennes", "La Celle-Saint-Cloud", "Croissy-sur-Seine", "Rueil-Malmaison", "Le Port-Marly"]),
    _v("Neuilly-sur-Seine", "Hauts-de-Seine", "92", "92200",
       "Hôtels particuliers, villas et immeubles haussmanniens : votre couvreur-zingueur à Neuilly-sur-Seine pour les particuliers et les copropriétés.",
       "Entre le bois de Boulogne et la Seine, Neuilly-sur-Seine réunit hôtels particuliers, villas et immeubles de standing aux toitures en zinc et en ardoise, avec combles mansardés, lucarnes et terrassons. Ces couvertures exigent le savoir-faire des couvreurs-zingueurs parisiens.",
       "Nous intervenons pour les propriétaires comme pour les syndics de copropriété : réfection de couverture zinc, isolation des combles, remplacement de fenêtres de toit et restauration de lucarnes.",
       ["Levallois-Perret", "Courbevoie", "Puteaux", "Paris 16e", "Paris 17e"]),
    _v("Boulogne-Billancourt", "Hauts-de-Seine", "92", "92100",
       "Villas des années 1920-1930, maisons de ville et immeubles : votre couvreur à Boulogne-Billancourt.",
       "Boulogne-Billancourt est connue pour ses villas modernistes des années 1920-1930, dont plusieurs signées Le Corbusier ou Mallet-Stevens, mais aussi pour ses maisons de ville, ses quartiers résidentiels proches du bois de Boulogne et ses nombreux immeubles en copropriété.",
       "Toitures-terrasses, couvertures zinc, ardoise ou tuiles : nous rénovons, isolons et entretenons tous les types de toits, pour les particuliers comme pour les syndics.",
       ["Paris 16e", "Issy-les-Moulineaux", "Saint-Cloud", "Sèvres", "Meudon"]),
    _v("Saint-Cloud", "Hauts-de-Seine", "92", "92210",
       "Villas de Montretout, maisons bourgeoises et immeubles de caractère : votre couvreur à Saint-Cloud.",
       "Accrochée aux coteaux face à Paris, à côté de son domaine national, Saint-Cloud est une commune résidentielle prisée, des villas du quartier de Montretout aux maisons bourgeoises et immeubles du centre. Ardoise, zinc, tuiles et lucarnes composent des toitures variées.",
       ABF, ["Garches", "Vaucresson", "Sèvres", "Boulogne-Billancourt", "Suresnes"]),
    _v("Sceaux", "Hauts-de-Seine", "92", "92330",
       "Maisons bourgeoises, villas et centre ancien près du parc : votre couvreur à Sceaux.",
       "Autour de son célèbre parc dessiné par Le Nôtre, Sceaux offre un cadre résidentiel recherché : maisons bourgeoises, villas en meulière et centre ancien aux toitures de tuiles et d'ardoise. Beaucoup de ces couvertures centenaires arrivent à l'âge d'une rénovation complète.",
       ABF, ["Bourg-la-Reine", "Antony", "Fontenay-aux-Roses", "Châtenay-Malabry", "Le Plessis-Robinson"]),
    _v("Ville-d'Avray", "Hauts-de-Seine", "92", "92410",
       "Villas et propriétés entre étangs et forêt : votre couvreur à Ville-d'Avray.",
       "Nichée entre la forêt de Fausses-Reposes et les étangs peints par Corot, Ville-d'Avray est une commune résidentielle et boisée, faite de villas et de propriétés aux toitures souvent anciennes. L'environnement forestier favorise mousses et encrassement des gouttières.",
       "Nous assurons la rénovation de ces toitures, leur isolation, mais aussi leur nettoyage et l'entretien de la zinguerie, pour préserver durablement votre maison.",
       ["Sèvres", "Chaville", "Marnes-la-Coquette", "Saint-Cloud", "Versailles"]),
    _v("Marnes-la-Coquette", "Hauts-de-Seine", "92", "92430",
       "Grandes propriétés et villas en lisière du parc de Saint-Cloud : votre couvreur à Marnes-la-Coquette.",
       "Petite commune très résidentielle en lisière du domaine national de Saint-Cloud, Marnes-la-Coquette se compose de grandes propriétés et de villas entourées de verdure. Leurs toitures, souvent d'exception, demandent une exécution irréprochable.",
       "Ardoise, zinc, tuile plate, lucarnes et zinguerie décorative : nous réalisons des travaux soignés, avec un interlocuteur unique du diagnostic à la réception.",
       ["Vaucresson", "Garches", "Ville-d'Avray", "Saint-Cloud", "La Celle-Saint-Cloud"]),
    _v("Vaucresson", "Hauts-de-Seine", "92", "92420",
       "Villas, maisons individuelles et propriétés arborées : votre couvreur à Vaucresson.",
       "Commune résidentielle et verdoyante de l'ouest parisien, Vaucresson est composée majoritairement de villas et de maisons individuelles entourées de jardins. Ces toitures, de la villa ancienne à la maison d'architecte, appellent des travaux de qualité.",
       "Rénovation, isolation par l'extérieur, couverture zinc pour extensions contemporaines, fenêtres de toit : nous prenons en charge l'ensemble de votre projet de toiture.",
       ["Garches", "Marnes-la-Coquette", "La Celle-Saint-Cloud", "Le Chesnay-Rocquencourt", "Rueil-Malmaison"]),
    _v("Garches", "Hauts-de-Seine", "92", "92380",
       "Villas, maisons bourgeoises et résidences : votre couvreur à Garches.",
       "Entre le domaine de Saint-Cloud et le golf de Saint-Cloud situé sur son territoire, Garches est une commune résidentielle où dominent villas, maisons bourgeoises et petites résidences. Les toitures y sont souvent en tuiles ou en ardoise, avec lucarnes et zinguerie.",
       "Nous intervenons pour les particuliers comme pour les copropriétés : réfection, isolation des combles, fenêtres de toit et entretien.",
       ["Vaucresson", "Saint-Cloud", "Rueil-Malmaison", "Marnes-la-Coquette", "Suresnes"]),
    _v("Rueil-Malmaison", "Hauts-de-Seine", "92", "92500",
       "Villas de Buzenval, maisons de caractère et résidences : votre couvreur à Rueil-Malmaison.",
       "Ville de l'impératrice Joséphine et de son château de Malmaison, Rueil-Malmaison mêle quartiers résidentiels recherchés comme Buzenval ou la Malmaison, villas des bords de Seine et nombreuses copropriétés. Une grande diversité de toitures, de la tuile à l'ardoise et au zinc.",
       "Nous accompagnons les propriétaires et les syndics de Rueil-Malmaison dans la rénovation, l'isolation et l'entretien de leurs toitures.",
       ["Nanterre", "Suresnes", "Garches", "Bougival", "Chatou"]),
    _v("Meudon", "Hauts-de-Seine", "92", "92190",
       "Villas de Bellevue, maisons en meulière et résidences : votre couvreur à Meudon.",
       "Entre la forêt de Meudon et les coteaux de Seine, Meudon offre des quartiers résidentiels prisés comme Bellevue ou Meudon-sur-Seine, avec leurs villas, leurs maisons en meulière et de nombreuses résidences. Les toitures anciennes y sont nombreuses.",
       "Rénovation de couverture, isolation des combles, lucarnes et fenêtres de toit : nous intervenons pour les particuliers et les copropriétés de Meudon.",
       ["Sèvres", "Issy-les-Moulineaux", "Clamart", "Chaville", "Vélizy-Villacoublay"]),
]

def ville(v):
    url = f"/{v['slug']}/"
    name = v["name"]
    trail = [("/", "Accueil"), ("/zones-intervention/", "Zones d'intervention"), (url, f"Couvreur {name}")]
    faq = [
        (f"Intervenez-vous à {name} ?",
         f"Oui. Depuis notre siège de Courtry, nos équipes interviennent à {name} ({v['num']}) et dans les communes voisines : {', '.join(v['voisines'][:4])}. Le déplacement et le devis sont gratuits."),
        (f"Faut-il une autorisation pour refaire sa toiture à {name} ?",
         f"Si les travaux modifient l'aspect extérieur (matériau, couleur, fenêtres de toit), une déclaration préalable doit généralement être déposée en mairie de {name}. Dans un secteur protégé, l'avis de l'Architecte des Bâtiments de France peut être requis. Nous pouvons gérer ces démarches pour vous, du dossier au dépôt en mairie."),
        ("Quels travaux réalisez-vous ?",
         "Rénovation et remplacement de toiture, isolation des combles (entreprise RGE), fenêtres de toit VELUX et lucarnes, toiture de maison neuve, couverture zinc et bardage pour maisons d'architecte, travaux pour copropriétés et syndics, nettoyage, charpente et zinguerie."),
    ]
    svc = {"@context": "https://schema.org", "@type": "Service", "name": f"Couvreur à {name}",
           "serviceType": "Couverture, charpente et zinguerie", "url": SITE + url,
           "provider": {"@id": SITE + "/#entreprise"},
           "areaServed": {"@type": "City", "name": name,
                          "containedInPlace": {"@type": "AdministrativeArea", "name": v["dept"]}}}
    lds = [org_ld(), crumbs_ld(trail), svc, faq_ld(faq)]
    html = head(f"Couvreur {name} ({v['num']}) : rénovation, isolation | JMC",
                f"Couvreur à {name} depuis 1985 : rénovation, isolation RGE, toiture zinc, maison neuve, nettoyage. QUALIBAT. Devis gratuit ☎ {BIZ['phone']}.",
                url, lds)
    html += header(url)
    html += page_hero(trail, f"{v['dept']} ({v['num']}) · {v['cp']}", f"Couvreur à {name}", v["lead"])
    paras = "".join(f"<p>{t}</p>" for t in v["texte"])
    quartiers = (f"<h3>Quartiers où nous intervenons</h3><p>{', '.join(v['quartiers'])}.</p>" if v["quartiers"] else "")
    html += f"""
<section><div class="wrap split">
  <article class="prose">
    <h2>Les toitures de {name}</h2>
    {paras}
    <h2>Nos services de couverture à {name}</h2>
    <ul class="checks">
      <li><a href="/renovation-toiture/"><strong>Rénovation et remplacement de toiture</strong></a> : réfection complète, de la charpente aux gouttières.</li>
      <li><a href="/isolation-toiture/"><strong>Isolation de toiture</strong></a> par l'extérieur, <a href="/isolation-rampants/">sous rampants</a> ou <a href="/isolation-combles-perdus/">combles perdus</a>, par une entreprise RGE.</li>
      <li><a href="/couverture-zinc-bardage/"><strong>Couverture zinc et bardage</strong></a> pour maisons d'architecte, extensions et surélévations.</li>
      <li><a href="/toiture-maison-neuve/"><strong>Toiture de maison neuve</strong></a> : charpente, couverture et zinguerie de votre construction.</li>
      <li><a href="/fenetre-de-toit-velux-lucarnes/"><strong>Fenêtres de toit VELUX et lucarnes</strong></a> : remplacement, création et restauration.</li>
      <li><a href="/couvreur-copropriete-syndic/"><strong>Copropriétés et syndics</strong></a> : réfection, réparation, isolation des combles.</li>
      <li><a href="/nettoyage-toiture/"><strong>Nettoyage et démoussage</strong></a> avec traitement anti-mousse et hydrofuge.</li>
      <li><a href="/charpente/">Charpente</a> et <a href="/zinguerie/">zinguerie</a> : gouttières, chéneaux, lucarnes, habillages.</li>
    </ul>
    {photo("mansarde")}
    {quartiers}
    <h3>Communes voisines</h3>
    <p>Nous intervenons aussi à {', '.join(v['voisines'])} et dans toute l'<a href="/zones-intervention/">Île-de-France</a>.</p>
  </article>
  {aside(f"Votre couvreur à {name}")}
</div></section>
"""
    html += faq_html(faq, f"Questions fréquentes – couvreur à {name}")
    html += cta_band(f"Un projet de toiture à {name} ?", "Visite sur place et devis détaillé gratuits, sans engagement.")
    html += footer()
    write(url, html)


VILLES += [
    _v("Chelles", "Seine-et-Marne", "77", "77500",
       "Pavillons, maisons en meulière et résidences : votre couvreur à Chelles, à deux pas de notre siège de Courtry.",
       "Voisine directe de Courtry, Chelles est l'une des plus grandes villes de Seine-et-Marne. Pavillons des années 1930 aux années 1980, maisons en meulière, maisons de ville et copropriétés : nous connaissons parfaitement ses toitures, pour y intervenir depuis 1985.",
       "Notre proximité est un atout : visites et devis rapides, suivi de chantier facilité et une équipe SAV toute proche. Rénovation, isolation, nettoyage, fenêtres de toit et zinguerie : nous prenons en charge tous vos travaux de toiture à Chelles.",
       ["Courtry", "Brou-sur-Chantereine", "Vaires-sur-Marne", "Montfermeil", "Gagny", "Le Pin"]),
    _v("Le Raincy", "Seine-Saint-Denis", "93", "93340",
       "Villas, maisons bourgeoises et demeures de caractère : votre couvreur au Raincy, à quelques minutes de Courtry.",
       "Commune résidentielle réputée pour ses villas et ses maisons bourgeoises entourées de jardins, Le Raincy abrite aussi l'église Notre-Dame construite par Auguste Perret. Ses toitures anciennes, en tuiles, en ardoise ou en zinc, demandent un savoir-faire traditionnel.",
       "Tout proches, nous intervenons au Raincy pour la rénovation complète de toitures, l'isolation, la restauration de lucarnes et de zinguerie, ainsi que pour les copropriétés de la commune.",
       ["Villemomble", "Gagny", "Montfermeil", "Clichy-sous-Bois", "Livry-Gargan"]),
]

DEPTS_PAGES = [
    {"num": "77", "name": "Seine-et-Marne", "slug": "couvreur-seine-et-marne-77", "art": "en",
     "lead": "Notre siège est à Courtry : la Seine-et-Marne est notre territoire depuis 1985. Rénovation, isolation, maisons neuves et nettoyage de toiture, de Chelles à Fontainebleau.",
     "texte": ["Plus grand département d'Île-de-France, la Seine-et-Marne réunit des réalités très différentes : pavillons et maisons en meulière de l'ouest du département, villes nouvelles de Marne-la-Vallée aux nombreuses maisons récentes, bourgs anciens et belles propriétés du sud autour de Fontainebleau et de Barbizon.",
               "Basés à Courtry, nous intervenons rapidement dans tout le département avec nos équipes et notre flotte de véhicules : rénovation et isolation de toitures anciennes, toitures de maisons neuves dans les nouveaux quartiers, nettoyage et démoussage des toitures des années 1990-2000, travaux pour les copropriétés."],
     "autres": ["Meaux", "Melun", "Torcy", "Pontault-Combault", "Roissy-en-Brie", "Claye-Souilly", "Mitry-Mory", "Villeparisis", "Vaires-sur-Marne", "Serris", "Montévrain", "Gretz-Armainvilliers", "Lésigny", "Ferrières-en-Brie", "Bois-le-Roi", "Samois-sur-Seine", "Avon", "Coupvray"]},
    {"num": "94", "name": "Val-de-Marne", "slug": "couvreur-val-de-marne-94", "art": "dans le",
     "lead": "Maisons bourgeoises des bords de Marne, villas en meulière et copropriétés : votre couvreur dans le Val-de-Marne, de Saint-Maur-des-Fossés à Nogent-sur-Marne.",
     "texte": ["Le Val-de-Marne concentre certaines des plus belles communes résidentielles de l'est parisien : Saint-Maur-des-Fossés et La Varenne, Nogent-sur-Marne, Le Perreux-sur-Marne, Vincennes, Saint-Mandé, Bry-sur-Marne. Villas Belle Époque, maisons en meulière et immeubles de caractère y portent des toitures riches et complexes.",
               "Ardoise, tuile plate, brisis et lucarnes en zinc, chéneaux et ornements : nous rénovons ces toitures dans le respect de leur architecture, avec une isolation performante et une zinguerie neuve. Nous intervenons aussi pour les syndics des nombreuses copropriétés du département."],
     "autres": ["Vincennes", "Saint-Mandé", "Bry-sur-Marne", "Joinville-le-Pont", "Champigny-sur-Marne", "Le Plessis-Trévise", "Chennevières-sur-Marne", "Fontenay-sous-Bois", "Maisons-Alfort", "Créteil", "Charenton-le-Pont", "Villiers-sur-Marne"]},
    {"num": "78", "name": "Yvelines", "slug": "couvreur-yvelines-78", "art": "dans les",
     "lead": "Hôtels particuliers de Versailles, villas du Vésinet et de Saint-Germain-en-Laye : votre couvreur dans les Yvelines pour des toitures d'exception.",
     "texte": ["Les Yvelines abritent un patrimoine résidentiel remarquable : Versailles et ses hôtels particuliers, la ville-parc du Vésinet, Saint-Germain-en-Laye, Maisons-Laffitte, Chatou, Croissy-sur-Seine ou Louveciennes. Une grande partie de ces communes est protégée, et les travaux de toiture y relèvent souvent de l'Architecte des Bâtiments de France.",
               "Couvreurs-zingueurs expérimentés, nous intervenons sur ces toitures exigeantes : ardoise, tuile plate, combles mansardés, lucarnes et zinguerie fine, rénovation et isolation, sans oublier les maisons d'architecte en zinc et les copropriétés."],
     "autres": ["La Celle-Saint-Cloud", "L'Étang-la-Ville", "Chambourcy", "Le Pecq", "Montesson", "Viroflay", "Rambouillet", "Poissy", "Saint-Nom-la-Bretèche", "Le Port-Marly", "Mareil-Marly", "Bailly"]},
    {"num": "92", "name": "Hauts-de-Seine", "slug": "couvreur-hauts-de-seine-92", "art": "dans les",
     "lead": "Hôtels particuliers de Neuilly, villas de Saint-Cloud et Ville-d'Avray, immeubles en zinc : votre couvreur-zingueur dans les Hauts-de-Seine.",
     "texte": ["Des immeubles haussmanniens de Neuilly-sur-Seine aux villas modernistes de Boulogne-Billancourt, des coteaux de Saint-Cloud aux propriétés de Marnes-la-Coquette, de Vaucresson ou de Ville-d'Avray, les Hauts-de-Seine offrent une grande variété de toitures, souvent en zinc et en ardoise.",
               "Nous y intervenons pour les particuliers comme pour les syndics de copropriété : réfection de couverture zinc et ardoise, isolation des combles, fenêtres de toit VELUX, restauration de lucarnes, bardage zinc pour les extensions et les maisons d'architecte."],
     "autres": ["Sèvres", "Chaville", "Bourg-la-Reine", "Levallois-Perret", "Issy-les-Moulineaux", "Antony", "Suresnes", "Puteaux", "Courbevoie", "Clamart", "Le Plessis-Robinson", "Châtenay-Malabry"]},
    {"num": "93", "name": "Seine-Saint-Denis", "slug": "couvreur-seine-saint-denis-93", "art": "en",
     "lead": "Villas du Raincy, pavillons de Villemomble et de Gagny, copropriétés et équipements publics : votre couvreur en Seine-Saint-Denis, à la porte de notre siège.",
     "texte": ["Courtry est à la frontière de la Seine-Saint-Denis : nous y intervenons depuis 1985, pour les particuliers, les copropriétés et les collectivités, comme les groupes scolaires de Montfermeil. Villas du Raincy, maisons bourgeoises de Villemomble, pavillons de Gagny ou de Livry-Gargan : nous connaissons chaque type de toiture du département.",
               "Notre proximité nous permet des visites rapides, un suivi de chantier attentif et un SAV réactif. Rénovation, isolation des combles, nettoyage, fenêtres de toit et zinguerie : tous vos travaux de toiture avec un seul interlocuteur."],
     "autres": ["Villemomble", "Gagny", "Montfermeil", "Coubron", "Vaujours", "Livry-Gargan", "Clichy-sous-Bois", "Neuilly-Plaisance", "Neuilly-sur-Marne", "Noisy-le-Grand", "Les Pavillons-sous-Bois", "Rosny-sous-Bois"]},
    {"num": "75", "name": "Paris", "slug": "couvreur-paris", "art": "à",
     "lead": "Toitures en zinc et en ardoise, combles mansardés, lucarnes et balcons : un couvreur-zingueur à Paris pour les copropriétés, les syndics et les propriétaires.",
     "texte": ["Les toits de Paris sont un patrimoine à part : couvertures en zinc, brisis d'ardoise, lucarnes, chiens-assis, terrassons et balcons en plomb. Le savoir-faire des couvreurs-zingueurs parisiens est d'ailleurs inscrit au patrimoine culturel immatériel de l'UNESCO depuis 2024.",
               "Nous intervenons à Paris depuis de nombreuses années, rue de la Croix-Nivert, rue Raffet pour Nexity ou boulevard de Sébastopol : réfection de couvertures zinc, charpente, isolation des combles, fenêtres de toit, restauration de lucarnes et de balcons, en lien avec les syndics et les architectes."],
     "autres": ["Paris 7e", "Paris 8e", "Paris 11e", "Paris 12e", "Paris 15e", "Paris 16e", "Paris 17e", "Paris 20e"]},
]


def dept_page(d):
    url = f"/{d['slug']}/"
    label = f"{d['name']} ({d['num']})" if d["num"] != "75" else "Paris"
    trail = [("/", "Accueil"), ("/zones-intervention/", "Zones d'intervention"), (url, f"Couvreur {label}")]
    villes_dept = [v for v in VILLES if v["num"] == d["num"]]
    faq = [
        (f"Intervenez-vous partout {d['art']} {d['name']} ?",
         (f"Oui. Depuis notre siège de Courtry, nos équipes interviennent dans tous les arrondissements de Paris" if d["num"] == "75" else f"Oui. Depuis notre siège de Courtry, nos équipes interviennent dans tout le département ({label})") + ", pour les particuliers, les copropriétés et les professionnels. Le déplacement et le devis sont gratuits."),
        ("Quels travaux de toiture réalisez-vous ?",
         "Rénovation et remplacement de toiture, isolation des combles et de la toiture (entreprise RGE), toiture de maison neuve, couverture zinc et bardage, fenêtres de toit VELUX et lucarnes, nettoyage et démoussage, charpente et zinguerie, travaux pour copropriétés."),
        ("Quelles garanties proposez-vous ?",
         "Nos travaux sont couverts par la garantie décennale. Nous sommes certifiés QUALIBAT et RGE, et une équipe SAV et qualité interne assure le suivi après le chantier."),
    ]
    svc = {"@context": "https://schema.org", "@type": "Service", "name": f"Couvreur {label}",
           "serviceType": "Couverture, charpente et zinguerie", "url": SITE + url,
           "provider": {"@id": SITE + "/#entreprise"},
           "areaServed": {"@type": "AdministrativeArea", "name": d["name"]}}
    lds = [org_ld(), crumbs_ld(trail), svc, faq_ld(faq)]
    title = (f"Couvreur {d['num']} – {d['name']} : rénovation, isolation | JMC" if d["num"] != "75"
             else "Couvreur zingueur Paris : toiture zinc, ardoise, copropriété | JMC")
    html = head(title,
                f"Couvreur {d['art']} {d['name']} depuis 1985 : rénovation, isolation RGE, zinc, VELUX, copropriétés. Noté 4,9/5 sur Google. Devis gratuit ☎ {BIZ['phone']}.",
                url, lds)
    html += header(url)
    html += page_hero(trail, f"{d['name']} · {d['num']}", f"Couvreur {d['art']} {d['name']}" + (f" ({d['num']})" if d["num"] != "75" else ""), d["lead"])
    links = "".join(f'<a href="/{v["slug"]}/">Couvreur {v["name"]}</a>' for v in villes_dept)
    paras = "".join(f"<p>{t}</p>" for t in d["texte"])
    html += f"""
<section><div class="wrap split">
  <article class="prose">
    <h2>Vos toitures {d['art']} {d['name']}</h2>
    {paras}
    {('<h2>Nos pages par ville</h2><div class="city-links">' + links + '</div>') if links else ''}
    <h2>Nos services de couverture {d['art']} {d['name']}</h2>
    <ul class="checks">
      <li><a href="/renovation-toiture/"><strong>Rénovation et remplacement de toiture</strong></a></li>
      <li><a href="/isolation-toiture/"><strong>Isolation de toiture</strong></a>, <a href="/isolation-rampants/">des rampants</a> et <a href="/isolation-combles-perdus/">des combles perdus</a> (entreprise RGE)</li>
      <li><a href="/fenetre-de-toit-velux-lucarnes/"><strong>Pose et remplacement de VELUX</strong>, lucarnes</a></li>
      <li><a href="/couverture-zinc-bardage/"><strong>Couverture zinc et bardage</strong></a> pour maisons d'architecte</li>
      <li><a href="/couvreur-copropriete-syndic/"><strong>Travaux pour copropriétés et syndics</strong></a></li>
      <li><a href="/toiture-maison-neuve/"><strong>Toiture de maison neuve</strong></a></li>
      <li><a href="/nettoyage-toiture/"><strong>Nettoyage et démoussage</strong></a></li>
    </ul>
    {photo("drone")}
    <h3>Autres communes où nous intervenons</h3>
    <p>{', '.join(d['autres'])}, et toutes les communes {('de Paris' if d['num'] == '75' else 'du département')}.</p>
  </article>
  {aside(f"Votre couvreur {d['art']} {d['name']}")}
</div></section>
"""
    html += faq_html(faq, f"Questions fréquentes – couvreur {d['art']} {d['name']}")
    html += cta_band(f"Un projet de toiture {d['art']} {d['name']} ?", "Visite sur place et devis détaillé gratuits, sans engagement.")
    html += footer()
    write(url, html)


def depts():
    for d in DEPTS_PAGES:
        dept_page(d)



def city_groups():
    order = [("94", "Val-de-Marne"), ("78", "Yvelines"), ("92", "Hauts-de-Seine"), ("77", "Seine-et-Marne"), ("93", "Seine-Saint-Denis")]
    out = ""
    for num, dept in order:
        links = "".join(f'<a href="/{v["slug"]}/">Couvreur {v["name"]}</a>' for v in VILLES if v["num"] == num)
        dslug = next(d["slug"] for d in DEPTS_PAGES if d["num"] == num)
        if links:
            out += (f'<h3 class="city-dept"><a href="/{dslug}/">Couvreur {dept} ({num})</a></h3>'
                    f'<div class="city-links">{links}</div>')
    return out


def villes():
    for v in VILLES:
        ville(v)


def copropriete():
    trail = [("/", "Accueil"), ("/couvreur-copropriete-syndic/", "Copropriétés et syndics")]
    faq = [
        ("Travaillez-vous avec les syndics professionnels et bénévoles ?",
         "Oui. Nous intervenons pour des syndics professionnels, des syndics bénévoles et des conseils syndicaux, sur des copropriétés de toutes tailles, du petit immeuble à la résidence de plusieurs bâtiments."),
        ("Fournissez-vous des devis pour l'assemblée générale ?",
         "Oui. Après visite et diagnostic, nous remettons un devis détaillé poste par poste, accompagné d'un descriptif des travaux et, si besoin, de plusieurs variantes, pour faciliter le vote en assemblée générale."),
        ("Quelles aides pour isoler les combles d'une copropriété ?",
         "Entreprise RGE, nous permettons à la copropriété de prétendre aux aides à la rénovation énergétique, comme les primes CEE ou MaPrimeRénov' Copropriété lorsque les travaux s'inscrivent dans un projet de rénovation globale. L'éligibilité dépend des conditions en vigueur et du projet."),
        ("Comment se passent les travaux dans un immeuble habité ?",
         "Nous organisons le chantier en site occupé : information des résidents, protection des parties communes, sécurisation des accès, gestion des déchets et respect des horaires. Un interlocuteur unique assure le suivi avec le syndic."),
        ("Pouvez-vous intervenir pour une réparation ponctuelle ?",
         "Oui : remplacement de tuiles ou d'ardoises, reprise de solins, chéneaux, descentes, fenêtres de toit ou lucarnes. Nous établissons un constat et un devis rapidement pour le syndic."),
        ("Pouvez-vous aider à préparer le plan pluriannuel de travaux ?",
         "Nous réalisons un état des lieux complet de la toiture (couverture, charpente, zinguerie, isolation) et chiffrons les travaux à prévoir, des éléments utiles au diagnostic et au plan pluriannuel de travaux (PPT) désormais obligatoires pour les copropriétés."),
    ]
    desc = "Travaux de toiture pour copropriétés et syndics : réfection, réparation, isolation des combles, fenêtres de toit VELUX, lucarnes et zinguerie."
    svc = service_ld("Couverture et isolation pour copropriétés", "/couvreur-copropriete-syndic/", desc)
    svc["audience"] = {"@type": "BusinessAudience", "audienceType": "Syndics de copropriété et conseils syndicaux"}
    lds = [org_ld(), crumbs_ld(trail), svc, faq_ld(faq)]
    html = head("Couvreur copropriété et syndic en Île-de-France : toiture, isolation | JMC",
                "Couvreur pour syndics et copropriétés : réfection et réparation de toiture, isolation des combles RGE, fenêtres de toit VELUX, lucarnes, zinguerie. Devis pour AG.",
                "/couvreur-copropriete-syndic/", lds)
    html += header("/couvreur-copropriete-syndic/")
    html += page_hero(trail, "Copropriétés · Syndics", "Couvreur pour copropriétés et syndics en Île-de-France",
                      "Réfection et réparation de toiture, isolation des combles, fenêtres de toit VELUX et lucarnes : une entreprise structurée, certifiée QUALIBAT et RGE, qui parle le langage des syndics et des conseils syndicaux.")
    html += f"""
<section><div class="wrap split">
  <article class="prose">
    {photo("drone", eager=True)}
    <h2>Un partenaire fiable pour les syndics</h2>
    <p>Depuis 1985, JMC intervient sur des immeubles, des résidences et des bâtiments publics en Île-de-France : immeubles parisiens rue de la Croix-Nivert ou boulevard de Sébastopol, programmes pour des promoteurs, écoles et équipements communaux. Nous savons ce qu'attend un gestionnaire de copropriété : des devis clairs, des délais tenus, un chantier propre et un interlocuteur joignable.</p>

    <h2>Travaux de toiture en copropriété</h2>
    <h3>Réfection et réparation de couverture</h3>
    <p>Réfection complète de toiture d'immeuble en tuiles, ardoise ou zinc, réparations ponctuelles, remplacement de tuiles et d'ardoises, reprise de faîtages, de solins et d'abergements de cheminées.</p>
    <h3>Isolation des combles</h3>
    <p><a href="/isolation-combles-perdus/">Isolation des combles perdus</a> par soufflage ou déroulage, <a href="/isolation-rampants/">isolation sous rampants</a> des lots aménagés sous les toits, isolation par l'extérieur lors d'une réfection : des travaux RGE qui améliorent le DPE collectif et le confort des derniers étages. Voir aussi notre page <a href="/isolation-toiture/">isolation de toiture</a>.</p>
    <h3>Fenêtres de toit VELUX</h3>
    <p>Remplacement de fenêtres de toit VELUX et d'autres marques, souvent dans les dimensions existantes, création de fenêtres de toit pour les lots sous combles, raccords d'étanchéité, volets roulants et stores. Détails sur notre page <a href="/fenetre-de-toit-velux-lucarnes/">fenêtres de toit et lucarnes</a>.</p>
    <h3>Lucarnes</h3>
    <p>Restauration et habillage zinc des lucarnes existantes, réfection des jouées et des couvertures de lucarnes, création de lucarnes lorsque le règlement de copropriété et l'urbanisme le permettent.</p>
    <h3>Zinguerie et eaux pluviales</h3>
    <p>Chéneaux, gouttières, descentes, noues, terrassons et brisis en zinc : nous reprenons l'ensemble de la <a href="/zinguerie/">zinguerie</a> de l'immeuble.</p>

    <h2>Notre méthode avec le syndic</h2>
    <ol class="steps">
      <li><strong>Visite et état des lieux</strong><br>Inspection de la toiture, des combles et de la zinguerie, photos et constat.</li>
      <li><strong>Devis détaillé pour l'assemblée générale</strong><br>Descriptif, quantités, variantes éventuelles et planning prévisionnel.</li>
      <li><strong>Préparation du chantier</strong><br>Démarches de voirie et d'urbanisme, échafaudage, information des résidents.</li>
      <li><strong>Travaux et suivi</strong><br>Un interlocuteur unique, des points d'avancement réguliers avec le syndic.</li>
      <li><strong>Réception</strong><br>Réception des travaux, photos, attestations et garanties pour le dossier de la copropriété.</li>
      <li><strong>SAV et suivi</strong><br>Notre équipe SAV et qualité interne reste l'interlocutrice du syndic après le chantier.</li>
    </ol>

    <h2>Loi Climat : anticiper les travaux</h2>
    <p>Diagnostic de performance énergétique collectif et plan pluriannuel de travaux (PPT) s'imposent désormais aux copropriétés. La toiture et l'isolation des combles y figurent presque toujours parmi les postes prioritaires : nous vous aidons à les chiffrer et à les planifier.</p>
  </article>
  {aside("Syndics : pourquoi JMC ?")}
</div></section>
"""
    html += faq_html(faq, "Questions fréquentes des syndics et conseils syndicaux")
    html += cta_band("Un immeuble à faire diagnostiquer ?", "Visite, état des lieux et devis pour votre assemblée générale, gratuits.")
    html += footer()
    write("/couvreur-copropriete-syndic/", html)


def fenetres():
    trail = [("/", "Accueil"), ("/fenetre-de-toit-velux-lucarnes/", "Fenêtres de toit et lucarnes")]
    faq = [
        ("Combien de temps pour remplacer une fenêtre de toit VELUX ?",
         "Un remplacement dans les mêmes dimensions se fait généralement en une journée, sans reprendre la couverture autour. Un changement de taille ou une création demande davantage de travail sur la charpente et la couverture."),
        ("Faut-il une autorisation pour créer une fenêtre de toit ou une lucarne ?",
         "Oui en général : la création d'une fenêtre de toit ou d'une lucarne modifie l'aspect extérieur et nécessite une déclaration préalable en mairie, voire l'accord de l'Architecte des Bâtiments de France en secteur protégé. En copropriété, l'accord de l'assemblée générale est aussi nécessaire."),
        ("Peut-on motoriser une fenêtre de toit existante ?",
         "Selon le modèle, il est possible d'ajouter une motorisation, un volet roulant solaire ou un store. Souvent, le remplacement par une fenêtre neuve plus performante et motorisée est la meilleure option."),
        ("Quelle différence entre lucarne et fenêtre de toit ?",
         "La fenêtre de toit s'intègre dans le plan de la toiture. La lucarne est un petit ouvrage maçonné ou en charpente qui dépasse du toit, avec sa propre couverture : elle apporte de la hauteur sous plafond et du caractère, mais demande plus de travaux."),
    ]
    desc = "Pose, remplacement et création de fenêtres de toit VELUX, restauration et création de lucarnes, habillage zinc, pour particuliers et copropriétés."
    lds = [org_ld(), crumbs_ld(trail), service_ld("Fenêtres de toit et lucarnes", "/fenetre-de-toit-velux-lucarnes/", desc), faq_ld(faq)]
    html = head("Pose et remplacement de VELUX, lucarnes en Île-de-France | JMC",
                "Remplacement et pose de fenêtres de toit VELUX, création et rénovation de lucarnes en zinc ou ardoise en Île-de-France. Particuliers et copropriétés. Devis gratuit.",
                "/fenetre-de-toit-velux-lucarnes/", lds)
    html += header("/fenetre-de-toit-velux-lucarnes/")
    html += page_hero(trail, "Fenêtres de toit · Lucarnes", "Pose et remplacement de VELUX, fenêtres de toit et lucarnes",
                      "Plus de lumière sous les toits, une isolation renforcée, des combles enfin habitables : nos couvreurs posent et remplacent vos fenêtres de toit et créent ou restaurent vos lucarnes.")
    html += f"""
<section><div class="wrap split">
  <article class="prose">
    {photo("mansarde", eager=True)}
    <h2>Pose et remplacement de VELUX</h2>
    <h3>Remplacement de VELUX et de fenêtres de toit</h3>
    <p>Une fenêtre de toit de plus de 20 ans laisse passer l'air, la chaleur et parfois l'eau. Nous remplaçons vos fenêtres VELUX ou d'autres marques, le plus souvent dans les dimensions existantes, avec un raccord d'étanchéité neuf et un isolant périphérique : un gain immédiat de confort.</p>
    <h3>Pose de VELUX et création de fenêtre de toit</h3>
    <p>Pour éclairer des combles aménagés, nous ouvrons la toiture, réalisons le chevêtre dans la charpente, posons la fenêtre et refaisons la couverture autour dans les règles de l'art.</p>
    <h3>Options de confort</h3>
    <ul class="checks">
      <li>Fenêtres à rotation ou à projection, verrières d'angle</li>
      <li>Motorisation et capteur de pluie</li>
      <li>Volets roulants solaires et stores occultants</li>
      <li>Vitrages isolants et phoniques</li>
    </ul>

    <h2>Lucarnes</h2>
    <h3>Restauration de lucarnes anciennes</h3>
    <p>Lucarnes en ardoise, en zinc ou en bois : nous reprenons leur couverture, leurs jouées, leurs habillages et leur zinguerie, en respectant le style de la maison ou de l'immeuble, comme sur cette maison bourgeoise aux trois lucarnes habillées de zinc.</p>
    <h3>Création de lucarnes</h3>
    <p>Lucarne jacobine, capucine, rampante ou <a href="/chien-assis-lucarne/">chien-assis</a> : nous créons la lucarne adaptée à votre toiture et à votre projet d'aménagement, de la charpente à la couverture et à la <a href="/couverture-zinc-bardage/">finition zinc</a>.</p>
    {photo("drone")}

    <h2>Pour les particuliers comme pour les copropriétés</h2>
    <p>Nous intervenons dans les maisons individuelles comme dans les immeubles, en lien avec le <a href="/couvreur-copropriete-syndic/">syndic de copropriété</a> pour les fenêtres de toit et les lucarnes des lots sous combles. Ces travaux se combinent idéalement avec une <a href="/isolation-toiture/">isolation de toiture</a> ou une <a href="/renovation-toiture/">rénovation complète</a>.</p>
    {reviews_block(['richard', 'marcelino'], "Ils nous ont confié leurs VELUX")}
    <p class="small">VELUX est une marque déposée de son propriétaire. JMC pose et remplace les fenêtres de toit de cette marque et d'autres fabricants.</p>
  </article>
  {aside("Fenêtres de toit et lucarnes")}
</div></section>
"""
    html += faq_html(faq, "Questions fréquentes sur les fenêtres de toit et les lucarnes")
    html += cta_band("Plus de lumière sous vos toits ?", "Devis gratuit pour vos fenêtres de toit et lucarnes.")
    html += footer()
    write("/fenetre-de-toit-velux-lucarnes/", html)


def promotion():
    trail = [("/", "Accueil"), ("/couvreur-promotion-immobiliere/", "Promotion immobilière")]
    faq = [
        ("Quels types de programmes réalisez-vous ?",
         "Logements collectifs, maisons individuelles groupées, résidences, équipements publics et scolaires : nous réalisons les lots charpente, couverture et zinguerie de programmes neufs et de réhabilitations en Île-de-France."),
        ("Quels documents fournissez-vous ?",
         "Attestations d'assurance décennale et de responsabilité civile, qualifications QUALIBAT et RGE, documents de sécurité et de chantier, puis dossier des ouvrages exécutés à la réception, selon les exigences du maître d'ouvrage."),
        ("Pouvez-vous tenir des plannings serrés ?",
         "Oui. Nos équipes, notre atelier et notre flotte de véhicules sont dimensionnés pour la promotion immobilière : nous mobilisons les compagnons nécessaires pour tenir les jalons de mise hors d'eau et de livraison."),
        ("Un particulier peut-il bénéficier de cette organisation ?",
         "Oui, c'est tout l'intérêt : les particuliers profitent de la même structure, des mêmes équipes et des mêmes méthodes que nos clients promoteurs, avec un interlocuteur dédié du devis à la réception."),
    ]
    desc = "Lots charpente, couverture et zinguerie pour promoteurs immobiliers, constructeurs et maîtres d'œuvre en Île-de-France."
    lds = [org_ld(), crumbs_ld(trail), service_ld("Couverture pour la promotion immobilière", "/couvreur-promotion-immobiliere/", desc), faq_ld(faq)]
    html = head("Couvreur pour la promotion immobilière en Île-de-France | JMC",
                "Charpente, couverture et zinguerie pour promoteurs, constructeurs et maîtres d'œuvre en Île-de-France. Équipes dédiées, plannings tenus, QUALIBAT & RGE.",
                "/couvreur-promotion-immobiliere/", lds)
    html += header("/couvreur-promotion-immobiliere/")
    html += page_hero(trail, "Promotion immobilière", "Couvreur de la promotion immobilière, au service des promoteurs et des particuliers",
                      "Depuis 1985, promoteurs, architectes et collectivités nous confient la charpente, la couverture et la zinguerie de leurs programmes. Cette structure et ces équipes sont aussi à la disposition des particuliers.")
    html += f"""
<section><div class="wrap split">
  <article class="prose">
    {photo("depot", eager=True)}
    <h2>Une structure taillée pour la promotion immobilière</h2>
    <p>Travailler pour la promotion immobilière impose une organisation que peu d'entreprises de couverture possèdent : des équipes nombreuses et qualifiées, un atelier de façonnage, une flotte de véhicules, un encadrement de chantier et une capacité à mener plusieurs opérations en parallèle. C'est la structure que JMC a construite depuis 40 ans à Courtry.</p>
    <ul class="checks">
      <li><strong>Des équipes dédiées</strong> : couvreurs, charpentiers et zingueurs salariés de l'entreprise</li>
      <li><strong>Un atelier</strong> pour façonner la zinguerie et préparer les chantiers</li>
      <li><strong>Une flotte de véhicules</strong> pour intervenir partout en Île-de-France</li>
      <li><strong>Un encadrement de chantier</strong> et un interlocuteur unique pour le maître d'ouvrage</li>
      <li><strong>Des garanties solides</strong> : décennale, responsabilité civile, QUALIBAT, RGE</li>
      <li><strong>Une équipe SAV et qualité interne</strong> pour le contrôle avant réception et la levée des réserves</li>
    </ul>

    <h2>Nos prestations pour les promoteurs</h2>
    <ul class="checks">
      <li>Lots charpente, couverture et zinguerie de logements collectifs et de maisons individuelles groupées</li>
      <li>Couvertures tuiles, ardoise, zinc et bac acier, toitures-terrasses</li>
      <li>Bardages zinc, habillages, lucarnes et fenêtres de toit</li>
      <li>Réhabilitation d'immeubles anciens : charpente, couverture, balcons et ouvrages en plomb ou en zinc</li>
      <li>Respect des plannings de mise hors d'eau, des exigences des bureaux de contrôle et des levées de réserves</li>
    </ul>

    <h2>Ils nous font confiance</h2>
    <p>Bouygues Immobilier, Kaufman &amp; Broad, Nexity, Archicrea, des architectes et des collectivités d'Île-de-France : rue de la Croix-Nivert et rue Raffet à Paris, boulevard de Sébastopol, groupes scolaires de Montfermeil… Voir <a href="/nos-references/">nos références</a>.</p>

    <h2>Et pour les particuliers : la même structure</h2>
    <p>Les particuliers bénéficient exactement des mêmes équipes et des mêmes méthodes : diagnostic précis, devis détaillé, planning tenu, chantier encadré et propre. Que vous fassiez <a href="/toiture-maison-neuve/">construire votre maison</a>, <a href="/renovation-toiture/">rénover votre toiture</a>, <a href="/isolation-toiture/">l'isoler</a> ou réaliser une <a href="/couverture-zinc-bardage/">maison d'architecte en zinc</a>, vous êtes accompagné par une entreprise capable de mener des chantiers d'envergure.</p>
  </article>
  {aside("Promoteurs, constructeurs, maîtres d'œuvre")}
</div></section>
"""
    html += faq_html(faq, "Questions fréquentes – promotion immobilière")
    html += cta_band("Un programme à consulter ?", "Envoyez-nous votre dossier de consultation : réponse et chiffrage rapides.")
    html += footer()
    write("/couvreur-promotion-immobiliere/", html)


PROCESS = [
    ("Écoute et premier contact", "Par téléphone ou via le formulaire, vous nous décrivez votre projet. Un interlocuteur dédié vous est attribué dès le départ."),
    ("Visite technique et diagnostic", "Un professionnel inspecte la couverture, la charpente, la zinguerie et l'isolation, photos à l'appui."),
    ("Devis détaillé et conseil", "Un devis clair, poste par poste, avec nos recommandations, les variantes possibles et les aides mobilisables."),
    ("Démarches et préparation", "Nous pouvons gérer les démarches en mairie, travailler avec votre maître d'œuvre et vous recommander des prestataires compétents pour préparer au mieux les travaux, puis planifier et préparer le chantier en atelier."),
    ("Chantier sûr, propre et encadré", "Des équipes formées à la sécurité et à la propreté, un chef de chantier, une maison protégée, un chantier nettoyé chaque jour et des points d'avancement réguliers."),
    ("Contrôle qualité et réception", "Les travaux sont vérifiés par notre équipe qualité avant la réception, réalisée avec vous. Photos et attestations vous sont remises."),
    ("SAV et suivi dans la durée", "Après le chantier, notre équipe SAV interne reste votre interlocutrice pour toute question ou intervention liée à nos travaux."),
]


def process_html(n=None):
    items = "".join(f"<li><strong>{t}</strong><br>{d}</li>" for t, d in PROCESS[:n])
    return f'<ol class="steps grid g2">{items}</ol>'


def methode():
    trail = [("/", "Accueil"), ("/notre-methode-sav-qualite/", "Notre méthode, SAV et qualité")]
    faq = [
        ("Qui contacter après la fin de mon chantier ?",
         "Notre équipe SAV et qualité, interne à l'entreprise. Elle connaît votre chantier et organise le suivi avec nos équipes."),
        ("Quelles garanties couvrent mes travaux ?",
         "Après la réception, vos travaux bénéficient des garanties légales : garantie de parfait achèvement (1 an), garantie biennale de bon fonctionnement des équipements (2 ans) et garantie décennale (10 ans), couverte par notre assurance."),
        ("Comment est contrôlée la qualité des travaux ?",
         "Chaque chantier est encadré par un chef de chantier et vérifié par notre équipe qualité avant la réception : étanchéité, finitions, zinguerie, propreté. La réception se fait ensuite avec vous."),
    ]
    page = {"@context": "https://schema.org", "@type": "AboutPage", "url": SITE + "/notre-methode-sav-qualite/",
            "name": "Notre méthode, SAV et qualité", "about": {"@id": SITE + "/#entreprise"}}
    lds = [org_ld(), crumbs_ld(trail), page, faq_ld(faq)]
    html = head("Notre méthode : sécurité, propreté, SAV et qualité | JMC",
                "La méthode JMC en 7 étapes : équipes formées à la sécurité et à la propreté, contrôle qualité avant réception et équipe SAV interne dédiée.",
                "/notre-methode-sav-qualite/", lds)
    html += header("/notre-methode-sav-qualite/")
    html += page_hero(trail, "Méthode · SAV · Qualité", "Notre méthode : du premier contact au SAV, une équipe dédiée",
                      "Une toiture réussie ne s'arrête pas à la fin du chantier. Méthode éprouvée sur les chantiers de promotion immobilière, contrôle qualité avant réception et équipe SAV interne : vous êtes suivi avant, pendant et après les travaux.")
    html += f"""
<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">Notre process</span><h2>7 étapes pour un chantier maîtrisé</h2>
  <p>La même méthode pour un particulier, un syndic ou un promoteur : c'est ce qui garantit des délais tenus et un résultat durable.</p></div>
  {process_html()}
</div></section>
{secu_proprete()}

<section class="section-alt"><div class="wrap split">
  <article class="prose">
    <h2>Une équipe SAV et qualité dédiée, en interne</h2>
    <p>Chez JMC, le service après-vente n'est pas une formalité. Une <strong>équipe interne est dédiée au SAV et à la qualité</strong> : elle contrôle les chantiers avant leur réception, puis reste votre interlocutrice une fois les travaux terminés.</p>
    <ul class="checks">
      <li><strong>Contrôle avant réception</strong> : étanchéité, finitions, zinguerie, nettoyage du chantier</li>
      <li><strong>Réception avec vous</strong>, photos et attestations remises</li>
      <li><strong>Un interlocuteur SAV identifié</strong> après le chantier, au sein de l'entreprise</li>
      <li><strong>Intervention de nos propres équipes</strong> pour toute demande liée à nos travaux</li>
      <li><strong>Garanties légales</strong> : parfait achèvement, biennale et décennale</li>
    </ul>
    <h2>Démarches, maîtres d'œuvre et prestataires</h2>
    <ul class="checks">
      <li><strong>Démarches en mairie</strong> : nous pouvons préparer et déposer pour vous la déclaration préalable de travaux</li>
      <li><strong>Maîtres d'œuvre et architectes</strong> : nous travaillons régulièrement à leurs côtés et suivons leurs prescriptions</li>
      <li><strong>Prestataires compétents</strong> : nous pouvons vous recommander des professionnels de confiance pour préparer au mieux vos travaux</li>
    </ul>
    <h2>Pourquoi c'est important</h2>
    <p>Beaucoup d'entreprises disparaissent une fois le chantier payé. Notre structure, construite pour répondre aux exigences de la <a href="/couvreur-promotion-immobiliere/">promotion immobilière</a>, où chaque réserve doit être levée, nous permet d'assurer un vrai suivi dans la durée, pour les promoteurs comme pour les <a href="/toiture-maison-neuve/">particuliers</a> et les <a href="/couvreur-copropriete-syndic/">copropriétés</a>.</p>
    <p>Vous êtes déjà client et avez une demande de SAV ? <a href="/contact/">Contactez-nous</a> en choisissant « SAV – client JMC » dans le formulaire, ou appelez le <a href="tel:{BIZ['phone_intl']}">{BIZ['phone']}</a>.</p>
  </article>
  {aside("Suivi et qualité JMC")}
</div></section>
"""
    html += faq_html(faq, "Questions fréquentes sur le suivi et le SAV")
    html += cta_band()
    html += footer()
    write("/notre-methode-sav-qualite/", html)


def _guide(url, crumb, title, desc, eyebrow, h1, lead, body, faq, svc_name, cta=("Un projet ?", "Visite et devis gratuits par un couvreur-zingueur certifié QUALIBAT.")):
    trail = [("/", "Accueil"), (url, crumb)]
    lds = [org_ld(), crumbs_ld(trail), service_ld(svc_name, url, desc), faq_ld(faq)]
    html = head(title, desc, url, lds)
    html += header(url)
    html += page_hero(trail, eyebrow, h1, lead)
    html += f"""
<section><div class="wrap split">
  <article class="prose">
{body}
  </article>
  {aside()}
</div></section>
"""
    html += faq_html(faq, f"Questions fréquentes – {crumb.lower()}")
    html += cta_band(*cta)
    html += footer()
    write(url, html)


def chien_assis():
    faq = [
        ("Quelle est la différence entre un chien-assis et une lucarne ?",
         "Le chien-assis est un type de lucarne : son toit est incliné dans le sens inverse de la pente de la toiture, ce qui lui donne sa silhouette caractéristique. Dans le langage courant, on appelle souvent « chien-assis » toute lucarne qui dépasse du toit."),
        ("Faut-il une autorisation pour créer un chien-assis ?",
         "Oui. La création d'un chien-assis ou d'une lucarne modifie l'aspect extérieur : une déclaration préalable est en général nécessaire, et un permis de construire si la surface de plancher créée dépasse les seuils prévus par le code de l'urbanisme. En secteur protégé, l'avis de l'Architecte des Bâtiments de France est requis."),
        ("Quel est le prix d'un chien-assis ?",
         "Le prix dépend de la taille de la lucarne, du type choisi, des modifications de charpente, du matériau de couverture et d'habillage (zinc, ardoise, tuile) et de la menuiserie. Après visite, nous vous remettons un devis détaillé et gratuit."),
        ("Lucarne ou fenêtre de toit VELUX : que choisir ?",
         "La fenêtre de toit est plus simple et plus économique. Le chien-assis ou la lucarne crée de la hauteur sous plafond, une vraie fenêtre verticale et du cachet, mais demande davantage de travaux. Nous vous conseillons selon votre projet."),
        ("Combien de temps durent les travaux ?",
         "Selon la taille et la complexité, la création d'une lucarne prend en général de quelques jours à deux semaines, la toiture étant protégée pendant toute la durée du chantier."),
    ]
    body = f"""    {photo("drone", eager=True)}
    <h2>Chien-assis et lucarnes : de la lumière et de l'espace sous les toits</h2>
    <p>Créer un chien-assis ou une lucarne, c'est transformer des combles sombres et bas de plafond en vraies pièces à vivre : une fenêtre verticale, de la hauteur sous plafond, une vue dégagée et un cachet incomparable. Couvreurs, charpentiers et zingueurs, nos équipes réalisent l'ensemble de l'ouvrage, de l'ouverture de la toiture à l'habillage final.</p>

    <h2>Les différents types de lucarnes</h2>
    <h3>Le chien-assis</h3>
    <p>Son toit à un seul pan est incliné dans le sens inverse de la toiture. Très répandu sur les maisons de la région parisienne, il offre un maximum de hauteur et de surface vitrée.</p>
    <h3>La lucarne jacobine</h3>
    <p>Lucarne à deux pans formant un fronton triangulaire en façade. C'est la lucarne classique des maisons bourgeoises et des toitures en ardoise ou en tuile plate.</p>
    <h3>La lucarne capucine</h3>
    <p>Lucarne à trois pans, dont un pan en croupe à l'avant. Élégante et discrète, elle se fond dans les toitures traditionnelles.</p>
    <h3>La lucarne rampante</h3>
    <p>Lucarne à un seul pan, incliné dans le même sens que la toiture mais avec une pente plus faible. Idéale pour gagner de la surface habitable sur toute la longueur d'un versant.</p>
    <h3>Les lucarnes en zinc et en ardoise</h3>
    <p>Joues, toit et fronton peuvent être habillés de <a href="/couverture-zinc-bardage/">zinc</a>, d'ardoise ou de tuile. Le zinc permet des lignes nettes et contemporaines ; l'ardoise s'impose sur les toitures <a href="/toiture-mansardee-brisis-terrasson/">mansardées</a> et les maisons de caractère.</p>
    {photo("mansarde")}

    <h2>Les étapes de la création d'un chien-assis</h2>
    <ol class="steps">
      <li><strong>Visite et étude</strong><br>Choix du type de lucarne, dimensions, vérification de la charpente et des règles d'urbanisme.</li>
      <li><strong>Démarches</strong><br>Nous pouvons gérer pour vous la déclaration préalable auprès de la mairie (plans, insertion, descriptif).</li>
      <li><strong>Ouverture et charpente</strong><br>Dépose de la couverture, création du chevêtre et de l'ossature de la lucarne.</li>
      <li><strong>Couverture et habillage</strong><br>Toit de la lucarne, joues, fronton, raccords d'étanchéité en zinc ou en plomb.</li>
      <li><strong>Menuiserie et isolation</strong><br>Pose de la fenêtre et isolation de la lucarne, pour un résultat étanche et performant.</li>
    </ol>

    <h2>Restaurer une lucarne ancienne</h2>
    <p>Joues fissurées, habillage zinc percé, fronton abîmé : nous restaurons aussi les lucarnes existantes, à l'identique, notamment sur les maisons bourgeoises, en meulière et les immeubles parisiens. Découvrez aussi nos <a href="/fenetre-de-toit-velux-lucarnes/">fenêtres de toit VELUX</a>.</p>"""
    _guide("/chien-assis-lucarne/", "Chien-assis et lucarnes",
           "Chien-assis et lucarne : création, types, prix | Couvreur JMC",
           "Création de chien-assis et de lucarnes (jacobine, capucine, rampante) en zinc ou ardoise, en Île-de-France. Démarches, étapes et devis gratuit par un couvreur-charpentier.",
           "Chien-assis · Lucarnes", "Chien-assis et lucarnes : création et rénovation",
           "Jacobine, capucine, rampante ou chien-assis : nous créons et restaurons vos lucarnes, de la charpente à l'habillage en zinc ou en ardoise, partout en Île-de-France.",
           body, faq, "Création de chien-assis et de lucarnes",
           ("Un projet de chien-assis ?", "Étude, aide aux démarches et devis gratuits."))


def mansarde():
    faq = [
        ("Qu'est-ce qu'un brisis et un terrasson ?",
         "Une toiture mansardée comporte deux pentes par versant : le brisis, partie basse presque verticale qui abrite les fenêtres et les lucarnes, et le terrasson, partie haute à faible pente. Le brisis est souvent couvert d'ardoise ou de zinc, le terrasson le plus souvent de zinc."),
        ("Pourquoi le terrasson est-il souvent en zinc ?",
         "Sa pente est trop faible pour des ardoises ou des tuiles classiques. Le zinc, posé à joint debout ou à tasseaux, assure une parfaite étanchéité sur ces faibles pentes."),
        ("Peut-on isoler une toiture mansardée ?",
         "Oui. Lors de la réfection, l'isolation peut être placée par l'extérieur ou sous rampants, en traitant soigneusement la jonction entre brisis et terrasson, point faible fréquent des combles mansardés."),
        ("Une rénovation de mansarde nécessite-t-elle une autorisation ?",
         "Une réfection à l'identique est souvent dispensée, mais tout changement de matériau, de teinte ou de lucarnes demande en général une déclaration préalable, et l'avis de l'Architecte des Bâtiments de France en secteur protégé."),
    ]
    body = f"""    {photo("mansarde", eager=True)}
    <h2>La toiture mansardée, signature des maisons bourgeoises</h2>
    <p>Popularisée par l'architecte François Mansart au XVIIe siècle puis généralisée par l'architecture haussmannienne, la toiture à la Mansart permet de créer un étage habitable sous les combles. On la retrouve sur les immeubles parisiens comme sur les maisons bourgeoises de Saint-Maur-des-Fossés, de Versailles ou du Vésinet.</p>

    <h2>Le brisis : ardoise ou zinc</h2>
    <p>Partie basse et très pentue de la mansarde, le brisis porte les fenêtres et les <a href="/chien-assis-lucarne/">lucarnes</a>. Il est traditionnellement couvert d'ardoise naturelle posée au crochet ou au clou, ou habillé de zinc. Nous refaisons les brisis à l'identique ou dans le matériau autorisé par votre commune.</p>
    <h2>Le terrasson : le domaine du zinc</h2>
    <p>Partie haute à faible pente, le terrasson est le plus souvent couvert de zinc à joint debout ou à tasseaux. Mal entretenu, c'est une source fréquente d'infiltrations : nous le remplaçons avec ses accessoires (faîtage, ourlets, raccord avec le brisis).</p>
    {photo("drone")}

    <h2>Nos travaux sur les toitures mansardées</h2>
    <ul class="checks">
      <li>Réfection complète des brisis en ardoise ou en zinc</li>
      <li>Remplacement des terrassons en zinc</li>
      <li>Restauration et création de lucarnes, habillages zinc</li>
      <li>Chéneaux, gouttières et <a href="/cheneau-noue-zinc/">noues</a> en zinc</li>
      <li>Isolation des combles mansardés (entreprise RGE)</li>
      <li>Épis de faîtage, ornements et zinguerie décorative</li>
    </ul>
    <p>Pour les immeubles, nous intervenons en lien avec le <a href="/couvreur-copropriete-syndic/">syndic de copropriété</a>.</p>"""
    _guide("/toiture-mansardee-brisis-terrasson/", "Toiture mansardée",
           "Toiture mansardée : brisis ardoise, terrasson zinc | Couvreur JMC",
           "Rénovation de toiture mansardée en Île-de-France : brisis en ardoise ou zinc, terrasson zinc, lucarnes et isolation des combles, par des couvreurs-zingueurs.",
           "Toiture mansardée", "Toiture mansardée : brisis en ardoise et terrasson en zinc",
           "Réfection des brisis et des terrassons, lucarnes, zinguerie et isolation : nous rénovons les toitures à la Mansart des maisons bourgeoises et des immeubles d'Île-de-France.",
           body, faq, "Rénovation de toiture mansardée")


def cheneau():
    faq = [
        ("Qu'est-ce qu'une noue de toiture ?",
         "La noue est l'angle rentrant formé par la rencontre de deux versants de toit. L'eau de pluie s'y concentre : c'est l'un des points les plus sollicités de la couverture, généralement réalisé en zinc ou en plomb."),
        ("Quelle différence entre chéneau et gouttière ?",
         "La gouttière est suspendue en bas du toit. Le chéneau est un canal plus large, souvent encaissé dans la maçonnerie ou posé sur la corniche, typique des immeubles et des maisons anciennes."),
        ("Pourquoi mon chéneau fuit-il ?",
         "Soudures fatiguées, zinc percé par la corrosion, pente insuffisante, dilatation mal gérée ou débris qui bloquent l'écoulement. Un chéneau qui fuit endommage rapidement les murs et la charpente : il vaut mieux le refaire avant les dégâts."),
        ("Combien de temps dure un chéneau en zinc ?",
         "Bien posé et entretenu, un chéneau en zinc dure plusieurs décennies. Un nettoyage régulier des feuilles et débris prolonge nettement sa durée de vie."),
    ]
    body = f"""    {photo("meuliere", eager=True)}
    <h2>Chéneaux et noues : là où l'eau se concentre</h2>
    <p>Sur une toiture, toute l'eau de pluie converge vers quelques points clés : les noues, entre deux versants, et les chéneaux, qui la recueillent en bas du toit avant les descentes. Ces ouvrages en zinc travaillent en permanence ; lorsqu'ils vieillissent, ce sont eux qui provoquent les dégâts les plus coûteux.</p>

    <h2>La noue en zinc</h2>
    <p>Nous réalisons des noues en zinc façonnées sur mesure dans notre atelier, avec recouvrement correct des tuiles ou des ardoises, pour une évacuation rapide et durable de l'eau.</p>
    <h2>Le chéneau en zinc</h2>
    <h3>Chéneau encaissé</h3>
    <p>Intégré dans l'épaisseur de la maçonnerie ou derrière un acrotère, il est fréquent sur les immeubles et les maisons anciennes. Nous refaisons son fond (voligeage) et son habillage zinc, avec les joints de dilatation nécessaires.</p>
    <h3>Chéneau à l'égout et sur corniche</h3>
    <p>Posé en bas du versant, il protège la corniche et la façade. Nous le remplaçons avec ses talons, naissances et raccords aux descentes.</p>

    <h2>Nos travaux de zinguerie d'eaux pluviales</h2>
    <ul class="checks">
      <li>Création et réfection de noues en zinc</li>
      <li>Chéneaux encaissés et chéneaux sur corniche</li>
      <li>Gouttières pendantes, havraises et nantaises</li>
      <li>Descentes d'eaux pluviales en zinc et dauphins</li>
      <li>Couvertines et bandeaux en zinc</li>
      <li>Nettoyage et entretien des chéneaux et gouttières</li>
    </ul>
    <p>Voir aussi notre page <a href="/zinguerie/">zinguerie</a> et nos travaux pour <a href="/couvreur-copropriete-syndic/">copropriétés</a>.</p>"""
    _guide("/cheneau-noue-zinc/", "Chéneaux et noues en zinc",
           "Chéneau et noue en zinc : réfection et création | Couvreur JMC",
           "Réfection de chéneaux encaissés, noues en zinc, gouttières et descentes en Île-de-France, façonnés sur mesure par nos zingueurs. Devis gratuit.",
           "Zinguerie · Chéneaux · Noues", "Chéneaux et noues en zinc : réfection et création",
           "Noues, chéneaux encaissés, gouttières et descentes : nos zingueurs façonnent sur mesure les ouvrages qui protègent votre maison des eaux de pluie.",
           body, faq, "Chéneaux et noues en zinc")


def cheminee():
    faq = [
        ("Qu'est-ce qu'un solin de cheminée ?",
         "Le solin assure l'étanchéité entre la souche de cheminée et la couverture. Il peut être réalisé en mortier ou, plus durablement, avec une bande métallique en zinc ou en plomb engravée dans la maçonnerie."),
        ("Qu'est-ce que l'abergement d'une cheminée ?",
         "C'est l'ensemble des pièces en zinc ou en plomb posées autour de la souche, en amont, sur les côtés et en aval, pour rendre la jonction avec la toiture parfaitement étanche."),
        ("Quand faut-il refaire une souche de cheminée ?",
         "Joints qui se creusent, briques ou enduit qui s'effritent, couronnement fissuré, traces d'humidité dans les combles autour du conduit : ce sont les signes qu'une réfection s'impose."),
        ("Peut-on supprimer une souche de cheminée inutilisée ?",
         "Oui, il est possible de démolir une souche inutilisée et de refaire la couverture à cet endroit, ce qui supprime un point faible de la toiture. Une autorisation peut être nécessaire selon la commune."),
    ]
    body = f"""    {photo("drone", eager=True)}
    <h2>La cheminée, point sensible de la toiture</h2>
    <p>La souche de cheminée traverse la couverture : c'est l'un des points où l'étanchéité est la plus difficile à assurer. Avec le temps, les joints se dégradent, l'enduit se fissure et les raccords se décollent. Nos couvreurs-zingueurs remettent en état l'ensemble de l'ouvrage.</p>

    <h2>Nos travaux sur les cheminées</h2>
    <h3>Réfection de souche de cheminée</h3>
    <p>Rejointoiement ou reconstruction des briques, réfection de l'enduit, nouveau couronnement et chapeau de cheminée.</p>
    <h3>Solins et abergements</h3>
    <p>Remplacement des solins en mortier par des bandes en zinc ou en plomb engravées, abergements complets autour de la souche, raccordés à la couverture en tuile, en ardoise ou en zinc.</p>
    <h3>Habillage de souche</h3>
    <p>Habillage en zinc ou en ardoise pour protéger durablement une souche fatiguée et lui redonner une belle finition.</p>
    <h3>Suppression de souche inutilisée</h3>
    <p>Démolition de la souche et réfection de la couverture : un point faible en moins sur votre toit.</p>
    <p>Ces travaux s'intègrent idéalement à une <a href="/renovation-toiture/">rénovation de toiture</a> ou à des travaux de <a href="/zinguerie/">zinguerie</a>.</p>"""
    _guide("/souche-cheminee-solin-abergement/", "Souche de cheminée",
           "Souche de cheminée, solin et abergement : réfection | JMC",
           "Réfection de souche de cheminée, solins et abergements en zinc ou plomb, habillage de souche en Île-de-France, par des couvreurs-zingueurs. Devis gratuit.",
           "Cheminée · Solin · Abergement", "Souche de cheminée : réfection, solins et abergements",
           "Souche fissurée, solin dégradé, abergement à reprendre : nous remettons en état la cheminée et son raccord avec la toiture, en zinc, en plomb ou en ardoise.",
           body, faq, "Réfection de souche de cheminée")


def terrasse():
    faq = [
        ("Quelle étanchéité choisir pour une toiture terrasse ?",
         "Les deux grandes solutions sont la membrane EPDM, posée en une seule pièce sans joint, et l'étanchéité bitumineuse (membranes en bitume élastomère, généralement en bicouche). Le choix dépend de la surface, de l'usage de la terrasse (accessible ou non), de l'isolation et des relevés. Nous vous conseillons après visite."),
        ("Pourquoi ma toiture terrasse fuit-elle ?",
         "Les causes les plus fréquentes sont des relevés d'étanchéité décollés, des évacuations bouchées ou mal raccordées, une membrane vieillie ou percée, ou une pente insuffisante qui laisse l'eau stagner. Un diagnostic permet de savoir s'il faut réparer ou refaire."),
        ("Peut-on isoler une toiture terrasse en refaisant l'étanchéité ?",
         "Oui, c'est le bon moment : l'isolant est posé sous la nouvelle étanchéité. Réalisée par une entreprise RGE, cette isolation peut ouvrir droit à des aides selon les conditions en vigueur."),
        ("Reprenez-vous aussi les descentes d'eaux pluviales ?",
         "Oui. Naissances, trop-pleins, descentes et raccordements sont repris en même temps que l'étanchéité : une terrasse étanche doit aussi évacuer l'eau correctement."),
    ]
    body = f"""    <h2>L'étanchéité, protection vitale des toits plats</h2>
    <p>Toits-terrasses de maisons contemporaines, extensions, garages, immeubles : une toiture plate ne pardonne pas les défauts d'étanchéité. Nos équipes réalisent la réfection complète ou la création de l'étanchéité de vos toitures terrasses, avec l'isolation, les relevés et l'évacuation des eaux pluviales.</p>

    <h2>Nos solutions d'étanchéité</h2>
    <h3>Membrane EPDM</h3>
    <p>Une membrane en caoutchouc synthétique posée d'un seul tenant, sans joint, résistante aux UV et aux écarts de température : idéale pour les toits plats de maisons, extensions et garages.</p>
    <h3>Étanchéité bitumineuse</h3>
    <p>Membranes en bitume élastomère posées en une ou deux couches, solution éprouvée pour les terrasses de grande surface et les immeubles.</p>
    <h3>Isolation de la terrasse</h3>
    <p>Lors de la réfection, nous intégrons un isolant sous l'étanchéité pour améliorer le confort et les performances énergétiques du logement (voir <a href="/isolation-toiture/">isolation de toiture</a>).</p>
    <h3>Relevés, acrotères et couvertines</h3>
    <p>Les points singuliers font la qualité d'une étanchéité : relevés soignés, acrotères protégés par des couvertines en zinc ou en aluminium, seuils et traversées traités dans les règles de l'art.</p>

    <h2>Reprise des descentes d'eaux pluviales</h2>
    <p>Une terrasse étanche doit aussi évacuer l'eau rapidement. Nous reprenons les naissances, les trop-pleins, les descentes d'eaux pluviales en zinc ou en PVC et leurs raccordements, sur les toits plats comme sur les toitures en pente (voir <a href="/cheneau-noue-zinc/">chéneaux et noues</a> et <a href="/zinguerie/">zinguerie</a>).</p>
    {photo("pavillon")}

    <h2>Pour les particuliers, les copropriétés et les maîtres d'œuvre</h2>
    <p>Maisons, extensions, immeubles en <a href="/couvreur-copropriete-syndic/">copropriété</a> ou programmes neufs : nous intervenons en direct ou aux côtés de votre maître d'œuvre ou de votre architecte, avec la même rigueur.</p>"""
    _guide("/etancheite-toiture-terrasse/", "Étanchéité toiture terrasse",
           "Étanchéité de toiture terrasse : EPDM, bitume, réfection | JMC",
           "Réfection et création d'étanchéité de toiture terrasse (EPDM, bitume), isolation, relevés et reprise des descentes d'eaux pluviales en Île-de-France. Devis gratuit.",
           "Étanchéité · Toit-terrasse", "Étanchéité de toiture terrasse et descentes d'eaux pluviales",
           "Membrane EPDM ou étanchéité bitumineuse, isolation, relevés et évacuations : nous refaisons l'étanchéité de vos toits plats et reprenons vos descentes d'eaux pluviales.",
           body, faq, "Étanchéité de toiture terrasse",
           ("Un toit-terrasse à refaire ?", "Diagnostic et devis gratuits pour votre étanchéité."))


def photovoltaique():
    faq = [
        ("Pourquoi refaire la toiture avant d'installer des panneaux photovoltaïques ?",
         "Les panneaux sont installés pour 25 à 30 ans environ. Si la couverture doit être refaite pendant cette période, il faudra déposer puis reposer l'installation, ce qui coûte cher. Mieux vaut vérifier et, si besoin, rénover la toiture avant la pose."),
        ("Comment savoir si ma toiture peut accueillir des panneaux ?",
         "Nous vérifions l'état de la couverture, des tuiles ou ardoises, de l'écran sous-toiture, des liteaux et de la charpente, ainsi que sa capacité à supporter le poids de l'installation. Vous savez ainsi si des travaux sont nécessaires avant la pose."),
        ("Posez-vous les panneaux photovoltaïques ?",
         "Notre rôle est de préparer une toiture saine et adaptée : réfection de couverture, renfort de charpente, zinguerie. Nous travaillons en coordination avec votre installateur photovoltaïque pour que la pose se fasse dans les meilleures conditions."),
        ("Peut-on combiner rénovation de toiture et isolation avant la pose ?",
         "Oui. C'est même le moment idéal pour isoler la toiture par l'extérieur, avant que les panneaux ne rendent l'intervention plus complexe."),
    ]
    body = f"""    {photo("pavillon", eager=True)}
    <h2>Une toiture saine avant vos panneaux solaires</h2>
    <p>Une installation photovoltaïque est prévue pour durer plusieurs décennies. Encore faut-il que la toiture qui la porte soit en état de durer aussi longtemps. Poser des panneaux sur une couverture fatiguée, c'est prendre le risque de devoir tout déposer quelques années plus tard pour refaire le toit.</p>

    <h2>Nos travaux de préparation</h2>
    <ul class="checks">
      <li><strong>Diagnostic de la toiture</strong> : couverture, écran sous-toiture, liteaux, zinguerie</li>
      <li><strong>Vérification de la charpente</strong> et renfort si nécessaire pour supporter les panneaux</li>
      <li><strong>Rénovation ou remplacement de la couverture</strong> sur le versant concerné ou sur l'ensemble du toit</li>
      <li><strong>Isolation de la toiture</strong> par l'extérieur avant la pose (entreprise RGE)</li>
      <li><strong>Zinguerie neuve</strong> : gouttières, noues, abergements</li>
      <li><strong>Coordination avec votre installateur</strong> pour enchaîner les travaux sans perte de temps</li>
    </ul>

    <h2>Pourquoi passer par un couvreur ?</h2>
    <p>L'installateur de panneaux connaît son matériel ; le couvreur connaît votre toiture. En faisant intervenir JMC en amont, vous partez sur une base saine, étanche et garantie par notre assurance décennale, et vous évitez les mauvaises surprises une fois les panneaux en place.</p>
    <p>Voir aussi : <a href="/renovation-toiture/">rénovation de toiture</a>, <a href="/charpente/">charpente</a>, <a href="/isolation-toiture/">isolation</a>.</p>"""
    _guide("/toiture-avant-panneaux-photovoltaiques/", "Toiture avant panneaux photovoltaïques",
           "Rénover sa toiture avant des panneaux photovoltaïques | JMC",
           "Diagnostic, renfort de charpente, réfection de couverture et isolation avant l'installation de panneaux solaires photovoltaïques, en Île-de-France. Devis gratuit.",
           "Photovoltaïque", "Rénover sa toiture avant l'installation de panneaux photovoltaïques",
           "Avant de poser des panneaux pour 25 à 30 ans, assurez-vous que votre toiture tiendra aussi longtemps : diagnostic, charpente, couverture et isolation par un couvreur certifié.",
           body, faq, "Travaux de couverture avant pose de panneaux photovoltaïques",
           ("Un projet photovoltaïque ?", "Faites vérifier votre toiture avant la pose : diagnostic et devis gratuits."))


def combles_perdus():
    faq = [
        ("Qu'est-ce que des combles perdus ?",
         "Ce sont des combles non aménagés, trop bas ou encombrés par la charpente pour être habités. On isole alors le plancher des combles, et non la toiture : c'est la solution la plus simple et la plus rentable."),
        ("Soufflage ou rouleaux : que choisir ?",
         "Le soufflage d'isolant en vrac (laine de verre, laine de roche ou ouate de cellulose) remplit parfaitement tous les recoins, même dans les combles difficiles d'accès. Les rouleaux ou panneaux déroulés conviennent aux combles dégagés, faciles à parcourir. Nous choisissons la technique selon la configuration."),
        ("Quelle épaisseur d'isolant faut-il ?",
         "Pour être performante et éligible aux aides, l'isolation des combles perdus doit généralement atteindre une résistance thermique R ≥ 7 m².K/W, ce qui représente souvent 30 à 40 cm d'isolant selon le matériau."),
        ("Combien de temps durent les travaux ?",
         "Pour une maison individuelle, l'isolation des combles perdus par soufflage se réalise le plus souvent en une journée, sans travaux dans les pièces habitées."),
        ("Y a-t-il des aides pour isoler les combles perdus ?",
         "Réalisés par une entreprise RGE comme JMC, ces travaux peuvent bénéficier d'aides, notamment des primes CEE, selon votre situation et les conditions en vigueur au moment des travaux."),
    ]
    body = f"""    <h2>Les combles perdus, première source de déperdition</h2>
    <p>Dans une maison mal isolée, la chaleur monte et s'échappe d'abord par le haut. Isoler le plancher des combles perdus est l'un des travaux les plus rentables de la rénovation énergétique : un chantier rapide, sans toucher aux pièces de vie, pour un gain de confort immédiat en hiver comme en été.</p>

    <h2>Nos techniques</h2>
    <h3>Isolation par soufflage</h3>
    <p>Un isolant en vrac (laine de verre, laine de roche ou ouate de cellulose) est projeté à l'aide d'une machine sur toute la surface du plancher, en couche régulière et continue, jusque dans les recoins inaccessibles. Des piges de repérage permettent de contrôler l'épaisseur.</p>
    <h3>Isolation par rouleaux ou panneaux</h3>
    <p>Pour des combles dégagés, l'isolant est déroulé en une ou deux couches croisées, avec un pare-vapeur côté chauffé si nécessaire.</p>

    <h2>Un chantier préparé dans les règles</h2>
    <ul class="checks">
      <li>Inspection de la charpente et de la couverture avant isolation : pas question d'isoler sous un toit qui fuit</li>
      <li>Protection des spots et boîtiers électriques, écarts de sécurité autour des conduits de cheminée</li>
      <li>Maintien de la ventilation de la toiture (déflecteurs en pied de versant)</li>
      <li>Isolation et étanchéité de la trappe d'accès</li>
      <li>Repérage de l'épaisseur et attestation de fin de travaux pour vos aides</li>
    </ul>

    <h2>Le regard du couvreur, en plus</h2>
    <p>Parce que nous sommes couvreurs, nous vérifions aussi l'état de votre toiture et de votre charpente lors de la visite. Si une <a href="/renovation-toiture/">rénovation de toiture</a> s'impose à court terme, nous vous le disons : il serait dommage d'isoler sous une couverture à refaire.</p>
    <p>Combles aménagés ou à aménager ? Voir l'<a href="/isolation-rampants/">isolation des rampants</a>. Toutes nos solutions : <a href="/isolation-toiture/">isolation de toiture</a>. En immeuble, nous intervenons aussi pour les <a href="/couvreur-copropriete-syndic/">copropriétés</a>.</p>"""
    _guide("/isolation-combles-perdus/", "Isolation des combles perdus",
           "Isolation des combles perdus par soufflage, entreprise RGE | JMC",
           "Isolation des combles perdus par soufflage ou déroulage (laine minérale, ouate de cellulose) en Île-de-France, par un couvreur RGE. Aides possibles, devis gratuit.",
           "Isolation · Combles perdus", "Isolation des combles perdus par soufflage",
           "Une journée de travaux pour un gain de confort immédiat : nous isolons vos combles perdus par soufflage ou déroulage, avec le regard d'un couvreur sur votre toiture.",
           body, faq, "Isolation des combles perdus",
           ("Vos combles sont-ils bien isolés ?", "Visite, diagnostic et devis gratuits par une entreprise RGE."))


def rampants():
    faq = [
        ("Qu'est-ce que l'isolation des rampants ?",
         "Ce sont les parties inclinées du toit, côté intérieur. On isole les rampants lorsque les combles sont aménagés ou à aménager : l'isolant est posé entre et sous les chevrons, sous la couverture."),
        ("Quelle performance viser ?",
         "Pour être efficace et éligible aux aides, l'isolation des rampants doit généralement atteindre une résistance thermique R ≥ 6 m².K/W, souvent obtenue en deux couches croisées d'isolant."),
        ("Isolation des rampants ou isolation par l'extérieur ?",
         "Sous rampants, l'isolation se fait par l'intérieur sans toucher à la couverture, mais réduit un peu le volume habitable. Par l'extérieur (sarking), l'isolant est posé au-dessus des chevrons lors d'une réfection de toiture : aucun volume perdu, aucun pont thermique. Nous vous conseillons selon l'état de votre toiture."),
        ("Quel isolant choisir pour les rampants ?",
         "La laine de verre ou de roche est performante et économique. La fibre de bois, plus dense, améliore nettement le confort d'été dans les pièces sous les toits. La ouate de cellulose est une bonne alternative biosourcée."),
        ("Qui réalise la finition intérieure ?",
         "Nous réalisons l'isolation et le pare-vapeur. Pour la finition (plaques de plâtre, peinture), nous pouvons vous recommander des prestataires compétents qui interviennent dans la foulée."),
    ]
    body = f"""    <h2>Des combles aménagés confortables, été comme hiver</h2>
    <p>Chambres, bureau, salle de jeux sous les toits : des combles aménagés mal isolés sont glacials l'hiver et étouffants l'été. L'isolation des rampants traite la toiture par l'intérieur pour en faire des pièces agréables toute l'année.</p>

    <h2>Notre méthode d'isolation sous rampants</h2>
    <ol class="steps">
      <li><strong>Vérification de la toiture</strong><br>Couverture, écran sous-toiture et charpente : on n'isole pas sous un toit qui doit être refait.</li>
      <li><strong>Première couche entre chevrons</strong><br>Isolant posé entre les chevrons, en conservant la ventilation sous la couverture.</li>
      <li><strong>Deuxième couche croisée</strong><br>Sur ossature, pour supprimer les ponts thermiques et atteindre la performance visée.</li>
      <li><strong>Pare-vapeur continu</strong><br>Membrane soigneusement raccordée et scotchée pour une parfaite étanchéité à l'air.</li>
      <li><strong>Finition</strong><br>Plaques de plâtre par un prestataire compétent que nous vous recommandons.</li>
    </ol>

    <h2>Les isolants que nous posons</h2>
    <ul class="checks">
      <li><strong>Laine de verre et laine de roche</strong> : performantes et économiques</li>
      <li><strong>Fibre de bois</strong> : excellent confort d'été grâce à sa densité</li>
      <li><strong>Ouate de cellulose</strong> en panneaux : solution biosourcée</li>
    </ul>

    {reviews_block(['richard', 'larry'])}
    <h2>Et si vous refaites votre toiture ?</h2>
    <p>Si la couverture doit être refaite, l'<a href="/isolation-toiture/">isolation par l'extérieur (sarking)</a> devient la meilleure option : posée au-dessus des chevrons pendant la <a href="/renovation-toiture/">rénovation de toiture</a>, elle ne prend aucun centimètre à vos pièces. Pour les combles non aménagés, voir l'<a href="/isolation-combles-perdus/">isolation des combles perdus</a>.</p>"""
    _guide("/isolation-rampants/", "Isolation des rampants",
           "Isolation des rampants et combles aménagés, entreprise RGE | JMC",
           "Isolation sous rampants des combles aménagés en Île-de-France : laine minérale, fibre de bois, pare-vapeur, par un couvreur RGE. Aides possibles, devis gratuit.",
           "Isolation · Rampants", "Isolation des rampants et des combles aménagés",
           "Des pièces sous les toits chaudes l'hiver et fraîches l'été : nous isolons vos rampants par l'intérieur, en deux couches croisées avec pare-vapeur, après vérification de votre toiture.",
           body, faq, "Isolation des rampants",
           ("Des combles trop chauds ou trop froids ?", "Visite, diagnostic et devis gratuits par une entreprise RGE."))


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
                "Chantiers JMC : toitures en ardoise et zinc, charpente à Paris, écoles à Montfermeil, balcons boulevard de Sébastopol. Photos et avis clients.",
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
        for k in ("drone", "mansarde", "meuliere", "pavillon") if photo_src(k))
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
  <div class="grid g2">{"".join(google_review(k) for k in GOOGLE_REVIEWS)}</div>
  <h3 style="margin-top:36px">Témoignages de nos clients</h3>
  <div class="grid g3">{reviews_html(len(REVIEWS), old=True)}</div>
  <p style="margin-top:24px"><a class="btn btn-dark" href="{BIZ['reviews']}" target="_blank" rel="noopener">Lire et laisser un avis sur Google</a></p>
</div></section>
"""
    html += cta_band("Votre chantier sera notre prochaine référence")
    html += footer()
    write("/nos-references/", html)


def zones():
    trail = [("/", "Accueil"), ("/zones-intervention/", "Zones d'intervention")]
    lds = [org_ld(), crumbs_ld(trail)]
    groups = [
        ("Seine-et-Marne (77)", ["Lagny-sur-Marne", "Ozoir-la-Ferrière", "Bussy-Saint-Georges", "Gretz-Armainvilliers",
                                 "Lésigny", "Ferrières-en-Brie", "Serris", "Montévrain", "Thorigny-sur-Marne",
                                 "Saint-Thibault-des-Vignes", "Coupvray", "Fontainebleau", "Bois-le-Roi", "Samois-sur-Seine",
                                 "Barbizon", "Courtry", "Chelles", "Le Pin", "Annet-sur-Marne", "Claye-Souilly"]),
        ("Seine-Saint-Denis (93)", ["Vaujours", "Coubron", "Montfermeil", "Clichy-sous-Bois", "Livry-Gargan",
                                    "Sevran", "Le Raincy", "Villemomble", "Gagny", "Neuilly-sur-Marne",
                                    "Noisy-le-Grand", "Noisy-le-Sec", "Aulnay-sous-Bois", "Tremblay-en-France"]),
        ("Paris (75)", ["Tous les arrondissements"]),
        ("Val-de-Marne (94)", ["Saint-Maur-des-Fossés", "La Varenne-Saint-Hilaire", "Nogent-sur-Marne", "Le Perreux-sur-Marne",
                               "Vincennes", "Saint-Mandé", "Bry-sur-Marne", "Joinville-le-Pont", "Le Plessis-Trévise",
                               "Chennevières-sur-Marne", "Fontenay-sous-Bois", "Maisons-Alfort"]),
        ("Hauts-de-Seine (92)", ["Neuilly-sur-Seine", "Boulogne-Billancourt", "Saint-Cloud", "Sceaux", "Ville-d'Avray",
                                 "Marnes-la-Coquette", "Vaucresson", "Garches", "Rueil-Malmaison", "Meudon", "Sèvres",
                                 "Chaville", "Bourg-la-Reine", "Levallois-Perret", "Issy-les-Moulineaux", "Antony"]),
        ("Val-d'Oise (95)", ["Cergy", "Argenteuil", "Enghien-les-Bains", "Montmorency", "Roissy-en-France",
                             "Sarcelles", "Pontoise", "L'Isle-Adam"]),
        ("Yvelines (78)", ["Versailles", "Le Vésinet", "Saint-Germain-en-Laye", "Maisons-Laffitte",
                           "Le Chesnay-Rocquencourt", "Chatou", "Croissy-sur-Seine", "Louveciennes", "Marly-le-Roi",
                           "Bougival", "La Celle-Saint-Cloud", "L'Étang-la-Ville", "Chambourcy", "Viroflay", "Rambouillet"]),
        ("Essonne (91)", ["Évry-Courcouronnes", "Massy", "Palaiseau", "Corbeil-Essonnes",
                          "Brunoy", "Yerres", "Savigny-sur-Orge", "Étampes"]),
    ]
    blocks = "".join(
        f'<div class="card"><h3>{g}</h3><ul class="cities" style="columns:2 140px">'
        + "".join(f"<li>{c}</li>" for c in cs) + "</ul></div>" for g, cs in groups)
    html = head("Couvreur en Île-de-France : 94, 78, 92, 77 et Paris | JMC",
                "Couvreur dans toute l'Île-de-France : Saint-Maur, Nogent, Versailles, Le Vésinet, Neuilly, Saint-Cloud, Fontainebleau, Paris et les 8 départements.",
                "/zones-intervention/", lds)
    html += header("/zones-intervention/")
    html += page_hero(trail, "Zones d'intervention", "Couvreur dans toute l'Île-de-France",
                      "Depuis notre siège de Courtry (77), nos équipes et notre flotte de véhicules interviennent à Paris et dans les huit départements franciliens, pour les particuliers comme pour les professionnels.")
    html += f"""
<section><div class="wrap">
  <div class="section-head"><h2>Nos villes prioritaires</h2><p>Une page dédiée pour chaque commune où nous intervenons le plus souvent.</p></div>
  <div style="margin-bottom:40px">{city_groups()}</div>
  <h2>Toutes nos communes d'intervention par département</h2>
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
      <label>Comment nous avez-vous connu ?
        <select name="origine">
          <option>Recommandation d'un proche ou d'un voisin</option>
          <option>Panneau de chantier JMC</option>
          <option>Recherche Google</option>
          <option>Instagram</option>
          <option>Déjà client JMC</option>
          <option>Autre</option>
        </select></label>
      <label>Type de travaux
        <select name="travaux">
          <option>Remplacement / rénovation de toiture</option>
          <option>Nettoyage / démoussage de toiture</option>
          <option>Toiture de maison neuve / extension</option>
          <option>Isolation de toiture</option>
          <option>Isolation des rampants / combles aménagés</option>
          <option>Isolation des combles perdus</option>
          <option>Couverture zinc / bardage (maison d'architecte)</option>
          <option>Charpente</option>
          <option>Zinguerie / gouttières</option>
          <option>Copropriété / syndic</option>
          <option>Promotion immobilière / constructeur</option>
          <option>Fenêtre de toit VELUX / lucarne</option>
          <option>Étanchéité toiture terrasse / descentes</option>
          <option>Toiture avant panneaux photovoltaïques</option>
          <option>SAV – client JMC</option>
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
    <p><strong>Devis gratuit et sans engagement</strong> · <a href="{BIZ['reviews']}" target="_blank" rel="noopener">Avis Google</a>{insta_link(" · ")}</p>
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
           ("/renovation-toiture/", "0.95"), ("/nettoyage-toiture/", "0.95"), ("/toiture-maison-neuve/", "0.95"), ("/isolation-toiture/", "0.95"), ("/couverture-zinc-bardage/", "0.95"), ("/couvreur-copropriete-syndic/", "0.95"), ("/fenetre-de-toit-velux-lucarnes/", "0.9"), ("/couvreur-promotion-immobiliere/", "0.9"), ("/notre-methode-sav-qualite/", "0.8"), ("/chien-assis-lucarne/", "0.9"), ("/toiture-mansardee-brisis-terrasson/", "0.85"), ("/cheneau-noue-zinc/", "0.85"), ("/souche-cheminee-solin-abergement/", "0.85"), ("/etancheite-toiture-terrasse/", "0.9"), ("/isolation-combles-perdus/", "0.9"), ("/isolation-rampants/", "0.9"), ("/toiture-avant-panneaux-photovoltaiques/", "0.85"), ("/zones-intervention/", "0.7"), ("/nos-references/", "0.7"),
           ("/contact/", "0.8")]


def seo_files():
    SITEMAP.extend((f"/{d['slug']}/", "0.9") for d in DEPTS_PAGES)
    SITEMAP.extend((f"/{v['slug']}/", "0.85") for v in VILLES)
    urls = "\n".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod><priority>{p}</priority></url>"
                     for u, p in SITEMAP)
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n',
        encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /merci/\n\nSitemap: {SITE}/sitemap.xml\n",
                                     encoding="utf-8")
    print("écrit sitemap.xml, robots.txt")


if __name__ == "__main__":
    for fn in (home, couverture, charpente, zinguerie, renovation, nettoyage, maison_neuve, isolation, zinc_bardage, copropriete, fenetres, promotion, methode, chien_assis, mansarde, cheneau, cheminee, terrasse, photovoltaique, combles_perdus, rampants, villes, depts, references, zones, contact, merci, mentions, notfound):
        fn()
    seo_files()
