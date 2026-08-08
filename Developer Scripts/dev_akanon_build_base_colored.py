"""Ak'Anon ROMULAN-styled base: dark cavern hatch around the city, dark blue-green water
flood-filled (flows north around the Rogue/Palace island), grey-green metalwork, green
gem accents. Palette: greens/greys/blacks."""
import numpy as np, math, random
from scipy.ndimage import binary_dilation, label as _label
def parse(path):
    out=[]
    for l in open(path,encoding='utf-8',errors='replace'):
        l=l.strip()
        if not l.startswith('L'): continue
        f=l[2:].split(','); out.append((float(f[0]),float(f[1]),float(f[2]),float(f[3]),float(f[4]),float(f[5]),(int(f[6]),int(f[7]),int(f[8]))))
    return out
B=parse('akanon.txt')
minx,maxx,miny,maxy=-210,1050,-2255,84
# --- palette ---
CAVERN=(72,86,76); CAVERN2=(52,64,56)        # cavern rock hatch
WALL=(58,70,64); WALL_D=(40,50,45)            # metalwork
WFILL=(26,74,82); WFILL2=(34,92,98); WOUT=(46,128,120)   # dark blue-green water
GEM=(46,180,96); GOLDGEM=(120,180,70)
z0=-1.0; out=[]
def emit(x1,y1,x2,y2,c): out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z0,x2,y2,z0,c[0],c[1],c[2]))

CELL=14.0; gw=int((maxx-minx)/CELL)+2; gh=int((maxy-miny)/CELL)+2
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
xg=(np.arange(gw)*CELL+minx)[None,:]; yg=(np.arange(gh)*CELL+miny)[:,None]

# ---- WATER: flood-fill enclosed by the green outline, minus structures (islands show) ----
green_bar=raster(lambda c:c==(85,184,20),dil=1)
freeG=~green_bar; lblG,_=_label(freeG)
edge=set()
for ix in range(gw): edge.add(lblG[0,ix]); edge.add(lblG[gh-1,ix])
for iy in range(gh): edge.add(lblG[iy,0]); edge.add(lblG[iy,gw-1])
water=freeG & (~np.isin(lblG,list(edge)))          # enclosed by green
black_bar=raster(lambda c:c==(0,0,0),dil=1)
water_hatch = water & (~black_bar)                  # keep structures dry

# ---- CAVERN: hatch the rock OUTSIDE the city footprint (within the content area) ----
allgeom=raster(lambda c:True,dil=0)
city=binary_dilation(allgeom,iterations=10)          # city footprint blob
PADIN=170
cav=( (xg>minx+PADIN)&(xg<maxx-PADIN)&(yg>miny+PADIN)&(yg<maxy-PADIN) ) & (~city)

# 1) cavern hatch FIRST (background), diagonal dark strokes
random.seed(5)
for iy in range(0,gh,2):
    ix=0
    while ix<gw:
        if cav[iy,ix]:
            j=ix
            while j<gw and cav[iy,j]: j+=1
            # diagonal hatch across the run
            x0=minx+ix*CELL; x1=minx+j*CELL; yy=miny+iy*CELL
            xx=x0
            while xx<x1:
                emit(xx,yy,xx+CELL*1.6,yy+CELL*1.6, CAVERN if (int(xx)//40)%2 else CAVERN2); xx+=CELL*2.4
            ix=j
        else: ix+=1

# 2) water fill (dark blue-green) on top of cavern
for iy in range(gh):
    ix=0
    while ix<gw:
        if water_hatch[iy,ix]:
            j=ix
            while j<gw and water_hatch[iy,j]: j+=1
            emit(minx+ix*CELL, miny+iy*CELL, minx+j*CELL, miny+iy*CELL, WFILL if iy%2 else WFILL2); ix=j
        else: ix+=1

# ---- 3) geometry ON TOP: recolor to Romulan metalwork ----
for x1,y1,z1,x2,y2,z2,c in B:
    if   c==(0,0,0): nc=WALL
    elif c==(85,184,20): nc=WOUT             # water outline -> teal
    elif c==(255,215,0): nc=GOLDGEM          # gold forges -> green-gold
    else: nc=c
    out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z1,x2,y2,z2,nc[0],nc[1],nc[2]))

# ---- 4) green GEM accents: small diamonds scattered on structure clusters ----
random.seed(9); occ=raster(lambda c:c==(0,0,0),dil=0); wi=np.argwhere(occ & (~binary_dilation(water,iterations=2)))
def gem(cx,cy,s):
    emit(cx,cy-s,cx+s,cy,GEM); emit(cx+s,cy,cx,cy+s,GEM); emit(cx,cy+s,cx-s,cy,GEM); emit(cx-s,cy,cx,cy-s,GEM)
placed=0
if len(wi):
    for _ in range(46):
        iy,ix=wi[random.randrange(len(wi))]; gem(minx+ix*CELL,miny+iy*CELL,7); placed+=1
open('akanon_colored.txt','w',newline='').write('\r\n'.join(out)+'\r\n')
print('water cells=%d cavern hatch + %d gems  L=%d'%(int(water_hatch.sum()),placed,len(out)))
