import numpy as np, math, random
def parse(path):
    out=[]
    for l in open(path,encoding='utf-8',errors='replace'):
        l=l.strip()
        if not l.startswith('L'): continue
        f=l[2:].split(','); out.append((float(f[0]),float(f[1]),float(f[2]),float(f[3]),float(f[4]),float(f[5]),(int(f[6]),int(f[7]),int(f[8]))))
    return out
B=parse('lfaydark.txt')
minx,maxx,miny,maxy=-3937,2222,-2208,1182
CAN=(48,86,52); CAN2=(36,66,42); CANFILL=(74,116,72); TRUNK=(74,56,34); WALL=(64,54,44); PATH=(140,108,60)
z0=1.0; out=[]
def emit(x1,y1,x2,y2,c): out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z0,x2,y2,z0,c[0],c[1],c[2]))
for x1,y1,z1,x2,y2,z2,c in B:
    nc=WALL if c==(0,0,0) else (PATH if c in ((160,120,60),(100,50,0)) else c)
    out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z1,x2,y2,z2,nc[0],nc[1],nc[2]))
CELL=42.0; gw=int((maxx-minx)/CELL)+1; gh=int((maxy-miny)/CELL)+1
occ=np.zeros((gh,gw),bool); gx=lambda x:int((x-minx)/CELL); gy=lambda y:int((y-miny)/CELL)
for x1,y1,_,x2,y2,_,c in B:
    n=int(max(abs(x2-x1),abs(y2-y1))/CELL)+1
    for i in range(n+1):
        t=i/n; ix=gx(x1+(x2-x1)*t); iy=gy(y1+(y2-y1)*t)
        if 0<=ix<gw and 0<=iy<gh: occ[iy,ix]=True
from scipy.ndimage import binary_dilation
near=binary_dilation(occ, iterations=3)
def tree(cx,cy,r,seed):
    rnd=random.Random(seed); n=rnd.choice([9,10,11]); off=rnd.random()*6.28; pts=[]
    for i in range(n):
        a=off+2*math.pi*i/n; rr=r*(0.80+0.34*rnd.random()); pts.append((cx+rr*math.cos(a),cy+rr*math.sin(a)))
    for i in range(n): emit(*pts[i],*pts[(i+1)%n],CAN)
    ys=[p[1] for p in pts]; yy=min(ys)+3
    while yy<max(ys):
        xs=[]
        for i in range(n):
            x1,y1=pts[i]; x2,y2=pts[(i+1)%n]
            if (y1<=yy<y2) or (y2<=yy<y1): t=(yy-y1)/(y2-y1); xs.append(x1+(x2-x1)*t)
        xs.sort()
        for k in range(0,len(xs)-1,2):
            if xs[k+1]-xs[k]>=2: emit(xs[k],yy,xs[k+1],yy,CANFILL)
        yy+=9
    emit(cx-3,cy,cx+3,cy,TRUNK)
random.seed(5); SP=180; placed=0; y=miny+150
while y<maxy-150:
    x=minx+150
    while x<maxx-150:
        jx=x+random.uniform(-54,54); jy=y+random.uniform(-54,54); ix,iy=gx(jx),gy(jy)
        if 0<=ix<gw and 0<=iy<gh and not near[iy,ix]:
            tree(jx,jy,random.uniform(34,60),placed); placed+=1
        x+=SP
    y+=SP
open('lfaydark_colored.txt','w',newline='').write('\r\n'.join(out)+'\r\n')
print('dark trees: %d  L=%d'%(placed,len(out)))
