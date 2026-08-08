"""Butcherblock colored base: flood-fill the OCEAN within its real bounds (shore + map
edge, no spill), warm gray ridges to rock, scatter LARGER peaks on land only (never in
water), draw walls on top of the water so they stay visible."""
import numpy as np, math, random
from scipy.ndimage import binary_dilation, label
def parse(path):
    out=[]
    for l in open(path,encoding='utf-8',errors='replace'):
        l=l.strip()
        if not l.startswith('L'): continue
        f=l[2:].split(','); out.append((float(f[0]),float(f[1]),float(f[2]),float(f[3]),float(f[4]),float(f[5]),(int(f[6]),int(f[7]),int(f[8]))))
    return out
B=parse('butcher.txt')
minx,maxx,miny,maxy=-4009,3283,-3172,3179
STONEC=(60,54,48); ROCK=(120,104,84); ROCK_D=(92,80,62); PATHC=(150,116,66)
WATER=(48,100,190); WFILL=(96,152,208); WRIP=(150,188,224)
z0=0.0; out=[]
def emit(x1,y1,x2,y2,c): out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z0,x2,y2,z0,c[0],c[1],c[2]))

# ---- OCEAN: flood-fill bounded by the shore, CLIPPED to the shore's y-extent ----
from scipy.ndimage import label as _label
CELL=20.0; gw=int((maxx-minx)/CELL)+2; gh=int((maxy-miny)/CELL)+2
gx=lambda x:int((x-minx)/CELL); gy=lambda y:int((y-miny)/CELL)
bl=[(s2[0],s2[1],s2[3],s2[4]) for s2 in B if s2[6]==(0,0,255)]
bx=[v for a,b,c,d in bl for v in (a,c)]; by=[v for a,b,c,d in bl for v in (b,d)]
ymin_b,ymax_b,sxmax=min(by),max(by),max(bx)
barrier=np.zeros((gh,gw),bool)
for x1,y1,x2,y2 in bl:
    n=int(max(abs(x2-x1),abs(y2-y1))/CELL)+1
    for i in range(n+1):
        t=i/n; ix=gx(x1+(x2-x1)*t); iy=gy(y1+(y2-y1)*t)
        if 0<=ix<gw and 0<=iy<gh: barrier[iy,ix]=True
barrier=binary_dilation(barrier,iterations=3)   # close small gaps so the flood can't leak into the land corners
lbl,_=_label(~barrier)
seeds=set()
for yy in (-1500,-800,0,800,1500):               # seed clearly INSIDE the ocean strip
    ix=gx((min(bx)+max(bx))/2); iy=gy(yy)
    if 0<=ix<gw and 0<=iy<gh and lbl[iy,ix]: seeds.add(lbl[iy,ix])
water=np.isin(lbl,list(seeds))                   # bounded by ALL blue shores (incl. horizontal top/bottom)
yg=(np.arange(gh)*CELL+miny)[:,None]; xg=(np.arange(gw)*CELL+minx)[None,:]
if water.sum() > 0.25*gw*gh: water=np.zeros_like(water)   # safety: never flood the whole map

# carve DOCK platforms out of the water and colour them wood (enclosed black regions in dock area)
DOCK=(122,86,50); DKX0,DKX1,DKY0,DKY1=-3320,-2560,-1560,-430
blk=np.zeros((gh,gw),bool)
for x1,y1,z1,x2,y2,z2,c in B:
    if c==(0,0,0):
        n=int(max(abs(x2-x1),abs(y2-y1))/CELL)+1
        for i in range(n+1):
            t=i/n; ix=gx(x1+(x2-x1)*t); iy=gy(y1+(y2-y1)*t)
            if 0<=ix<gw and 0<=iy<gh: blk[iy,ix]=True
inbox=(yg>=DKY0)&(yg<=DKY1)&(xg>=DKX0)&(xg<=DKX1)
lbl2,_=_label(~binary_dilation(blk,iterations=1) & inbox)
outside=set()
for iy in range(gh):
    for ix in range(gw):
        if inbox[iy,ix] and lbl2[iy,ix] and (iy in (gy(DKY0),gy(DKY1)) or ix in (gx(DKX0),gx(DKX1))):
            outside.add(lbl2[iy,ix])
dock=inbox & (~np.isin(lbl2,list(outside))) & (lbl2>0)   # enclosed pockets = dock platforms

# 1) water hatch FIRST (bottom layer), skip dock platforms
water_only = water & (~dock)
for iy in range(gh):
    ix=0
    while ix<gw:
        if water_only[iy,ix]:
            j=ix
            while j<gw and water_only[iy,j]: j+=1
            emit(minx+ix*CELL, miny+iy*CELL, minx+j*CELL, miny+iy*CELL, WFILL); ix=j
        else: ix+=1
random.seed(3); wi=np.argwhere(water_only)
if len(wi):
    for _ in range(30):
        iy,ix=wi[random.randrange(len(wi))]; rx=minx+ix*CELL; ry=miny+iy*CELL
        emit(rx-6,ry,rx-1,ry-2,WRIP); emit(rx-1,ry-2,rx+4,ry,WRIP)
# 1b) dock platforms coloured wood, on top of water
for iy in range(gh):
    ix=0
    while ix<gw:
        if dock[iy,ix]:
            j=ix
            while j<gw and dock[iy,j]: j+=1
            emit(minx+ix*CELL, miny+iy*CELL, minx+j*CELL, miny+iy*CELL, DOCK); ix=j
        else: ix+=1

# ---- ROCK: mesas + contour tendrils/enclosed shapes shaded as Butcherblock stone ----
gray=np.zeros((gh,gw),bool); blackc=np.zeros((gh,gw),bool); pathm=np.zeros((gh,gw),bool)
for x1,y1,_,x2,y2,_,c in B:
    tgt = gray if c==(128,128,128) else (pathm if c==(160,120,60) else (blackc if c==(0,0,0) else None))
    if tgt is None: continue
    n=int(max(abs(x2-x1),abs(y2-y1))/CELL)+1
    for i in range(n+1):
        t=i/n; ix=gx(x1+(x2-x1)*t); iy=gy(y1+(y2-y1)*t)
        if 0<=ix<gw and 0<=iy<gh: tgt[iy,ix]=True
grayd=binary_dilation(gray,iterations=1); blackd=binary_dilation(blackc,iterations=1)
lg,_=_label(~grayd); edg=set()
for ix in range(gw): edg.add(lg[0,ix]); edg.add(lg[gh-1,ix])
for iy in range(gh): edg.add(lg[iy,0]); edg.add(lg[iy,gw-1])
mesa_in=(~grayd)&(~np.isin(lg,list(edg)))                 # mesa interiors
bar=blackd|grayd|binary_dilation(water,iterations=2)
lf,_=_label(~bar); szs=np.bincount(lf.ravel()); szs[0]=0
valley=(lf==szs.argmax())                                  # big open lowland = forest valley
enclosed=(~bar)&(~valley)                                  # tendrils + enclosed shapes = rock
rock=(mesa_in|enclosed|gray) & (~water)
clearm=((xg>minx+430)&(xg<maxx-430)&(yg>miny+330)&(yg<maxy-330))
# angular hatch (denser + cross-strokes on mesa interiors = blocky "stone teeth")
random.seed(4)
for iy in range(0,gh,2):
    ix=0
    while ix<gw:
        if rock[iy,ix] and clearm[iy,ix]:
            j=ix
            while j<gw and rock[iy,j] and clearm[iy,j]: j+=1
            yy=miny+iy*CELL; xx=minx+ix*CELL
            while xx<minx+j*CELL:
                dense = mesa_in[iy,ix]
                if dense or random.random()<0.55:
                    emit(xx,yy,xx+CELL*1.25,yy+CELL*1.25, ROCK if random.random()<0.6 else ROCK_D)
                    if dense and random.random()<0.5:
                        emit(xx+CELL*0.9,yy,xx+CELL*0.9-CELL*0.55,yy+CELL*0.55, ROCK_D)   # cross facet
                xx+=CELL*(1.5 if dense else 2.3)
            ix=j
        else: ix+=1

# ---- 2) geometry ON TOP (walls stay visible over water/rock) ----
for x1,y1,z1,x2,y2,z2,c in B:
    if   c==(0,0,0): nc=STONEC
    elif c==(128,128,128): nc=ROCK_D
    elif c==(160,120,60): nc=PATHC
    elif c==(100,50,0): nc=ROCK_D
    elif c==(0,0,255): nc=WATER
    else: nc=c
    out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z1,x2,y2,z2,nc[0],nc[1],nc[2]))

# ---- 3) FOREST — trees ONLY in the valleys (never on rock) ----
TREE=(58,112,62); TREE_D=(42,88,48)
treeok = valley & clearm & (~binary_dilation(rock,iterations=1)) & (~binary_dilation(pathm,iterations=1)) & (~binary_dilation(water,iterations=2))
def tree(cx,cy,s,seed):
    r=random.Random(seed); rr=s*(0.55+0.3*r.random()); pts=[]
    for a in range(8):
        ang=a/8*2*math.pi; rad=rr*(0.8+0.25*r.random()); pts.append((cx+math.cos(ang)*rad, cy+math.sin(ang)*rad))
    for k in range(len(pts)):
        emit(pts[k][0],pts[k][1],pts[(k+1)%len(pts)][0],pts[(k+1)%len(pts)][1], TREE if seed%3 else TREE_D)
    emit(cx,cy+rr*0.7,cx,cy+rr*1.15,TREE_D)
random.seed(11); SP=140; placed=0; y=miny+330
while y<maxy-330:
    x=minx+430
    while x<maxx-430:
        jx=x+random.uniform(-46,46); jy=y+random.uniform(-46,46); ix,iy=gx(jx),gy(jy)
        if 0<=ix<gw and 0<=iy<gh and treeok[iy,ix]:
            tree(jx,jy,random.uniform(38,60),placed); placed+=1
        x+=SP
    y+=SP
open('butcher_colored.txt','w',newline='').write('\r\n'.join(out)+'\r\n')
print('rock cells: %d  valley trees: %d  L=%d'%(int(rock.sum()),placed,len(out)))
