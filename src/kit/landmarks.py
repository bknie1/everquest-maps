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
