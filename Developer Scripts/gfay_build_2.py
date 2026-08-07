"""Greater Faydark decoration (_2): clean grid, title, garlands, broadleaf trees,
wizard-gateway sketch, corner compass. All margin doodles sit inside a CLEAR band
so nothing touches the border. Placement-tracked + overlap-validated."""
import math
from eqmap_toolkit import Canvas, frame, title, compass
import gfay_decor as G
from qrg_decor import leaf_garland, pinecone, leaf_motif, LEAF, WOOD_D

MINX,MAXX,MINY,MAXY = -2699.0, 2663.0, -2709.0, 2736.0
PAD, INSET, CLEAR = 660, 110, 140
cv = Canvas((MINX,MAXX,MINY,MAXY), PAD)
BR=WOOD_D
TIN = INSET+CLEAR                       # doodles stay this far inside the outer border
# safe-zone edges
SX0=cv.bx0+TIN; SX1=cv.bx1-TIN; SY0=cv.by0+TIN; SY1=cv.by1-TIN
TH=160                                  # broadleaf canopy half-width
LX=SX0+TH; RX=SX1-TH

ELEMENTS=[]
def track(name, fn):
    i0=len(cv.L); fn(); seg=cv.L[i0:]
    if not seg: return
    xs=[];ys=[]
    for l in seg:
        f=l[2:].split(','); xs+=[float(f[0]),float(f[3])]; ys+=[float(f[1]),float(f[4])]
    ELEMENTS.append([name,min(xs),min(ys),max(xs),max(ys)])

# ---- clean grid clipped to CONTENT only ----
GC=(196,186,166); STEP=536
gx0=math.ceil(MINX/STEP)*STEP
while gx0<MAXX: cv.add(gx0,MINY,gx0,MAXY,GC); gx0+=STEP
gy0=math.ceil(MINY/STEP)*STEP
while gy0<MAXY: cv.add(MINX,gy0,MAXX,gy0,GC); gy0+=STEP
cv.add(MINX,MINY,MAXX,MINY,GC); cv.add(MINX,MAXY,MAXX,MAXY,GC)
cv.add(MINX,MINY,MINX,MAXY,GC); cv.add(MAXX,MINY,MAXX,MAXY,GC)

# ---- frame + title ----
frame(cv, outer=BR, inner=(120,90,50), step=240, depth=70, inset=INSET,
      corner=lambda c,x,y,sx,sy: pinecone(c, x+sx*80, y+sy*80, 34))
title(cv, "GREATER_FAYDARK", BR, shadow=(150,120,80), height=300)

# ---- compass in the bottom-right CORNER (sized to fit inside the clear band) ----
CR=165; LR=CR*1.30
ccx=SX1-LR; ccy=SY1-LR
band0=INSET; band1=PAD; bc=(band0+band1)/2; CRpad=max(70,(band1-band0)/2/1.28*0.66)
track("compass", lambda: compass(cv, cv.bx1-bc, cv.by1-bc, CRpad,
        ring=(BR,(120,90,50)), rose=(BR,LEAF), center=leaf_motif,
        center_colors=(BR,LEAF), label=BR, n_label=BR, arrow=BR))

# ---- leaf garlands: top full width; bottom stops short of the compass corner ----
track("garland_top", lambda: leaf_garland(cv, SX0+80, SX1-80, SY0, step=150))
track("garland_bot", lambda: leaf_garland(cv, SX0+80, ccx-CR-90, SY1, step=150))

# ---- broadleaf Faydark trees down the side margins (inside the clear band) ----
for k,by in enumerate((-1500,-820,-140,540,1220,1900)):
    track(f"tree_L{k}", lambda by=by,k=k: G.broadleaf_tree(cv, LX, by, h=440, seed=k+1))
for k,by in enumerate((-1500,-820,-140,540,1220)):
    track(f"tree_R{k}", lambda by=by,k=k: G.broadleaf_tree(cv, RX, by, h=440, seed=k+7))

# ---- wizard + gateway in the bottom margin, lifted clear of the border ----
track("wizard", lambda: G.wizard(cv, 220, SY1-40, h=340))

# ---- validate ----
def ov(a,b,p=4): return not (a[3]<b[1]-p or b[3]<a[1]-p or a[4]<b[2]-p or b[4]<a[2]-p)
hits=[(ELEMENTS[i][0],ELEMENTS[j][0]) for i in range(len(ELEMENTS)) for j in range(i+1,len(ELEMENTS)) if ov(ELEMENTS[i],ELEMENTS[j])]
cv.write('gfaydark_2.txt')
print('wrote gfaydark_2.txt L=%d P=%d elements=%d'%(len(cv.L),len(cv.P),len(ELEMENTS)))
print('safe band: %.0f from outer border; compass CR=%d at (%.0f,%.0f)'%(TIN,CR,ccx,ccy))
print('OVERLAPS:', hits if hits else 'none — VALIDATION OK')
