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
