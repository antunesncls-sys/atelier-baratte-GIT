"""Génère la signature e-mail Construisez.

Usage : python3 -I signature-mail/build.py   (depuis la racine du dépôt)
Écrit :
  signature-mail/signature-construisez.html  la signature seule (version complète et version courte),
                                             à ouvrir dans un navigateur, sélectionner, copier, coller
  signature-mail/page.html                   la page publiée en artefact (aperçu, boutons Copier, marche à suivre)
Le logo est chargé depuis construisez.fr, pour qu'il s'affiche chez tous les destinataires.
"""
import base64
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO_URL = 'https://www.construisez.fr/assets/brand/logo-mark.png'
SITE = 'https://www.construisez.fr/?utm_source=email&utm_medium=signature&utm_campaign=signature'
NOM = 'Nicolas Antunes'
TITRE = 'Fondateur de Construisez · Ingénieur bâtiment'
TEL, TEL_LIEN = '07 61 70 53 59', 'tel:+33761705359'
MAIL = 'construisez@outlook.fr'
RESEAUX = [('Instagram', 'https://www.instagram.com/permis_de_construire_idf/'),
           ('TikTok', 'https://www.tiktok.com/@permisdeconstruire'),
           ('Facebook', 'https://www.facebook.com/Construisez.idf/')]

F = "font-family:Arial,Helvetica,sans-serif;"
DARK, GREY, ACC, LEAF = '#1c1d21', '#5f6470', '#3e6b5c', '#6db33f'
A = f"color:{DARK};text-decoration:none;"


def complete(logo):
    reseaux = ' &nbsp;·&nbsp; '.join(f'<a href="{u}" style="color:{ACC};text-decoration:none;">{n}</a>' for n, u in RESEAUX)
    return f'''<table cellpadding="0" cellspacing="0" border="0" role="presentation" style="border-collapse:collapse;{F}">
  <tr>
    <td valign="top" style="padding:2px 16px 0 0;">
      <a href="{SITE}" style="text-decoration:none;"><img src="{logo}" width="58" height="59" alt="Construisez" style="display:block;border:0;width:58px;height:59px;"></a>
    </td>
    <td valign="top" style="border-left:2px solid {LEAF};padding:0 0 0 16px;">
      <div style="{F}font-size:16px;line-height:20px;font-weight:bold;color:{DARK};">{NOM}</div>
      <div style="{F}font-size:13px;line-height:18px;color:{GREY};">{html.escape(TITRE)}</div>
      <div style="{F}font-size:13px;line-height:18px;font-weight:bold;color:{ACC};padding-top:8px;">Permis de construire &amp; déclarations préalables en Île-de-France</div>
      <div style="{F}font-size:13px;line-height:19px;color:{DARK};padding-top:6px;">
        <a href="{TEL_LIEN}" style="{A}">{TEL}</a> &nbsp;·&nbsp; <a href="mailto:{MAIL}" style="{A}">{MAIL}</a><br>
        <a href="{SITE}" style="{A}font-weight:bold;">construisez.fr</a> &nbsp;·&nbsp; Saint-Maur-des-Fossés (94)
      </div>
      <div style="{F}font-size:12px;line-height:18px;color:{GREY};padding-top:6px;">★ 5/5 sur Google &nbsp;·&nbsp; plus de 300 projets depuis 2018</div>
      <table cellpadding="0" cellspacing="0" border="0" role="presentation" style="border-collapse:collapse;margin-top:10px;">
        <tr><td style="background:{ACC};border-radius:4px;padding:7px 14px;">
          <a href="{SITE}" style="{F}font-size:13px;line-height:16px;font-weight:bold;color:#ffffff;text-decoration:none;">Étudier mon projet · devis sous 24 h →</a>
        </td></tr>
      </table>
      <div style="{F}font-size:12px;line-height:18px;padding-top:8px;">{reseaux}</div>
    </td>
  </tr>
</table>'''


def courte(logo):
    return f'''<table cellpadding="0" cellspacing="0" border="0" role="presentation" style="border-collapse:collapse;{F}">
  <tr>
    <td valign="middle" style="padding:0 12px 0 0;"><img src="{logo}" width="34" height="35" alt="Construisez" style="display:block;border:0;width:34px;height:35px;"></td>
    <td valign="middle" style="border-left:2px solid {LEAF};padding:0 0 0 12px;">
      <div style="{F}font-size:14px;line-height:18px;color:{DARK};"><b>{NOM}</b> &nbsp;·&nbsp; Construisez</div>
      <div style="{F}font-size:12px;line-height:18px;color:{GREY};"><a href="{TEL_LIEN}" style="color:{GREY};text-decoration:none;">{TEL}</a> &nbsp;·&nbsp; <a href="{SITE}" style="color:{ACC};text-decoration:none;font-weight:bold;">construisez.fr</a></div>
    </td>
  </tr>
</table>'''


def perso():
    # Adresse personnelle : pas de logo ni de bouton, juste le nom, le numéro et une ligne discrète vers Construisez.
    # L'adresse e-mail n'y figure pas : le destinataire la voit déjà comme expéditeur.
    return f'''<table cellpadding="0" cellspacing="0" border="0" role="presentation" style="border-collapse:collapse;{F}">
  <tr>
    <td valign="top" style="border-left:2px solid {LEAF};padding:0 0 0 12px;">
      <div style="{F}font-size:14px;line-height:19px;font-weight:bold;color:{DARK};">{NOM}</div>
      <div style="{F}font-size:13px;line-height:19px;color:{DARK};"><a href="{TEL_LIEN}" style="{A}">{TEL}</a></div>
      <div style="{F}font-size:12px;line-height:18px;color:{GREY};padding-top:2px;">Fondateur de <a href="{SITE.replace('campaign=signature', 'campaign=signature-perso')}" style="color:{ACC};text-decoration:none;font-weight:bold;">Construisez</a></div>
    </td>
  </tr>
</table>'''


def texte(full):
    if full == 'perso':
        return f'{NOM}\n{TEL}\nFondateur de Construisez'
    if not full:
        return f'{NOM} · Construisez\n{TEL} · construisez.fr'
    return '\n'.join([NOM, TITRE, 'Permis de construire & déclarations préalables en Île-de-France',
                      f'{TEL} · {MAIL}', 'construisez.fr · Saint-Maur-des-Fossés (94)'])


# 1. Signature seule, logo en ligne
open(os.path.join(HERE, 'signature-construisez.html'), 'w', encoding='utf-8').write(f'''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><title>Signature Construisez</title></head>
<body style="margin:24px;background:#ffffff;">
<p style="{F}font-size:13px;color:{GREY};">Version complète (nouveaux messages) : sélectionnez-la, copiez, puis collez dans les réglages de signature de votre messagerie.</p>
<br>
{complete(LOGO_URL)}
<br><br><br>
<p style="{F}font-size:13px;color:{GREY};">Version courte (réponses et transferts) :</p>
<br>
{courte(LOGO_URL)}
<br><br><br>
<p style="{F}font-size:13px;color:{GREY};">Adresse personnelle :</p>
<br>
{perso()}
</body></html>
''')

# 2. Page de l'artefact : l'aperçu montre le logo intégré (seul construisez.fr est bloqué dans le cadre de la page),
#    le bouton Copier copie la version qui charge le logo depuis construisez.fr.
logo_data = 'data:image/png;base64,' + base64.b64encode(open(os.path.join(HERE, 'logo-mark.png'), 'rb').read()).decode()
sigs = {'complete': {'html': complete(LOGO_URL), 'text': texte(True)}, 'courte': {'html': courte(LOGO_URL), 'text': texte(False)}, 'perso': {'html': perso(), 'text': texte('perso')}}
page = open(os.path.join(HERE, 'page.template.html'), encoding='utf-8').read()
page = (page.replace('{{PREVIEW_COMPLETE}}', complete(logo_data))
            .replace('{{PREVIEW_COURTE}}', courte(logo_data))
            .replace('{{PREVIEW_PERSO}}', perso())
            .replace('{{SIGS_JSON}}', json.dumps(sigs, ensure_ascii=False).replace('</', '<\\/')))
open(os.path.join(HERE, 'page.html'), 'w', encoding='utf-8').write(page)
print('signature-construisez.html et page.html écrits')
