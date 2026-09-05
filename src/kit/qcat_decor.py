"""qcat_decor.py -- the gross stuff dripping through Qeynos Catacombs.

The catacombs' top margin is brick above and blank parchment below; this kit
fills the blank with what a sewer actually leaks: slime trickles running off
the brickwork, ooze puddles where they land, cracked outfall pipes, bone
litter, and fungus sprouting where the damp never dries. Rats, spiders and
bats come from fauna.py -- this module is only the filth itself.

    from qcat_decor import drip, puddle, pipe, bones, shroom
"""
import math
import random

OOZE = (96, 118, 58)          # fresh slime
OOZE_D = (66, 84, 44)         # dried / shaded slime
MURK = (84, 76, 60)           # sewage brown
BONE = (168, 158, 136)
STONE = (110, 100, 92)


def drip(cx, cy, h, seed=0):
    """A slime trickle running down from (cx, cy): a slow wobbling line that
    thins out and ends in a hanging droplet."""
    rng = random.Random(seed)
    out = []
    n = max(3, int(h / 9))
    x, y = cx, cy
    amp = h * rng.uniform(0.04, 0.09)
    for k in range(n):
        nx = cx + amp * math.sin((k + rng.random()) * 1.8)
        ny = cy + h * (k + 1) / n
        out.append((x, y, nx, ny, OOZE if k < n - 1 else OOZE_D))
        y_prev = y
        x, y = nx, ny
    r = h * 0.045 + 0.8                                # the droplet
    for i in range(6):
        a0, a1 = 2 * math.pi * i / 6, 2 * math.pi * (i + 1) / 6
        out.append((x + r * math.cos(a0), y + r + r * math.sin(a0),
                    x + r * math.cos(a1), y + r + r * math.sin(a1), OOZE))
    return out


def puddle(cx, cy, s, seed=0):
    """A lumpy ooze puddle: irregular closed blob, a dark inner rim on the
    shadow side, one small satellite splot."""
    rng = random.Random(seed)
    out = []
    n = 11
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        r = s * rng.uniform(0.62, 1.0)
        pts.append((cx + r * math.cos(a) * 1.45, cy + r * math.sin(a) * 0.5))
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]
        out.append((a[0], a[1], b[0], b[1], OOZE))
    for i in range(n // 2):                            # shaded south rim
        a, b = pts[i], pts[(i + 1) % n]
        out.append((a[0], a[1] + s * 0.08, b[0], b[1] + s * 0.08, OOZE_D))
    sa = rng.uniform(0, 2 * math.pi)                   # satellite splot
    sx, sy = cx + math.cos(sa) * s * 1.9, cy + math.sin(sa) * s * 0.5
    for i in range(5):
        a0, a1 = 2 * math.pi * i / 5, 2 * math.pi * (i + 1) / 5
        out.append((sx + s * 0.16 * math.cos(a0), sy + s * 0.10 * math.sin(a0),
                    sx + s * 0.16 * math.cos(a1), sy + s * 0.10 * math.sin(a1), OOZE_D))
    return out


def pipe(cx, cy, s, seed=0):
    """A cracked outfall stub jutting from the brickwork at (cx, cy), mouth
    down-right, sludge running over its lip."""
    out = []
    w, h = s * 0.9, s * 0.55
    # the stub: open-ended box with a rim
    out += [(cx - w, cy - h, cx + w * 0.7, cy - h, STONE),
            (cx - w, cy + h, cx + w * 0.7, cy + h, STONE),
            (cx + w * 0.7, cy - h * 1.25, cx + w * 0.7, cy + h * 1.25, STONE),
            (cx + w * 0.85, cy - h * 1.25, cx + w * 0.85, cy + h * 1.25, STONE),
            (cx + w * 0.7, cy - h * 1.25, cx + w * 0.85, cy - h * 1.25, STONE),
            (cx + w * 0.7, cy + h * 1.25, cx + w * 0.85, cy + h * 1.25, STONE)]
    out.append((cx - w * 0.3, cy - h, cx - w * 0.05, cy + h, STONE))   # crack
    out.append((cx - w * 0.05, cy + h, cx + w * 0.15, cy - h * 0.2, STONE))
    # sludge over the lip
    out += [(cx + w * 0.78, cy + h * 0.9, cx + w * 0.95, cy + h * 1.6, OOZE),
            (cx + w * 0.95, cy + h * 1.6, cx + w * 0.9, cy + h * 2.3, OOZE)]
    out += drip(cx + w * 0.9, cy + h * 2.3, s * 1.4, seed=seed + 1)
    return out


def bones(cx, cy, s, seed=0):
    """Bone litter: two crossed long bones with knuckle nubs, a few chips."""
    rng = random.Random(seed)
    out = []
    for k in (0, 1):
        a = rng.uniform(0.3, 1.2) + k * 1.5
        dx, dy = math.cos(a) * s, math.sin(a) * s * 0.55
        x1, y1, x2, y2 = cx - dx, cy - dy, cx + dx, cy + dy
        out.append((x1, y1, x2, y2, BONE))
        for (ex, ey, ux, uy) in ((x1, y1, -dy, dx), (x2, y2, -dy, dx)):
            n = s * 0.16 / max(math.hypot(ux, uy), 0.001)
            out.append((ex - ux * n, ey - uy * n, ex + ux * n, ey + uy * n, BONE))
    for _ in range(3):                                 # chips
        px = cx + rng.uniform(-s, s) * 1.4
        py = cy + rng.uniform(-s, s) * 0.5
        out.append((px, py, px + rng.uniform(2, 4), py + rng.uniform(-1, 1), BONE))
    return out


def shroom(cx, cy, s, seed=0):
    """A clump of pale sewer fungus: two or three capped stalks."""
    rng = random.Random(seed)
    out = []
    for k in range(rng.randint(2, 3)):
        x = cx + (k - 1) * s * 0.55 + rng.uniform(-1, 1)
        hh = s * rng.uniform(0.6, 1.0)
        w = hh * 0.62
        out.append((x, cy, x, cy - hh, OOZE_D))        # stalk
        out += [(x - w, cy - hh, x, cy - hh - w * 0.7, MURK),
                (x, cy - hh - w * 0.7, x + w, cy - hh, MURK),
                (x - w, cy - hh, x + w, cy - hh, MURK)]
    return out


KIT = {"drip": drip, "puddle": puddle, "pipe": pipe, "bones": bones, "shroom": shroom}

if __name__ == "__main__":
    for n, fn in KIT.items():
        print("%-7s %d strokes" % (n, len(fn(0, 0, 20, seed=1))))
