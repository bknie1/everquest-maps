"""kaladim_decor.py -- the Kaladim gate, from Brandon's in-game capture.

The dwarven colossus standing in a recess between two banded pillars, over the
green-stone curtain wall and the arched gate the guards hold. It is the first
thing you see coming from Butcherblock, so it is the zone's identity piece --
the Kaladim equivalent of Najena's banner.

Drawn bold rather than fine: at map scale the motif has to survive as a
silhouette, so the reading cues are the horned helm, the beard, the chest
medallion, the two pillars and the black arch. Everything else is fill.

    from kaladim_decor import gate
    segs = gate(cx, cy, w, h, seed=0)     # (cx,cy) = centre of the motif
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(__file__))
from fauna_sil import SIL  # noqa: E402

PALE = (188, 168, 128)        # lit pillar stone
STONE = (150, 132, 104)       # statue / mid stone
SHADE = (110, 94, 70)         # shaded stone, block lines
DEEP = (56, 48, 38)           # recess behind the colossus
WALL = (86, 132, 70)          # the green-tinted curtain wall
WALL_D = (62, 104, 56)        # its shaded courses -- the margin rock green
GOLD = (198, 150, 60)         # trim course and brazier bowls
DARK = (46, 42, 38)           # the gate opening
FLAME = (230, 150, 50)
FLAME_HOT = (250, 210, 120)


def _carve(ink):
    """Recolour a live figure's ink into the gate's stone, by luminance.

    The figure carries the dark end of the range: like every other silhouette in
    this atlas it reads against parchment, not against a filled ground. Filling
    the niche behind it merely striped the two together."""
    lum = 0.299 * ink[0] + 0.587 * ink[1] + 0.114 * ink[2]
    if lum < 95:
        return DEEP
    if lum < 150:
        return SHADE
    return STONE


def _solid(poly, ink, step):
    """Scanline-fill a polygon into horizontal strokes."""
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
            if xs[i + 1] - xs[i] > 0.3:
                out.append((xs[i], y, xs[i + 1], y, ink))
        y += step
    return out


class _G:
    """Local frame: x in [-0.5,0.5] across the motif, y from 0 (ground) to 1 (top)."""

    def __init__(self, cx, cy, w, h):
        self.cx, self.cy, self.w, self.h = cx, cy, w, h
        self.out = []
        self.step = max(0.6, h * 0.016)

    def T(self, x, y):
        return (self.cx + x * self.w, self.cy + (0.5 - y) * self.h)

    def L(self, x1, y1, x2, y2, ink):
        a, b = self.T(x1, y1), self.T(x2, y2)
        self.out.append((a[0], a[1], b[0], b[1], ink))

    def poly(self, pts, fill, line=None, pitch=1.0):
        pp = [self.T(*p) for p in pts]
        self.out += _solid(pp, fill, self.step * pitch)
        e = line or fill
        for i in range(len(pp)):
            a, b = pp[i], pp[(i + 1) % len(pp)]
            self.out.append((a[0], a[1], b[0], b[1], e))

    def box(self, x0, x1, y0, y1, fill, line=None, pitch=1.0):
        self.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill, line, pitch)

    def disc(self, x, y, r, fill, n=12, line=None):
        self.poly([(x + r * math.cos(t * 2 * math.pi / n),
                    y + r * math.cos(0) * math.sin(t * 2 * math.pi / n) * (self.w / self.h))
                   for t in range(n)], fill, line)


def _brazier(G, x, y, sx=0.016, sy=0.030):
    """Small gold bowl with a flame. Deliberately tiny: at map scale these are
    accents beside the colossus, not features competing with it."""
    G.poly([(x - sx, y), (x + sx, y), (x + sx * 0.55, y + sy * 0.6),
            (x - sx * 0.55, y + sy * 0.6)], GOLD, SHADE, pitch=0.7)
    for ink, sc in ((FLAME, 1.0), (FLAME_HOT, 0.5)):
        G.poly([(x - sx * 0.7 * sc, y + sy * 0.5), (x, y + sy * (0.5 + 1.7 * sc)),
                (x + sx * 0.7 * sc, y + sy * 0.5)], ink, ink, pitch=0.6)


def gate(cx, cy, w, h, seed=0):
    """The Kaladim gate: colossus in its recess, two banded pillars, curtain
    wall with a gold trim course, arched gate, four braziers."""
    G = _G(cx, cy, w, h)
    rnd = random.Random(seed)

    # --- the niche. Outlined and lightly hatched only: a solid ground behind
    # the statue interleaves with the statue's own fill and stripes them into
    # one grey block. The figure needs parchment to read against.
    G.box(-0.175, 0.175, 0.30, 1.00, SHADE, SHADE, pitch=4.5)

    # --- colossus ------------------------------------------------------------
    # It is a statue OF A DWARF, so it is the kit's dwarf -- carved in stone
    # rather than redrawn worse by hand. Recoloured up into the stone tones so
    # the figure stays light against the dark recess.
    feet = G.T(0.0, 0.335)
    figure = SIL['dwarf'](feet[0], feet[1], h * 0.80, seed=seed, face=1)
    G.out += [(a, b, c, d, _carve(ink)) for (a, b, c, d, ink) in figure]
    # the brooch at the chest -- the one bright point, as in the capture
    G.disc(0.0, 0.60, 0.022, GOLD, line=SHADE)

    # --- the two banded pillars ---------------------------------------------
    for sgn in (-1, 1):
        x0, x1 = sgn * 0.190, sgn * 0.290
        a, b = min(x0, x1), max(x0, x1)
        G.box(a, b, 0.30, 1.00, PALE, SHADE, pitch=1.3)
        y = 0.34
        while y < 1.00:                                     # the block courses
            G.L(a, y, b, y, SHADE)
            G.L(a, y + 0.012, b, y + 0.012, STONE)
            y += 0.105
        G.box(a - 0.012, b + 0.012, 0.97, 1.02, STONE, SHADE)   # cap

    # --- curtain wall --------------------------------------------------------
    G.box(-0.50, 0.50, 0.06, 0.30, WALL, WALL_D, pitch=1.5)
    course = 0.06
    row = 0
    while course < 0.30:                                    # staggered masonry
        G.L(-0.50, course, 0.50, course, WALL_D)
        x = -0.50 + (0.045 if row % 2 else 0.0)
        while x < 0.50:
            G.L(x, course, x, min(course + 0.06, 0.30), WALL_D)
            x += 0.09
        course += 0.06
        row += 1
    G.box(-0.50, 0.50, 0.30, 0.335, GOLD, SHADE)            # gold trim course

    # --- the gate the guards hold -------------------------------------------
    G.box(-0.085, 0.085, 0.06, 0.20, DARK, DARK, pitch=1.4)
    for k in range(7):                                      # arched head
        t0 = math.pi * k / 7
        t1 = math.pi * (k + 1) / 7
        G.L(0.085 * math.cos(t0), 0.20 + 0.055 * math.sin(t0),
            0.085 * math.cos(t1), 0.20 + 0.055 * math.sin(t1), SHADE)

    # --- braziers: a pair on each flanking terrace ---------------------------
    for x in (-0.400, -0.340, 0.340, 0.400):
        _brazier(G, x, 0.337)

    return G.out


KIT = {'gate': gate}


if __name__ == '__main__':
    print('gate  %d strokes' % len(gate(0, 0, 200, 100)))
