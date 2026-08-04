"""Blackburrow colored base: recolor geometry BY FLOOR (3 stacked Z-levels) +
shade the water areas (extracted from the wiki floor maps) with a hatched blue fill.
Replaces blackburrow.txt (same geometry, themed colors + water)."""
import numpy as np, water as WT

P=np.load('geo.npy'); mz=(P[:,2]+P[:,5])/2
b1,b2=[float(x) for x in open('floorcuts.txt').read().split()]
real_mask=mz<120
minx,maxx,miny,maxy=-489,397,-349,254

# ---- floor theme colors (grade darker as you descend the gnoll warren) ----
F1=(170,132,58)     # top ravine  - sunlit ochre/sandstone
F2=(152,86,46)      # mid caves    - torchlit rust/terracotta
F3=(86,112,148)     # deep dens    - cold slate-blue (near the lake)
JUNK_Z=120          # drop the floating z~605 artifact lines

WFILL=(58,150,215)  # water body
WEDGE=(30,78,150)   # water outline
WRIP =(120,180,225) # ripples

def floor_of(z): return 'f3' if z<b1 else ('f2' if z<b2 else 'f1')
COL={'f1':F1,'f2':F2,'f3':F3}
FZ={'f1':0.0,'f2':-50.0,'f3':-142.0}

out=[]
def L(x1,y1,x2,y2,c,z): out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z,x2,y2,z,c[0],c[1],c[2]))

# 1) recolor real geometry by floor (drop floating junk)
for r in P:
    zz=(r[2]+r[5])/2
    if zz>=JUNK_Z: continue
    c=COL[floor_of(zz)]
    out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(r[0],r[1],r[2],r[3],r[4],r[5],c[0],c[1],c[2]))

# ---- rasterizer helpers (native grid) ----
CELL=3.0
gw=int((maxx-minx)/CELL)+1; gh=int((maxy-miny)/CELL)+1
def gx(x): return int((x-minx)/CELL)
def gy(y): return int((y-miny)/CELL)

def rasterize_lines(lines):
    m=np.zeros((gh,gw),bool)
    for x1,y1,x2,y2 in lines:
        n=int(max(abs(x2-x1),abs(y2-y1))/CELL)+1
        for i in range(n+1):
            t=i/n; xx=x1+(x2-x1)*t; yy=y1+(y2-y1)*t
            ix,iy=gx(xx),gy(yy)
            if 0<=ix<gw and 0<=iy<gh: m[iy,ix]=True
    return m

def dilate(m,k):
    from scipy.ndimage import binary_dilation
    return binary_dilation(m,iterations=k)

# 2) water per floor -> clip to footprint -> hatch fill
def add_water(fname,floor):
    z=FZ[floor]
    zr=(P[:,2]+P[:,5])/2
    if floor=='f1': fg=P[real_mask & (zr>=b2)]
    elif floor=='f2': fg=P[real_mask & (zr>=b1) & (zr<b2)]
    else: fg=P[real_mask & (zr<b1)]
    foot=dilate(rasterize_lines(fg[:,:4]),7)   # ~21u dilation around floor geometry
    wp=WT.native_water_points(fname)
    wp=wp[(wp[:,0]>=minx)&(wp[:,0]<=maxx)&(wp[:,1]>=miny)&(wp[:,1]<=maxy)]
    wm=np.zeros((gh,gw),bool)
    for x,y in wp:
        ix,iy=gx(x),gy(y)
        if foot[iy,ix]: wm[iy,ix]=True
    from scipy.ndimage import binary_closing,label
    wm=binary_closing(wm,iterations=2)
    lab,nlab=label(wm)
    for k in range(1,nlab+1):
        if (lab==k).sum()<12: wm[lab==k]=False
    return fill_water_mask(wm, z, floor)

def fill_water_mask(wm, z, seed):
    # hatch fill: horizontal runs every HSTEP native units
    HSTEP=5
    for iy in range(0,gh, max(1,int(HSTEP/CELL))):
        row=wm[iy]; ix=0
        while ix<gw:
            if row[ix]:
                j=ix
                while j<gw and row[j]: j+=1
                x_a=minx+ix*CELL; x_b=minx+(j-1)*CELL; yy=miny+iy*CELL
                if x_b-x_a>=2: L(x_a,yy,x_b,yy,WFILL,z)
                ix=j
            else: ix+=1
    edge=wm & ~(np.roll(wm,1,0)&np.roll(wm,-1,0)&np.roll(wm,1,1)&np.roll(wm,-1,1))
    ys,xs=np.where(edge)
    for iy,ix in zip(ys,xs):
        xx=minx+ix*CELL; yy=miny+iy*CELL
        L(xx-1.2,yy,xx+1.2,yy,WEDGE,z)
    interior=wm & (np.roll(wm,3,1)&np.roll(wm,-3,1)&np.roll(wm,3,0)&np.roll(wm,-3,0))
    ys,xs=np.where(interior)
    if len(xs):
        import random; random.seed(hash(seed)%99)
        idx=random.sample(range(len(xs)),min(len(xs)//40+3,40,len(xs)))
        for i in idx:
            xx=minx+xs[i]*CELL; yy=miny+ys[i]*CELL
            L(xx-5,yy,xx-1,yy-2,WRIP,z); L(xx-1,yy-2,xx+3,yy,WRIP,z); L(xx+3,yy,xx+7,yy-2,WRIP,z)
    return int(wm.sum())

def stamp_disc(mask,cx,cy,rad):
    r=int(rad/CELL)
    for dy in range(-r,r+1):
        for dx in range(-r,r+1):
            if (dx*CELL)**2+(dy*CELL)**2<=rad*rad:
                ix=gx(cx)+dx; iy=gy(cy)+dy
                if 0<=ix<gw and 0<=iy<gh: mask[iy,ix]=True

def add_river_f1():
    # The ravine river on Floor 1, traced from in-game /loc points the player
    # walked along it (native coords == /loc). Waterfall at the north (high-y) end.
    z=0.0
    center=[(6,-52),(13,-26),(21,6),(29,42),(33,64),(35,82)]     # river centerline
    wm=np.zeros((gh,gw),bool)
    for (x1,y1),(x2,y2) in zip(center,center[1:]):
        n=int(max(abs(x2-x1),abs(y2-y1))/CELL)+1
        for i in range(n+1):
            t=i/n; stamp_disc(wm, x1+(x2-x1)*t, y1+(y2-y1)*t, 8.5)
    stamp_disc(wm, 35, 86, 15)                                    # plunge pool at the falls
    ncells=fill_water_mask(wm, z, 'f1river')
    # waterfall: vertical falling-water streaks above the plunge pool
    for sx in (27,31,35,39,43):
        L(sx, 84, sx, 108, WFILL, z)
        L(sx-1, 90, sx-1, 104, WRIP, z)
    L(24, 84, 46, 84, WEDGE, z)                                   # lip of the falls
    return ncells

for fl,fn in [('f2','f2'),('f3','f3')]:
    n=add_water(fn,fl); print('water cells %s: %d'%(fl,n))
print('water cells f1-river: %d'%add_river_f1())

open('blackburrow_colored.txt','w',newline='').write('\r\n'.join(out)+'\r\n')
print('wrote blackburrow_colored.txt  L=%d'%len(out))
