"""Splitpaw Lair — gnoll den cave (Blackburrow 2.0). Shade the SURROUNDING ROCK (brown, graded
by depth) so the walkable tunnels stay clear/visible; shade the river but knock out paths
that traverse it."""
import numpy as np, math, random
from scipy.ndimage import binary_dilation, binary_fill_holes, binary_erosion, binary_closing, distance_transform_edt
def parse(path):
    out=[]
    for l in open(path,encoding='utf-8',errors='replace'):
        l=l.strip()
        if l.startswith('L'):
            f=l[2:].split(','); out.append((float(f[0]),float(f[1]),float(f[2]),float(f[3]),float(f[4]),float(f[5]),(int(f[6]),int(f[7]),int(f[8]))))
    return out
B=parse('paw.txt')
xs=[v for s in B for v in (s[0],s[3])]; ys=[v for s in B for v in (s[1],s[4])]
minx,maxx,miny,maxy=min(xs),max(xs),min(ys),max(ys)
zs=[(s[2]+s[5])/2 for s in B]; zlo,zhi=np.percentile(zs,8),np.percentile(zs,92); zc1=zlo+(zhi-zlo)*0.38; zc2=zlo+(zhi-zlo)*0.68
R1=(150,120,72); R2=(132,100,58); R3=(112,96,110)   # rock shades: warm dirt (high) -> ochre -> cool slate (deep)
WFILL=(70,150,205); WFILL2=(88,166,216); WEDGE=(34,84,150); WRIP=(140,190,225)
ROCKLN=(150,132,110); ROCKD=(110,96,80); DIRT=(150,120,70)
z0=-1.0; out=[]
def emit(x1,y1,x2,y2,c): out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z0,x2,y2,z0,c[0],c[1],c[2]))
CELL=5.0; gw=int((maxx-minx)/CELL)+2; gh=int((maxy-miny)/CELL)+2
gx=lambda x:int((x-minx)/CELL); gy=lambda y:int((y-miny)/CELL)
def raster(cond,dil=0):
    m=np.zeros((gh,gw),bool)
    for s in B:
        if cond(s):
            x1,y1,x2,y2=s[0],s[1],s[3],s[4]; n=int(max(abs(x2-x1),abs(y2-y1))/CELL)+1
            for i in range(n+1):
                t=i/n; ix=gx(x1+(x2-x1)*t); iy=gy(y1+(y2-y1)*t)
                if 0<=ix<gw and 0<=iy<gh: m[iy,ix]=True
    return binary_dilation(m,iterations=dil) if dil else m
walls=raster(lambda s:True); blue=raster(lambda s:s[6]==(0,0,255))
wfat=binary_dilation(walls,iterations=1)
walkable=binary_fill_holes(wfat)              # tunnels+rooms interior (+walls)
hull=binary_fill_holes(binary_dilation(walls,iterations=9))
rock=hull & (~walkable)                        # SOLID ROCK around the tunnels -> shade this
# depth grid (nearest geometry z per cell) for grading the rock
zgrid=np.full((gh,gw),np.nan)
for s in B:
    x1,y1,x2,y2=s[0],s[1],s[3],s[4]; zz=(s[2]+s[5])/2; n=int(max(abs(x2-x1),abs(y2-y1))/CELL)+1
    for i in range(n+1):
        t=i/n; ix=gx(x1+(x2-x1)*t); iy=gy(y1+(y2-y1)*t)
        if 0<=ix<gw and 0<=iy<gh: zgrid[iy,ix]=zz
idx=distance_transform_edt(np.isnan(zgrid),return_distances=False,return_indices=True); zgrid=zgrid[tuple(idx)]
water=binary_fill_holes(binary_closing(binary_dilation(blue,iterations=2),iterations=2)) & hull
wz = np.nanmedian([ (b[2]+b[5])/2 for b in B if b[6]==(0,0,255) ]) if blue.any() else 0
bridge = binary_fill_holes(wfat) & (zgrid > wz + 8)     # walkable surfaces well above water = bridges
water_shade = water & (~bridge)                          # shade river, knock out bridges only
xg=(np.arange(gw)*CELL+minx)[None,:]; yg=(np.arange(gh)*CELL+miny)[:,None]
PAD=int(max(maxx-minx,maxy-miny)*0.04); inb=(xg>minx+PAD)&(xg<maxx-PAD)&(yg>miny+PAD)&(yg<maxy-PAD)
# shade the ROCK (hatch), graded by depth
for iy in range(gh):
    ix=0
    while ix<gw:
        if rock[iy,ix] and inb[iy,ix]:
            j=ix
            while j<gw and rock[iy,j] and inb[iy,j]: j+=1
            z=zgrid[iy,(ix+j)//2]; col=R3 if z<zc1 else (R2 if z<zc2 else R1)
            emit(minx+ix*CELL,miny+iy*CELL,minx+j*CELL,miny+iy*CELL, col); ix=j
        else: ix+=1
# water (minus paths), edge, ripples
for iy in range(gh):
    ix=0
    while ix<gw:
        if water_shade[iy,ix] and inb[iy,ix]:
            j=ix
            while j<gw and water_shade[iy,j]: j+=1
            emit(minx+ix*CELL,miny+iy*CELL,minx+j*CELL,miny+iy*CELL, WFILL if iy%2 else WFILL2); ix=j
        else: ix+=1
edge=water_shade & (~binary_erosion(water_shade,iterations=1))
for iy,ix in np.argwhere(edge):
    if inb[iy,ix]: emit(minx+ix*CELL,miny+iy*CELL,minx+ix*CELL+CELL,miny+iy*CELL, WEDGE)
# geometry recolor
for x1,y1,z1,x2,y2,z2,c in B:
    if   c==(0,0,255): nc=WEDGE
    elif c==(160,120,60): nc=DIRT
    elif c==(128,128,128): nc=ROCKLN
    elif c==(0,0,0): nc=ROCKD
    else: nc=c
    out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z1,x2,y2,z2,nc[0],nc[1],nc[2]))
open('paw_colored.txt','w',newline='').write('\r\n'.join(out)+'\r\n')
print('splitpaw INVERSE: rock=%d walkable=%d water=%d L=%d'%(int(rock.sum()),int(walkable.sum()),int(water_shade.sum()),len(out)))
