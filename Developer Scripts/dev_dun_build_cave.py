"""Generic cave/dungeon styler — INVERSE shading (shade surrounding rock, keep tunnels clear),
shaded water with bridges knocked out. Themes: ice / jungle / swamp."""
import sys, numpy as np, random
from scipy.ndimage import binary_dilation, binary_fill_holes, binary_erosion, binary_closing, distance_transform_edt
ZONE,THEME=sys.argv[1],sys.argv[2]
PAL={
 'ice':   dict(R1=(150,176,196),R2=(124,150,174),R3=(100,126,156),WALL=(120,140,162),WALLN=(88,108,134),
               ACC=(198,220,236),WFILL=(150,200,225),WFILL2=(168,212,232),WEDGE=(96,150,190),DIRT=(150,150,150)),
 'jungle':dict(R1=(122,120,78),R2=(98,104,62),R3=(78,88,52),WALL=(84,80,58),WALLN=(58,58,42),
               ACC=(150,140,70),WFILL=(78,120,86),WFILL2=(92,134,98),WEDGE=(46,84,56),DIRT=(120,96,54),GREEN=(96,150,60)),
 'swamp': dict(R1=(122,110,74),R2=(100,92,60),R3=(84,80,54),WALL=(80,74,52),WALLN=(56,52,38),
               ACC=(150,132,80),WFILL=(96,122,84),WFILL2=(110,136,96),WEDGE=(58,84,58),DIRT=(120,100,60)),
}[THEME]
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
zs=[(s[2]+s[5])/2 for s in B]; zlo,zhi=np.percentile(zs,8),np.percentile(zs,92); zc1=zlo+(zhi-zlo)*.38; zc2=zlo+(zhi-zlo)*.68
z0=-1.0; out=[]
def emit(x1,y1,x2,y2,c): out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z0,x2,y2,z0,c[0],c[1],c[2]))
span=max(maxx-minx,maxy-miny); CELL=span/300.0
gw=int((maxx-minx)/CELL)+2; gh=int((maxy-miny)/CELL)+2
gx=lambda x:int((x-minx)/CELL); gy=lambda y:int((y-miny)/CELL)
def raster(cond):
    m=np.zeros((gh,gw),bool)
    for s in B:
        if cond(s):
            x1,y1,x2,y2=s[0],s[1],s[3],s[4]; n=int(max(abs(x2-x1),abs(y2-y1))/CELL)+1
            for i in range(n+1):
                t=i/n; ix=gx(x1+(x2-x1)*t); iy=gy(y1+(y2-y1)*t)
                if 0<=ix<gw and 0<=iy<gh: m[iy,ix]=True
    return m
walls=raster(lambda s:True); blue=raster(lambda s:s[6]==(0,0,255))
wfat=binary_dilation(walls,iterations=1)
walkable=binary_fill_holes(wfat)
hull=binary_fill_holes(binary_dilation(walls,iterations=9))
rock=hull & (~walkable)
zgrid=np.full((gh,gw),np.nan)
for s in B:
    x1,y1,x2,y2=s[0],s[1],s[3],s[4]; zz=(s[2]+s[5])/2; n=int(max(abs(x2-x1),abs(y2-y1))/CELL)+1
    for i in range(n+1):
        t=i/n; ix=gx(x1+(x2-x1)*t); iy=gy(y1+(y2-y1)*t)
        if 0<=ix<gw and 0<=iy<gh: zgrid[iy,ix]=zz
idx=distance_transform_edt(np.isnan(zgrid),return_distances=False,return_indices=True); zg=zgrid[tuple(idx)]
water=binary_fill_holes(binary_closing(binary_dilation(blue,iterations=2),iterations=2)) & hull
wz=np.nanmedian([(s[2]+s[5])/2 for s in B if s[6]==(0,0,255)]) if blue.any() else 0
bridge=walkable & (zg>wz+8); water_shade=water & (~bridge)
xg=(np.arange(gw)*CELL+minx)[None,:]; yg=(np.arange(gh)*CELL+miny)[:,None]
PAD=int(span*0.04); inb=(xg>minx+PAD)&(xg<maxx-PAD)&(yg>miny+PAD)&(yg<maxy-PAD)
R1,R2,R3=PAL['R1'],PAL['R2'],PAL['R3']
for iy in range(gh):
    ix=0
    while ix<gw:
        if rock[iy,ix] and inb[iy,ix]:
            j=ix
            while j<gw and rock[iy,j] and inb[iy,j]: j+=1
            z=zg[iy,(ix+j)//2]; col=R3 if z<zc1 else (R2 if z<zc2 else R1)
            emit(minx+ix*CELL,miny+iy*CELL,minx+j*CELL,miny+iy*CELL,col); ix=j
        else: ix+=1
for iy in range(gh):
    ix=0
    while ix<gw:
        if water_shade[iy,ix] and inb[iy,ix]:
            j=ix
            while j<gw and water_shade[iy,j]: j+=1
            emit(minx+ix*CELL,miny+iy*CELL,minx+j*CELL,miny+iy*CELL, PAL['WFILL'] if iy%2 else PAL['WFILL2']); ix=j
        else: ix+=1
edge=water_shade & (~binary_erosion(water_shade,iterations=1))
for iy,ix in np.argwhere(edge):
    if inb[iy,ix]: emit(minx+ix*CELL,miny+iy*CELL,minx+ix*CELL+CELL,miny+iy*CELL, PAL['WEDGE'])
for x1,y1,z1,x2,y2,z2,c in B:
    if   c==(0,0,255): nc=PAL['WEDGE']
    elif c==(255,215,0): nc=PAL['ACC']
    elif c==(160,120,60) or c==(100,50,0): nc=PAL['DIRT']
    elif c==(128,128,128): nc=PAL['WALL']
    elif c==(85,184,20): nc=PAL.get('GREEN',PAL['WALL'])
    elif c==(0,0,0): nc=PAL['WALLN']
    else: nc=c
    out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z1,x2,y2,z2,nc[0],nc[1],nc[2]))
open(f'{ZONE}_colored.txt','w',newline='').write('\r\n'.join(out)+'\r\n')
print('%s(%s) rock=%d water=%d L=%d'%(ZONE,THEME,int(rock.sum()),int(water_shade.sum()),len(out)))
