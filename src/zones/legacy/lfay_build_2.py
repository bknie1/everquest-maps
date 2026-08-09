"""Lesser Faydark decoration (_2): dark forest — dark broadleaf trees, orc hut,
pixie, fae drake, leaf garlands, LESSER FAYDARK title, leaf compass. draw_fit + validated."""
import math
from eqmap_toolkit import Canvas, frame, title, compass, draw_fit, knockout, build_occupancy, seg_hits_content, parse_L_segments
import lfay_decor as G
from gfay_decor import broadleaf_tree
from qrg_decor import leaf_garland, pinecone, leaf_motif, LEAF, WOOD_D

MINX,MAXX,MINY,MAXY=-3937.0,2222.0,-2208.0,1182.0
PAD,INSET,CLEAR=520,110,150
cv=Canvas((MINX,MAXX,MINY,MAXY),PAD)
BR=(58,48,36)   # dark bark border
TIN=INSET+CLEAR
SX0=cv.bx0+TIN; SX1=cv.bx1-TIN; SY0=cv.by0+TIN; SY1=cv.by1-TIN
BOX=190

ELEMENTS=[]
def track(name, fn):
    i0=len(cv.L); fn(); seg=cv.L[i0:]
    if not seg: return
    S=[];xs=[];ys=[]
    for l in seg:
        f=l[2:].split(','); a,b,c,d=float(f[0]),float(f[1]),float(f[3]),float(f[4]); S.append((a,b,c,d)); xs+=[a,c]; ys+=[b,d]
    ELEMENTS.append([name,min(xs),min(ys),max(xs),max(ys),S])

GC=(150,150,140); STEP=560
gx=math.ceil(MINX/STEP)*STEP
while gx<MAXX: cv.add(gx,MINY,gx,MAXY,GC); gx+=STEP
gy=math.ceil(MINY/STEP)*STEP
while gy<MAXY: cv.add(MINX,gy,MAXX,gy,GC); gy+=STEP
for a,b,c,d in [(MINX,MINY,MAXX,MINY),(MINX,MAXY,MAXX,MAXY),(MINX,MINY,MINX,MAXY),(MAXX,MINY,MAXX,MAXY)]: cv.add(a,b,c,d,GC)

f0=len(cv.L)
frame(cv, outer=BR, inner=(90,74,50), step=260, depth=70, inset=INSET,
      corner=lambda c,x,y,sx,sy: pinecone(c, x+sx*90, y+sy*90, 40))
leaf_garland(cv, SX0+80, SX1-80, SY0, step=170, c=G.DARKCAN)   # top garland — into the knockout range
f1=len(cv.L)
t0=len(cv.L)
title(cv, "LESSER_FAYDARK", BR, shadow=(110,90,60), height=300)
tseg=[]
for l in cv.L[t0:]:
    f=l[2:].split(','); tseg.append((float(f[0]),float(f[1]),float(f[3]),float(f[4])))
knockout(cv, f0, f1, tseg, pad=24)   # frame + garland weave behind the title strokes

track("garland_bot", lambda: leaf_garland(cv, SX0+80, SX1-80, SY1, step=170, c=G.DARKCAN))

# side margins, spaced so nothing overlaps (draw_fit keeps each within BOX)
GAP=70
LX=MINX-GAP-BOX/2; RX=MAXX+GAP+BOX/2   # fixed gap outside content on both sides
track("pixie",   lambda: draw_fit(cv, lambda c: G.pixie(c,0,0,s=180), LX, -1900, BOX*0.8, BOX*0.8))
track("drake",   lambda: draw_fit(cv, lambda c: G.fae_drake(c,0,0,s=200), RX, -1900, BOX, BOX*0.8))
for k,by in enumerate((-950,150)):
    track(f"tree_L{k}", lambda by=by,k=k: draw_fit(cv, lambda c: broadleaf_tree(c,0,0,h=460,seed=k+1), LX, by, BOX, BOX*1.1))
    track(f"tree_R{k}", lambda by=by,k=k: draw_fit(cv, lambda c: broadleaf_tree(c,0,0,h=460,seed=k+5), RX, by, BOX, BOX*1.1))
track("orc_hut", lambda: draw_fit(cv, lambda c: G.orc_hut(c,0,0,s=180), LX, 1150, BOX*0.9, BOX*0.9))

CR=200; LR=CR*1.30
band0=INSET; band1=PAD; bc=(band0+band1)/2; CRpad=max(70,(band1-band0)/2/1.28*0.66)
track("compass", lambda: compass(cv, cv.bx1-bc, cv.by1-bc, CRpad,
        ring=(BR,(90,74,50)), rose=(BR,LEAF), center=leaf_motif,
        center_colors=(BR,G.DARKCAN), label=BR, n_label=BR, arrow=BR))

def ov(a,b,p=4): return not (a[3]<b[1]-p or b[3]<a[1]-p or a[4]<b[2]-p or b[4]<a[2]-p)
hits=[(ELEMENTS[i][0],ELEMENTS[j][0]) for i in range(len(ELEMENTS)) for j in range(i+1,len(ELEMENTS)) if ov(ELEMENTS[i],ELEMENTS[j])]
occ=build_occupancy(parse_L_segments('lfaydark_colored.txt'), (MINX,MAXX,MINY,MAXY), cell=40, dilate=1)
content_hits=[e[0] for e in ELEMENTS if seg_hits_content(e[5], occ)]
cv.write('lfaydark_2.txt')
print('wrote lfaydark_2.txt L=%d elements=%d'%(len(cv.L),len(ELEMENTS)))
print('SKETCH OVERLAPS:', hits if hits else 'none')
print('CONTENT OVERLAPS:', content_hits if content_hits else 'none — VALIDATION OK')
