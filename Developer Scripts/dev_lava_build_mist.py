"""Castle Mistmoore — gothic dark-elf vampire stronghold. Blue-grey stone floors, dark moat,
torch-lit gold paths, purple crest accents, mazelike corridors kept dark."""
import numpy as np, math, random
from scipy.ndimage import binary_dilation, binary_fill_holes, binary_erosion
def parse(path):
    out=[]
    for l in open(path,encoding='utf-8',errors='replace'):
        l=l.strip()
        if l.startswith('L'):
            f=l[2:].split(','); out.append((float(f[0]),float(f[1]),float(f[2]),float(f[3]),float(f[4]),float(f[5]),(int(f[6]),int(f[7]),int(f[8]))))
    return out
B=parse('mistmoore.txt')
xs=[v for s in B for v in (s[0],s[3])]; ys=[v for s in B for v in (s[1],s[4])]
minx,maxx,miny,maxy=min(xs),max(xs),min(ys),max(ys)
FLOOR=(122,132,154); FLOOR2=(110,120,142); WALL=(64,72,94); WATER=(46,58,94); WATER2=(58,70,106); WEDGE=(34,44,74)
STONE=(140,148,164); GOLD=(172,142,72); ACCENT=(150,90,175); MOSS=(86,96,78); MOSS2=(74,84,68)
z0=-1.0; out=[]
def emit(x1,y1,x2,y2,c): out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z0,x2,y2,z0,c[0],c[1],c[2]))
CELL=5.0; gw=int((maxx-minx)/CELL)+2; gh=int((maxy-miny)/CELL)+2
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
black=raster(lambda c:c==(0,0,0)); blue=raster(lambda c:c==(0,0,255)); gray=raster(lambda c:c==(128,128,128))
foot=binary_fill_holes(binary_dilation(black,iterations=5))
water=binary_fill_holes(binary_dilation(blue,iterations=2)) & (~binary_dilation(black,iterations=1))
stonefloor=binary_fill_holes(binary_dilation(gray,iterations=2)) & foot & (~water)
floor=foot & (~water)
outer=(~foot) & (~water)
xg=(np.arange(gw)*CELL+minx)[None,:]; yg=(np.arange(gh)*CELL+miny)[:,None]
PAD=int(max(maxx-minx,maxy-miny)*0.05); inb=(xg>minx+PAD)&(xg<maxx-PAD)&(yg>miny+PAD)&(yg<maxy-PAD)
def fillmask(mask,c1,c2,step=1):
    for iy in range(0,gh,step):
        ix=0
        while ix<gw:
            if mask[iy,ix] and inb[iy,ix]:
                j=ix
                while j<gw and mask[iy,j]: j+=1
                emit(minx+ix*CELL,miny+iy*CELL,minx+j*CELL,miny+iy*CELL, c1 if iy%2 else c2); ix=j
            else: ix+=1
fillmask(floor, FLOOR, FLOOR2)
fillmask(stonefloor, STONE, (128,136,152))
fillmask(water, WATER, WATER2)
edge=water & (~binary_erosion(water,iterations=1))
for iy,ix in np.argwhere(edge):
    if inb[iy,ix]: emit(minx+ix*CELL,miny+iy*CELL,minx+ix*CELL+CELL,miny+iy*CELL, WEDGE)
# outer courtyard = dark moss hatch (sparse)
random.seed(3); ii=np.argwhere(outer & inb)
for k in range(0,len(ii),4):
    iy,ix=ii[k]
    if random.random()<0.4: emit(minx+ix*CELL,miny+iy*CELL,minx+ix*CELL+CELL*1.4,miny+iy*CELL,MOSS if random.random()<0.6 else MOSS2)
# geometry recolor: gold->torch-gold, gray->stone, blue->water edge, black->dark wall
for x1,y1,z1,x2,y2,z2,c in B:
    if   c==(0,0,255): nc=WEDGE
    elif c==(150,100,0): nc=GOLD
    elif c==(255,215,0): nc=ACCENT
    elif c==(128,128,128): nc=STONE
    elif c==(0,0,0): nc=WALL
    else: nc=c
    out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z1,x2,y2,z2,nc[0],nc[1],nc[2]))
open('mistmoore_colored.txt','w',newline='').write('\r\n'.join(out)+'\r\n')
print('mistmoore: floor=%d water=%d stone=%d L=%d'%(int(floor.sum()),int(water.sum()),int(stonefloor.sum()),len(out)))
