"""civic_decor.py -- decoration for the races that had none.

Twelve of fifteen races in races.py had an empty decor list; this fills them so a
build never has to invent shapes inline.
"""
import math, random

def _ring(cx, cy, r, ink, n=24, squash=1.0):
    out=[]; prev=None
    for k in range(n+1):
        a=2*math.pi*k/n
        p=(cx+math.cos(a)*r, cy+math.sin(a)*r*squash)
        if prev: out.append((prev[0],prev[1],p[0],p[1],ink))
        prev=p
    return out

# ---- barbarian (Halas): hide tents, totems, fire pits
def hide_tent(cx, cy, r, ink=(120,104,84), dark=(90,70,50), seed=0):
    out=[(cx-r,cy,cx,cy-r*1.25,ink),(cx,cy-r*1.25,cx+r,cy,ink),(cx-r,cy,cx+r,cy,dark)]
    out+=[(cx-r*0.30,cy,cx-r*0.10,cy-r*0.72,dark),(cx+r*0.30,cy,cx+r*0.10,cy-r*0.72,dark)]
    out.append((cx,cy-r*1.25,cx,cy-r*1.55,dark))
    return out

def totem(cx, cy, r, ink=(120,104,84), dark=(90,70,50), seed=0):
    out=[(cx-r*0.28,cy,cx-r*0.28,cy-r*1.6,ink),(cx+r*0.28,cy,cx+r*0.28,cy-r*1.6,ink),
         (cx-r*0.28,cy-r*1.6,cx+r*0.28,cy-r*1.6,ink)]
    for k in range(3):
        yy=cy-r*(0.35+0.45*k)
        out.append((cx-r*0.28,yy,cx+r*0.28,yy,dark))
        out.append((cx-r*0.45,yy-r*0.10,cx-r*0.28,yy,dark))
        out.append((cx+r*0.45,yy-r*0.10,cx+r*0.28,yy,dark))
    return out

def fire_pit(cx, cy, r, ink=(120,104,84), flame=(190,110,60), seed=0):
    out=_ring(cx,cy,r*0.65,ink,n=12,squash=0.45)
    rnd=random.Random(seed)
    for k in range(4):
        x=cx+rnd.uniform(-r*0.3,r*0.3)
        out.append((x,cy-r*0.05,x+rnd.uniform(-r*0.12,r*0.12),cy-r*0.55,flame))
    return out

# ---- dwarf (Kaladim): forge, anvil, ore cart
def anvil(cx, cy, r, ink=(112,104,96), dark=(78,72,66), seed=0):
    out=[(cx-r*0.6,cy,cx+r*0.6,cy,dark),(cx-r*0.3,cy,cx-r*0.3,cy-r*0.4,ink),
         (cx+r*0.3,cy,cx+r*0.3,cy-r*0.4,ink),
         (cx-r*0.75,cy-r*0.4,cx+r*0.55,cy-r*0.4,ink),
         (cx-r*0.75,cy-r*0.4,cx-r*0.95,cy-r*0.62,ink),
         (cx-r*0.95,cy-r*0.62,cx+r*0.55,cy-r*0.62,ink),
         (cx+r*0.55,cy-r*0.62,cx+r*0.55,cy-r*0.4,ink)]
    return out

def forge(cx, cy, r, ink=(112,104,96), flame=(190,110,60), seed=0):
    out=[(cx-r*0.7,cy,cx-r*0.7,cy-r*0.9,ink),(cx+r*0.7,cy,cx+r*0.7,cy-r*0.9,ink),
         (cx-r*0.7,cy-r*0.9,cx+r*0.7,cy-r*0.9,ink),(cx-r*0.9,cy,cx+r*0.9,cy,ink)]
    out.append((cx,cy-r*0.9,cx,cy-r*1.5,ink))
    out+=_ring(cx,cy-r*0.45,r*0.32,flame,n=10)
    return out

def ore_cart(cx, cy, r, ink=(112,104,96), dark=(78,72,66), seed=0):
    out=[(cx-r*0.7,cy-r*0.25,cx+r*0.7,cy-r*0.25,ink),
         (cx-r*0.7,cy-r*0.25,cx-r*0.55,cy-r*0.8,ink),
         (cx+r*0.7,cy-r*0.25,cx+r*0.55,cy-r*0.8,ink),
         (cx-r*0.55,cy-r*0.8,cx+r*0.55,cy-r*0.8,ink)]
    out+=_ring(cx-r*0.35,cy,r*0.22,dark,n=10)
    out+=_ring(cx+r*0.35,cy,r*0.22,dark,n=10)
    return out

# ---- high elf / wood elf: spire, arch, treehouse
def elf_spire(cx, cy, r, ink=(150,160,180), dark=(110,124,150), seed=0):
    out=[(cx-r*0.32,cy,cx-r*0.32,cy-r*1.3,ink),(cx+r*0.32,cy,cx+r*0.32,cy-r*1.3,ink),
         (cx-r*0.32,cy-r*1.3,cx,cy-r*1.95,ink),(cx,cy-r*1.95,cx+r*0.32,cy-r*1.3,ink),
         (cx-r*0.45,cy,cx+r*0.45,cy,dark)]
    for k in range(2):
        yy=cy-r*(0.45+0.42*k)
        out.append((cx-r*0.32,yy,cx+r*0.32,yy,dark))
    return out

def treehouse(cx, cy, r, ink=(96,124,78), dark=(70,96,58), seed=0):
    out=[(cx,cy,cx,cy-r*1.0,dark)]
    out+=[(cx-r*0.6,cy-r*1.0,cx+r*0.6,cy-r*1.0,ink),
          (cx-r*0.5,cy-r*1.0,cx-r*0.5,cy-r*1.5,ink),
          (cx+r*0.5,cy-r*1.0,cx+r*0.5,cy-r*1.5,ink),
          (cx-r*0.62,cy-r*1.5,cx,cy-r*1.9,ink),(cx,cy-r*1.9,cx+r*0.62,cy-r*1.5,ink)]
    out+=_ring(cx,cy-r*0.55,r*0.5,ink,n=10)
    return out

# ---- halfling (Rivervale): hobbit door, pie, fence
def burrow_door(cx, cy, r, ink=(140,110,70), dark=(96,78,54), seed=0):
    out=_ring(cx,cy-r*0.35,r*0.62,ink,n=18)
    out=[t for t in out if t[1]<=cy and t[3]<=cy]
    out.append((cx-r*0.62,cy,cx+r*0.62,cy,dark))
    out+=_ring(cx+r*0.30,cy-r*0.35,r*0.07,dark,n=8)
    return out

def pie(cx, cy, r, ink=(180,150,90), dark=(140,110,60), seed=0):
    out=_ring(cx,cy,r*0.5,ink,n=14,squash=0.55)
    for k in range(3):
        a=math.pi*(k+1)/4
        out.append((cx-math.cos(a)*r*0.45,cy-r*0.10,cx+math.cos(a)*r*0.45,cy-r*0.10,dark))
    return out

# ---- erudite (Erudin): tome, orrery, obelisk
def tome(cx, cy, r, ink=(96,110,140), dark=(70,86,120), seed=0):
    out=[(cx-r*0.6,cy,cx+r*0.6,cy,ink),(cx-r*0.6,cy,cx-r*0.55,cy-r*0.75,ink),
         (cx+r*0.6,cy,cx+r*0.55,cy-r*0.75,ink),
         (cx-r*0.55,cy-r*0.75,cx,cy-r*0.62,ink),(cx,cy-r*0.62,cx+r*0.55,cy-r*0.75,ink),
         (cx,cy-r*0.62,cx,cy,dark)]
    return out

def orrery(cx, cy, r, ink=(120,140,180), dark=(70,86,120), seed=0):
    out=_ring(cx,cy-r*0.4,r*0.16,ink,n=10)
    for k,rr in enumerate((0.45,0.72,1.0)):
        out+=_ring(cx,cy-r*0.4,r*rr,dark if k%2 else ink,n=20,squash=0.42)
    out.append((cx,cy-r*0.4,cx,cy+r*0.7,ink))
    out.append((cx-r*0.3,cy+r*0.7,cx+r*0.3,cy+r*0.7,ink))
    return out

def obelisk(cx, cy, r, ink=(120,140,180), dark=(70,86,120), seed=0):
    out=[(cx-r*0.26,cy,cx-r*0.18,cy-r*1.5,ink),(cx+r*0.26,cy,cx+r*0.18,cy-r*1.5,ink),
         (cx-r*0.18,cy-r*1.5,cx,cy-r*1.8,ink),(cx,cy-r*1.8,cx+r*0.18,cy-r*1.5,ink),
         (cx-r*0.4,cy,cx+r*0.4,cy,dark)]
    for k in range(3):
        yy=cy-r*(0.35+0.38*k)
        out.append((cx-r*0.22,yy,cx+r*0.22,yy,dark))
    return out

# ---- humans: banner, ship, market stall, guard post
def banner(cx, cy, r, ink=(150,60,50), pole=(120,100,72), seed=0):
    w,h=r*0.62,r*1.7
    out=[(cx,cy,cx,cy-h,pole),(cx-w,cy-h*0.92,cx+w,cy-h*0.92,ink),
         (cx-w,cy-h*0.92,cx-w,cy-h*0.30,ink),(cx+w,cy-h*0.92,cx+w,cy-h*0.30,ink),
         (cx-w,cy-h*0.30,cx,cy-h*0.44,ink),(cx+w,cy-h*0.30,cx,cy-h*0.44,ink)]
    for k in range(3):
        yy=cy-h*0.80+k*h*0.16
        out.append((cx-w*0.7,yy,cx+w*0.7,yy,ink))
    return out

def caravel(cx, cy, r, ink=(128,108,80), sail=(180,168,140), seed=0):
    out=[(cx-r*0.9,cy,cx+r*0.9,cy,ink),(cx-r*0.9,cy,cx-r*0.62,cy-r*0.32,ink),
         (cx+r*0.9,cy,cx+r*0.62,cy-r*0.32,ink),(cx-r*0.62,cy-r*0.32,cx+r*0.62,cy-r*0.32,ink)]
    out.append((cx,cy-r*0.32,cx,cy-r*1.5,ink))
    out+=[(cx,cy-r*1.4,cx+r*0.55,cy-r*0.95,sail),(cx+r*0.55,cy-r*0.95,cx,cy-r*0.5,sail),
          (cx,cy-r*1.4,cx-r*0.42,cy-r*1.0,sail),(cx-r*0.42,cy-r*1.0,cx,cy-r*0.62,sail)]
    return out

def market_stall(cx, cy, r, ink=(128,108,80), cloth=(150,70,55), seed=0):
    out=[(cx-r*0.75,cy,cx-r*0.75,cy-r*0.75,ink),(cx+r*0.75,cy,cx+r*0.75,cy-r*0.75,ink)]
    for k in range(4):
        x0=cx-r*0.9+r*1.8*k/4; x1=cx-r*0.9+r*1.8*(k+1)/4
        out.append((x0,cy-r*0.75,(x0+x1)/2,cy-r*0.95,cloth))
        out.append(((x0+x1)/2,cy-r*0.95,x1,cy-r*0.75,cloth))
    out.append((cx-r*0.75,cy-r*0.3,cx+r*0.75,cy-r*0.3,ink))
    return out

# ---- troll (Grobb): bone pile, hut, stink pot
def bone_pile(cx, cy, r, ink=(180,176,160), dark=(130,126,112), seed=0):
    rnd=random.Random(seed); out=[]
    for k in range(6):
        x=cx+rnd.uniform(-r*0.6,r*0.6); y=cy+rnd.uniform(-r*0.18,r*0.10)
        ln=r*rnd.uniform(0.25,0.5); a=rnd.uniform(-0.6,0.6)
        x2,y2=x+math.cos(a)*ln, y+math.sin(a)*ln*0.5
        out.append((x,y,x2,y2, ink if k%2 else dark))
        out.append((x,y-r*0.04,x,y+r*0.04, ink))
        out.append((x2,y2-r*0.04,x2,y2+r*0.04, ink))
    return out

def swamp_hut(cx, cy, r, ink=(112,100,76), dark=(80,70,52), seed=0):
    out=[(cx-r*0.7,cy,cx-r*0.55,cy-r*0.6,ink),(cx+r*0.7,cy,cx+r*0.55,cy-r*0.6,ink),
         (cx-r*0.55,cy-r*0.6,cx,cy-r*1.05,ink),(cx,cy-r*1.05,cx+r*0.55,cy-r*0.6,ink),
         (cx-r*0.7,cy,cx+r*0.7,cy,dark)]
    for k in range(3):
        x=cx-r*0.45+r*0.45*k
        out.append((x,cy,x,cy-r*0.30,dark))
    return out

# ---- ogre (Oggok): crude pillar, aqueduct, war drum
def crude_pillar(cx, cy, r, ink=(126,110,84), dark=(96,84,62), seed=0):
    rnd=random.Random(seed)
    h=r*1.5*rnd.uniform(0.7,1.15); w=r*0.42
    out=[(cx-w,cy,cx-w,cy-h,ink),(cx+w,cy,cx+w,cy-h*rnd.uniform(0.55,1.0),ink),
         (cx-w*1.4,cy,cx+w*1.4,cy,dark)]
    out.append((cx-w,cy-h,cx+w*0.4,cy-h*0.9,ink))
    for k in range(3):
        yy=cy-h*(0.22+0.26*k)
        out.append((cx-w*0.9,yy,cx+w*0.9,yy,dark))
    return out

def aqueduct(cx, cy, r, ink=(126,110,84), dark=(96,84,62), seed=0):
    rnd=random.Random(seed)
    w,h=r*2.0,r*1.0
    out=[(cx-w/2,cy,cx+w/2,cy,dark),(cx-w/2,cy-h,cx+w/2,cy-h,dark)]
    for k in range(3):
        ax=cx-w/2+w*(k+0.5)/3; ar=w/6.5; prev=None
        for j in range(11):
            a=math.pi*(j/10)
            p=(ax+math.cos(a)*ar, cy-math.sin(a)*ar*1.1)
            if prev: out.append((prev[0],prev[1],p[0],p[1],ink))
            prev=p
        out.append((ax-ar,cy,ax-ar,cy-h,ink))
        out.append((ax+ar,cy,ax+ar,cy-h,ink))
    return [t for t in out if rnd.random()>0.12]

def war_drum(cx, cy, r, ink=(126,110,84), dark=(96,84,62), seed=0):
    out=_ring(cx,cy-r*0.45,r*0.55,ink,n=16,squash=0.45)
    out+=[(cx-r*0.55,cy-r*0.45,cx-r*0.48,cy+r*0.15,ink),
          (cx+r*0.55,cy-r*0.45,cx+r*0.48,cy+r*0.15,ink)]
    out+=_ring(cx,cy+r*0.15,r*0.48,dark,n=16,squash=0.45)
    for k in range(4):
        a=2*math.pi*k/4
        out.append((cx+math.cos(a)*r*0.5,cy-r*0.45+math.sin(a)*r*0.22,
                    cx+math.cos(a)*r*0.46,cy+r*0.15+math.sin(a)*r*0.20,dark))
    return out

# ---- froglok (Guk): lily pad, croaking stone
def lily_pad(cx, cy, r, ink=(86,132,96), dark=(60,102,72), seed=0):
    out=_ring(cx,cy,r*0.55,ink,n=16,squash=0.5)
    out.append((cx,cy,cx+r*0.55,cy-r*0.05,dark))
    out+=_ring(cx+r*0.35,cy-r*0.25,r*0.16,dark,n=8,squash=0.6)
    return out

# ---- kerran: fishing rack
def fish_rack(cx, cy, r, ink=(140,120,90), dark=(100,86,64), seed=0):
    out=[(cx-r*0.7,cy,cx-r*0.6,cy-r*0.9,ink),(cx+r*0.7,cy,cx+r*0.6,cy-r*0.9,ink),
         (cx-r*0.6,cy-r*0.9,cx+r*0.6,cy-r*0.9,ink)]
    for k in range(3):
        x=cx-r*0.4+r*0.4*k
        out.append((x,cy-r*0.9,x,cy-r*0.45,dark))
        out+=_ring(x,cy-r*0.35,r*0.13,dark,n=8,squash=0.5)
    return out

SHAPES = {
 'hide_tent':hide_tent,'totem':totem,'fire_pit':fire_pit,
 'anvil':anvil,'forge':forge,'ore_cart':ore_cart,
 'elf_spire':elf_spire,'treehouse':treehouse,
 'burrow_door':burrow_door,'pie':pie,
 'tome':tome,'orrery':orrery,'obelisk':obelisk,
 'banner':banner,'caravel':caravel,'market_stall':market_stall,
 'bone_pile':bone_pile,'swamp_hut':swamp_hut,
 'crude_pillar':crude_pillar,'aqueduct':aqueduct,'war_drum':war_drum,
 'lily_pad':lily_pad,'fish_rack':fish_rack,
}
