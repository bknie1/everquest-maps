"""build_unrest.py -- the Estate of Unrest flagship pass (round 2).

Idempotent: every ink this script writes is owned by it and stripped before
re-drawing; base-layer recolors (bronze borders, per-floor wood tones, the
water shoreline) are one-way and re-run as no-ops.

Round 2 (Brandon's review): walking scarecrows, solid hedge masses, no
checkerboard, no pale-gold inks, Faydwer forest-floor moss/ferns, manor
exterior border + per-floor wall tones instead of the roof wash, carpets and
a mosaic hint, lanky small ghouls, stone perimeter wall, Goosebumps title.

    python src/tools/build_unrest.py
"""
import math
import os
import random
import sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, '..', 'kit'))
sys.path.insert(0, os.path.join(HERE, '..', 'toolkit'))
sys.path.insert(0, HERE)

from fauna_hd_zombie import zombie
from fauna_hd_ghoul import ghoul
from unrest_decor import (scarecrow, death_beetle, stone_gate, pillar,
                          CARPET, MOSAIC, STONE, STONE_DK)
import flora_hd
import terrain
from eqmap_toolkit import LETTERS
from shade_city import components as sc_components, fill_component
import build as kit_build

MAPS = os.environ.get('EQ_MAPS', 'Emoda Legends Maps')
CRLF = '\r\n'

PALE = (130, 140, 120)
BLUE = (80, 98, 112)
GREEN = (74, 106, 64)
GOLD_OLD = (172, 144, 82)        # pale gold -- banned on parchment
BRONZE = (130, 82, 12)           # its replacement
WATER = (60, 120, 180)

ROOF = (128, 102, 68)            # gazebo roof
ROOF_DK = (94, 72, 48)
HEDGE = (46, 72, 48)
BORDER = (58, 48, 40)            # manor exterior border
CLOUD = (112, 114, 126)
CLOUD_DK = (78, 80, 94)
BOLT = (210, 200, 150)
BOLT_DK = (86, 80, 96)
RAIN = (118, 128, 146)
TITLE_INK = (60, 45, 40)         # haunted lettering
TITLE_OLD = (96, 84, 74)

# per-floor warm wood tones (darkest low, consistent within a floor)
FLOOR_TONES = [(108, 88, 64), (122, 100, 70), (134, 112, 78), (144, 124, 86)]
FLOOR_CUTS = [10, 26, 42]        # z-band edges between floors
MANOR_BOX = (-175, 175, -815, -478)
MANOR_INKS = set(FLOOR_TONES) | {PALE, BLUE, GOLD_OLD, BRONZE}

BASE_OWNED = {ROOF, ROOF_DK}


def _probe_inks():
    inks = set()
    probes = (zombie(0, 0, 20, seed=1), ghoul(0, 0, 14, seed=1),
              scarecrow(0, 0, 30, seed=1), death_beetle(0, 0, 7, seed=1),
              stone_gate(0, 0, 15, seed=1), pillar(0, 0, 3),
              flora_hd.broadleaf(0, 0, 20, seed=1), flora_hd.fir(0, 0, 20, seed=1),
              flora_hd.broadleaf(0, 0, 20, seed=5), flora_hd.fir(0, 0, 20, seed=7),
              flora_hd.bush(0, 0, 10, seed=1), flora_hd.bush(0, 0, 10, seed=3),
              flora_hd.moss_patch(0, 0, 5, seed=1), flora_hd.fern_curl(0, 0, 5, seed=1))
    for shape in probes:
        for s in shape:
            inks.add(tuple(s[4]))
    return inks


DECO_OWNED = {HEDGE, CLOUD, CLOUD_DK, BOLT, BOLT_DK, RAIN, BORDER, TITLE_INK,
              CARPET, MOSAIC, STONE, STONE_DK, (44, 40, 36),
              flora_hd.MOSS, flora_hd.MOSS_DK,
              (200, 172, 116), (156, 130, 84),   # round-1 pale sandstone
              (112, 116, 92), (76, 82, 62), (98, 84, 58),
              (86, 80, 94), (58, 54, 66), (120, 114, 124)} | _probe_inks()


def fmt(x1, y1, x2, y2, ink):
    return 'L %.4f, %.4f, 0.0000, %.4f, %.4f, 0.0000, %d, %d, %d' % (
        x1, y1, x2, y2, ink[0], ink[1], ink[2])


def load(path):
    return open(path, encoding='utf-8').read().splitlines()


def save(path, lines):
    open(path, 'w', newline='', encoding='utf-8').write(CRLF.join(lines) + CRLF)
    b = open(path, 'rb').read()
    assert sum(1 for i, c in enumerate(b) if c == 10 and (i == 0 or b[i-1] != 13)) == 0


def ink_of(line):
    q = line[2:].split(',')
    return (int(q[6]), int(q[7]), int(q[8]))


def strip_owned(lines, owned):
    return [ln for ln in lines
            if not (ln.startswith('L') and ink_of(ln) in owned)]


def segs_of(lines):
    out = []
    for ln in lines:
        if ln.startswith('L'):
            q = ln[2:].split(',')
            out.append((float(q[0]), float(q[1]), float(q[3]), float(q[4]),
                        (int(q[6]), int(q[7]), int(q[8])), float(q[2]), float(q[5])))
    return out


def in_box(x1, y1, x2, y2, box):
    return box[0] <= min(x1, x2) and max(x1, x2) <= box[1] \
        and box[2] <= min(y1, y2) and max(y1, y2) <= box[3]


# ------------------------------------------------------------ base recolors

def recolor_base(base):
    """One-way base recolors: shoreline to water blue, pale gold to bronze,
    manor pale walls to per-floor wood tones. Re-runs are no-ops."""
    n_shore = n_bronze = n_floor = 0
    for i, ln in enumerate(base):
        if not ln.startswith('L'):
            continue
        q = [v.strip() for v in ln[2:].split(',')]
        ink = (int(q[6]), int(q[7]), int(q[8]))
        x1, y1, x2, y2 = float(q[0]), float(q[1]), float(q[3]), float(q[4])
        new = None
        if ink == BLUE and min(x1, x2) > 195:
            new = WATER; n_shore += 1
        elif ink == GOLD_OLD:
            new = BRONZE; n_bronze += 1
        elif ink == PALE and in_box(x1, y1, x2, y2, MANOR_BOX):
            z = (float(q[2]) + float(q[5])) / 2
            band = sum(1 for c in FLOOR_CUTS if z >= c)
            new = FLOOR_TONES[band]; n_floor += 1
        if new:
            base[i] = 'L ' + ', '.join(q[:6]) + ', %d, %d, %d' % new
    print('recolors: shoreline %d, bronze %d, floor tones %d'
          % (n_shore, n_bronze, n_floor))


# ------------------------------------------------------------ base additions

def gazebo_roof(segs):
    sub = [s for s in segs if s[4] == PALE
           and in_box(s[0], s[1], s[2], s[3], (240, 305, -535, -465))]
    out = []
    for comp in sc_components(sub):
        strokes = [sub[j] for j in comp]
        if len(strokes) < 40:
            continue
        cy = [v for s in strokes for v in (s[1], s[3])]
        shadow_from = min(cy) + (max(cy) - min(cy)) * 0.62
        for (a, y, b) in fill_component([s[:5] for s in strokes], 5.5):
            out.append(fmt(a, y, b, y, ROOF_DK if y > shadow_from else ROOF))
    return out


# ------------------------------------------------------------ _2 additions

def hedge_shading(base_segs):
    """Solid hedge masses: dark parallel strokes at three offsets either side
    of every maze wall stroke, so each hedge reads as one dense band."""
    band = (-252, 252, -478, -300)
    ponds = ((-51, -9, -321, -228), (9, 51, -321, -228))
    out = []
    n_walls = 0
    for s in base_segs:
        (x1, y1, x2, y2, c) = s[:5]
        if c != GREEN or not in_box(x1, y1, x2, y2, band):
            continue
        if any(in_box(x1, y1, x2, y2, p) for p in ponds):
            continue
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy)
        if L < 1.0:
            continue
        n_walls += 1
        nx, ny = -dy / L, dx / L
        t = min(0.7, L * 0.06) / L
        ax, ay = x1 + dx * t, y1 + dy * t
        bx, by = x2 - dx * t, y2 - dy * t
        for k in (-1.8, -1.2, -0.6, 0.6, 1.2, 1.8):
            out.append(fmt(ax + nx * k, ay + ny * k, bx + nx * k, by + ny * k, HEDGE))
    print('hedge: %d wall strokes -> %d fill strokes' % (n_walls, len(out)))
    return out


def manor_border(base_segs):
    """A heavy dark border around the manor's exterior silhouette: rasterise,
    flood the outside, then double-offset every wall stroke whose one side
    faces open ground (the BRAIN-8 halo method, tightened)."""
    box = MANOR_BOX
    cell = 3.0
    W = int((box[1] - box[0]) / cell) + 1
    H = int((box[3] - box[2]) / cell) + 1
    occ = [[False] * W for _ in range(H)]
    geom = [s for s in base_segs if s[4] in MANOR_INKS
            and in_box(s[0], s[1], s[2], s[3], box)]
    for (x1, y1, x2, y2, c, *_z) in geom:
        L = math.hypot(x2 - x1, y2 - y1)
        n = max(1, int(L / (cell * 0.5)))
        for k in range(n + 1):
            t = k / n
            cxi = int((x1 + (x2 - x1) * t - box[0]) / cell)
            cyi = int((y1 + (y2 - y1) * t - box[2]) / cell)
            if 0 <= cxi < W and 0 <= cyi < H:
                occ[cyi][cxi] = True
    outside = [[False] * W for _ in range(H)]
    stack = [(x, y) for x in range(W) for y in (0, H - 1)] + \
            [(x, y) for x in (0, W - 1) for y in range(H)]
    while stack:
        cxi, cyi = stack.pop()
        if not (0 <= cxi < W and 0 <= cyi < H):
            continue
        if outside[cyi][cxi] or occ[cyi][cxi]:
            continue
        outside[cyi][cxi] = True
        stack += [(cxi+1, cyi), (cxi-1, cyi), (cxi, cyi+1), (cxi, cyi-1)]

    def is_out(px, py):
        cxi = int((px - box[0]) / cell)
        cyi = int((py - box[2]) / cell)
        if not (0 <= cxi < W and 0 <= cyi < H):
            return True
        return outside[cyi][cxi]

    out = []
    for (x1, y1, x2, y2, c, *_z) in geom:
        L = math.hypot(x2 - x1, y2 - y1)
        if L < 5:
            continue
        dx, dy = (x2 - x1) / L, (y2 - y1) / L
        nx, ny = -dy, dx
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        o_pos = is_out(mx + nx * 4.5, my + ny * 4.5)
        o_neg = is_out(mx - nx * 4.5, my - ny * 4.5)
        if o_pos == o_neg:
            continue
        sgn = 1 if o_pos else -1
        t = min(1.0, L * 0.08)
        ax, ay = x1 + dx * t, y1 + dy * t
        bx, by = x2 - dx * t, y2 - dy * t
        for k in (1.4, 2.8):
            out.append(fmt(ax + sgn * nx * k, ay + sgn * ny * k,
                           bx + sgn * nx * k, by + sgn * ny * k, BORDER))
    print('manor border: %d strokes' % len(out))
    return out


def perimeter_wall():
    """The estate's octagonal outer wall is stone: fill the band between its
    double lines with stone gray and block joints."""
    faces = [
        ((-310, -400), (-310, -800), (-300, -400), (-300, -790)),
        ((-310, -800), (-210, -900), (-300, -790), (-200, -890)),
        ((-210, -900), (210, -900), (-200, -890), (200, -890)),
        ((210, -900), (310, -800), (200, -890), (300, -790)),
        ((310, -800), (310, -400), (300, -790), (300, -400)),
    ]
    out = []
    for (o0, o1, i0, i1) in faces:
        L = math.hypot(o1[0] - o0[0], o1[1] - o0[1])
        # two longitudinal courses
        for fr in (0.35, 0.68):
            a = (o0[0] + (i0[0] - o0[0]) * fr, o0[1] + (i0[1] - o0[1]) * fr)
            b = (o1[0] + (i1[0] - o1[0]) * fr, o1[1] + (i1[1] - o1[1]) * fr)
            out.append(fmt(a[0], a[1], b[0], b[1], STONE))
        # block joints across the band, staggered half-course
        n = max(2, int(L / 13))
        for k in range(1, n):
            t = k / n
            ox = o0[0] + (o1[0] - o0[0]) * t
            oy = o0[1] + (o1[1] - o0[1]) * t
            ix = i0[0] + (i1[0] - i0[0]) * t
            iy = i0[1] + (i1[1] - i0[1]) * t
            if k % 2:
                out.append(fmt(ox, oy, ox + (ix - ox) * 0.55, oy + (iy - oy) * 0.55,
                               STONE_DK))
            else:
                out.append(fmt(ix, iy, ix + (ox - ix) * 0.55, iy + (oy - iy) * 0.55,
                               STONE_DK))
    print('perimeter wall: %d strokes' % len(out))
    return out


def rear_pillars(base_segs):
    spans = []
    for s in base_segs:
        (x1, y1, x2, y2, c) = s[:5]
        if c in MANOR_INKS and abs(y1 - y2) < 0.5 and -766 <= y1 <= -755 \
                and -105 <= min(x1, x2) and max(x1, x2) <= 10:
            spans.append((min(x1, x2), max(x1, x2)))
    spans.sort()
    gap = None
    for i in range(len(spans) - 1):
        g0, g1 = spans[i][1], spans[i + 1][0]
        if 6 <= g1 - g0 <= 30:
            gap = (g0, g1)
            break
    if gap is None:
        gap = (-58, -42)
    out = []
    for s in pillar(gap[0] - 3.0, -769.5, 3.2) + pillar(gap[1] + 3.0, -769.5, 3.2):
        out.append(fmt(*s[:4], s[4]))
    return out, gap


def interior_pillars(base_segs):
    out = []
    spots = []
    sub = [s[:5] for s in base_segs if s[4] in MANOR_INKS and s[4] != BRONZE
           and in_box(s[0], s[1], s[2], s[3], (-170, 170, -810, -490))]
    for comp in sc_components(sub):
        if not 4 <= len(comp) <= 14:
            continue
        xs = [v for j in comp for v in (sub[j][0], sub[j][2])]
        ys = [v for j in comp for v in (sub[j][1], sub[j][3])]
        w, h = max(xs) - min(xs), max(ys) - min(ys)
        if 4 <= max(w, h) <= 12 and min(w, h) >= 3:
            spots.append(((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2))
    for (px, py) in spots[:6]:
        for s in pillar(px, py, 2.6):
            out.append(fmt(*s[:4], s[4]))
    return out, spots[:6]


def interior_flavor():
    """Haunted-house flavour, restrained: deep-red carpets in the big rooms
    and a subtle mosaic lattice hint at two ceiling/landing spots."""
    out = []

    def carpet(cx, cy, w, h):
        x0, y0, x1, y1 = cx - w/2, cy - h/2, cx + w/2, cy + h/2
        for (a, b, c, d) in ((x0, y0, x1, y0), (x1, y0, x1, y1),
                             (x1, y1, x0, y1), (x0, y1, x0, y0)):
            out.append(fmt(a, b, c, d, CARPET))
        i = 1.6
        for (a, b, c, d) in ((x0+i, y0+i, x1-i, y0+i), (x1-i, y0+i, x1-i, y1-i),
                             (x1-i, y1-i, x0+i, y1-i), (x0+i, y1-i, x0+i, y0+i)):
            out.append(fmt(a, b, c, d, CARPET))
        out.append(fmt(x0 + w*0.3, cy, x1 - w*0.3, cy, CARPET))

    def mosaic(cx, cy, w, h, cell=4.5):
        x0, y0, x1, y1 = cx - w/2, cy - h/2, cx + w/2, cy + h/2
        d = x0 + y0 - (h if h < w else w)
        while d < x1 + y1:
            ax, ay = max(x0, d - y1), min(y1, d - x0)
            bx, by = min(x1, d - y0), max(y0, d - x1)
            if ax < bx:
                out.append(fmt(ax, d - ax, bx, d - bx, MOSAIC))
            d += cell
        d = x0 - y1
        while d < x1 - y0:
            ax = max(x0, d + y0); ay = ax - d
            bx = min(x1, d + y1); by = bx - d
            if ax < bx:
                out.append(fmt(ax, ay, bx, by, MOSAIC))
            d += cell

    carpet(0, -547, 26, 13)          # main hall
    carpet(-93, -612, 16, 9)         # barroom
    carpet(-52, -750, 16, 8)         # north wing
    mosaic(64, -696, 26, 17, cell=5.0)   # tower octagon ceiling
    mosaic(22, -642, 16, 10, cell=5.5)   # stair landing, subtler
    return out


def figures_trees_gate():
    out = []
    S = lambda seglist: out.extend(fmt(*s[:4], s[4]) for s in seglist)

    S(zombie(-62, -455, 16, seed=2, face=1))
    S(zombie(118, -464, 16, seed=5, face=-1))
    S(zombie(-278, -482, 15, seed=8, face=1))
    S(zombie(-185, -792, 15, seed=11, face=-1))

    # lanky ghouls, smaller than the zombies, inside the manor
    S(ghoul(-90, -600, 10, seed=3, face=1))
    S(ghoul(-25, -555, 10, seed=7, face=-1))

    S(death_beetle(28, -506, 7, seed=1))
    S(death_beetle(-52, -416, 6, seed=2))
    S(death_beetle(152, -522, 6, seed=3))

    # walking scarecrow-men
    S(scarecrow(-190, -462, 30, seed=4, face=1))
    S(scarecrow(205, -483, 30, seed=9, face=-1))

    S(stone_gate(0.44, -424, 15, seed=1))

    trees = [
        ('b', -285, -700, 22), ('f', -248, -628, 18), ('b', -292, -548, 20),
        ('f', -218, -756, 19), ('b', -128, -848, 20), ('f', -42, -858, 17),
        ('b', 72, -852, 21), ('f', -190, -838, 18), ('b', 115, -812, 18),
        ('f', 172, -652, 17), ('b', 164, -578, 18), ('f', -282, -428, 18),
        ('b', 225, -448, 17),
        ('f', 150, -705, 17), ('b', 215, -582, 18), ('f', -90, -862, 16),
        ('b', -260, -462, 17), ('f', 100, -870, 15),
    ]
    for i, (kind, tx, ty, ts) in enumerate(trees):
        fn = flora_hd.broadleaf if kind == 'b' else flora_hd.fir
        S(fn(tx, ty, ts, seed=i * 3 + 1))
    S(flora_hd.bush(-64, -268, 10, seed=21))
    S(flora_hd.bush(64, -246, 10, seed=22))
    return out, [(t[1], t[2]) for t in trees]


def forest_floor(base_segs, tree_pts, deco_lines):
    """Faydwer ground convention: patchy moss and fern curls clumped near
    trees, hedges and walls, bare parchment in the open lawn."""
    # proximity hash of all base geometry (auto-avoids paths, walls, water)
    cell = 8.0
    grid = {}
    for s in base_segs:
        (x1, y1, x2, y2) = s[:4]
        L = math.hypot(x2 - x1, y2 - y1)
        n = max(1, int(L / 4))
        for k in range(n + 1):
            t = k / n
            px, py = x1 + (x2-x1)*t, y1 + (y2-y1)*t
            grid.setdefault((int(px // cell), int(py // cell)), []).append((px, py))

    def near_geom(x, y, r=3.5):
        ci, cj = int(x // cell), int(y // cell)
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                for (px, py) in grid.get((ci + di, cj + dj), ()):
                    if (px - x) ** 2 + (py - y) ** 2 < r * r:
                        return True
        return False

    labels = []
    for ln in load(os.path.join(MAPS, 'unrest_1.txt')):
        if ln.startswith('P'):
            q = ln[2:].split(',')
            lx, ly, name = float(q[0]), float(q[1]), q[7].strip()
            labels.append((lx - 6, lx + 4.2 * len(name) + 4, ly - 10, ly + 4))

    decor_pts = [(-70, -470), (118, -464), (-278, -482), (-185, -792),
                 (-190, -462), (205, -483), (0, -424), (28, -506),
                 (-52, -416), (152, -522), (-64, -268), (64, -246)]

    def reject(x, y):
        if abs(x) > 288 or y < -878 or y > -240:
            return True
        if x > 193 and y < -455:
            return True                      # east water + ramp
        if in_box(x, y, x, y, (-30, 30, -462, -100)):
            return True                      # centre path
        if in_box(x, y, x, y, (-24, 24, -484, -420)):
            return True                      # forecourt
        if in_box(x, y, x, y, (-250, 250, -460, -305)):
            return True                      # hedge maze interior
        if in_box(x, y, x, y, MANOR_BOX):
            return True                      # manor interior
        for (a, b, c, d) in labels:
            if a <= x <= b and c <= y <= d:
                return True
        for (px, py) in decor_pts:
            if (px - x) ** 2 + (py - y) ** 2 < 100:
                return True
        for (px, py) in tree_pts:
            if (px - x) ** 2 + (py - y) ** 2 < 16:
                return True                  # not on a trunk (near is good)
        return near_geom(x, y)

    anchors = list(tree_pts)
    for bx in range(-240, 241, 40):          # hedge fringes
        anchors += [(bx, -468), (bx, -298)]
    for wy in range(-760, -419, 60):         # estate wall bases
        anchors += [(-292, wy), (292, wy)]
    for wx in range(-180, 181, 60):          # north wall base
        anchors.append((wx, -874))
    anchors += [(-45, -315), (45, -315), (-45, -235), (45, -235)]   # pond skirts
    anchors += [(238, -470), (150, -560)]

    segs = flora_hd.faydwer_floor(anchors, reject=reject, seed=17,
                                  clumps=(3, 6), spread=15.0)
    # sparse lawn singles so the open ground is not sterile
    rnd = random.Random(23)
    n = 0
    while n < 26:
        x = rnd.uniform(-280, 280); y = rnd.uniform(-870, -250)
        if reject(x, y):
            n += 1  # count attempts to bound the loop
            continue
        segs += (flora_hd.moss_patch(x, y, rnd.uniform(2.5, 4), seed=n)
                 if rnd.random() < 0.7 else
                 flora_hd.fern_curl(x, y, rnd.uniform(3, 5), seed=n))
        n += 1
    print('forest floor: %d strokes' % len(segs))
    return [fmt(*s[:4], s[4]) for s in segs]


def haunted_title(deco):
    """Goosebumps lettering: wipe the stick title, redraw ESTATE OF UNREST
    with per-letter tilt and size jitter, doubled strokes, and drips.
    Guard: title_health must not drop (BRAIN 6)."""
    segs = segs_of(deco)
    grid = [s for s in segs if s[4] == (120, 124, 112)]
    gy0 = min(min(s[1], s[3]) for s in grid)
    gx0 = min(min(s[0], s[2]) for s in grid)
    gx1 = max(max(s[0], s[2]) for s in grid)
    health_before = kit_build.title_health([s[:5] for s in segs], gy0)

    out = [ln for ln in deco
           if not (ln.startswith('L') and ink_of(ln) == TITLE_OLD
                   and ln.startswith('L')
                   and max(float(ln[2:].split(',')[1]),
                           float(ln[2:].split(',')[4])) < gy0)]
    wiped = len(deco) - len(out)

    text = 'ESTATE OF UNREST'
    H = 46.0
    cw = H * 0.60
    gap = cw * 0.38
    widths = [cw * (0.42 if ch == ' ' else 1.0) for ch in text]
    total = sum(widths) + gap * (len(text) - 1)
    scale = min(1.0, (gx1 - gx0) * 0.90 / total)
    H *= scale; cw *= scale; gap *= scale
    widths = [w * scale for w in widths]
    x = (gx0 + gx1) / 2 - (sum(widths) + gap * (len(text) - 1)) / 2
    ybase = -1012.0
    rnd = random.Random(5)
    new = []
    drip_from = []
    for i, ch in enumerate(text):
        w = widths[i]
        if ch != ' ':
            th = math.radians(rnd.uniform(3, 7) * rnd.choice((-1, 1)))
            sc = rnd.uniform(0.90, 1.10)
            dy = rnd.uniform(-2.5, 2.5)
            cxm, cym = x + w / 2, ybase - H * 0.5 + dy
            ca, sa = math.cos(th), math.sin(th)

            def T(px, py):
                lx = (px - 0.5) * w * sc
                ly = (0.5 - py) * H * sc + dy      # glyph y up -> map y down
                return (cxm + lx * ca - ly * sa, cym - dy + lx * sa + ly * ca + dy)

            for poly in LETTERS.get(ch, []):
                for j in range(len(poly) - 1):
                    a = T(*poly[j]); b = T(*poly[j + 1])
                    new.append(fmt(a[0], a[1], b[0], b[1], TITLE_INK))
                    new.append(fmt(a[0] + 1.1, a[1] + 0.9,
                                   b[0] + 1.1, b[1] + 0.9, TITLE_INK))
            if rnd.random() < 0.45:
                bx, by = T(rnd.uniform(0.15, 0.85), 0.0)
                drip_from.append((bx, by))
        x += w + gap
    for (dx0, dy0) in drip_from[:6]:
        px, py = dx0, dy0
        for k in range(3):
            nx = px + rnd.uniform(-1.6, 1.6)
            ny = py + rnd.uniform(3.5, 6.5)
            new.append(fmt(px, py, nx, ny, TITLE_INK))
            px, py = nx, ny
        new.append(fmt(px - 0.6, py + 1.6, px + 0.6, py + 1.6, TITLE_INK))

    out += new
    health_after = kit_build.title_health([s[:5] for s in segs_of(out)], gy0)
    print('title: wiped %d, drew %d; health %d -> %d'
          % (wiped, len(new), health_before, health_after))
    assert health_after >= health_before, 'title health dropped -- rollback'
    return out


def storm_margins(deco_lines):
    segs = segs_of(deco_lines)
    grid = [s for s in segs if s[4] == (120, 124, 112)]
    gx0 = min(min(s[0], s[2]) for s in grid); gx1 = max(max(s[0], s[2]) for s in grid)
    gy0 = min(min(s[1], s[3]) for s in grid); gy1 = max(max(s[1], s[3]) for s in grid)
    frame = [s for s in segs if s[4] == (64, 70, 64)]
    fx0 = min(min(s[0], s[2]) for s in frame); fx1 = max(max(s[0], s[2]) for s in frame)
    fy0 = min(min(s[1], s[3]) for s in frame); fy1 = max(max(s[1], s[3]) for s in frame)
    title = [s for s in segs if s[4] in (TITLE_INK, TITLE_OLD)
             and max(s[1], s[3]) < gy0]
    tx0 = min(min(s[0], s[2]) for s in title) - 14; tx1 = max(max(s[0], s[2]) for s in title) + 14
    ty0 = min(min(s[1], s[3]) for s in title) - 12; ty1 = max(max(s[1], s[3]) for s in title) + 12
    compass = (-478, -318, 8, 178)

    def clear(x, y):
        if tx0 <= x <= tx1 and ty0 <= y <= ty1:
            return False
        if compass[0] <= x <= compass[1] and compass[2] <= y <= compass[3]:
            return False
        return True

    out = []
    for (cx, cy, w, h, sd) in ((-360, -1092, 150, 40, 11),
                               (95, -1120, 200, 46, 12),
                               (430, -1082, 120, 34, 13)):
        for (x1, y1, x2, y2, c) in terrain.cloud(cx, cy, w, h, ink=CLOUD,
                                                 deep=CLOUD_DK, seed=sd):
            out.append(fmt(x1, y1, x2, y2, c))

    bolts = [
        [(-352, -1070), (-386, -1022), (-362, -1000), (-395, -958)],
        [(408, -1062), (442, -1015), (420, -992), (452, -948)],
        [(-437, -680), (-465, -628), (-443, -604), (-472, -552)],
    ]
    for pts in bolts:
        for i in range(len(pts) - 1):
            out.append(fmt(*pts[i], *pts[i + 1], BOLT))
        for i in range(len(pts) - 1):
            out.append(fmt(pts[i][0] + 3.0, pts[i][1] + 2.5,
                           pts[i + 1][0] + 3.0, pts[i + 1][1] + 2.5, BOLT_DK))
        tip = pts[-1]
        out.append(fmt(tip[0], tip[1], tip[0] + 9, tip[1] - 14, BOLT))

    rnd = random.Random(7)
    bands = [
        (fx0 + 6, gx0 - 8, gy0 - 6, gy1 + 4),
        (gx1 + 8, fx1 - 6, gy0 - 6, gy1 + 4),
        (fx0 + 6, fx1 - 6, fy0 + 8, gy0 - 10),
        (fx0 + 6, fx1 - 6, gy1 + 8, fy1 - 8),
    ]
    per = [30, 30, 70, 40]
    for (bx0, bx1, by0, by1), n in zip(bands, per):
        placed = 0
        tries = 0
        while placed < n and tries < n * 30:
            tries += 1
            L = rnd.uniform(45, 105)
            dx, dy = -L * 0.42, L * 0.91
            x0 = rnd.uniform(bx0, bx1)
            y0 = rnd.uniform(by0, by1)
            x1, y1 = x0 + dx, y0 + dy
            if not (bx0 <= x1 <= bx1 and by0 <= y1 <= by1):
                continue
            if not (clear(x0, y0) and clear(x1, y1)
                    and clear((x0 + x1) / 2, (y0 + y1) / 2)):
                continue
            out.append(fmt(x0, y0, x1, y1, RAIN))
            placed += 1
    return out


def main():
    base_p = os.path.join(MAPS, 'unrest.txt')
    deco_p = os.path.join(MAPS, 'unrest_2.txt')

    base = strip_owned(load(base_p), BASE_OWNED)
    deco = strip_owned(load(deco_p), DECO_OWNED)
    recolor_base(base)
    base_segs = segs_of(base)

    gz = gazebo_roof(base_segs)
    base_out = gz + base
    print('base: +%d gazebo runs -> %d L' % (
        len(gz), sum(1 for l in base_out if l.startswith('L'))))

    add = []
    add += hedge_shading(base_segs)
    add += manor_border(base_segs)
    add += perimeter_wall()
    rp, gap = rear_pillars(base_segs); add += rp
    print('rear entrance gap at x %.1f..%.1f' % gap)
    ip, spots = interior_pillars(base_segs); add += ip
    print('interior pillars:', [(round(x), round(y)) for x, y in spots])
    add += interior_flavor()
    ft, tree_pts = figures_trees_gate(); add += ft
    add += forest_floor(base_segs, tree_pts, deco)

    deco_mid = haunted_title(deco + add)
    sm = storm_margins(deco_mid)
    deco_out = deco_mid + sm
    print('deco: %d L' % sum(1 for l in deco_out if l.startswith('L')))

    save(base_p, base_out)
    save(deco_p, deco_out)
    tot = sum(1 for l in base_out + deco_out if l.startswith('L'))
    print('zone total L across layers: %d' % tot)


if __name__ == '__main__':
    main()
