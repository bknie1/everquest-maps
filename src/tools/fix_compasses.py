"""Move any compass that has map content running through it.

Preference order, per your note:
  1. an empty pocket INSIDE the grid, as near a corner as it can get
  2. failing that, the margin — again cornerwards

The compass is found by its own N/S/E/W labels, and its geometry is every line
lying wholly inside its disc; anything crossing the disc but extending past it is
by definition something else (a grid line, a wall) and is left alone.
"""
import os, math, collections

O = '/mnt/user-data/outputs'

def parse(l):
    f = l[2:].split(',')
    return float(f[0]), float(f[1]), float(f[3]), float(f[4])

def seg_dist(px, py, x1, y1, x2, y2):
    dx, dy = x2-x1, y2-y1
    L2 = dx*dx + dy*dy
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((px-x1)*dx + (py-y1)*dy)/L2))
    return math.hypot(px-(x1+dx*t), py-(y1+dy*t))

def relocate(z):
    p2 = f'{O}/{z}_2.txt'
    raw = [l.rstrip('\r\n') for l in open(p2, encoding='utf-8', errors='replace') if l.strip()]
    labs = []
    for i, l in enumerate(raw):
        if l.startswith('P'):
            q = l[1:].split(',')
            if ','.join(q[7:]).strip() in ('N','S','E','W'):
                labs.append((i, float(q[0]), float(q[1])))
    if len(labs) < 3: return None
    cx = sum(p[1] for p in labs)/len(labs)
    cy = sum(p[2] for p in labs)/len(labs)
    R  = max(math.hypot(p[1]-cx, p[2]-cy) for p in labs)

    own, other = [], []
    for i, l in enumerate(raw):
        if not l.startswith('L'): continue
        x1,y1,x2,y2 = parse(l)
        if math.hypot(x1-cx,y1-cy) <= R*1.25 and math.hypot(x2-cx,y2-cy) <= R*1.25:
            own.append(i)
        else:
            other.append((x1,y1,x2,y2))
    crossing = sum(1 for s in other if seg_dist(cx,cy,*s) < R*0.95)
    if not crossing: return None

    base = [parse(l) for l in open(f'{O}/{z}.txt', encoding='utf-8', errors='replace')
            if l.startswith('L')]
    bxs = [a for s in base for a in (s[0],s[2])]; bys = [a for s in base for a in (s[1],s[3])]
    CX0,CX1,CY0,CY1 = min(bxs),max(bxs),min(bys),max(bys)          # the grid area
    fxs = [a for s in other for a in (s[0],s[2])]; fys = [a for s in other for a in (s[1],s[3])]
    FX0,FX1,FY0,FY1 = min(fxs),max(fxs),min(fys),max(fys)          # the frame

    # the frame border is not clutter — a compass is meant to sit near it. Drop
    # lines hugging the frame edge so margin positions can qualify.
    SPAN = max(FX1-FX0, FY1-FY0)
    EDGE = SPAN*0.055
    def on_border(s):
        return (min(s[0],s[2]) <= FX0+EDGE or max(s[0],s[2]) >= FX1-EDGE or
                min(s[1],s[3]) <= FY0+EDGE or max(s[1],s[3]) >= FY1-EDGE)
    obstacles = base + [s for s in other if not on_border(s)]
    CELL = max(R*0.6, 20.0)
    grid = collections.defaultdict(list)
    for x1,y1,x2,y2 in obstacles:
        n = max(1, int(math.hypot(x2-x1, y2-y1)//(CELL*0.5)))
        for i in range(n+1):
            t = i/n
            px, py = x1+(x2-x1)*t, y1+(y2-y1)*t
            grid[(int(px//CELL), int(py//CELL))].append((px,py))
    def clearance(px, py, cap=4):
        gx, gy = int(px//CELL), int(py//CELL); best = 1e9
        for dx in range(-cap, cap+1):
            for dy in range(-cap, cap+1):
                for qx, qy in grid.get((gx+dx, gy+dy), ()):
                    d = (qx-px)**2 + (qy-py)**2
                    if d < best: best = d
        return best**0.5

    NEED = R*1.06
    step = max(R*0.28, 10.0)
    def scan(x0,x1,y0,y1, corners):
        best=None
        x=x0
        while x<=x1:
            y=y0
            while y<=y1:
                c=clearance(x,y)
                if c>=NEED:
                    corner=min(math.hypot(x-a,y-b) for a,b in corners)
                    score=(corner, -c)
                    if best is None or score<best[0]: best=(score,(x,y),c)
                y+=step
            x+=step
        return best

    inset = R*1.15
    inner = scan(CX0+inset, CX1-inset, CY0+inset, CY1-inset,
                 [(CX0,CY0),(CX1,CY0),(CX0,CY1),(CX1,CY1)])
    if inner:
        nx, ny = inner[1]; clr = inner[2]; where = 'grid corner pocket'
    else:
        outer = scan(FX0+inset, FX1-inset, FY0+inset, FY1-inset,
                     [(FX0,FY0),(FX1,FY0),(FX0,FY1),(FX1,FY1)])
        if not outer:
            # nothing fits at full size: take the roomiest spot anywhere in the
            # margin and shrink the compass to suit it
            best=None; step2=max(R*0.3,10.0)
            x=FX0+inset
            while x<=FX1-inset:
                y=FY0+inset
                while y<=FY1-inset:
                    if not (CX0<x<CX1 and CY0<y<CY1):
                        c=clearance(x,y)
                        if best is None or c>best[0]: best=(c,(x,y))
                    y+=step2
                x+=step2
            if not best or best[0] < R*0.55: return ('nowhere', z, crossing, 0, 0)
            nx, ny = best[1]; clr = best[0]; where='margin (shrunk)'
            k = min(1.0, (clr*0.92)/(R*1.06))
            for i in own:
                f=raw[i][2:].split(',')
                for a,b_ in ((0,1),(3,4)):
                    f[a]=" %.4f"%(cx+(float(f[a])-cx)*k)
                    f[b_]=" %.4f"%(cy+(float(f[b_])-cy)*k)
                raw[i]='L '+','.join(f)
            newlabs=[]
            for i,lx,ly in labs:
                nlx=cx+(lx-cx)*k; nly=cy+(ly-cy)*k
                newlabs.append((i,nlx,nly))
            labs=newlabs
            R=R*k
        else:
            nx, ny = outer[1]; clr = outer[2]; where = 'margin'

    if where=='margin (shrunk)':
        pass
    elif math.hypot(nx-cx, ny-cy) < R*0.4: return None
    dx, dy = nx-cx, ny-cy
    for i in own:
        f = raw[i][2:].split(',')
        f[0] = " %.4f"%(float(f[0])+dx); f[1] = " %.4f"%(float(f[1])+dy)
        f[3] = " %.4f"%(float(f[3])+dx); f[4] = " %.4f"%(float(f[4])+dy)
        raw[i] = 'L '+','.join(f)
    for i, lx, ly in labs:
        f = raw[i][1:].split(',')
        f[0] = " %.4f"%(lx+dx); f[1] = " %.4f"%(ly+dy)
        raw[i] = 'P'+','.join(f)
    open(p2, 'w', newline='').write('\r\n'.join(raw)+'\r\n')
    b = open(p2,'rb').read()
    assert sum(1 for i,ch in enumerate(b) if ch==10 and (i==0 or b[i-1]!=13))==0, z
    return (where, z, crossing, clr, R)

zones = sorted(b[:-6] for b in os.listdir(O) if b.endswith('_2.txt'))
moved = collections.Counter(); fails=[]
for z in zones:
    r = relocate(z)
    if not r: continue
    where, zz, crossing, clr, R = r
    if where == 'nowhere': fails.append(zz); continue
    moved[where] += 1
    print(f"  {zz:14} {crossing:3} lines crossing -> {where:20} clearance {clr:6.0f} (needed {R*1.18:.0f})")
print(f"\nmoved: {dict(moved)}")
if fails: print("no clear spot found:", fails)
