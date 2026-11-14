# Retouche d'un photomontage d'insertion (maison SketchUp collée dans une photo de rue) pour le rendre moins « maquette » :
# traits noirs fondus dans l'enduit, lumière chaude du soleil, ombres sous les débords de toit, reflets du ciel dans les vitres,
# rive de toit en tuiles, grain commun à la photo et à la maison. Les volumes et les ouvertures ne bougent pas.
#
# Usage : python3 visuels/retouche-insertion.py <après.webp> <avant.webp> <sortie.webp> x0,y0,x1,y1 [yline] [yglass]
#   x0,y0,x1,y1 : rectangle qui contient la maison projetée
#   yline  : plus bas, on ne touche plus aux traits (haut de la clôture, pour ne pas abîmer le portail)
#   yglass : plus haut, aucune vitre (toiture)
# Exemple (Sannois) :
#   python3 visuels/retouche-insertion.py visuels/brand/photos/projets/sannois-rue-apres.webp \
#     visuels/brand/photos/projets/sannois-rue-avant.webp visuels/brand/photos/projets/sannois-rue-apres-retouche.webp \
#     560,380,1270,1100 912 595
# Écrit aussi <sortie>-mask.png (contrôle : gris = enduit, rouge = traits, bleu = fenêtres, jaune = rive).
import sys
import numpy as np
from PIL import Image, ImageFilter, ImageDraw

src, ref, out = sys.argv[1], sys.argv[2], sys.argv[3]
x0, y0, x1, y1 = [int(v) for v in sys.argv[4].split(',')]          # zone de la maison projetée
yline = int(sys.argv[5]) if len(sys.argv) > 5 else y1              # limite basse du traitement des traits (haut de la clôture)
yglass = int(sys.argv[6]) if len(sys.argv) > 6 else y0             # aucune vitre au-dessus de cette ligne (toiture)
img = Image.open(src).convert('RGB')
A = np.asarray(img).astype(np.float32)
R = np.asarray(Image.open(ref).convert('RGB').resize(img.size)).astype(np.float32)
Hh, Ww = A.shape[:2]
rng = np.random.default_rng(7)

def blur(arr, r):
    return np.asarray(Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r))).astype(np.float32)
def blur1(m, r):  # masque 0..1
    return blur(m * 255, r) / 255
def grow(m, k):
    return np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(k))) > 127
def shrink(m, k):
    return np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(k))) > 127

# 1. Masques
zone = np.zeros((Hh, Ww), bool); zone[y0:y1, x0:x1] = True
rows = np.arange(Hh)[:, None]
mx, mn = A.max(2), A.min(2)
flat = (mx - mn) < 34
bright = zone & flat & (mx > 95)
diff = np.abs(A - R).sum(2) > 45
core = grow(shrink(bright & diff, 5), 5) & bright
core = shrink(grow(core, 17), 17) & bright                # enduit, bandeaux, vitres du modèle 3D
dark = zone & flat & (mx <= 95)
thin = dark & ~grow(shrink(dark, 15), 19) & (rows < yline)   # traits et cadres : sombres mais fins (ni haie ni ombre)
thin &= grow(core, 15)
# zones fermées par des traits (vitres posées sur une ancienne fenêtre de la photo, par exemple) : elles font partie du modèle
def holes_of(mask):
    im = Image.new('L', (Ww, Hh), 0); im.paste(Image.fromarray(((mask & zone) * 255).astype(np.uint8)))
    ImageDraw.floodfill(im, (0, 0), 128)
    return (np.asarray(im) == 0) & zone
core |= holes_of(core | thin) & (mx > 95)
# fenêtres : là où traits sombres et vitres grises forment un bloc d'au moins 30 px
neutral = core & ((mx - mn) < 10) & ((mx < 212) | (mx >= 246)) & (rows > yglass)   # vitres grises, panneaux blancs
neutral = grow(shrink(neutral, 7), 7) & neutral
blocks = shrink(grow(thin | neutral, 13), 13)
blocks |= holes_of(blocks) & (mx < 215)             # vitre teintée entourée de son cadre (jamais l'enduit, plus clair)
win = grow(shrink(blocks, 31), 35) & blocks & (rows > yglass)
near_win = win.copy()                                    # cadres qui dépassent du bloc : 12 px sur les côtés, 4 px en hauteur
for d in range(1, 13):
    near_win[:, d:] |= win[:, :-d]; near_win[:, :-d] |= win[:, d:]
nw = near_win.copy()
for d in range(1, 5):
    near_win[d:] |= nw[:-d]; near_win[:-d] |= nw[d:]
near_win &= ~win
line = grow(thin, 3) & ~win & ~near_win
house = core | line | win
hm = blur1(house.astype(np.float32), 1.2)[..., None]
wall = house & ~win

# 2. Traits noirs hors fenêtres : remplacés par l'enduit voisin
keep = core & ~grow(thin, 7) & ~win
num = blur(A * keep[..., None], 6); den = blur1(keep.astype(np.float32), 6)[..., None]
B = A.copy()
B[line] = (num / np.maximum(den, 1e-3))[line]
far = line & (den[..., 0] < 0.04)                        # trait isolé sans enduit autour : on garde la photo d'origine
B[far] = R[far]
# rive de toit : le trait qui touche le ciel devient une rive de tuiles brunes
sky = (A[..., 2] > A[..., 0] + 35) & ~house
sky_above = np.zeros_like(sky); sky_above[5:] = sky[:-5]
rive = line & grow(sky_above, 3)

# traits restés autour de la maison (retours de toiture, bas de porte) : on reprend la photo d'origine
left = dark & ~grow(shrink(dark, 15), 19) & (rows < yline) & grow(house, 11) & ~house & (R.max(2) > 95)
B[left] = R[left]
house_all = house | left
hm = blur1(house_all.astype(np.float32), 1.2)[..., None]

# 3. Lumière : soleil bas et chaud venant de la gauche, ombre portée sous les débords de toit et les appuis
warm = np.array([1.04, 0.985, 0.885], np.float32)
yy, xx = np.mgrid[0:Hh, 0:Ww].astype(np.float32)
ty = np.clip((yy - y0) / (y1 - y0), 0, 1); tx = np.clip((xx - x0) / (x1 - x0), 0, 1)
shade = 1.05 - 0.13 * ty - 0.05 * tx
occl = blur1(line.astype(np.float32), 6)
sh = np.zeros_like(occl); sh[11:, 7:] = occl[:-11, :-7]
light = shade * (1 - 0.38 * np.clip(sh * 2.2, 0, 1))
stucco = blur(rng.normal(128, 26, (Hh, Ww, 1)).repeat(3, 2), 0.8)[..., :1] / 128
B = np.where(wall[..., None], B * warm * light[..., None] * (0.985 + 0.015 * stucco), B)
B[rive] = np.array([104, 72, 56], np.float32)

# 4. Fenêtres : on garde le dessin d'origine ; noir adouci en anthracite, vitres en reflet du ciel
skyc = R[sky].mean(0) if sky.any() else np.array([120, 160, 215], np.float32)
wdark = (win | (near_win & thin)) & (mx <= 95)
B[wdark] = A[wdark] * 0.72 + np.array([22, 24, 26], np.float32)
edge = near_win & thin & (mx <= 95)
B[edge] = A[edge] * 0.5 + np.array([66, 62, 58], np.float32)
wgrey = win & (mx > 95) & (mx < 215) & ((mx - mn) < 10)
other = win & (mx > 95) & (mx < 246) & ~wgrey             # vitre teintée ou interstice entre deux traits du cadre
pane = grow(shrink(other, 9), 9) & other
B[other & ~pane] = np.array([58, 62, 66], np.float32)
wglass = wgrey | pane
g = (0.80 - 0.28 * ty)[..., None]
streak = blur1((np.sin((xx + yy * 0.9) / 60.0) > 0.8).astype(np.float32), 6)[..., None] * 0.12
lum = np.clip(A.mean(2, keepdims=True) / 183, 0.55, 1.1)
glass_rgb = (0.58 * skyc * (g + streak) + 0.42 * np.array([34, 38, 44], np.float32)) * (0.55 + 0.45 * lum)
B = np.where(wglass[..., None], glass_rgb, B)
wwhite = win & (mx >= 246)
B[wwhite] = A[wwhite] * warm * 0.97

# 6. Fond dans la photo : flou léger de la maison, fusion par le masque adouci
soft = blur(B, 0.7)
C = A * (1 - hm) + soft * hm

# 7. Étalonnage commun et grain : même traitement pour la photo et la maison
C = (C - 128) * 1.06 + 128
C[..., 0] *= 1.012; C[..., 2] *= 1.035                 # ciel un peu plus franc, comme la photo d'origine
C += rng.normal(0, 2.2, (Hh, Ww, 1))
Image.fromarray(np.clip(C, 0, 255).astype(np.uint8)).save(out, quality=93)
dbg = np.zeros((Hh, Ww, 3), np.uint8); dbg[core] = (90, 90, 90); dbg[line] = (255, 60, 60); dbg[win] = (60, 120, 255); dbg[rive] = (255, 220, 0)
Image.fromarray(dbg).save(out.rsplit('.', 1)[0] + '-mask.png')
