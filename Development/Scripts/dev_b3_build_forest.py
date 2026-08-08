import sys, numpy as np, random, math
from scipy.ndimage import binary_dilation, binary_fill_holes
ZONE,MODE=sys.argv[1],sys.argv[2]
def parse(p):
    o=[]
    for l in open(p,encoding='utf-8',errors='replace'):
        l=l.strip()
        if l.startswith('L'):
            f=l[2:].split(','); o.append((float(f[0]),float(f[1]),float(f[2]),float(f[3]),float(f[4]),float(f[5]),(int(f[6]),int(f[7]),int(f[8]))))
    return o
B=parse(f'{ZONE}.txt')
xs=[v for s in B for v in (s[0],s[3])]; ys=[v for s in B for v in (s[1],s[4])]
minx,maxx,miny,maxy=min(xs),max(xs),min(ys),max(ys)
z0=-1.0; out=[]
def emit(x1,y1,x2,y2,c): out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z0,x2,y2,z0,c[0],c[1],c[2]))
def disc(cx,cy,R,cols):
    for k,rr in enumerate(range(int(R),2,-3)):
        col=cols[min(k,len(cols)-1)]
        pts=[(cx+rr*math.cos(math.radians(a)),cy+rr*math.sin(math.radians(a))) for a in range(0,360,20)]
        for i in range(len(pts)): emit(pts[i][0],pts[i][1],pts[(i+1)%len(pts)][0],pts[(i+1)%len(pts)][1],col)
span=max(maxx-minx,maxy-miny); CELL=span/240.0
gw=int((maxx-minx)/CELL)+2; gh=int((maxy-miny)/CELL)+2
gx=lambda x:int((x-minx)/CELL); gy=lambda y:int((y-miny)/CELL)
m=np.zeros((gh,gw),bool)
for s in B:
    x1,y1,x2,y2=s[0],s[1],s[3],s[4]; n=int(max(abs(x2-x1),abs(y2-y1))/CELL)+1
    for i in range(n+1):
        t=i/n; ix=gx(x1+(x2-x1)*t); iy=gy(y1+(y2-y1)*t)
        if 0<=ix<gw and 0<=iy<gh: m[iy,ix]=True
interior=binary_fill_holes(binary_dilation(m,iterations=4))
PAD=int(span*0.05)
def inb(x,y): return minx+PAD<x<maxx-PAD and miny+PAD<y<maxy-PAD
random.seed(3)
if MODE=='kithicor':
    FLOOR=(96,104,80); TRUNK=(120,66,40); RING=(150,96,58); CORE=(88,48,28); CAN=(70,90,58)
    # massive redwood trunk cross-sections (wide as houses) scattered thickly
    step=int(span/14)
    for gxx in range(int(minx),int(maxx),step):
        for gyy in range(int(miny),int(maxy),step):
            cx=gxx+random.uniform(-step*.3,step*.3); cy=gyy+random.uniform(-step*.3,step*.3)
            if inb(cx,cy) and interior[gy(cy),gx(cx)] and random.random()<0.62:
                R=span*random.uniform(0.018,0.032)   # house-wide trunks
                disc(cx,cy,R,[TRUNK,RING,TRUNK,RING,CORE])
                for a in range(0,360,60): emit(cx,cy,cx+R*0.85*math.cos(math.radians(a)),cy+R*0.85*math.sin(math.radians(a)),RING)
    WALL=(78,64,50)
else:  # dark elf Nektulos: moody, obsidian, sparse dark canopy
    FLOOR=None; CAN=(70,72,88); TRUNK=(58,50,66); WALL=(74,70,86)
    step=int(span/22)
    for gxx in range(int(minx),int(maxx),step):
        for gyy in range(int(miny),int(maxy),step):
            cx=gxx+random.uniform(-step*.3,step*.3); cy=gyy+random.uniform(-step*.3,step*.3)
            if inb(cx,cy) and interior[gy(cy),gx(cx)] and random.random()<0.4:
                s=span*random.uniform(0.006,0.012)
                disc(cx,cy,s,[CAN,(58,60,78)]); emit(cx,cy+s,cx,cy+s*1.6,TRUNK)
# recolor geometry
for x1,y1,z1,x2,y2,z2,c in B:
    if MODE=='kithicor':
        nc=(150,120,72) if c==(160,120,60) else ((70,150,205) if c==(0,0,255) else ((110,72,44) if c==(100,50,0) else ((90,80,64) if c==(0,0,0) else c)))
    else:
        nc=(70,150,205) if c==(0,0,255) else ((92,84,74) if c in ((150,100,0),(60,40,0)) else ((78,74,92) if c in ((0,0,0),(64,64,64)) else c))
    out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z1,x2,y2,z2,nc[0],nc[1],nc[2]))
open(f'{ZONE}_colored.txt','w',newline='').write('\r\n'.join(out)+'\r\n')
print('%s(%s) L=%d'%(ZONE,MODE,len(out)))
