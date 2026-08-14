"""flora_hd.py -- high-fidelity flora.

The originals were wireframes: a fir was 13 lines, a dead tree 4. The shapes that
read well on the maps -- bookshelf, root_bunch, iksar_glyph -- are 160-330 lines
because they use hatched fill and real internal structure. These match that.

Every shape: tapered trunk drawn as two edges with bark ticks, branch structure,
foliage built from overlapping hatched lobes, and a shadow side.
"""
import math, random

PALETTE = {
    'fir':        (68, 100, 62),  'fir_north': (84, 112, 96),
    'broadleaf':  (86, 132, 70),  'willow':    (104, 146, 92),
    'palm':       (96, 140, 84),  'redwood':   (72, 104, 66),
    'dead':       (120, 108, 88), 'trunk':     (96, 78, 54),
    'trunk_dark': (70, 56, 38),   'under':     (78, 116, 66),
    'flower':     (176, 108, 128),'fungus':    (150, 130, 150),
    'reed':       (110, 142, 90),
}


def _hatch(poly, ink, step):
    """Fill a polygon with horizontal hatching (even-odd)."""
    ys = [p[1] for p in poly]
    out = []
    y = min(ys) + step*0.5
    while y < max(ys):
        xs = []
        for i in range(len(poly)):
            (x1, y1), (x2, y2) = poly[i], poly[(i+1) % len(poly)]
            if (y1 > y) != (y2 > y):
                xs.append(x1 + (y-y1)*(x2-x1)/(y2-y1))
        xs.sort()
        for i in range(0, len(xs)-1, 2):
            if xs[i+1]-xs[i] > 0.6:
                out.append((xs[i], y, xs[i+1], y, ink))
        y += step
    return out


def _outline(poly, ink):
    return [(poly[i][0], poly[i][1], poly[(i+1) % len(poly)][0],
             poly[(i+1) % len(poly)][1], ink) for i in range(len(poly))]


def _trunk(cx, base_y, top_y, w0, w1, ink, dark, rnd, lean=0.0):
    """A tapered trunk with bark ticks and a shaded side."""
    out = []
    n = 7
    left = []; right = []
    for i in range(n+1):
        t = i/n
        y = base_y + (top_y-base_y)*t
        x = cx + lean*t*t
        w = w0 + (w1-w0)*t
        wob = rnd.uniform(-w0*0.12, w0*0.12)
        left.append((x-w+wob, y)); right.append((x+w+wob, y))
    out += _hatch(left + right[::-1], ink, max(0.8, abs(top_y-base_y)*0.055))
    for i in range(len(left)-1):
        out.append((left[i][0], left[i][1], left[i+1][0], left[i+1][1], dark))
        out.append((right[i][0], right[i][1], right[i+1][0], right[i+1][1], ink))
    for i in range(1, len(left)-1, 2):          # bark ticks
        out.append((left[i][0], left[i][1], left[i][0]+ (right[i][0]-left[i][0])*0.45,
                    left[i][1]+abs(top_y-base_y)*0.02, dark))
    return out, left, right


def _lobe(cx, cy, rx, ry, ink, dark, rnd, step):
    """One irregular foliage lobe: hatched body, ragged outline, shaded underside."""
    poly = []
    n = 16
    for k in range(n):
        a = 2*math.pi*k/n
        rr = rnd.uniform(0.82, 1.18)
        poly.append((cx+math.cos(a)*rx*rr, cy+math.sin(a)*ry*rr))
    out = _hatch(poly, ink, step)
    out += _outline(poly, ink)
    lower = [p for p in poly if p[1] > cy]
    if len(lower) > 2:
        out += _hatch(lower + [(cx, cy)], dark, step*1.6)
    return out


def fir(cx, cy, s, ink=None, seed=0, trunk=None):
    """A conifer: tapered bole, tiered boughs, needled edges."""
    rnd = random.Random(seed)
    ink = ink or PALETTE['fir']; trunk = trunk or PALETTE['trunk']
    dark = tuple(max(0, c-26) for c in ink)
    tdark = PALETTE['trunk_dark']
    out, L, R = _trunk(cx, cy, cy-s*0.55, s*0.075, s*0.045, trunk, tdark, rnd)
    tiers = 5
    for k in range(tiers):
        t = k/(tiers-1)
        y = cy - s*0.30 - s*0.72*t
        half = s*(0.52 - 0.36*t)
        drop = s*0.20*(1-t*0.4)
        poly = [(cx, y-s*0.16)]
        steps = 7
        for i in range(steps+1):                 # right side, notched
            u = i/steps
            poly.append((cx+half*u, y+drop*u + (s*0.035 if i % 2 else 0)))
        for i in range(steps+1):                 # left side back
            u = 1-i/steps
            poly.append((cx-half*u, y+drop*u + (s*0.035 if i % 2 else 0)))
        out += _hatch(poly, ink if k % 2 else dark, max(0.9, s*0.055))
        out += _outline(poly, ink)
    out.append((cx, cy-s*1.02, cx, cy-s*1.20, ink))
    return out


def broadleaf(cx, cy, s, ink=None, seed=0, trunk=None):
    """A deciduous tree: forking trunk, three to five hatched crown lobes."""
    rnd = random.Random(seed)
    ink = ink or PALETTE['broadleaf']; trunk = trunk or PALETTE['trunk']
    dark = tuple(max(0, c-30) for c in ink)
    tdark = PALETTE['trunk_dark']
    out, L, R = _trunk(cx, cy, cy-s*0.62, s*0.085, s*0.040, trunk, tdark, rnd)
    for k in range(3):                            # branches into the crown
        a = -math.pi/2 + rnd.uniform(-0.85, 0.85)
        x0, y0 = cx, cy-s*0.55
        x1, y1 = x0+math.cos(a)*s*0.34, y0+math.sin(a)*s*0.34
        out.append((x0, y0, x1, y1, trunk))
        out.append((x1, y1, x1+math.cos(a)*s*0.16, y1+math.sin(a)*s*0.16, tdark))
    n = rnd.randint(3, 5)
    for k in range(n):
        a = 2*math.pi*k/n + rnd.uniform(-0.3, 0.3)
        lx = cx + math.cos(a)*s*0.30
        ly = cy - s*0.86 + math.sin(a)*s*0.20
        out += _lobe(lx, ly, s*rnd.uniform(0.30, 0.42), s*rnd.uniform(0.24, 0.34),
                     ink, dark, rnd, max(0.9, s*0.050))
    return out


def redwood(cx, cy, s, ink=None, seed=0, trunk=None):
    """A tall redwood: very long bole, narrow crown high up."""
    rnd = random.Random(seed)
    ink = ink or PALETTE['redwood']; trunk = trunk or PALETTE['trunk']
    dark = tuple(max(0, c-26) for c in ink)
    out, L, R = _trunk(cx, cy, cy-s*1.25, s*0.085, s*0.035,
                       trunk, PALETTE['trunk_dark'], rnd)
    for k in range(4):
        t = k/3
        y = cy - s*0.80 - s*0.62*t
        half = s*(0.34 - 0.19*t)
        poly = [(cx, y-s*0.13)]
        for i in range(6):
            u = i/5; poly.append((cx+half*u, y+s*0.14*u))
        for i in range(6):
            u = 1-i/5; poly.append((cx-half*u, y+s*0.14*u))
        out += _hatch(poly, ink if k % 2 else dark, max(0.9, s*0.048))
        out += _outline(poly, ink)
    return out


def palm(cx, cy, s, ink=None, seed=0, trunk=None):
    """A palm: curved bole with ring scars, arching hatched fronds, coconuts."""
    rnd = random.Random(seed)
    ink = ink or PALETTE['palm']; trunk = trunk or PALETTE['trunk']
    dark = tuple(max(0, c-28) for c in ink)
    tdark = PALETTE['trunk_dark']
    lean = s*rnd.uniform(-0.22, 0.22)
    out, L, R = _trunk(cx, cy, cy-s*0.92, s*0.070, s*0.048,
                       trunk, tdark, rnd, lean=lean)
    tx = cx + lean; ty = cy - s*0.92
    for i in range(1, 6):                        # ring scars
        t = i/6
        y = cy + (ty-cy)*t
        x = cx + lean*t*t
        out.append((x-s*0.062, y, x+s*0.062, y, tdark))
    for k in range(6):
        a = math.pi*(0.12 + 0.76*k/5) + math.pi
        ex = tx + math.cos(a)*s*0.62
        ey = ty + math.sin(a)*s*0.30 + s*0.10
        mx = (tx+ex)/2; my = min(ty, ey) - s*0.16
        spine = [(tx, ty)]
        for i in range(1, 9):
            u = i/8
            spine.append(((1-u)**2*tx + 2*(1-u)*u*mx + u*u*ex,
                          (1-u)**2*ty + 2*(1-u)*u*my + u*u*ey))
        wid = s*0.12
        poly = [(p[0], p[1]-wid*(1-i/len(spine))) for i, p in enumerate(spine)]
        poly += [(p[0], p[1]+wid*(1-i/len(spine)))
                 for i, p in reversed(list(enumerate(spine)))]
        out += _hatch(poly, ink if k % 2 else dark, max(0.8, s*0.040))
        for i in range(len(spine)-1):
            out.append((spine[i][0], spine[i][1], spine[i+1][0], spine[i+1][1], dark))
    for k in range(3):
        a = 2*math.pi*k/3
        out += _lobe(tx+math.cos(a)*s*0.07, ty+s*0.06+math.sin(a)*s*0.04,
                     s*0.038, s*0.034, trunk, tdark, rnd, s*0.030)
    return out


def willow(cx, cy, s, ink=None, seed=0, trunk=None):
    """A willow: broad bole, drooping hatched curtains."""
    rnd = random.Random(seed)
    ink = ink or PALETTE['willow']; trunk = trunk or PALETTE['trunk']
    dark = tuple(max(0, c-30) for c in ink)
    out, L, R = _trunk(cx, cy, cy-s*0.50, s*0.095, s*0.055,
                       trunk, PALETTE['trunk_dark'], rnd)
    for k in range(4):
        a = 2*math.pi*k/4 + 0.4
        lx = cx+math.cos(a)*s*0.26; ly = cy-s*0.72+math.sin(a)*s*0.12
        out += _lobe(lx, ly, s*0.34, s*0.22, ink, dark, rnd, max(0.9, s*0.048))
    for k in range(9):                            # trailing withes
        x = cx + s*rnd.uniform(-0.55, 0.55)
        y0 = cy - s*0.62 + abs(x-cx)*0.32
        px, py = x, y0
        for i in range(5):
            nx = px + rnd.uniform(-s*0.05, s*0.05)
            ny = py + s*0.13
            out.append((px, py, nx, ny, ink if i % 2 else dark))
            px, py = nx, ny
    return out


def dead_tree(cx, cy, s, ink=None, seed=0):
    """A bare snag: split bole, broken limbs, hollows."""
    rnd = random.Random(seed)
    ink = ink or PALETTE['dead']
    dark = tuple(max(0, c-34) for c in ink)
    out, L, R = _trunk(cx, cy, cy-s*0.95, s*0.070, s*0.028, ink, dark, rnd,
                       lean=s*rnd.uniform(-0.12, 0.12))
    for k in range(5):
        t = rnd.uniform(0.25, 0.90)
        y = cy - s*0.95*t
        a = rnd.choice([-1, 1])*rnd.uniform(0.5, 1.15)
        x1 = cx + math.cos(a)*s*0.40*abs(math.cos(a))
        px, py = cx, y
        for i in range(3):
            nx = px + (x1-cx)/3 + rnd.uniform(-s*0.04, s*0.04)
            ny = py - s*rnd.uniform(0.04, 0.12)
            out.append((px, py, nx, ny, ink if i % 2 else dark))
            px, py = nx, ny
        if rnd.random() < 0.6:
            out.append((px, py, px+rnd.uniform(-s*0.10, s*0.10), py-s*0.10, dark))
    for k in range(2):                            # hollows
        hy = cy - s*rnd.uniform(0.25, 0.7)
        out += _hatch([(cx-s*0.035, hy), (cx+s*0.02, hy-s*0.03),
                       (cx+s*0.03, hy+s*0.05), (cx-s*0.02, hy+s*0.06)],
                      dark, s*0.022)
    return out


def bush(cx, cy, s, ink=None, seed=0):
    rnd = random.Random(seed)
    ink = ink or PALETTE['under']; dark = tuple(max(0, c-30) for c in ink)
    out = []
    for k in range(rnd.randint(3, 4)):
        out += _lobe(cx+rnd.uniform(-s*0.24, s*0.24), cy-s*0.18+rnd.uniform(-s*0.10, s*0.10),
                     s*rnd.uniform(0.22, 0.34), s*rnd.uniform(0.16, 0.24),
                     ink, dark, rnd, max(0.8, s*0.055))
    for k in range(4):
        x = cx+rnd.uniform(-s*0.22, s*0.22)
        out.append((x, cy, x+rnd.uniform(-s*0.04, s*0.04), cy-s*0.16, dark))
    return out


def fern(cx, cy, s, ink=None, seed=0):
    """A fern: arching fronds with pinnate leaflets."""
    rnd = random.Random(seed)
    ink = ink or PALETTE['under']; dark = tuple(max(0, c-30) for c in ink)
    out = []
    for k in range(rnd.randint(5, 7)):
        a = -math.pi/2 + rnd.uniform(-1.0, 1.0)
        ln = s*rnd.uniform(0.45, 0.72)
        spine = [(cx, cy)]
        px, py = cx, cy
        for i in range(6):
            u = (i+1)/6
            px = cx + math.cos(a)*ln*u
            py = cy + math.sin(a)*ln*u + s*0.16*u*u
            spine.append((px, py))
        for i in range(len(spine)-1):
            out.append((spine[i][0], spine[i][1], spine[i+1][0], spine[i+1][1],
                        ink if i % 2 else dark))
        for i in range(1, len(spine)):
            w = s*0.11*(1-i/len(spine))
            nx, ny = spine[i]
            out.append((nx, ny, nx-w, ny-w*0.5, ink))
            out.append((nx, ny, nx+w, ny-w*0.5, ink))
    return out


def reeds(cx, cy, s, ink=None, seed=0):
    rnd = random.Random(seed)
    ink = ink or PALETTE['reed']; dark = tuple(max(0, c-28) for c in ink)
    out = []
    for k in range(rnd.randint(6, 9)):
        x = cx + rnd.uniform(-s*0.32, s*0.32)
        h = s*rnd.uniform(0.45, 0.85)
        lean = rnd.uniform(-s*0.12, s*0.12)
        px, py = x, cy
        for i in range(4):
            nx = x + lean*((i+1)/4)**2
            ny = cy - h*(i+1)/4
            out.append((px, py, nx, ny, ink if i % 2 else dark))
            px, py = nx, ny
        if rnd.random() < 0.5:                    # seed head
            out += _hatch([(px-s*0.020, py), (px+s*0.020, py),
                           (px+s*0.020, py-s*0.10), (px-s*0.020, py-s*0.10)],
                          dark, s*0.026)
    return out


def flowers(cx, cy, s, ink=None, seed=0):
    rnd = random.Random(seed)
    ink = ink or PALETTE['flower']; leaf = PALETTE['under']
    out = []
    for k in range(rnd.randint(3, 5)):
        x = cx+rnd.uniform(-s*0.28, s*0.28); h = s*rnd.uniform(0.24, 0.42)
        out.append((x, cy, x, cy-h, leaf))
        out.append((x, cy-h*0.5, x+s*0.09, cy-h*0.62, leaf))
        for p in range(5):
            a = 2*math.pi*p/5
            out.append((x, cy-h, x+math.cos(a)*s*0.070, cy-h+math.sin(a)*s*0.070, ink))
            out.append((x+math.cos(a)*s*0.070, cy-h+math.sin(a)*s*0.070,
                        x+math.cos(a+0.6)*s*0.070, cy-h+math.sin(a+0.6)*s*0.070, ink))
    return out


def mushrooms(cx, cy, s, ink=None, seed=0):
    rnd = random.Random(seed)
    ink = ink or PALETTE['fungus']; dark = tuple(max(0, c-34) for c in ink)
    out = []
    for k in range(rnd.randint(2, 4)):
        x = cx+rnd.uniform(-s*0.26, s*0.26); h = s*rnd.uniform(0.18, 0.32)
        r = s*rnd.uniform(0.11, 0.18)
        out += [(x-r*0.30, cy, x-r*0.24, cy-h, ink), (x+r*0.30, cy, x+r*0.24, cy-h, ink)]
        cap = []
        for j in range(11):
            a = math.pi*(j/10)
            cap.append((x+math.cos(a)*r, cy-h-math.sin(a)*r*0.72))
        cap.append((x+r, cy-h)); cap.append((x-r, cy-h))
        out += _hatch(cap, ink, max(0.7, s*0.032))
        out += _outline(cap, dark)
        for j in range(3):
            out.append((x-r*0.5+r*j*0.5, cy-h-r*0.30, x-r*0.4+r*j*0.5, cy-h-r*0.44, dark))
    return out


def grass_tuft(cx, cy, s, ink=None, seed=0):
    rnd = random.Random(seed)
    ink = ink or PALETTE['under']; dark = tuple(max(0, c-26) for c in ink)
    out = []
    for k in range(rnd.randint(5, 8)):
        x = cx+rnd.uniform(-s*0.24, s*0.24)
        h = s*rnd.uniform(0.18, 0.36)
        lean = rnd.uniform(-s*0.14, s*0.14)
        out.append((x, cy, x+lean*0.5, cy-h*0.6, ink))
        out.append((x+lean*0.5, cy-h*0.6, x+lean, cy-h, dark))
    return out


TREES = {'fir': fir, 'broadleaf': broadleaf, 'palm': palm,
         'willow': willow, 'redwood': redwood, 'dead_tree': dead_tree}
UNDERGROWTH = {'bush': bush, 'fern': fern, 'reeds': reeds,
               'flowers': flowers, 'mushrooms': mushrooms, 'grass_tuft': grass_tuft}
ALL = dict(TREES); ALL.update(UNDERGROWTH)
