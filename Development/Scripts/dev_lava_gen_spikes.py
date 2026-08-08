import numpy as np, random
from scipy.ndimage import binary_dilation, binary_fill_holes
def parse(path):
    out=[]
    for l in open(path,encoding='utf-8',errors='replace'):
        l=l.strip()
        if l.startswith('L'):
            f=l[2:].split(','); out.append((float(f[0]),float(f[1]),float(f[3]),float(f[4]),(int(f[6]),int(f[7]),int(f[8]))))
    return out
B=parse('lavastorm.txt')
xs=[v for a,b,c,d,e in B for v in (a,c)]; ys=[v for a,b,c,d,e in B for v in (b,d)]
minx,maxx,miny,maxy=min(xs),max(xs),min(ys),max(ys)
SPK1=(96,84,74); SPK2=(70,60,52); VROCK=(112,98,86); STEAM=(176,178,184)
z0=-1.0; out=[]
def emit(x1,y1,x2,y2,c): out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z0,x2,y2,z0,c[0],c[1],c[2]))
CELL=10.0; gw=int((maxx-minx)/CELL)+2; gh=int((maxy-miny)/CELL)+2
gx=lambda x:int((x-minx)/CELL); gy=lambda y:int((y-miny)/CELL)
def raster(cond,dil=0):
    m=np.zeros((gh,gw),bool)
    for a,b,c,d,e in B:
        if cond(e):
            n=int(max(abs(c-a),abs(d-b))/CELL)+1
            for i in range(n+1):
                t=i/n; ix=gx(a+(c-a)*t); iy=gy(b+(d-b)*t)
                if 0<=ix<gw and 0<=iy<gh: m[iy,ix]=True
    return binary_dilation(m,iterations=dil) if dil else m
black=raster(lambda e:e==(0,0,0)); red=raster(lambda e:e==(255,0,0))
interior=binary_fill_holes(binary_dilation(black,iterations=3))
if interior.sum()<gw*gh*0.2: interior=np.ones((gh,gw),bool)
lava=binary_fill_holes(binary_dilation(red,iterations=3)) & interior   # avoid lava a bit wider
rock=interior & (~lava)
xg=(np.arange(gw)*CELL+minx)[None,:]; yg=(np.arange(gh)*CELL+miny)[:,None]
PAD=int(max(maxx-minx,maxy-miny)*0.05); inb=(xg>minx+PAD)&(xg<maxx-PAD)&(yg>miny+PAD)&(yg<maxy-PAD)
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
        if rock[iy,ix] and inb[iy,ix] and random.random()<0.25:
            cx=minx+ix*CELL+random.uniform(-12,12); cy=miny+iy*CELL+random.uniform(-12,12)
            if random.random()<0.68: spike(cx,cy,random.uniform(16,30),ix*7+iy); ns+=1
            else: vent(cx,cy,random.uniform(16,26)); nv+=1
open('spikes_vents.txt','w',newline='').write('\r\n'.join(out)+'\r\n')
print('spikes=%d vents=%d L=%d'%(ns,nv,len(out)))
