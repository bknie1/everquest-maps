"""flora.py — trees, undergrowth and ground cover.

Companion to fauna.py. Every function takes (cx, cy, s, ink=None, seed=0) and
returns [(x1,y1,x2,y2,ink)], so trees are interchangeable in a scatter and a zone
can be re-forested by swapping which names go in the list.

`s` is the tree's full height; canopies are drawn ABOVE (cx, cy), which is the
trunk base, so a tree placed at a point sits on it rather than centred over it.
"""
import math, random

PALETTE = {
    'fir':        (46, 72, 48),
    'fir_north':  (62, 52, 84),     # the purple cast Nektulos takes toward Neriak
    'broadleaf':  (50, 76, 50),
    'willow':     (54, 80, 46),
    'dead':       (84, 82, 76),
    'redwood':    (58, 66, 46),
    'palm':       (70, 96, 58),
    'trunk':      (56, 48, 40),
    'under':      (66, 90, 56),     # ferns, bushes
    'reed':       (86, 104, 62),
    'flower':     (128, 96, 120),
    'fungus':     (120, 104, 122),
}


def _P(out, pts, ink, close=False):
    for i in range(len(pts)-1):
        out.append((pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1], ink))
    if close and len(pts) > 2:
        out.append((pts[-1][0], pts[-1][1], pts[0][0], pts[0][1], ink))


# ------------------------------------------------------------------ trees --
def fir(cx, cy, s, ink=None, seed=0, trunk=None):
    """Conifer: four stacked tiers. The workhorse of a temperate forest."""
    ink = ink or PALETTE['fir']; trunk = trunk or PALETTE['trunk']
    out = [(cx, cy, cx, cy-s*0.16, trunk)]
    for i in range(4):
        by = cy - s*0.13 - (s*0.80)*i/4
        ap = by - s*0.95/4
        wv = s*0.30*(1 - i/4*0.62)
        out += [(cx-wv, by, cx, ap, ink), (cx, ap, cx+wv, by, ink), (cx-wv, by, cx+wv, by, ink)]
    return out

def broadleaf(cx, cy, s, ink=None, seed=0, trunk=None):
    """Round lobed crown on a short trunk."""
    ink = ink or PALETTE['broadleaf']; trunk = trunk or PALETTE['trunk']
    out = []
    r = s*0.34; top = cy - s*0.52
    prev = None
    for k in range(25):
        t = 2*math.pi*k/24
        wob = 1.0 + 0.10*math.sin(7*t + seed)
        p = (cx+math.cos(t)*r*wob, top+math.sin(t)*r*0.88*wob)
        if prev: out.append((prev[0], prev[1], p[0], p[1], ink))
        prev = p
    out.append((cx, top+r*0.82, cx, cy, trunk))
    return out

def willow(cx, cy, s, ink=None, seed=0, trunk=None):
    """Weeping crown with trailing fronds."""
    ink = ink or PALETTE['willow']; trunk = trunk or PALETTE['trunk']
    rnd = random.Random(seed)
    out = [(cx, cy, cx, cy-s*0.48, trunk)]
    cr = cy - s*0.48; rw = s*0.34
    prev = None
    for k in range(11):
        a = math.pi*k/10
        p = (cx-rw*math.cos(a), cr-s*0.20*math.sin(a))
        if prev: out.append((prev[0], prev[1], p[0], p[1], ink))
        prev = p
    for k in range(6):
        a = math.pi*(k+0.5)/6
        x0 = cx-rw*math.cos(a)*0.92; y0 = cr-s*0.20*math.sin(a)*0.92
        out.append((x0, y0, x0+rnd.uniform(-6, 6), y0+s*(0.28+0.14*math.sin(a)), ink))
    return out

def dead_tree(cx, cy, s, ink=None, seed=0):
    """Bare trunk and three broken limbs."""
    ink = ink or PALETTE['dead']
    out = [(cx, cy, cx, cy-s, ink)]
    for fy, a, ln in ((0.55, -0.6, 0.40), (0.40, 0.72, 0.46), (0.70, 0.5, 0.28)):
        by = cy - s*fy
        out.append((cx, by, cx+math.sin(a)*s*ln, by-math.cos(a)*s*ln, ink))
    return out

def redwood(cx, cy, s, ink=None, seed=0, trunk=None):
    """Tall column with a narrow crown high up — Kithicor and Jaggedpine."""
    ink = ink or PALETTE['redwood']; trunk = trunk or PALETTE['trunk']
    out = []
    tw = s*0.10
    out += [(cx-tw, cy, cx-tw*0.7, cy-s*0.62, trunk),
            (cx+tw, cy, cx+tw*0.7, cy-s*0.62, trunk)]
    for i in range(3):
        by = cy - s*0.58 - (s*0.36)*i/3
        ap = by - s*0.36/3
        wv = s*0.24*(1 - i/3*0.5)
        out += [(cx-wv, by, cx, ap, ink), (cx, ap, cx+wv, by, ink)]
    for k in range(3):
        yy = cy - s*(0.12+0.16*k)
        out.append((cx-tw*0.9, yy, cx+tw*0.9, yy, trunk))
    return out

def palm(cx, cy, s, ink=None, seed=0, trunk=None):
    """Leaning trunk, splayed fronds — Oasis, Timorous."""
    ink = ink or PALETTE['palm']; trunk = trunk or PALETTE['trunk']
    rnd = random.Random(seed)
    lean = rnd.uniform(-0.18, 0.18)
    top = (cx + s*lean, cy - s*0.72)
    prev = None
    out = []
    for k in range(6):
        t = k/5.0
        p = (cx + s*lean*t*t, cy - s*0.72*t)
        if prev: out.append((prev[0], prev[1], p[0], p[1], trunk))
        prev = p
    for k in range(6):
        a = math.pi*(0.15 + 0.7*k/5)
        ex = top[0] + math.cos(a)*s*0.34
        ey = top[1] - math.sin(a)*s*0.20 + s*0.10
        mx = (top[0]+ex)/2; my = (top[1]+ey)/2 - s*0.10
        _P(out, [top, (mx, my), (ex, ey)], ink)
    return out


# ------------------------------------------------------------ undergrowth --
def bush(cx, cy, s, ink=None, seed=0):
    """Low rounded shrub."""
    ink = ink or PALETTE['under']
    out = []
    prev = None
    for k in range(13):
        a = math.pi + math.pi*k/12
        wob = 1.0 + 0.18*math.sin(5*a + seed)
        p = (cx+math.cos(a)*s*0.5*wob, cy+math.sin(a)*s*0.34*wob)
        if prev: out.append((prev[0], prev[1], p[0], p[1], ink))
        prev = p
    out.append((cx-s*0.5, cy, cx+s*0.5, cy, ink))
    return out

def fern(cx, cy, s, ink=None, seed=0):
    """Arching fronds from a single crown."""
    ink = ink or PALETTE['under']
    rnd = random.Random(seed)
    out = []
    for k in range(5):
        a = math.pi*(0.12 + 0.76*k/4) + rnd.uniform(-0.06, 0.06)
        ex = cx + math.cos(a)*s*0.5
        ey = cy - math.sin(a)*s*0.5
        mx = (cx+ex)/2 + math.cos(a)*s*0.06
        my = (cy+ey)/2 - s*0.12
        _P(out, [(cx, cy), (mx, my), (ex, ey)], ink)
        for j in (0.4, 0.7):
            bx = cx + (ex-cx)*j; by = cy + (my-cy)*j*1.2
            out.append((bx, by, bx+math.cos(a+1.4)*s*0.10, by-math.sin(a+1.4)*s*0.10, ink))
    return out

def reeds(cx, cy, s, ink=None, seed=0):
    """Waterside stems — pair with a shoreline."""
    ink = ink or PALETTE['reed']
    rnd = random.Random(seed)
    out = []
    for k in range(5):
        x = cx + (k-2)*s*0.12 + rnd.uniform(-2, 2)
        h = s*rnd.uniform(0.55, 1.0)
        lean = rnd.uniform(-0.18, 0.18)
        out.append((x, cy, x+lean*h, cy-h, ink))
        out.append((x+lean*h, cy-h, x+lean*h+s*0.06, cy-h+s*0.10, ink))
    return out

def mushrooms(cx, cy, s, ink=None, seed=0):
    """Cluster of caps — damp, dark forest floor."""
    ink = ink or PALETTE['fungus']
    rnd = random.Random(seed)
    out = []
    for k in range(3):
        x = cx + (k-1)*s*0.26 + rnd.uniform(-3, 3)
        h = s*rnd.uniform(0.3, 0.5)
        r = s*rnd.uniform(0.14, 0.22)
        out.append((x, cy, x, cy-h, ink))
        prev = None
        for j in range(7):
            a = math.pi + math.pi*j/6
            p = (x+math.cos(a)*r, cy-h+math.sin(a)*r*0.6)
            if prev: out.append((prev[0], prev[1], p[0], p[1], ink))
            prev = p
        out.append((x-r, cy-h, x+r, cy-h, ink))
    return out

def flowers(cx, cy, s, ink=None, seed=0):
    """Small blooms for meadow accents."""
    ink = ink or PALETTE['flower']
    rnd = random.Random(seed)
    out = []
    for k in range(4):
        x = cx + rnd.uniform(-s*0.4, s*0.4); y = cy + rnd.uniform(-s*0.2, s*0.2)
        h = s*rnd.uniform(0.24, 0.4)
        out.append((x, y, x, y-h, ink))
        for a in (0.4, 1.2, 2.0, 2.8):
            out.append((x, y-h, x+math.cos(a)*s*0.09, y-h-math.sin(a)*s*0.09, ink))
    return out

def grass_tuft(cx, cy, s, ink=None, seed=0):
    """A few blades — use grass_field in terrain.py for whole areas."""
    ink = ink or PALETTE['under']
    rnd = random.Random(seed)
    out = []
    for k in range(4):
        x = cx + (k-1.5)*s*0.14
        h = s*rnd.uniform(0.4, 0.8)
        out.append((x, cy, x+rnd.uniform(-0.3, 0.3)*h, cy-h, ink))
    return out


TREES = {'fir': fir, 'broadleaf': broadleaf, 'willow': willow,
         'dead_tree': dead_tree, 'redwood': redwood, 'palm': palm}
UNDERGROWTH = {'bush': bush, 'fern': fern, 'reeds': reeds,
               'mushrooms': mushrooms, 'flowers': flowers, 'grass_tuft': grass_tuft}
