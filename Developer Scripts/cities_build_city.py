"""Themed city styler with careful water shading. foot->floor, water(blue)->filled water,
outer->theme (dark cavern / rock / snow)."""
import sys, numpy as np, math, random
from scipy.ndimage import binary_dilation, binary_fill_holes, binary_erosion, label as _label
ZONE=sys.argv[1]; THEME=sys.argv[2]
TH={
 'neriak': dict(FLOOR=(78,72,92),FLOOR2=(68,62,82),WALL=(122,108,148),WATER=(58,74,108),WATER2=(70,88,122),WEDGE=(40,52,84),ACC=(150,90,180),ACCSRC=(100,50,0),BRN=(120,120,150),outer='dark'),
 'kaladim':dict(FLOOR=(188,168,128),FLOOR2=(176,156,118),WALL=(140,118,88),WATER=(96,146,176),WATER2=(112,160,188),WEDGE=(60,104,140),ACC=(198,150,60),ACCSRC=(150,100,0),BRN=(150,110,70),outer='rock'),
 'halas':  dict(FLOOR=(202,194,178),FLOOR2=(190,182,166),WALL=(122,100,74),WATER=(150,192,214),WATER2=(166,204,224),WEDGE=(96,146,176),ACC=(150,120,80),ACCSRC=(150,100,0),BRN=(122,100,74),outer='snow'),
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
black=raster(lambda c:c==(0,0,0)); blue=raster(lambda c:c==(0,0,255)); dbrown=raster(lambda c:c==(100,50,0))
struct=black|dbrown
foot=binary_fill_holes(binary_dilation(struct,iterations=6))
water=binary_fill_holes(binary_dilation(blue,iterations=2)) & (~binary_dilation(black,iterations=1))
floor=foot & (~water)
outer=(~foot) & (~water)
xg=(np.arange(gw)*CELL+minx)[None,:]; yg=(np.arange(gh)*CELL+miny)[:,None]
PAD=int(max(maxx-minx,maxy-miny)*0.05); inb=(xg>minx+PAD)&(xg<maxx-PAD)&(yg>miny+PAD)&(yg<maxy-PAD)
def fillmask(mask,c1,c2):
    for iy in range(gh):
        ix=0
        while ix<gw:
            if mask[iy,ix] and inb[iy,ix]:
                j=ix
                while j<gw and mask[iy,j]: j+=1
                emit(minx+ix*CELL,miny+iy*CELL,minx+j*CELL,miny+iy*CELL, c1 if iy%2 else c2); ix=j
            else: ix+=1
fillmask(floor, TH['FLOOR'], TH['FLOOR2'])
fillmask(water, TH['WATER'], TH['WATER2'])
edge=water & (~binary_erosion(water,iterations=1))
for iy,ix in np.argwhere(edge):
    if inb[iy,ix]: emit(minx+ix*CELL,miny+iy*CELL,minx+ix*CELL+CELL,miny+iy*CELL, TH['WEDGE'])
# outer texture
random.seed(3); ii=np.argwhere(outer & inb)
if TH['outer']=='dark':
    for k in range(0,len(ii),3):
        iy,ix=ii[k]
        if random.random()<0.5: emit(minx+ix*CELL,miny+iy*CELL,minx+ix*CELL+CELL*1.6,miny+iy*CELL+CELL*1.6,(58,52,64))
elif TH['outer']=='rock':
    for k in range(0,len(ii),3):
        iy,ix=ii[k]
        if random.random()<0.5: emit(minx+ix*CELL,miny+iy*CELL,minx+ix*CELL+CELL*1.6,miny+iy*CELL+CELL*1.6,(150,132,104))
elif TH['outer']=='snow':
    for k in range(0,len(ii),4):
        iy,ix=ii[k]
        if random.random()<0.35: emit(minx+ix*CELL,miny+iy*CELL,minx+ix*CELL+CELL*1.2,miny+iy*CELL,(150,166,182))
# geometry recolor
for x1,y1,z1,x2,y2,z2,c in B:
    if   c==(0,0,255): nc=TH['WEDGE']
    elif c==(100,50,0): nc=TH['BRN']
    elif c==(160,120,60): nc=TH['ACC']
    elif c==(150,100,0): nc=TH['ACC']
    elif c==(85,184,20): nc=(96,132,70)
    elif c==(128,128,128): nc=TH['WALL']
    elif c==(128,0,0): nc=(150,60,50)
    elif c==(0,0,0): nc=TH['WALL']
    else: nc=c
    out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z1,x2,y2,z2,nc[0],nc[1],nc[2]))
open(f'{ZONE}_colored.txt','w',newline='').write('\r\n'.join(out)+'\r\n')
print('%s(%s): floor=%d water=%d L=%d'%(ZONE,THEME,int(floor.sum()),int(water.sum()),len(out)))
