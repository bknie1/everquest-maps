"""landmarks.py -- world landmark sketches drawn at their true /loc positions.

Unlike margin art, these sit INSIDE the map at real coordinates: druid rings,
wizard spires, and whatever else a player would use to orient. Keep them small
enough that labels still read (2-4% of the zone span).

Each function returns a list of (x1, y1, x2, y2, (r, g, b)) strokes.
"""
import math
import random

STONE = (108, 108, 92)
STONE_DARK = (78, 78, 64)
RUNE = (140, 60, 40)


def druid_ring(cx, cy, r, seed=0):
    """Rune-marked standing-stone circle, plan view with standing-stone height.

    Eight stones around an ellipse (squashed for the top-down-ish house look);
    front stones taller, each a tapered block with a hatched shadow side, one
    carrying a rune stroke. r is the ring radius.
    """
    rng = random.Random(seed)
    out = []
    n = 8
    for k in range(n):
        a = 2 * math.pi * k / n + rng.uniform(-0.08, 0.08)
        sx = cx + r * math.cos(a)
        sy = cy + r * 0.62 * math.sin(a)
        depth = (math.sin(a) + 1) / 2                 # 0 back .. 1 front
        h = r * (0.42 + 0.30 * depth)                 # front stones taller
        w = r * rng.uniform(0.16, 0.22)
        lean = rng.uniform(-0.12, 0.12) * w
        # block: two verticals + top; slight taper and lean
        x0, x1 = sx - w / 2, sx + w / 2
        t0, t1 = x0 + w * 0.12 + lean, x1 - w * 0.12 + lean
        out.append((x0, sy, t0, sy - h, STONE))
        out.append((x1, sy, t1, sy - h, STONE))
        out.append((t0, sy - h, t1, sy - h, STONE))
        out.append((x0, sy, x1, sy, STONE_DARK))      # foot line
        # shadow-side hatch (east face)
        for j in range(2 + int(2 * depth)):
            yy = sy - h * (0.2 + 0.6 * j / 3)
            out.append((x1 - w * 0.18, yy, x1 - w * 0.02, yy + h * 0.06, STONE_DARK))
        # one rune on the most frontal stones
        if depth > 0.75:
            rx, ry = sx + lean * 0.5, sy - h * 0.62
            out.append((rx - w * 0.10, ry - h * 0.10, rx + w * 0.10, ry - h * 0.10, RUNE))
            out.append((rx, ry - h * 0.10, rx, ry + h * 0.14, RUNE))
    # worn ground ellipse hinted by short arcs
    for k in range(6):
        a0 = 2 * math.pi * (k / 6) + 0.12
        a1 = a0 + 0.55
        out.append((cx + r * 1.22 * math.cos(a0), cy + r * 0.62 * 1.22 * math.sin(a0),
                    cx + r * 1.22 * math.cos(a1), cy + r * 0.62 * 1.22 * math.sin(a1),
                    STONE_DARK))
    return out


def stratovolcano(cx, base_y, w, h, seed=0, snow=True, secondary=True):
    """A Shasta-like solitary volcano: broad concave cone, snow cap, glacier
    streaks, optional secondary cone on the left shoulder (Shastina).

    cx, base_y = center of the base line; w = base width; h = height.
    """
    rng = random.Random(seed)
    ROCK = (110, 88, 66)
    SHADE = (86, 68, 50)
    SNOW = (152, 162, 172)
    out = []
    apex = (cx + rng.uniform(-0.02, 0.02) * w, base_y - h)

    def flank(x_end, bulge):
        """Concave profile from apex to a base end, 4 segments."""
        pts = [apex]
        for t in (0.3, 0.55, 0.8, 1.0):
            px = apex[0] + (x_end - apex[0]) * t
            py = apex[1] + (base_y - apex[1]) * (t ** (1.0 + bulge))
            pts.append((px, py))
        for i in range(len(pts) - 1):
            out.append((pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], ROCK))
        return pts

    left = flank(cx - w / 2, 0.35)
    right = flank(cx + w / 2, 0.30)
    # crater notch
    out.append((apex[0] - w * 0.015, apex[1], apex[0], apex[1] + h * 0.03, ROCK))
    out.append((apex[0], apex[1] + h * 0.03, apex[0] + w * 0.02, apex[1] - h * 0.005, ROCK))
    if secondary:
        # Shastina: smaller cone riding the left shoulder
        sx = cx - w * 0.30
        sy = base_y - h * 0.52
        sw, sh = w * 0.22, h * 0.34
        s_apex = (sx, sy - sh)
        out.append((sx - sw / 2, sy + h * 0.10, s_apex[0], s_apex[1], ROCK))
        out.append((s_apex[0], s_apex[1], sx + sw * 0.35, sy - sh * 0.35, ROCK))
        if snow:
            out.append((sx - sw * 0.2, s_apex[1] + sh * 0.25,
                        sx + sw * 0.15, s_apex[1] + sh * 0.30, SNOW))
    if snow:
        # snowline: broken zigzag across the upper third, then glacier streaks
        sl = base_y - h * 0.62
        px = None
        for k in range(9):
            t = k / 8
            x = apex[0] + (t - 0.5) * w * 0.5
            y = sl + rng.uniform(-1, 1) * h * 0.04 + abs(t - 0.5) * h * 0.16
            if px is not None and rng.random() < 0.8:
                out.append((px[0], px[1], x, y, SNOW))
            px = (x, y)
        for k in range(4):
            gx = apex[0] + rng.uniform(-0.16, 0.16) * w
            g0 = apex[1] + h * rng.uniform(0.08, 0.15)
            out.append((gx, g0, gx + rng.uniform(-0.03, 0.03) * w,
                        g0 + h * rng.uniform(0.18, 0.30), SNOW))
    # shadow hatch on the southeast flank
    for k in range(6):
        t = 0.30 + k * 0.11
        ax = apex[0] + (right[-1][0] - apex[0]) * t
        ay = apex[1] + (base_y - apex[1]) * (t ** 1.3)
        out.append((ax, ay, ax - w * 0.045, ay + h * 0.09, SHADE))
    # foothill skirt
    for sgn in (-1, 1):
        fx = cx + sgn * w * rng.uniform(0.52, 0.60)
        out.append((fx, base_y, fx + sgn * w * 0.10, base_y - h * 0.06, ROCK))
        out.append((fx + sgn * w * 0.10, base_y - h * 0.06, fx + sgn * w * 0.18, base_y, ROCK))
    return out


def karana_bridge(cx, cy, w, seed=0):
    """The great chained bridge of the Karanas, side view: timber deck on two
    piers, four big diagonal strut beams radiating from the crowns, chains
    staked to the earth with pegs."""
    rng = random.Random(seed)
    TIMBER = (124, 96, 62)
    DARK = (92, 70, 46)
    CHAIN = (104, 104, 104)
    out = []
    h = w * 0.34
    deck_y = cy - h * 0.45
    # deck: gentle arc, doubled
    px = None
    for k in range(9):
        t = k / 8
        x = cx - w / 2 + w * t
        y = deck_y - math.sin(math.pi * t) * h * 0.10
        if px:
            out.append((px[0], px[1], x, y, TIMBER))
            out.append((px[0], px[1] + h * 0.06, x, y + h * 0.06, DARK))
        px = (x, y)
    # planking ticks
    for k in range(7):
        t = 0.08 + k * 0.14
        x = cx - w / 2 + w * t
        y = deck_y - math.sin(math.pi * t) * h * 0.10
        out.append((x, y, x, y + h * 0.06, DARK))
    # two piers
    for sgn in (-1, 1):
        bx = cx + sgn * w * 0.22
        out.append((bx - w * 0.03, cy, bx - w * 0.02, deck_y, TIMBER))
        out.append((bx + w * 0.03, cy, bx + w * 0.02, deck_y, TIMBER))
        for j in range(3):
            yy = cy - (cy - deck_y) * (j + 0.5) / 3
            out.append((bx - w * 0.03, yy, bx + w * 0.03, yy, DARK))
        # crown: two strut beams radiating outward-up
        crown = (bx, deck_y - h * 0.12)
        out.append((bx - w * 0.02, deck_y, crown[0], crown[1], TIMBER))
        for beam_sgn in (-1, 1):
            tip = (bx + beam_sgn * w * rng.uniform(0.26, 0.32),
                   deck_y - h * rng.uniform(0.55, 0.75))
            out.append((crown[0], crown[1], tip[0], tip[1], TIMBER))
            out.append((crown[0] + w * 0.012, crown[1] + h * 0.03,
                        tip[0] + w * 0.012, tip[1] + h * 0.03, DARK))
            # chain from beam tip staked to the ground: dashed sag curve + peg
            gx = tip[0] + beam_sgn * w * 0.14
            for k in range(4):
                t0, t1 = k / 4, (k + 0.6) / 4
                def sag(t):
                    x = tip[0] + (gx - tip[0]) * t
                    y = tip[1] + (cy - tip[1]) * (t ** 0.8) + math.sin(math.pi * t) * h * 0.06
                    return x, y
                a, b = sag(t0), sag(t1)
                out.append((a[0], a[1], b[0], b[1], CHAIN))
            out.append((gx - w * 0.012, cy, gx + w * 0.012, cy - h * 0.06, DARK))  # peg
    return out


def mine_entrance(cx, cy, w, seed=0, caved_in=True):
    """Dwarven mine adit: timber portal (posts + heavy lintel), rune mark,
    rubble pile choking the opening, a stub of cart rail."""
    rng = random.Random(seed)
    TIMBER = (118, 94, 62)
    STONE = (108, 108, 92)
    DARK = (78, 78, 64)
    RUNE = (140, 60, 40)
    out = []
    h = w * 0.75
    # portal posts, slightly leaning
    out.append((cx - w * 0.32, cy, cx - w * 0.28, cy - h * 0.72, TIMBER))
    out.append((cx + w * 0.32, cy, cx + w * 0.26, cy - h * 0.70, TIMBER))
    # heavy lintel, cracked
    out.append((cx - w * 0.36, cy - h * 0.72, cx - w * 0.02, cy - h * 0.76, TIMBER))
    out.append((cx + w * 0.02, cy - h * 0.73, cx + w * 0.34, cy - h * 0.70, TIMBER))
    out.append((cx - w * 0.02, cy - h * 0.76, cx + w * 0.02, cy - h * 0.73, DARK))  # crack
    # rune on the lintel left half
    out.append((cx - w * 0.22, cy - h * 0.80, cx - w * 0.14, cy - h * 0.80, RUNE))
    out.append((cx - w * 0.18, cy - h * 0.80, cx - w * 0.18, cy - h * 0.70, RUNE))
    # hillside over the portal
    out.append((cx - w * 0.55, cy, cx - w * 0.30, cy - h * 0.95, STONE))
    out.append((cx - w * 0.30, cy - h * 0.95, cx + w * 0.05, cy - h * 1.05, STONE))
    out.append((cx + w * 0.05, cy - h * 1.05, cx + w * 0.42, cy - h * 0.80, STONE))
    out.append((cx + w * 0.42, cy - h * 0.80, cx + w * 0.55, cy, STONE))
    if caved_in:
        # rubble choking the opening
        for k in range(7):
            rx = cx + rng.uniform(-0.24, 0.24) * w
            ry = cy - rng.uniform(0.02, 0.34) * h
            rr = w * rng.uniform(0.05, 0.10)
            out.append((rx - rr, ry, rx, ry - rr * 0.8, STONE))
            out.append((rx, ry - rr * 0.8, rx + rr, ry, STONE))
            out.append((rx - rr, ry, rx + rr, ry, DARK))
    # cart rail stub running out
    out.append((cx - w * 0.10, cy, cx - w * 0.20, cy + h * 0.14, DARK))
    out.append((cx + w * 0.02, cy, cx - w * 0.08, cy + h * 0.15, DARK))
    out.append((cx - w * 0.16, cy + h * 0.075, cx - w * 0.02, cy + h * 0.075, DARK))
    return out


def flaming_sword(cx, cy, h, seed=0):
    """Memorial: a sword planted point-down in a stone mound, flames rising
    along the blade. For Aradune. cx, cy = ground point; h = full height."""
    rng = random.Random(seed)
    STEEL = (150, 155, 165)
    STEEL_DARK = (110, 115, 125)
    FLAME = (200, 110, 50)
    FLAME_IN = (230, 170, 60)
    STONE_ = (108, 108, 92)
    out = []
    w = h * 0.30
    tip = (cx, cy)
    guard_y = cy - h * 0.62
    pommel_y = cy - h * 0.92
    # blade: two edges tapering to the tip, center fuller line
    out.append((cx - w * 0.10, guard_y, tip[0], tip[1], STEEL))
    out.append((cx + w * 0.10, guard_y, tip[0], tip[1], STEEL))
    out.append((cx, guard_y - h * 0.01, cx, cy - h * 0.10, STEEL_DARK))
    # crossguard, slightly swept
    out.append((cx - w * 0.55, guard_y - h * 0.035, cx + w * 0.55, guard_y + h * 0.035, STEEL))
    out.append((cx - w * 0.55, guard_y - h * 0.035, cx - w * 0.62, guard_y - h * 0.075, STEEL_DARK))
    out.append((cx + w * 0.55, guard_y + h * 0.035, cx + w * 0.62, guard_y - h * 0.005, STEEL_DARK))
    # grip and pommel
    out.append((cx - w * 0.06, guard_y, cx - w * 0.06, pommel_y, STEEL_DARK))
    out.append((cx + w * 0.06, guard_y, cx + w * 0.06, pommel_y, STEEL_DARK))
    for k in range(3):
        gy = guard_y - (guard_y - pommel_y) * (k + 1) / 4
        out.append((cx - w * 0.06, gy, cx + w * 0.06, gy, STEEL_DARK))
    out.append((cx - w * 0.13, pommel_y, cx + w * 0.13, pommel_y, STEEL))
    out.append((cx - w * 0.13, pommel_y, cx, pommel_y - h * 0.045, STEEL))
    out.append((cx + w * 0.13, pommel_y, cx, pommel_y - h * 0.045, STEEL))
    # flames: wavy licks hugging the blade, inner and outer
    for sgn in (-1, 1):
        for (ink, r0, amp) in ((FLAME, 0.16, 0.10), (FLAME_IN, 0.10, 0.06)):
            px = None
            for k in range(6):
                t = k / 5
                y = cy - h * (0.08 + t * 0.48)
                x = cx + sgn * w * (r0 + math.sin(t * math.pi * 2.2 + sgn) * amp) \
                    * (1.0 - t * 0.35)
                if px and rng.random() < 0.9:
                    out.append((px[0], px[1], x, y, ink))
                px = (x, y)
            # a detached lick above
            lx = cx + sgn * w * rng.uniform(0.12, 0.22)
            ly = cy - h * rng.uniform(0.58, 0.66)
            out.append((lx, ly, lx + sgn * w * 0.05, ly - h * 0.05, FLAME))
    # stone mound at the base
    for k in range(4):
        rx = cx + (k - 1.5) * w * 0.28
        rr = w * rng.uniform(0.10, 0.16)
        out.append((rx - rr, cy, rx, cy - rr, STONE_))
        out.append((rx, cy - rr, rx + rr, cy, STONE_))
    out.append((cx - w * 0.65, cy, cx + w * 0.65, cy, STONE_))
    return out


def wizard_spires(cx, cy, r, seed=0):
    """Cluster of pale crystalline teleport spires: one tall center, three flanks."""
    rng = random.Random(seed)
    PALE = (168, 186, 200)
    PALE_DARK = (120, 140, 158)
    out = []
    spires = [(0, 0, 1.0), (-0.55, 0.18, 0.6), (0.5, 0.22, 0.68), (0.12, 0.34, 0.45)]
    for (ox, oy, s) in spires:
        bx, by = cx + ox * r, cy + oy * r
        h = r * 1.7 * s
        w = r * 0.28 * s
        lean = rng.uniform(-0.06, 0.06) * r
        tip = (bx + lean, by - h)
        out.append((bx - w / 2, by, tip[0], tip[1], PALE))
        out.append((bx + w / 2, by, tip[0], tip[1], PALE))
        out.append((bx - w / 2, by, bx + w / 2, by, PALE_DARK))
        out.append((bx + w * 0.1, by - h * 0.35, tip[0], tip[1], PALE_DARK))  # facet edge
    return out


BLOOD = (150, 44, 38)
BLOOD_DARK = (104, 28, 24)


def splitpaw_claws(cx, cy, r, seed=0):
    """The three curved stone spires over the Lair of Splitpaw tunnel.

    From Brandon's in-game shot: tall stone pillars that curve like claws out
    of the earth, each capped in a bloody red the whole upper third. They are
    the landmark you actually navigate by -- the tunnel mouth itself is a small
    hole between them.
    """
    rng = random.Random(seed)
    out = []
    # three claws around the tunnel, each leaning outward from the centre
    claws = [(-0.62, 0.30, 1.00, -1), (0.58, 0.16, 0.86, 1), (0.02, -0.52, 0.72, 1)]
    for (ox, oy, sc, curl) in claws:
        bx, by = cx + ox * r, cy + oy * r
        h = r * 1.45 * sc
        w = r * 0.30 * sc
        bend = curl * r * 0.34 * sc               # how far the tip hooks over
        N = 7
        left, right = [], []
        for k in range(N + 1):
            t = k / N
            # centreline curves as it rises; width tapers to a point
            mx = bx + bend * t * t
            my = by - h * t
            ww = w * (1.0 - 0.88 * t)
            left.append((mx - ww / 2, my))
            right.append((mx + ww / 2, my))
        for k in range(N):
            top = (k / N) >= 0.66              # upper third wears the blood
            ink = BLOOD if top else STONE
            dark = BLOOD_DARK if top else STONE_DARK
            out.append((left[k][0], left[k][1], left[k + 1][0], left[k + 1][1], ink))
            out.append((right[k][0], right[k][1], right[k + 1][0], right[k + 1][1], dark))
            # cross ties give the pillar mass at map scale; the blood cap gets
            # every tie so it reads as a solid red tip, not a red outline
            if top or k % 2 == 0:
                out.append((left[k][0], left[k][1], right[k][0], right[k][1], ink if top else dark))
            if top:
                mxa = (left[k][0] + right[k][0]) / 2
                mxb = (left[k + 1][0] + right[k + 1][0]) / 2
                out.append((mxa, left[k][1], mxb, left[k + 1][1], BLOOD))
        out.append((left[N][0], left[N][1], right[N][0], right[N][1], BLOOD_DARK))
        out.append((bx - w * 0.75, by, bx + w * 0.75, by, STONE_DARK))          # footing
    return out


def aviak_lookout(cx, cy, h, seed=0):
    """An aviak lookout: a tall tree with a tiny hut lashed on top, standing on
    a hill. From Brandon's shots -- the aviaks build their perches up trees on
    the high ground, so the hill is part of the landmark, not scenery.

    (cx, cy) is the foot of the tree; h is the tree's full height.
    """
    rng = random.Random(seed)
    TRUNK = (110, 84, 52)
    TRUNK_D = (78, 58, 36)
    LEAF = (72, 102, 60)
    LEAF_D = (52, 78, 46)
    HUT = (146, 118, 78)
    HUT_D = (96, 74, 48)
    out = []
    def L(x1, y1, x2, y2, c):
        out.append((x1, y1, x2, y2, c))

    # the hill it stands on: one brow line plus a couple of hachures
    hw = h * 0.95
    n = 16
    prev = None
    for k in range(n + 1):
        t = -1.0 + 2.0 * k / n
        x = cx + t * hw
        y = cy + h * 0.10 - (h * 0.26) * (1.0 - t * t)
        if prev:
            L(prev[0], prev[1], x, y, TRUNK_D)
        prev = (x, y)
    for t in (-0.62, -0.3, 0.3, 0.62):
        x = cx + t * hw
        y = cy + h * 0.10 - (h * 0.26) * (1.0 - t * t)
        L(x, y, x + h * 0.03, y + h * 0.07, TRUNK_D)

    # trunk
    L(cx - h * 0.045, cy, cx - h * 0.030, cy - h * 0.62, TRUNK)
    L(cx + h * 0.045, cy, cx + h * 0.030, cy - h * 0.62, TRUNK_D)
    L(cx - h * 0.045, cy, cx + h * 0.045, cy, TRUNK_D)
    # canopy: three lobes, drawn as arcs so it does not read as a solid blob
    for (ox, oy, rr) in ((-0.20, -0.66, 0.20), (0.20, -0.68, 0.19), (0.0, -0.78, 0.22)):
        bx, by = cx + ox * h, cy + oy * h
        r = rr * h
        m = 10
        for k in range(m):
            a0 = 2 * math.pi * k / m
            a1 = 2 * math.pi * (k + 1) / m
            L(bx + r * math.cos(a0), by + r * 0.72 * math.sin(a0),
              bx + r * math.cos(a1), by + r * 0.72 * math.sin(a1),
              LEAF if k % 3 else LEAF_D)
    # the hut on top: platform, walls, peaked roof
    py = cy - h * 0.92
    pw = h * 0.17
    L(cx - pw, py, cx + pw, py, HUT_D)                                  # platform
    L(cx - pw * 0.8, py, cx - pw * 0.8, py - h * 0.13, HUT)             # walls
    L(cx + pw * 0.8, py, cx + pw * 0.8, py - h * 0.13, HUT)
    L(cx - pw * 0.8, py - h * 0.13, cx + pw * 0.8, py - h * 0.13, HUT_D)
    L(cx - pw * 1.05, py - h * 0.13, cx, py - h * 0.25, HUT)            # roof
    L(cx + pw * 1.05, py - h * 0.13, cx, py - h * 0.25, HUT_D)
    L(cx - pw * 0.35, py, cx - pw * 0.35, py - h * 0.13, HUT_D)         # doorway
    L(cx + pw * 0.10, py, cx + pw * 0.10, py - h * 0.13, HUT_D)
    return out


def spiked_peak(cx, cy, w, h, seed=0):
    """A mountain that means it: one tall blade of rock thrown up steeply, with
    lesser spikes flanking it. For Mt. Hatespike -- a rounded mound reads as a
    hill, and the name is Hatespike.

    Steepness is the whole trick: the main face climbs at better than 70 degrees
    and the ridgeline is cut with notches rather than smoothed.
    """
    rng = random.Random(seed)
    ink = (92, 84, 88)
    dark = (58, 52, 58)
    lit = (140, 132, 134)
    out = []
    def L(x1, y1, x2, y2, c):
        out.append((x1, y1, x2, y2, c))

    foot = cy + h * 0.42
    apex = (cx + w * 0.02, foot - h)
    # left face -- steep, notched on the way up
    left = [(cx - w * 0.46, foot), (cx - w * 0.34, foot - h * 0.26),
            (cx - w * 0.30, foot - h * 0.22), (cx - w * 0.22, foot - h * 0.52),
            (cx - w * 0.17, foot - h * 0.48), (cx - w * 0.09, foot - h * 0.80),
            (cx - w * 0.05, foot - h * 0.76), apex]
    # right face -- steeper still, so the summit leans and looks unstable
    right = [apex, (cx + w * 0.07, foot - h * 0.72), (cx + w * 0.11, foot - h * 0.76),
             (cx + w * 0.17, foot - h * 0.40), (cx + w * 0.23, foot - h * 0.44),
             (cx + w * 0.32, foot - h * 0.14), (cx + w * 0.44, foot)]
    for seq in (left, right):
        for i in range(len(seq) - 1):
            L(*seq[i], *seq[i + 1], ink)
    # flanking spikes, lower and sharper
    for (bx, sc, side) in ((-w * 0.42, 0.42, -1), (w * 0.40, 0.34, 1)):
        base = cx + bx
        tip = (base + side * w * 0.05, foot - h * sc)
        L(base - w * 0.11, foot, tip[0], tip[1], dark)
        L(tip[0], tip[1], base + w * 0.12, foot, dark)
        L(base - w * 0.04, foot - h * sc * 0.42, base + w * 0.05, foot - h * sc * 0.36, dark)
    # fall-line hachures down the main faces -- shading, and they read as scree
    for t in range(1, 9):
        f = t / 9.0
        ax = apex[0] - w * 0.30 * f
        ay = apex[1] + h * 0.92 * f
        L(ax, ay, ax - w * 0.055, ay + h * 0.10, dark if t % 2 else ink)
        bx2 = apex[0] + w * 0.26 * f
        L(bx2, ay, bx2 + w * 0.050, ay + h * 0.09, dark if t % 2 else ink)
    # a lit edge on the summit blade so the apex reads sharp, not blunt
    L(apex[0], apex[1], apex[0] - w * 0.05, apex[1] + h * 0.16, lit)
    L(apex[0], apex[1], apex[0] + w * 0.04, apex[1] + h * 0.13, lit)
    # broken rubble at the foot instead of a ruled baseline
    x = cx - w * 0.50
    while x < cx + w * 0.50:
        d = rng.uniform(w * 0.02, w * 0.05)
        L(x, foot + rng.uniform(-h * 0.01, h * 0.02), x + d, foot + rng.uniform(-h * 0.01, h * 0.02), dark)
        x += d + rng.uniform(w * 0.01, w * 0.035)
    return out


def darkelf_castle(cx, cy, w, h, seed=0):
    """A small, mean teir'dal castle: narrow towers with barbed spires, a
    portcullis arch, and a curtain wall that leans. Drawn for Nektropos Castle
    off Nektulos' west edge.

    Everything is angular and slightly asymmetric -- a symmetrical keep with
    round towers reads as a friendly fairytale castle, which is the opposite of
    what this place is.
    """
    rng = random.Random(seed)
    STONE = (86, 74, 104)
    DEEP = (54, 44, 70)
    LIT = (128, 116, 150)
    GATE = (34, 28, 44)
    out = []
    def L(x1, y1, x2, y2, c):
        out.append((x1, y1, x2, y2, c))

    base = cy + h * 0.46
    # curtain wall with crenellations
    wl, wr = cx - w * 0.46, cx + w * 0.46
    wt = base - h * 0.34
    L(wl, base, wr, base, DEEP)
    L(wl, wt, wl, base, STONE)
    L(wr, wt, wr, base, STONE)
    L(wl, wt, wr, wt, STONE)
    x = wl
    k = 0
    while x < wr - w * 0.02:
        step = w * 0.075
        if k % 2 == 0:
            L(x, wt, x, wt - h * 0.06, STONE)
            L(x, wt - h * 0.06, min(x + step, wr), wt - h * 0.06, STONE)
            L(min(x + step, wr), wt - h * 0.06, min(x + step, wr), wt, STONE)
        x += step
        k += 1
    # three towers, unequal heights, each with a barbed spire
    for (ox, th, lean) in ((-0.36, 0.92, -0.05), (0.02, 1.16, 0.03), (0.34, 0.80, 0.06)):
        bx = cx + ox * w
        tw = w * 0.11
        top = base - h * th
        L(bx - tw, base, bx - tw + lean * w, top, STONE)
        L(bx + tw, base, bx + tw + lean * w, top, DEEP)
        L(bx - tw + lean * w, top, bx + tw + lean * w, top, STONE)
        for band in (0.34, 0.62):                       # storey lines
            by = base - h * th * band
            f = band
            L(bx - tw + lean * w * f, by, bx + tw + lean * w * f, by, DEEP)
        # barbed spire: a spike with two downward hooks
        sx = bx + lean * w
        spire = top - h * 0.30
        L(bx - tw + lean * w, top, sx, spire, STONE)
        L(bx + tw + lean * w, top, sx, spire, DEEP)
        hy = (top + spire) / 2                          # barbs SWEEP OUT from the
        L(sx - tw * 0.45, hy, sx - tw * 1.45, hy + h * 0.055, DEEP)   # spire, past its
        L(sx + tw * 0.45, hy, sx + tw * 1.45, hy + h * 0.055, DEEP)   # silhouette --
        L(sx - tw * 1.45, hy + h * 0.055, sx - tw * 1.05, hy + h * 0.02, DEEP)
        L(sx + tw * 1.45, hy + h * 0.055, sx + tw * 1.05, hy + h * 0.02, DEEP)
        L(sx, spire, sx, spire - h * 0.09, LIT)         # finial
        # a narrow lit window slit
        L(sx, base - h * th * 0.5, sx, base - h * th * 0.5 - h * 0.07, LIT)
    # portcullis arch in the curtain wall
    gw = w * 0.085
    L(cx - gw, base, cx - gw, base - h * 0.16, GATE)
    L(cx + gw, base, cx + gw, base - h * 0.16, GATE)
    m = 6
    for i in range(m):
        a0 = math.pi * i / m
        a1 = math.pi * (i + 1) / m
        L(cx + gw * math.cos(a0), base - h * 0.16 - gw * 0.9 * math.sin(a0),
          cx + gw * math.cos(a1), base - h * 0.16 - gw * 0.9 * math.sin(a1), GATE)
    for t in (-0.5, 0.0, 0.5):                          # bars
        L(cx + gw * t, base, cx + gw * t, base - h * 0.16, GATE)
    # a few rocks at the foot so it does not float
    x = cx - w * 0.52
    while x < cx + w * 0.52:
        d = rng.uniform(w * 0.02, w * 0.045)
        L(x, base + rng.uniform(0, h * 0.02), x + d, base + rng.uniform(0, h * 0.02), DEEP)
        x += d + rng.uniform(w * 0.015, w * 0.04)
    return out


def stone_pool(cx, cy, r, seed=0):
    """A hexagonal flagstone apron with a diamond pool set into the middle.
    From Brandon's shot beside Vhalen Nostrolo in South Karana -- a pool rather
    than a fountain: still water, no spout.
    """
    rng = random.Random(seed)
    FLAG = (146, 140, 128)
    FLAG_D = (104, 98, 90)
    WATER = (60, 104, 140)
    WATER_D = (40, 74, 108)
    RIM = (120, 96, 76)
    out = []
    def L(x1, y1, x2, y2, c):
        out.append((x1, y1, x2, y2, c))

    hexp = [(cx + r * math.cos(math.pi / 6 + k * math.pi / 3),
             cy + r * 0.72 * math.sin(math.pi / 6 + k * math.pi / 3)) for k in range(6)]
    for i in range(6):
        L(*hexp[i], *hexp[(i + 1) % 6], FLAG_D)
    # flagstone joints: a few chords across the apron, not a full grid
    for t in (-0.55, -0.2, 0.2, 0.55):
        L(cx - r * 0.86, cy + r * 0.72 * t, cx + r * 0.86, cy + r * 0.72 * t, FLAG)
    for t in (-0.5, 0.0, 0.5):
        L(cx + r * t, cy - r * 0.62, cx + r * t * 0.6, cy + r * 0.62, FLAG)
    # the diamond pool, rim then water
    dr = r * 0.42
    dia = [(cx, cy - dr * 0.86), (cx + dr, cy), (cx, cy + dr * 0.86), (cx - dr, cy)]
    for i in range(4):
        L(*dia[i], *dia[(i + 1) % 4], RIM)
    step = max(1.2, r * 0.05)
    y = cy - dr * 0.86 + step
    while y < cy + dr * 0.86 - step * 0.5:
        f = 1.0 - abs(y - cy) / (dr * 0.86)
        hwid = dr * f * 0.92
        if hwid > step * 0.4:
            L(cx - hwid, y, cx + hwid, y, WATER if int((y - cy) / step) % 3 else WATER_D)
        y += step
    return out


def petrified_stump(cx, cy, rx, ry, seed=0):
    """Growth rings and radial cracks, to be drawn OVER an existing rock blob.

    Butcherblock's scattered "blocks" are petrified ancient tree stumps (per
    Brandon), but the base drew each as a faceted polyhedral boulder. Facets
    are the problem: rings laid over them just read as more scribble, so the
    boulder wireframe is replaced rather than overdrawn.

    Draws the whole stump -- a rounded, slightly lobed bark edge, growth rings,
    radial cracks and a heartwood centre. rx, ry are the half-extents.
    """
    rng = random.Random(seed)
    RING = (120, 104, 84)
    CRACK = (70, 62, 52)
    HEART = (96, 84, 66)
    out = []

    def ring(fr, ink, jit, n=13):
        pts = []
        for k in range(n + 1):
            a = 2 * math.pi * k / n
            j = 1.0 + rng.uniform(-jit, jit)
            pts.append((cx + rx * fr * j * math.cos(a), cy + ry * fr * j * math.sin(a)))
        for i in range(n):
            out.append((pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], ink))

    # bark edge: lobed, and drawn twice just off-register so it reads as thick
    # At map scale a stump is barely 30px across, so this is deliberately
    # sparse: a bark edge and two rings. More rings merge into a dark blob,
    # which is exactly what the boulder wireframe did wrong.
    ring(1.00, CRACK, 0.10, n=15)
    for fr, jit in ((0.64, 0.08), (0.33, 0.06)):
        ring(fr, RING, jit)
    # radial cracks: start off-centre and run out through the rings
    for k in range(3):
        a = rng.uniform(0, 2 * math.pi)
        r0 = rng.uniform(0.10, 0.24)
        r1 = rng.uniform(0.72, 0.94)
        steps = 2
        px, py = cx + rx * r0 * math.cos(a), cy + ry * r0 * math.sin(a)
        for t in range(1, steps + 1):
            f = r0 + (r1 - r0) * t / steps
            aa = a + rng.uniform(-0.10, 0.10)
            nx, ny = cx + rx * f * math.cos(aa), cy + ry * f * math.sin(aa)
            out.append((px, py, nx, ny, CRACK))
            px, py = nx, ny
    out.append((cx - rx * 0.06, cy, cx + rx * 0.06, cy, HEART))      # heartwood
    out.append((cx, cy - ry * 0.06, cx, cy + ry * 0.06, HEART))
    return out


ROCK_SHADE = (80, 64, 46)
ROCK_SHADE_D = (58, 46, 34)


def rock_shade(points, seed=0, light=(-1.0, -1.0), density=1.0):
    """Hatch the shaded flank of an outcrop that is ALREADY drawn.

    Butcherblock's rock masses are good drawings; they just read flat. This
    adds form without redrawing them: rays are cast from the mass's centroid,
    the silhouette radius is measured along each, and short ticks are laid
    inside the edge on the flank facing away from the light. Because it only
    ever adds strokes inside the existing outline, it is append-only -- the
    base drawing is untouched.

    `points` is the outcrop's stroke-endpoint cloud [(x, y), ...].
    """
    import math as _m
    rng = random.Random(seed)
    if len(points) < 8:
        return []
    cx = sum(p[0] for p in points) / len(points)
    cy = sum(p[1] for p in points) / len(points)
    lx, ly = light
    n = _m.hypot(lx, ly) or 1.0
    lx, ly = lx / n, ly / n
    shade_dir = _m.atan2(-ly, -lx)          # the flank opposite the light
    out = []
    # bucket the cloud by angle so we can find the silhouette cheaply
    NB = 48
    rad = [0.0] * NB
    for px, py in points:
        dx, dy = px - cx, py - cy
        r = _m.hypot(dx, dy)
        b = int((_m.atan2(dy, dx) + _m.pi) / (2 * _m.pi) * NB) % NB
        if r > rad[b]:
            rad[b] = r
    span = _m.pi * 0.62                      # how much of the rim is in shadow
    steps = max(6, int(14 * density))
    for k in range(steps):
        a = shade_dir - span + (2 * span) * k / (steps - 1)
        b = int((a + _m.pi) / (2 * _m.pi) * NB) % NB
        r = max(rad[b], rad[(b - 1) % NB], rad[(b + 1) % NB])
        if r < 6:
            continue
        # a tick lying just inside the rim, plus a shorter inner one
        for f0, f1, ink in ((0.94, 0.66, ROCK_SHADE), (0.60, 0.40, ROCK_SHADE_D)):
            if f0 < 0.7 and rng.random() < 0.45:
                continue
            j = rng.uniform(-0.045, 0.045)
            aa = a + j
            out.append((cx + r * f0 * _m.cos(aa), cy + r * f0 * _m.sin(aa),
                        cx + r * f1 * _m.cos(aa), cy + r * f1 * _m.sin(aa), ink))
    return out
