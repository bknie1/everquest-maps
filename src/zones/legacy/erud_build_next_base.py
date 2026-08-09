"""Erudin (erudnext) v4 — UNIFIED flat classification: every cell is exactly one of
{water, dock, grass(courtyard), rock(empty), structure}. Water = NOT land (inside the blue
coast, around the L-dock). Then each class is extracted to its layer. No overlaps."""
import numpy as np, math, random
from scipy.ndimage import binary_dilation, label as _label, binary_fill_holes
def parse(path):
    out=[]
    for l in open(path,encoding='utf-8',errors='replace'):
        l=l.strip()
        if l.startswith('L'):
            f=l[2:].split(','); out.append((float(f[0]),float(f[1]),float(f[2]),float(f[3]),float(f[4]),float(f[5]),(int(f[6]),int(f[7]),int(f[8]))))
    return out
B=parse('erudnext.txt')
minx,maxx,miny,maxy=-128,2051,-812,1599
WFILL=(150,196,224); WFILL2=(128,180,214); WOUT=(70,140,196)
CLIFF=(168,150,120); CLIFF2=(150,132,104)
GRASS=(126,168,98); GRASS2=(108,150,82)
MARBLE=(120,132,150); DOCK=(150,110,64); PATHB=(120,172,212); TELE=(86,196,214)
z0=-1.0; out=[]
def emit(x1,y1,x2,y2,c): out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z0,x2,y2,z0,c[0],c[1],c[2]))
CELL=10.0; gw=int((maxx-minx)/CELL)+2; gh=int((maxy-miny)/CELL)+2
gx=lambda x:int((x-minx)/CELL); gy=lambda y:int((y-miny)/CELL)
xg=(np.arange(gw)*CELL+minx)[None,:]; yg=(np.arange(gh)*CELL+miny)[:,None]
def raster(cond,dil=0):
    m=np.zeros((gh,gw),bool)
    for s in B:
        if cond(s[6]):
            x1,y1,x2,y2=s[0],s[1],s[3],s[4]; n=int(max(abs(x2-x1),abs(y2-y1))/CELL)+1
            for i in range(n+1):
                t=i/n; ix=gx(x1+(x2-x1)*t); iy=gy(y1+(y2-y1)*t)
                if 0<=ix<gw and 0<=iy<gh: m[iy,ix]=True
    return binary_dilation(m,iterations=dil) if dil else m
blue2=raster(lambda c:c==(0,0,255),dil=2)
brown0=raster(lambda c:c==(100,50,0),dil=0); brownd=raster(lambda c:c==(100,50,0),dil=1)
black0=raster(lambda c:c==(0,0,0),dil=0); blackthin=raster(lambda c:c==(0,0,0),dil=1)
tan0=raster(lambda c:c==(150,100,0),dil=1)
# --- LAND flood (from land edges: left + bottom), bounded by the blue coast ---
comp,_=_label(~blue2)
land_labs=set()
for iy in range(gh):
    for ix in (0,1): 
        if comp[iy,ix]: land_labs.add(comp[iy,ix])
for ix in range(gw):
    for iy in (gh-1,gh-2):
        if comp[iy,ix]: land_labs.add(comp[iy,ix])
land=np.isin(comp,list(land_labs))
# --- single flat classification ---
dockreg = binary_fill_holes(binary_dilation(brown0,iterations=1))   # solid L-dock (interior included)
water = (~land) & (~blue2) & (~dockreg) & (~blackthin)     # ocean + harbor, around the solid L-dock
cityfoot = binary_fill_holes(binary_dilation(black0,iterations=7))
openland = land & (~blackthin) & (~tan0) & (~brownd)
grass = openland & cityfoot & (~water)
PADIN=150
rock  = openland & (~cityfoot) & (~water) & (xg>minx+PADIN)&(xg<maxx-PADIN)&(yg>miny+PADIN)&(yg<maxy-PADIN)
# --- emit layers (mutually exclusive) ---
def fill(mask, c1, c2):
    for iy in range(gh):
        ix=0
        while ix<gw:
            if mask[iy,ix]:
                j=ix
                while j<gw and mask[iy,j]: j+=1
                emit(minx+ix*CELL,miny+iy*CELL,minx+j*CELL,miny+iy*CELL, c1 if iy%2 else c2); ix=j
            else: ix+=1
fill(water, WFILL, WFILL2)
fill(dockreg & (~blackthin), DOCK, DOCK)      # solid L-dock (no water lines inside)
random.seed(3)                                   # rock hatch (diagonal)
for iy in range(0,gh,2):
    ix=0
    while ix<gw:
        if rock[iy,ix]:
            j=ix
            while j<gw and rock[iy,j]: j+=1
            xx=minx+ix*CELL
            while xx<minx+j*CELL:
                if random.random()<0.7: emit(xx,miny+iy*CELL,xx+CELL*1.7,miny+iy*CELL+CELL*1.7, CLIFF if random.random()<0.6 else CLIFF2)
                xx+=CELL*2.4
            ix=j
        else: ix+=1
fill(grass, GRASS, GRASS2)
# --- geometry lines on top ---
for x1,y1,z1,x2,y2,z2,c in B:
    if   c==(0,0,255): nc=WOUT
    elif c==(150,100,0): nc=PATHB
    elif c==(100,50,0): nc=DOCK
    elif c==(0,0,0): nc=MARBLE
    else: nc=c
    out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z1,x2,y2,z2,nc[0],nc[1],nc[2]))
# teleport-pad glow rings
pad=raster(lambda c:c==(150,100,0),dil=0); lp,npad=_label(binary_dilation(pad,iterations=2))
for k in range(1,npad+1):
    ys,xs=np.where(lp==k)
    if len(xs)<14: continue
    cx=minx+xs.mean()*CELL; cy=miny+ys.mean()*CELL; r=max(30, CELL*max(xs.max()-xs.min(),ys.max()-ys.min())*0.55)
    pts=[(cx+math.cos(a*math.pi/8)*r, cy+math.sin(a*math.pi/8)*r) for a in range(17)]
    for i in range(16): emit(pts[i][0],pts[i][1],pts[i+1][0],pts[i+1][1], TELE)
open('erudnext_colored.txt','w',newline='').write('\r\n'.join(out)+'\r\n')
print('water=%d grass=%d rock=%d L=%d'%(int(water.sum()),int(grass.sum()),int(rock.sum()),len(out)))
