"""Solusek fire dungeons. Sol A/B/C are pre-colored multi-level (blue=Z-level, NOT water) ->
recolor to a fiery palette. Temple = black+red(lava) geometry -> lava shading."""
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
B=parse(f'{ZONE}.txt'); out=[]
if ZONE in ('soldunga','soldungb','soldungc'):
    # fire z-level recolor
    MAIN=(198,118,72)   # teal level -> ember terracotta
    LOW =(150,74,60)    # blue level -> deep rust/maroon (NOT water)
    ACC =(224,152,58)   # gold level -> bright lava-gold
    for x1,y1,z1,x2,y2,z2,c in B:
        if   c==(60,190,180): nc=MAIN
        elif c==(70,110,200): nc=LOW
        elif c==(225,175,70): nc=ACC
        else: nc=c
        out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z1,x2,y2,z2,nc[0],nc[1],nc[2]))
else:  # soltemple: black walls + red(127,0,0) lava
    xs=[v for s in B for v in (s[0],s[3])]; ys=[v for s in B for v in (s[1],s[4])]
    minx,maxx,miny,maxy=min(xs),max(xs),min(ys),max(ys)
    LAVA=(214,84,22); LAVA2=(196,66,16); CRUST=(120,42,12); GLOW=(248,150,50); WALL=(120,96,84)
    z0=-1.0
    def emit(x1,y1,x2,y2,c): out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z0,x2,y2,z0,c[0],c[1],c[2]))
    CELL=6.0; gw=int((maxx-minx)/CELL)+2; gh=int((maxy-miny)/CELL)+2
    gx=lambda x:int((x-minx)/CELL); gy=lambda y:int((y-miny)/CELL)
    def raster(cond):
        m=np.zeros((gh,gw),bool)
        for s in B:
            if cond(s[6]):
                x1,y1,x2,y2=s[0],s[1],s[3],s[4]; n=int(max(abs(x2-x1),abs(y2-y1))/CELL)+1
                for i in range(n+1):
                    t=i/n; ix=gx(x1+(x2-x1)*t); iy=gy(y1+(y2-y1)*t)
                    if 0<=ix<gw and 0<=iy<gh: m[iy,ix]=True
        return m
    red=raster(lambda c:c==(127,0,0))
    lava=binary_fill_holes(binary_dilation(red,iterations=2))
    for iy in range(gh):
        ix=0
        while ix<gw:
            if lava[iy,ix]:
                j=ix
                while j<gw and lava[iy,j]: j+=1
                emit(minx+ix*CELL,miny+iy*CELL,minx+j*CELL,miny+iy*CELL, LAVA if iy%2 else LAVA2); ix=j
            else: ix+=1
    edge=lava & (~binary_erosion(lava,iterations=1))
    for iy,ix in np.argwhere(edge): emit(minx+ix*CELL,miny+iy*CELL,minx+ix*CELL+CELL,miny+iy*CELL,CRUST)
    for x1,y1,z1,x2,y2,z2,c in B:
        if   c==(127,0,0): nc=CRUST
        elif c==(0,0,0): nc=WALL
        elif c==(127,127,127): nc=(150,140,130)
        else: nc=c
        out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z1,x2,y2,z2,nc[0],nc[1],nc[2]))
open(f'{ZONE}_colored.txt','w',newline='').write('\r\n'.join(out)+'\r\n')
print('%s L=%d'%(ZONE,len(out)))
