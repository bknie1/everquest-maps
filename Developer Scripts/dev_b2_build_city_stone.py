"""Qeynos/Freeport stone-city styler — stone plazas, shaded harbor/canal water, dirt roads."""
import sys, numpy as np
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
FLOOR=(198,190,170); FLOOR2=(188,180,160); WALL=(96,90,80); STONE=(150,144,130); ROAD=(176,150,104); GRASS=(120,150,90)
WFILL=(96,164,212); WFILL2=(112,178,222); WEDGE=(40,92,158)
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
allg=raster(lambda s:True); blue=raster(lambda s:s[6]==(0,0,255))
interior=binary_fill_holes(binary_dilation(allg,iterations=4))
water=binary_fill_holes(binary_dilation(blue,iterations=2)) & interior
floor=interior & (~water)
xg=(np.arange(gw)*CELL+minx)[None,:]; yg=(np.arange(gh)*CELL+miny)[:,None]
PAD=int(span*0.045); inb=(xg>minx+PAD)&(xg<maxx-PAD)&(yg>miny+PAD)&(yg<maxy-PAD)
for iy in range(gh):
    ix=0
    while ix<gw:
        if floor[iy,ix] and inb[iy,ix]:
            j=ix
            while j<gw and floor[iy,j] and inb[iy,j]: j+=1
            emit(minx+ix*CELL,miny+iy*CELL,minx+j*CELL,miny+iy*CELL, FLOOR if iy%2 else FLOOR2); ix=j
        else: ix+=1
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
for x1,y1,z1,x2,y2,z2,c in B:
    if   c==(0,0,255): nc=WEDGE
    elif c==(100,50,0): nc=ROAD
    elif c==(150,100,0): nc=ROAD
    elif c==(64,64,64): nc=STONE
    elif c==(128,128,128): nc=STONE
    elif c==(0,127,0) or c==(0,125,0): nc=GRASS
    elif c==(0,0,0): nc=WALL
    else: nc=c
    out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z1,x2,y2,z2,nc[0],nc[1],nc[2]))
open(f'{ZONE}_colored.txt','w',newline='').write('\r\n'.join(out)+'\r\n')
print('%s L=%d water=%d floor=%d'%(ZONE,len(out),int(water.sum()),int(floor.sum())))
