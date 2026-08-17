"""build_freportn.py -- North Freeport city pass (Ottoman/Dornish desert city).

Idempotent. Three moves:

1. BASE: sandstone building fill. The base's street texture shares the wall
   ink (96,90,80: walls are the long/diagonal strokes, streets a stipple of
   tiny horizontal ticks), so shade_city's component detector only found
   free-standing rooms. Here: global even-odd scanline over the wall ink,
   dropping any run that collides with STREET texture (the wall-ink stipple,
   the tan plaza stipple, water hatch). Building interiors carry only the
   pale citywide wash, which is ignored, so they keep their runs. Shadow ink
   on the lower third of each region, nudged right. Owned inks are stripped
   before refilling, so re-runs are no-ops.

2. _2: replace the old sparse crescent arcs (10-chord circles in the margin,
   inks 205,120,45 / 155,48,36, chord ~14.7) with the desert-mercantile
   margin: minarets, domes, striped awning stalls, palms, evened on all four
   sides, plus long sand-dash sweeps. Frame, compass, corner diamonds, sand
   dashes, figures and title are untouched.

3. _1: APPEND-ONLY wiki POIs (locs transformed native=(-b,-a)), matching
   Brandon's category colors. Skipped if the label already exists.

    python src/tools/build_freportn.py
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'kit'))

import flora_hd
import freeport_decor as FD

MAPS = os.environ.get('EQ_MAPS', 'Emoda Legends Maps')
CRLF = '\r\n'
WALL = (96, 90, 80)
ROOF = (196, 150, 96)        # sandstone (shade_city STYLES)
SHADOW = (150, 108, 62)
BASE_OWNED = {ROOF, SHADOW}

OLD_ARC_INKS = {(205, 120, 45), (155, 48, 36)}
KEEP_ALWAYS = {(45, 40, 38), (115, 110, 104), (116, 88, 56)}  # frame/title/figures


def read(path):
    return open(path, encoding='utf-8').read().splitlines()


def write(path, lines):
    open(path, 'w', newline='', encoding='utf-8').write(CRLF.join(lines) + CRLF)
    b = open(path, 'rb').read()
    assert sum(1 for i, c in enumerate(b)
               if c == 10 and (i == 0 or b[i - 1] != 13)) == 0, 'CRLF broke'


def parse_L(line):
    f = line[2:].split(',')
    return (float(f[0]), float(f[1]), float(f[3]), float(f[4]),
            (int(f[6]), int(f[7]), int(f[8])))


def fmt(x1, y1, x2, y2, ink):
    return 'L %.4f, %.4f, 0.0000, %.4f, %.4f, 0.0000, %d, %d, %d' % (
        x1, y1, x2, y2, *ink)


# ---------------------------------------------------------------- base fill
# Interior seed points for the structures that should read as sandstone
# blocks. Each is an indoor NPC/merchant /loc from the wiki, transformed
# native=(-b,-a) -- a guaranteed point INSIDE the building footprint.
SEEDS = [
    ('Bank of Freeport', 230, 40),
    ('Hall of Truth', 142, -239),
    ('Hall of Truth E', 189, -259),
    ("Marsheart's Chords", -570, 135),
    ("Groflah's Forge", -470, 27),
    ('Office of Landholders', -295, -295),
    ('Coalition of Tradefolk', -200, 117),
    ('Emporium N', 139, -27),
    ('Emporium S', 154, -64),
    ('Clothier Shop', 185, 100),
    ('Inn by the gate', 50, 187),
]

# Fallback for buildings whose door gaps defeat the flood: per row, fill the
# wall-crossing span containing the seed x. Rows touching water are skipped,
# so the Temple's piranha moat stays open. (name, seed_x, y_top, y_bottom)
COLUMN_FILLS = [
    ('Temple of Marr', -350, -160, -30),
    ("Tassel's Tavern", 40, -96, -60),
    ('Blue Building', -202, 156, 202),
    ('Jade Tiger Den', -64, -92, -52),
]
CELL = 2.0
DILATE_DOOR = 4          # cells: closes door gaps for the core flood
MAX_SPAN = 160.0         # a building bbox larger than this is a leak


def refill_base(path):
    raw = [l for l in read(path) if l.strip()]
    kept = [l for l in raw if not (l.startswith('L') and
                                   parse_L(l)[4] in BASE_OWNED)]
    segs = [parse_L(l) for l in kept if l.startswith('L')]
    walls = [s for s in segs if s[4] == WALL]

    # rasterize walls onto a coarse grid
    xs = [v for s in walls for v in (s[0], s[2])]
    ys = [v for s in walls for v in (s[1], s[3])]
    x0, y0 = min(xs) - 8, min(ys) - 8
    W = int((max(xs) - x0) / CELL) + 8
    H = int((max(ys) - y0) / CELL) + 8
    wall_cells = set()
    for (ax, ay, bx, by, _c) in walls:
        n = max(1, int(math.hypot(bx - ax, by - ay) / (CELL * 0.5)))
        for i in range(n + 1):
            t = i / n
            cx = int((ax + (bx - ax) * t - x0) / CELL)
            cy = int((ay + (by - ay) * t - y0) / CELL)
            wall_cells.add((cx, cy))

    def dilate(cells, k):
        out = set()
        for (cx, cy) in cells:
            for dx in range(-k, k + 1):
                for dy in range(-k, k + 1):
                    out.add((cx + dx, cy + dy))
        return out

    barrier0 = dilate(wall_cells, 1)
    barriers = {k: dilate(wall_cells, k) for k in (4, 6, 8)}

    def flood(seed_cell, barrier, cap):
        stack = [seed_cell]
        region = set()
        while stack:
            c = stack.pop()
            if c in region or c in barrier:
                continue
            if not (0 <= c[0] < W and 0 <= c[1] < H):
                return None                      # leaked off-grid
            region.add(c)
            if len(region) > cap:
                return None                      # leaked into the streets
            stack.extend(((c[0] + 1, c[1]), (c[0] - 1, c[1]),
                          (c[0], c[1] + 1), (c[0], c[1] - 1)))
        return region

    cap = int((MAX_SPAN / CELL) ** 2)
    new = []
    n_ok = 0
    for (name, sx, sy) in SEEDS:
        sc = (int((sx - x0) / CELL), int((sy - y0) / CELL))
        core = None
        used_k = None
        for k in sorted(barriers):               # widen the door-closing
            barrier1 = barriers[k]               # dilation until it holds
            if sc in barrier1:                   # seed sits inside the thick
                for d in range(1, k + 3):        # wall band: nudge outward
                    for (dx, dy) in ((d, 0), (-d, 0), (0, d), (0, -d),
                                     (d, d), (-d, -d), (d, -d), (-d, d)):
                        c2 = (sc[0] + dx, sc[1] + dy)
                        if c2 not in barrier1:
                            core = flood(c2, barrier1, cap)
                            if core:
                                break
                    if core:
                        break
            else:
                core = flood(sc, barrier1, cap)
            if core:
                used_k = k
                break
        if not core:
            print(f'  seed {name}: leaked at every dilation, skipped')
            continue
        # expand the core back through the door-closing dilation, walls stop it
        region = set(core)
        frontier = set(core)
        for _ in range(used_k):
            nxt = set()
            for (cx, cy) in frontier:
                for c2 in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                    if c2 not in region and c2 not in barrier0:
                        nxt.add(c2)
            region |= nxt
            frontier = nxt
        gx = [c[0] for c in region]
        gy = [c[1] for c in region]
        if (max(gx) - min(gx)) * CELL > MAX_SPAN or \
           (max(gy) - min(gy)) * CELL > MAX_SPAN:
            print(f'  seed {name}: region too large, skipped')
            continue
        n_ok += 1
        # region -> horizontal runs every other cell row
        y_sh = min(gy) + (max(gy) - min(gy)) * 0.62
        for row in range(min(gy), max(gy) + 1, 2):
            cols = sorted(c[0] for c in region if c[1] == row)
            if not cols:
                continue
            spans = []
            a = b = cols[0]
            for c in cols[1:]:
                if c == b + 1:
                    b = c
                else:
                    spans.append((a, b))
                    a = b = c
            spans.append((a, b))
            yy = y0 + (row + 0.5) * CELL
            ink = SHADOW if row > y_sh else ROOF
            off = 1.5 if row > y_sh else 0.0
            for (a, b) in spans:
                if b - a < 2:
                    continue
                new.append(fmt(x0 + (a + 0.35) * CELL + off, yy,
                               x0 + (b + 0.65) * CELL + off, yy, ink))
    # ---- column-fill fallback (wide-doored halls; skips water rows)
    WATER = {(40, 92, 158), (52, 92, 148), (112, 178, 222), (96, 164, 212)}
    whoriz = {}
    for s in segs:
        if s[4] in WATER:
            yl, yh = sorted((s[1], s[3]))
            for band in range(int(yl // 4), int(yh // 4) + 1):
                whoriz.setdefault(band, []).append(s)
    vwalls = [s for s in walls if abs(s[1] - s[3]) > 0.05]
    n_col = 0
    for (name, sx, ytop, ybot) in COLUMN_FILLS:
        n_col += 1
        y_sh = ytop + (ybot - ytop) * 0.62
        y = ytop + 2.0
        while y < ybot:
            xs = []
            for (x1, y1, x2, y2, _c) in vwalls:
                lo, hi = (y1, y2) if y1 < y2 else (y2, y1)
                if lo <= y < hi:
                    xs.append(x1 + (x2 - x1) * (y - y1) / (y2 - y1))
            xs.sort()
            dd = []
            for x in xs:
                if dd and x - dd[-1] < 5.0:
                    continue
                dd.append(x)
            for i in range(len(dd) - 1):
                if not (dd[i] < sx < dd[i + 1]):
                    continue
                a, b = dd[i] + 2.4, dd[i + 1] - 2.4
                if not (3.5 <= b - a <= 95):
                    break
                wet = False
                for s in whoriz.get(int(y // 4), []):
                    yl, yh = sorted((s[1], s[3]))
                    if yl - 2.5 <= y <= yh + 2.5 and \
                       min(b, max(s[0], s[2])) - max(a, min(s[0], s[2])) > 1.0:
                        wet = True
                        break
                if wet:
                    break
                ink = SHADOW if y > y_sh else ROOF
                off = 1.5 if y > y_sh else 0.0
                new.append(fmt(a + off, y, b + off, y, ink))
                break
            y += 4.0
    print(f'base: {n_ok}/{len(SEEDS)} seeded + {n_col} column-filled '
          f'buildings, {len(new)} sandstone runs '
          f'(stripped {len(raw) - len(kept)} owned strokes)')
    write(path, new + kept)


# ---------------------------------------------------------------- margins
BRONZE = FD.PALETTE['bronze']


def _shape(kind, x, y, r, seed=0):
    if kind == 'minaret':
        return FD.minaret_tower(x, y, r, seed=seed)
    if kind == 'dome':
        return FD.dome_roof(x, y, r, seed=seed)
    if kind == 'stall':
        return FD.awning_stall(x, y, r, seed=seed)
    if kind == 'palm':
        return flora_hd.palm(x, y, r, seed=seed or 1)
    raise KeyError(kind)


def in_margin(x, y):
    """True in the frame margin ring (outside the tangible map + title gap)."""
    return x < -750 or x > 500 or y < -770 or y > 535


def margin_art():
    deco = []

    def add(shape):
        for (x1, y1, x2, y2, ink) in shape:
            deco.append(fmt(x1, y1, x2, y2, ink))

    # ---- top band: standing on the existing sand dash line (y ~ -786)
    TOPY = -788.0
    for (x, kind, r, seed) in ((-730, 'minaret', 24, 1), (-620, 'palm', 20, 2),
                               (-490, 'stall', 20, 3), (-330, 'palm', 18, 31),
                               (-165, 'dome', 26, 4), (0, 'minaret', 22, 32),
                               (125, 'stall', 20, 5), (300, 'dome', 24, 33),
                               (468, 'minaret', 24, 6), (540, 'palm', 16, 7)):
        add(_shape(kind, x, TOPY, r, seed))
    # extend the ground dash line where the old one stops
    for (x0, x1) in ((-758, -700), (-672, -628), (-596, -540),
                     (462, 500), (516, 552)):
        deco.append(fmt(x0, -785.78, x1, -785.78, BRONZE))

    # ---- bottom band: base y 588 (inner frame at 591)
    BOTY = 588.0
    for (x, kind, r, seed) in ((-700, 'palm', 18, 8), (-560, 'dome', 24, 9),
                               (-420, 'minaret', 21, 10), (-280, 'stall', 19, 11),
                               (-140, 'palm', 18, 12), (0, 'dome', 25, 13),
                               (140, 'minaret', 21, 14), (285, 'palm', 18, 15),
                               (420, 'stall', 19, 16)):
        add(_shape(kind, x, BOTY, r, seed))
    for (x0, x1) in ((-758, -726), (-668, -594), (-528, -452),
                     (-390, -314), (-246, -172), (-104, -34),
                     (34, 106), (174, 252), (318, 388), (458, 552)):
        deco.append(fmt(x0, BOTY, x1, BOTY, BRONZE))

    # ---- left band: x center -786 (band -815..-756)
    for (y, kind, r, seed) in ((-560, 'minaret', 20, 17), (-380, 'palm', 17, 18),
                               (-200, 'dome', 24, 19), (-20, 'stall', 17, 20),
                               (160, 'minaret', 20, 21), (340, 'palm', 17, 22),
                               (500, 'dome', 22, 23)):
        add(_shape(kind, -786, y, r, seed))

    # ---- right band: x center 534 (band 504..563)
    for (y, kind, r, seed) in ((-560, 'palm', 17, 24), (-380, 'dome', 24, 25),
                               (-200, 'minaret', 20, 26), (-20, 'palm', 17, 27),
                               (160, 'stall', 17, 28), (340, 'minaret', 20, 29),
                               (500, 'palm', 16, 30)):
        add(_shape(kind, 534, y, r, seed))

    # ---- long sand-dash sweeps across the open ground corners
    add(FD.sand_sweep(-740, -430, -400, -465, bow=0.10))   # top-left interior
    add(FD.sand_sweep(240, -395, 485, -430, bow=-0.08))    # top-right interior
    add(FD.sand_sweep(320, 445, 495, 415, bow=0.08))       # bottom-right interior
    add(FD.sand_sweep(-735, 470, -470, 445, bow=-0.08))    # bottom-left interior
    return deco


def deco_owned_inks():
    """Every ink the margin art can emit. Stripping is zone-restricted (see
    rebuild_deco) because 'hull' (116,88,56) is also the kept figures' ink and
    'flag'/'stone' family inks echo legacy margin art."""
    inks = set(FD.PALETTE.values())
    for shape in (flora_hd.palm(0, 0, 18, seed=1), flora_hd.palm(0, 0, 18, seed=4)):
        for s in shape:
            inks.add(tuple(s[4]))
    return inks


def rebuild_deco(path):
    raw = [l for l in read(path) if l.strip()]
    owned = deco_owned_inks()
    kept = []
    dropped = 0
    for l in raw:
        if l.startswith('L'):
            s = parse_L(l)
            mx, my = (s[0] + s[2]) / 2, (s[1] + s[3]) / 2
            if s[4] in KEEP_ALWAYS:
                kept.append(l)
                continue
            if s[4] == BRONZE:                # sweeps + dash extensions, ours
                dropped += 1
                continue
            if s[4] in owned and in_margin(mx, my):
                dropped += 1                  # ours from a previous run
                continue
            if s[4] in OLD_ARC_INKS:
                d = math.hypot(s[2] - s[0], s[3] - s[1])
                if d < 20.0:                  # old crescent chords are ~14.7;
                    dropped += 1              # also re-collects our short
                    continue                  # stall-stripe strokes on re-runs
        kept.append(l)
    new = margin_art()
    print(f'deco: dropped {dropped} old strokes, added {len(new)} margin strokes')
    write(path, kept + new)


# ---------------------------------------------------------------- POIs (_1)
POIS = [
    # native x, native y, z, r, g, b, size, label  (wiki /loc -> native (-b,-a))
    (40, -75, 0, 30, 70, 90, 2, "Tassel's_Tavern_(#12_Brew_Barrel)"),
    (146, -45, 0, 30, 70, 90, 2, "Emporium_(#13_Cloth)"),
    (195, 95, 0, 30, 70, 90, 2, "Clothier_Shop_(#19_Pottery/Cloth)"),
    (25, -230, 0, 30, 70, 90, 2, "Hall_of_Truth_Moat_(Minnows)"),
    (-528, 113, 0, 165, 60, 20, 2, "Marus_Kemson_(GM_BRD)"),
    (-580, -475, 0, 140, 35, 30, 2, "Bondl_Felligan_(Shaman_Epic)"),
    (57, 104, 0, 35, 95, 55, 2, "Timor_Strongbranch_(Fletching)"),
    (257, -132, 0, 110, 0, 60, 2, "Guard_Willia_(Token_of_Truth)"),
]


def append_pois(path):
    raw = [l for l in read(path) if l.strip()]
    have = set()
    for l in raw:
        if l.startswith('P'):
            have.add(l.rsplit(',', 1)[-1].strip())
    added = 0
    for (x, y, z, r, g, b, sz, label) in POIS:
        if label in have:
            continue
        raw.append('P %.4f, %.4f, %.4f, %d, %d, %d, %d, %s'
                   % (x, y, z, r, g, b, sz, label))
        added += 1
    print(f'_1: appended {added} POIs')
    write(path, raw)


def main():
    base = os.path.join(MAPS, 'freportn.txt')
    deco = os.path.join(MAPS, 'freportn_2.txt')
    poi = os.path.join(MAPS, 'freportn_1.txt')
    refill_base(base)
    rebuild_deco(deco)
    append_pois(poi)
    total = sum(len(read(p)) for p in (base, deco, poi))
    print('zone total lines:', total)
    assert total <= 30000, 'stroke budget blown'


if __name__ == '__main__':
    main()
