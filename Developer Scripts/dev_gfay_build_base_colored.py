"""Greater Faydark colored base: keep geometry, litter the forest AROUND Kelethin
with Gfay canopy trees (Nektulos-style density), avoiding platforms/paths/edges."""
import numpy as np, math, random
def parse(path):
    out=[]
    for l in open(path,encoding='utf-8',errors='replace'):
        l=l.strip()
        if not l.startswith('L'): continue
        f=l[2:].split(','); out.append((float(f[0]),float(f[1]),float(f[2]),float(f[3]),float(f[4]),float(f[5]),(int(f[6]),int(f[7]),int(f[8]))))
    return out
B=parse('gfaydark.txt')
minx,maxx,miny,maxy=-2699,2663,-2709,2736

CAN=(58,104,52); CAN2=(44,84,42); CANFILL=(108,158,86); TRUNK=(92,60,30); PATH=(150,116,66); WALL=(70,58,44)
HUTW=(104,72,40); HUTR=(142,98,46); HUTD=(70,45,25)
z0=1.0
out=[]
def emit(x1,y1,x2,y2,c,z=z0): out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z,x2,y2,z,c[0],c[1],c[2]))

# 1) copy geometry (soften black->wall brown, keep tan paths & platforms)
for x1,y1,z1,x2,y2,z2,c in B:
    nc = WALL if c==(0,0,0) else (PATH if c==(160,120,60) else c)
    out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z1,x2,y2,z2,nc[0],nc[1],nc[2]))

# 2) occupancy grid for rejection (trees avoid geometry: platforms, paths, walls)
CELL=40.0
gw=int((maxx-minx)/CELL)+1; gh=int((maxy-miny)/CELL)+1
occ=np.zeros((gh,gw),bool)
def gx(x): return int((x-minx)/CELL)
def gy(y): return int((y-miny)/CELL)
for x1,y1,_,x2,y2,_,c in B:
    n=int(max(abs(x2-x1),abs(y2-y1))/CELL)+1
    for i in range(n+1):
        t=i/n; ix=gx(x1+(x2-x1)*t); iy=gy(y1+(y2-y1)*t)
        if 0<=ix<gw and 0<=iy<gh: occ[iy,ix]=True
from scipy.ndimage import binary_dilation
near=binary_dilation(occ, iterations=3)   # ~120u buffer around geometry

# Kelethin platform cluster to keep tree-free (tight core)
CITY=(-720,720,-820,650)   # x0,x1,y0,y1

def gfay_tree(cx,cy,r,seed):
    rnd=random.Random(seed); n=rnd.choice([9,10,11])
    off=rnd.random()*6.28
    pts=[]
    for i in range(n):
        a=off+2*math.pi*i/n; rr=r*(0.80+0.34*rnd.random())
        pts.append((cx+rr*math.cos(a),cy+rr*math.sin(a)))
    for i in range(n): emit(*pts[i],*pts[(i+1)%n],CAN)           # canopy outline
    # SHADE: green hatch fill inside the canopy
    ys=[p[1] for p in pts]; yy=min(ys)+3
    while yy<max(ys):
        xs=[]
        for i in range(n):
            x1,y1=pts[i]; x2,y2=pts[(i+1)%n]
            if (y1<=yy<y2) or (y2<=yy<y1):
                t=(yy-y1)/(y2-y1); xs.append(x1+(x2-x1)*t)
        xs.sort()
        for k in range(0,len(xs)-1,2):
            if xs[k+1]-xs[k]>=2: emit(xs[k],yy,xs[k+1],yy,CANFILL)
        yy+=8.5
    emit(cx-3,cy,cx+3,cy,TRUNK); emit(cx,cy-3,cx,cy+3,TRUNK)     # trunk

def orc_hut(cx,cy,s=46):
    w=s*0.5; wallh=s*0.42; roofh=s*0.62; baseY=cy+s*0.4
    emit(cx-w,baseY,cx-w*0.9,baseY-wallh,HUTW); emit(cx+w,baseY,cx+w*0.9,baseY-wallh,HUTW)
    emit(cx-w,baseY,cx+w,baseY,HUTW)                             # ground
    ay=baseY-wallh
    emit(cx-w*1.15,ay,cx,ay-roofh,HUTR); emit(cx+w*1.15,ay,cx,ay-roofh,HUTR); emit(cx-w*1.15,ay,cx+w*1.15,ay,HUTR)
    for t in (0.32,0.62): emit(cx-w*1.15*(1-t),ay-roofh*t,cx+w*1.15*(1-t),ay-roofh*t,HUTR)
    emit(cx-w*0.3,baseY,cx-w*0.3,baseY-wallh*0.7,HUTD); emit(cx+w*0.3,baseY,cx+w*0.3,baseY-wallh*0.7,HUTD)
    emit(cx-w*0.3,baseY-wallh*0.7,cx+w*0.3,baseY-wallh*0.7,HUTD)

# 2b) orc camps in the northern forest (goblin-style huts) — mark so trees avoid them
CAMPS=[(-1980,-1780),(-1870,-1700),(-1910,-1880),     # near An Orc Arsonist (NW)
       (-820,-1620),(-930,-1540),(-720,-1700),         # north-central camp
       (250,-1560),(370,-1660),(170,-1690),            # camp toward Crushbone (N)
       (-300,-1930),(-120,-2010)]                       # scattered north
for (hx,hy) in CAMPS:
    orc_hut(hx,hy,48)
    ix,iy=gx(hx),gy(hy)
    for dx in range(-2,3):
        for dy in range(-2,3):
            if 0<=iy+dy<gh and 0<=ix+dx<gw: near[iy+dy,ix+dx]=True

# 3) scatter on jittered grid
random.seed(42); SP=185; placed=0
y=miny+165
while y<maxy-165:
    x=minx+165
    while x<maxx-165:
        jx=x+random.uniform(-55,55); jy=y+random.uniform(-55,55)
        ix,iy=gx(jx),gy(jy)
        incity = CITY[0]-90<jx<CITY[1]+90 and CITY[2]-90<jy<CITY[3]+90
        if 0<=ix<gw and 0<=iy<gh and not near[iy,ix] and not incity:
            r=random.uniform(34,64); gfay_tree(jx,jy,r,placed); placed+=1
        x+=SP
    y+=SP
open('gfaydark_colored.txt','w',newline='').write('\r\n'.join(out)+'\r\n')
print('trees placed: %d   wrote gfaydark_colored.txt L=%d'%(placed,len(out)))
