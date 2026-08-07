"""Steamfont decoration (_2): corner steaming mountains + low linking range (below
content), gear compass, fitted margin creatures. Sketch-vs-sketch AND sketch-vs-content
validation."""
import math
from eqmap_toolkit import Canvas, frame, title, compass, draw_fit, build_occupancy, seg_hits_content, parse_L_segments
import steam_decor as G

MINX,MAXX,MINY,MAXY=-2217.0,2447.0,-1955.0,2063.0
PAD,INSET,CLEAR=440,90,120
cv=Canvas((MINX,MAXX,MINY,MAXY),PAD)
BR=G.ROCK_D; TIN=INSET+CLEAR
SX0=cv.bx0+TIN; SX1=cv.bx1-TIN; SY0=cv.by0+TIN; SY1=cv.by1-TIN
BOX=240; LX=SX0+BOX/2; RX=SX1-BOX/2

ELEMENTS=[]
def track(name, fn):
    i0=len(cv.L); fn(); seg=cv.L[i0:]
    if not seg: return
    S=[]; xs=[]; ys=[]
    for l in seg:
        f=l[2:].split(','); a,b,c,d=float(f[0]),float(f[1]),float(f[3]),float(f[4])
        S.append((a,b,c,d)); xs+=[a,c]; ys+=[b,d]
    ELEMENTS.append([name,min(xs),min(ys),max(xs),max(ys),S])

GC=(196,186,168); STEP=520
gx=math.ceil(MINX/STEP)*STEP
while gx<MAXX: cv.add(gx,MINY,gx,MAXY,GC); gx+=STEP
gy=math.ceil(MINY/STEP)*STEP
while gy<MAXY: cv.add(MINX,gy,MAXX,gy,GC); gy+=STEP
for a,b,c,d in [(MINX,MINY,MAXX,MINY),(MINX,MAXY,MAXX,MAXY),(MINX,MINY,MINX,MAXY),(MAXX,MINY,MAXX,MAXY)]: cv.add(a,b,c,d,GC)

frame(cv, outer=BR, inner=(120,104,80), step=220, depth=60, inset=INSET,
      corner=lambda c,x,y,sx,sy: G.gear(c, x+sx*70, y+sy*70, 44, teeth=9, c=G.STEEL))
title(cv, "STEAMFONT_MOUNTAINS", BR, shadow=(150,120,80), height=250)

# --- bottom border: two STEAMING mountains in the corners + a low linking range ---
def link_range(x0,x1,base_y,n):
    step=(x1-x0)/n
    for k in range(n):
        cxk=x0+step*(k+0.5); w=step*1.08; h=104+24*(k%2)          # FIXED short peaks
        G._poly(cv,[(cxk-w/2,base_y),(cxk,base_y-h),(cxk+w/2,base_y)],G.ROCK)
        cv.add(cxk-w*0.2,base_y-h*0.5,cxk+w*0.2,base_y-h*0.5,G.ROCK)
track("steamer_BL", lambda: G.mountain_steam(cv, SX0+110, SY1, w=190, h=210))
track("steamer_BR", lambda: G.mountain_steam(cv, SX1-110, SY1, w=190, h=210))
track("mtn_range_bot", lambda: link_range(SX0+260, SX1-260, SY1, n=16))

def _cogs(c): G.gear(c,-40,40,90,teeth=12,c=G.STEEL); G.gear(c,60,-60,55,teeth=9,c=G.BRASS)
track("minotaur",  lambda: draw_fit(cv, lambda c: G.minotaur_head(c,0,0,s=180), LX, -1000, BOX, BOX))
track("cwspider_L",lambda: draw_fit(cv, lambda c: G.clockwork_spider(c,0,0,s=180), LX, -150, BOX, BOX))
track("kobold",    lambda: draw_fit(cv, lambda c: G.kobold(c,0,0,s=180), LX, 850, BOX, BOX))
track("cogs_R",    lambda: draw_fit(cv, _cogs, RX, -1000, BOX, BOX))
track("windmills",lambda: draw_fit(cv, lambda c: G.windmill_cluster(c,0,0,s=190), RX, -150, BOX, BOX))
track("mtn_R",     lambda: draw_fit(cv, lambda c: G.mountain_steam(c,0,0,w=260,h=300), RX, 850, BOX, BOX))

CR=180; LR=CR*1.30
track("compass", lambda: compass(cv, SX1-LR, SY0+LR, CR,
        ring=(BR,G.STEEL), rose=(BR,G.BRASS), center=G.cog_motif,
        center_colors=(G.STEEL,G.BRASS), label=BR, n_label=BR, arrow=BR))

# --- validation: sketch-vs-sketch AND sketch-vs-map-content ---
def ov(a,b,p=4): return not (a[3]<b[1]-p or b[3]<a[1]-p or a[4]<b[2]-p or b[4]<a[2]-p)
hits=[(ELEMENTS[i][0],ELEMENTS[j][0]) for i in range(len(ELEMENTS)) for j in range(i+1,len(ELEMENTS)) if ov(ELEMENTS[i],ELEMENTS[j])]
occ=build_occupancy(parse_L_segments('steamfont_colored.txt'), (MINX,MAXX,MINY,MAXY), cell=40, dilate=1)
content_hits=[e[0] for e in ELEMENTS if seg_hits_content(e[5], occ)]
cv.write('steamfont_2.txt')
print('wrote steamfont_2.txt L=%d elements=%d'%(len(cv.L),len(ELEMENTS)))
print('SKETCH OVERLAPS:', hits if hits else 'none')
print('CONTENT OVERLAPS:', content_hits if content_hits else 'none — VALIDATION OK')
