"""Felwithe decoration (_2) — MARGIN PASS standard: content sits inside a clear parchment
margin, grid clipped to content bbox, frame drawn PAD outside. High-elf gold/marble theme."""
import sys, math
from eqmap_toolkit import Canvas, frame, title, compass, title_band_knockout
ZONE=sys.argv[1]; TITLE=sys.argv[2]
def parse(path):
    L=[]
    for l in open(path,encoding='utf-8',errors='replace'):
        l=l.strip()
        if l.startswith('L'):
            f=l[2:].split(','); L.append((float(f[0]),float(f[1]),float(f[3]),float(f[4])))
    return L
B=parse(f'{ZONE}.txt')
xs=[v for a,b,c,d in B for v in (a,c)]; ys=[v for a,b,c,d in B for v in (b,d)]
MINX,MAXX,MINY,MAXY=min(xs),max(xs),min(ys),max(ys)
# --- MARGIN STANDARD: PAD - INSET leaves a clear band between content and inner border ---
PAD,INSET,CLEAR=240,80,110
cv=Canvas((MINX,MAXX,MINY,MAXY),PAD)
GOLD=(180,150,60); MARBLE=(150,138,120); BROWN=(110,90,70); GREEN=(45,95,55); RED=(150,40,40); GC=(178,172,158)
TIN=INSET+CLEAR
SX0=cv.bx0+TIN; SX1=cv.bx1-TIN; SY0=cv.by0+TIN; SY1=cv.by1-TIN
# grid — ONLY across the content bbox (leaves the margin band clear)
g0=len(cv.L)
STEP=max(120, round(max(MAXX-MINX,MAXY-MINY)/8/20)*20)
gx=math.ceil(MINX/STEP)*STEP
while gx<MAXX: cv.add(gx,MINY,gx,MAXY,GC); gx+=STEP
gy=math.ceil(MINY/STEP)*STEP
while gy<MAXY: cv.add(MINX,gy,MAXX,gy,GC); gy+=STEP
for a,b,c,d in [(MINX,MINY,MAXX,MINY),(MINX,MAXY,MAXX,MAXY),(MINX,MINY,MINX,MAXY),(MAXX,MINY,MAXX,MAXY)]: cv.add(a,b,c,d,GC)
# high-elf banner corner motif (red/gold shield)
def banner(c,x,y,s,col,g):
    c.add(x-s*0.4,y-s*0.7,x+s*0.4,y-s*0.7,g); c.add(x-s*0.4,y-s*0.7,x-s*0.4,y+s*0.5,col)
    c.add(x+s*0.4,y-s*0.7,x+s*0.4,y+s*0.5,col); c.add(x-s*0.4,y+s*0.5,x,y+s*0.85,col); c.add(x+s*0.4,y+s*0.5,x,y+s*0.85,col)
    c.add(x,y-s*0.55,x,y+s*0.3,g); c.add(x-s*0.18,y-s*0.2,x+s*0.18,y-s*0.2,g)
# frame with gold/marble border + banner corners
frame(cv, outer=BROWN, inner=GOLD, step=260, depth=70, inset=INSET,
      corner=lambda c,x,y,sx,sy: banner(c, x+sx*70, y+sy*70, 70, RED, GOLD))
gf1=len(cv.L)
# title
title(cv, TITLE, (150,60,25), shadow=GOLD, height=250)
title_band_knockout(cv, g0, gf1, pad_x=int(span*0.03) if "span" in dir() else 80, pad_y=int(span*0.05) if "span" in dir() else 100)
# compass in a corner
band0=INSET; band1=PAD; bc=(band0+band1)/2
CR=max(70,(band1-band0)/2/1.28*0.66)
compass(cv, cv.bx0+bc, cv.by1-bc, CR, ring=(BROWN,GOLD), rose=(GOLD,MARBLE), label=BROWN, n_label=(150,60,25), arrow=(150,60,25))
cv.write(f'{ZONE}_2.txt')
# report the achieved margin
inner_x0=cv.bx0+INSET
print('%s: content x[%.0f,%.0f] inner-border x0=%.0f  MARGIN=%.0f  L=%d'%(ZONE,MINX,MAXX,inner_x0,MINX-inner_x0,len(cv.L)))
