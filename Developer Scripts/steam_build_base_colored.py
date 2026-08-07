"""Steamfont CORRECTED base: inside the green loops = rock + STEAM mountains;
between them = green FOREST (trees). Plus iconic gnome WINDMILLS. Tan paths kept."""
import numpy as np, math, random
from scipy.ndimage import binary_dilation, label
import steam_decor as G
def parse(path):
    out=[]
    for l in open(path,encoding='utf-8',errors='replace'):
        l=l.strip()
        if not l.startswith('L'): continue
        f=l[2:].split(','); out.append((float(f[0]),float(f[1]),float(f[2]),float(f[3]),float(f[4]),float(f[5]),(int(f[6]),int(f[7]),int(f[8]))))
    return out
B=parse('steamfont_base.txt')
minx,maxx,miny,maxy=-2217,2447,-1955,2063
ROCK=(140,120,95); ROCK_D=(112,94,72); RIDGE=(120,100,78); STEAM=(205,205,210)
TREE=(46,112,54); TREE_D=(34,88,42); PATH=(150,116,66)
z0=0.0; out=[]
def emit(x1,y1,x2,y2,c): out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z0,x2,y2,z0,c[0],c[1],c[2]))

CELL=18.0; gw=int((maxx-minx)/CELL)+2; gh=int((maxy-miny)/CELL)+2
gx=lambda x:int((x-minx)/CELL); gy=lambda y:int((y-miny)/CELL)
def raster(cond,dil=0):
    m=np.zeros((gh,gw),bool)
    for s in B:
        if cond(s[6]):
            x1,y1,x2,y2=s[0],s[1],s[3],s[4]; n=int(max(abs(x2-x1),abs(y2-y1))/CELL)+1
            for i in range(n+1):
                t=i/n; ix=gx(x1+(x2-x1)*t); iy=gy(y1+(y2-y1)*t)
                if 0<=ix<gw and 0<=iy<gh: m[iy,ix]=True
    return binary_dilation(m,iterations=dil) if dil else m
xg=(np.arange(gw)*CELL+minx)[None,:]; yg=(np.arange(gh)*CELL+miny)[:,None]
green=raster(lambda c:c in ((0,150,0),(0,125,0)),dil=1)
path=raster(lambda c:c==(150,100,0),dil=1)
free=~green; lbl,n=label(free)
edge=set()
for ix in range(gw): edge.add(lbl[0,ix]); edge.add(lbl[gh-1,ix])
for iy in range(gh): edge.add(lbl[iy,0]); edge.add(lbl[iy,gw-1])
forest = free & (~np.isin(lbl,list(edge)))   # inside the green loops = FOREST (trees)
mtn    = free & np.isin(lbl,list(edge))       # between / edge = MOUNTAINS (rock + steam)
clearm = ((xg>minx+250)&(xg<maxx-250)&(yg>miny+110)&(yg<maxy-110)) & (~((xg>maxx-620)&(yg<miny+620)))
mtn &= clearm; forest &= clearm               # keep frame/side-doodles/compass clear

# ---- 1) MOUNTAIN interior: sparse rock hatch + steam puffs ----
random.seed(4)
mi=np.argwhere(mtn & (~path))
for iy in range(0,gh,3):
    ix=0
    while ix<gw:
        if mtn[iy,ix] and not path[iy,ix]:
            j=ix
            while j<gw and mtn[iy,j]: j+=1
            xx=minx+ix*CELL
            while xx<minx+j*CELL:
                if random.random()<0.5: emit(xx,miny+iy*CELL,xx+CELL*1.3,miny+iy*CELL+CELL*1.3, ROCK if random.random()<0.6 else ROCK_D)
                xx+=CELL*2.2
            ix=j
        else: ix+=1
# steam puffs rising from scattered mountain points
for _ in range(120):
    iy,ix=mi[random.randrange(len(mi))]; cx=minx+ix*CELL; cy=miny+iy*CELL
    for k in range(3):
        yy=cy-k*16; w=6+k*3
        emit(cx-w,yy,cx-w*0.3,yy-8,STEAM); emit(cx-w*0.3,yy-8,cx+w*0.3,yy-4,STEAM); emit(cx+w*0.3,yy-4,cx+w,yy-10,STEAM)

# ---- 2) FOREST floor: green tree scatter (canopy) ----
def tree(cx,cy,s,seed):
    r=random.Random(seed); rr=s*(0.5+0.3*r.random())
    pts=[]
    import math as m
    for a in range(8):
        ang=a/8*2*m.pi; rad=rr*(0.8+0.25*r.random())
        pts.append((cx+m.cos(ang)*rad, cy+m.sin(ang)*rad))
    for i in range(len(pts)):
        emit(pts[i][0],pts[i][1],pts[(i+1)%len(pts)][0],pts[(i+1)%len(pts)][1], TREE if seed%3 else TREE_D)
    emit(cx,cy+rr*0.7,cx,cy+rr*1.15,TREE_D)   # trunk
random.seed(11); SP=185; placed=0; y=miny+30
while y<maxy-30:
    x=minx+30
    while x<maxx-30:
        jx=x+random.uniform(-60,60); jy=y+random.uniform(-60,60); ix,iy=gx(jx),gy(jy)
        if 0<=ix<gw and 0<=iy<gh and forest[iy,ix] and not path[iy,ix] and (jx>minx+250 and jx<maxx-250 and jy>miny+110 and jy<maxy-110 and not (jx>maxx-620 and jy<miny+620)):
            tree(jx,jy,random.uniform(26,42),placed); placed+=1
        x+=SP
    y+=SP

# ---- 3) geometry ON TOP: green ridge lines -> rock; keep tan paths ----
for x1,y1,z1,x2,y2,z2,c in B:
    if c in ((0,150,0),(0,125,0)): nc=RIDGE
    elif c==(150,100,0): nc=PATH
    elif c==(0,0,0): nc=(70,64,56)
    else: nc=c
    out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z1,x2,y2,z2,nc[0],nc[1],nc[2]))

# (windmills are a MARGIN sketch in _2, not on-map icons)
open('steamfont_colored.txt','w',newline='').write('\r\n'.join(out)+'\r\n')
print('trees=%d  mountains hatched  L=%d'%(placed,len(out)))
