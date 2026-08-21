"""fauna_hd_human.py -- high-fidelity human guard/soldier for Qeynos, the Karanas,
Freeport, Highpass -- anywhere humans hold the ground.

Side-view standing guard built like the other HD fauna (closed part polygons,
even-odd hatched fill, a darker shadow side): upright and squared-off, a knee-
length tabard/surcoat over mail, a round pot-helm, a planted spear, and a round
shield on the near arm. Pass ink= to recolour for a faction (Qeynos slate,
Freeport brown). 100-240 strokes.

    from fauna_hd_human import human
    segs = human(cx, cy, s, seed=3)      # (cx, cy) = feet, s = height
    segs = human(cx, cy, s, face=1)      # face right
"""
import random

CLOTH = (78, 84, 110)        # qeynos slate-blue tabard (fauna PALETTE['qeynos'])
DARK = (52, 58, 82)          # shadow side
MAIL = (120, 120, 130)       # helm / mail
STEEL = (150, 150, 160)      # spearhead
WOOD = (120, 100, 72)        # spear shaft


def _hatch(poly, ink, step, jitter, rnd):
    ys = [p[1] for p in poly]
    out = []
    y = min(ys) + step * 0.5
    while y < max(ys):
        xs = []
        for i in range(len(poly)):
            (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % len(poly)]
            if (y1 > y) != (y2 > y):
                xs.append(x1 + (y - y1) * (x2 - x1) / (y2 - y1))
        xs.sort()
        for i in range(0, len(xs) - 1, 2):
            if xs[i + 1] - xs[i] > step * 0.4:
                w = rnd.uniform(-jitter, jitter)
                out.append((xs[i] + jitter * 0.3, y + w,
                            xs[i + 1] - jitter * 0.3, y + w, ink))
        y += step
    return out


def _outline(poly, ink, rnd, jitter):
    out = []
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        out.append((x1, y1 + rnd.uniform(-jitter, jitter),
                    x2, y2 + rnd.uniform(-jitter, jitter), ink))
    return out


def _part(poly, ink, dark, step, rnd, shade_from=None):
    j = step * 0.16
    out = _outline(poly, ink, rnd, j * 0.6)
    if shade_from is None:
        out += _hatch(poly, ink, step, j, rnd)
    else:
        lit = [(min(x, shade_from), y) for x, y in poly]
        shd = [(max(x, shade_from), y) for x, y in poly]
        out += _hatch(lit, ink, step, j, rnd)
        out += _hatch(shd, dark, step * 0.82, j, rnd)
    return out


def human(cx, cy, s, ink=None, seed=0, face=-1):
    """Side-view human guard. (cx, cy) = feet, s = full height. face=-1 left."""
    rnd = random.Random(seed)
    ink = ink or CLOTH
    dark = DARK
    f = face

    def P(pts):
        return [(cx + f * x * s, cy - y * s) for x, y in pts]

    def seg(x1, y1, x2, y2, c):
        out.append((cx + f * x1 * s, cy - y1 * s, cx + f * x2 * s, cy - y2 * s, c))

    step = s * 0.048
    out = []

    # rear leg (shadow) -- straight, boot
    rear_leg = P([(0.03, 0.42), (0.11, 0.42), (0.11, 0.22), (0.13, 0.02),
                  (0.05, 0.02), (0.04, 0.22), (-0.01, 0.40)])
    out += _part(rear_leg, dark, dark, step * 0.9, rnd)
    # front leg -- straight, boot forward
    front_leg = P([(-0.09, 0.44), (-0.01, 0.44), (-0.02, 0.22), (-0.05, 0.02),
                   (-0.14, 0.02), (-0.15, 0.00), (-0.03, 0.00), (0.00, 0.02),
                   (0.03, 0.22), (-0.03, 0.42)])
    out += _part(front_leg, ink, dark, step, rnd, shade_from=cx)

    # torso / tabard -- knee-length surcoat over the body, squared shoulders
    tabard = P([(-0.10, 0.40), (-0.13, 0.52), (-0.13, 0.66), (-0.10, 0.74),
                (-0.02, 0.78), (0.08, 0.76), (0.13, 0.66), (0.13, 0.52),
                (0.11, 0.40), (0.05, 0.44), (-0.02, 0.42), (-0.06, 0.44)])
    out += _part(tabard, ink, dark, step, rnd, shade_from=cx + f * s * 0.0)
    # belt + a heraldic bar down the tabard
    seg(-0.11, 0.52, 0.12, 0.53, dark)
    seg(-0.02, 0.72, -0.02, 0.44, MAIL)
    seg(-0.05, 0.58, 0.01, 0.58, MAIL)

    # rear arm (shadow) planting a spear
    rear_arm = P([(0.02, 0.72), (0.09, 0.68), (0.09, 0.54), (0.12, 0.42),
                  (0.07, 0.42), (0.04, 0.54), (-0.01, 0.68)])
    out += _part(rear_arm, dark, dark, step * 0.85, rnd)
    # spear -- planted, tall
    seg(0.09, 0.40, 0.06, 1.08, WOOD)
    seg(0.06, 1.08, 0.045, 1.18, STEEL)                  # spearhead
    seg(0.06, 1.08, 0.075, 1.18, STEEL)
    seg(0.045, 1.18, 0.075, 1.18, STEEL)

    # neck + head + pot-helm
    seg(-0.03, 0.78, -0.03, 0.82, ink)
    head = P([(-0.02, 0.82), (-0.08, 0.855), (-0.12, 0.85), (-0.14, 0.82),
              (-0.12, 0.795), (-0.05, 0.79), (-0.01, 0.80)])
    out += _part(head, ink, dark, step * 0.6, rnd)
    # pot-helm dome + nasal
    helm = P([(-0.02, 0.845), (-0.09, 0.875), (-0.13, 0.865), (-0.13, 0.845),
              (-0.02, 0.845)])
    out += _part(helm, MAIL, DARK, step * 0.55, rnd)
    seg(-0.125, 0.85, -0.13, 0.815, MAIL)                # nasal guard
    seg(-0.07, 0.83, -0.10, 0.826, dark)                 # eye slit

    # front arm holding a round shield across the body
    front_arm = P([(-0.06, 0.70), (-0.14, 0.64), (-0.15, 0.52), (-0.11, 0.48),
                   (-0.08, 0.52), (-0.09, 0.62), (-0.03, 0.66)])
    out += _part(front_arm, ink, dark, step * 0.85, rnd, shade_from=cx - f * s * 0.10)
    # round shield -- a disc with a boss and rim
    scx, scy, sr = cx - f * 0.16 * s, cy - 0.56 * s, s * 0.11
    N = 16
    ring = [(scx + sr * __import__("math").cos(t * 6.28318 / N),
             scy + sr * __import__("math").sin(t * 6.28318 / N)) for t in range(N + 1)]
    for i in range(N):
        out.append((*ring[i], *ring[i + 1], MAIL))
    out += _hatch([(x, y) for (x, y) in ring], ink, step * 0.9, step * 0.14, rnd)
    out.append((scx - sr * 0.3, scy, scx + sr * 0.3, scy, MAIL))   # boss cross
    out.append((scx, scy - sr * 0.3, scx, scy + sr * 0.3, MAIL))

    return out


if __name__ == "__main__":
    for sd in range(4):
        print("seed", sd, len(human(0, 0, 100, seed=sd)), "strokes")
