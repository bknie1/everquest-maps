import math
from eqmap_toolkit import Canvas, frame, title, compass, title_band_knockout, kobold_motif, peak_motif
def parse(path):
    L=[]
    for l in open(path,encoding='utf-8',errors='replace'):
        l=l.strip()
        if l.startswith('L'):
            f=l[2:].split(','); L.append((float(f[0]),float(f[1]),float(f[3]),float(f[4])))
    return L
B=parse('stonebrunt.txt')
xs=[v for a,b,c,d in B for v in (a,c)]; ys=[v for a,b,c,d in B for v in (b,d)]
MINX,MAXX,MINY,MAXY=min(xs),max(xs),min(ys),max(ys)
span=max(MAXX-MINX,MAXY-MINY)
PAD=max(150,int(span*0.15)); INSET=int(span*0.05); CLEAR=int(span*0.05)
cv=Canvas((MINX,MAXX,MINY,MAXY),PAD)
OUT=(96,88,76); INN=(150,146,138); GC=(160,158,150); TC=(84,78,68); SH=(150,146,138); SNOW=(220,224,228); RIDGE=(120,112,100)
g0=len(cv.L)
STEP=max(600, round(span/8/100)*100)
gx=math.ceil(MINX/STEP)*STEP
while gx<MAXX: cv.add(gx,MINY,gx,MAXY,GC); gx+=STEP
gy=math.ceil(MINY/STEP)*STEP
while gy<MAXY: cv.add(MINX,gy,MAXX,gy,GC); gy+=STEP
for a,b,c,d in [(MINX,MINY,MAXX,MINY),(MINX,MAXY,MAXX,MAXY),(MINX,MINY,MINX,MAXY),(MAXX,MINY,MAXX,MAXY)]: cv.add(a,b,c,d,GC)
# frame with snow-peak corner motifs (kobold mountains)
frame(cv, outer=OUT, inner=INN, step=int(span*0.06), depth=int(span*0.02), inset=INSET,
      corner=lambda c,x,y,sx,sy: peak_motif(c, x+sx*int(span*0.02), y+sy*int(span*0.02), int(span*0.022), RIDGE, SNOW))
gf1=len(cv.L)
title(cv, "STONEBRUNT", TC, shadow=SH, height=int(span*0.05))
title_band_knockout(cv, g0, gf1, pad_x=int(span*0.03), pad_y=int(span*0.05))
# kobold-face compass in the bottom-left margin
band0=INSET; band1=PAD; bc=(band0+band1)/2
CR=max(90,(band1-band0)/2/1.28*0.66)
compass(cv, cv.bx0+bc, cv.by1-bc, CR, ring=(OUT,INN), rose=(INN,GC),
        center=kobold_motif, center_colors=((84,70,58),(120,100,80)), label=OUT, n_label=TC, arrow=TC)
cv.write('stonebrunt_2.txt')
print('stonebrunt _2: L=%d (kobold compass + peak corners)'%len(cv.L))
