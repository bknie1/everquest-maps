"""Felwithe style pass (high-elf marble/water/grass) via unified flat classification.
Parameterized per zone. Buildings->cream marble, water channels->blue, courtyards+outer->grass,
gold trim kept. Checkered entrance kept dark."""
import sys, numpy as np, math, random
from scipy.ndimage import binary_dilation, binary_fill_holes, label as _label
ZONE=sys.argv[1]
def parse(path):
    out=[]
    for l in open(path,encoding='utf-8',errors='replace'):
        l=l.strip()
        if l.startswith('L'):
            f=l[2:].split(','); out.append((float(f[0]),float(f[1]),float(f[2]),float(f[3]),float(f[4]),float(f[5]),(int(f[6]),int(f[7]),int(f[8]))))
    return out
B=parse(f'{ZONE}.txt')
xs=[v for s in B for v in (s[0],s[3])]; ys=[v for s in B for v in (s[1],s[4])]
minx,maxx,miny,maxy=min(xs),max(xs),min(ys),max(ys)
MARBLE=(208,200,176); MARBLE_W=(150,145,125); TEAL=(120,175,165); GOLD=(198,168,86)
WFILL=(150,196,224); WFILL2=(128,180,214); WOUT=(70,140,196)
GRASS=(126,168,98); GRASS2=(108,150,82); TREE=(60,116,64)
z0=-1.0; out=[]
def emit(x1,y1,x2,y2,c): out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z0,x2,y2,z0,c[0],c[1],c[2]))
CELL=7.0; gw=int((maxx-minx)/CELL)+2; gh=int((maxy-miny)/CELL)+2
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
black=raster(lambda c:c==(0,0,0)); blue=raster(lambda c:c==(0,0,255))
# footprint of the whole city (fill-holes of dilated geometry)
allgeo=black|blue
foot=binary_fill_holes(binary_dilation(allgeo,iterations=6))
water=binary_fill_holes(binary_dilation(blue,iterations=2)) & (~binary_dilation(black,iterations=1))
marble=foot & (~water)                               # whole city interior = marble floor
outer=(~foot)                                        # Faydark forest edge
def fillmask(mask,c1,c2):
    for iy in range(gh):
        ix=0
        while ix<gw:
            if mask[iy,ix]:
                j=ix
                while j<gw and mask[iy,j]: j+=1
                emit(minx+ix*CELL,miny+iy*CELL,minx+j*CELL,miny+iy*CELL, c1 if iy%2 else c2); ix=j
            else: ix+=1
fillmask(marble, MARBLE, MARBLE)
fillmask(water, WFILL, WFILL2)
# outer forest: light grass hatch + sparse trees
random.seed(5)
ii=np.argwhere(outer)
for k in range(0,len(ii),9):
    iy,ix=ii[k]
    if iy%2==0: emit(minx+ix*CELL,miny+iy*CELL,minx+ix*CELL+CELL*1.3,miny+iy*CELL, GRASS2)
def tree(cx,cy,s,seed):
    r=random.Random(seed); rr=s*(0.6); 
    pts=[(cx+math.cos(a/6*2*math.pi)*rr,cy+math.sin(a/6*2*math.pi)*rr) for a in range(6)]
    for i in range(6): emit(pts[i][0],pts[i][1],pts[(i+1)%6][0],pts[(i+1)%6][1],TREE)
random.seed(9); pl=0
for k in range(0,len(ii),140):
    iy,ix=ii[k]; tree(minx+ix*CELL,miny+iy*CELL,random.uniform(20,32),pl); pl+=1
# geometry on top
for x1,y1,z1,x2,y2,z2,c in B:
    if   c==(0,0,255): nc=WOUT
    elif c==(255,215,0): nc=GOLD
    elif c==(0,0,0): nc=MARBLE_W
    elif c==(150,0,200): nc=c   # keep zone-line purple markers if any in base
    else: nc=c
    out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z1,x2,y2,z2,nc[0],nc[1],nc[2]))
open(f'{ZONE}_colored.txt','w',newline='').write('\r\n'.join(out)+'\r\n')
print('%s: marble=%d water=%d L=%d'%(ZONE,int(marble.sum()),int(water.sum()),len(out)))
