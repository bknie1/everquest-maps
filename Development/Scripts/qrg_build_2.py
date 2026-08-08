"""Surefall Glade decoration (_2): nature/ranger-druid theme.
Longbows on the side borders, leaf garlands top & bottom, tall redwood pines in
the margins, SUREFALL GLADE title, leaf compass. Placement-tracked + overlap-validated."""
import random, math
from eqmap_toolkit import Canvas, frame, grid, title, compass
import qrg_decor as G
random.seed(11)

MINX,MAXX,MINY,MAXY = -279.0, 713.0, -867.0, 616.0
PAD, INSET = 235, 40
cv = Canvas((MINX,MAXX,MINY,MAXY), PAD)
BR=G.WOOD_D; LEAF=G.LEAF; WOOD=G.WOOD

LX=(cv.bx0+INSET+cv.minx)/2
RX=(cv.bx1-INSET+cv.maxx)/2
TY=(cv.by0+INSET+cv.miny)/2
BY=(cv.by1-INSET-cv.maxy)/2 + cv.maxy
midy=(MINY+MAXY)/2

ELEMENTS=[]
def track(name, fn):
    i0=len(cv.L); fn(); seg=cv.L[i0:]
    if not seg: return
    xs=[];ys=[]
    for l in seg:
        f=l[2:].split(','); xs+=[float(f[0]),float(f[3])]; ys+=[float(f[1]),float(f[4])]
    ELEMENTS.append([name,min(xs),min(ys),max(xs),max(ys)])

# ---- structural: grid + thin branch frame ----
grid(cv, (188,178,158), step=200)
frame(cv, outer=BR, inner=(140,104,60), step=110, depth=26, inset=INSET,
      corner=lambda c,x,y,sx,sy: G.pinecone(c, x+sx*40, y+sy*40, 16))

# ---- title ----
title(cv, "SUREFALL_GLADE", BR, shadow=(150,120,80), height=120)

# ---- top & bottom leaf garlands ----
track("garland_top", lambda: G.leaf_garland(cv, cv.bx0+INSET+40, cv.bx1-INSET-40, cv.by0+INSET+26))
track("garland_bot", lambda: G.leaf_garland(cv, cv.bx0+INSET+40, cv.bx1-INSET-40, cv.by1-INSET-26))

# ---- redwood pines fill the side margins (bows dropped in favor of more trees) ----
import random as _r
for k,by in enumerate((-720,-480,-240,0,240,480)):
    hh=190+((k*53)%40)-20
    track(f"pine_L{k}", lambda by=by,hh=hh: G.redwood_pine(cv, LX, by, h=hh))
    track(f"pine_R{k}", lambda by=by,hh=hh: G.redwood_pine(cv, RX, by, h=hh))

# ---- compass with leaf motif, in the open lower-left of the map ----
band0=INSET; band1=PAD; bc=(band0+band1)/2; CRpad=max(70,(band1-band0)/2/1.28*0.66)
track("compass", lambda: compass(cv, cv.bx0+bc, cv.by1-bc, CRpad,
        ring=(BR, (140,104,60)), rose=(BR, LEAF),
        center=G.leaf_motif, center_colors=(BR, LEAF),
        label=BR, n_label=BR, arrow=BR))

# ---- validate ----
def overlaps(a,b,pad=2):
    return not (a[3]<b[1]-pad or b[3]<a[1]-pad or a[4]<b[2]-pad or b[4]<a[2]-pad)
hits=[(ELEMENTS[i][0],ELEMENTS[j][0]) for i in range(len(ELEMENTS)) for j in range(i+1,len(ELEMENTS)) if overlaps(ELEMENTS[i],ELEMENTS[j])]
cv.write('qrg_2.txt')
print('wrote qrg_2.txt  L=%d P=%d  elements=%d'%(len(cv.L),len(cv.P),len(ELEMENTS)))
print('OVERLAPS:', hits if hits else 'none — VALIDATION OK')
