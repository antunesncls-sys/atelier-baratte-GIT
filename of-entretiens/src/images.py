"""Prépare toutes les images du site (WebP sans métadonnées + images de partage JPEG).
Usage : python3 -I src/images.py <dossier des JPEG d'origine> <dossier de sortie>"""
import sys, os
from PIL import Image, ImageOps
SRC, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
def ouvrir(n): return ImageOps.exif_transpose(Image.open(os.path.join(SRC, n))).convert("RGB")
def recadrer(im, rw, rh, cx=.5, cy=.5):
    w, h = im.size; tw = min(w, h * rw / rh); th = tw * rh / rw
    x = max(0, min(w - tw, cx * w - tw / 2)); y = max(0, min(h - th, cy * h - th / 2))
    return im.crop((int(x), int(y), int(x + tw), int(y + th)))
def webp(im, nom, largeur, q=70):
    im = im.copy()
    if im.width > largeur: im = im.resize((largeur, round(im.height * largeur / im.width)), Image.LANCZOS)
    im.save(os.path.join(OUT, nom + ".webp"), "WEBP", quality=q, method=6)
    return f"{nom}.webp {im.width}x{im.height}"
def og(im, nom, cx=.5, cy=.5):
    recadrer(im, 1200, 630, cx, cy).resize((1200, 630), Image.LANCZOS).save(os.path.join(OUT, nom + ".jpg"), "JPEG", quality=80, optimize=True, progressive=True)

facade, toiture = ouvrir("facade-nacelle.jpg"), ouvrir("toiture-site-logistique.jpg")
print(webp(recadrer(facade, 16, 10, .5, .33), "hero-1600", 1600, 62))
print(webp(recadrer(facade, 16, 10, .5, .33), "hero-800", 800, 62))
print(webp(recadrer(facade, 4, 5, .5, .4), "hero-mobile", 640, 62))
# cartes de services (3:2)
cartes = {"carte-carottage": ("reprise-platrerie.jpg", .5, .45), "carte-corvoyage": ("corvoyage-logement.jpg", .5, .5),
          "carte-nettoyage": ("tuile-nettoyage.jpg", .5, .4), "carte-logistique": ("toiture-site-logistique.jpg", .45, .6),
          "carte-facade": ("facade-nacelle.jpg", .5, .33), "carte-tce": ("reprise-allege.jpg", .5, .45)}
for nom, (f, cx, cy) in cartes.items(): print(webp(recadrer(ouvrir(f), 3, 2, cx, cy), nom, 640))
# photos de galerie / pages (proportions d'origine)
for f in ["corvoyage-logement", "reprise-platrerie", "reserve-detail", "reprise-allege", "local-technique", "residence-exterieurs",
          "programme-allee", "programme-coursives", "site-bardage", "site-cuve", "avant-soubassement",
          "apres-soubassement", "toiture-site-logistique", "facade-nacelle"]:
    print(webp(ouvrir(f + ".jpg"), f, 1000))
# bandeaux larges des pages de service (2:1)
for nom, (f, cx, cy) in {"bandeau-carottage": ("reprise-platrerie.jpg", .5, .45), "bandeau-corvoyage": ("programme-coursives.jpg", .5, .5),
                         "bandeau-nettoyage": ("tuile-nettoyage.jpg", .5, .4), "bandeau-logistique": ("toiture-site-logistique.jpg", .5, .55)}.items():
    print(webp(recadrer(ouvrir(f), 2, 1, cx, cy), nom, 1200))
# images de partage (vraies photos)
og(facade, "og-accueil", .5, .33); og(ouvrir("reprise-platrerie.jpg"), "og-carottage", .5, .42)
og(ouvrir("programme-coursives.jpg"), "og-corvoyage"); og(facade, "og-nettoyage", .5, .5); og(toiture, "og-logistique", .5, .55)
print("og OK")
