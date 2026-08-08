"""Lavastorm Mountains — glowing lava pools + charred rocky mountains, ~25% covered in
spiky rocks and steaming vents (Feerrott=100%, Faydark=50%, Lavastorm=25%)."""
import numpy as np, math, random
from scipy.ndimage import binary_dilation, binary_fill_holes, binary_erosion
def parse(path):
    out=[]
    for l in open(path,encoding='utf-8',errors='replace'):
        l=l.strip()
        if l.startswith('L'):
            f=l[2:].split(','); out.append((float(f[0]),float(f[1]),float(f[2]),float(f[3]),float(f[4]),float(f[5]),(int(f[6]),int(f[7]),int(f[8]))))
    return out
B=parse('lavastorm.txt')
xs=[v for s in B for v in (s[0],s[3])]; ys=[v for s in B for v in (s[1],s[4])]
minx,maxx,miny,maxy=min(xs),max(xs),min(ys),max(ys)
LAVA=(232,96,24); LAVA2=(214,74,16); CRUST=(120,42,12); GLOW=(250,150,50)
ROCK=(120,96,80); RIDGE=(138,112,92); SPK1=(96,84,74); SPK2=(70,60,52); VROCK=(112,98,86); STEAM=(176,178,184); DIRT=(150,120,80)
z0=-1.0; out=[]
def emit(x1,y1,x2,y2,c): out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z0,x2,y2,z0,c[0],c[1],c[2]))
CELL=10.0; gw=int((maxx-minx)/CELL)+2; gh=int((maxy-miny)/CELL)+2
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
black=raster(lambda c:c==(0,0,0)); red=raster(lambda c:c==(255,0,0))
interior=binary_fill_holes(binary_dilation(black,iterations=3))
if interior.sum()<gw*gh*0.2: interior=np.ones((gh,gw),bool)
lava=binary_fill_holes(binary_dilation(red,iterations=2)) & interior
rock=interior & (~lava)
xg=(np.arange(gw)*CELL+minx)[None,:]; yg=(np.arange(gh)*CELL+miny)[:,None]
PAD=int(max(maxx-minx,maxy-miny)*0.05); inb=(xg>minx+PAD)&(xg<maxx-PAD)&(yg>miny+PAD)&(yg<maxy-PAD)
# 0) lava fill (glowing) + crust edge + bright cracks
for iy in range(gh):
    ix=0
    while ix<gw:
        if lava[iy,ix] and inb[iy,ix]:
            j=ix
            while j<gw and lava[iy,j]: j+=1
            emit(minx+ix*CELL,miny+iy*CELL,minx+j*CELL,miny+iy*CELL, LAVA if iy%2 else LAVA2); ix=j
        else: ix+=1
edge=lava & (~binary_erosion(lava,iterations=1))
for iy,ix in np.argwhere(edge):
    if inb[iy,ix]: emit(minx+ix*CELL,miny+iy*CELL,minx+ix*CELL+CELL,miny+iy*CELL, CRUST)
random.seed(5)
for iy,ix in np.argwhere(binary_erosion(lava,iterations=1)):
    if inb[iy,ix] and random.random()<0.10: emit(minx+ix*CELL,miny+iy*CELL,minx+ix*CELL+CELL*random.uniform(1,2),miny+iy*CELL,GLOW)
# 1) sparse charred mountain-ridge hatch on the rock (light)
random.seed(2)
for iy in range(0,gh,3):
    ix=0
    while ix<gw:
        if rock[iy,ix] and inb[iy,ix]:
            j=ix
            while j<gw and rock[iy,j]: j+=1
            xx=minx+ix*CELL
            while xx<minx+j*CELL:
                if random.random()<0.22:
                    Ln=CELL*random.uniform(1.4,2.6); emit(xx,miny+iy*CELL,xx+Ln,miny+iy*CELL+Ln, RIDGE)
                xx+=CELL*random.uniform(3.5,5.5)
            ix=j
        else: ix+=1
# 2) ~25% coverage: spiky rock clusters + steam vents scattered on the rock
def spike(cx,cy,s,seed):
    r=random.Random(seed)
    for _ in range(r.randint(2,4)):
        bx=cx+r.uniform(-s*.6,s*.6); h=s*r.uniform(.8,1.5); w=s*r.uniform(.25,.5)
        emit(bx-w,cy+s*.3,bx,cy-h,SPK1); emit(bx+w,cy+s*.3,bx,cy-h,SPK1); emit(bx-w,cy+s*.3,bx+w,cy+s*.3,SPK2)
def vent(cx,cy,s):
    emit(cx-s*.5,cy+s*.25,cx-s*.3,cy,VROCK); emit(cx-s*.3,cy,cx+s*.3,cy,VROCK)
    emit(cx+s*.3,cy,cx+s*.5,cy+s*.25,VROCK); emit(cx-s*.5,cy+s*.25,cx+s*.5,cy+s*.25,VROCK)
    for dx in (-s*.18,s*.12):
        emit(cx+dx,cy-s*.05,cx+dx-s*.15,cy-s*.5,STEAM); emit(cx+dx-s*.15,cy-s*.5,cx+dx+s*.1,cy-s*.95,STEAM)
        emit(cx+dx+s*.1,cy-s*.95,cx+dx-s*.08,cy-s*1.35,STEAM)
random.seed(11); STEP=5; ns=nv=0
for iy in range(0,gh,STEP):
    for ix in range(0,gw,STEP):
        if rock[iy,ix] and inb[iy,ix] and random.random()<0.25:   # 25% of sampled cells
            cx=minx+ix*CELL+random.uniform(-12,12); cy=miny+iy*CELL+random.uniform(-12,12)
            if random.random()<0.68: spike(cx,cy,random.uniform(16,30),ix*7+iy); ns+=1
            else: vent(cx,cy,random.uniform(16,26)); nv+=1
# geometry recolor
for x1,y1,z1,x2,y2,z2,c in B:
    if   c==(255,0,0): nc=CRUST
    elif c==(100,50,0): nc=DIRT
    elif c==(0,0,0): nc=ROCK
    else: nc=c
    out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z1,x2,y2,z2,nc[0],nc[1],nc[2]))
open('lavastorm_colored.txt','w',newline='').write('\r\n'.join(out)+'\r\n')
print('lavastorm: lava=%d rock=%d spikes=%d vents=%d L=%d'%(int(lava.sum()),int(rock.sum()),ns,nv,len(out)))
