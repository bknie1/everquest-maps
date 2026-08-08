"""Qeynos/Freeport human cities — shade harbor/moat water, recolor to warm sandstone-stone."""
import sys, numpy as np
from scipy.ndimage import binary_dilation, binary_fill_holes, binary_erosion
Z=sys.argv[1]
def parse(path):
    out=[]
    for l in open(path,encoding='utf-8',errors='replace'):
        l=l.strip()
        if l.startswith('L'):
            f=l[2:].split(','); out.append((float(f[0]),float(f[1]),float(f[2]),float(f[3]),float(f[4]),float(f[5]),(int(f[6]),int(f[7]),int(f[8]))))
    return out
B=parse(f'{Z}.txt')
xs=[v for s in B for v in (s[0],s[3])]; ys=[v for s in B for v in (s[1],s[4])]
minx,maxx,miny,maxy=min(xs),max(xs),min(ys),max(ys)
WFILL=(90,150,205); WFILL2=(108,166,216); WEDGE=(40,86,150); WRIP=(150,195,225)
STONE=(150,146,132); DSTONE=(112,104,92); SAND=(178,150,104); ROOF=(176,140,80); GRASS=(112,140,84)
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
isblue=lambda c: c[2]>c[0]+35 and c[2]>c[1]+15
blue=raster(isblue)
allg=raster(lambda c:True)
hull=binary_fill_holes(binary_dilation(allg,iterations=6))
water=binary_fill_holes(binary_dilation(blue,iterations=2)) & hull
xg=(np.arange(gw)*CELL+minx)[None,:]; yg=(np.arange(gh)*CELL+miny)[:,None]
PAD=int(max(maxx-minx,maxy-miny)*0.04); inb=(xg>minx+PAD)&(xg<maxx-PAD)&(yg>miny+PAD)&(yg<maxy-PAD)
for iy in range(0,gh,2):
    ix=0
    while ix<gw:
        if water[iy,ix] and inb[iy,ix]:
            j=ix
            while j<gw and water[iy,j]: j+=1
            emit(minx+ix*CELL,miny+iy*CELL,minx+j*CELL,miny+iy*CELL, WFILL); ix=j
        else: ix+=1
edge=water & (~binary_erosion(water,iterations=1))
for iy,ix in np.argwhere(edge):
    if inb[iy,ix]: emit(minx+ix*CELL,miny+iy*CELL,minx+ix*CELL+CELL,miny+iy*CELL, WEDGE)
for x1,y1,z1,x2,y2,z2,c in B:
    if   isblue(c): nc=WEDGE
    elif c==(100,50,0): nc=SAND
    elif c in ((64,64,64),(128,128,128)): nc=STONE
    elif c==(0,0,0): nc=DSTONE
    elif c in ((150,100,0),(255,215,0)): nc=ROOF
    elif c==(0,127,0): nc=GRASS
    else: nc=c
    out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z1,x2,y2,z2,nc[0],nc[1],nc[2]))
open(f'{Z}_colored.txt','w',newline='').write('\r\n'.join(out)+'\r\n')
print('%s water=%d L=%d'%(Z,int(water.sum()),len(out)))
