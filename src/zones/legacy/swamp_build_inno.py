"""Innothule Swamp — CORRECTED: water is the connected BACKGROUND (muddy blue-green),
green contour blobs are vegetation ISLANDS (land) with trees. Knockout buffer keeps trees
on the islands, off the open water. Base: innothule.txt."""
import numpy as np, math, random
from scipy.ndimage import binary_dilation, binary_fill_holes, label as _label
def parse(path):
    out=[]
    for l in open(path,encoding='utf-8',errors='replace'):
        l=l.strip()
        if l.startswith('L'):
            f=l[2:].split(','); out.append((float(f[0]),float(f[1]),float(f[2]),float(f[3]),float(f[4]),float(f[5]),(int(f[6]),int(f[7]),int(f[8]))))
    return out
B=parse('innothule.txt')
xs=[v for s in B for v in (s[0],s[3])]; ys=[v for s in B for v in (s[1],s[4])]
minx,maxx,miny,maxy=min(xs),max(xs),min(ys),max(ys)
WATER=(104,140,124); WATER2=(120,156,138); ISLE=(120,152,84); ISLE2=(104,136,70); VEG=(92,132,66); TREE=(70,100,54); VINE=(84,112,64); MUD=(132,122,92)
z0=-1.0; out=[]
def emit(x1,y1,x2,y2,c): out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z0,x2,y2,z0,c[0],c[1],c[2]))
CELL=14.0; gw=int((maxx-minx)/CELL)+2; gh=int((maxy-miny)/CELL)+2
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
black=raster(lambda c:c==(0,0,0)); green=raster(lambda c:c==(85,184,20)); gray=raster(lambda c:c==(128,128,128))
interior=binary_fill_holes(binary_dilation(black,iterations=2))
if interior.sum()<gw*gh*0.3: interior=np.ones((gh,gw),bool)
greend=binary_dilation(green,iterations=1)
notg=interior & (~greend)
lab,n=_label(notg)
sizes=np.array([(lab==k).sum() for k in range(1,n+1)])
water_lab=1+int(np.argmax(sizes)) if n else 0
WATERM=(lab==water_lab)                       # connected background = WATER
islands=interior & (~WATERM)                  # everything else (green rings + enclosed) = LAND/veg
xg=(np.arange(gw)*CELL+minx)[None,:]; yg=(np.arange(gh)*CELL+miny)[:,None]
PAD=170; inb=(xg>minx+PAD)&(xg<maxx-PAD)&(yg>miny+PAD)&(yg<maxy-PAD)
def fillmask(mask,c1,c2,everyrow=True):
    for iy in range(0,gh,1 if everyrow else 2):
        ix=0
        while ix<gw:
            if mask[iy,ix] and inb[iy,ix]:
                j=ix
                while j<gw and mask[iy,j]: j+=1
                emit(minx+ix*CELL,miny+iy*CELL,minx+j*CELL,miny+iy*CELL, c1 if iy%2 else c2); ix=j
            else: ix+=1
# WATER = dominant muddy blue-green background (dense ripples)
fillmask(WATERM, WATER, WATER2, everyrow=True)
# ISLANDS = green land (lighter hatch)
fillmask(islands & inb, ISLE, ISLE2, everyrow=False)
# viney swamp trees — ON THE ISLANDS ONLY (knockout keeps them off open water)
def swtree(cx,cy,s,seed):
    r=random.Random(seed); n=7
    pts=[(cx+math.cos(a/n*2*math.pi)*s*r.uniform(.8,1.15), cy+math.sin(a/n*2*math.pi)*s*r.uniform(.8,1.15)) for a in range(n)]
    for i in range(n): emit(pts[i][0],pts[i][1],pts[(i+1)%n][0],pts[(i+1)%n][1],TREE)
    for _ in range(2):
        vx=cx+r.uniform(-s*.6,s*.6); emit(vx,cy+s*.5,vx,cy+s*.5+r.uniform(s*.7,s*1.3),VINE)
random.seed(11); pl=0
tree_zone=islands & inb                        # trees only on land islands
ii=np.argwhere(tree_zone)
for k in range(0,len(ii),22):
    iy,ix=ii[k]
    if random.random()<0.9:
        swtree(minx+ix*CELL,miny+iy*CELL, random.uniform(18,30), pl); pl+=1
# geometry recolor
for x1,y1,z1,x2,y2,z2,c in B:
    if   c==(85,184,20): nc=VEG
    elif c==(128,128,128): nc=MUD
    elif c==(0,0,0): nc=(90,84,70)
    else: nc=c
    out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z1,x2,y2,z2,nc[0],nc[1],nc[2]))
open('innothule_colored.txt','w',newline='').write('\r\n'.join(out)+'\r\n')
print('innothule: WATER=%d islands=%d trees=%d L=%d'%(int(WATERM.sum()),int(islands.sum()),pl,len(out)))
