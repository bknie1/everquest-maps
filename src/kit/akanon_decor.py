"""akanon_decor.py -- Ak'Anon: the gnome city in a CAVE, not a forest.

The margins carried 4,500 strokes of broadleaf forest green, which is wrong on
its face: Ak'Anon sits inside a mountain cavern. This kit supplies what belongs
there instead -- clockwork denizens, tesla arcs, and cave rock.

Built in the solid-silhouette style of fauna_sil (a few filled polygons plus one
signature accent), because that is what survives at map scale.

    from akanon_decor import clockwork_gnome, clockwork_spider, tesla_arc, \
        stalactite, stalagmite
    segs = clockwork_spider(cx, cy, s, seed=3)
"""
import math
import random

BRASS = (172, 140, 66)
IRON = (122, 122, 132)
DARK = (62, 58, 64)
TESLA = (46, 180, 96)          # the zone's existing bright green -- matched
TESLA_HOT = (150, 240, 170)
GLASS = (150, 190, 200)


def _solid(poly, ink, step=1.6):
    ys = [p[1] for p in poly]
    out = []
    y = min(ys)
    while y < max(ys):
        xs = []
        for i in range(len(poly)):
            (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % len(poly)]
            if (y1 > y) != (y2 > y):
                xs.append(x1 + (y - y1) * (x2 - x1) / (y2 - y1))
        xs.sort()
        for i in range(0, len(xs) - 1, 2):
            if xs[i + 1] - xs[i] > 0.4:
                out.append((xs[i], y, xs[i + 1], y, ink))
        y += step
    return out


def _edge(poly, ink, out):
    for i in range(len(poly)):
        a, b = poly[i], poly[(i + 1) % len(poly)]
        out.append((a[0], a[1], b[0], b[1], ink))


class _F:
    def __init__(self, cx, cy, s, face=-1):
        self.cx, self.cy, self.s, self.f = cx, cy, s, face
        self.out = []
        self.step = max(0.7, s * 0.014)

    def P(self, pts):
        return [(self.cx + self.f * x * self.s, self.cy - y * self.s) for x, y in pts]

    def L(self, x1, y1, x2, y2, c):
        self.out.append((self.cx + self.f * x1 * self.s, self.cy - y1 * self.s,
                         self.cx + self.f * x2 * self.s, self.cy - y2 * self.s, c))

    def poly(self, pts, fill, line=None, pitch=1.0):
        pp = self.P(pts)
        self.out += _solid(pp, fill, self.step * pitch)
        _edge(pp, line or fill, self.out)

    def disc(self, x, y, r, fill, n=12):
        self.poly([(x + r * math.cos(t * 2 * math.pi / n),
                    y + r * 0.95 * math.sin(t * 2 * math.pi / n)) for t in range(n)],
                  fill)


def clockwork_gnome(cx, cy, s, seed=0, face=-1):
    """Gnome-shaped automaton: boxy riveted torso, gear on the chest, dome head
    with a single glowing lens and an antenna. Reads as 'gnome' by proportion
    (huge head, tiny body) and 'machine' by its hard edges."""
    F = _F(cx, cy, s, face)
    F.poly([(-0.10, 0.02), (-0.12, 0.20), (0.12, 0.20), (0.10, 0.02),
            (0.04, 0.02), (0.05, 0.14), (-0.05, 0.14), (-0.04, 0.02)], DARK, DARK)
    F.poly([(-0.13, 0.20), (-0.15, 0.34), (-0.11, 0.44), (0.11, 0.44),
            (0.15, 0.34), (0.13, 0.20)], IRON, DARK)                     # torso
    F.disc(-0.01, 0.32, 0.07, BRASS)                                     # chest gear
    for k in range(6):                                                   # gear teeth
        a = k * math.pi / 3
        F.L(-0.01 + 0.07 * math.cos(a), 0.32 + 0.07 * math.sin(a),
            -0.01 + 0.10 * math.cos(a), 0.32 + 0.10 * math.sin(a), BRASS)
    F.poly([(-0.16, 0.42), (-0.20, 0.30), (-0.17, 0.28), (-0.13, 0.40)], IRON, DARK)
    F.poly([(0.16, 0.42), (0.20, 0.30), (0.17, 0.28), (0.13, 0.40)], IRON, DARK)
    F.disc(-0.01, 0.58, 0.14, IRON, n=14)                                # big dome head
    F.disc(-0.06, 0.60, 0.045, TESLA)                                    # glowing lens
    F.L(0.02, 0.70, 0.08, 0.86, BRASS)                                   # antenna
    F.disc(0.08, 0.88, 0.025, TESLA_HOT)
    return F.out


def clockwork_spider(cx, cy, s, seed=0, face=-1):
    """Eight angular legs off a riveted brass carapace, single red-green lens.
    Legs are drawn as bent segments so it reads mechanical, not organic."""
    F = _F(cx, cy, s, face)
    rnd = random.Random(seed)
    body = [(-0.20, 0.30), (-0.10, 0.42), (0.10, 0.42), (0.20, 0.30),
            (0.16, 0.18), (-0.16, 0.18)]
    for side in (-1, 1):
        for k in range(4):
            hx = side * 0.16
            hy = 0.36 - k * 0.05
            kx = side * (0.34 + k * 0.05)
            ky = hy + 0.10 - k * 0.02
            fx = side * (0.42 + k * 0.06)
            F.L(hx, hy, kx, ky, IRON)                    # femur up
            F.L(kx, ky, fx, 0.02, IRON)                  # tibia down to floor
            F.L(fx, 0.02, fx + side * 0.03, 0.02, DARK)  # foot
    F.poly(body, BRASS, DARK)
    F.disc(0.0, 0.30, 0.06, IRON)                        # dorsal plate
    F.poly([(-0.16, 0.24), (-0.24, 0.28), (-0.24, 0.20), (-0.16, 0.19)], IRON, DARK)
    F.disc(-0.21, 0.24, 0.035, TESLA)                    # eye lens
    for k in range(3):                                   # rivets
        F.L(-0.08 + k * 0.08, 0.38, -0.07 + k * 0.08, 0.38, DARK)
    return F.out


def tesla_arc(cx, cy, s, seed=0, face=-1):
    """Ak'Anon's signature: a green lightning arc between two brass terminals.
    The bolt is a jagged polyline with a hot core, so it reads as electricity
    rather than a crack in the rock."""
    F = _F(cx, cy, s, face)
    rnd = random.Random(seed)
    for x in (-0.22, 0.22):                              # terminals
        F.poly([(x - 0.05, 0.02), (x - 0.04, 0.16), (x + 0.04, 0.16),
                (x + 0.05, 0.02)], IRON, DARK)
        F.disc(x, 0.19, 0.05, BRASS)
    for pass_ in range(2):                               # bolt + hot core
        ink = TESLA if pass_ == 0 else TESLA_HOT
        jitter = 0.09 if pass_ == 0 else 0.05
        px, py = -0.20, 0.20
        for k in range(1, 7):
            nx = -0.20 + 0.40 * k / 6
            ny = 0.20 + rnd.uniform(-jitter, jitter) + (0.10 if k % 2 else -0.02)
            F.L(px, py, nx, ny, ink)
            if pass_ == 0 and k in (2, 4):               # forked branches
                F.L(nx, ny, nx + rnd.uniform(-0.08, 0.08), ny + 0.12, ink)
            px, py = nx, ny
        F.L(px, py, 0.20, 0.20, ink)
    return F.out


def glow_diamond(cx, cy, s, seed=0, face=-1):
    """Ak'Anon's actual lighting: a green glowing diamond on a bracket.

    Faceted rather than flat -- lit upper-left facets, shaded lower-right, a
    hot core and a radiating halo. The same facet treatment the historical
    (EQOA) POI diamonds want, so `facets()` below is shared with them.
    """
    F = _F(cx, cy, s, face)
    r = 0.20
    cyd = 0.44
    for k, rr in ((0, r * 1.9), (1, r * 1.5)):          # halo rings, faint
        pts = [(0 + rr * math.cos(t * math.pi / 2), cyd + rr * math.sin(t * math.pi / 2))
               for t in range(4)]
        for i in range(4):
            F.L(*pts[i], *pts[(i + 1) % 4], TESLA if k else (34, 120, 70))
    for k in range(8):                                   # radiating glints
        a = k * math.pi / 4
        F.L(0 + r * 1.15 * math.cos(a), cyd + r * 1.15 * math.sin(a),
            0 + r * 1.55 * math.cos(a), cyd + r * 1.55 * math.sin(a), TESLA)
    F.out += facets(F, 0.0, cyd, r)
    F.poly([(-0.05, 0.0), (0.05, 0.0), (0.03, cyd - r), (-0.03, cyd - r)],
           IRON, DARK)                                   # bracket
    return F.out


def facets(F, x, y, r, lit=TESLA_HOT, mid=TESLA, dark=(24, 96, 56)):
    """A shaded diamond: four facets, light from the upper left.

    Shared with the historical POI diamonds, which are still flat outlines --
    a diamond only reads as a gem once its facets disagree about the light.
    """
    top, bot = (x, y + r), (x, y - r)
    left, right = (x - r * 0.72, y), (x + r * 0.72, y)
    out = []
    for tri, ink in (((top, left, (x, y)), lit),
                     ((top, right, (x, y)), mid),
                     ((bot, left, (x, y)), mid),
                     ((bot, right, (x, y)), dark)):
        pp = F.P(list(tri))
        out += _solid(pp, ink, F.step * 0.9)
        _edge(pp, dark, out)
    out += _solid(F.P([top, right, bot, left]), None, 1e9) if False else []
    _edge(F.P([top, right, bot, left]), (18, 70, 42), out)
    return out


def stalactite(cx, cy, s, seed=0, face=-1):
    """Cave ceiling spike, hanging down -- the biome correction."""
    F = _F(cx, cy, s, face)
    rnd = random.Random(seed)
    w = 0.16 * rnd.uniform(0.7, 1.3)
    F.poly([(-w, 0.40), (w, 0.40), (rnd.uniform(-0.03, 0.03), -0.02)],
           (108, 104, 112), (68, 66, 74))
    F.L(-w * 0.3, 0.34, -w * 0.1, 0.10, (78, 76, 84))
    return F.out


def stalagmite(cx, cy, s, seed=0, face=-1):
    """Cave floor spike, rising."""
    F = _F(cx, cy, s, face)
    rnd = random.Random(seed)
    w = 0.16 * rnd.uniform(0.7, 1.3)
    F.poly([(-w, 0.0), (w, 0.0), (rnd.uniform(-0.03, 0.03), 0.40)],
           (116, 112, 120), (72, 70, 78))
    F.L(-w * 0.3, 0.06, -w * 0.1, 0.30, (84, 82, 90))
    return F.out


KIT = {"clockwork_gnome": clockwork_gnome, "clockwork_spider": clockwork_spider,
       "glow_diamond": glow_diamond, "tesla_arc": tesla_arc, "stalactite": stalactite, "stalagmite": stalagmite}


if __name__ == "__main__":
    for n, fn in KIT.items():
        print("%-18s %d strokes" % (n, len(fn(0, 0, 100))))
