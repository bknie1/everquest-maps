"""Erud's Crossing (erudsxing) — generic Kerra island: ocean flood-filled blue everywhere,
small sandy island (palms + beach), camp/dock structures kept."""
import numpy as np, math, random
from scipy.ndimage import binary_dilation, label as _label
def parse(path):
    out=[]
    for l in open(path,encoding='utf-8',errors='replace'):
        l=l.strip()
        if l.startswith('L'):
            f=l[2:].split(','); out.append((float(f[0]),float(f[1]),float(f[2]),float(f[3]),float(f[4]),float(f[5]),(int(f[6]),int(f[7]),int(f[8]))))
    return out
B=parse('erudsxing.txt')
minx,maxx,miny,maxy=-4805,2728,-2751,4640
OCEAN=(150,196,224); OCEAN2=(128,180,214); WOUT=(70,140,196)
SAND=(214,198,150); SAND2=(196,178,126); PALM=(60,120,60); PALMTR=(120,90,50)
z0=0.0; out=[]
def emit(x1,y1,x2,y2,c): out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z0,x2,y2,z0,c[0],c[1],c[2]))
CELL=34.0; gw=int((maxx-minx)/CELL)+2; gh=int((maxy-miny)/CELL)+2
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
# island coast = blue in the center; flood island interior from its centroid
islcoast=np.zeros((gh,gw),bool)
for s in B:
    x1,y1,x2,y2=s[0],s[1],s[3],s[4]
    if s[6]==(0,0,255) and abs((x1+x2)/2)<1800 and 200<(y1+y2)/2<2400:
        n=int(max(abs(x2-x1),abs(y2-y1))/CELL)+1
        for i in range(n+1):
            t=i/n; ix=gx(x1+(x2-x1)*t); iy=gy(y1+(y2-y1)*t)
            if 0<=ix<gw and 0<=iy<gh: islcoast[iy,ix]=True
# EVEN-ODD fill of the island coast polygon (center blue segments)
csegs=[(s[0],s[1],s[3],s[4]) for s in B if s[6]==(0,0,255) and abs((s[0]+s[3])/2)<1900 and 300<(s[1]+s[4])/2<2200]
cy0=min(min(b,d) for a,b,c,d in csegs); cy1=max(max(b,d) for a,b,c,d in csegs)
island=np.zeros((gh,gw),bool)
yy=cy0+2
while yy<cy1:
    xs=[]
    for x1,y1,x2,y2 in csegs:
        if (y1<=yy<y2) or (y2<=yy<y1):
            t=(yy-y1)/(y2-y1); xs.append(x1+(x2-x1)*t)
    xs.sort()
    for k in range(0,len(xs)-1,2):
        for ix in range(gx(xs[k]), gx(xs[k+1])+1):
            if 0<=ix<gw: island[gy(yy),ix]=True
    yy+=CELL
ocean=~island
# 1) ocean hatch (coarse) — skip island
for iy in range(0,gh,1):
    ix=0
    while ix<gw:
        if ocean[iy,ix]:
            j=ix
            while j<gw and ocean[iy,j]: j+=1
            if iy%2==0: emit(minx+ix*CELL,miny+iy*CELL,minx+j*CELL,miny+iy*CELL, OCEAN if (iy//2)%2 else OCEAN2)
            ix=j
        else: ix+=1
# 2) island sand fill
for iy in range(gh):
    ix=0
    while ix<gw:
        if island[iy,ix]:
            j=ix
            while j<gw and island[iy,j]: j+=1
            emit(minx+ix*CELL,miny+iy*CELL,minx+j*CELL,miny+iy*CELL, SAND if iy%2 else SAND2); ix=j
        else: ix+=1
# 3) palm trees scattered on the island
def palm(cx,cy,s):
    emit(cx,cy,cx,cy-s,PALMTR)                       # trunk
    for a in (-60,-30,0,30,60):
        ang=math.radians(a-90); ex=cx+math.cos(ang)*s*0.7; ey=cy-s+math.sin(ang)*s*0.7
        emit(cx,cy-s,ex,ey,PALM)                     # fronds
random.seed(5); ii=np.argwhere(island); placed=0
if len(ii):
    for _ in range(min(40,len(ii))):
        iy,ix=ii[random.randrange(len(ii))]
        if binary_dilation(islcoast,iterations=2)[iy,ix]: continue
        palm(minx+ix*CELL,miny+iy*CELL, random.uniform(40,70)); placed+=1
# 4) geometry on top
for x1,y1,z1,x2,y2,z2,c in B:
    if   c==(0,0,255): nc=WOUT
    elif c==(100,50,0): nc=(150,110,64)   # island paths/dock -> wood/sand-brown
    elif c==(0,0,0): nc=(90,84,74)
    else: nc=c
    out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z1,x2,y2,z2,nc[0],nc[1],nc[2]))
open('erudsxing_colored.txt','w',newline='').write('\r\n'.join(out)+'\r\n')
print('island=%d palms=%d L=%d'%(int(island.sum()),placed,len(out)))
