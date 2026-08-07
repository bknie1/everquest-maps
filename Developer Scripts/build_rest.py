"""Everfrost (snow + ice river), Runnyeye (goblin recolor), Stonebrunt (mountain)."""
import sys, numpy as np, math, random
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
z0=-1.0; out=[]
def emit(x1,y1,x2,y2,c): out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z0,x2,y2,z0,c[0],c[1],c[2]))
span=max(maxx-minx,maxy-miny); CELL=max(8.0, span/440); gw=int((maxx-minx)/CELL)+2; gh=int((maxy-miny)/CELL)+2
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
xg=(np.arange(gw)*CELL+minx)[None,:]; yg=(np.arange(gh)*CELL+miny)[:,None]
PAD=int(span*0.05); inb=(xg>minx+PAD)&(xg<maxx-PAD)&(yg>miny+PAD)&(yg<maxy-PAD)
def fillmask(mask,c1,c2,step=1):
    for iy in range(0,gh,step):
        ix=0
        while ix<gw:
            if mask[iy,ix] and inb[iy,ix]:
                j=ix
                while j<gw and mask[iy,j]: j+=1
                emit(minx+ix*CELL,miny+iy*CELL,minx+j*CELL,miny+iy*CELL, c1 if iy%2 else c2); ix=j
            else: ix+=1

if ZONE=='everfrost':
    black=raster(lambda c:c==(0,0,0)); ice=raster(lambda c:c==(150,255,255)); blue=raster(lambda c:c==(0,0,255))
    interior=binary_fill_holes(binary_dilation(black,iterations=3))
    water=binary_fill_holes(binary_dilation(ice|blue,iterations=2))
    struct=binary_fill_holes(binary_dilation(black,iterations=2))
    snow=interior & (~water)
    fillmask(snow,(224,230,238),(214,222,232),step=1)         # snow ground (light, cool)
    fillmask(water,(150,214,230),(166,224,238),step=1)        # ice water
    edge=water & (~binary_erosion(water,iterations=1))
    for iy,ix in np.argwhere(edge):
        if inb[iy,ix]: emit(minx+ix*CELL,miny+iy*CELL,minx+ix*CELL+CELL,miny+iy*CELL,(96,150,180))
    for x1,y1,z1,x2,y2,z2,c in B:
        if c==(150,255,255): nc=(120,180,205)
        elif c==(0,0,255): nc=(96,150,180)
        elif c==(128,128,128): nc=(150,158,170)     # rock/snow contours
        elif c==(0,0,0): nc=(96,102,112)
        else: nc=c
        out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z1,x2,y2,z2,nc[0],nc[1],nc[2]))

elif ZONE=='runnyeye':
    # pre-colored multi-level dungeon; recolor to GREEN GOBLIN (blue here is a Z-level, NOT water)
    for x1,y1,z1,x2,y2,z2,c in B:
        if   c==(60,190,180): nc=(110,158,78)     # teal level -> goblin green
        elif c==(70,110,200): nc=(74,120,60)      # blue level -> deep green (NOT water)
        elif c==(225,175,70): nc=(190,150,66)     # gold -> torch amber
        else: nc=c
        out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z1,x2,y2,z2,nc[0],nc[1],nc[2]))

elif ZONE=='stonebrunt':
    black=raster(lambda c:c==(0,0,0)); blue=raster(lambda c:c==(0,0,255)); green=raster(lambda c:c==(0,127,0))
    water=binary_fill_holes(binary_dilation(blue,iterations=2)) & (~binary_dilation(black,iterations=1))
    fillmask(water,(120,164,196),(136,178,206),step=1)
    # sparse rocky ground tint in the vegetation basins
    veg=binary_fill_holes(binary_dilation(green,iterations=2))
    random.seed(3); ii=np.argwhere(veg & inb)
    for k in range(0,len(ii),5):
        iy,ix=ii[k]
        if random.random()<0.4: emit(minx+ix*CELL,miny+iy*CELL,minx+ix*CELL+CELL*1.4,miny+iy*CELL,(150,170,120))
    for x1,y1,z1,x2,y2,z2,c in B:
        if   c==(0,0,255): nc=(96,140,176)
        elif c==(0,127,0): nc=(96,140,80)          # vegetation
        elif c==(240,240,240): nc=(224,228,232)    # snow peaks
        elif c==(64,64,64): nc=(120,116,108)       # rock
        elif c==(100,50,0): nc=(150,120,80)        # dirt
        else: nc=c
        out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z1,x2,y2,z2,nc[0],nc[1],nc[2]))

open(f'{ZONE}_colored.txt','w',newline='').write('\r\n'.join(out)+'\r\n')
print('%s L=%d'%(ZONE,len(out)))
