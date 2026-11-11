"""Générateur du site OF ENTRETIENS.

Produit des pages HTML statiques dans ../site/ (aucun framework côté visiteur).
L'en-tête, le pied de page, les coordonnées et les données structurées sont définis
une seule fois ici, ce qui évite les incohérences entre pages.

Usage :  python3 -I src/build.py
"""
import html, json, os, re, sys
from datetime import date

ICI = os.path.dirname(os.path.abspath(__file__))
SORTIE = os.path.normpath(os.path.join(ICI, "..", "site"))
AUJOURDHUI = date.today().isoformat()

# --------------------------------------------------------------------------
# Données de l'entreprise (source : docs/base-de-reference.md)
# --------------------------------------------------------------------------
SITE = "https://www.ofentretiens.com"
NOM = "OF ENTRETIENS"
VILLE = "Montfermeil"
TEL = "06 62 06 93 22"
TEL_LIEN = "tel:+33662069322"
TEL_INTL = "+33662069322"
EMAIL = "mike.ofentretiens@gmail.com"
RUE, CP = "8 avenue des Frères Lumière", "93370"
INSTAGRAM = "https://www.instagram.com/ofentretiens/"
VILLES = ["Montfermeil", "Clichy-sous-Bois", "Coubron", "Gagny", "Livry-Gargan", "Le Raincy", "Vaujours",
          "Villemomble", "Chelles", "Neuilly-sur-Marne", "Noisy-le-Grand", "Bondy", "Sevran",
          "Aulnay-sous-Bois", "Montreuil", "Paris"]
DEPARTEMENTS = "75, 77, 78, 91, 92, 93, 94, 95"

SERVICES = [
    dict(cle="carottage", url="/carottage-urgence-montfermeil/", menu="Carottage en urgence",
         sous="Percements, coupe-feu, reprises", carte="carte-carottage",
         titre="Carottage en urgence",
         texte="Une réservation manque et le chantier s’arrête ? Nous carottons, traitons le coupe-feu et reprenons le doublage."),
    dict(cle="corvoyage", url="/corvoyage-montfermeil/", menu="Corvoyage & levée de réserves",
         sous="Livraison, réserves, SAV et GPA", carte="carte-corvoyage",
         titre="Corvoyage & levée de réserves",
         texte="Logements prêts à livrer, réserves levées jusqu’au dernier quitus, SAV et GPA en lieu et place de vos équipes."),
    dict(cle="nettoyage", url="/nettoyage-bureaux-montfermeil/", menu="Nettoyage de bureaux & base-vie",
         sous="Locaux, sanitaires, base-vie de chantier", carte="carte-nettoyage",
         titre="Nettoyage de bureaux & base-vie",
         texte="Bureaux, sanitaires, parties communes et base-vie de chantier entretenus selon un périmètre défini ensemble."),
    dict(cle="logistique", url="/plateformes-logistiques/", menu="Plateformes logistiques",
         sous="Propreté, maintenance, urgences", carte="carte-logistique",
         titre="Plateformes logistiques",
         texte="Propreté, maintenance en site occupé, urgences après sinistre et aménagements, sans gêner vos flux."),
]
CARTES_EN_PLUS = [
    dict(url="/estimation/?service=facade", carte="carte-facade", titre="Nettoyage de façade & bardage",
         texte="Remise en propreté des façades et des bardages, en nacelle si nécessaire, avant une livraison ou en entretien."),
    dict(url="/contact/", carte="carte-tce", titre="Travaux tous corps d’état",
         texte="Plâtrerie, menuiseries, sols, peinture, serrurerie, gros œuvre, plomberie, électricité : un seul interlocuteur."),
]

def e(t):
    return html.escape(t, quote=True)

# --------------------------------------------------------------------------
# Gabarit commun
# --------------------------------------------------------------------------
def entete(actif):
    def cur(url):
        return ' aria-current="page"' if url == actif else ""
    sous = "\n".join(
        f'          <li><a href="{s["url"]}"{cur(s["url"])}>{s["menu"]}<small>{s["sous"]}</small></a></li>' for s in SERVICES)
    sous_mobile = "\n".join(f'      <a href="{s["url"]}"{cur(s["url"])}>{s["menu"]}</a>' for s in SERVICES)
    return f'''<a class="lien-evitement" href="#contenu">Aller au contenu</a>
<header class="entete">
  <div class="conteneur">
    <a class="logo" href="/" aria-label="{NOM}, retour à l’accueil"><b>OF</b>ENTRETIENS</a>
    <nav aria-label="Navigation principale">
      <ul class="menu">
        <li>
          <button type="button" aria-expanded="false" aria-controls="sous-menu-services">Services</button>
          <ul class="sous-menu" id="sous-menu-services">
{sous}
          </ul>
        </li>
        <li><a href="/realisations/"{cur("/realisations/")}>Réalisations</a></li>
        <li><a href="/qui-sommes-nous/"{cur("/qui-sommes-nous/")}>Qui sommes-nous</a></li>
        <li><a href="/contact/"{cur("/contact/")}>Contact</a></li>
      </ul>
    </nav>
    <div class="entete-actions">
      <a class="btn btn-action btn-tel" href="{TEL_LIEN}" aria-label="Appeler le {TEL}"><span>{TEL}</span></a>
      <a class="btn btn-sombre btn-devis" href="/estimation/">Devis gratuit</a>
      <button class="burger" type="button" aria-label="Ouvrir le menu" aria-expanded="false" aria-controls="menu-mobile"><span></span><span></span><span></span></button>
    </div>
  </div>
  <nav class="menu-mobile" id="menu-mobile" aria-label="Menu mobile" hidden>
    <a href="/"{cur("/")}>Accueil</a>
    <p class="titre-groupe">Services</p>
    <div class="sous">
{sous_mobile}
    </div>
    <a href="/realisations/"{cur("/realisations/")}>Réalisations</a>
    <a href="/qui-sommes-nous/"{cur("/qui-sommes-nous/")}>Qui sommes-nous</a>
    <a href="/contact/"{cur("/contact/")}>Contact</a>
    <div class="groupe-btn">
      <a class="btn btn-action btn-tel" href="{TEL_LIEN}">Appeler</a>
      <a class="btn btn-sombre" href="/estimation/">Devis gratuit</a>
    </div>
  </nav>
</header>
'''

def pied():
    services = "\n".join(f'          <li><a href="{s["url"]}">{s["menu"]}</a></li>' for s in SERVICES)
    villes = "\n".join(f"          <li>{v}</li>" for v in VILLES)
    return f'''<footer class="pied">
  <div class="conteneur">
    <div class="pied-grille">
      <div>
        <a class="logo" href="/"><b>OF</b>ENTRETIENS</a>
        <p style="margin-top:.8rem">Entretien, travaux et interventions urgentes pour les promoteurs, les bailleurs, les entreprises et les sites logistiques.</p>
        <p style="margin-top:1rem"><a class="tel" href="{TEL_LIEN}">{TEL}</a><br>
        <a href="mailto:{EMAIL}">{EMAIL}</a><br>
        {RUE}<br>{CP} {VILLE}</p>
        <p style="margin-top:.8rem"><a href="{INSTAGRAM}" rel="noopener">Instagram : @ofentretiens</a></p>
      </div>
      <div>
        <h2>Nos services</h2>
        <ul>
{services}
          <li><a href="/estimation/">Estimation gratuite</a></li>
        </ul>
      </div>
      <div>
        <h2>Plan du site</h2>
        <ul>
          <li><a href="/">Accueil</a></li>
          <li><a href="/realisations/">Réalisations</a></li>
          <li><a href="/qui-sommes-nous/">Qui sommes-nous</a></li>
          <li><a href="/contact/">Contact</a></li>
          <li><a href="/mentions-legales/">Mentions légales</a></li>
        </ul>
      </div>
      <div>
        <h2>Villes desservies</h2>
        <ul class="villes">
{villes}
        </ul>
        <p style="margin-top:.6rem;font-size:.88rem">Et toute l’Île-de-France ({DEPARTEMENTS}).</p>
      </div>
    </div>
    <div class="pied-bas">
      <p>{NOM} — SASU au capital de 500&nbsp;€ · RCS Bobigny 927&nbsp;491&nbsp;357 · TVA FR80927491357</p>
      <p><a href="/mentions-legales/">Mentions légales</a> · <button type="button" data-gerer-cookies>Gérer les cookies</button></p>
    </div>
  </div>
</footer>
'''

BARRE = f'''<div class="barre-mobile" role="region" aria-label="Contact rapide">
  <a class="btn btn-action btn-tel" href="{TEL_LIEN}">Appeler</a>
  <a class="btn btn-sombre" href="/estimation/">Devis gratuit</a>
</div>
'''

COOKIES = '''<div class="cookies" id="cookies" role="dialog" aria-labelledby="cookies-titre" hidden>
  <h2 id="cookies-titre">Cookies</h2>
  <p>Ce site ne dépose aucun cookie publicitaire. Avec votre accord seulement, nous pourrions mesurer
  l’audience de façon anonyme. Votre choix est modifiable à tout moment via « Gérer les cookies ».</p>
  <div class="reglages" hidden>
    <label><input type="checkbox" checked disabled> <span><b>Nécessaires</b> — mémorisent votre choix. Toujours actifs.</span></label>
    <label><input type="checkbox" name="mesure"> <span><b>Mesure d’audience</b> — statistiques de visite anonymes (aucun outil installé pour l’instant).</span></label>
  </div>
  <div class="boutons">
    <button type="button" data-cookies="refuser">Tout refuser</button>
    <button type="button" data-cookies="personnaliser">Personnaliser</button>
    <button type="button" data-cookies="accepter">Tout accepter</button>
  </div>
</div>
'''

def jsonld(*objets):
    return "\n".join('<script type="application/ld+json">\n' + json.dumps(o, ensure_ascii=False, indent=1) + "\n</script>" for o in objets)

ADRESSE = {"@type": "PostalAddress", "streetAddress": RUE, "postalCode": CP, "addressLocality": VILLE,
           "addressRegion": "Île-de-France", "addressCountry": "FR"}
FOURNISSEUR = {"@type": "HomeAndConstructionBusiness", "@id": SITE + "/#entreprise", "name": NOM,
               "telephone": TEL_INTL, "url": SITE + "/", "address": ADRESSE}

def fil_ariane(liste):
    """liste = [(nom, url), …] ; renvoie (html, jsonld)."""
    items = [("Accueil", "/")] + liste
    h = "\n".join(
        (f'      <li><a href="{u}">{n}</a></li>' if i < len(items) - 1 else f'      <li aria-current="page">{n}</li>')
        for i, (n, u) in enumerate(items))
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(items)]}
    return f'<nav class="fil conteneur" aria-label="Fil d’Ariane">\n    <ol>\n{h}\n    </ol>\n  </nav>', ld

def faq(questions):
    h = "\n".join(f'''      <details>
        <summary>{e(q)}</summary>
        <div class="reponse"><p>{r}</p></div>
      </details>''' for q, r in questions)
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", r)}}
        for q, r in questions]}
    return f'<div class="faq">\n{h}\n    </div>', ld

PAGES = []  # pour le sitemap

def page(chemin, titre, description, og_image, corps, donnees=(), actif=None, noindex=False,
         preload="", scripts=(), mots_min=0):
    assert len(titre) < 60, f"Titre trop long ({len(titre)}) : {titre}"
    assert len(description) < 155, f"Description trop longue ({len(description)}) : {description}"
    url = SITE + chemin
    robots = '<meta name="robots" content="noindex, follow">\n' if noindex else ""
    js = "".join(f'<script src="{s}" defer></script>\n' for s in ("/assets/site.js",) + tuple(scripts))
    doc = f'''<!doctype html>
<html lang="fr" data-mesure-audience="off">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(titre)}</title>
<meta name="description" content="{e(description)}">
{robots}<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="{NOM}">
<meta property="og:title" content="{e(titre)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/img/{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0A1A52">
<link rel="icon" href="/assets/img/favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/gabarito-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/outfit-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
{preload}<link rel="stylesheet" href="/assets/style.css">
{jsonld(*donnees) if donnees else ""}
</head>
<body>
{entete(actif or chemin)}
<main id="contenu">
{corps}
</main>
{BARRE}
{pied()}
{COOKIES}
{js}</body>
</html>
'''
    if mots_min:
        parties = re.findall(r'<p class="chapo">.*?</p>|<article class="article">.*?</article>|<div class="faq">.*?</div>\s*</section>', corps, re.S)
        texte = re.sub(r"<[^>]+>", " ", " ".join(parties))
        nb = len(re.findall(r"[A-Za-zÀ-ÿœ’'-]+", html.unescape(texte)))
        assert nb >= mots_min, f"{chemin} : {nb} mots, minimum {mots_min}"
        print(f"  {chemin} : {nb} mots")
    dossier = os.path.join(SORTIE, chemin.strip("/")) if chemin not in ("/", "/404.html") else SORTIE
    os.makedirs(dossier, exist_ok=True)
    fichier = os.path.join(SORTIE, "404.html") if chemin == "/404.html" else os.path.join(dossier, "index.html")
    with open(fichier, "w", encoding="utf8") as f:
        f.write(doc)
    if not noindex:
        PAGES.append(chemin)

def img(nom, alt, l, h, classe="", lazy=True, sizes=None):
    a = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    s = f' sizes="{sizes}"' if sizes else ""
    c = f' class="{classe}"' if classe else ""
    return f'<img{c} src="/assets/img/{nom}.webp" alt="{e(alt)}" width="{l}" height="{h}"{a}{s}>'

ASIDE = lambda service, cle: f'''    <aside class="aside-devis" aria-label="Demander un devis">
      <h2>Devis gratuit</h2>
      <p>{service} : décrivez votre besoin, nous vous rappelons pour en parler concrètement.</p>
      <a class="btn btn-action" href="/estimation/?service={cle}">Estimer en 2 minutes</a>
      <a class="btn btn-clair btn-tel" href="{TEL_LIEN}">{TEL}</a>
      <ul><li>Devis gratuit et sans engagement</li><li>Visite sur place avant chiffrage</li><li>Toute l’Île-de-France</li></ul>
    </aside>'''

def autres_services(sauf):
    liens = "\n".join(f'      <a href="{s["url"]}">{s["menu"]}</a>' for s in SERVICES if s["url"] != sauf)
    return f'''  <section class="section section-blanche" aria-labelledby="autres-titre">
    <div class="conteneur">
      <h2 id="autres-titre" style="margin-bottom:1.4rem">Nos autres services</h2>
      <div class="autres">
{liens}
      <a href="/estimation/?service=facade">Nettoyage de façade &amp; bardage</a>
      </div>
    </div>
  </section>'''

def cta_final(phrase, cle):
    return f'''  <section class="section">
    <div class="conteneur">
      <div class="cta-final">
        <div>
          <h2>{phrase}</h2>
          <p>Devis gratuit et sans engagement, établi après une visite sur place. Toute l’Île-de-France.</p>
        </div>
        <div class="groupe-btn">
          <a class="btn btn-action" href="/estimation/?service={cle}">Demander un devis gratuit</a>
          <a class="btn btn-contour btn-tel" href="{TEL_LIEN}">{TEL}</a>
        </div>
      </div>
    </div>
  </section>'''

def page_service(s, titre, description, og, h1, chapo, bandeau, bandeau_alt, legende, article, questions, phrase_finale, type_service):
    fil_html, fil_ld = fil_ariane([("Services", "/#services"), (s["menu"], s["url"])])
    faq_html, faq_ld = faq(questions)
    corps = f'''  {fil_html}
  <section class="page-tete conteneur">
    <p class="surtitre">{VILLE} · Seine-Saint-Denis · Toute l’Île-de-France</p>
    <h1>{h1}</h1>
    <p class="chapo">{chapo}</p>
    <div class="groupe-btn">
      <a class="btn btn-action" href="/estimation/?service={s["cle"]}">Devis gratuit</a>
      <a class="btn btn-contour btn-tel" href="{TEL_LIEN}">{TEL}</a>
    </div>
  </section>
  <div class="conteneur">
    <figure>
      <div class="bandeau">{img(bandeau, bandeau_alt, 1200, 600, lazy=False, sizes="(max-width:1220px) 100vw, 1180px")}</div>
      <figcaption class="legende">{legende}</figcaption>
    </figure>
  </div>
  <div class="conteneur mise-en-page">
    <article class="article">
{article}
    </article>
{ASIDE(s["menu"], s["cle"])}
  </div>
  <section class="section section-blanche" aria-labelledby="faq-titre">
    <div class="conteneur" style="max-width:860px">
      <p class="surtitre">Questions fréquentes</p>
      <h2 id="faq-titre" style="margin-bottom:1.4rem">{s["menu"]} : vos questions</h2>
      {faq_html}
    </div>
  </section>
{cta_final(phrase_finale, s["cle"])}
{autres_services(s["url"])}'''
    service_ld = {"@context": "https://schema.org", "@type": "Service", "name": h1.replace("&nbsp;", " "),
                  "serviceType": type_service, "description": re.sub(r"<[^>]+>", "", chapo),
                  "provider": FOURNISSEUR, "url": SITE + s["url"],
                  "areaServed": [{"@type": "City", "name": v} for v in VILLES] + [{"@type": "AdministrativeArea", "name": "Île-de-France"}],
                  "offers": {"@type": "Offer", "description": "Devis gratuit et sans engagement, après visite sur place"}}
    page(s["url"], titre, description, og, corps, (service_ld, fil_ld, faq_ld),
         preload=f'<link rel="preload" as="image" href="/assets/img/{bandeau}.webp" fetchpriority="high">\n', mots_min=600)

# ==========================================================================
# PAGE D'ACCUEIL
# ==========================================================================
ICONES = {
    "eclair": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M13 2 4 14h7l-1 8 9-12h-7z"/></svg>',
    "niveau": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 9h18v6H3z"/><path d="M10 12h4"/><path d="M7 9V6M17 9V6"/></svg>',
    "devis": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/><path d="m9 14 2 2 4-4"/></svg>',
}

def carte(c, titre_balise="h3"):
    return f'''        <article class="carte revele">
          {img(c["carte"], c["titre"] + " à " + VILLE + " par " + NOM, 640, 427, sizes="(max-width:699px) 100vw, (max-width:959px) 50vw, 380px")}
          <div class="corps">
            <{titre_balise}>{c["titre"]}</{titre_balise}>
            <p>{c["texte"]}</p>
            <a class="lien-fleche" href="{c["url"]}">En savoir plus<span class="visuellement-cache"> : {c["titre"]}</span></a>
          </div>
        </article>'''

def accueil():
    cartes = "\n".join(carte(s) for s in SERVICES + CARTES_EN_PLUS)
    corps = f'''  <section class="hero" aria-labelledby="titre-accueil">
    <div class="hero-cadre">
      <picture class="hero-photo">
        <source media="(max-width:599px)" srcset="/assets/img/hero-mobile.webp" width="640" height="800">
        <img src="/assets/img/hero-800.webp" srcset="/assets/img/hero-800.webp 800w, /assets/img/hero-1600.webp 1500w" sizes="(max-width:1320px) 100vw, 1300px" width="1500" height="937" alt="Nettoyage de façade en nacelle à {VILLE} par l’équipe {NOM}" fetchpriority="high">
      </picture>
      <div class="hero-contenu">
        <div>
          <p class="surtitre" style="color:#9DBDFF">{VILLE} (93) · Toute l’Île-de-France</p>
          <h1 id="titre-accueil">{NOM}, votre spécialiste de l’entretien de bâtiments à <em>{VILLE}</em></h1>
          <p class="sous-titre">Carottage en urgence, corvoyage, levée de réserves, nettoyage de bureaux et de façades : nous intervenons à {VILLE}, en Seine-Saint-Denis et dans toute l’Île-de-France.</p>
          <div class="groupe-btn">
            <a class="btn btn-clair" href="#services">Découvrir nos services</a>
          </div>
        </div>
        <aside class="estimer" aria-labelledby="estimer-titre">
          <h2 id="estimer-titre">Estimez votre intervention en 2&nbsp;minutes</h2>
          <p>Quatre questions simples : nous vous rappelons pour en parler et organiser une visite.</p>
          <a class="btn btn-action" href="/estimation/">Estimer</a>
          <ul class="rassurance"><li>Devis gratuit</li><li>Sans engagement</li><li>Interlocuteur direct</li></ul>
        </aside>
      </div>
    </div>
  </section>

  <section class="confiance" aria-labelledby="confiance-titre">
    <div class="conteneur">
      <h2 id="confiance-titre" class="visuellement-cache">Ils nous font confiance</h2>
      <!-- AVIS GOOGLE : quand la fiche Google aura de vrais avis, remplacer ce bloc par la note,
           le nombre d’avis, un lien vers la fiche et 3 à 6 avis réels (texte + prénom).
           Ajouter alors "aggregateRating" au JSON-LD de cette page avec les MÊMES chiffres. -->
      <div class="confiance-grille">
        <div class="engagement reference">
          <img src="/assets/img/ref-bouygues-immobilier.webp" alt="Logo Bouygues Immobilier, client d’OF ENTRETIENS" width="450" height="171" loading="lazy">
          <p><b>Bouygues Immobilier</b> nous fait confiance : nous intervenons sur le programme « Un Balcon en Forêt ».</p>
        </div>
        <div class="engagement"><strong>Un interlocuteur direct</strong><p>Vous parlez au directeur général, qui connaît votre site et suit votre dossier.</p></div>
        <div class="engagement"><strong>Tous corps d’état</strong><p>Une seule équipe pour les reprises : pas besoin de faire revenir chaque entreprise.</p></div>
      </div>
    </div>
  </section>

  <section class="section section-blanche" aria-labelledby="pourquoi-titre">
    <div class="conteneur">
      <div class="intro">
        <p class="surtitre">Nos engagements</p>
        <h2 id="pourquoi-titre">Pourquoi choisir {NOM}&nbsp;?</h2>
      </div>
      <div class="atouts">
        <article class="atout revele">
          <div class="icone">{ICONES["eclair"]}</div>
          <h3>Réactivité</h3>
          <p>Un imprévu sur un chantier ou un site&nbsp;? Nous nous mobilisons en délai court, et nous vous disons franchement quand nous pouvons être là.</p>
        </article>
        <article class="atout revele">
          <div class="icone">{ICONES["niveau"]}</div>
          <h3>Travail soigné</h3>
          <p>Tous corps d’état maîtrisés, zone laissée propre, photos de l’intervention : vous voyez exactement ce qui a été fait.</p>
        </article>
        <article class="atout revele">
          <div class="icone">{ICONES["devis"]}</div>
          <h3>Devis gratuit et sans engagement</h3>
          <p>Nous venons voir sur place, nous définissons le périmètre avec vous, puis nous chiffrons. Vous savez ce qui est inclus.</p>
        </article>
      </div>
      <a class="btn btn-action btn-tel" href="{TEL_LIEN}">Appeler le {TEL}</a>
    </div>
  </section>

  <section class="section" id="services" aria-labelledby="services-titre">
    <div class="conteneur">
      <div class="intro">
        <p class="surtitre">Ce que nous faisons</p>
        <h2 id="services-titre">Nos services à {VILLE} et en Île-de-France</h2>
        <p>Du chantier à l’entrepôt : préparer, réparer, nettoyer et dépanner, avec la même exigence partout.</p>
      </div>
      <div class="cartes">
{cartes}
      </div>
    </div>
  </section>

  <section class="section section-blanche" aria-labelledby="realisations-titre">
    <div class="conteneur">
      <div class="intro">
        <p class="surtitre">Sur le terrain</p>
        <h2 id="realisations-titre">Nos réalisations</h2>
        <p>Des photos prises sur nos chantiers et nos sites d’intervention, sans mise en scène.</p>
      </div>
      <div class="galerie">
        <figure class="large revele">{img("reserve-detail", "Levée de réserves sur une menuiserie avant livraison à " + VILLE, 1000, 1333, sizes="(max-width:599px) 100vw, 66vw")}<figcaption>Réserves : constat, reprise, contrôle</figcaption></figure>
        <figure class="revele"><span class="etiquette">Avant</span>{img("avant-soubassement", "Soubassement d’une résidence avant reprise d’enduit", 1000, 562, sizes="(max-width:599px) 50vw, 33vw")}<figcaption>Soubassement à reprendre</figcaption></figure>
        <figure class="revele"><span class="etiquette apres">Après</span>{img("apres-soubassement", "Même soubassement après reprise d’enduit par OF ENTRETIENS", 1000, 750, sizes="(max-width:599px) 50vw, 33vw")}<figcaption>Enduit repris, finition propre</figcaption></figure>
        <figure class="revele">{img("reprise-platrerie", "Reprise de plâtrerie autour de gaines techniques après carottage", 1000, 1333, sizes="(max-width:599px) 50vw, 33vw")}<figcaption>Reprise autour de gaines</figcaption></figure>
        <figure class="revele">{img("toiture-site-logistique", "Toiture terrasse d’une plateforme logistique en Île-de-France", 1000, 562, sizes="(max-width:599px) 50vw, 33vw")}<figcaption>Toiture terrasse logistique</figcaption></figure>
        <figure class="revele">{img("reprise-allege", "Reprise d’allège et de plâtrerie autour d’une fenêtre", 1000, 1287, sizes="(max-width:599px) 50vw, 33vw")}<figcaption>Reprise d’allège</figcaption></figure>
      </div>
      <p style="margin-top:1.6rem"><a class="lien-fleche" href="/realisations/">Voir toutes nos réalisations</a></p>
    </div>
  </section>

  <section class="section">
    <div class="conteneur">
      <div class="urgence">
        <div>
          <p class="pastille">Urgence chantier</p>
          <h2>Un carottage bloque votre chantier&nbsp;? Une livraison approche&nbsp;?</h2>
          <p>Appelez-nous : nous vous disons tout de suite si et quand nous pouvons intervenir. Pas de promesse intenable, un délai que nous savons tenir.</p>
        </div>
        <div class="groupe-btn">
          <a class="btn btn-action btn-tel" href="{TEL_LIEN}">{TEL}</a>
          <a class="btn btn-clair" href="/carottage-urgence-montfermeil/">Carottage en urgence</a>
        </div>
      </div>
    </div>
  </section>

  <section class="section section-blanche" aria-labelledby="metier-titre">
    <div class="conteneur texte-long">
      <h2 id="metier-titre">Entretien et travaux de bâtiment à {VILLE} : un seul interlocuteur</h2>
      <p>Installée à {VILLE}, en Seine-Saint-Denis, {NOM} accompagne depuis 2024 les promoteurs immobiliers, les bailleurs, les entreprises générales et les responsables de sites qui ont besoin d’un partenaire fiable pour entretenir, préparer ou remettre en état leurs bâtiments. Notre particularité&nbsp;: réunir la propreté, les travaux tous corps d’état et les interventions urgentes, pour que vous n’ayez qu’un seul numéro à appeler. Résultat&nbsp;: moins d’intermédiaires, moins de relances, et un interlocuteur qui connaît vraiment votre bâtiment.</p>
      <h3>Pour les promoteurs et les bailleurs</h3>
      <p>Avant une livraison, chaque logement doit être prêt et chaque réserve levée. Nous assurons le <a href="/corvoyage-montfermeil/">corvoyage</a>, les visites cloisons, de pré-livraison et de livraison, la levée des réserves tous corps d’état, puis le SAV et le suivi de la garantie de parfait achèvement en lieu et place de vos équipes.</p>
      <h3>Pour les chantiers et les entreprises générales</h3>
      <p>Une réservation oubliée, une gaine à faire passer, un seuil à reprendre&nbsp;: notre équipe se mobilise en délai court pour le <a href="/carottage-urgence-montfermeil/">carottage en urgence</a>, le traitement coupe-feu des gaines et les reprises de doublage ou de plâtrerie. Nous assurons aussi le nettoyage des base-vie, pour des équipes qui travaillent dans de bonnes conditions.</p>
      <h3>Pour les entreprises et les sites logistiques</h3>
      <p>Bureaux, locaux sociaux, sanitaires, façades et bardages&nbsp;: pour le <a href="/nettoyage-bureaux-montfermeil/">nettoyage de vos locaux</a>, nous définissons avec vous un périmètre clair et des créneaux qui ne gênent pas votre activité. Sur les <a href="/plateformes-logistiques/">plateformes logistiques</a>, nous intervenons en site occupé, dans le respect strict des consignes de sécurité.</p>
      <h3>{VILLE}, la Seine-Saint-Denis et toute l’Île-de-France</h3>
      <p>Depuis notre siège de {VILLE}, nous intervenons à Clichy-sous-Bois, Gagny, Livry-Gargan, Le Raincy, Chelles, Noisy-le-Grand et dans l’ensemble des départements franciliens. Chaque devis est gratuit et établi après une visite sur place&nbsp;: nous préférons comprendre votre besoin avant de chiffrer quoi que ce soit.</p>
    </div>
  </section>

  <section class="section" aria-labelledby="qui-titre">
    <div class="conteneur qui">
      <figure class="revele">{img("corvoyage-logement", "Intervenant d’OF ENTRETIENS préparant un logement neuf avant livraison", 1000, 750, sizes="(max-width:959px) 100vw, 560px")}</figure>
      <div>
        <p class="surtitre">Qui sommes-nous</p>
        <h2 id="qui-titre">Une entreprise à taille humaine, un engagement direct</h2>
        <p style="margin-top:1rem">{NOM} est une entreprise créée en 2024, dont le siège est à {VILLE}. Votre interlocuteur est le directeur général lui-même&nbsp;: il connaît votre site, suit votre dossier et vous répond directement.</p>
        <p>Notre façon de travailler tient en une phrase&nbsp;: comprendre d’abord, intervenir ensuite. Nous visitons, nous définissons un périmètre clair, nous respectons vos règles — et quand un imprévu survient, vous l’apprenez de nous, tout de suite.</p>
        <div class="groupe-btn">
          <a class="btn btn-contour" href="/qui-sommes-nous/">En savoir plus</a>
          <a class="btn btn-action btn-tel" href="{TEL_LIEN}">{TEL}</a>
        </div>
      </div>
    </div>
  </section>'''
    entreprise = {
        "@context": "https://schema.org", "@type": "HomeAndConstructionBusiness", "@id": SITE + "/#entreprise",
        "name": NOM, "legalName": NOM, "url": SITE + "/", "telephone": TEL_INTL, "email": EMAIL,
        "image": SITE + "/assets/img/og-accueil.jpg", "logo": SITE + "/assets/img/logo.jpg",
        "description": "Carottage en urgence, corvoyage, levée de réserves, nettoyage de bureaux, de base-vie et de façades, maintenance de plateformes logistiques à Montfermeil et en Île-de-France.",
        "address": ADRESSE, "foundingDate": "2024-03-22", "vatID": "FR80927491357",
        "identifier": {"@type": "PropertyValue", "propertyID": "SIREN", "value": "927491357"},
        "areaServed": [{"@type": "City", "name": v} for v in VILLES] + [{"@type": "AdministrativeArea", "name": "Île-de-France"}],
        "sameAs": [INSTAGRAM],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["titre"], "url": SITE + s["url"]}} for s in SERVICES]},
        # Horaires et fiche Google à ajouter dès qu'ils sont connus (voir docs/checklist-mise-en-ligne.md)
    }
    page("/", "Entretien de bâtiments à Montfermeil – OF ENTRETIENS",
         "Carottage en urgence, corvoyage, nettoyage de bureaux et de façades à Montfermeil et en Île-de-France. Devis gratuit : appelez le 06 62 06 93 22.",
         "og-accueil.jpg", corps, (entreprise,),
         preload='<link rel="preload" as="image" href="/assets/img/hero-mobile.webp" media="(max-width:599px)" fetchpriority="high">\n'
                 '<link rel="preload" as="image" imagesrcset="/assets/img/hero-800.webp 800w, /assets/img/hero-1600.webp 1500w" imagesizes="(max-width:1320px) 100vw, 1300px" media="(min-width:600px)" fetchpriority="high">\n')

# ==========================================================================
# PAGES DE SERVICE
# ==========================================================================
def service_carottage():
    s = SERVICES[0]
    article = f'''      <section>
        <h2>Quand faire appel à nous&nbsp;?</h2>
        <p>Un carottage, ce ne sont souvent que quelques percements. Mais quand il manque, ce sont des corps d’état bloqués, un planning qui glisse et parfois une date de livraison menacée. Voici les situations pour lesquelles on nous appelle le plus souvent&nbsp;:</p>
        <ul class="liste-coche">
          <li><b>Une réservation manquante ou mal placée</b>&nbsp;: le passage prévu n’existe pas, ou pas au bon endroit, et les réseaux ne peuvent pas passer.</li>
          <li><b>Des gaines et des réseaux à faire traverser</b> une dalle ou un voile pour que les lots suivants puissent avancer.</li>
          <li><b>Une livraison qui approche</b>&nbsp;: la remise des clés ne bouge pas, le point bloquant doit être traité maintenant.</li>
          <li><b>Une reprise à faire autour du percement</b>&nbsp;: rebouchage, traitement coupe-feu, doublage, pour un ouvrage conforme et propre.</li>
        </ul>
      </section>
      <section>
        <h2>Le déroulé de l’intervention</h2>
        <ol class="etapes">
          <li><strong>Vous nous appelez ou vous remplissez l’estimation.</strong> Indiquez le support (dalle, voile, mur), le nombre et l’emplacement des carottages, l’adresse du chantier et l’échéance. Quelques photos nous aident beaucoup.</li>
          <li><strong>Nous vérifions ensemble les points sensibles.</strong> Plans, emplacement exact des percements, accès au chantier, consignes de sécurité et horaires autorisés.</li>
          <li><strong>Nous vous donnons une date réaliste.</strong> Pas de promesse intenable&nbsp;: un délai que nous savons tenir, annoncé clairement.</li>
          <li><strong>Nous carottons et nous traitons les reprises.</strong> Selon le besoin&nbsp;: traitement coupe-feu des gaines, rebouchage, pose de doublage avec bandes, reprise de plâtrerie.</li>
          <li><strong>Nous laissons la zone propre et nous envoyons les photos.</strong> Vous savez ce qui a été fait, et le chantier peut reprendre.</li>
        </ol>
      </section>
      <section>
        <h2>Le matériel que nous apportons</h2>
        <p>Nous venons avec le matériel de carottage adapté au support, de quoi protéger la zone de travail et de quoi traiter les reprises dans la foulée&nbsp;: produits coupe-feu, plaques de doublage, bandes et enduits. Résultat&nbsp;: une seule intervention au lieu de trois entreprises qui se succèdent.</p>
        <p>Les diamètres et les épaisseurs possibles dépendent de votre chantier&nbsp;: nous les confirmons avec vous au téléphone, avant de nous déplacer.</p>
      </section>
      <section>
        <h2>Délai et préparation&nbsp;: ce qui fait gagner du temps</h2>
        <p>Un carottage ne se programme pas à une fréquence régulière&nbsp;: il se traite au moment où il bloque. Ce qui accélère vraiment les choses, c’est la préparation&nbsp;:</p>
        <ul class="liste-coche">
          <li>les plans ou un croquis avec l’emplacement des percements&nbsp;;</li>
          <li>des photos du support et de son environnement&nbsp;;</li>
          <li>le nom d’un contact sur place et les horaires d’accès&nbsp;;</li>
          <li>les reprises attendues après le percement (coupe-feu, doublage, finitions).</li>
        </ul>
      </section>
      <section>
        <h2>Combien coûte un carottage à {VILLE}&nbsp;?</h2>
        <p>Chaque chantier est différent, c’est pourquoi nous établissons un devis gratuit plutôt qu’un tarif unique. Le prix dépend principalement&nbsp;:</p>
        <ul class="liste-coche">
          <li>du nombre de carottages et de leur diamètre&nbsp;;</li>
          <li>de l’épaisseur et de la nature du support (béton, béton armé, maçonnerie)&nbsp;;</li>
          <li>de l’accessibilité et de la hauteur de travail&nbsp;;</li>
          <li>des reprises à prévoir (coupe-feu, doublage, plâtrerie)&nbsp;;</li>
          <li>du délai demandé.</li>
        </ul>
        <p>Vous recevez un devis clair, avec ce qui est inclus et ce qui ne l’est pas. Pas de surprise à la facture.</p>
        <div class="encadre">
          <span class="titre">Exemple réel</span>
          <p>Un imprévu bloquait l’avancement d’un chantier&nbsp;: notre équipe s’est mobilisée en délai court pour réaliser <b>5 carottages</b>, poser un <b>panneau de doublage avec bandes</b>, rectifier un <b>seuil d’ascenseur</b> et traiter le <b>coupe-feu de plusieurs gaines</b>. Le chantier a pu reprendre dans de bonnes conditions.</p>
        </div>
        <div class="encadre franchise">
          <span class="titre">Ce que nous ne promettons pas</span>
          <p>Nous n’affichons pas de «&nbsp;24h/24&nbsp;» ni de délai garanti. Quand vous appelez, nous vous disons franchement quand nous pouvons être sur place — et nous tenons ce que nous annonçons.</p>
        </div>
      </section>'''
    questions = [
        ("Intervenez-vous vraiment en urgence pour un carottage ?",
         "Oui. Quand un carottage manque et bloque un chantier, nous nous mobilisons en délai court à Montfermeil et dans toute l’Île-de-France. Nous ne promettons pas de délai garanti : au téléphone, nous vous disons franchement quand nous pouvons être sur place."),
        ("Traitez-vous le coupe-feu après le carottage ?",
         "Oui. Nous réalisons le traitement coupe-feu des gaines traversantes après le passage des réseaux, ainsi que les reprises autour de l’ouvrage : rebouchage, doublage avec bandes, plâtrerie."),
        ("Quelles informations préparer avant d’appeler ?",
         "Le support à percer (dalle, voile, mur), le nombre et l’emplacement des carottages, l’adresse du chantier, l’échéance et, si possible, des photos et les plans. Nous pouvons ainsi vous répondre vite et précisément."),
        ("Le devis est-il gratuit ?",
         "Oui, le devis est gratuit et sans engagement. Il détaille le nombre de carottages, les reprises prévues et ce qui est inclus, pour que vous puissiez décider en toute clarté."),
    ]
    page_service(s, "Carottage en urgence à Montfermeil – OF ENTRETIENS",
                 "Carottage en urgence à Montfermeil et en Île-de-France : percements, coupe-feu, reprises. Devis gratuit, appelez le 06 62 06 93 22.",
                 "og-carottage.jpg", f"Carottage en urgence à {VILLE} et en Île-de-France",
                 f"Une réservation oubliée, une gaine à faire passer, une livraison qui approche&nbsp;: quand un carottage manque, tout le chantier attend. {NOM} se mobilise en délai court depuis {VILLE} et traite aussi ce qui va avec&nbsp;: coupe-feu, rebouchage, doublage.",
                 "bandeau-carottage", "Reprise de plâtrerie autour de gaines techniques après un carottage à " + VILLE,
                 "Reprise de plâtrerie autour de gaines techniques — photo prise sur un de nos chantiers.",
                 article, questions, "Un carottage bloque votre chantier&nbsp;?", "Carottage en urgence sur chantier")

def service_corvoyage():
    s = SERVICES[1]
    article = f'''      <section>
        <h2>Le corvoyage, qu’est-ce que c’est&nbsp;?</h2>
        <p>Le corvoyage consiste à préparer et à suivre les logements d’une opération immobilière avant et après leur livraison&nbsp;: contrôler l’état de chaque logement, réaliser les reprises de finitions, suivre chaque réserve jusqu’à sa levée et récupérer les quitus. Le corvoyeur est l’intervenant qui permet au promoteur ou au bailleur de livrer à la date prévue, sans faire revenir chaque corps d’état.</p>
        <p>{NOM} intervient pour les promoteurs immobiliers, les bailleurs et les entreprises générales, à {VILLE} et dans toute l’Île-de-France. Bouygues Immobilier nous fait confiance sur le programme «&nbsp;Un Balcon en Forêt&nbsp;».</p>
      </section>
      <section>
        <h2>Nos missions de corvoyage et de levée de réserves</h2>
        <ul class="liste-coche">
          <li><b>Préparation des logements avant livraison</b> et levée de réserves tous corps d’état, logement par logement.</li>
          <li><b>Visites cloisons, de pré-livraison et de livraison</b>, pour les promoteurs comme pour les bailleurs, avec présence le jour de la remise des clés.</li>
          <li><b>Prise de rendez-vous client par une personne dédiée</b>&nbsp;: vos acquéreurs et vos locataires ont un interlocuteur identifié.</li>
          <li><b>Réalisation des travaux</b>, y compris en limite de prestation&nbsp;: plâtrerie, menuiseries intérieures et extérieures, sols durs et souples, peinture, serrurerie, gros œuvre, plomberie, électricité.</li>
          <li><b>Transmission des quitus et reportage photos</b> de chaque intervention.</li>
          <li><b>Démarches liées aux demandes de mairie</b>, prises en charge pour votre compte.</li>
        </ul>
      </section>
      <section>
        <h2>Le déroulé, de la visite cloisons au dernier quitus</h2>
        <ol class="etapes">
          <li><strong>Visite cloisons.</strong> Au stade du cloisonnement, nous vérifions les implantations pendant qu’il est encore temps d’ajuster.</li>
          <li><strong>Visite de pré-livraison.</strong> Passage en revue complet de chaque logement, constat des réserves et organisation des reprises avant le jour J.</li>
          <li><strong>Livraison.</strong> Présence le jour de la remise des clés aux acquéreurs ou aux locataires, pour une livraison dans de bonnes conditions.</li>
          <li><strong>Levée des réserves.</strong> Du constat à la reprise, jusqu’au contrôle final et à la transmission du quitus.</li>
          <li><strong>SAV et GPA.</strong> Suivi des réserves à J+30 et pendant la garantie de parfait achèvement, en lieu et place de vos équipes.</li>
        </ol>
      </section>
      <section>
        <h2>Nos outils de suivi</h2>
        <p>Vous savez à tout moment où en est chaque logement. Nous assurons le pointage régulier des réserves sur votre logiciel ou sur Excel, le reportage photos de chaque levée et la coordination avec tous les intervenants&nbsp;: maîtrise d’ouvrage, MOEX, OPC, entreprises, clients, bailleurs et syndics. Nous vous accompagnons aussi lors des expertises.</p>
        <p>Côté terrain, une équipe qui maîtrise l’ensemble des corps d’état réalise les reprises&nbsp;: une réserve ne reste pas en attente d’un sous-traitant.</p>
      </section>
      <section>
        <h2>À quel moment nous solliciter&nbsp;?</h2>
        <p>Le plus tôt est le mieux&nbsp;: idéalement dès la visite cloisons, et au plus tard avant la visite de pré-livraison. Plus nous intervenons en amont, plus les réserves sont traitées tôt et plus la livraison se passe sereinement. Nous pouvons aussi reprendre une opération en cours, quand les réserves s’accumulent ou que la date de livraison se rapproche.</p>
      </section>
      <section>
        <h2>Quel prix pour une mission de corvoyage&nbsp;?</h2>
        <p>Chaque opération est différente&nbsp;: nous établissons un devis gratuit après avoir vu le programme. Le prix dépend notamment&nbsp;:</p>
        <ul class="liste-coche">
          <li>du nombre de logements et de leur typologie&nbsp;;</li>
          <li>du volume de réserves et des corps d’état concernés&nbsp;;</li>
          <li>des visites à assurer (cloisons, pré-livraison, livraison)&nbsp;;</li>
          <li>de la durée du suivi SAV et GPA&nbsp;;</li>
          <li>du calendrier de l’opération.</li>
        </ul>
        <div class="encadre">
          <span class="titre">Référence</span>
          <p>Nous intervenons actuellement pour <b>Bouygues Immobilier</b> sur le programme «&nbsp;Un Balcon en Forêt&nbsp;» (SCCV), en Île-de-France.</p>
        </div>
      </section>'''
    questions = [
        ("Qu’est-ce qu’un corvoyeur ?",
         "Le corvoyeur prépare et suit les logements d’une opération avant leur livraison : contrôle de l’état, reprises de finitions, suivi des réserves jusqu’à leur levée et récupération des quitus. Il est l’interlocuteur du promoteur sur cette dernière ligne droite."),
        ("Faites-vous les visites pour les promoteurs et les bailleurs ?",
         "Oui. Nous réalisons les visites cloisons, de pré-livraison et de livraison pour les promoteurs immobiliers comme pour les bailleurs, et nous sommes présents le jour de la remise des clés."),
        ("Assurez-vous le SAV et le suivi pendant la GPA ?",
         "Oui, en lieu et place de vos équipes : suivi des réserves à J+30 et pendant la garantie de parfait achèvement, pointage sur logiciel ou Excel, coordination des intervenants, prise de rendez-vous par une personne dédiée et accompagnement lors des expertises."),
        ("Intervenez-vous en dehors de Montfermeil ?",
         "Oui, partout en Île-de-France : Paris (75), Seine-et-Marne (77), Yvelines (78), Essonne (91), Hauts-de-Seine (92), Seine-Saint-Denis (93), Val-de-Marne (94) et Val-d’Oise (95)."),
    ]
    page_service(s, "Corvoyage et réserves à Montfermeil – OF ENTRETIENS",
                 "Corvoyage, visites de livraison, levée de réserves, SAV et GPA à Montfermeil et en Île-de-France. Devis gratuit au 06 62 06 93 22.",
                 "og-corvoyage.jpg", f"Corvoyage et levée de réserves à {VILLE}",
                 "Entre la fin du chantier et la remise des clés, tout se joue vite. Nous préparons les logements, levons les réserves tous corps d’état jusqu’au dernier quitus et assurons le SAV et la GPA à votre place.",
                 "bandeau-corvoyage", "Programme immobilier neuf en cours de livraison en Île-de-France, suivi en corvoyage",
                 "«&nbsp;Un Balcon en Forêt&nbsp;» (SCCV — Bouygues Immobilier), programme sur lequel nous intervenons. Photo prise sur site.",
                 article, questions, "Une livraison à préparer&nbsp;?", "Corvoyage, levée de réserves, SAV et GPA")

def service_nettoyage():
    s = SERVICES[2]
    article = f'''      <section>
        <h2>Des locaux propres, sans y penser</h2>
        <p>Des bureaux nets, des sanitaires impeccables, une base-vie de chantier où les équipes se changent et déjeunent dans de bonnes conditions&nbsp;: c’est autant une question d’image que de respect des personnes. {NOM} assure l’entretien de vos espaces à {VILLE} et dans toute l’Île-de-France, en régulier ou en ponctuel, selon un périmètre défini ensemble et tenu dans la durée.</p>
      </section>
      <section>
        <h2>Ce que nous entretenons</h2>
        <h3>Bureaux et locaux professionnels</h3>
        <ul class="liste-coche">
          <li>Postes de travail, salles de réunion, espaces d’accueil&nbsp;;</li>
          <li>sanitaires, cuisines et espaces de pause&nbsp;;</li>
          <li>parties communes, circulations et zones de passage&nbsp;;</li>
          <li>vitrages accessibles et surfaces de contact.</li>
        </ul>
        <h3>Base-vie de chantier</h3>
        <ul class="liste-coche">
          <li>Vestiaires et réfectoires&nbsp;;</li>
          <li>sanitaires de chantier&nbsp;;</li>
          <li>abords et zones de stockage selon le périmètre convenu.</li>
        </ul>
      </section>
      <section>
        <h2>Comment se passe la mise en place</h2>
        <ol class="etapes">
          <li><strong>Nous visitons vos locaux.</strong> Les lieux, les usages, les horaires, les points sensibles&nbsp;: le besoin réel se comprend sur place.</li>
          <li><strong>Nous définissons un périmètre clair.</strong> Ce qui est inclus, ce qui ne l’est pas, à quelle fréquence et sur quels créneaux. Pas de zone grise.</li>
          <li><strong>Nous intégrons vos règles.</strong> Accès, sécurité, présence de vos équipes&nbsp;: nos intervenants arrivent préparés.</li>
          <li><strong>Nous intervenons et nous suivons la prestation.</strong> Un interlocuteur direct, des points réguliers, des ajustements quand votre activité évolue.</li>
        </ol>
      </section>
      <section>
        <h2>Produits et matériel</h2>
        <p>Nous utilisons des produits et du matériel adaptés à chaque surface et à chaque usage&nbsp;: on n’entretient pas un sanitaire de chantier comme une salle de réunion. Les besoins particuliers (zones sensibles, contraintes d’accès, demandes spécifiques) sont listés dès la visite et intégrés au devis.</p>
      </section>
      <section>
        <h2>Quelle fréquence de nettoyage choisir&nbsp;?</h2>
        <p>La bonne fréquence dépend de la fréquentation de vos locaux. À titre indicatif&nbsp;:</p>
        <ul class="liste-coche">
          <li><b>sanitaires et espaces de pause très utilisés</b>&nbsp;: un passage à chaque jour d’occupation est généralement nécessaire&nbsp;;</li>
          <li><b>bureaux à fréquentation moyenne</b>&nbsp;: deux à trois passages par semaine suffisent souvent&nbsp;;</li>
          <li><b>base-vie de chantier</b>&nbsp;: une fréquence qui suit l’effectif présent et l’avancement du chantier.</li>
        </ul>
        <p>Nous ajustons ensuite le rythme avec vous, en fonction de ce que vous constatez au quotidien.</p>
      </section>
      <section>
        <h2>Pourquoi nous confier l’entretien de vos locaux&nbsp;?</h2>
        <ul class="liste-coche">
          <li><b>Un interlocuteur direct</b>&nbsp;: vous parlez au directeur général, qui connaît vos locaux et ajuste la prestation sans intermédiaire.</li>
          <li><b>Un périmètre tenu dans la durée</b>&nbsp;: ce qui est écrit dans le devis est fait, à chaque passage, et ce qui pose problème vous est signalé.</li>
          <li><b>Le respect des personnes</b>&nbsp;: vos équipes comme les nôtres méritent des locaux propres et des conditions de travail dignes.</li>
          <li><b>Les petites réparations dans la foulée</b>&nbsp;: une poignée, une plinthe, une reprise de peinture&nbsp;? Notre équipe maîtrise aussi les travaux tous corps d’état, sans faire venir une autre entreprise.</li>
        </ul>
      </section>
      <section>
        <h2>Quel prix pour l’entretien de vos locaux&nbsp;?</h2>
        <p>Le devis est gratuit, établi après visite. Le prix dépend de la surface, du type de locaux, de la fréquence de passage, des horaires d’intervention et des prestations incluses. Vous recevez un devis détaillé, poste par poste, pour savoir exactement ce que vous payez.</p>
      </section>'''
    questions = [
        ("Intervenez-vous en régulier ou ponctuellement ?",
         "Les deux. Nous assurons l’entretien courant de vos locaux à la fréquence convenue, et nous intervenons aussi ponctuellement, par exemple avant un événement ou après des travaux."),
        ("Nettoyez-vous les base-vie de chantier ?",
         "Oui : vestiaires, réfectoires et sanitaires de chantier, pour que les équipes travaillent dans des conditions correctes. La fréquence suit l’effectif et l’avancement du chantier."),
        ("Comment est fixé le périmètre de la prestation ?",
         "Lors d’une visite sur place. Nous listons ensemble ce qui est inclus, ce qui ne l’est pas, la fréquence et les créneaux. Le tout figure noir sur blanc dans le devis gratuit."),
        ("Dans quelles villes intervenez-vous ?",
         "À Montfermeil, Clichy-sous-Bois, Gagny, Livry-Gargan, Le Raincy, Chelles, Noisy-le-Grand et dans toute l’Île-de-France."),
    ]
    page_service(s, "Nettoyage de bureaux à Montfermeil – OF ENTRETIENS",
                 "Nettoyage de bureaux, de locaux et de base-vie à Montfermeil et en Île-de-France, en régulier ou ponctuel. Devis gratuit : 06 62 06 93 22.",
                 "og-nettoyage.jpg", f"Nettoyage de bureaux, de locaux et de base-vie à {VILLE}",
                 "Bureaux, sanitaires, parties communes et base-vie de chantier&nbsp;: un entretien régulier ou ponctuel, selon un périmètre défini ensemble et respecté dans la durée.",
                 "bandeau-nettoyage", "Entretien de bureaux et de locaux professionnels à " + VILLE,
                 "Image d’illustration — à remplacer par une photo de nos équipes en intervention.",
                 article, questions, "Des locaux à entretenir&nbsp;?", "Nettoyage de bureaux, de locaux et de base-vie")

def service_logistique():
    s = SERVICES[3]
    article = f'''      <section>
        <h2>Ce que vivent les responsables de site</h2>
        <ul class="liste-coche">
          <li><b>La continuité d’activité avant tout</b>&nbsp;: les quais, les allées et les locaux doivent rester exploitables pendant les interventions.</li>
          <li><b>De la co-activité permanente</b>&nbsp;: caristes, préparateurs, transporteurs, toute intervention doit composer avec les flux.</li>
          <li><b>Des règles de sécurité strictes</b>&nbsp;: plan de circulation, équipements, consignes d’accès.</li>
          <li><b>Des horaires contraints</b>&nbsp;: les créneaux utiles sont ceux qui ne perturbent pas l’exploitation.</li>
        </ul>
      </section>
      <section>
        <h2>Propreté au quotidien</h2>
        <p>Nettoyage et entretien courant des bureaux, locaux sociaux, sanitaires, vestiaires et zones de passage du site, planifiés avec vous sur les créneaux qui respectent vos pics d’activité. Vos règles de sécurité, d’accès et de circulation sont intégrées avant la première intervention.</p>
      </section>
      <section>
        <h2>Maintenance, urgences et sinistres</h2>
        <ul class="liste-coche">
          <li><b>Intervention d’urgence après sinistre</b>, documentée (constats, photos) pour appuyer votre demande d’assurance.</li>
          <li><b>Reprise de défauts d’étanchéité</b>, toiture terrasse comprise (entretien et réparation).</li>
          <li><b>Fixations et équipements</b>&nbsp;: reprise de fixations de spots et de luminaires.</li>
          <li><b>Nettoyage de bardage</b> et réparations ponctuelles.</li>
        </ul>
      </section>
      <section>
        <h2>Aménagements et installations</h2>
        <ul class="liste-coche">
          <li>Aménagement de bureaux, de cafétéria et de locaux sociaux&nbsp;;</li>
          <li>pose de signalétique et marquage au sol&nbsp;;</li>
          <li>menuiserie intérieure&nbsp;: portes, cloisons et agencements&nbsp;;</li>
          <li>petits travaux tous corps d’état&nbsp;: maçonnerie, plâtrerie, serrurerie, carottage.</li>
        </ul>
        <div class="encadre">
          <span class="titre">Notre méthode</span>
          <p>Nous visitons d’abord votre site pour comprendre les zones, les flux et les consignes. Les interventions sont ensuite planifiées avec vous, et nos intervenants arrivent préparés aux règles du site.</p>
        </div>
      </section>
      <section>
        <h2>Sécurité et co-activité&nbsp;: nos règles sur votre site</h2>
        <ul class="liste-coche">
          <li>Nous suivons l’accueil sécurité de votre site avant la première intervention.</li>
          <li>Nous respectons le plan de circulation, les zones balisées et les priorités des engins.</li>
          <li>Nous coordonnons nos horaires avec vos équipes pour ne jamais bloquer un quai ou une allée.</li>
          <li>Nous signalons immédiatement tout risque ou toute anomalie constatée pendant l’intervention.</li>
          <li>Nous laissons les zones de travail propres, dégagées et prêtes à être exploitées.</li>
        </ul>
      </section>
      <section>
        <h2>Un seul prestataire plutôt que cinq</h2>
        <p>Sur un site logistique, multiplier les prestataires, c’est multiplier les accueils sécurité, les plans de prévention et les interlocuteurs à relancer. {NOM} réunit la propreté, la maintenance courante, les urgences et les petits aménagements&nbsp;: un seul numéro, un seul interlocuteur qui connaît votre site, et des interventions qui s’enchaînent sans temps mort.</p>
      </section>
      <section>
        <h2>À quelle fréquence intervenir&nbsp;?</h2>
        <p>La propreté des bureaux, des locaux sociaux et des sanitaires se planifie à la fréquence qui correspond à vos effectifs et à vos horaires&nbsp;: elle est fixée ensemble lors de la visite, puis ajustée si votre activité évolue. Les travaux de maintenance et les aménagements se programment à la demande, et les urgences se traitent dès votre appel, avec une date d’intervention annoncée franchement.</p>
      </section>
      <section>
        <h2>Quel prix pour l’entretien d’une plateforme logistique&nbsp;?</h2>
        <p>Le devis est gratuit et établi après la visite de votre site. Le prix dépend des surfaces à entretenir, de la fréquence de passage, des créneaux imposés par l’exploitation, de la nature des travaux de maintenance et des contraintes d’accès ou de sécurité. Vous recevez un devis détaillé, avec ce qui est inclus et ce qui ne l’est pas.</p>
      </section>'''
    questions = [
        ("Intervenez-vous en urgence après un sinistre ?",
         "Oui. Nous nous mobilisons en délai court pour remettre en état, et nous documentons l’intervention (constats, photos) pour appuyer votre demande auprès de votre assurance."),
        ("Pouvez-vous traiter un défaut d’étanchéité ?",
         "Oui, y compris en toiture terrasse : entretien et réparation, pour protéger les marchandises et l’exploitation."),
        ("Comment intervenez-vous sans perturber l’exploitation ?",
         "Nous visitons d’abord le site, puis nous planifions les interventions avec vous sur des créneaux qui évitent vos pics d’activité, dans le respect des consignes de sécurité."),
        ("Le devis est-il gratuit ?",
         "Oui, le devis est gratuit et sans engagement, établi après une visite de votre site."),
    ]
    fil_html, fil_ld = fil_ariane([("Services", "/#services"), (s["menu"], s["url"])])
    faq_html, faq_ld = faq(questions)
    corps = f'''  {fil_html}
  <section class="page-tete conteneur">
    <p class="surtitre">Plateformes logistiques et entrepôts · Toute l’Île-de-France</p>
    <h1>Plateformes logistiques&nbsp;: intervenir sans gêner l’exploitation</h1>
    <p class="chapo">Propreté au quotidien, maintenance en site occupé, urgence après sinistre, étanchéité, aménagements&nbsp;: une seule équipe, organisée autour de vos flux et de vos consignes.</p>
    <div class="groupe-btn">
      <a class="btn btn-action" href="/estimation/?service=logistique">Devis gratuit</a>
      <a class="btn btn-contour btn-tel" href="{TEL_LIEN}">{TEL}</a>
    </div>
  </section>
  <div class="conteneur">
    <figure>
      <div class="bandeau">{img("bandeau-logistique", "Toiture terrasse d’une plateforme logistique entretenue par OF ENTRETIENS", 1200, 600, lazy=False)}</div>
      <figcaption class="legende">Toiture terrasse d’un site logistique — photo prise sur site.</figcaption>
    </figure>
  </div>
  <div class="conteneur mise-en-page">
    <article class="article">
{article}
    </article>
{ASIDE("Plateforme logistique", "logistique")}
  </div>
  <section class="section section-blanche" aria-labelledby="faq-titre">
    <div class="conteneur" style="max-width:860px">
      <p class="surtitre">Questions fréquentes</p>
      <h2 id="faq-titre" style="margin-bottom:1.4rem">Plateformes logistiques : vos questions</h2>
      {faq_html}
    </div>
  </section>
{cta_final("Et si on commençait par une visite de votre site&nbsp;?", "logistique")}
{autres_services(s["url"])}'''
    service_ld = {"@context": "https://schema.org", "@type": "Service", "name": "Propreté, maintenance et urgences pour plateformes logistiques",
                  "serviceType": "Entretien et maintenance de plateformes logistiques", "provider": FOURNISSEUR, "url": SITE + s["url"],
                  "areaServed": {"@type": "AdministrativeArea", "name": "Île-de-France"}}
    page(s["url"], "Plateformes logistiques en Île-de-France – OF ENTRETIENS",
         "Propreté, maintenance, urgences et étanchéité pour plateformes logistiques en Île-de-France. Devis gratuit après visite : 06 62 06 93 22.",
         "og-logistique.jpg", corps, (service_ld, fil_ld, faq_ld),
         preload='<link rel="preload" as="image" href="/assets/img/bandeau-logistique.webp" fetchpriority="high">\n', mots_min=600)

# ==========================================================================
# ESTIMATION (formulaire en plusieurs étapes)
# ==========================================================================
def estimation():
    fil_html, fil_ld = fil_ariane([("Estimation gratuite", "/estimation/")])
    options = [("carottage", "Carottage en urgence", "Percement, coupe-feu, reprises"),
               ("corvoyage", "Corvoyage et levée de réserves", "Logements, visites, SAV et GPA"),
               ("nettoyage", "Nettoyage de bureaux, locaux ou base-vie", "Régulier ou ponctuel"),
               ("logistique", "Plateforme logistique", "Propreté, maintenance, urgences"),
               ("facade", "Nettoyage de façade ou de bardage", "Bâtiments, résidences, entrepôts"),
               ("autre", "Autres travaux", "Tous corps d’état")]
    choix = "\n".join(f'''          <label><input type="radio" name="service" value="{v}" data-cle="{k}" required><span class="rond"></span><span>{v}<small>{d}</small></span></label>''' for k, v, d in options)
    surfaces = ["Moins de 50 m²", "50 à 200 m²", "200 à 1 000 m²", "Plus de 1 000 m²", "Je ne sais pas / sans objet"]
    choix_surface = "\n".join(f'''          <label><input type="radio" name="surface" value="{v}" required><span class="rond"></span><span>{v}</span></label>''' for v in surfaces)
    delais = ["Urgent (quelques jours)", "Sous 2 semaines", "Dans le mois", "Pas pressé"]
    choix_delai = "\n".join(f'''          <label><input type="radio" name="delai" value="{v}" required><span class="rond"></span><span>{v}</span></label>''' for v in delais)
    corps = f'''  {fil_html}
  <section class="page-tete conteneur" style="text-align:center">
    <p class="surtitre">Devis gratuit et sans engagement</p>
    <h1 style="margin-inline:auto">Estimez votre intervention en 2&nbsp;minutes</h1>
    <p class="chapo" style="margin-inline:auto">Quatre étapes, puis nous vous rappelons pour en parler et organiser une visite. Pour une urgence, appelez directement le <a href="{TEL_LIEN}">{TEL}</a>.</p>
  </section>
  <div class="conteneur" style="padding-bottom:clamp(48px,7vw,88px)">
    <div class="estimation carte-blanche">
      <div class="progression" aria-live="polite">
        <div class="progression-info"><span>Étape 1 sur 4</span><span>Votre besoin</span></div>
        <div class="progression-barre" role="presentation"><span></span></div>
      </div>
      <form class="formulaire" id="form-estimation" name="estimation" method="POST" action="/merci/" data-netlify="true" netlify-honeypot="site-web">
        <input type="hidden" name="form-name" value="estimation">
        <p class="pot-de-miel"><label>Ne pas remplir<input name="site-web" tabindex="-1" autocomplete="off"></label></p>

        <fieldset class="etape active">
          <legend>1. Quel est votre besoin&nbsp;?</legend>
          <div class="choix deux">
{choix}
          </div>
        </fieldset>

        <fieldset class="etape">
          <legend>2. Quelle est l’ampleur des travaux&nbsp;?</legend>
          <p class="aide" style="margin-bottom:.8rem">Surface concernée (approximative)</p>
          <div class="choix deux">
{choix_surface}
          </div>
          <label for="est-detail" style="margin-top:1.2rem"><span data-detail-label>Précisions utiles</span> <span class="aide">(facultatif)</span>
            <textarea id="est-detail" name="precisions" rows="3" placeholder="Nombre de carottages, de logements, type de locaux…"></textarea></label>
        </fieldset>

        <fieldset class="etape">
          <legend>3. Où et quand&nbsp;?</legend>
          <div class="champs-2">
            <label for="est-cp">Code postal du chantier ou du site
              <input id="est-cp" name="code-postal" inputmode="numeric" autocomplete="postal-code" pattern="(7[5789]|9[1-5])[0-9]{{3}}" maxlength="5" required data-nom="code postal d’Île-de-France" placeholder="93370"></label>
            <label for="est-ville">Ville <span class="aide">(facultatif)</span>
              <input id="est-ville" name="ville" autocomplete="address-level2" placeholder="{VILLE}"></label>
          </div>
          <p class="aide" style="margin:1.1rem 0 .7rem">Délai souhaité</p>
          <div class="choix deux">
{choix_delai}
          </div>
        </fieldset>

        <fieldset class="etape">
          <legend>4. Vos coordonnées</legend>
          <div class="champs-2">
            <label for="est-nom">Nom et prénom<input id="est-nom" name="nom" autocomplete="name" required data-nom="nom"></label>
            <label for="est-societe">Société <span class="aide">(facultatif)</span><input id="est-societe" name="societe" autocomplete="organization"></label>
            <label for="est-tel">Téléphone<input id="est-tel" name="telephone" type="tel" autocomplete="tel" required data-nom="téléphone" pattern="[0-9 +.()-]{{10,}}"></label>
            <label for="est-email">E-mail<input id="est-email" name="email" type="email" autocomplete="email" required data-nom="e-mail"></label>
          </div>
          <label for="est-message" style="margin-top:1rem">Message <span class="aide">(facultatif)</span><textarea id="est-message" name="message" rows="3"></textarea></label>
          <p class="note" style="margin-top:.8rem">Vos données servent uniquement à répondre à votre demande. <a href="/mentions-legales/#confidentialite">En savoir plus</a>.</p>
        </fieldset>

        <p class="erreur" role="alert"></p>
        <div class="navigation-etapes">
          <button type="button" class="btn btn-contour btn-retour" data-precedent hidden>Précédent</button>
          <button type="button" class="btn btn-sombre" data-suivant style="margin-left:auto">Continuer</button>
          <button type="submit" class="btn btn-action" data-envoyer style="margin-left:auto">Recevoir mon devis gratuit</button>
        </div>
      </form>
    </div>
  </div>'''
    page("/estimation/", "Devis gratuit en 2 minutes – OF ENTRETIENS",
         "Estimez votre intervention en 2 minutes : carottage, corvoyage, nettoyage à Montfermeil et en Île-de-France. Devis gratuit et sans engagement.",
         "og-accueil.jpg", corps, (fil_ld,), scripts=("/assets/estimation.js",))

# ==========================================================================
# AUTRES PAGES
# ==========================================================================
def realisations():
    fil_html, fil_ld = fil_ariane([("Réalisations", "/realisations/")])
    photos = [
        ("corvoyage-logement", 1000, 750, "Préparation d’un logement neuf avant livraison", "Corvoyage : préparation d’un logement avant livraison", True),
        ("reserve-detail", 1000, 1333, "Réserve constatée au-dessus d’une menuiserie, en attente de reprise", "Réserves : constat, reprise, contrôle", False),
        ("reprise-allege", 1000, 1287, "Reprise d’allège et de plâtrerie autour d’une fenêtre", "Reprise d’allège et de plâtrerie", False),
        ("reprise-platrerie", 1000, 1333, "Reprise de plâtrerie autour de gaines techniques", "Reprise autour de gaines techniques", False),
        ("local-technique", 1000, 1333, "Gaines et réseaux dans un local technique", "Local technique", False),
        ("facade-nacelle", 1000, 1333, "Nettoyage de façade en nacelle sur un bâtiment d’activité", "Nettoyage de façade en nacelle", False),
        ("toiture-site-logistique", 1000, 562, "Toiture terrasse d’une plateforme logistique", "Toiture terrasse d’un site logistique", True),
        ("site-bardage", 1000, 1001, "Bardage encrassé d’un entrepôt, réparation repérée", "Bardage à remettre en propreté", False),
        ("site-cuve", 1000, 1001, "Dépôts et coulures sur une cuve métallique avant nettoyage", "Cuve avant nettoyage", False),
        ("programme-coursives", 1000, 853, "Coursives et jardins d’un programme immobilier en cours", "« Un Balcon en Forêt » — Bouygues Immobilier", False),
        ("programme-allee", 1000, 750, "Allée d’un programme immobilier neuf", "Abords d’un programme neuf", False),
        ("residence-exterieurs", 1000, 1333, "Espaces verts et terrasse d’une résidence livrée", "Extérieurs d’une résidence livrée", False),
    ]
    fig = "\n".join(f'''        <figure class="{"large " if large else ""}revele">{img(n, a + " — " + NOM, l, h, sizes="(max-width:599px) 100vw, 33vw")}<figcaption>{c}</figcaption></figure>''' for n, l, h, a, c, large in photos)
    corps = f'''  {fil_html}
  <section class="page-tete conteneur">
    <p class="surtitre">Sur le terrain</p>
    <h1>Nos réalisations à {VILLE} et en Île-de-France</h1>
    <p class="chapo">Des photos prises sur nos chantiers et nos sites d’intervention, sans mise en scène&nbsp;: corvoyage, reprises, façades, sites logistiques.</p>
  </section>
  <section class="conteneur" style="padding-bottom:2rem">
    <h2 style="margin-bottom:1.2rem">Avant / après</h2>
    <div class="galerie">
      <figure class="revele"><span class="etiquette">Avant</span>{img("avant-soubassement", "Soubassement d’une résidence protégé, avant reprise", 1000, 562)}<figcaption>Soubassement en attente de reprise</figcaption></figure>
      <figure class="revele"><span class="etiquette apres">Après</span>{img("apres-soubassement", "Même soubassement après reprise d’enduit", 1000, 750)}<figcaption>Enduit réalisé, finition propre</figcaption></figure>
    </div>
  </section>
  <section class="conteneur" style="padding-block:2rem clamp(48px,7vw,88px)">
    <h2 style="margin-bottom:1.2rem">Nos chantiers en images</h2>
    <div class="galerie">
{fig}
    </div>
  </section>
{cta_final("Un projet similaire&nbsp;?", "autre")}'''
    page("/realisations/", "Nos réalisations à Montfermeil – OF ENTRETIENS",
         "Corvoyage, reprises, façades, sites logistiques : nos réalisations à Montfermeil et en Île-de-France. Devis gratuit au 06 62 06 93 22.",
         "og-corvoyage.jpg", corps, (fil_ld,))

def qui_sommes_nous():
    fil_html, fil_ld = fil_ariane([("Qui sommes-nous", "/qui-sommes-nous/")])
    corps = f'''  {fil_html}
  <section class="page-tete conteneur">
    <p class="surtitre">Qui sommes-nous</p>
    <h1>Une entreprise à taille humaine, installée à {VILLE}</h1>
    <p class="chapo">Créée en 2024, {NOM} accompagne les promoteurs, les bailleurs, les entreprises et les sites logistiques d’Île-de-France, avec un interlocuteur direct du premier appel au suivi des travaux.</p>
  </section>
  <section class="conteneur qui" style="padding-bottom:clamp(48px,7vw,88px)">
    <figure>{img("logo", "Logo OF ENTRETIENS — corvoyage, levée de réserves, partenaire des promoteurs et des plateformes logistiques", 700, 522, sizes="(max-width:959px) 100vw, 560px")}</figure>
    <div class="texte-long">
      <h2>Comprendre d’abord, intervenir ensuite</h2>
      <p>{NOM} est une société par actions simplifiée dont le siège est à {VILLE}, en Seine-Saint-Denis. Nous intervenons dans toute l’Île-de-France, avec le directeur général comme interlocuteur direct&nbsp;: il connaît votre site, suit vos engagements et règle les ajustements sans intermédiaire.</p>
      <p>Du nettoyage de bureaux à la levée de réserves, en passant par les base-vie, les façades, le carottage en urgence et les entrepôts, la même exigence s’applique partout&nbsp;: un travail propre, annoncé clairement, et tenu.</p>
      <h3>Notre méthode</h3>
      <ol class="etapes">
        <li><strong>Nous visitons et nous écoutons.</strong> Le besoin réel se comprend sur place.</li>
        <li><strong>Nous définissons un périmètre clair.</strong> Inclus, exclu, fréquence, créneaux.</li>
        <li><strong>Nous intégrons vos règles.</strong> Sécurité, accès, co-activité.</li>
        <li><strong>Nous faisons le travail et nous le suivons.</strong> Avec des points réguliers.</li>
        <li><strong>Nous disons les imprévus.</strong> Tôt, et avec une solution.</li>
      </ol>
      <h3>Ils nous font confiance</h3>
      <p>Bouygues Immobilier — nous intervenons sur le programme «&nbsp;Un Balcon en Forêt&nbsp;» (SCCV), en Île-de-France.</p>
      <div class="groupe-btn" style="margin-top:1.4rem">
        <a class="btn btn-action" href="/estimation/">Devis gratuit</a>
        <a class="btn btn-contour btn-tel" href="{TEL_LIEN}">{TEL}</a>
      </div>
    </div>
  </section>'''
    page("/qui-sommes-nous/", "Qui sommes-nous – OF ENTRETIENS, Montfermeil",
         "OF ENTRETIENS, entreprise à taille humaine basée à Montfermeil : méthode, valeurs, références. Devis gratuit au 06 62 06 93 22.",
         "og-corvoyage.jpg", corps, (fil_ld,))

def contact():
    fil_html, fil_ld = fil_ariane([("Contact", "/contact/")])
    options = "".join(f"<option>{o}</option>" for o in ["Carottage en urgence", "Corvoyage et levée de réserves", "Nettoyage de bureaux, locaux ou base-vie", "Plateforme logistique", "Nettoyage de façade ou de bardage", "Autres travaux", "Autre demande"])
    corps = f'''  {fil_html}
  <section class="page-tete conteneur">
    <p class="surtitre">Contact</p>
    <h1>Contactez {NOM} à {VILLE}</h1>
    <p class="chapo">Le plus rapide&nbsp;: le téléphone. Sinon, écrivez-nous, nous vous rappelons pour parler concrètement de votre besoin.</p>
  </section>
  <div class="conteneur mise-en-page" style="padding-top:0">
    <div class="carte-blanche">
      <h2 style="font-size:1.6rem;margin-bottom:1rem">Écrivez-nous</h2>
      <form class="formulaire" name="contact" method="POST" action="/merci/" data-netlify="true" netlify-honeypot="site-web">
        <input type="hidden" name="form-name" value="contact">
        <p class="pot-de-miel"><label>Ne pas remplir<input name="site-web" tabindex="-1" autocomplete="off"></label></p>
        <div class="champs-2">
          <label for="c-nom">Nom et prénom<input id="c-nom" name="nom" autocomplete="name" required></label>
          <label for="c-societe">Société <span class="aide">(facultatif)</span><input id="c-societe" name="societe" autocomplete="organization"></label>
          <label for="c-tel">Téléphone<input id="c-tel" name="telephone" type="tel" autocomplete="tel" required></label>
          <label for="c-email">E-mail<input id="c-email" name="email" type="email" autocomplete="email" required></label>
        </div>
        <label for="c-objet">Objet<select id="c-objet" name="objet">{options}</select></label>
        <label for="c-message">Votre message<textarea id="c-message" name="message" rows="5" required></textarea></label>
        <p class="note">Vos données servent uniquement à répondre à votre demande. <a href="/mentions-legales/#confidentialite">En savoir plus</a>.</p>
        <button class="btn btn-action" type="submit">Envoyer ma demande</button>
      </form>
    </div>
    <aside class="aside-devis" aria-label="Coordonnées">
      <h2>Nos coordonnées</h2>
      <p><a class="btn btn-action btn-tel" href="{TEL_LIEN}">{TEL}</a></p>
      <ul>
        <li><a href="mailto:{EMAIL}" style="color:#fff">{EMAIL}</a></li>
        <li>{RUE}, {CP} {VILLE}</li>
        <li>Interventions dans toute l’Île-de-France</li>
      </ul>
      <a class="btn btn-clair" href="/estimation/">Estimation en 2 minutes</a>
    </aside>
  </div>'''
    contact_ld = {"@context": "https://schema.org", "@type": "ContactPage", "url": SITE + "/contact/", "about": FOURNISSEUR}
    page("/contact/", "Contact et devis à Montfermeil – OF ENTRETIENS",
         "Contactez OF ENTRETIENS à Montfermeil : 06 62 06 93 22 ou formulaire en ligne. Devis gratuit et sans engagement partout en Île-de-France.",
         "og-accueil.jpg", corps, (contact_ld, fil_ld))

def merci():
    corps = f'''  <section class="page-tete conteneur" style="padding-block:clamp(56px,9vw,120px);text-align:center">
    <p class="surtitre">Demande envoyée</p>
    <h1 style="margin-inline:auto">Merci, votre demande nous est bien parvenue</h1>
    <p class="chapo" style="margin-inline:auto">Nous revenons vers vous pour en parler concrètement et organiser une visite. Pour une urgence, appelez-nous directement.</p>
    <div class="groupe-btn" style="justify-content:center;margin-top:1.8rem">
      <a class="btn btn-action btn-tel" href="{TEL_LIEN}">{TEL}</a>
      <a class="btn btn-contour" href="/">Retour à l’accueil</a>
    </div>
  </section>'''
    page("/merci/", "Demande envoyée – OF ENTRETIENS",
         "Votre demande a bien été transmise à OF ENTRETIENS. Nous vous recontactons pour organiser une visite.",
         "og-accueil.jpg", corps, noindex=True)

def mentions():
    fil_html, fil_ld = fil_ariane([("Mentions légales", "/mentions-legales/")])
    corps = f'''  {fil_html}
  <section class="page-tete conteneur"><h1>Mentions légales et confidentialité</h1></section>
  <section class="conteneur texte-long" style="padding-bottom:clamp(48px,7vw,88px)">
    <h2>Éditeur du site</h2>
    <p><b>{NOM}</b> — société par actions simplifiée unipersonnelle (SASU) au capital de 500&nbsp;€<br>
    Siège social&nbsp;: {RUE}, {CP} {VILLE}, France<br>
    RCS Bobigny 927&nbsp;491&nbsp;357 · SIRET 927&nbsp;491&nbsp;357&nbsp;00012 · TVA intracommunautaire FR80927491357<br>
    Téléphone&nbsp;: <a href="{TEL_LIEN}">+33 6 62 06 93 22</a> · E-mail&nbsp;: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
    <h2>Directeur de la publication</h2>
    <p>Le directeur général d’{NOM}, joignable à l’adresse <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
    <h2>Hébergement</h2>
    <p>Netlify, Inc. — 101 2nd Street, Suite 575, San Francisco, CA 94105, États-Unis — <a href="https://www.netlify.com" rel="noopener">www.netlify.com</a></p>
    <h2>Propriété intellectuelle</h2>
    <p>Les textes, les photographies de chantier et le logo d’{NOM} sont sa propriété. Toute reproduction sans autorisation écrite est interdite. Certaines illustrations proviennent de la banque d’images Unsplash et sont utilisées selon sa licence. Le logo Bouygues Immobilier reste la propriété de son titulaire&nbsp;; il est reproduit au titre de référence client.</p>
    <h2 id="confidentialite">Confidentialité et données personnelles</h2>
    <p><b>Responsable du traitement&nbsp;:</b> {NOM}, {RUE}, {CP} {VILLE}.</p>
    <p><b>Données collectées&nbsp;:</b> uniquement celles que vous saisissez dans les formulaires (estimation et contact)&nbsp;: nom, société, téléphone, e-mail, code postal, ville, nature et description de votre besoin.</p>
    <p><b>Finalité et base légale&nbsp;:</b> répondre à votre demande et établir un devis. Ce traitement repose sur les mesures précontractuelles prises à votre demande (article 6.1.b du RGPD).</p>
    <p><b>Destinataires&nbsp;:</b> {NOM} uniquement. Les formulaires sont reçus par notre hébergeur Netlify&nbsp;; ce transfert hors de l’Union européenne est encadré par les garanties prévues par le RGPD. Vos données ne sont ni vendues ni cédées.</p>
    <p><b>Durée de conservation&nbsp;:</b> trois ans à compter de notre dernier échange, sauf relation contractuelle, auquel cas les durées légales s’appliquent.</p>
    <p><b>Vos droits&nbsp;:</b> accès, rectification, effacement, limitation, opposition et portabilité, en écrivant à <a href="mailto:{EMAIL}">{EMAIL}</a>. Vous pouvez aussi saisir la CNIL (<a href="https://www.cnil.fr" rel="noopener">www.cnil.fr</a>).</p>
    <h2 id="politique-cookies">Cookies</h2>
    <p>Ce site ne dépose aucun cookie publicitaire ni de mesure d’audience. Seul votre choix en matière de cookies est mémorisé dans votre navigateur. Les polices de caractères sont hébergées sur le site lui-même. Vous pouvez revoir votre choix à tout moment&nbsp;: <button type="button" class="btn btn-contour" data-gerer-cookies style="min-height:44px;padding:.4rem 1rem">Gérer les cookies</button></p>
  </section>'''
    page("/mentions-legales/", "Mentions légales – OF ENTRETIENS",
         "Mentions légales, hébergeur, confidentialité et cookies du site OF ENTRETIENS, entreprise basée à Montfermeil.",
         "og-accueil.jpg", corps, (fil_ld,))

def erreur404():
    corps = f'''  <section class="page-tete conteneur" style="padding-block:clamp(56px,9vw,120px);text-align:center">
    <p class="surtitre">Erreur 404</p>
    <h1 style="margin-inline:auto">Cette page n’existe pas ou a été déplacée</h1>
    <p class="chapo" style="margin-inline:auto">Retrouvez nos services depuis l’accueil, ou appelez-nous directement.</p>
    <div class="groupe-btn" style="justify-content:center;margin-top:1.8rem">
      <a class="btn btn-contour" href="/">Retour à l’accueil</a>
      <a class="btn btn-action btn-tel" href="{TEL_LIEN}">{TEL}</a>
    </div>
  </section>'''
    page("/404.html", "Page introuvable – OF ENTRETIENS", "Cette page est introuvable sur le site OF ENTRETIENS.",
         "og-accueil.jpg", corps, noindex=True, actif="-")

# ==========================================================================
# FICHIERS TECHNIQUES
# ==========================================================================
def fichiers_techniques():
    urls = "\n".join(f"  <url><loc>{SITE}{p}</loc><lastmod>{AUJOURDHUI}</lastmod></url>" for p in PAGES)
    with open(os.path.join(SORTIE, "sitemap.xml"), "w", encoding="utf8") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')
    with open(os.path.join(SORTIE, "robots.txt"), "w", encoding="utf8") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    with open(os.path.join(SORTIE, "_redirects"), "w", encoding="utf8") as f:
        f.write("""# Anciennes adresses -> nouvelles (redirections permanentes, conservent le référencement)
/corvoyage.html               /corvoyage-montfermeil/             301
/promoteurs.html              /corvoyage-montfermeil/             301
/plateformes-logistiques.html /plateformes-logistiques/           301
/carottage-urgence.html       /carottage-urgence-montfermeil/     301
/mentions-legales.html        /mentions-legales/                  301
/merci.html                   /merci/                             301
/index.html                   /                                   301
""")
    with open(os.path.join(SORTIE, "_headers"), "w", encoding="utf8") as f:
        f.write("""/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: SAMEORIGIN
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()

/assets/fonts/*
  Cache-Control: public, max-age=31536000, immutable

/assets/img/*
  Cache-Control: public, max-age=2592000

/assets/*.css
  Cache-Control: public, max-age=604800

/assets/*.js
  Cache-Control: public, max-age=604800
""")
    with open(os.path.join(SORTIE, "netlify.toml"), "w", encoding="utf8") as f:
        f.write('# Site statique : aucun build, le dossier est publié tel quel.\n[build]\n  publish = "."\n')

if __name__ == "__main__":
    print("Génération du site dans", SORTIE)
    accueil()
    service_carottage(); service_corvoyage(); service_nettoyage(); service_logistique()
    estimation(); realisations(); qui_sommes_nous(); contact(); merci(); mentions(); erreur404()
    fichiers_techniques()
    print("Pages indexables :", len(PAGES))
