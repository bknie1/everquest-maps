"""Stonebrunt Mountains — craggy KOBOLD highlands. Rocky ridge shading, scattered snow-capped
peaks, trees in the green basins, mountain rivers. (Steamfont/Butcherblock energy, rockier.)"""
import numpy as np, math, random
from scipy.ndimage import binary_dilation, binary_fill_holes, binary_erosion
def parse(path):
    out=[]
    for l in open(path,encoding='utf-8',errors='replace'):
        l=l.strip()
        if l.startswith('L'):
            f=l[2:].split(','); out.append((float(f[0]),float(f[1]),float(f[2]),float(f[3]),float(f[4]),float(f[5]),(int(f[6]),int(f[7]),int(f[8]))))
    return out
B=parse('stonebrunt.txt')
xs=[v for s in B for v in (s[0],s[3])]; ys=[v for s in B for v in (s[1],s[4])]
minx,maxx,miny,maxy=min(xs),max(xs),min(ys),max(ys)
ROCK=(150,142,128); ROCK2=(132,124,110); RIDGE=(120,112,100); PEAK=(150,146,138); SNOW=(224,228,232); TREE=(74,110,64); VEGF=(120,150,90); RIVER=(96,140,176)
z0=-1.0; out=[]
def emit(x1,y1,x2,y2,c): out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z0,x2,y2,z0,c[0],c[1],c[2]))
span=max(maxx-minx,maxy-miny); CELL=span/300; gw=int((maxx-minx)/CELL)+2; gh=int((maxy-miny)/CELL)+2
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
green=raster(lambda c:c==(0,127,0)); blue=raster(lambda c:c==(0,0,255)); black=raster(lambda c:c==(0,0,0))
basin=binary_fill_holes(binary_dilation(green,iterations=2))
water=binary_fill_holes(binary_dilation(blue,iterations=2)) & (~binary_dilation(black,iterations=1))
xg=(np.arange(gw)*CELL+minx)[None,:]; yg=(np.arange(gh)*CELL+miny)[:,None]
PAD=int(span*0.05); inb=(xg>minx+PAD)&(xg<maxx-PAD)&(yg>miny+PAD)&(yg<maxy-PAD)
mountain=(~basin) & (~water) & inb
# rocky ridge shading: angular cross-hatch across the highlands (Butcherblock-ish, sparse)
random.seed(4)
for iy in range(0,gh,2):
    ix=0
    while ix<gw:
        if mountain[iy,ix]:
            j=ix
            while j<gw and mountain[iy,j]: j+=1
            xx=minx+ix*CELL
            while xx<minx+j*CELL:
                if random.random()<0.4:
                    Ln=CELL*random.uniform(1.6,3.0); emit(xx,miny+iy*CELL,xx+Ln,miny+iy*CELL+Ln, ROCK if random.random()<0.6 else ROCK2)
                xx+=CELL*random.uniform(3.0,5.0)
            ix=j
        else: ix+=1
# water fill
for iy in range(gh):
    ix=0
    while ix<gw:
        if water[iy,ix] and inb[iy,ix]:
            j=ix
            while j<gw and water[iy,j]: j+=1
            emit(minx+ix*CELL,miny+iy*CELL,minx+j*CELL,miny+iy*CELL, RIVER); ix=j
        else: ix+=1
# trees in the basins
def tree(cx,cy,s,seed):
    r=random.Random(seed); n=6
    pts=[(cx+math.cos(a/n*2*math.pi)*s*r.uniform(.7,1.1),cy+math.sin(a/n*2*math.pi)*s*r.uniform(.7,1.1)) for a in range(n)]
    for i in range(n): emit(pts[i][0],pts[i][1],pts[(i+1)%n][0],pts[(i+1)%n][1],TREE)
random.seed(8); pl=0; bb=np.argwhere(basin & inb)
for k in range(0,len(bb),40):
    iy,ix=bb[k]; tree(minx+ix*CELL,miny+iy*CELL,random.uniform(30,55),pl); pl+=1
# snow-capped peaks scattered across the mountains
def peak(cx,cy,s):
    emit(cx-s,cy+s*0.6,cx,cy-s,RIDGE); emit(cx+s,cy+s*0.6,cx,cy-s,RIDGE); emit(cx-s,cy+s*0.6,cx+s,cy+s*0.6,RIDGE)
    emit(cx-s*0.32,cy-s*0.15,cx,cy-s,SNOW); emit(cx+s*0.32,cy-s*0.15,cx,cy-s,SNOW)
random.seed(12); mm=np.argwhere(mountain)
for k in range(0,len(mm),90):
    iy,ix=mm[k]
    if random.random()<0.7: peak(minx+ix*CELL,miny+iy*CELL,random.uniform(55,105))
# geometry recolor
for x1,y1,z1,x2,y2,z2,c in B:
    if   c==(0,0,255): nc=RIVER
    elif c==(0,127,0): nc=VEGF
    elif c==(240,240,240): nc=SNOW
    elif c==(64,64,64): nc=RIDGE
    elif c==(100,50,0): nc=(150,120,84)
    else: nc=c
    out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z1,x2,y2,z2,nc[0],nc[1],nc[2]))
open('stonebrunt_colored.txt','w',newline='').write('\r\n'.join(out)+'\r\n')
print('stonebrunt: mountain=%d basin=%d peaks L=%d'%(int(mountain.sum()),int(basin.sum()),len(out)))
