"""Butcherblock (dwarf-inspired) POI sketches for margin cells."""
import math
STONE=(96,90,80); STONE_D=(70,66,58); IRON=(90,96,108); BEARD=(150,120,70); SKIN=(150,110,80)
WOOD=(120,84,48); SAIL=(180,172,150); WATER=(70,120,180); GOB=(90,110,70); FEATHER=(120,100,70)
def _poly(cv,pts,c,close=False):
    P=list(pts)+([list(pts)[0]] if close else [])
    for i in range(len(P)-1): cv.add(P[i][0],P[i][1],P[i+1][0],P[i+1][1],c)

def dwarf(cv,cx,cy,s=100):
    # helmet dome
    _poly(cv,[(cx-s*0.24,cy-s*0.34),(cx-s*0.2,cy-s*0.5),(cx+s*0.2,cy-s*0.5),(cx+s*0.24,cy-s*0.34)],IRON)
    cv.add(cx-s*0.26,cy-s*0.34,cx+s*0.26,cy-s*0.34,IRON)         # helmet rim
    cv.add(cx,cy-s*0.5,cx,cy-s*0.58,IRON)                         # spike
    # face
    cv.add(cx-s*0.16,cy-s*0.3,cx+s*0.16,cy-s*0.3,SKIN)           # brow
    cv.add(cx-s*0.08,cy-s*0.24,cx-s*0.04,cy-s*0.24,STONE_D); cv.add(cx+s*0.04,cy-s*0.24,cx+s*0.08,cy-s*0.24,STONE_D) # eyes
    # big beard (triangular, braided)
    _poly(cv,[(cx-s*0.22,cy-s*0.28),(cx-s*0.28,cy+s*0.12),(cx,cy+s*0.34),(cx+s*0.28,cy+s*0.12),(cx+s*0.22,cy-s*0.28)],BEARD,close=True)
    cv.add(cx-s*0.1,cy-s*0.14,cx-s*0.12,cy+s*0.18,BEARD); cv.add(cx+s*0.1,cy-s*0.14,cx+s*0.12,cy+s*0.18,BEARD)  # braids
    cv.add(cx,cy-s*0.16,cx,cy+s*0.24,BEARD)
    # shoulders + axe
    cv.add(cx-s*0.3,cy+s*0.14,cx+s*0.3,cy+s*0.14,STONE_D)
    cv.add(cx+s*0.34,cy-s*0.4,cx+s*0.34,cy+s*0.2,WOOD)           # axe haft
    _poly(cv,[(cx+s*0.34,cy-s*0.4),(cx+s*0.5,cy-s*0.34),(cx+s*0.5,cy-s*0.16),(cx+s*0.34,cy-s*0.14)],IRON,close=True)  # axe head

def chessboard(cv,cx,cy,s=110):
    # board in slight perspective (trapezoid), 4x4 with alternating hatched squares
    tl=(cx-s*0.34,cy-s*0.12); tr=(cx+s*0.34,cy-s*0.12); bl=(cx-s*0.5,cy+s*0.3); br=(cx+s*0.5,cy+s*0.3)
    _poly(cv,[tl,tr,br,bl],STONE,close=True)
    for i in range(1,4):
        t=i/4
        cv.add(tl[0]+(tr[0]-tl[0])*t, tl[1], bl[0]+(br[0]-bl[0])*t, bl[1], STONE)  # verticals
        ly=tl[1]+(bl[1]-tl[1])*t; lx0=tl[0]+(bl[0]-tl[0])*t; lx1=tr[0]+(br[0]-tr[0])*t
        cv.add(lx0,ly,lx1,ly,STONE)                                                # horizontals
    # hatch a few squares (checker)
    for (a,b) in [(0,0),(1,1),(2,0),(0,2),(2,2),(3,1),(1,3),(3,3)]:
        u0=(a+0.15)/4; u1=(a+0.85)/4; v0=(b+0.2)/4; v1=(b+0.8)/4
        def P(u,v):
            topx=tl[0]+(tr[0]-tl[0])*u; botx=bl[0]+(br[0]-bl[0])*u
            x=topx+(botx-topx)*v; y=tl[1]+(bl[1]-tl[1])*v; return (x,y)
        for q in range(3):
            f=q/2; cv.add(*P(u0+ (u1-u0)*f,v0),*P(u0,v0+(v1-v0)*(1-f)),STONE_D)      # diagonal hatch
    # a king piece
    px,py=cx+s*0.05,cy-s*0.12
    cv.add(px,py,px,py-s*0.28,IRON); _poly(cv,[(px-s*0.08,py),(px-s*0.06,py-s*0.28),(px+s*0.06,py-s*0.28),(px+s*0.08,py)],IRON,close=True)
    cv.add(px-s*0.05,py-s*0.34,px+s*0.05,py-s*0.34,IRON); cv.add(px,py-s*0.3,px,py-s*0.4,IRON)  # crown cross

def boat(cv,cx,cy,s=110):
    _poly(cv,[(cx-s*0.4,cy+s*0.1),(cx-s*0.28,cy+s*0.3),(cx+s*0.28,cy+s*0.3),(cx+s*0.4,cy+s*0.1)],WOOD,close=True)  # hull
    cv.add(cx-s*0.4,cy+s*0.1,cx+s*0.4,cy+s*0.1,WOOD)             # deck
    cv.add(cx,cy+s*0.1,cx,cy-s*0.42,WOOD)                         # mast
    _poly(cv,[(cx,cy-s*0.4),(cx+s*0.26,cy-s*0.1),(cx,cy-s*0.06)],SAIL,close=True)  # sail
    _poly(cv,[(cx,cy-s*0.36),(cx-s*0.2,cy-s*0.1),(cx,cy-s*0.08)],SAIL,close=True)
    for wx in (-0.5,-0.2,0.1,0.4):                                # water ripples
        cv.add(cx+s*wx,cy+s*0.4,cx+s*wx+s*0.08,cy+s*0.36,WATER); cv.add(cx+s*wx+s*0.08,cy+s*0.36,cx+s*wx+s*0.16,cy+s*0.4,WATER)

def stone_ring(cv,cx,cy,s=110):
    # ellipse of standing stones with lintels
    import math
    for i in range(7):
        a=math.pi*(0.1+0.8*i/6)  # front arc
        ex=cx+math.cos(a)*s*0.44; ey=cy+s*0.18-math.sin(a)*s*0.16
        _poly(cv,[(ex-s*0.05,ey),(ex-s*0.05,ey-s*0.3),(ex+s*0.05,ey-s*0.3),(ex+s*0.05,ey)],STONE,close=True)  # stone
    # back stones (smaller)
    for i in range(5):
        a=math.pi*(0.15+0.7*i/4)
        ex=cx+math.cos(a)*s*0.38; ey=cy-s*0.16-math.sin(a)*s*0.1
        cv.add(ex-s*0.04,ey,ex-s*0.04,ey-s*0.2,STONE_D); cv.add(ex+s*0.04,ey,ex+s*0.04,ey-s*0.2,STONE_D)
        cv.add(ex-s*0.04,ey-s*0.2,ex+s*0.04,ey-s*0.2,STONE_D)

def dwarf_statue(cv,cx,cy,s=110):
    # pedestal
    _poly(cv,[(cx-s*0.3,cy+s*0.4),(cx-s*0.24,cy+s*0.18),(cx+s*0.24,cy+s*0.18),(cx+s*0.3,cy+s*0.4)],STONE_D,close=True)
    # carved dwarf head/bust
    _poly(cv,[(cx-s*0.22,cy+s*0.18),(cx-s*0.26,cy-s*0.18),(cx-s*0.12,cy-s*0.34),(cx+s*0.12,cy-s*0.34),(cx+s*0.26,cy-s*0.18),(cx+s*0.22,cy+s*0.18)],STONE,close=True)
    cv.add(cx-s*0.12,cy-s*0.4,cx+s*0.12,cy-s*0.4,STONE)          # helmet
    cv.add(cx-s*0.14,cy-s*0.16,cx-s*0.05,cy-s*0.16,STONE_D); cv.add(cx+s*0.05,cy-s*0.16,cx+s*0.14,cy-s*0.16,STONE_D)  # eyes
    _poly(cv,[(cx-s*0.16,cy-s*0.06),(cx,cy+s*0.16),(cx+s*0.16,cy-s*0.06)],STONE_D)  # beard
    cv.add(cx,cy-s*0.1,cx,cy+s*0.06,STONE_D)                      # nose

def goblin(cv,cx,cy,s=90):
    _poly(cv,[(cx-s*0.14,cy-s*0.1),(cx-s*0.2,cy+s*0.08),(cx,cy+s*0.16),(cx+s*0.2,cy+s*0.08),(cx+s*0.14,cy-s*0.1)],GOB,close=True)  # head
    _poly(cv,[(cx-s*0.14,cy-s*0.06),(cx-s*0.34,cy-s*0.22),(cx-s*0.06,cy-s*0.12)],GOB)  # ear L
    _poly(cv,[(cx+s*0.14,cy-s*0.06),(cx+s*0.34,cy-s*0.22),(cx+s*0.06,cy-s*0.12)],GOB)  # ear R
    cv.add(cx-s*0.08,cy-s*0.02,cx-s*0.03,cy-s*0.02,STONE_D); cv.add(cx+s*0.03,cy-s*0.02,cx+s*0.08,cy-s*0.02,STONE_D)  # eyes
    cv.add(cx,cy+s*0.16,cx,cy+s*0.42,GOB)                         # body
    cv.add(cx+s*0.16,cy-s*0.2,cx+s*0.16,cy+s*0.4,WOOD)           # spear
    cv.add(cx+s*0.16,cy-s*0.2,cx+s*0.1,cy-s*0.3,IRON); cv.add(cx+s*0.16,cy-s*0.2,cx+s*0.22,cy-s*0.3,IRON)

def aviak(cv,cx,cy,s=95):
    _poly(cv,[(cx-s*0.1,cy-s*0.16),(cx-s*0.12,cy),(cx+s*0.12,cy),(cx+s*0.1,cy-s*0.16)],FEATHER,close=True)  # head
    _poly(cv,[(cx+s*0.1,cy-s*0.08),(cx+s*0.26,cy-s*0.04),(cx+s*0.1,cy)],(150,120,40))  # beak
    cv.add(cx-s*0.04,cy-s*0.1,cx-s*0.01,cy-s*0.1,STONE_D); cv.add(cx+s*0.02,cy-s*0.1,cx+s*0.05,cy-s*0.1,STONE_D)
    cv.add(cx,cy,cx,cy+s*0.3,FEATHER)                             # body
    _poly(cv,[(cx,cy+s*0.04),(cx-s*0.34,cy-s*0.06),(cx-s*0.28,cy+s*0.16),(cx,cy+s*0.14)],FEATHER,close=True)  # wing L
    _poly(cv,[(cx,cy+s*0.04),(cx+s*0.34,cy-s*0.06),(cx+s*0.28,cy+s*0.16),(cx,cy+s*0.14)],FEATHER,close=True)  # wing R
    cv.add(cx-s*0.06,cy+s*0.3,cx-s*0.06,cy+s*0.42,(150,120,40)); cv.add(cx+s*0.06,cy+s*0.3,cx+s*0.06,cy+s*0.42,(150,120,40))  # legs

def guard_tower(cv,cx,cy,s=100):
    _poly(cv,[(cx-s*0.18,cy+s*0.42),(cx-s*0.14,cy-s*0.28),(cx+s*0.14,cy-s*0.28),(cx+s*0.18,cy+s*0.42)],STONE,close=True)  # tower
    for yy in (0.0,0.18):
        cv.add(cx-s*0.16+s*0.04,cy+s*yy,cx+s*0.16-s*0.04,cy+s*yy,STONE_D)   # courses
    # crenellations
    for i in range(4):
        bx=cx-s*0.14+ i*s*0.28/3
        cv.add(bx,cy-s*0.28,bx,cy-s*0.38,STONE); cv.add(bx,cy-s*0.38,bx+s*0.05,cy-s*0.38,STONE); cv.add(bx+s*0.05,cy-s*0.38,bx+s*0.05,cy-s*0.28,STONE)
    cv.add(cx-s*0.05,cy+s*0.42,cx-s*0.05,cy+s*0.2,STONE_D); cv.add(cx+s*0.05,cy+s*0.42,cx+s*0.05,cy+s*0.2,STONE_D)  # door
    cv.add(cx-s*0.05,cy+s*0.2,cx+s*0.05,cy+s*0.2,STONE_D)

def axe_motif(cv,cx,cy,s,body,legs):
    # dwarven crossed axes for the compass center
    for sgn in (-1,1):
        cv.add(cx,cy+s*0.5,cx+sgn*s*0.5,cy-s*0.5,body)           # haft
        _poly(cv,[(cx+sgn*s*0.32,cy-s*0.3),(cx+sgn*s*0.62,cy-s*0.34),(cx+sgn*s*0.6,cy-s*0.08),(cx+sgn*s*0.3,cy-s*0.12)],legs,close=True)
