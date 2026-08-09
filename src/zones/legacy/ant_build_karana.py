"""Karana plains styler — soft grassland, dirt roads, shaded river, and z-graded CLIFF/RAVINE
emphasis (slope shading on steep terrain) for the Eastern Plains gorge + Highpass cliffs."""
import sys, numpy as np, random
from scipy.ndimage import binary_dilation, binary_fill_holes, binary_erosion
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
GRASS=(120,150,86); GRASS2=(134,162,98); ROAD=(168,140,86); HILL=(150,120,70); ROCK=(140,124,104)
CONTOUR=(150,150,110); CLIFF=(120,96,74); CLIFFD=(96,74,56); SLOPE=(110,88,66)
WFILL=(90,160,210); WFILL2=(108,176,220); WEDGE=(40,92,158)
z0=-1.0; out=[]
def emit(x1,y1,x2,y2,c): out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z0,x2,y2,z0,c[0],c[1],c[2]))
span=max(maxx-minx,maxy-miny); CELL=span/260.0
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
allg=raster(lambda s:True); blue=raster(lambda s:s[6]==(0,0,255))
interior=binary_fill_holes(binary_dilation(allg,iterations=3))
water=binary_fill_holes(binary_dilation(blue,iterations=2)) & interior
# z grid for cliff grading
zgrid=np.full((gh,gw),np.nan)
for s in B:
    x1,y1,x2,y2=s[0],s[1],s[3],s[4]; zz=(s[2]+s[5])/2; n=int(max(abs(x2-x1),abs(y2-y1))/CELL)+1
    for i in range(n+1):
        t=i/n; ix=gx(x1+(x2-x1)*t); iy=gy(y1+(y2-y1)*t)
        if 0<=ix<gw and 0<=iy<gh: zgrid[iy,ix]=zz
from scipy.ndimage import distance_transform_edt
idx=distance_transform_edt(np.isnan(zgrid),return_distances=False,return_indices=True); zg=zgrid[tuple(idx)]
gyv,gxv=np.gradient(zg); slope=np.hypot(gyv,gxv)   # steepness -> cliffs
slo,shi=np.percentile(slope,60),np.percentile(slope,90)
xg=(np.arange(gw)*CELL+minx)[None,:]; yg=(np.arange(gh)*CELL+miny)[:,None]
PAD=int(span*0.04); inb=(xg>minx+PAD)&(xg<maxx-PAD)&(yg>miny+PAD)&(yg<maxy-PAD)
zlo,zhi=np.nanpercentile([ (s[2]+s[5])/2 for s in B],[10,90])
random.seed(7)
# grass tufts (sparse) + cliff shading (steep) on interior
for iy in range(0,gh,2):
    ix=0
    while ix<gw:
        if interior[iy,ix] and not water[iy,ix] and inb[iy,ix]:
            j=ix
            while j<gw and interior[iy,j] and not water[iy,j]: j+=1
            xx=minx+ix*CELL
            while xx<minx+j*CELL:
                cc=gx(xx); st=slope[iy,min(cc,gw-1)]; z=zg[iy,min(cc,gw-1)]
                if st>shi and random.random()<0.55:            # steep -> CLIFF hatch (dense)
                    Ln=CELL*random.uniform(1.4,2.4); col=CLIFFD if z<(zlo+zhi)/2 else CLIFF
                    emit(xx,miny+iy*CELL,xx+Ln,miny+iy*CELL+Ln*0.5,col); xx+=CELL*random.uniform(1.2,2.0)
                elif st>slo and random.random()<0.30:          # moderate slope marks
                    emit(xx,miny+iy*CELL,xx+CELL*1.2,miny+iy*CELL+CELL*0.6,SLOPE); xx+=CELL*random.uniform(3,5)
                elif random.random()<0.10:                     # sparse grass tuft
                    emit(xx,miny+iy*CELL,xx+CELL*0.5,miny+iy*CELL-CELL*0.7,GRASS if random.random()<.6 else GRASS2)
                    emit(xx+CELL*0.5,miny+iy*CELL,xx+CELL*0.5,miny+iy*CELL-CELL*0.6,GRASS)
                    xx+=CELL*random.uniform(4,7)
                else: xx+=CELL*random.uniform(2,4)
            ix=j
        else: ix+=1
# river fill + edge
for iy in range(gh):
    ix=0
    while ix<gw:
        if water[iy,ix] and inb[iy,ix]:
            j=ix
            while j<gw and water[iy,j]: j+=1
            emit(minx+ix*CELL,miny+iy*CELL,minx+j*CELL,miny+iy*CELL, WFILL if iy%2 else WFILL2); ix=j
        else: ix+=1
edge=water & (~binary_erosion(water,iterations=1))
for iy,ix in np.argwhere(edge):
    if inb[iy,ix]: emit(minx+ix*CELL,miny+iy*CELL,minx+ix*CELL+CELL,miny+iy*CELL, WEDGE)
# geometry recolor
for x1,y1,z1,x2,y2,z2,c in B:
    if   c==(0,0,255): nc=WEDGE
    elif c==(160,120,60): nc=ROAD
    elif c==(100,50,0): nc=HILL
    elif c==(128,128,128): nc=ROCK
    elif c==(0,0,0): nc=CONTOUR
    else: nc=c
    out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z1,x2,y2,z2,nc[0],nc[1],nc[2]))
open(f'{ZONE}_colored.txt','w',newline='').write('\r\n'.join(out)+'\r\n')
print('%s L=%d water=%d'%(ZONE,len(out),int(water.sum())))
