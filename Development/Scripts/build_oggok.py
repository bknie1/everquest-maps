"""Oggok — crumbled Roman ogre ruins. Sandstone floors, the coliseum, bronze ruins accents,
jungle creeping in at the edges (connected to Feerrott) but the city core is stone. No water."""
import numpy as np, math, random
from scipy.ndimage import binary_dilation, binary_fill_holes, binary_erosion, label as _label
def parse(path):
    out=[]
    for l in open(path,encoding='utf-8',errors='replace'):
        l=l.strip()
        if l.startswith('L'):
            f=l[2:].split(','); out.append((float(f[0]),float(f[1]),float(f[2]),float(f[3]),float(f[4]),float(f[5]),(int(f[6]),int(f[7]),int(f[8]))))
    return out
B=parse('oggok.txt')
xs=[v for s in B for v in (s[0],s[3])]; ys=[v for s in B for v in (s[1],s[4])]
minx,maxx,miny,maxy=min(xs),max(xs),min(ys),max(ys)
SAND=(214,198,158); SAND2=(202,186,146); WALL=(150,138,110); BRONZE=(176,146,74); JUNGLE=(96,132,70); TREE=(66,102,54); DIRT=(150,126,88)
z0=-1.0; out=[]
def emit(x1,y1,x2,y2,c): out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z0,x2,y2,z0,c[0],c[1],c[2]))
CELL=8.0; gw=int((maxx-minx)/CELL)+2; gh=int((maxy-miny)/CELL)+2
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
black=raster(lambda c:c==(0,0,0)); gold=raster(lambda c:c==(255,215,0)); green=raster(lambda c:c==(85,184,20))
struct=black|gold
foot=binary_fill_holes(binary_dilation(struct,iterations=6))
marble=foot
outer=(~foot)
xg=(np.arange(gw)*CELL+minx)[None,:]; yg=(np.arange(gh)*CELL+miny)[:,None]
PAD=120; inb=(xg>minx+PAD)&(xg<maxx-PAD)&(yg>miny+PAD)&(yg<maxy-PAD)
def fillmask(mask,c1,c2):
    for iy in range(gh):
        ix=0
        while ix<gw:
            if mask[iy,ix] and inb[iy,ix]:
                j=ix
                while j<gw and mask[iy,j]: j+=1
                emit(minx+ix*CELL,miny+iy*CELL,minx+j*CELL,miny+iy*CELL, c1 if iy%2 else c2); ix=j
            else: ix+=1
fillmask(marble, SAND, SAND2)
# jungle creeping at the edges: sparse grass hatch + trees
random.seed(3); ii=np.argwhere(outer & inb)
for k in range(0,len(ii),7):
    iy,ix=ii[k]
    if iy%2==0 and random.random()<0.6: emit(minx+ix*CELL,miny+iy*CELL,minx+ix*CELL+CELL*1.3,miny+iy*CELL,JUNGLE)
def tree(cx,cy,s,seed):
    r=random.Random(seed); n=6
    pts=[(cx+math.cos(a/n*2*math.pi)*s*r.uniform(.7,1.1),cy+math.sin(a/n*2*math.pi)*s*r.uniform(.7,1.1)) for a in range(n)]
    for i in range(n): emit(pts[i][0],pts[i][1],pts[(i+1)%n][0],pts[(i+1)%n][1],TREE)
random.seed(9); pl=0
for k in range(0,len(ii),60):
    iy,ix=ii[k]; tree(minx+ix*CELL,miny+iy*CELL,random.uniform(14,24),pl); pl+=1
# broken columns (ruins) scattered in the marble core: small dashes
random.seed(5); mm=np.argwhere(marble & inb)
for k in range(0,len(mm),240):
    iy,ix=mm[k]; cx,cy=minx+ix*CELL,miny+iy*CELL
    emit(cx-6,cy,cx+6,cy,BRONZE); emit(cx,cy-6,cx,cy+6,BRONZE)   # broken column stub
# geometry recolor: gold->bronze ruins, green->jungle, black->sandstone wall
for x1,y1,z1,x2,y2,z2,c in B:
    if   c==(255,215,0): nc=BRONZE
    elif c==(85,184,20): nc=JUNGLE
    elif c==(160,120,60): nc=DIRT
    elif c==(0,0,0): nc=WALL
    else: nc=c
    out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z1,x2,y2,z2,nc[0],nc[1],nc[2]))
open('oggok_colored.txt','w',newline='').write('\r\n'.join(out)+'\r\n')
print('oggok: marble=%d L=%d'%(int(marble.sum()),len(out)))
