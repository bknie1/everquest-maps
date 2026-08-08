"""Ocean of Tears base: ocean flood-filled blue, islands carved out as green (Faydwer-style
grass + trees) with sandy edges, structures kept."""
import numpy as np, math, random
from scipy.ndimage import binary_dilation, label as _label
def parse(path):
    out=[]
    for l in open(path,encoding='utf-8',errors='replace'):
        l=l.strip()
        if l.startswith('L'):
            f=l[2:].split(','); out.append((float(f[0]),float(f[1]),float(f[2]),float(f[3]),float(f[4]),float(f[5]),(int(f[6]),int(f[7]),int(f[8]))))
    return out
B=parse('oot.txt')
minx,maxx,miny,maxy=-11148,10983,-3495,5374
OCEAN=(150,196,224); OCEAN2=(128,180,214); WOUT=(70,140,196)
GRASS=(96,150,84); GRASS2=(78,132,66); TREE=(52,104,56); TREE_D=(38,84,42); SAND=(210,196,150); STONE=(120,112,100)
z0=0.0; out=[]
def emit(x1,y1,x2,y2,c): out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z0,x2,y2,z0,c[0],c[1],c[2]))
CELL=26.0; gw=int((maxx-minx)/CELL)+2; gh=int((maxy-miny)/CELL)+2
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
coast=raster(lambda c:c==(0,0,255),dil=2); black=raster(lambda c:c==(0,0,0),dil=1)
lbl,n=_label(~(coast|black))
sizes=np.bincount(lbl.ravel()); sizes[0]=0
ocean=(lbl==sizes.argmax())                # largest free region = open ocean
island=(lbl>0)&(~ocean)&(~coast)           # all enclosed regions = islands
# guard: islands should be a small fraction
gridarea=gw*gh
# 1) ocean hatch
for iy in range(gh):
    ix=0
    while ix<gw:
        if ocean[iy,ix]:
            j=ix
            while j<gw and ocean[iy,j]: j+=1
            if iy%2==0: emit(minx+ix*CELL,miny+iy*CELL,minx+j*CELL,miny+iy*CELL, OCEAN if (iy//2)%2 else OCEAN2)
            ix=j
        else: ix+=1
# 2) island grass fill
for iy in range(gh):
    ix=0
    while ix<gw:
        if island[iy,ix]:
            j=ix
            while j<gw and island[iy,j]: j+=1
            emit(minx+ix*CELL,miny+iy*CELL,minx+j*CELL,miny+iy*CELL, GRASS if iy%2 else GRASS2); ix=j
        else: ix+=1
# 3) trees scattered on islands (Faydwer forest); avoid coast edge + structures
edge=binary_dilation(coast,iterations=2)|binary_dilation(black,iterations=1)
def tree(cx,cy,s,seed):
    r=random.Random(seed); rr=s*(0.5+0.3*r.random()); pts=[]
    for a in range(7):
        ang=a/7*2*math.pi; rad=rr*(0.8+0.2*r.random()); pts.append((cx+math.cos(ang)*rad,cy+math.sin(ang)*rad))
    for i in range(len(pts)): emit(pts[i][0],pts[i][1],pts[(i+1)%len(pts)][0],pts[(i+1)%len(pts)][1], TREE if seed%3 else TREE_D)
    emit(cx,cy+rr*0.7,cx,cy+rr*1.1,TREE_D)
random.seed(7); ii=np.argwhere(island & (~edge)); placed=0
if len(ii):
    step=max(1,len(ii)//220)
    for k in range(0,len(ii),step):
        iy,ix=ii[k]; tree(minx+ix*CELL+random.uniform(-10,10),miny+iy*CELL+random.uniform(-10,10),random.uniform(46,80),placed); placed+=1
# 4) geometry on top
for x1,y1,z1,x2,y2,z2,c in B:
    if   c==(0,0,255): nc=WOUT
    elif c==(128,128,128): nc=(150,120,84)   # island hills -> tan rock
    elif c==(100,50,0): nc=(150,110,64)       # docks/paths -> wood
    elif c==(0,0,0): nc=STONE
    else: nc=c
    out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z1,x2,y2,z2,nc[0],nc[1],nc[2]))
open('oot_colored.txt','w',newline='').write('\r\n'.join(out)+'\r\n')
print('ocean=%d island=%d trees=%d L=%d'%(int(ocean.sum()),int(island.sum()),placed,len(out)))
