import sys, math
from eqmap_toolkit import Canvas, frame, title, compass, title_band_knockout
ZONE=sys.argv[1]; TITLE=sys.argv[2]; THEME=sys.argv[3]
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
# margin standard: PAD-INSET clear band ~ 12-14% of content
span=max(MAXX-MINX,MAXY-MINY)
PAD=int(span*0.16); INSET=int(span*0.05); CLEAR=int(span*0.06)
cv=Canvas((MINX,MAXX,MINY,MAXY),PAD)
if THEME=='swamp': OUT=(70,80,50); INN=(120,140,80); GC=(120,132,96); TCOL=(70,96,50); SHAD=(120,140,80)
else:              OUT=(40,58,36); INN=(90,120,70); GC=(96,116,86); TCOL=(46,72,40); SHAD=(90,120,70)
TIN=INSET+CLEAR; SX0=cv.bx0+TIN; SX1=cv.bx1-TIN; SY0=cv.by0+TIN; SY1=cv.by1-TIN
g0=len(cv.L)
STEP=max(200, round(span/9/50)*50)
gx=math.ceil(MINX/STEP)*STEP
while gx<MAXX: cv.add(gx,MINY,gx,MAXY,GC); gx+=STEP
gy=math.ceil(MINY/STEP)*STEP
while gy<MAXY: cv.add(MINX,gy,MAXX,gy,GC); gy+=STEP
for a,b,c,d in [(MINX,MINY,MAXX,MINY),(MINX,MAXY,MAXX,MAXY),(MINX,MINY,MINX,MAXY),(MAXX,MINY,MAXX,MAXY)]: cv.add(a,b,c,d,GC)
def leaf(c,x,y,s,col):  # simple leaf/reed corner motif
    c.add(x,y-s,x,y+s*0.4,col); c.add(x,y-s,x-s*0.5,y-s*0.2,col); c.add(x,y-s,x+s*0.5,y-s*0.2,col)
    c.add(x,y-s*0.3,x-s*0.5,y+s*0.3,col); c.add(x,y-s*0.3,x+s*0.5,y+s*0.3,col)
frame(cv, outer=OUT, inner=INN, step=int(span*0.06), depth=int(span*0.02), inset=INSET,
      corner=lambda c,x,y,sx,sy: leaf(c, x+sx*int(span*0.02), y+sy*int(span*0.02), int(span*0.03), OUT))
gf1=len(cv.L)
title(cv, TITLE, TCOL, shadow=SHAD, height=int(span*0.055))
title_band_knockout(cv, g0, gf1, pad_x=int(span*0.03) if "span" in dir() else 80, pad_y=int(span*0.05) if "span" in dir() else 100)
band0=INSET; band1=PAD; bc=(band0+band1)/2
CR=max(70,(band1-band0)/2/1.28*0.66)
compass(cv, cv.bx0+bc, cv.by1-bc, CR, ring=(OUT,INN), rose=(INN,GC), label=OUT, n_label=TCOL, arrow=TCOL)
cv.write(f'{ZONE}_2.txt')
print('%s _2: MARGIN=%d L=%d'%(ZONE, MINX-(cv.bx0+INSET), len(cv.L)))
