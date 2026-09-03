"""kedge_decor.py -- underwater margin motif for Kedge Keep.

Kedge's margins were 1,800 strokes of short horizontal dashes: dead texture,
no motif, and loud enough that the keep itself was hard to pick out. The zone
is a sunken keep, so the replacement is what you would actually see through the
water -- kelp, coral and rising bubbles.

Kept deliberately sparse and pale. The point of the margin here is to frame the
dungeon, not to compete with it.

    from kedge_decor import kelp, coral, bubbles
"""
import math
import random

KELP = (58, 106, 92)
KELP_D = (40, 78, 68)
CORAL = (132, 104, 104)
CORAL_D = (96, 74, 78)
BUBBLE = (128, 168, 182)


def kelp(cx, cy, h, seed=0):
    """A kelp stalk: one slow S-curve with blades hanging off alternate sides.
    Anchored at (cx, cy), growing upward (toward smaller y)."""
    rng = random.Random(seed)
    out = []
    n = 7
    amp = h * rng.uniform(0.06, 0.13)
    phase = rng.uniform(0, math.pi)
    pts = []
    for k in range(n + 1):
        t = k / n
        pts.append((cx + amp * math.sin(phase + t * 2.4), cy - h * t))
    for i in range(n):
        out.append((pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], KELP))
    for i in range(1, n):
        side = -1 if i % 2 else 1
        bx, by = pts[i]
        ln = h * rng.uniform(0.10, 0.19)
        tipx = bx + side * ln
        tipy = by - ln * 0.42
        out.append((bx, by, tipx, tipy, KELP))
        out.append((bx, by + h * 0.035, tipx, tipy + h * 0.02, KELP_D))
    return out


def coral(cx, cy, s, seed=0):
    """Branching coral: a short trunk that forks twice. Antler-shaped, so it
    reads as coral rather than as a bush."""
    rng = random.Random(seed)
    out = []

    def branch(x, y, ang, ln, depth):
        nx, ny = x + math.cos(ang) * ln, y - math.sin(ang) * ln
        out.append((x, y, nx, ny, CORAL if depth else CORAL_D))
        if depth < 2:
            for d in (-1, 1):
                branch(nx, ny, ang + d * rng.uniform(0.42, 0.72),
                       ln * rng.uniform(0.55, 0.72), depth + 1)

    branch(cx, cy, math.pi / 2 + rng.uniform(-0.25, 0.25), s * 0.42, 0)
    for k in range(3):                              # a few polyps at the base
        a = rng.uniform(0, math.pi)
        r = s * 0.07
        out.append((cx + math.cos(a) * r * 1.6, cy - abs(math.sin(a)) * r * 0.5,
                    cx + math.cos(a) * r * 2.1, cy - abs(math.sin(a)) * r * 0.8, CORAL_D))
    return out


def bubbles(cx, cy, s, seed=0):
    """A rising string of bubbles, drawn as small open rings that get larger
    and drift as they climb."""
    rng = random.Random(seed)
    out = []
    x, y = cx, cy
    for k in range(rng.randint(3, 5)):
        r = s * (0.05 + 0.035 * k)
        n = 7
        for i in range(n):
            a0 = 2 * math.pi * i / n
            a1 = 2 * math.pi * (i + 1) / n
            out.append((x + r * math.cos(a0), y + r * math.sin(a0),
                        x + r * math.cos(a1), y + r * math.sin(a1), BUBBLE))
        y -= s * (0.20 + 0.06 * k)
        x += rng.uniform(-s * 0.06, s * 0.06)
    return out


KIT = {"kelp": kelp, "coral": coral, "bubbles": bubbles}

if __name__ == "__main__":
    for n, fn in KIT.items():
        print("%-9s %d strokes" % (n, len(fn(0, 0, 100, seed=1))))
