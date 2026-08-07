"""The Feerrott — dense dark jungle. RIVER = the green bank lines (starts north, forks into
two going south); channel filled blue via morphological closing, with canopy KNOCKOUT buffer
around the water + bridges. Buildings (Oggok, Cazic-Thule) get tree knockout. Brown = trail."""
import numpy as np, math, random
from scipy.ndimage import binary_dilation, binary_fill_holes, binary_closing, binary_erosion, uniform_filter, label as _label
def parse(path):
    out=[]
    for l in open(path,encoding='utf-8',errors='replace'):
        l=l.strip()
        if l.startswith('L'):
            f=l[2:].split(','); out.append((float(f[0]),float(f[1]),float(f[2]),float(f[3]),float(f[4]),float(f[5]),(int(f[6]),int(f[7]),int(f[8]))))
    return out
B=parse('feerrott.txt')
xs=[v for s in B for v in (s[0],s[3])]; ys=[v for s in B for v in (s[1],s[4])]
minx,maxx,miny,maxy=min(xs),max(xs),min(ys),max(ys)
CAN=(56,86,44); CAN2=(44,72,36); CAN3=(66,98,52); TREE=(38,62,32); TREE2=(50,78,42)
RWATER=(112,162,198); RWATER2=(128,176,208); REDGE=(60,108,150); TRAIL=(154,126,74); STONE=(120,116,104)
z0=-1.0; out=[]
def emit(x1,y1,x2,y2,c): out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z0,x2,y2,z0,c[0],c[1],c[2]))
CELL=13.0; gw=int((maxx-minx)/CELL)+2; gh=int((maxy-miny)/CELL)+2
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
black=raster(lambda c:c==(0,0,0)); brown=raster(lambda c:c==(160,120,60)); green=raster(lambda c:c==(85,184,20))
interior=binary_fill_holes(binary_dilation(black,iterations=3))
if interior.sum()<gw*gh*0.25: interior=np.ones((gh,gw),bool)
# RIVER = channel between the green banks (close to fill the gap), Y-shape north->two south
river_core=binary_closing(green,iterations=13) & interior
river_core=binary_dilation(river_core,iterations=1)
river_knock=binary_dilation(river_core,iterations=3)
# BUILDINGS = dense black clusters -> tree knockout (Kelethin-style)
dens=uniform_filter(black.astype(float),size=7); building=dens>0.33
building_knock=binary_dilation(building,iterations=8)
trail_knock=binary_dilation(brown,iterations=3)             # KNOCKOUT along the trail/path
xg=(np.arange(gw)*CELL+minx)[None,:]; yg=(np.arange(gh)*CELL+miny)[:,None]
PAD=230; inb=(xg>minx+PAD)&(xg<maxx-PAD)&(yg>miny+PAD)&(yg<maxy-PAD)
canopy=interior & inb & (~river_knock) & (~building_knock) & (~trail_knock)
# BRIDGES: grey stone decks where structures cross the river -> carve out of the water
STONE_L=(170,167,160); STONE_D=(126,123,116)
bnr=black & binary_dilation(river_core,iterations=4)                    # bridge outlines on/over the river
bridge=binary_fill_holes(binary_dilation(bnr,iterations=2))            # fill the deck from the outline
bridge=binary_dilation(bridge,iterations=1) & interior
water=river_core & (~bridge)
# 0) RIVER fill (blue, EXCLUDING the bridge decks) + darker edge
for iy in range(gh):
    ix=0
    while ix<gw:
        if water[iy,ix]:
            j=ix
            while j<gw and water[iy,j]: j+=1
            emit(minx+ix*CELL,miny+iy*CELL,minx+j*CELL,miny+iy*CELL, RWATER if iy%2 else RWATER2); ix=j
        else: ix+=1
edge=water & (~binary_erosion(water,iterations=1))
for iy,ix in np.argwhere(edge): emit(minx+ix*CELL,miny+iy*CELL,minx+ix*CELL+CELL,miny+iy*CELL, REDGE)
# (stone bridge drawn LAST, after geometry, so nothing paints over it)
# 1) dense dark canopy hatch (diagonal)
random.seed(2)
for iy in range(0,gh,2):
    ix=0
    while ix<gw:
        if canopy[iy,ix]:
            j=ix
            while j<gw and canopy[iy,j]: j+=1
            xx=minx+ix*CELL
            while xx<minx+j*CELL:
                if random.random()<0.5:
                    Ln=CELL*random.uniform(1.4,2.6); emit(xx,miny+iy*CELL,xx+Ln,miny+iy*CELL+Ln, CAN2 if random.random()<0.5 else CAN)
                xx+=CELL*random.uniform(1.5,2.3)
            ix=j
        else: ix+=1
# 2) dense overlapping tree canopies
def jtree(cx,cy,s,seed):
    r=random.Random(seed); n=6
    pts=[(cx+math.cos(a/n*2*math.pi)*s*r.uniform(.75,1.2), cy+math.sin(a/n*2*math.pi)*s*r.uniform(.75,1.2)) for a in range(n)]
    for i in range(n): emit(pts[i][0],pts[i][1],pts[(i+1)%n][0],pts[(i+1)%n][1],TREE if seed%2 else TREE2)
    emit(cx,cy,cx,cy+s*0.5,TREE)
ii=np.argwhere(canopy); random.seed(7); pl=0
for k in range(0,len(ii),19):
    iy,ix=ii[k]; jtree(minx+ix*CELL+random.uniform(-6,6),miny+iy*CELL+random.uniform(-6,6),random.uniform(22,40),pl); pl+=1
# geometry recolor: green->river edge(blue), brown->trail, black->structures
for x1,y1,z1,x2,y2,z2,c in B:
    if   c==(85,184,20): nc=REDGE       # green banks = river edge
    elif c==(160,120,60): nc=TRAIL      # brown = trail
    elif c==(128,128,128): nc=STONE
    elif c==(0,0,0): nc=(70,80,58)
    else: nc=c
    out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z1,x2,y2,z2,nc[0],nc[1],nc[2]))
from scipy.ndimage import binary_erosion as _ero
bedge=bridge & (~_ero(bridge,iterations=1))
for iy in range(gh):
    ix=0
    while ix<gw:
        if bridge[iy,ix]:
            j=ix
            while j<gw and bridge[iy,j]: j+=1
            emit(minx+ix*CELL,miny+iy*CELL,minx+j*CELL,miny+iy*CELL, STONE_L if iy%2 else STONE_D)
            for xx in range(ix,j,3): emit(minx+xx*CELL,miny+iy*CELL,minx+xx*CELL,miny+(iy+1)*CELL, STONE_D)
            ix=j
        else: ix+=1
for iy,ix in np.argwhere(bedge): emit(minx+ix*CELL,miny+iy*CELL,minx+ix*CELL+CELL,miny+iy*CELL, (72,70,64))
open('feerrott_colored.txt','w',newline='').write('\r\n'.join(out)+'\r\n')
print('feerrott: river=%d canopy=%d trees=%d L=%d'%(int(river_core.sum()),int(canopy.sum()),pl,len(out)))
