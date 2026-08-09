"""Nektulos colour pass.

Feerrott gets its darkness from a rainforest canopy — thousands of overlapping
crowns. Nektulos is temperate and comparatively open: a road, a river, camps,
grassland between the trees. Copying Feerrott's density would read as jungle.

So the density goes where it is true: the MARGINS, packed with canopy to say this
map is one surveyed clearing inside a much larger dark forest. Inside the grid the
colour comes off the ground instead — grass, plus deeper individual crowns — which
tints the map without burying labels.
"""
import sys, math, collections, random
sys.path.insert(0, '/home/claude/work')
import terrain as TR, fauna as FA
random.seed(2024)

O = '/mnt/user-data/outputs'
BASE = f'{O}/nektulos.txt'; DECO = f'{O}/nektulos_2.txt'

GRASS   = (TR.PALETTE['grass_dark'], TR.PALETTE['grass'], TR.PALETTE['grass_lit'])
ROCKB   = TR.PALETTE['rock_brown']; ROCKL = TR.PALETTE['rock_brown_l']
CANOPY  = TR.PALETTE['canopy']; CANOPY_D = TR.PALETTE['canopy_deep']
BRIDGE  = (128, 96, 60); BRIDGE_D = (96, 70, 44)
WATER   = (52, 92, 148)
TREE_INKS = {(46,72,48),(54,80,46),(84,82,76),(50,76,50),(56,48,40),
             (62,52,84),(70,58,92),(66,54,88),(52,42,58),(112,116,112)}
MINE = set(GRASS) | {ROCKB, ROCKL, CANOPY, CANOPY_D, BRIDGE, BRIDGE_D} | \
       {FA.PALETTE[k] for k in FA.PALETTE}

def parse(l):
    f = l[2:].split(',')
    return float(f[0]), float(f[1]), float(f[3]), float(f[4]), (int(f[6]), int(f[7]), int(f[8]))

base = [l.rstrip('\r\n') for l in open(BASE, encoding='utf-8', errors='replace') if l.startswith('L')]
raw  = [l.rstrip('\r\n') for l in open(DECO, encoding='utf-8', errors='replace') if l.strip()]
head = [l for l in raw if not l.startswith('L')]
deco = [l for l in raw if l.startswith('L')]
deco = [l for l in deco if parse(l)[4] not in MINE]          # rebuildable

bxs = [a for l in base for a in (parse(l)[0], parse(l)[2])]
bys = [a for l in base for a in (parse(l)[1], parse(l)[3])]
sx, sy = sorted(bxs), sorted(bys)
GX0, GX1 = sx[int(len(sx)*0.01)], sx[int(len(sx)*0.99)]
GY0, GY1 = sy[int(len(sy)*0.01)], sy[int(len(sy)*0.99)]
W_, H_ = GX1-GX0, GY1-GY0
fxs = [a for l in deco for a in (parse(l)[0], parse(l)[2])]
fys = [a for l in deco for a in (parse(l)[1], parse(l)[3])]
FX0, FX1, FY0, FY1 = min(fxs), max(fxs), min(fys), max(fys)
print(f"grid x[{GX0:.0f},{GX1:.0f}] y[{GY0:.0f},{GY1:.0f}]   frame x[{FX0:.0f},{FX1:.0f}] y[{FY0:.0f},{FY1:.0f}]")

# ---------- occupancy: everything already drawn ----------
CELL = 46.0
occ = collections.defaultdict(list)
def add_occ(lines):
    for l in lines:
        x1,y1,x2,y2,c = parse(l)
        n = max(1, int(math.hypot(x2-x1, y2-y1)//22))
        for i in range(n+1):
            t = i/n
            px, py = x1+(x2-x1)*t, y1+(y2-y1)*t
            occ[(int(px//CELL), int(py//CELL))].append((px, py))
add_occ(base); add_occ(deco)
def clear_of(x, y, r=2):
    gx, gy = int(x//CELL), int(y//CELL); best = 1e9
    for dx in range(-r, r+1):
        for dy in range(-r, r+1):
            for px, py in occ.get((gx+dx, gy+dy), ()):
                d = (px-x)**2 + (py-y)**2
                if d < best: best = d
    return best**0.5

# water, so grass stays out of it
water_pts = [((parse(l)[0]+parse(l)[2])/2, (parse(l)[1]+parse(l)[3])/2)
             for l in deco if parse(l)[4] == WATER]
wg = collections.defaultdict(list)
for px, py in water_pts: wg[(int(px//CELL), int(py//CELL))].append((px, py))
def in_water(x, y, r=60):
    gx, gy = int(x//CELL), int(y//CELL)
    for dx in (-1,0,1):
        for dy in (-1,0,1):
            for px, py in wg.get((gx+dx, gy+dy), ()):
                if (px-x)**2 + (py-y)**2 < r*r: return True
    return False

# ---------- the rock shelf: the top band, creeping down both flanks ----------
def on_rock(x, y):
    t = (y - GY0) / H_
    if t < 0.085: return True                                    # the northern shelf
    if x < GX0 + W_*0.13 and t < 0.30: return True               # west, by the hobbit camp
    if x > GX1 - W_*0.13 and t < 0.26: return True               # east, toward Neriak gate
    if x < GX0 + W_*0.07 and t < 0.42: return True
    return False

rock = TR.rock_band(lambda x,y: on_rock(x,y) and clear_of(x,y) > 26,
                    GX0, GY0-40, GX1, GY0+H_*0.45, step=36.0, seed=11)
print(f"rock shelf: {len(rock)} strokes")

# ---------- grass over the open floor ----------
def on_grass(x, y):
    if not (GX0+10 < x < GX1-10 and GY0+10 < y < GY1-10): return False
    if on_rock(x, y): return False
    if in_water(x, y): return False
    return clear_of(x, y) > 34
grass = TR.grass_field(on_grass, GX0, GY0, GX1, GY1, step=40.0, ink=GRASS,
                       seed=7, density=0.85)
print(f"grass: {len(grass)} blades")

# ---------- margins: packed forest, knockout-friendly ----------
def in_margin(x, y):
    if GX0-30 < x < GX1+30 and GY0-30 < y < GY1+30: return False   # never over the grid
    if not (FX0+40 < x < FX1-40 and FY0+40 < y < FY1-40): return False
    return clear_of(x, y) > 145      # crowns are wide: keep well off title, compass, sketches
margin = TR.foliage_margin(in_margin, FX0, FY0, FX1, FY1, step=74.0, seed=5, count=900)
print(f"margin foliage: {len(margin)} lines")

# ---------- deepen the existing crowns ----------
tree_pts = []
idx = [i for i,l in enumerate(deco) if parse(l)[4] in TREE_INKS]
G = 44.0; cells = collections.defaultdict(list)
for i in idx:
    x1,y1,x2,y2,c = parse(deco[i])
    cells[(int(((x1+x2)/2)//G), int(((y1+y2)/2)//G))].append(i)
seen=set()
for k in list(cells):
    if k in seen: continue
    st=[k]; comp=[]
    while st:
        d=st.pop()
        if d in seen or d not in cells: continue
        seen.add(d); comp+=cells[d]
        for dx in(-1,0,1):
            for dy in(-1,0,1):
                nn=(d[0]+dx,d[1]+dy)
                if nn in cells and nn not in seen: st.append(nn)
    xs=[];ys=[]
    for i in comp:
        x1,y1,x2,y2,c = parse(deco[i]); xs+=[x1,x2]; ys+=[y1,y2]
    tree_pts.append((sum(xs)/len(xs), min(ys)+ (max(ys)-min(ys))*0.32,
                     max(max(xs)-min(xs), (max(ys)-min(ys))*0.5)*0.42))
shade=[]
for cx, cy, r in tree_pts:
    if r < 12: continue
    shade += TR.canopy_shade(cx, cy, r*0.85, CANOPY_D, seed=int(cx), rows=4)
print(f"canopy shading on {len(tree_pts)} crowns: {len(shade)} lines")

# ---------- the bridge, coloured as timber ----------
bridge=[]
for l in base:
    x1,y1,x2,y2,c = parse(l)
    if c == (78,74,92) and -20 < (x1+x2)/2 < 200 and 700 < (y1+y2)/2 < 1200:
        bridge.append((x1,y1,x2,y2,BRIDGE))
if bridge:
    bx = [v for s in bridge for v in (s[0],s[2])]; by = [v for s in bridge for v in (s[1],s[3])]
    x0,x1_,y0,y1_ = min(bx),max(bx),min(by),max(by)
    yy = y0+6
    while yy < y1_-4:                                   # planks
        bridge.append((x0+3, yy, x1_-3, yy, BRIDGE_D)); yy += 14
    for k in range(4):
        xx = x0 + (x1_-x0)*(k+1)/5
        bridge.append((xx, y0, xx, y1_, BRIDGE_D))
print(f"bridge: {len(bridge)} lines in timber")

# ---------- fauna ----------
def place(fn, n, x0, y0, x1, y1, size, seed, ink=None):
    pts = TR.scatter(x0, y0, x1, y1, n, size*2.4,
                     reject=lambda x,y: clear_of(x,y) < size*0.9 or on_rock(x,y) or in_water(x,y),
                     seed=seed)
    out=[]
    for i,(x,y) in enumerate(pts):
        out += fn(x, y, size, ink, seed=seed+i) if ink else fn(x, y, size, seed=seed+i)
    return out, len(pts)
crit=[]
g,n1 = place(FA.spider,   7, GX0+W_*0.15, GY0+H_*0.18, GX1-W_*0.10, GY1-H_*0.25, 62, 21)
crit+=g
g,n2 = place(FA.skeleton, 5, GX0+W_*0.20, GY0+H_*0.12, GX1-W_*0.15, GY0+H_*0.55, 60, 33)
crit+=g
g,n3 = place(FA.hobbit,   4, GX0+W_*0.05, GY0+H_*0.62, GX0+W_*0.45, GY1-H_*0.05, 58, 44)
crit+=g
g,n4 = place(FA.darkelf,  4, GX1-W_*0.42, GY0+H_*0.06, GX1-W_*0.04, GY0+H_*0.42, 60, 55)
crit+=g
print(f"fauna: {n1} spiders, {n2} skeletons, {n3} halflings (SW), {n4} Teir'Dal (NE)")

# ---------- strays: clear the north, seed a few in the south ----------
kept=[]; removed=0
for l in deco:
    x1,y1,x2,y2,c = parse(l)
    my=(y1+y2)/2
    if c in TREE_INKS and my < GY0-20:
        removed+=1; continue
    kept.append(l)
deco = kept
print(f"removed {removed} stray tree/web lines north of the grid")
south=[]
for (x,y) in TR.scatter(GX0+W_*0.12, GY1+40, GX1-W_*0.12, min(GY1+240, FY1-90), 6, 150,
                        reject=lambda x,y: clear_of(x,y) < 60, seed=91):
    r = random.uniform(34, 52)
    prev=None
    for k in range(10):
        a=2*math.pi*k/9; wob=1.0+0.15*math.sin(3*a+x)
        p=(x+math.cos(a)*r*wob, y+math.sin(a)*r*0.85*wob)
        if prev: south.append((prev[0],prev[1],p[0],p[1],CANOPY))
        prev=p
    south += TR.canopy_shade(x, y, r*0.7, CANOPY_D, seed=int(x))
print(f"seeded {len(south)} lines of forest south of the grid")

out = rock + grass + margin + shade + bridge + crit + south
lines = ["L %.4f, %.4f, 0.0000, %.4f, %.4f, 0.0000, %d, %d, %d" % (a,b,c,d,*ink)
         for a,b,c,d,ink in out]
open(DECO, 'w', newline='').write('\r\n'.join(head + deco + lines) + '\r\n')
print(f"\nnektulos_2: {len(deco)} kept + {len(lines)} new = {len(deco)+len(lines)} lines")
b = open(DECO, 'rb').read()
print("CRLF OK" if sum(1 for i,ch in enumerate(b) if ch==10 and (i==0 or b[i-1]!=13))==0 else "BAD")
