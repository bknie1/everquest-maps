"""Grobb — troll mud pit (like Innothule). Muddy brown-green ground throughout, dark mud
walls, murky green patches, the arena kept. No open water."""
import numpy as np, math, random
from scipy.ndimage import binary_dilation, binary_fill_holes, label as _label
def parse(path):
    out=[]
    for l in open(path,encoding='utf-8',errors='replace'):
        l=l.strip()
        if l.startswith('L'):
            f=l[2:].split(','); out.append((float(f[0]),float(f[1]),float(f[2]),float(f[3]),float(f[4]),float(f[5]),(int(f[6]),int(f[7]),int(f[8]))))
    return out
B=parse('grobb.txt')
xs=[v for s in B for v in (s[0],s[3])]; ys=[v for s in B for v in (s[1],s[4])]
minx,maxx,miny,maxy=min(xs),max(xs),min(ys),max(ys)
MUD=(126,116,80); MUD2=(140,130,92); MUDW=(104,112,74); WALL=(88,78,58); MOSS=(96,124,68); TREE=(70,98,54); REDS=(150,60,50)
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
black=raster(lambda c:c==(0,0,0)); dbrown=raster(lambda c:c==(100,50,0)); green=raster(lambda c:c==(85,184,20))
foot=binary_fill_holes(binary_dilation(black|dbrown,iterations=7))
xg=(np.arange(gw)*CELL+minx)[None,:]; yg=(np.arange(gh)*CELL+miny)[:,None]
PAD=110; inb=(xg>minx+PAD)&(xg<maxx-PAD)&(yg>miny+PAD)&(yg<maxy-PAD)
# whole footprint = muddy ground (dense muddy hatch); darker mud in the dark-brown areas
mudpits=binary_fill_holes(binary_dilation(dbrown,iterations=2))
random.seed(4)
for iy in range(gh):
    ix=0
    while ix<gw:
        if foot[iy,ix] and inb[iy,ix]:
            j=ix
            while j<gw and foot[iy,j]: j+=1
            xx=minx+ix*CELL
            while xx<minx+j*CELL:
                col=MUDW if mudpits[iy,ix] else (MUD if random.random()<0.6 else MUD2)
                if mudpits[iy,ix] or random.random()<0.5: emit(xx,miny+iy*CELL,xx+CELL*random.uniform(1.1,2.0),miny+iy*CELL, col)
                xx+=CELL*random.uniform(2.0,3.2)
            ix=j
        else: ix+=1
# murky moss/veg patches + a few swamp trees on the mud
random.seed(8); pl=0; ii=np.argwhere(foot & inb)
def tree(cx,cy,s,seed):
    r=random.Random(seed); n=6
    pts=[(cx+math.cos(a/n*2*math.pi)*s*r.uniform(.7,1.1),cy+math.sin(a/n*2*math.pi)*s*r.uniform(.7,1.1)) for a in range(n)]
    for i in range(n): emit(pts[i][0],pts[i][1],pts[(i+1)%n][0],pts[(i+1)%n][1],TREE)
for k in range(0,len(ii),90):
    iy,ix=ii[k]; tree(minx+ix*CELL,miny+iy*CELL,random.uniform(12,20),pl); pl+=1
# geometry recolor
for x1,y1,z1,x2,y2,z2,c in B:
    if   c==(100,50,0): nc=(96,74,48)
    elif c==(85,184,20): nc=MOSS
    elif c==(128,0,0): nc=REDS
    elif c==(0,0,0): nc=WALL
    else: nc=c
    out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z1,x2,y2,z2,nc[0],nc[1],nc[2]))
open('grobb_colored.txt','w',newline='').write('\r\n'.join(out)+'\r\n')
print('grobb: foot=%d L=%d'%(int(foot.sum()),len(out)))
