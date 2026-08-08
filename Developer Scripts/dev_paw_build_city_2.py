"""Generic city decoration (_2) with MARGIN STANDARD. Theme-colored frame/title/compass."""
import sys, math
from eqmap_toolkit import Canvas, frame, title, compass, title_band_knockout
ZONE=sys.argv[1]; TITLE=sys.argv[2]; THEME=sys.argv[3]
THEMES={
 'ruins':  dict(OUT=(120,96,54), INN=(176,146,74), GC=(186,172,140), TC=(150,110,50), SH=(176,146,74)),  # oggok sandstone/bronze
 'mud':    dict(OUT=(84,72,50), INN=(120,140,80), GC=(150,144,112), TC=(90,80,54), SH=(120,140,80)),      # grobb
 'dark':   dict(OUT=(50,40,64), INN=(120,90,150), GC=(120,110,130), TC=(90,60,120), SH=(120,90,150)),     # neriak/nektulos
 'dwarf':  dict(OUT=(96,70,44), INN=(180,150,60), GC=(160,150,128), TC=(120,80,40), SH=(180,150,60)),     # kaladim
 'barb':   dict(OUT=(90,70,50), INN=(140,120,90), GC=(150,158,168), TC=(90,70,50), SH=(140,120,90)),      # halas
 'ice':    dict(OUT=(90,120,140), INN=(150,200,220), GC=(170,190,205), TC=(70,110,140), SH=(150,200,220)),# everfrost
 'goblin': dict(OUT=(60,90,50), INN=(120,170,90), GC=(140,160,120), TC=(60,100,50), SH=(120,170,90)),     # runnyeye
 'mtn':    dict(OUT=(90,84,74), INN=(150,150,140), GC=(160,158,150), TC=(80,76,68), SH=(150,150,140)),
 'den':    dict(OUT=(96,72,44), INN=(172,132,58), GC=(150,130,100), TC=(120,80,40), SH=(172,132,58)),    # stonebrunt
}
T=THEMES[THEME]
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
span=max(MAXX-MINX,MAXY-MINY)
PAD=max(150,int(span*0.16)); INSET=int(span*0.05); CLEAR=int(span*0.06)
cv=Canvas((MINX,MAXX,MINY,MAXY),PAD)
g0=len(cv.L)                                   # --- grid + frame (knockout range) ---
STEP=max(120, round(span/8/20)*20)
gx=math.ceil(MINX/STEP)*STEP
while gx<MAXX: cv.add(gx,MINY,gx,MAXY,T['GC']); gx+=STEP
gy=math.ceil(MINY/STEP)*STEP
while gy<MAXY: cv.add(MINX,gy,MAXX,gy,T['GC']); gy+=STEP
for a,b,c,d in [(MINX,MINY,MAXX,MINY),(MINX,MAXY,MAXX,MAXY),(MINX,MINY,MINX,MAXY),(MAXX,MINY,MAXX,MAXY)]: cv.add(a,b,c,d,T['GC'])
frame(cv, outer=T['OUT'], inner=T['INN'], step=max(120,int(span*0.06)), depth=max(30,int(span*0.02)), inset=INSET)
gf1=len(cv.L)                                  # end of grid+frame
title(cv, TITLE, T['TC'], shadow=T['SH'], height=max(120,int(span*0.05)))
title_band_knockout(cv, g0, gf1, pad_x=int(span*0.03), pad_y=int(span*0.05))   # clear grid/border around title
# compass centered in the bottom-left MARGIN band, sized to fit (offset off the corner)
band0=INSET; band1=PAD; bc=(band0+band1)/2
CR=max(70, (band1-band0)/2/1.28*0.66); 
compass(cv, cv.bx0+bc, cv.by1-bc, CR, ring=(T['OUT'],T['INN']), rose=(T['INN'],T['GC']), label=T['OUT'], n_label=T['TC'], arrow=T['TC'])
cv.write(f'{ZONE}_2.txt')
print('%s _2: MARGIN=%d L=%d'%(ZONE, MINX-(cv.bx0+INSET), len(cv.L)))
