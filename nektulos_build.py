"""
nektulos_build.py -- builds nektulos_2.txt from the reusable eqmap_toolkit.
Demonstrates the spreadsheet/cell layout:
  * Title  -> top heading row (full width)
  * Compass-> 2nd row, right margin column (best-fit side)
  * Gateway-> right margin cell aligned to its landmark's row (pseudo-3D, enlarged)
  * Volcanoes -> northern content edge ; Trees -> content ; Grid -> content
"""
import numpy as np, random, math
import eqmap_toolkit as T

random.seed(6)
BASE = "/mnt/user-data/uploads/nektulos.txt"
POI  = "/mnt/user-data/outputs/nektulos_1.txt"
OUT  = "/mnt/user-data/outputs/nektulos_2.txt"

# palette
DK=(45,38,55); PUR=(90,70,110); GREY=(95,90,100); DEAD=(70,60,55)
WEB=(120,115,125); TITLE=(120,105,135); TSH=(50,42,62); GRID=(80,75,92)

# ---- content bbox from geometry ----
A = np.array([[float(x) for x in l[2:].split(',')[:6]]
              for l in open(BASE).read().replace('\r\n','\n').split('\n') if l.strip().startswith('L')])
pts = np.vstack([A[:,0:2], A[:,3:5]])
bbox = (pts[:,0].min(), pts[:,0].max(), pts[:,1].min(), pts[:,1].max())
cv = T.Canvas(bbox, pad=700, gstep=750)
minx,maxx,miny,maxy = bbox

# landmark row for the gateway (align beside the Knowledge Portal)
portal_y = miny + (maxy-miny)*0.5
for l in open(POI).read().replace('\r\n','\n').split('\n'):
    if l.startswith('P') and 'Knowledge_Portal' in l:
        portal_y = float(l[2:].split(',')[1])

# ---- 1. grid (under everything, clipped to content) ----
T.grid(cv, GRID)

# ---- 2. frame with spider-web corners ----
T.frame(cv, DK, PUR, step=110, depth=80, inset=45,
        corner=lambda c,x,y,sx,sy: T.web_corner(c, x, y, sx, sy, WEB))

# ---- 3. trees across the content (+ bottom-left fill) ----
tb = cv.by0 + 560
for gx in np.arange(minx+140, maxx-80, 365):
    for gy in np.arange(miny+140, maxy-80, 365):
        if random.random() < 0.40: continue
        cx = gx+random.uniform(-150,150); cy = gy+random.uniform(-150,150)
        if cy < tb: continue
        T.dead_tree(cv, cx, cy, random.uniform(130,240), DEAD)
for gx in np.arange(minx+120, minx+(maxx-minx)*0.42, 300):
    for gy in np.arange(miny+(maxy-miny)*0.55, maxy-120, 300):
        if random.random() < 0.45: continue
        T.dead_tree(cv, gx+random.uniform(-120,120), gy+random.uniform(-120,120), random.uniform(130,230), DEAD)

# ---- 4. volcanoes along the northern content edge (Lavastorm border) ----
for bx in np.linspace(minx+260, maxx-260, 6):
    T.volcano(cv, bx+random.uniform(-100,100), random.uniform(miny-120, miny+80),
              random.uniform(150,240), random.uniform(200,300))

# ---- 5. wizard-gateway doodle: right margin cell beside its landmark (bigger, pseudo-3D) ----
T.wizard_gate(cv, cv.margin_x('right'), cv.snap_row(portal_y), 175, 300)

# ---- 6. title: full-width heading (row 0) ----
T.title(cv, "NEKTULOS FOREST", TITLE, shadow=TSH, height=270)

# ---- 7. compass: 2nd row, right margin column, drawn LAST (on top) ----
T.compass(cv, cv.margin_x('right'), cv.row_y(0), 155,
          ring=(GREY,PUR), rose=(GREY,PUR),
          center=T.spider_motif, center_colors=(DK,PUR),
          label=PUR, n_label=GREY, arrow=GREY)

cv.write(OUT)
print(f"{OUT}: {len(cv.L)} L + {len(cv.P)} P")
print(f"  gateway row y={cv.snap_row(portal_y):.0f} (beside Knowledge Portal), compass row y={cv.row_y(0):.0f}")
