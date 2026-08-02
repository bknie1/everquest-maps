"""lavastorm_build.py -- full pipeline for Lavastorm via eqmap_toolkit + fire doodles."""
import numpy as np, random, math
import eqmap_toolkit as T
random.seed(11)
BASE="/mnt/user-data/uploads/lavastorm.txt"; OUT="/mnt/user-data/outputs/lavastorm_2.txt"
DK=(60,45,45); EMBER=(155,65,30); GRID=(98,78,72); TITLE=(165,90,55); TSH=(75,45,40)
ROCK=(95,72,62); LAVA_FILL=(210,90,25); STEAM=(205,200,195)
DRAKE=(175,55,40); ELEM=(220,95,25); HIDE=(170,120,60); SPOT=(70,50,30)
N=lambda Y,X:(-X,-Y)

segs=[]
for l in open(BASE).read().replace('\r\n','\n').split('\n'):
    if l.startswith('L'):
        f=l[2:].split(','); segs.append((float(f[0]),float(f[1]),float(f[3]),float(f[4]),int(f[6]),int(f[7]),int(f[8])))
A=np.array([[s[0],s[1],s[2],s[3]] for s in segs]); exy=np.vstack([A[:,0:2],A[:,2:4]])
bbox=(A[:,[0,2]].min(),A[:,[0,2]].max(),A[:,[1,3]].min(),A[:,[1,3]].max())
minx,maxx,miny,maxy=bbox
cv=T.Canvas(bbox, pad=650, gstep=550)
def near_geo(x,y,th=180): return ((exy[:,0]-x)**2+(exy[:,1]-y)**2).min() < th*th

T.grid(cv, GRID)
def ember_corner(c,x,y,sx,sy):
    for r in (70,150,230):
        c.add(x,y+sy*r,x+sx*r*0.6,y+sy*r*0.55,EMBER); c.add(x+sx*r,y,x+sx*r*0.55,y+sy*r*0.55,EMBER)
T.frame(cv, DK, EMBER, step=120, depth=75, corner=ember_corner)

# fill base red lava pools -- EVEN-ODD scanline on the REAL outlines
# (no hull over-fill; adjacent pools stay separate; nothing spills past the lava edge)
red=[i for i,s in enumerate(segs) if (s[4],s[5],s[6])==(255,0,0)]
redseg=[(segs[i][0],segs[i][1],segs[i][2],segs[i][3]) for i in red]
ry=[s[1] for s in redseg]+[s[3] for s in redseg]
yv=min(ry)+3
while yv<max(ry)-3:
    xs=[]
    for (x1,y1,x2,y2) in redseg:
        if (y1<=yv<y2) or (y2<=yv<y1): xs.append(x1+(x2-x1)*(yv-y1)/(y2-y1))  # half-open: each vertex once
    xs.sort()
    for j in range(0,len(xs)-1,2): cv.add(xs[j],yv,xs[j+1],yv,LAVA_FILL)  # fill inside pairs, skip gaps
    yv+=11

# cluster outlines -> per-pool centroids (steam + caldera sizing only; NOT used for fill)
from collections import defaultdict
parent={i:i for i in red}
def find(a):
    while parent[a]!=a: parent[a]=parent[parent[a]]; a=parent[a]
    return a
TH=55; buck=defaultdict(list)
for i in red:
    for (x,y) in [(segs[i][0],segs[i][1]),(segs[i][2],segs[i][3])]: buck[(int(x//TH),int(y//TH))].append((x,y,i))
for i in red:
    for (x,y) in [(segs[i][0],segs[i][1]),(segs[i][2],segs[i][3])]:
        kx,ky=int(x//TH),int(y//TH)
        for dx in (-1,0,1):
            for dy in (-1,0,1):
                for (ox,oy,j) in buck.get((kx+dx,ky+dy),[]):
                    if (x-ox)**2+(y-oy)**2<=TH*TH: parent[find(i)]=find(j)
pools=defaultdict(list)
for i in red: pools[find(i)].append(i)
pools_info=[]
for idxs in pools.values():
    if len(idxs)<4: continue
    pts=[]
    for i in idxs: pts+=[(segs[i][0],segs[i][1]),(segs[i][2],segs[i][3])]
    cx=sum(p[0] for p in pts)/len(pts); cy=sum(p[1] for p in pts)/len(pts)
    rad=np.mean([((p[0]-cx)**2+(p[1]-cy)**2)**0.5 for p in pts])
    area=(max(p[0] for p in pts)-min(p[0] for p in pts))*(max(p[1] for p in pts)-min(p[1] for p in pts))
    pools_info.append((cx,cy,rad,area))
    for _ in range(2):
        sx=cx+random.uniform(-30,30)
        for k in range(3): cv.add(sx,cy-k*12,sx+random.uniform(-7,7),cy-(k+1)*12,STEAM)
npool=len(pools_info)

# Eye of Ro caldera: inner detailing over the existing north lava pool (near Temple entrance)
north=[p for p in pools_info if p[1] < -300]
if north:
    ex,ey,er,_=max(north, key=lambda p:p[3])
    T.caldera_inner(cv, ex, ey, er, rock=ROCK, lava=LAVA_FILL)
    print(f"  caldera overlaid on north pool at ({ex:.0f},{ey:.0f}) r={er:.0f}")

# fire elementals at spawn points (wiki Y,X)
for Y,X in [(60,-185),(285,-15),(467,-827),(-855,505),(-975,600),(-1165,145)]:
    x,y=N(Y,X); T.fire_elemental(cv,x,y,60,ELEM)
# goblin huts at camps
T.goblin_hut(cv, -368, -1135, 70, 55, HIDE, SPOT)   # beside Fire Goblin Camp #2 round shape
T.goblin_hut(cv,  178,   425, 55, 45, HIDE, SPOT)   # beside Goblin Camp #5 round shape
# fire drakes -- only within the real bounds (near geometry)
corridor_y=miny+0.70*(maxy-miny)   # keep drakes out of the bottom Nektulos-path corridor
placed=0; tries=0
while placed<11 and tries<800:
    tries+=1; rx=random.uniform(minx+150,maxx-150); ry=random.uniform(miny+150,corridor_y)
    dens=((exy[:,0]-rx)**2+(exy[:,1]-ry)**2 < 250**2).sum()
    if near_geo(rx,ry,130) and dens>=14: T.drake(cv,rx,ry,random.uniform(38,52),DRAKE); placed+=1

# Temple of Solusek Ro -> UPPER-LEFT margin, opposite the compass
T.solro_temple(cv, cv.margin_x('left'), cv.row_y(0), 135, 200)
# Solusek Ro face icon -> left margin, below the temple (recurring-character sketch)
T.solusek_ro_face(cv, cv.margin_x('left'), cv.row_y(3), 95, dark=(45,40,45), flame=(170,50,30), eye=(180,55,35))

# title + flame compass (2nd row, right, on top)
T.title(cv, "LAVASTORM", TITLE, shadow=TSH)
T.compass(cv, cv.margin_x('right'), cv.row_y(0), 150, ring=(EMBER,ROCK), rose=(EMBER,ROCK),
          center=T.flame_motif, center_colors=(EMBER,LAVA_FILL), label=EMBER, n_label=ROCK, arrow=EMBER)

cv.write(OUT)
print(f"{OUT}: {len(cv.L)} L + {len(cv.P)} P | filled {npool} pools, {placed} drakes in-bounds")
