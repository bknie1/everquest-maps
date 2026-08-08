"""Assemble newsebexp_2.txt -- the decoration layer for New Sebilis Expedition."""
import random, math
from eqmap_toolkit import Canvas, frame, grid, compass, LETTERS
import nse_decor as N

random.seed(1993)

# ---- content bbox from base geometry ----
MINX,MAXX,MINY,MAXY = -566.63, 323.92, -651.00, 900.17
PAD = 230
INSET = 46
cv = Canvas((MINX,MAXX,MINY,MAXY), PAD)     # gstep auto -> 200

IRON,IRON_L,ROOT,ROOT_D = N.IRON,N.IRON_L,N.ROOT,N.ROOT_D
GRIDC = (176,166,146)
Z=0.0

# ---------- helper: centered flipped stick word ----------
def word(text, cx, oy, height, color, gap_frac=0.34, shadow=None, z=Z):
    cw=height*0.66; gap=cw*gap_frac
    w=len(text)*cw+(len(text)-1)*gap
    ox=cx-w/2
    fy=lambda y: 2*oy+height - y
    x=ox
    for ch in text:
        for poly in LETTERS.get(ch,[]):
            for i in range(len(poly)-1):
                ax,ay=poly[i]; bx,by=poly[i+1]
                if shadow:
                    cv.add(x+ax*cw+6, fy(oy+ay*height)+7, x+bx*cw+6, fy(oy+by*height)+7, shadow, z)
                cv.add(x+ax*cw, fy(oy+ay*height), x+bx*cw, fy(oy+by*height), color, z)
        x+=cw+gap
    return w

# =========================================================== 1. GRID (under all)
grid(cv, GRIDC, step=200)

# =========================================================== 2. FRAME + root corners
frame(cv, outer=IRON, inner=ROOT, step=95, depth=42, inset=INSET,
      corner=lambda c,x,y,sx,sy: N.root_burst(c,x,y,sx,sy,reach=250))

# second, thin gold accent line just inside the inner frame (temple trim)
gx0,gy0,gx1,gy1 = cv.bx0+70, cv.by0+70, cv.bx1-70, cv.by1-70
for a,b in [((gx0,gy0),(gx1,gy0)),((gx1,gy0),(gx1,gy1)),((gx1,gy1),(gx0,gy1)),((gx0,gy1),(gx0,gy0))]:
    cv.add(*a,*b,N.GOLD,Z)

# =========================================================== 3. BROKEN CHAINS on border
# top & bottom inner edges: intermittent broken chain runs
iy_t, iy_b = cv.by0+46, cv.by1-46
for x0 in range(-500, 400, 300):
    N.broken_chain(cv, x0, iy_t, x0+230, iy_t, r=11)
    N.broken_chain(cv, x0, iy_b, x0+230, iy_b, r=11)
ix_l, ix_r = cv.bx0+46, cv.bx1-46
for y0 in range(-620, 1000, 360):
    N.broken_chain(cv, ix_l, y0, ix_l, y0+250, r=11)
    N.broken_chain(cv, ix_r, y0, ix_r, y0+250, r=11)
# (top-hanging manacles removed -- they sat under the title band; manacles now
#  live in the side/bottom margins where there's clear room)

# =========================================================== 4. TITLE (top margin)
tcx = (MINX+MAXX)/2
word("NEW SEBILIS", tcx, cv.by0+18, 96, IRON, shadow=ROOT_D)
word("EXPEDITION",  tcx, cv.by0+120, 46, ROOT_D)
# framing bars + flanking emblems
bar_w = 470
cv.add(tcx-bar_w, cv.by0+8, tcx+bar_w, cv.by0+8, IRON, Z)
cv.add(tcx-bar_w, cv.by0+176, tcx+bar_w, cv.by0+176, IRON, Z)
N.nse_emblem(cv, tcx-bar_w-46, cv.by0+92, 42)
N.nse_emblem(cv, tcx+bar_w+46, cv.by0+92, 42)

# =========================================================== 5. INTERIOR ROOTS (through ceiling)
random.seed(7)
for rx in (-470,-330,-190,-40,300):
    N.root_drip(cv, rx, MINY+4, random.uniform(120,190))
# a few short roots creeping down from the bottom cave ceilings
for rx in (-430,-250):
    N.root_drip(cv, rx, 610, 120)

# =========================================================== 6. LEFT MARGIN doodles
# lane centered between the inner frame line and the content edge -> clear of both
lx = (cv.bx0 + INSET + cv.minx)/2      # ~ minx-92
N.root_drip(cv, lx, cv.by0+150, 150)
N.bookcase(cv, lx, -230, 112, 150)
N.broken_chain(cv, lx, -70, lx, 140, r=11)
N.manacle(cv, lx, 210, r=22)
N.iksar_trooper(cv, lx-8, 470, 58)
N.bookcase(cv, lx, 700, 112, 150)
N.root_drip(cv, lx, 760, 150)

# =========================================================== 7. RIGHT MARGIN doodles
rx = (cv.bx1 - INSET + cv.maxx)/2      # ~ maxx+92
N.root_drip(cv, rx, cv.by0+150, 150)
N.war_standard(cv, rx, -120, 60)
N.broken_chain(cv, rx, 20, rx, 230, r=11)
N.bookcase(cv, rx, 470, 112, 150)
N.manacle(cv, rx, 560, r=22)
N.nse_emblem(cv, rx, 760, 60)

# =========================================================== 8. BOTTOM MARGIN row
by = cv.by1-40
N.iksar_trooper(cv, -420, by, 62)
N.war_standard(cv, -220, by, 60)
N.nse_emblem(cv, 30, by-70, 66)
N.bookcase(cv, 250, by-6, 150, 128)

# =========================================================== 9. COMPASS (last, on top)
N.emblem_center = N.emblem_motif
band0=INSET; band1=PAD; bc=(band0+band1)/2; CRpad=max(70,(band1-band0)/2/1.28*0.66)
compass(cv, cv.bx0+bc, cv.by1-bc, CRpad,
        ring=(IRON, ROOT), rose=(IRON, ROOT_D),
        center=N.emblem_motif, center_colors=(N.EMBER, IRON),
        label=ROOT_D, n_label=IRON, arrow=IRON)

cv.write('newsebexp_2.txt')
print('wrote newsebexp_2.txt  L=%d P=%d'%(len(cv.L),len(cv.P)))
