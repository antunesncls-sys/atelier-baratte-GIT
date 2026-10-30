#!/usr/bin/env python3
"""Signale toutes les pages du site à Bing (et aux moteurs IndexNow) après une mise en ligne.

Usage, une fois le nouveau ZIP déposé sur Netlify et le domaine jmccouverture.com actif :
    python3 _build/indexnow.py
Bing alimente la recherche de ChatGPT et de Copilot : vos nouvelles pages y sont prises en compte plus vite.
"""
import json, re, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "_build"))
key = re.search(r'INDEXNOW_KEY = "([0-9a-f]+)"', (ROOT / "_build" / "build.py").read_text()).group(1)
urls = re.findall(r"<loc>(.*?)</loc>", (ROOT / "sitemap.xml").read_text())
body = json.dumps({"host": "jmccouverture.com", "key": key,
                   "keyLocation": f"https://jmccouverture.com/{key}.txt", "urlList": urls}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                             headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req, timeout=30) as r:
    print(f"IndexNow : {len(urls)} pages envoyées, réponse HTTP {r.status} (200 ou 202 = OK)")
