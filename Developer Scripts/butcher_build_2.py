"""Butcherblock decoration (_2): rune-style dwarven title, POIs spatially placed into
the margin cell nearest each POI's map location, axe compass, low stone range.
Title knockout + sketch/content validation."""
import math
from eqmap_toolkit import (Canvas, frame, title, compass, draw_fit, knockout,
    build_occupancy, seg_hits_content, parse_L_segments, margin_cells, place_poi_sketches)
import butcher_decor as G

MINX,MAXX,MINY,MAXY=-4009.0,3283.0,-3172.0,3179.0
PAD,INSET,CLEAR=580,120,150
cv=Canvas((MINX,MAXX,MINY,MAXY),PAD)
BR=G.STONE_D; TIN=INSET+CLEAR
SX0=cv.bx0+TIN; SX1=cv.bx1-TIN; SY0=cv.by0+TIN; SY1=cv.by1-TIN

ELEMENTS=[]
def track(name, segs):
    if not segs: return
    xs=[v for s in segs for v in (s[0],s[2])]; ys=[v for s in segs for v in (s[1],s[3])]
    ELEMENTS.append([name,min(xs),min(ys),max(xs),max(ys),segs])
def track_fn(name, fn):
    i0=len(cv.L); fn()
    track(name,[(float(l[2:].split(',')[0]),float(l[2:].split(',')[1]),float(l[2:].split(',')[3]),float(l[2:].split(',')[4])) for l in cv.L[i0:]])

GC=(150,146,138); STEP=560
gx=math.ceil(MINX/STEP)*STEP
while gx<MAXX: cv.add(gx,MINY,gx,MAXY,GC); gx+=STEP
gy=math.ceil(MINY/STEP)*STEP
while gy<MAXY: cv.add(MINX,gy,MAXX,gy,GC); gy+=STEP
for a,b,c,d in [(MINX,MINY,MAXX,MINY),(MINX,MAXY,MAXX,MAXY),(MINX,MINY,MINX,MAXY),(MAXX,MINY,MAXX,MAXY)]: cv.add(a,b,c,d,GC)

# frame + RUNE title with knockout
f0=len(cv.L)
frame(cv, outer=BR, inner=(110,96,74), step=300, depth=80, inset=INSET,
      corner=lambda c,x,y,sx,sy: G.axe_motif(c, x+sx*90, y+sy*90, 46, BR, G.IRON))
f1=len(cv.L); t0=len(cv.L)
G.rune_title(cv, "BUTCHERBLOCK", BR, shadow=(120,104,80), height=300)
tseg=[(float(l[2:].split(',')[0]),float(l[2:].split(',')[1]),float(l[2:].split(',')[3]),float(l[2:].split(',')[4])) for l in cv.L[t0:]]
knockout(cv, f0, f1, tseg, pad=30)

# POIs → nearest margin cell to each real location (native coords, EQL wiki as truth)
Lc = margin_cells(cv, INSET, CLEAR, 'L', 4, fill=0.74)
Rc = margin_cells(cv, INSET, CLEAR, 'R', 4, fill=0.74)
pois=[
 {'priority':10,'label':'THE CHESSBOARD','fn':lambda c:G.chessboard(c,0,0,200),'loc':(2280,-847)},
 {'priority':9, 'label':'KALADIM','fn':lambda c:G.dwarf_face(c,0,0,200),'loc':(224,-3041)},
 {'priority':9, 'label':'THE DOCKS','fn':lambda c:G.boat(c,0,0,200),'loc':(-3256,-1354)},
 {'priority':8, 'label':'DWARVES','fn':lambda c:G.dwarf(c,0,0,200),'loc':(688,-2793)},
 {'priority':7, 'label':'STONE RING','fn':lambda c:G.stone_ring(c,0,0,200),'loc':(1645,-1335)},
 {'priority':5, 'label':'GOBLINS','fn':lambda c:G.goblin(c,0,0,200),'loc':(-471,1080)},
 {'priority':4, 'label':'KRAG AVIAKS','fn':lambda c:G.aviak(c,0,0,200),'loc':(3061,1316)},
]
for lbl,cx,cy,seg in place_poi_sketches(cv, Lc, Rc, pois, label_color=BR):
    track('poi:'+lbl, seg)

def stone_range(x0,x1,base_y,n):
    step=(x1-x0)/n
    for k in range(n):
        cxk=x0+step*(k+0.5); w=step*1.08; h=110+26*(k%2)
        G._poly(cv,[(cxk-w/2,base_y),(cxk,base_y-h),(cxk+w/2,base_y)],G.STONE)
        cv.add(cxk-w*0.2,base_y-h*0.5,cxk+w*0.2,base_y-h*0.5,G.STONE)
track_fn("range_bot", lambda: stone_range(SX0+40, SX1-40, SY1, 18))

CR=210; LR=CR*1.30
track_fn("compass", lambda: compass(cv, SX1-LR, SY0+LR, CR,
        ring=(BR,G.IRON), rose=(BR,G.BEARD), center=G.axe_motif,
        center_colors=(BR,G.IRON), label=BR, n_label=BR, arrow=BR))

def ov(a,b,p=4): return not (a[3]<b[1]-p or b[3]<a[1]-p or a[4]<b[2]-p or b[4]<a[2]-p)
hits=[(ELEMENTS[i][0],ELEMENTS[j][0]) for i in range(len(ELEMENTS)) for j in range(i+1,len(ELEMENTS)) if ov(ELEMENTS[i],ELEMENTS[j])]
occ=build_occupancy(parse_L_segments('butcher_colored.txt'), (MINX,MAXX,MINY,MAXY), cell=44, dilate=1)
content_hits=[e[0] for e in ELEMENTS if seg_hits_content(e[5], occ)]
cv.write('butcher_2.txt')
print('wrote butcher_2.txt L=%d elements=%d'%(len(cv.L),len(ELEMENTS)))
print('SKETCH OVERLAPS:', hits if hits else 'none')
print('CONTENT OVERLAPS:', content_hits if content_hits else 'none — VALIDATION OK')
