import sys, numpy as np, random
from scipy.ndimage import binary_dilation, binary_fill_holes, binary_erosion
ZONE=sys.argv[1]
def parse(p):
    o=[]
    for l in open(p,encoding='utf-8',errors='replace'):
        l=l.strip()
        if l.startswith('L'):
            f=l[2:].split(','); o.append((float(f[0]),float(f[1]),float(f[2]),float(f[3]),float(f[4]),float(f[5]),(int(f[6]),int(f[7]),int(f[8]))))
    return o
B=parse(f'{ZONE}.txt')
xs=[v for s in B for v in (s[0],s[3])]; ys=[v for s in B for v in (s[1],s[4])]
minx,maxx,miny,maxy=min(xs),max(xs),min(ys),max(ys)
SAND=(226,208,150); SAND2=(216,196,138); DUNE=(202,180,120); ROCK=(180,160,120); DIRT=(190,164,110)
WFILL=(96,178,196); WFILL2=(112,190,206); WEDGE=(48,120,150); PALM=(96,140,70)
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
allg=raster(lambda s:True); blue=raster(lambda s:s[6] in ((0,0,255),(0,0,240)))
interior=binary_fill_holes(binary_dilation(allg,iterations=3))
water=binary_fill_holes(binary_dilation(blue,iterations=2)) & interior
xg=(np.arange(gw)*CELL+minx)[None,:]; yg=(np.arange(gh)*CELL+miny)[:,None]
PAD=int(span*0.04); inb=(xg>minx+PAD)&(xg<maxx-PAD)&(yg>miny+PAD)&(yg<maxy-PAD)
# sand fill
for iy in range(gh):
    ix=0
    while ix<gw:
        if interior[iy,ix] and not water[iy,ix] and inb[iy,ix]:
            j=ix
            while j<gw and interior[iy,j] and not water[iy,j]: j+=1
            emit(minx+ix*CELL,miny+iy*CELL,minx+j*CELL,miny+iy*CELL, SAND if iy%2 else SAND2); ix=j
        else: ix+=1
# sparse dune ripples
random.seed(5)
for iy in range(0,gh,4):
    for ix in range(0,gw,6):
        if interior[iy,ix] and not water[iy,ix] and inb[iy,ix] and random.random()<0.3:
            x=minx+ix*CELL; y=miny+iy*CELL; w=CELL*random.uniform(3,6)
            emit(x,y,x+w*0.5,y-CELL*0.6,DUNE); emit(x+w*0.5,y-CELL*0.6,x+w,y,DUNE)
# oasis water
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
    if   c in ((0,0,255),(0,0,240)): nc=WEDGE
    elif c==(0,240,0) or c==(0,127,0): nc=PALM
    elif c==(100,50,0): nc=DIRT
    elif c==(128,128,128) or c==(125,125,125): nc=ROCK
    elif c==(0,0,0): nc=DUNE
    else: nc=c
    out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z1,x2,y2,z2,nc[0],nc[1],nc[2]))
open(f'{ZONE}_colored.txt','w',newline='').write('\r\n'.join(out)+'\r\n')
print('%s desert L=%d water=%d'%(ZONE,len(out),int(water.sum())))
