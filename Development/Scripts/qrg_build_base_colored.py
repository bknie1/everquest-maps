"""Surefall Glade colored base: fill the jaggedpine tree-circles brown (redwood
trunk cross-sections with growth rings), keep water blue. Replaces qrg.txt."""
import numpy as np, math, json
def parse(path):
    out=[]
    for l in open(path,encoding='utf-8',errors='replace'):
        l=l.strip()
        if not l.startswith('L'): continue
        f=l[2:].split(','); out.append((float(f[0]),float(f[1]),float(f[2]),float(f[3]),float(f[4]),float(f[5]),(int(f[6]),int(f[7]),int(f[8]))))
    return out
B=parse('qrg.txt')

# ---- detect tree-circles (small closed black octagons) ----
black=[i for i,s in enumerate(B) if s[6]==(0,0,0)]
def key(x,y): return (round(x,1),round(y,1))
pts={}
for i in black:
    x1,y1,_,x2,y2,_,_=B[i]; pts.setdefault(key(x1,y1),[]).append(i); pts.setdefault(key(x2,y2),[]).append(i)
parent={i:i for i in black}
def f(a):
    while parent[a]!=a: parent[a]=parent[parent[a]];a=parent[a]
    return a
for k,idxs in pts.items():
    for j in idxs[1:]: parent[f(j)]=f(idxs[0])
from collections import defaultdict
comp=defaultdict(list)
for i in black: comp[f(i)].append(i)
tree_ids=set(); trees=[]
for cid,idxs in comp.items():
    xs=[v for i in idxs for v in (B[i][0],B[i][3])]; ys=[v for i in idxs for v in (B[i][1],B[i][4])]
    w=max(xs)-min(xs); h=max(ys)-min(ys); cx=(min(xs)+max(xs))/2; cy=(min(ys)+max(ys))/2
    if 5<=len(idxs)<=12 and 30<=w<=80 and 30<=h<=80 and 0.6<w/h<1.6:
        trees.append((cx,cy,(w+h)/4)); tree_ids|=set(idxs)   # r = avg radius
print("jaggedpines to fill: %d"%len(trees))

BARK=(122,74,28); RING=(150,108,52); CORE=(92,54,20); WATER=(40,95,200); WRIP=(120,175,225)
z0=3.0
out=[]
def emit(x1,y1,x2,y2,c,z=z0): out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z,x2,y2,z,c[0],c[1],c[2]))

# 1) copy geometry: recolor tree outlines to bark-brown, brighten water, keep rest
for i,s in enumerate(B):
    x1,y1,z1,x2,y2,z2,c=s
    if i in tree_ids: c=BARK
    elif c==(0,0,255): c=WATER
    out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z1,x2,y2,z2,c[0],c[1],c[2]))

# 2) fill each jaggedpine: concentric growth rings + heartwood
def octagon(cx,cy,r,c,z=z0):
    p=[(cx+r*math.cos(math.radians(a)),cy+r*math.sin(math.radians(a))) for a in range(0,360,45)]
    for i in range(8): emit(p[i][0],p[i][1],p[(i+1)%8][0],p[(i+1)%8][1],c,z)
for cx,cy,r in trees:
    octagon(cx,cy,r*0.74,RING); octagon(cx,cy,r*0.50,RING); octagon(cx,cy,r*0.28,CORE)
    emit(cx-2,cy,cx+2,cy,CORE); emit(cx,cy-2,cx,cy+2,CORE)      # heartwood dot

# 3) SHADE the water via FLOOD-FILL: fill only regions enclosed by the blue outline,
#    seeded from the blue-adjacent edge and flowing AROUND the hut (black walls exclude it)
WFILL=(74,140,212)
import numpy as np, random
from scipy.ndimage import binary_dilation, label as _label
minx=min(v for s2 in B for v in (s2[0],s2[3])); maxx=max(v for s2 in B for v in (s2[0],s2[3]))
miny=min(v for s2 in B for v in (s2[1],s2[4])); maxy=max(v for s2 in B for v in (s2[1],s2[4]))
CELL=6.0; gw=int((maxx-minx)/CELL)+2; gh=int((maxy-miny)/CELL)+2
gx=lambda x:int((x-minx)/CELL); gy=lambda y:int((y-miny)/CELL)
def raster(colcond,dil=1):
    m=np.zeros((gh,gw),bool)
    for s2 in B:
        if colcond(s2[6]):
            x1,y1,x2,y2=s2[0],s2[1],s2[3],s2[4]
            n=int(max(abs(x2-x1),abs(y2-y1))/CELL)+1
            for i in range(n+1):
                t=i/n; ix=gx(x1+(x2-x1)*t); iy=gy(y1+(y2-y1)*t)
                if 0<=ix<gw and 0<=iy<gh: m[iy,ix]=True
    return binary_dilation(m,iterations=dil) if dil else m
blue_bar=raster(lambda c:c==(0,0,255),dil=1)
black_bar=raster(lambda c:c in ((0,0,0),(64,64,64),(100,50,0)),dil=2)
# land = free space (of ~blue) touching the map edge; water_cand = enclosed by blue
freeb=~blue_bar; lblL,_=_label(freeb)
edgeL=set()
for ix in range(gw): edgeL.add(lblL[0,ix]); edgeL.add(lblL[gh-1,ix])
for iy in range(gh): edgeL.add(lblL[iy,0]); edgeL.add(lblL[iy,gw-1])
water_cand = freeb & (~np.isin(lblL,list(edgeL)))
# exclude the hut: keep only enclosed regions that touch the blue shore (hut interior touches only black)
free2 = water_cand & (~black_bar)
lblW,_=_label(free2)
blue_adj = binary_dilation(blue_bar,iterations=1) & free2
keep=set(int(v) for v in np.unique(lblW[blue_adj]) if v>0)
water = np.isin(lblW,list(keep))
# hatch the water
for iy in range(gh):
    ix=0
    while ix<gw:
        if water[iy,ix]:
            j=ix
            while j<gw and water[iy,j]: j+=1
            emit(minx+ix*CELL, miny+iy*CELL, minx+j*CELL, miny+iy*CELL, WFILL); ix=j
        else: ix+=1
random.seed(7); wi=np.argwhere(water)
if len(wi):
    for _ in range(22):
        iy,ix=wi[random.randrange(len(wi))]; rx=minx+ix*CELL; ry=miny+iy*CELL
        emit(rx-5,ry,rx-1,ry-2,WRIP); emit(rx-1,ry-2,rx+3,ry,WRIP)
print('water cells: %d'%int(water.sum()))

open('qrg_colored.txt','w',newline='').write('\r\n'.join(out)+'\r\n')
print('wrote qrg_colored.txt  L=%d'%len(out))
