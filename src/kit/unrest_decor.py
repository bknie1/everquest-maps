"""unrest_decor.py -- Estate of Unrest signature decor.

Brandon's in-game ground truth: scarecrows with jack-o-lantern heads on the
grounds, a grand rusticated "Rockefeller carriage" stone entry gate, small
death beetles in the yard, a checkered black/white floor in the manor's rear
octagon, and sandstone pillars (a pair outside the rear entrance, more inside).

All shapes return (x1, y1, x2, y2, ink) tuples; y is map-down (north = -y).
"""
import math
import random

POLE = (96, 74, 48)          # weathered timber
COAT = (88, 72, 50)          # ragged burlap coat
COAT_DK = (62, 50, 36)
STRAW = (152, 130, 78)
PUMPKIN = (188, 118, 44)
PUMPKIN_DK = (140, 84, 30)
GLOW = (214, 176, 84)
STONE = (128, 122, 110)      # rusticated granite
STONE_DK = (94, 90, 80)
SAND = (160, 124, 72)        # sandstone (kept off pale yellow -- parchment rule)
SAND_DK = (118, 90, 52)
CARPET = (122, 38, 34)       # deep red carpet
MOSAIC = (116, 92, 64)       # muted ceiling-mosaic lattice
CHECK = (44, 40, 36)         # checkerboard dark squares
BEETLE = (58, 50, 42)
BEETLE_HL = (110, 96, 70)


def _hatch(poly, ink, step, rnd=None, jitter=0.0):
    ys = [p[1] for p in poly]
    out = []
    y = min(ys) + step * 0.5
    while y < max(ys):
        xs = []
        for i in range(len(poly)):
            (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % len(poly)]
            if (y1 > y) != (y2 > y):
                xs.append(x1 + (y - y1) * (x2 - x1) / (y2 - y1))
        xs.sort()
        for i in range(0, len(xs) - 1, 2):
            if xs[i + 1] - xs[i] > step * 0.4:
                w = rnd.uniform(-jitter, jitter) if rnd else 0.0
                out.append((xs[i], y + w, xs[i + 1], y + w, ink))
        y += step
    return out


def _poly(poly, ink, close=True):
    n = len(poly) if close else len(poly) - 1
    return [(poly[i][0], poly[i][1], poly[(i + 1) % len(poly)][0],
             poly[(i + 1) % len(poly)][1], ink) for i in range(n)]


def scarecrow(cx, cy, s, seed=0, face=1):
    """A WALKING scarecrow-man mid-shamble: no planted cross-pole -- stride
    legs, loose swinging arms, ragged coat, straw at the wrists and a wisp
    trailing behind, jack-o-lantern head. (cx, cy) = ground, s = height."""
    rnd = random.Random(seed)
    f = 1 if face >= 0 else -1
    out = []

    def X(x):
        return cx + f * x

    hip_y = cy - s*0.42
    sh_y = cy - s*0.72

    # stride legs: thin timber-limbed, lead leg planted, rear leg pushing off
    for (hx, kx, ky, fx, fy) in (
            (-0.02, -0.13, -0.22, -0.17, 0.0),        # lead leg
            (0.03, 0.13, -0.20, 0.24, -0.06)):        # trailing leg, heel up
        pts = [(X(s*hx), hip_y), (X(s*kx), cy - s*0.20 + s*ky*0.0),
               (X(s*kx), cy + s*ky), (X(s*fx), cy + s*fy)]
        out.append((pts[0][0], pts[0][1], X(s*kx), cy + s*ky, POLE))
        out.append((X(s*kx), cy + s*ky, X(s*fx), cy + s*fy, POLE))
        out.append((pts[0][0] + f*0.5, pts[0][1], X(s*kx) + f*0.5, cy + s*ky, COAT_DK))
        # ragged trouser cuff tick
        out.append((X(s*kx) - s*0.03, cy + s*ky - s*0.06,
                    X(s*kx) + s*0.03, cy + s*ky - s*0.04, STRAW))

    # ragged coat torso, leaning into the walk, sawtooth hem swinging
    coat = [(X(-s*0.16), sh_y), (X(s*0.12), sh_y - s*0.015),
            (X(s*0.19), sh_y + s*0.10), (X(s*0.16), hip_y - s*0.02)]
    hem_pts = []
    n = 5
    for i in range(n + 1):
        t = i / n
        hx = X(s*0.16 - s*0.36 * t)
        hy = hip_y + s*0.07 + (s*0.075 if i % 2 else 0.0) \
            + rnd.uniform(-1, 1) * s*0.015 - t * s*0.03
        hem_pts.append((hx, hy))
    coat += hem_pts + [(X(-s*0.20), hip_y - s*0.04)]
    out += _poly(coat, COAT)
    for (x1, y1, x2, y2, c) in _hatch(coat, COAT, s*0.06, rnd, s*0.012):
        out.append((x1, y1, x2, y2,
                    COAT_DK if (x1 + x2) * 0.5 > cx + f * s*0.04 else c))

    # loose arms: lead arm swinging forward-down, rear arm dangling back
    arm_f = [(X(s*0.10), sh_y + s*0.03), (X(s*0.24), sh_y + s*0.16),
             (X(s*0.30), sh_y + s*0.30)]
    arm_b = [(X(-s*0.12), sh_y + s*0.02), (X(-s*0.24), sh_y + s*0.14),
             (X(-s*0.30), sh_y + s*0.28)]
    for pts in (arm_f, arm_b):
        out += _poly(pts, COAT, close=False)
        out += _poly([(x + f*0.6, y + 0.5) for (x, y) in pts], COAT_DK, close=False)
        # straw bursting from the sleeve end
        ex, ey = pts[-1]
        d = 1 if pts is arm_f else -1
        for k in range(3):
            a = (k - 1) * 0.4
            out.append((ex, ey, ex + f * d * s*0.06 * math.cos(a),
                        ey + s*0.06 * math.sin(a) + s*0.03, STRAW))

    # straw wisp trailing off the coat-tail
    wx, wy = X(-s*0.20), hip_y + s*0.04
    out.append((wx, wy, wx - f * s*0.10, wy + s*0.02, STRAW))
    out.append((wx - f * s*0.10, wy + s*0.02, wx - f * s*0.16, wy - s*0.015, STRAW))

    # jack-o-lantern head, tipped into the walk
    hr = s*0.155
    hx0, hy0 = X(s*0.05), sh_y - hr * 0.95
    ring = []
    for k in range(13):
        a = 2 * math.pi * k / 12
        ring.append((hx0 + math.cos(a) * hr, hy0 + math.sin(a) * hr * 0.88))
    out += _poly(ring, PUMPKIN)
    # gourd ribs
    for rx in (-0.55, 0.0, 0.55):
        out.append((hx0 + rx * hr, hy0 - hr * 0.82, hx0 + rx * hr * 1.15,
                    hy0 + hr * 0.82, PUMPKIN_DK))
    # stem
    out.append((hx0 - s*0.015, hy0 - hr * 0.88, hx0 - s*0.03, hy0 - hr * 1.15, POLE))
    out.append((hx0 + s*0.015, hy0 - hr * 0.88, hx0 + s*0.02, hy0 - hr * 1.12, POLE))
    # triangle eyes (filled with a couple of glow strokes)
    for ex in (-0.42, 0.42):
        e0 = (hx0 + ex * hr - hr*0.16, hy0 - hr*0.10)
        e1 = (hx0 + ex * hr + hr*0.16, hy0 - hr*0.10)
        e2 = (hx0 + ex * hr, hy0 - hr*0.38)
        out += _poly([e0, e1, e2], GLOW)
        out.append(((e0[0] + e2[0]) / 2, (e0[1] + e2[1]) / 2,
                    (e1[0] + e2[0]) / 2, (e1[1] + e2[1]) / 2, GLOW))
    # triangle nose
    out += _poly([(hx0 - hr*0.09, hy0 + hr*0.12), (hx0 + hr*0.09, hy0 + hr*0.12),
                  (hx0, hy0 - hr*0.06)], GLOW)
    # jagged grin: zigzag across the lower face
    gz = []
    m = 6
    for i in range(m + 1):
        t = i / m
        gx = hx0 - hr*0.62 + hr*1.24 * t
        gy = hy0 + hr*0.42 + (hr*0.16 if i % 2 else 0.0) - hr*0.10 * abs(2*t - 1)
        gz.append((gx, gy))
    out += _poly(gz, GLOW, close=False)
    out += _poly([(p[0], p[1] + hr*0.14) for p in gz], GLOW, close=False)
    return out


def death_beetle(cx, cy, s, seed=0):
    """A small death beetle: oval carapace, wing-case split, head, six legs.
    12-20 strokes; keep s small (~6-9 units)."""
    rnd = random.Random(seed)
    a0 = rnd.uniform(0, math.pi)
    ca, sa = math.cos(a0), math.sin(a0)

    def R(px, py):
        return (cx + px * ca - py * sa, cy + px * sa + py * ca)

    out = []
    body = [R(math.cos(2*math.pi*k/8) * s*0.5, math.sin(2*math.pi*k/8) * s*0.34)
            for k in range(8)]
    out += _poly(body, BEETLE)
    out += _poly([R(-s*0.5, 0), R(s*0.35, 0)], BEETLE, close=False)   # wing split
    hx, hy = R(s*0.62, 0)
    out += _poly([R(s*0.5, -s*0.14), (hx, hy), R(s*0.5, s*0.14)], BEETLE, close=False)
    for k in (-1, 0, 1):
        for side in (-1, 1):
            j0 = R(k * s*0.28, side * s*0.32)
            j1 = R(k * s*0.28 - s*0.14, side * s*0.58)
            out.append((j0[0], j0[1], j1[0], j1[1], BEETLE))
    m0 = R(s*0.70, -s*0.10); m1 = R(s*0.82, -s*0.20)
    m2 = R(s*0.70, s*0.10);  m3 = R(s*0.82, s*0.20)
    out.append((m0[0], m0[1], m1[0], m1[1], BEETLE_HL))
    out.append((m2[0], m2[1], m3[0], m3[1], BEETLE_HL))
    return out


def stone_gate(cx, cy, s, seed=0):
    """The Rockefeller-carriage entry: two heavy rusticated piers, a shallow
    arch between, block coursing, a hung lantern. (cx, cy) = centre of the
    opening at ground line, s = opening half-width."""
    rnd = random.Random(seed)
    out = []
    pw = s * 0.55                       # pier width
    ph = s * 0.95                       # pier "depth" on the map (drawn tall)
    for side in (-1, 1):
        x0 = cx + side * s - (pw if side < 0 else 0)
        x1 = x0 + pw
        y0, y1 = cy - ph * 0.5, cy + ph * 0.5
        pier = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        out += _poly(pier, STONE)
        # cap slab, slightly proud
        out += _poly([(x0 - s*0.08, y0 - s*0.14), (x1 + s*0.08, y0 - s*0.14),
                      (x1 + s*0.08, y0), (x0 - s*0.08, y0)], STONE)
        # block coursing: staggered joints
        rows = 4
        for r in range(1, rows):
            yy = y0 + (y1 - y0) * r / rows
            out.append((x0, yy, x1, yy, STONE_DK))
            jx = x0 + pw * (0.33 if r % 2 else 0.66)
            yn = y0 + (y1 - y0) * (r + 1) / rows if r + 1 <= rows else y1
            out.append((jx, yy, jx, min(yy + (y1 - y0) / rows, y1), STONE_DK))
        out.append((x0 + pw * 0.5, y0, x0 + pw * 0.5,
                    y0 + (y1 - y0) / rows, STONE_DK))
        # rustication ticks on the outer face
        fx = x0 if side < 0 else x1
        for k in range(3):
            yy = y0 + (y1 - y0) * rnd.uniform(0.15, 0.85)
            out.append((fx, yy, fx - side * s*0.06, yy + s*0.03, STONE_DK))

    # shallow segmental arch spanning the opening
    n = 8
    arc = []
    for k in range(n + 1):
        t = k / n
        ax = cx - s + 2 * s * t
        ay = cy - ph * 0.5 - s*0.30 * math.sin(math.pi * t)
        arc.append((ax, ay))
    out += _poly(arc, STONE, close=False)
    out += _poly([(x, y + s*0.12) for (x, y) in arc], STONE, close=False)
    # voussoir joints
    for k in range(1, n):
        t = k / n
        (x1_, y1_) = arc[k]
        out.append((x1_, y1_, x1_, y1_ + s*0.12, STONE_DK))
    # keystone
    out += _poly([(cx - s*0.09, cy - ph*0.5 - s*0.34), (cx + s*0.09, cy - ph*0.5 - s*0.34),
                  (cx + s*0.06, cy - ph*0.5 - s*0.16), (cx - s*0.06, cy - ph*0.5 - s*0.16)],
                 STONE)
    # lantern hung from the arch centre
    ly = cy - ph * 0.5 + s*0.10
    out.append((cx, cy - ph*0.5 - s*0.02, cx, ly, STONE_DK))
    out += _poly([(cx - s*0.07, ly), (cx, ly - s*0.09), (cx + s*0.07, ly),
                  (cx, ly + s*0.11)], GLOW)
    for k in range(4):
        a = math.pi * 0.25 + k * math.pi * 0.5
        out.append((cx + math.cos(a) * s*0.10, ly + math.sin(a) * s*0.10,
                    cx + math.cos(a) * s*0.17, ly + math.sin(a) * s*0.17, GLOW))
    return out


def checkerboard(cx, cy, cell, n=6, seed=0):
    """A small black/white checkered floor motif: n x n cells centred on
    (cx, cy); dark squares hatched solid, light squares left parchment."""
    out = []
    half = n * cell / 2.0
    x0, y0 = cx - half, cy - half
    out += _poly([(x0, y0), (x0 + n*cell, y0), (x0 + n*cell, y0 + n*cell),
                  (x0, y0 + n*cell)], CHECK)
    for r in range(n):
        for c in range(n):
            if (r + c) % 2 == 0:
                continue
            sx, sy = x0 + c * cell, y0 + r * cell
            k = cell * 0.22
            yy = sy + k * 0.5
            while yy < sy + cell - k * 0.25:
                out.append((sx + 0.15, yy, sx + cell - 0.15, yy, CHECK))
                yy += k
    return out


def pillar(cx, cy, s, seed=0):
    """A sandstone pillar footprint marker: filled square base, proud cap
    ticks. s = half-width (keep ~3-5 units)."""
    out = []
    out += _poly([(cx - s, cy - s), (cx + s, cy - s), (cx + s, cy + s),
                  (cx - s, cy + s)], SAND)
    yy = cy - s + s * 0.45
    while yy < cy + s - s * 0.2:
        out.append((cx - s + 0.2, yy, cx + s - 0.2, yy, SAND))
        yy += s * 0.45
    # cap: four corner ticks proud of the base
    for dx in (-1, 1):
        for dy in (-1, 1):
            out.append((cx + dx * s, cy + dy * s,
                        cx + dx * (s + s*0.45), cy + dy * (s + s*0.45), SAND_DK))
    return out
