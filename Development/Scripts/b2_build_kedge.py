import numpy as np
from scipy.ndimage import binary_dilation, binary_fill_holes, binary_erosion
def parse(p):
    o=[]
    for l in open(p,encoding='utf-8',errors='replace'):
        l=l.strip()
        if l.startswith('L'):
            f=l[2:].split(','); o.append((float(f[0]),float(f[1]),float(f[2]),float(f[3]),float(f[4]),float(f[5]),(int(f[6]),int(f[7]),int(f[8]))))
    return o
B=parse('kedge.txt')
xs=[v for s in B for v in (s[0],s[3])]; ys=[v for s in B for v in (s[1],s[4])]
minx,maxx,miny,maxy=min(xs),max(xs),min(ys),max(ys)
WFILL=(70,150,205); WFILL2=(86,164,214); WEDGE=(40,92,158); WALL=(70,110,120); CORAL=(150,120,90)
z0=-1.0; out=[]
def emit(x1,y1,x2,y2,c): out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z0,x2,y2,z0,c[0],c[1],c[2]))
span=max(maxx-minx,maxy-miny); CELL=span/300.0
gw=int((maxx-minx)/CELL)+2; gh=int((maxy-miny)/CELL)+2
gx=lambda x:int((x-minx)/CELL); gy=lambda y:int((y-miny)/CELL)
m=np.zeros((gh,gw),bool)
for s in B:
    x1,y1,x2,y2=s[0],s[1],s[3],s[4]; n=int(max(abs(x2-x1),abs(y2-y1))/CELL)+1
    for i in range(n+1):
        t=i/n; ix=gx(x1+(x2-x1)*t); iy=gy(y1+(y2-y1)*t)
        if 0<=ix<gw and 0<=iy<gh: m[iy,ix]=True
flood=binary_fill_holes(binary_dilation(m,iterations=3))  # whole zone is underwater
PAD=int(span*0.04)
xg=(np.arange(gw)*CELL+minx)[None,:]; yg=(np.arange(gh)*CELL+miny)[:,None]
inb=(xg>minx+PAD)&(xg<maxx-PAD)&(yg>miny+PAD)&(yg<maxy-PAD)
for iy in range(gh):
    ix=0
    while ix<gw:
        if flood[iy,ix] and inb[iy,ix]:
            j=ix
            while j<gw and flood[iy,j]: j+=1
            emit(minx+ix*CELL,miny+iy*CELL,minx+j*CELL,miny+iy*CELL, WFILL if iy%2 else WFILL2); ix=j
        else: ix+=1
for x1,y1,z1,x2,y2,z2,c in B:
    nc=WALL if c==(0,0,0) else c
    out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z1,x2,y2,z2,nc[0],nc[1],nc[2]))
open('kedge_colored.txt','w',newline='').write('\r\n'.join(out)+'\r\n')
print('kedge underwater L=%d'%len(out))
