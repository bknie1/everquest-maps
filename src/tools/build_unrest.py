"""build_unrest.py -- the Estate of Unrest flagship pass.

Idempotent: every ink this script writes is owned by it, and it strips those
inks from the target layers before re-drawing. Base gets the manor/gazebo
shading (under everything); _2 gets hedge shading, figures, trees, the entry
gate, the checkerboard, pillars, and the storm margins.

    python src/tools/build_unrest.py
"""
import math
import os
import random
import sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, '..', 'kit'))
sys.path.insert(0, HERE)

from fauna_hd_zombie import zombie
from fauna_hd_ghoul import ghoul
from unrest_decor import (scarecrow, death_beetle, stone_gate, checkerboard,
                          pillar, GLOW)
import flora_hd
import terrain
from shade_city import components as sc_components, fill_component, parse as sc_parse

MAPS = os.environ.get('EQ_MAPS', 'Emoda Legends Maps')
CRLF = '\r\n'

PALE = (130, 140, 120)
BLUE = (80, 98, 112)
GREEN = (74, 106, 64)

ROOF = (128, 102, 68)        # warm wood-brown roof wash
ROOF_DK = (94, 72, 48)       # shadow side
HEDGE = (46, 72, 48)         # dark clipped-hedge green
CLOUD = (112, 114, 126)      # storm grey
CLOUD_DK = (78, 80, 94)
BOLT = (210, 200, 150)       # pale yellow-white lightning
BOLT_DK = (86, 80, 96)       # dark offset echo
RAIN = (118, 128, 146)       # grey-blue rain

BASE_OWNED = {ROOF, ROOF_DK}


def _probe_inks():
    """Every ink the kit shapes can emit, discovered by running them once --
    hardcoded lists rot (BRAIN 13.5: a shared/forgotten ink is a future bug)."""
    inks = set()
    probes = (zombie(0, 0, 20, seed=1), ghoul(0, 0, 14, seed=1),
              scarecrow(0, 0, 30, seed=1), death_beetle(0, 0, 7, seed=1),
              stone_gate(0, 0, 15, seed=1), checkerboard(0, 0, 5), pillar(0, 0, 3),
              flora_hd.broadleaf(0, 0, 20, seed=1), flora_hd.fir(0, 0, 20, seed=1),
              flora_hd.broadleaf(0, 0, 20, seed=5), flora_hd.fir(0, 0, 20, seed=7),
              flora_hd.bush(0, 0, 10, seed=1), flora_hd.bush(0, 0, 10, seed=3))
    for shape in probes:
        for s in shape:
            inks.add(tuple(s[4]))
    return inks


DECO_OWNED = {HEDGE, CLOUD, CLOUD_DK, BOLT, BOLT_DK, RAIN} | _probe_inks()


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
    out = []
    for ln in lines:
        if ln.startswith('L') and ink_of(ln) in owned:
            continue
        out.append(ln)
    return out


def segs_of(lines):
    out = []
    for ln in lines:
        if ln.startswith('L'):
            q = ln[2:].split(',')
            out.append((float(q[0]), float(q[1]), float(q[3]), float(q[4]),
                        (int(q[6]), int(q[7]), int(q[8]))))
    return out


# ---------------------------------------------------------------- base layer

def manor_wash(segs):
    """One warm-brown wash across the manor footprint: per row, fill between
    the outermost pale crossings. Lower third gets the shadow ink."""
    box = (-168, 168, -806, -488)
    sub = [(x1, y1, x2, y2) for (x1, y1, x2, y2, c) in segs if c == PALE
           and box[0] <= min(x1, x2) and max(x1, x2) <= box[1]
           and box[2] <= min(y1, y2) and max(y1, y2) <= box[3]]
    out = []
    y0, y1 = box[2], box[3]
    shadow_from = y0 + (y1 - y0) * 0.62
    y = y0 + 3.0
    while y < y1:
        xs = []
        for (a1, b1, a2, b2) in sub:
            if (b1 > y) != (b2 > y):
                xs.append(a1 + (y - b1) * (a2 - a1) / (b2 - b1))
        if len(xs) >= 2:
            a, b = min(xs) + 1.5, max(xs) - 1.5
            if b - a > 8:
                ink = ROOF_DK if y > shadow_from else ROOF
                off = 1.5 if y > shadow_from else 0.0
                out.append(fmt(a + off, y, b + off, y, ink))
        y += 5.5
    return out


def gazebo_roof(segs):
    """Shade the gazebo (the rich pale component on the east lawn)."""
    sub = [s for s in segs if s[4] == PALE
           and 240 <= min(s[0], s[2]) and max(s[0], s[2]) <= 305
           and -535 <= min(s[1], s[3]) and max(s[1], s[3]) <= -465]
    out = []
    for comp in sc_components(sub):
        strokes = [sub[j] for j in comp]
        if len(strokes) < 40:
            continue
        cy = [v for s in strokes for v in (s[1], s[3])]
        shadow_from = min(cy) + (max(cy) - min(cy)) * 0.62
        for (a, y, b) in fill_component(strokes, 5.5):
            ink = ROOF_DK if y > shadow_from else ROOF
            out.append(fmt(a, y, b, y, ink))
    return out


# ---------------------------------------------------------------- _2 layer

def hedge_shading(base_segs):
    """Thicken every maze wall stroke with a dark parallel stroke either side:
    the maze reads as dense clipped hedges, corridors stay parchment."""
    blocks = ((-250, -5, -460, -305), (5, 250, -460, -305))
    out = []
    for (x1, y1, x2, y2, c) in base_segs:
        if c != GREEN:
            continue
        inside = any(bx0 <= min(x1, x2) and max(x1, x2) <= bx1 and
                     by0 <= min(y1, y2) and max(y1, y2) <= by1
                     for (bx0, bx1, by0, by1) in blocks)
        if not inside:
            continue
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy)
        if L < 1.0:
            continue
        nx, ny = -dy / L, dx / L
        # trim ends slightly so corners do not sprout spurs
        t = min(0.9, L * 0.08) / L
        ax, ay = x1 + dx * t, y1 + dy * t
        bx, by = x2 - dx * t, y2 - dy * t
        for k in (-1.7, 1.7):
            out.append(fmt(ax + nx * k, ay + ny * k, bx + nx * k, by + ny * k, HEDGE))
    return out


def rear_pillars(base_segs):
    """Sandstone pillar pair outside the rear (north) entrance: find the door
    gap in the north wing's back wall from the geometry itself."""
    spans = []
    for (x1, y1, x2, y2, c) in base_segs:
        if c == PALE and abs(y1 - y2) < 0.5 and -766 <= y1 <= -755 \
                and -105 <= min(x1, x2) and max(x1, x2) <= 10:
            spans.append((min(x1, x2), max(x1, x2)))
    spans.sort()
    out = []
    gap = None
    for i in range(len(spans) - 1):
        g0, g1 = spans[i][1], spans[i + 1][0]
        if 6 <= g1 - g0 <= 30:
            gap = (g0, g1)
            break
    if gap is None:
        gap = (-58, -42)     # fall back to the porch centre
    y = -769.5
    for s in pillar(gap[0] - 3.0, y, 3.2) + pillar(gap[1] + 3.0, y, 3.2):
        out.append(fmt(*s[:4], s[4]))
    return out, gap


def interior_pillars(base_segs):
    """Sandstone markers on small square footprints inside the manor."""
    out = []
    spots = []
    for ink in (PALE, BLUE):
        sub = [s for s in base_segs if s[4] == ink
               and -170 <= min(s[0], s[2]) and max(s[0], s[2]) <= 170
               and -810 <= min(s[1], s[3]) and max(s[1], s[3]) <= -490]
        for comp in sc_components(sub):
            if not 4 <= len(comp) <= 14:
                continue
            xs = [v for j in comp for v in (sub[j][0], sub[j][2])]
            ys = [v for j in comp for v in (sub[j][1], sub[j][3])]
            w, h = max(xs) - min(xs), max(ys) - min(ys)
            if 4 <= max(w, h) <= 12 and min(w, h) >= 3:
                spots.append(((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2))
    spots = spots[:6]
    for (px, py) in spots:
        for s in pillar(px, py, 2.6):
            out.append(fmt(*s[:4], s[4]))
    return out, spots


def storm_margins(deco_lines):
    """Storm sky in the margins: cloud banks, lightning, long diagonal rain."""
    segs = segs_of(deco_lines)
    grid = [s for s in segs if s[4] == (120, 124, 112)]
    gx0 = min(min(s[0], s[2]) for s in grid); gx1 = max(max(s[0], s[2]) for s in grid)
    gy0 = min(min(s[1], s[3]) for s in grid); gy1 = max(max(s[1], s[3]) for s in grid)
    frame = [s for s in segs if s[4] == (64, 70, 64)]
    fx0 = min(min(s[0], s[2]) for s in frame); fx1 = max(max(s[0], s[2]) for s in frame)
    fy0 = min(min(s[1], s[3]) for s in frame); fy1 = max(max(s[1], s[3]) for s in frame)
    title = [s for s in segs if s[4] == (96, 84, 74) and max(s[1], s[3]) < gy0]
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
    # -- cloud banks along the top margin
    for (cx, cy, w, h, sd) in ((-360, -1092, 150, 40, 11),
                               (95, -1120, 200, 46, 12),
                               (430, -1082, 120, 34, 13)):
        for (x1, y1, x2, y2, c) in terrain.cloud(cx, cy, w, h, ink=CLOUD,
                                                 deep=CLOUD_DK, seed=sd):
            out.append(fmt(x1, y1, x2, y2, c))

    # -- lightning: jagged pale bolts with a dark echo
    bolts = [
        [(-352, -1070), (-386, -1022), (-362, -1000), (-395, -958)],
        [(408, -1062), (442, -1015), (420, -992), (452, -948)],
        [(-437, -680), (-465, -628), (-443, -604), (-472, -552)],
    ]
    for pts in bolts:
        for i in range(len(pts) - 1):
            out.append(fmt(*pts[i], *pts[i + 1], BOLT_DK if False else BOLT))
        for i in range(len(pts) - 1):
            out.append(fmt(pts[i][0] + 3.0, pts[i][1] + 2.5,
                           pts[i + 1][0] + 3.0, pts[i + 1][1] + 2.5, BOLT_DK))
        # forked tip
        tip = pts[-1]
        out.append(fmt(tip[0], tip[1], tip[0] + 9, tip[1] - 14, BOLT))

    # -- rain: long 65-degree strokes sweeping the margin bands
    rnd = random.Random(7)
    bands = [
        (fx0 + 6, gx0 - 8, gy0 - 6, gy1 + 4),          # left
        (gx1 + 8, fx1 - 6, gy0 - 6, gy1 + 4),          # right
        (fx0 + 6, fx1 - 6, fy0 + 8, gy0 - 10),         # top
        (fx0 + 6, fx1 - 6, gy1 + 8, fy1 - 8),          # bottom
    ]
    n_target = 170
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


def figures_and_trees():
    out = []
    S = lambda seglist: out.extend(fmt(*s[:4], s[4]) for s in seglist)

    # shambling zombies on the grounds
    S(zombie(-70, -470, 16, seed=2, face=1))
    S(zombie(118, -464, 16, seed=5, face=-1))
    S(zombie(-278, -482, 15, seed=8, face=1))
    S(zombie(-185, -792, 15, seed=11, face=-1))

    # ghouls inside the manor, clear of the room labels
    S(ghoul(-90, -600, 12, seed=3, face=1))
    S(ghoul(-25, -555, 12, seed=7, face=-1))

    # death beetles in the yard
    S(death_beetle(28, -506, 7, seed=1))
    S(death_beetle(-52, -416, 6, seed=2))
    S(death_beetle(152, -522, 6, seed=3))

    # the signature scarecrows
    S(scarecrow(-190, -462, 30, seed=4))
    S(scarecrow(205, -483, 30, seed=9))

    # the Rockefeller-carriage stone gate at the forecourt entrance
    S(stone_gate(0.44, -424, 15, seed=1))

    # checkerboard floor in the rear octagon (1F)
    S(checkerboard(52, -722, 5.0, 6))

    # Faydwer mixed forest on the grounds
    trees = [
        ('b', -285, -700, 22), ('f', -248, -628, 18), ('b', -292, -548, 20),
        ('f', -218, -756, 19), ('b', -128, -848, 20), ('f', -42, -858, 17),
        ('b', 72, -852, 21), ('f', -190, -838, 18), ('b', 115, -812, 18),
        ('f', 172, -652, 17), ('b', 164, -578, 18), ('f', -282, -428, 18),
        ('b', 225, -448, 17),
    ]
    for i, (kind, tx, ty, ts) in enumerate(trees):
        fn = flora_hd.broadleaf if kind == 'b' else flora_hd.fir
        S(fn(tx, ty, ts, seed=i * 3 + 1))
    S(flora_hd.bush(-64, -268, 10, seed=21))
    S(flora_hd.bush(64, -246, 10, seed=22))
    return out


def main():
    base_p = os.path.join(MAPS, 'unrest.txt')
    deco_p = os.path.join(MAPS, 'unrest_2.txt')

    base = strip_owned(load(base_p), BASE_OWNED)
    deco = strip_owned(load(deco_p), DECO_OWNED)

    # the east shore outline shares the basement's ink; give the waterline the
    # water's own ink so the lake reads as water, not as an elevation contour
    WATER = (64, 108, 152)
    recol = 0
    for i, ln in enumerate(base):
        if not ln.startswith('L'):
            continue
        q = ln[2:].split(',')
        if (int(q[6]), int(q[7]), int(q[8])) == BLUE \
                and min(float(q[0]), float(q[3])) > 195:
            base[i] = 'L %s, %d, %d, %d' % (','.join(q[:6]).strip(), *WATER)
            recol += 1
    print('shoreline strokes recoloured: %d' % recol)
    base_segs = segs_of(base)

    wash = manor_wash(base_segs) + gazebo_roof(base_segs)
    base_out = wash + base
    print('base: +%d wash runs -> %d L' % (
        len(wash), sum(1 for l in base_out if l.startswith('L'))))

    add = []
    hs = hedge_shading(base_segs); add += hs
    print('hedge shading: %d' % len(hs))
    rp, gap = rear_pillars(base_segs); add += rp
    print('rear entrance gap found at x %.1f..%.1f' % gap)
    ip, spots = interior_pillars(base_segs); add += ip
    print('interior pillar footprints:', [(round(x), round(y)) for x, y in spots])
    ft = figures_and_trees(); add += ft
    print('figures/trees/gate/checker: %d' % len(ft))
    deco_mid = deco + add
    sm = storm_margins(deco_mid)
    print('storm margins: %d' % len(sm))
    deco_out = deco_mid + sm
    print('deco: %d L' % sum(1 for l in deco_out if l.startswith('L')))

    save(base_p, base_out)
    save(deco_p, deco_out)
    tot = sum(1 for l in base_out + deco_out if l.startswith('L'))
    for extra in ('unrest_1.txt', 'unrest_3.txt'):
        p = os.path.join(MAPS, extra)
        if os.path.exists(p):
            tot += sum(1 for l in load(p) if l.startswith('L'))
    print('zone total L across layers: %d' % tot)


if __name__ == '__main__':
    main()
