"""terrain.py — reusable landscape assets.

Everything here returns [(x1,y1,x2,y2,ink)] in map coordinates, so it can be
appended straight to a layer or handed to a Canvas.

    peak()            broken rocky summit (the northern Nektulos mountain)
    rock_band()       brown rock shading over an irregular region
    grass_field()     dense short grass strokes — colours ground without hiding labels
    canopy_shade()    fill strokes inside a tree crown, to deepen a forest
    foliage_margin()  packed foliage for the frame margins
    scatter()         generic collision-aware placer used by all of the above

Colour, not crosshatch: the aim is to tint an area, not to bury it. Grass runs
short and sparse enough that a label still reads over it.
"""
import math, random

PALETTE = {
    # forest floor, dark and lush (matched to the Feerrott jungle greens)
    'grass_dark':  (56, 84, 48),
    'grass':       (72, 102, 60),
    'grass_lit':   (96, 124, 78),
    'canopy':      (46, 72, 48),
    'canopy_deep': (34, 58, 38),
    # rock
    'rock':        (104, 96, 96),
    'rock_shade':  (132, 124, 120),
    'rock_brown':  (124, 96, 68),
    'rock_brown_l':(150, 124, 92),
}


def scatter(x0, y0, x1, y1, n, min_dist, reject=None, seed=0, tries_mult=40):
    """Poisson-ish placement: n points in the box, no two closer than min_dist,
    `reject(x,y)` vetoes a position. Returns the points actually placed."""
    rnd = random.Random(seed)
    pts = []
    cell = min_dist
    grid = {}
    tries = 0
    while len(pts) < n and tries < n*tries_mult:
        tries += 1
        x = rnd.uniform(x0, x1); y = rnd.uniform(y0, y1)
        if reject and reject(x, y): continue
        gx, gy = int(x//cell), int(y//cell)
        ok = True
        for dx in (-1,0,1):
            for dy in (-1,0,1):
                for px, py in grid.get((gx+dx, gy+dy), ()):
                    if (px-x)**2 + (py-y)**2 < min_dist*min_dist: ok = False; break
                if not ok: break
            if not ok: break
        if not ok: continue
        pts.append((x, y)); grid.setdefault((gx,gy), []).append((x,y))
    return pts


def peak(cx, cy, w, h, ink=None, shade=None, seed=0):
    """A broken rocky summit: irregular ridgeline, subsidiary crag, spurs off the
    top, hachures down the fall line, rubble at the foot instead of a ruled base.
    Reads as rock rather than as a triangle symbol."""
    ink = ink or PALETTE['rock']; shade = shade or PALETTE['rock_shade']
    rnd = random.Random(seed)
    out = []
    def L(x1,y1,x2,y2,c): out.append((x1,y1,x2,y2,c))
    foot = cy + h*0.45
    ridge = [(cx-w*0.52, foot),
             (cx-w*0.40, foot-h*0.20), (cx-w*0.33, foot-h*0.16),
             (cx-w*0.24, foot-h*0.44), (cx-w*0.15, foot-h*0.40),
             (cx-w*0.06, foot-h*0.78), (cx-w*0.01, foot-h*0.93),
             (cx+w*0.03, foot-h*1.00),
             (cx+w*0.10, foot-h*0.80), (cx+w*0.16, foot-h*0.83),
             (cx+w*0.26, foot-h*0.52), (cx+w*0.34, foot-h*0.55),
             (cx+w*0.44, foot-h*0.22), (cx+w*0.56, foot)]
    for i in range(len(ridge)-1): L(*ridge[i], *ridge[i+1], ink)
    crag = [(cx-w*0.60, foot),(cx-w*0.50, foot-h*0.30),(cx-w*0.44, foot-h*0.26),
            (cx-w*0.36, foot-h*0.52),(cx-w*0.27, foot-h*0.30)]
    for i in range(len(crag)-1): L(*crag[i], *crag[i+1], shade)
    for frac, drop in ((0.02,0.86),(0.14,0.58),(-0.12,0.62)):
        sx, sy = cx+w*frac, foot-h*drop
        for k in range(4):
            px = sx + w*rnd.uniform(0.02,0.06)*(1 if frac>=0 else -1)
            py = sy + h*rnd.uniform(0.10,0.18)
            if py > foot-h*0.05: break
            L(sx, sy, px, py, shade); sx, sy = px, py
    for k in range(11):
        t=(k+1)/12.0
        ax = cx+w*0.05 + (w*0.50)*t; ay = foot-h*(1.0-t*0.95)
        L(ax, ay, ax+w*0.055, ay+h*0.075, shade)
    for k in range(8):
        t=(k+1)/9.0
        ax = cx-w*0.02 - (w*0.46)*t; ay = foot-h*(0.95-t*0.85)
        L(ax, ay, ax-w*0.05, ay+h*0.07, shade)
    for k in range(11):
        x = cx-w*0.55 + w*1.10*k/10.0 + rnd.uniform(-7,7)
        y = foot + rnd.uniform(-3,6); ww = rnd.uniform(7,17)
        L(x-ww, y, x-ww*0.3, y-rnd.uniform(4,9), shade)
        L(x-ww*0.3, y-rnd.uniform(3,7), x+ww*0.5, y, shade)
    return out


def rock_band(inside, x0, y0, x1, y1, step=26.0, ink=None, lit=None, seed=0):
    """Brown rock shading over any region `inside(x,y)` reports true for.
    Short broken strokes with occasional outcrops — reads as bare stone, and
    stays open enough not to swallow a label."""
    ink = ink or PALETTE['rock_brown']; lit = lit or PALETTE['rock_brown_l']
    rnd = random.Random(seed)
    out = []
    y = y0
    while y < y1:
        x = x0 + (step*0.5 if int((y-y0)/step) % 2 else 0)
        while x < x1:
            if inside(x, y):
                a = rnd.uniform(-0.5, 0.5)
                ln = step*rnd.uniform(0.30, 0.55)
                dx, dy = math.cos(a)*ln, math.sin(a)*ln*0.5
                c = lit if rnd.random() < 0.35 else ink
                out.append((x-dx*0.5, y-dy*0.5, x+dx*0.5, y+dy*0.5, c))
                if rnd.random() < 0.14:                     # small outcrop
                    r = step*rnd.uniform(0.16, 0.30)
                    pts=[(x+math.cos(t*2*math.pi/5)*r*rnd.uniform(0.7,1.2),
                          y+math.sin(t*2*math.pi/5)*r*0.6*rnd.uniform(0.7,1.2)) for t in range(5)]
                    for i in range(len(pts)):
                        out.append((*pts[i], *pts[(i+1)%len(pts)], ink))
            x += step
        y += step*0.86
    return out


def grass_field(inside, x0, y0, x1, y1, step=34.0, ink=None, seed=0, density=0.72):
    """Dense low grass: paired short blades, colour without clutter.

    Deliberately NOT tufts on bare ground — that reads as scrubland. These sit
    close together so the eye reads a green field, while each mark stays small
    enough for a label to sit on top."""
    inks = ink or (PALETTE['grass_dark'], PALETTE['grass'], PALETTE['grass_lit'])
    if isinstance(inks, tuple) and isinstance(inks[0], int): inks = (inks,)
    rnd = random.Random(seed)
    out = []
    y = y0
    row = 0
    while y < y1:
        x = x0 + (step*0.5 if row % 2 else 0)
        while x < x1:
            if rnd.random() < density:
                jx = x + rnd.uniform(-step*0.3, step*0.3)
                jy = y + rnd.uniform(-step*0.3, step*0.3)
                if inside(jx, jy):
                    c = inks[rnd.randrange(len(inks))]
                    h = step*rnd.uniform(0.30, 0.46)
                    lean = rnd.uniform(-0.35, 0.35)
                    out.append((jx, jy, jx+lean*h, jy-h, c))
                    out.append((jx+h*0.22, jy, jx+h*0.22+lean*h*0.7, jy-h*0.72, c))
            x += step
        y += step*0.78
        row += 1
    return out


def canopy_shade(cx, cy, r, ink=None, seed=0, rows=5):
    """Fill strokes inside a tree crown so the canopy reads as dark mass."""
    ink = ink or PALETTE['canopy_deep']
    rnd = random.Random(seed)
    out = []
    for k in range(rows):
        t = (k+0.5)/rows
        yy = cy - r + 2*r*t
        half = math.sqrt(max(0.0, 1 - (2*t-1)**2)) * r * 0.86
        if half < 2: continue
        x = cx - half
        while x < cx + half:
            seg = min(rnd.uniform(r*0.18, r*0.4), cx+half-x)
            out.append((x, yy, x+seg, yy, ink))
            x += seg + rnd.uniform(r*0.10, r*0.22)
    return out


def foliage_margin(inside, x0, y0, x1, y1, step=30.0, seed=0, dark=True, count=None):
    """Packed canopy for a frame margin: overlapping crowns, no trunks, so it
    reads as unbroken forest running off the edge of the surveyed area."""
    rnd = random.Random(seed)
    deep = PALETTE['canopy_deep'] if dark else PALETTE['grass']
    mid  = PALETTE['canopy']
    out = []
    n = count if count else min(400, int((x1-x0)*(y1-y0)/(step*step*4.0)))
    pts = scatter(x0, y0, x1, y1, n,
                  step*0.52, reject=lambda x,y: not inside(x,y), seed=seed)
    for (cx, cy) in pts:
        r = step*rnd.uniform(0.55, 0.92)
        c = deep if rnd.random() < 0.72 else mid
        prev = None
        n = 9
        for k in range(n+1):
            a = 2*math.pi*k/n
            wob = 1.0 + 0.16*math.sin(3*a + cx)
            p = (cx+math.cos(a)*r*wob, cy+math.sin(a)*r*0.82*wob)
            if prev: out.append((prev[0], prev[1], p[0], p[1], c))
            prev = p
        if rnd.random() < 0.85:
            out += canopy_shade(cx, cy, r*0.74, deep, seed=int(cx), rows=4)
    return out
